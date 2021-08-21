from base64 import b64encode
import jwt
import requests
from flask import request, jsonify
from flask_restful import Resource, reqparse
from sqlalchemy.exc import IntegrityError, OperationalError
import config
from app import db, app

# department_schema = DepartmentSchema()
# departments_schema = DepartmentSchema(many=True)
from app.models.models import UserSchema, EventModel, BookModel, AuthorModel, EventSchema, UserModel, AuthorSchema, \
    BookSchema
from app.rest.calculations import get_data_from_dict, user_from_request

user_schema = UserSchema()
users_schema = UserSchema(many=True)
event_schema = EventSchema()
events_schema = EventSchema(many=True)
author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)
book_schema = BookSchema()
books_schema = BookSchema(many=True)
DJ_PATH = 'http://127.0.0.1:8000/'


class AuthorList(Resource):
    """Read all authors;
    create new authors"""
    parser = reqparse.RequestParser()
    parser.add_argument('page')

    def get(self):
        """Get method to get all authors"""

        page = self.parser.parse_args().get('page')

        if not page or not page.isdigit():
            page = 1

        queryset = AuthorModel.query.paginate(page=page, per_page=2, error_out=False)

        return {
            'authors': authors_schema.dump(queryset.items)
        }

    def post(self):
        data = request.json
        try:
            author = AuthorModel(name=data.get("name"))
            db.session.add(author)
            db.session.commit()
            return {
                "message": "successful add new author",
                "data": author_schema.dump(author)
            }
        except OperationalError:
            return {"error": "Incorrect data entered"}
        except ValueError:
            return {"error": "Incorrect data entered"}


class Author(Resource):
    """Read, update and delete author"""

    def get(self, author_id):
        """Get method to list department"""

        author = AuthorModel.query.get(author_id)

        return {
            'author': book_schema.dump(author)
        }

    def put(self, author_id):
        """Put method for update department"""
        ...

    def delete(self, author_id):
        """Delete method for delete department"""
        ...


class AuthorsAPI(Resource):
    """Read all authors;
    create new authors"""
    parser = reqparse.RequestParser()
    parser.add_argument('page')

    def get(self):
        """Get method to get all authors"""

        page = self.parser.parse_args().get('page')

        if not page or not page.isdigit():
            page = 1

        api_response = requests.get(
            DJ_PATH + 'authors/api/',
            headers={},
            params={
                'page': page
            }
        )

        return {
            'authors': api_response.json()
        }

    def post(self):
        """Post method for create authors"""
        ...


class BookAPI(Resource):
    """Read all books;
    create new department"""
    parser = reqparse.RequestParser()
    parser.add_argument('page')

    def get(self):
        """Get method to list all books from django"""
        page = self.parser.parse_args().get('page')

        if not page or not page.isdigit():
            page = 1

        api_response = requests.get(
            DJ_PATH + 'books/api/',
            headers={},
            params={
                'page': page
            }
        )

        return {
            'books': api_response.json()
        }

    def post(self):
        """Post method to add new book"""
        ...


class BookList(Resource):
    """Read, update and delete book"""
    parser = reqparse.RequestParser()
    parser.add_argument('page')

    def get(self):
        """Get method to get all books"""

        page = self.parser.parse_args().get('page')

        if not page or not page.isdigit():
            page = 1

        queryset = BookModel.query.paginate(page=int(page), per_page=10, error_out=False)

        return {
            'books': books_schema.dump(queryset.items)
        }

    def post(self):
        """Post method for create book"""
        data = request.json
        try:
            book = BookModel(name=data.get("name"), author_id=int(data.get("author_id")))
            db.session.add(book)
            db.session.commit()
            return {
                       "message": "successful add new book"
                   }, 201
        except OperationalError:
            return {"error": "Incorrect data entered"}
        except ValueError:
            return {"error": "Incorrect data entered"}


class Book(Resource):
    """Read, update and delete book"""

    def get(self, book_id):
        """Get method to list book"""

        book = BookModel.query.get(book_id)

        return {
            'book': book_schema.dump(book)
        }

    def put(self, book_id):
        """Put method for update book"""
        ...

    def delete(self, book_id):
        """Delete method for delete book"""
        book = BookModel.query.get(book_id)
        db.session.delete(book)
        db.session.commit()
        return {
                   "message": "success delete"
               }, 204


