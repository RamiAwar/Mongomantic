# Mongomantic

<div align="center">

[![Build status](https://github.com/RamiAwar/mongomantic/workflows/build/badge.svg?branch=master&event=push)](https://github.com/RamiAwar/mongomantic/actions?query=workflow%3Abuild)
[![Python Version](https://img.shields.io/pypi/pyversions/mongomantic.svg)](https://pypi.org/project/mongomantic/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/RamiAwar/mongomantic/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/RamiAwar/mongomantic/blob/master/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%F0%9F%9A%80-semantic%20versions-informational.svg)](https://github.com/RamiAwar/mongomantic/releases)
[![License](https://img.shields.io/github/license/RamiAwar/mongomantic)](https://github.com/RamiAwar/mongomantic/blob/master/LICENSE)

A lightweight MongoDB ORM based on Pydantic and PyMongo, heavily inspired by Mongoengine.

</div>

## 🚀 TODO

[checkbox:unchecked] Documentation
[checkbox:checked] Basic API similar to mongoengine, without any queryset logic
[checkbox:checked] Built on Pydantic models, no other schema required
[checkbox:checked] BaseRepository responsible for all operations (instead of the model itself)
[checkbox:unchecked] ProductionRepository derived from BaseRepository with all errors handled
[checkbox:unchecked] Repository/model plugin framework (ex. SyncablePlugin, TimestampedPlugin, etc.)
[checkbox:unchecked] Wrapper for aggregation pipelines
[checkbox:checked] Mongomock tests
[checkbox:unchecked] Flexible connect() function wrapper around PyMongo client (aliases, replica sets, retry writes, etc.)
[checkbox:unchecked] Clean up imports and expose essentials in main file

## 🛡 License

[![License](https://img.shields.io/github/license/RamiAwar/mongomantic)](https://github.com/RamiAwar/mongomantic/blob/master/LICENSE)

This project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/RamiAwar/mongomantic/blob/master/LICENSE) for more details.

## 📃 Citation

```
@misc{mongomantic,
  author = {mongomantic},
  title = {A MongoDB Python ORM, built on Pydantic and PyMongo.},
  year = {2021},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/RamiAwar/mongomantic}}
}
```

## Credits

This project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template).
