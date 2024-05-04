from main import db, app
from Model import Book

if __name__=="__main__":
    with app.app_context():
        db.create_all()
        #db.session.commit()
        db.session.add(Book(title="asda", rating=3))
        db.session.commit()

        #flask db migrate