class EventList(Resource):
    """Read all events;
    create new event
    """
    parser = reqparse.RequestParser()
    parser.add_argument('page')
    parser.add_argument('status')

    def get(self):
        """Get method for list all events
        You can add query params as 'status' to filter events by status"""
        page = self.parser.parse_args().get('page', 1)
        status = self.parser.parse_args().get('status')

        if status == 'will' or status == 'was' or status == 'now':
            queryset = EventModel.query.filter(EventModel.status == status).paginate(
                page=page, per_page=10, error_out=False
            ).items
        else:
            queryset = EventModel.query.paginate(page=page, per_page=10, error_out=False).items

        return {
            'events': events_schema.dump(queryset)
        }

    def post(self):
        """
        Post method to add new event
        Required:
            name:str
            date_start:date in timestamp format
            date_end:date in timestamp format
        Not required:
            description:str
            items:id of BookModel in list
            guests_users:id of UserModel in list
            guests_authors:id of AuthorModel in list
        """

        correct_data = get_data_from_dict(request.json)

        new_event = self.create_model_event_from_correct_data(correct_data)

        try:
            db.session.add(new_event)
            db.session.commit()
        except OperationalError:
            db.session.rollback()
            return {"error": "Incorrect value enter error"}
        except ValueError:
            return {"error": "Incorrect value enter error"}
        return event_schema.dump(new_event), 201

    @staticmethod
    def create_model_event_from_correct_data(_correct_data):
        new_event = EventModel(
            name=_correct_data['name'],
            date_start=_correct_data['date_start'],
            date_end=_correct_data['date_end'],
            status=_correct_data['status'],
            description=_correct_data['description'],
        )

        if _correct_data['items']:
            for item in _correct_data['items']:
                new_event.items.append(item)

        if _correct_data['guests_users']:
            for g_u in _correct_data['guests_users']:
                new_event.guests_users.append(g_u)

        if _correct_data['guests_authors']:
            for g_a in _correct_data['guests_authors']:
                new_event.guests_authors.append(g_a)
        return new_event


class Event(Resource):
    """Read, update and delete event"""

    def get(self, event_id):
        """Get method to get event"""

        event = EventModel.query.get_or_404(event_id)

        return {
            'event': event_schema.dump(event)
        }

    def put(self, event_id):
        """Put method for update event"""
        event = EventModel.query.get_or_404(event_id)
        try:
            data = get_data_from_dict(request.json)

            if data:
                event.custom_update(data)

            db.session.commit()

            return {
                       "event": event_schema.dump(event)
                   }, 200
        except OperationalError:
            return {"error": "Incorrect data entered"}
        except ValueError:
            return {"error": "Incorrect data entered"}

    def delete(self, event_id):
        """Delete method for delete event"""
        event = EventModel.query.get(event_id)
        db.session.delete(event)
        db.session.commit()
        return '', 204


class EventRegistration(Resource):
    """Read, update and delete your registration on the event"""
    parser = reqparse.RequestParser()
    parser.add_argument('event')

    def get(self, *args, **kwargs):
        """Get method to list event for user"""

        user = user_from_request(request)

        if user.events:
            res_list = []
            for ev in user.events:
                res_list.append({ev, ev.id})
            return {"message": f"you are registered for the event(s) {res_list},"
                               f"you can delete yourself from event "}
        return {}

    def put(self):
        """Put method for update event registration"""
        ...

    def delete(self, *args, **kwargs):
        """Delete method for delete event"""
        user = user_from_request(request)
        event_to_delete = self.parser.parse_args().get('event')

        if not event_to_delete or not event_to_delete.isdigit():
            return {"message": "enter id for event you want to delete"}

        event_to_delete = int(event_to_delete)

        if user and user.events:
            list_of_user_events_id = [ev.id for ev in user.events]
            if event_to_delete in list_of_user_events_id:
                user.events.remove(EventModel.query.get(event_to_delete))
                db.session.commit()

                return {"message": f"you deleted yourself from event {event_to_delete}"}

        return {}


class User(Resource):
    """Read, update and delete user"""

    def get(self, user_id):
        """Get method to list user"""

        user = UserModel.query.get_or_404(user_id)

        return {
            'event': user_schema.dump(user)
        }

    def put(self, user_id):
        """Put method for update user"""
        user = UserModel.query.get(user_id)

        data = request.json

        if data.get('event_id'):
            user.events = []
            for ev_id in data.get('event_id'):
                user.events.append(EventModel.query.get(ev_id))

            db.session.commit()

        return user_schema.dump(user)

    def delete(self, user_id):
        """Delete method for delete user"""

        user = UserModel.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204


class UserList(Resource):
    """Get User list or create a new user"""
    parser = reqparse.RequestParser()
    parser.add_argument('page')

    def get(self):
        """Get method to get all users"""

        page = self.parser.parse_args().get('page')
        if not page or not page.isdigit():
            page = 1

        queryset = UserModel.query.paginate(page=int(page), per_page=10, error_out=False).items

        return {
            'users': users_schema.dump(queryset)
        }

    def post(self):
        """Post method for create user"""

        new_user = UserModel(username=request.json.get("username"))
        db.session.add(new_user)
        db.session.commit()
        return {
            "new_user": user_schema.dump(new_user)
        }
