![Logo](https://github.com/RamiAwar/mongomantic/raw/main/docs/assets/text_logo.png)

<p align='center'>
  <a href="https://github.com/RamiAwar/mongomantic/actions?query=workflow%3Abuild">
    <img src='https://github.com/RamiAwar/mongomantic/workflows/build/badge.svg?branch=main&event=push'>
  </a>
  
  <a href="https://ramiawar.github.io/Mongomantic">
    <img src='https://img.shields.io/badge/docs-passing-brightgreen'>
  </a>
  
  <a href="https://pypi.org/project/mongomantic/">
    <img src='https://img.shields.io/pypi/v/mongomantic?color=green'>
  </a>
</p>

<p align='center'>
  <a href="https://github.com/PyCQA/bandit">
    <img src='https://img.shields.io/badge/security-bandit-green.svg'>
  </a>
  
  <a href="https://github.com/RamiAwar/mongomantic/blob/main/LICENSE">
    <img src='https://img.shields.io/github/license/RamiAwar/mongomantic'>
  </a>
  
  <a href="https://github.com/RamiAwar/mongomantic/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot">
    <img src='https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg'>
  </a>
</p>
 
<p align='center'>
  <a href="https://github.com/RamiAwar/mongomantic/blob/master/.pre-commit-config.yaml">
    <img src='https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white'>
  </a>
  
  <a href="https://github.com/RamiAwar/mongomantic/releases">
    <img src='https://img.shields.io/badge/%F0%9F%9A%80-semantic%20versions-informational.svg'>
  </a>
</p>

<p align='center'>
  <a href="https://scrutinizer-ci.com/g/RamiAwar/Mongomantic/?branch=main">
  <img src='https://scrutinizer-ci.com/g/RamiAwar/Mongomantic/badges/quality-score.png?b=main'>
  </a>
  
  <a href="https://scrutinizer-ci.com/code-intelligence">
    <img src='https://scrutinizer-ci.com/g/RamiAwar/Mongomantic/badges/code-intelligence.svg?b=main'>
  </a>
  
  <a href="https://scrutinizer-ci.com/g/RamiAwar/Mongomantic/?branch=main">
    <img src='https://scrutinizer-ci.com/g/RamiAwar/Mongomantic/badges/coverage.png?b=main'>
  </a>
</p>

<br><br><br><br>

<p align="center">
    <em>Mongomantic = Pymongo + <a href="https://pydantic-docs.helpmanual.io/">Pydantic</a></em>
</p>

<p align="center">
  Mongomantic is a lightweight python MongoDB ORM based on Pydantic and PyMongo, heavily inspired by Mongoengine. 
</p>
  
## API

```python
from mongomantic import BaseRepository, MongoDBModel, connect

connect("localhost:27017", "test_db")  # Setup mongodb connection

class User(MongoDBModel):
    first_name: str
    last_name: str

class UserRepository(BaseRepository):

    class Meta:  # Required internal class
        model = User  # Define model type
        collection = "user"  # Define collection name


user = User(first_name="John", last_name="Smith")

user = UserRepository.save(user)  # PyMongo wrapping classmethods
user.id  # ObjectId that was saved

```

## Usage

```
pip install mongomantic
```

To connect to your database, a connect function similar to mongoengine is provided.

```
from mongomantic import connect

connect("localhost:27017", "test_db")  # Setup mongodb connection
```

For production use, you can either handle the errors thrown by BaseRepository in case of errors on your own, or you can use SafeRepository which handles all the errors for you and logs them, while returning meaningful safe values like `None` and `[]`. Usage is exactly similar to using BaseRepository.

```python
from mongomantic import SafeRepository, MongoDBModel, connect

connect("localhost:27017", "test_db")  # Setup mongodb connection

class User(MongoDBModel):
    first_name: str
    last_name: str

class UserRepository(SafeRepository):

    class Meta:  # Required internal class
        model = User  # Define model type
        collection = "user"  # Define collection name

user = UserRepository.get(id="123")  # DoesNotExist error handled

assert user is None

```

Similar to this example, all other errors are handled.

## Your Opinion is Needed

Mongomantic can be kept as a simple wrapper around PyMongo, or developed into a miniature version of Mongoengine that's built on Pydantic.
The first direction would result in the following API:

```
# Direct pymongo wrapper
users = UserRepository.find({"$and": [{"age": {"$gt": 12}}, {"name": "John"}]})

# But matches can be done as keyword arguments
john = UserRepository.find(name="John")
```

On the other hand, a more complex version of Mongomantic could lead to:

```
# More Pythonic way of writing queries
users = UserRepository.find(User.age > 12, name="John")

# Matches still compact
john = UserRepository.find(name="John")
```

Please submit your vote below.

<p><a href="https://api.gh-polls.com/poll/01F2Y55FJSGXFMJW97Z143C6E0/Simple%20PyMongo%20Wrapper%20-%20Prefer%20speed%20and%20native%20mongodb%20filters/vote"><img src="https://api.gh-polls.com/poll/01F2Y55FJSGXFMJW97Z143C6E0/Simple%20PyMongo%20Wrapper%20-%20Prefer%20speed%20and%20native%20mongodb%20filters" alt="">Simple PyMongo Wrapper - Prefer speed and native mongodb filters</a>
<a href="https://api.gh-polls.com/poll/01F2Y55FJSGXFMJW97Z143C6E0/More%20Complex%20Wrapper%20-%20Pythonic%20filters/vote"><img src="https://api.gh-polls.com/poll/01F2Y55FJSGXFMJW97Z143C6E0/More%20Complex%20Wrapper%20-%20Pythonic%20filters" alt="">More Complex Wrapper - Pythonic Filters</a></p>

## 🚀 TODO

- [ ] Documentation
- [x] Basic API similar to mongoengine, without any queryset logic
- [x] Built on Pydantic models, no other schema required
- [x] BaseRepository responsible for all operations (instead of the model itself)
- [x] SafeRepository derived from BaseRepository with all errors handled
- [ ] Repository/model plugin framework (ex. SyncablePlugin, TimestampedPlugin, etc.)
- [x] Wrapper for aggregation pipelines
- [x] Mongomock tests
- [x] Flexible connect() function wrapper around PyMongo client (aliases, replica sets, retry writes, etc.)
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
