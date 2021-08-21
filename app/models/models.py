from datetime import datetime

from sqlalchemy.orm import relationship, backref

from app import db, ma
from app.models.custom_utils_for_models import ChoiceType


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(200), nullable=True)

    events = relationship("EventModel", secondary="table_user_guests")

    def __repr__(self):
        """Use when call in print() function"""
        return self.username


class EventModel(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True)
    date_start = db.Column(db.DateTime, nullable=True)
    date_end = db.Column(db.DateTime, nullable=True)
    description = db.Column(db.String(200), nullable=True)
    status = db.Column(
        ChoiceType({"was": "was", "now": "now", "will": "will"}), nullable=False
    )

    items = relationship("BookModel", secondary="table_event_items")
    guests_users = relationship("UserModel", secondary="table_user_guests")
    guests_authors = relationship("AuthorModel", secondary="table_author_guests")

    def __repr__(self):
        return self.name

    def custom_update(self, _data):
        if "name" in _data:
            self.name = _data["name"]
        if "date_start" in _data:
            self.date_start = _data["date_start"]
        if "date_end" in _data:
            self.date_end = _data["date_end"]
        if "status" in _data:
            self.status = _data["status"]
        if "description" in _data:
            self.description = _data["description"]

        if "items" in _data:
            self.items = []
            for item in _data['items']:
                self.items.append(item)

        if "guests_users" in _data:
            self.guests_users = []
            for g_u in _data['guests_users']:
                self.guests_users.append(g_u)

        if "guests_authors" in _data:
            self.guests_authors = []
            for g_a in _data['guests_authors']:
                self.guests_authors.append(g_a)

        return self


class BookModel(db.Model):
    """Create Book table"""
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True)

    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    events = relationship("EventModel", secondary="table_event_items")

    def __repr__(self):
        """Use when call in print() function"""
        return self.name


class AuthorModel(db.Model):
    """Create Author table"""
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True)

    books = relationship("BookModel")
    events = relationship("EventModel", secondary="table_author_guests")

    def __repr__(self):
        """Use when call in print() function"""
        return self.name


class UserGuests(db.Model):
    __tablename__ = 'table_user_guests'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    user = relationship(UserModel, backref=backref("event_guests", cascade="all, delete-orphan"))
    event = relationship(EventModel, backref=backref("user_guests", cascade="all, delete-orphan"))


class EventItems(db.Model):
    __tablename__ = 'table_event_items'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    book = relationship(BookModel, backref=backref("event_items", cascade="all, delete-orphan"))
    event = relationship(EventModel, backref=backref("event_items", cascade="all, delete-orphan"))


class AuthorGuests(db.Model):
    __tablename__ = 'table_author_guests'
    id = db.Column(db.Integer, primary_key=True)

    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    author = relationship(AuthorModel, backref=backref("event_authors", cascade="all, delete-orphan"))
    event = relationship(EventModel, backref=backref("author_guests", cascade="all, delete-orphan"))


class UserSchema(ma.SQLAlchemyAutoSchema):
    """Generate marshmallow schema for user model"""

    class Meta:
        model = UserModel

    events = ma.auto_field()


class BookSchema(ma.SQLAlchemyAutoSchema):
    """Generate marshmallow schema for book model"""

    class Meta:
        model = BookModel

    id = ma.auto_field()
    name = ma.auto_field()
    author_id = ma.auto_field()
    events = ma.auto_field()


class AuthorSchema(ma.SQLAlchemyAutoSchema):
    """Generate marshmallow schema for author model"""

    class Meta:
        model = AuthorModel
        include_fk = True

    books = ma.auto_field()
    events = ma.auto_field()


class EventSchema(ma.SQLAlchemyAutoSchema):
    """Generate marshmallow schema for Event model"""

    class Meta:
        model = EventModel

    items = ma.auto_field()
    guests_users = ma.auto_field()
    guests_authors = ma.auto_field()
