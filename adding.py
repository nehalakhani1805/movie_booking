from flaskblog import db
from flaskblog.models import Seat, Admin, User, Movie, Screening, Reserved, Cost
st=""
for i in range(1,11):
	for j in range (1,21):
		if(i>=1 and i<=2):
			st="Recliner"
		elif(i>2 and i<=8):
			st="Premium"
		else:
			st="Classic"
		seat=Seat(row=i,column=j,stype=st)
		db.session.add(seat)
		db.session.commit()

a=Admin(username="Neha",email="neha@gmail.com",password="neha")
a2=Admin(username="Anas",email="anas@gmail.com",password="anas")
a3=Admin(username="Harshita",email="harshita@gmail.com",password="harshita")
db.session.add(a)
db.session.add(a2)
db.session.add(a3)
db.session.commit()

m1=Movie(title="Inception",content="A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
	director="Christopher Nolan",cast="Leonardo DiCaprio, Joseph Gordon-Levitt, Ellen Page",duration=148,genre="Thriller, Mystery")
m2=Movie(title="The Sixth Sense",content="A boy who communicates with spirits seeks the help of a disheartened child psychologist.",
	     director="M. Night Shyamalan", cast=" Bruce Willis, Haley Joel Osment, Toni Collette", duration=107,genre="Thriller, Mystery")
db.session.add(m1)
db.session.add(m2)
db.session.commit()

s1=Screening(movie_id=1,timing="9:30")
s2=Screening(movie_id=2,timing="12:30")
s3=Screening(movie_id=1,timing="15:30")
s4=Screening(movie_id=2,timing="18:30")
db.session.add(s1)
db.session.add(s2)
db.session.add(s3)
db.session.add(s4)
db.session.commit()

u=User(username="User1",email="user1@gmail.com",password="user1")
u2=User(username="Neha",email="neha@gmail.com",password="neha")
u3=User(username="Anas",email="anas@gmail.com",password="anas")
u4=User(username="Harshita",email="harshita@gmail.com",password="harshita")
db.session.add(u2)
db.session.add(u3)
db.session.add(u4)
db.session.add(u)
db.session.commit()

c1=Cost(movie_name="Inception",seat_type="Recliner",cost=200)
c2=Cost(movie_name="Inception",seat_type="Premium",cost=150)
c3=Cost(movie_name="Inception",seat_type="Classic",cost=100)
db.session.add(c1)
db.session.add(c2)
db.session.add(c3)
db.session.commit()

c4=Cost(movie_name="The Sixth Sense",seat_type="Recliner",cost=200)
c5=Cost(movie_name="The Sixth Sense",seat_type="Premium",cost=150)
c6=Cost(movie_name="The Sixth Sense",seat_type="Classic",cost=100)
db.session.add(c4)
db.session.add(c5)
db.session.add(c6)
db.session.commit()