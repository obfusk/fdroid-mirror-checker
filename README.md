<!-- SPDX-FileCopyrightText: 2023 FC Stegerman <flx@obfusk.net> -->
<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->

[![CI](https://github.com/obfusk/fdroid-mirror-checker/workflows/CI/badge.svg)](https://github.com/obfusk/fdroid-mirror-checker/actions?query=workflow%3ACI)
[![AGPLv3+](https://img.shields.io/badge/license-AGPLv3+-blue.svg)](https://www.gnu.org/licenses/agpl-3.0.html)

# fdroid-mirror-checker

check f-droid mirrors

```sh
$ SERVER=localhost:5000 MIRROR=https://ftp.fau.de/fdroid
$ curl "$SERVER/latest-apk/org.fdroid.fdroid?mirror=$MIRROR"
{"status": "up-to-date"}
$ curl "$SERVER/timestamp?mirror=$MIRROR"
{"status": "up-to-date"}
$ curl "$SERVER/timestamp?mirror=$MIRROR&component=archive"
{"status": "up-to-date"}
```

## Uptime Kuma (ansible)

<details>

```yaml
- name: "apt: ensure required packages are installed"
  ansible.builtin.apt:
    install_recommends: no
    name: "{{ item }}"
  with_items:
    - gunicorn
    - python3-flask
    - python3-requests

- name: "git: clone fdroid-mirror-checker"
  ansible.builtin.git:
    repo: https://github.com/obfusk/fdroid-mirror-checker.git
    dest: /opt/fdroid-mirror-checker
    version: <sha1>

- name: "symlink fdroid-mirror-checker.service"
  ansible.builtin.file:
    src: /opt/fdroid-mirror-checker/fdroid-mirror-checker.service
    dest: /etc/systemd/system/fdroid-mirror-checker.service
    owner: root
    group: root
    state: link

- name: "systemd: enable & start fdroid-mirror-checker"
  ansible.builtin.systemd:
    name: fdroid-mirror-checker
    state: started
    enabled: true
```

```yaml
- name: "monitor: ..."
  lucasheld.uptime_kuma.monitor:
    url: "http://host.docker.internal:8888/timestamp?mirror={{ item.base_url }}"
    type: "http"
    ...

- name: "monitor: ..."
  lucasheld.uptime_kuma.monitor:
    url: "http://host.docker.internal:8888/timestamp?mirror={{ item.base_url }}&component=archive"
    type: "http"
    ...

- name: "monitor: ..."
  lucasheld.uptime_kuma.monitor:
    url: "http://host.docker.internal:8888/latest-apk/{{ item.appid }}?mirror={{ item.base_url }}"
    type: "http"
    ...
```

</details>

## License

[![AGPLv3+](https://www.gnu.org/graphics/agplv3-155x51.png)](https://www.gnu.org/licenses/agpl-3.0.html)

<!-- vim: set tw=70 sw=2 sts=2 et fdm=marker : -->
