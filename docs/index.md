# Mongomantic

![Logo](assets/text_logo.png){ align=center }

<p align="center">
    <em>Mongomantic = Pymongo + <a href="https://pydantic-docs.helpmanual.io/">Pydantic</a></em>
</p>
<p>Mongomantic is an easy-to-use, easy-to-learn wrapper around PyMongo, built around <a href="https://pydantic-docs.helpmanual.io/">Pydantic</a> models.</p>

## Why?

Pymongo offers a very raw set of CRUD operations, and is not an <a href="https://blog.bitsrc.io/what-is-an-orm-and-why-you-should-use-it-b2b6f75f5e2a">Object Relational Mapper</a>.

Other ORMs like Mongoengine (which Mongomantic is inspired heavily by) require their own schema definition.
This means that if you want to use Pydantic's data validation along with an ORM like Mongoengine, you would have to
write two schemas, along with handling the conversion back and forth.

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
- [ ] ProductionRepository derived from BaseRepository with all possible errors handled as an example for production use
- [ ] Repository/model plugin framework (ex. SyncablePlugin, TimestampedPlugin, etc.)
- [x] Mongomock tests
