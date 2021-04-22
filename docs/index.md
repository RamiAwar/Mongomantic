# Mongomantic

![Logo](assets/text_logo.png){ align=center }

<p align="center">
    <em>Mongomantic = Pymongo + <a href="https://pydantic-docs.helpmanual.io/">Pydantic</a></em>
</p>
<p>Mongomantic is an easy-to-use, easy-to-learn wrapper around PyMongo, built around <a href="https://pydantic-docs.helpmanual.io/">Pydantic</a> models.</p>

## Why?

Pymongo offers a very raw set of CRUD operations, and is not an <a href="https://blog.bitsrc.io/what-is-an-orm-and-why-you-should-use-it-b2b6f75f5e2a">Object Relational Mapper</a>.

Other ORMs like Mongoengine (which Mongomantic is inspired heavily by) require their own schema definition.
This means that if you want to use Pydantic's data validation along with an ORM like Mongoengine, you would have to write two schemas, along with handling your model conversion back and forth.

Mongomantic just requires a pydantic model.

## How?

Basic CRUD operations are exposed through a base repository that can be subclassed.
This is an fully functioning example of how Mongomantic would be used:

```python hl_lines="5 9 11 18"
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

And that is all you have to do to get a functional ORM with built-in data validation using ONLY python type annotations!

## Features

- [ ] Documentation
- [x] Basic API similar to mongoengine, without any queryset logic
- [x] Built on <a href="https://pydantic-docs.helpmanual.io/">Pydantic models</a> which allows for data validation with type annotations
- [x] BaseRepository class supports all CRUD operations and MongoDB aggregation framework
- [x] SafeRepository derived from BaseRepository with all possible errors handled as an example for production use
- [ ] Repository/model plugin framework (ex. SyncablePlugin, TimestampedPlugin, etc.)
- [x] Mongomock tests

## Usage

```
pip install mongomantic
```

### Connection to MongoDB

To connect to your database, a connect function similar to mongoengine is provided.

```
from mongomantic import connect

connect("localhost:27017", "test_db")  # Setup mongodb connection
```

### Repository Usage

The BaseRepository class wraps around MongoDBModel, providing functions to save models into a collection, retrieve models, create indexes, and use the aggregation pipeline syntax on the collection.

To implement a new repository, you must first inherit from BaseRepository and provide an internal Meta class to specify the model and collection being used.

```python hl_lines="3 4"
class UserRepository(BaseRepository):
    class Meta:
        model = User
        collection = "user"
```

And that's it! You can now access repository CRUD operations and more. More details found in the [Repositories](repository.md) guide.

Adding indexes is simple using the Mongomantic Index model:

```python hl_lines="2"
class UserRepository(BaseRepository):
    class Meta:
        model = User
        collection = "user"
        indexes = [
            Index(fields=["+first_name"]),
            Index(fields=["+first_name", "-last_name"], unique=True)
        ]
```

### Safe Repository

For production use, you can either handle the errors thrown by BaseRepository in case of errors on your own (recommended), or you can use SafeRepository which handles all the errors for you and logs them (very defensive), while returning meaningful safe values like `None` and `[]`. Usage is exactly similar to using BaseRepository.

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
