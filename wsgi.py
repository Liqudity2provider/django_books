from app.rest.crud import BookAPI, EventList, BookList, Book, AuthorsAPI, Event, EventRegistration, \
    AuthorList, \
    User, UserList, Author
# from app.rest.calculations import DateFilter, CertainDateFilter, AverageSalary, TotalSalary
from app import app, api, db, create_app
from app.rest import crud
from app.views import view


"""Api endpoints"""

api.add_resource(BookAPI, '/api/books')
api.add_resource(BookList, '/books')
api.add_resource(Book, '/book/<int:book_id>')

api.add_resource(AuthorsAPI, '/api/authors')
api.add_resource(AuthorList, '/authors')
api.add_resource(Author, '/author/<int:author_id>')


api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserList, '/users')

api.add_resource(EventList, '/api/events')
api.add_resource(Event, '/api/event/<int:event_id>')
api.add_resource(EventRegistration, '/api/event_registration/')

if __name__ == '__main__':
    db.create_all(app=app)
    app.run()
