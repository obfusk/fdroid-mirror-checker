#!/usr/bin/python3
# SPDX-FileCopyrightText: 2023 FC Stegerman <flx@obfusk.net>
# SPDX-License-Identifier: AGPL-3.0-or-later

import time

from typing import Any, Dict, Tuple

import requests

from flask import Flask, abort, jsonify, request

FDROID = "https://f-droid.org"
TIMEOUT = 5
TTL = 600

app = Flask(__name__)
cache: Dict[Any, Tuple[Any, Any]] = {}


def cached(f: Any) -> Any:
    def g(*args: Any) -> Any:
        k = (f.__name__,) + args
        t = time.time()
        if k in cache and t - cache[k][0] < TTL:
            return cache[k][1]
        result = f(*args)
        cache[k] = (t, result)
        return result
    return g


@cached
def timestamp(mirror: str, component: str) -> int:
    r = requests.get(f"{mirror}/{component}/entry.json", timeout=TIMEOUT)
    r.raise_for_status()
    ts: int = r.json()["timestamp"]
    return ts // 1000


@cached
def latest_apk(appid: str) -> str:
    r = requests.get(f"{FDROID}/api/v1/packages/{appid}", timeout=TIMEOUT)
    r.raise_for_status()
    version = r.json()["suggestedVersionCode"]
    return f"{appid}_{version}.apk"


def mirror_uptodate(mirror: str, component: str) -> bool:
    fdroid_ts = timestamp(FDROID, component)
    mirror_ts = timestamp(mirror, component)
    app.logger.info(f"f-droid [{component}] timestamp = {fdroid_ts}")
    app.logger.info(f"{mirror} [{component}] timestamp = {mirror_ts}")
    return bool(mirror_ts == fdroid_ts)


def mirror_has_apk(mirror: str, appid: str) -> bool:
    apk = latest_apk(appid)
    r = requests.head(f"{mirror}/repo/{apk}", timeout=TIMEOUT)
    app.logger.info(f"{mirror} [{apk}] status = {r.status_code}")
    return r.status_code == 200


def mirror_component() -> Tuple[str, str]:
    try:
        mirror = request.args["mirror"]
        component = request.args.get("component", "repo")
    except KeyError:
        abort(400)
    if component not in ("repo", "archive"):
        abort(400)
    return mirror, component


def handler(f: Any, fail_status: str, ok_status: str = "up-to-date") -> Any:
    try:
        if not f():
            resp = jsonify({"status": fail_status})
            resp.status_code = 400
            return resp
    except requests.RequestException as e:
        app.logger.error(f"requests exception: {e}")
        error = {"status": "error"}
        if (r := getattr(e, "response", None)) is not None:
            error["url"] = r.url
            error["status_code"] = r.status_code
        resp = jsonify(error)
        resp.status_code = 500
        return resp
    return jsonify({"status": ok_status})


@app.route("/latest-apk/<appid>")
def r_latest_apk(appid: str) -> Any:
    mirror, _ = mirror_component()
    return handler(lambda: mirror_has_apk(mirror, appid), "missing")


@app.route("/timestamp")
def r_timestamp() -> Any:
    mirror, component = mirror_component()
    return handler(lambda: mirror_uptodate(mirror, component), "outdated")
