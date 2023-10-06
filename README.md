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

## License

[![AGPLv3+](https://www.gnu.org/graphics/agplv3-155x51.png)](https://www.gnu.org/licenses/agpl-3.0.html)

<!-- vim: set tw=70 sw=2 sts=2 et fdm=marker : -->
