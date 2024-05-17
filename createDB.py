from app import db, app
from Model import Book
from Model import User

if __name__=="__main__":
    with app.app_context():
        db.create_all()
        #db.session.commit()
        db.session.add(User(username="admin", password="admin", is_admin=True))
        db.session.add(User(username="a", password="a", is_admin=True))
        db.session.add(User(username="u3", password="p3", is_admin=False))
        db.session.add(User(username="u4", password="p4", is_admin=False))
        db.session.add(User(username="u5", password="p5", is_admin=False))

        db.session.add(Book(title="b1", rating=3.4, user_id=3))
        db.session.add(Book(title="b2", rating=3.1, user_id=3))
        db.session.add(Book(title="b3", rating=3.6, user_id=3))
        db.session.add(Book(title="b4", rating=3.2, user_id=4))
        db.session.add(Book(title="b5", rating=3.1, user_id=4))
        db.session.add(Book(title="b6", rating=3.2, user_id=4))
        db.session.add(Book(title="b7", rating=3.2, user_id=4))
        db.session.add(Book(title="b8", rating=3.9, user_id=5))
        db.session.add(Book(title="b9", rating=3.9, user_id=5))
        db.session.add(Book(title="b10", rating=3.2, user_id=5))
        db.session.add(Book(title="b11", rating=3.1, user_id=5))
        db.session.add(Book(title="b12", rating=2, user_id=5))
        db.session.add(Book(title="b13", rating=5, user_id=5))

        db.session.commit()

        #flask db migrate
