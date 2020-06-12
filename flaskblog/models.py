from flaskblog import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    date_released = db.Column(db.String(20), nullable=False, default='4-April-2020')
    content = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    screenings = db.relationship('Screening', backref='nowshowing', lazy="joined")
    director = db.Column(db.String(100), nullable=False)
    cast = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    costs=db.relationship('Cost',backref='moviecost', lazy="joined")


    def __repr__(self):
        return f"Movie('{self.title}', '{self.date_released}','{self.content}', '{self.director}','{self.cast}', '{self.duration}','{self.genre}')"

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    def __repr__(self):
        return f"Admin('{self.username}', '{self.email}')"
class Screening(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    timing= db.Column(db.String(20), unique=True, nullable=False)
    reserves = db.relationship('Reserved', backref='screens', lazy="joined")

    def __repr__(self):
        return f"Screening('{self.movie_id}', '{self.timing}')"
class Seat(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    row=db.Column(db.Integer, nullable=False)
    column=db.Column(db.Integer, nullable=False)
    stype=db.Column(db.String(20), nullable=False)
    reserves = db.relationship('Reserved', backref='seatsgone', lazy="joined")
    costs=db.relationship('Cost',backref='seatcost', lazy="joined")

    def __repr__(self):
        return f"Seat('{self.row}', '{self.column}','{self.stype}', '{self.cost}')"

class Reserved(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    seat_id = db.Column(db.Integer, db.ForeignKey('seat.id'), nullable=False)
    screening_id = db.Column(db.Integer, db.ForeignKey('screening.id'), nullable=False)

    def __repr__(self):
        return f"Reserved('{self.id}', '{self.seat_id}', '{self.screening_id}')"

class Cost(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)    
    movie_name = db.Column(db.Integer, db.ForeignKey('movie.title'), nullable=False)
    seat_type=db.Column(db.String(20),db.ForeignKey('seat.stype'),nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f"Admin('{self.movie_name}', '{self.seat_type}','{self.cost}')"