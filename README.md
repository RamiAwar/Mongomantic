![Logo](https://github.com/RamiAwar/mongomantic/blob/main/docs/assets/text_logo.png)

<p align="center">
    <em>Mongomantic = Pymongo + <a href="https://pydantic-docs.helpmanual.io/">Pydantic</a></em>
</p>
<p>Mongomantic is an easy-to-use, easy-to-learn wrapper around PyMongo, built around <a href="https://pydantic-docs.helpmanual.io/">Pydantic</a> models.</p>

<div align="center">

[![Build status](https://github.com/RamiAwar/mongomantic/workflows/build/badge.svg?branch=main&event=push)](https://github.com/RamiAwar/mongomantic/actions?query=workflow%3Abuild)

<!-- [![Python Version](https://img.shields.io/pypi/pyversions/mongomantic.svg)](https://pypi.org/project/mongomantic/)-->

[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/RamiAwar/mongomantic/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/RamiAwar/mongomantic/blob/master/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%F0%9F%9A%80-semantic%20versions-informational.svg)](https://github.com/RamiAwar/mongomantic/releases)
[![License](https://img.shields.io/github/license/RamiAwar/mongomantic)](https://github.com/RamiAwar/mongomantic/blob/main/LICENSE)

A lightweight MongoDB ORM based on Pydantic and PyMongo, heavily inspired by Mongoengine.

</div>

## API

```python
from mongomantic import BaseRepository, MongoDBModel


class User(MongoDBModel):
    first_name: str
    last_name: str

class UserRepository(BaseRepository):
    @property
    def _model(self):  # Define model type
        return User

    @property
    def _collection(self):  # Define collection name
        return "user"

user = User(first_name="John", last_name="Smith")
user_repo = UserRepository()

user = user_repo.save(user)
user.id  # ObjectId that was saved

```

## Your Opinion is Needed

Mongomantic can be kept as a simple wrapper around PyMongo, or developed into a miniature version of Mongoengine that's built on Pydantic.
The first direction would result in the following API:

```
# Direct pymongo wrapper
users = user_repo.find({"$and": [{"age": {"$gt": 12}}, {"name": "John"}]})

# But matches can be done as keyword arguments
john = user_repo.find(name="John")
```

On the other hand, a more complex version of Mongomantic could lead to:

```
# More Pythonic way of writing queries
users = user_repo.find(User.age > 12, name="John")

# Matches still compact
john = user_repo.find(name="John")
```

Please submit your vote below.

<p><a href="https://api.gh-polls.com/poll/01F2Y55FJSGXFMJW97Z143C6E0/Simple%20PyMongo%20Wrapper%20-%20Prefer%20speed%20and%20native%20mongodb%20filters/vote"><img src="https://api.gh-polls.com/poll/01F2Y55FJSGXFMJW97Z143C6E0/Simple%20PyMongo%20Wrapper%20-%20Prefer%20speed%20and%20native%20mongodb%20filters" alt="">Simple PyMongo Wrapper - Prefer speed and native mongodb filters</a>
<a href="https://api.gh-polls.com/poll/01F2Y55FJSGXFMJW97Z143C6E0/More%20Complex%20Wrapper%20-%20Pythonic%20filters/vote"><img src="https://api.gh-polls.com/poll/01F2Y55FJSGXFMJW97Z143C6E0/More%20Complex%20Wrapper%20-%20Pythonic%20filters" alt="">More Complex Wrapper - Pythonic Filters</a></p>


## 🚀 TODO

- [ ] Documentation
- [x] Basic API similar to mongoengine, without any queryset logic
- [x] Built on Pydantic models, no other schema required
- [x] BaseRepository responsible for all operations (instead of the model itself)
- [ ] ProductionRepository derived from BaseRepository with all errors handled
- [ ] Repository/model plugin framework (ex. SyncablePlugin, TimestampedPlugin, etc.)
- [ ] Wrapper for aggregation pipelines
- [x] Mongomock tests
- [ ] Flexible connect() function wrapper around PyMongo client (aliases, replica sets, retry writes, etc.)
- [ ] Clean up imports and expose essentials in main file

## 🛡 License

[![License](https://img.shields.io/github/license/RamiAwar/mongomantic)](https://github.com/RamiAwar/mongomantic/blob/main/LICENSE)

This project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/RamiAwar/mongomantic/blob/main/LICENSE) for more details.

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
