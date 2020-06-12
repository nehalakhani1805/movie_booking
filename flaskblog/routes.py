from flask import render_template, url_for, flash, redirect,request,jsonify
from flaskblog.forms import RegistrationForm, LoginForm, AddShowForm, DeleteShowForm, UpdateShowForm, DeleteMovieForm, AddMovieForm
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from flaskblog.models import User, Admin, Movie, Seat, Screening, Reserved, Cost
from flaskblog import app, db, bcrypt, csrf
from flask_login import login_user, current_user, logout_user, login_required
import json
from flaskblog.add_movie import add 
show=None

@app.route('/')
@app.route('/home')
def home():
    movies=Movie.query.all()
    return render_template('home.html', movies=movies)

@app.route('/about')
def about():
  return render_template('about.html',title='About')	

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password==form.password.data:
            login_user(user)#, remember=form.remember.data)
            next_page = request.args.get('next')
            #flash('Login successful!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

class TicketForm(FlaskForm):
    #timing=StringField('Show Time')
    #tickets=IntegerField('Number of tickets')
    #seats=StringField('Choose seats')
    #timing = SelectField(u'Show time', coerce=int)
    showtiming=SelectField(u'Show timing',choices=[])
    tickets = SelectField(u'Number of seats', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10')])
    submit = SubmitField('Proceed to seat selection')



@app.route('/index/<int:id>', methods=['GET','POST'])
@login_required
def index(id):
    click=0
    movies=Movie.query.all()
    #screenings=Screening.query.all()
    arr=[]
    arr2=[]
    for i in range(0,200):
        arr.append('0')
        #print(arr)form.username.data
    screenings=Screening.query.filter_by(movie_id=id).all()
    form=TicketForm(obj=screenings)    
    #if form.validate_on_submit():
    if request.method=='POST':
        selected=form.tickets.data
        show=form.showtiming.data
        print(selected)
        print(show)
        s=Screening.query.get(show);
        m=Movie.query.get(s.movie_id);
        r2=None
        p=None
        c3=None
        costs=Cost.query.filter_by(movie_name=m.title).all();
        for cos in costs:
            if cos.seat_type=="Recliner":
                r2=cos.cost;
            elif cos.seat_type=="Premium":
                p=cos.cost
            else:
                c3=cos.cost
        #s=Screening.query.filter_by(timing=show).first()
        rs=Reserved.query.filter_by(screening_id=show).all()
        for r in rs:
            arr[r.seat_id-1]='1' 
        c=[]
        c2=['A','B','C','D','E','F','G','H','I','J']
        for i in range (0,10):
            for j in range(0,10):
                c.append(c2[i])                    
        for i in range(1,101):
            j=i%10;
            if j==0:
                j=j+10
            arr2.append(j);
        return render_template('process.html',arr=arr,selected=selected,arr2=arr2,show=show,r2=r2,c=c,p=p,c3=c3)

    else:
        print('false')
    form.showtiming.choices=[(screening.id,screening.timing) for screening in screenings]
    return render_template('index.html',movies=movies,id=id,screenings=screenings,form=form)


@app.route('/process',methods=['GET','POST'])
def process():
    check2=""
    #req_data = request.get_json()
    #check2=req_data['check2']
    #print(check2)
    #return "hi"
    if request.method=="GET":

            #if request.data:
            check2 = request.args.get('check2', None)
            #check2 = str(request.json['check2'])
            #if check2:
            #return jsonify({"check2":check2})
            #check2=request.form['data']
            #print(isinstance(check2,str))

            #print(check2[len(check2)-1])
            li = list(check2.split(","))
            print(li)
            for i in range (0,len(li)):
                li[i]=int(li[i])                
            print(li)
            for i in range (0, len(li)-1):
                r=Reserved(seat_id=li[i]+1,screening_id=li[len(li)-1])
                db.session.add(r)
            db.session.commit()

            return json.dumps({'success': True}), 200, {'ContentType':'application/json'}
            #return render_template('trying.html')
    #return jsonify({"check2":check2})
    print(request.data)
    print(request.is_json)
    #print(request.json)
    return json.dumps({'success': False}), 200, {'ContentType':'application/json'}
    

@app.route("/account")
@login_required
def account():
    return render_template('account.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/addmovie",methods=['GET','POST'])
@login_required
def addmovie():
    if(Admin.query.filter_by(email=current_user.email).first()):
        print("true")
        form=AddMovieForm()
        if form.validate_on_submit():
            movie_add=form.moviename.data
            year_add=form.year.data
            print(movie_add)
            add(movie_add,year_add)
            return redirect(url_for('home'))
        return render_template('addmovie.html',form=form)
    else:
        print(current_user.email)
        return render_template('errored.html')

@app.route("/deletemovie",methods=['GET','POST'])
@login_required
def deletemovie():
    if(Admin.query.filter_by(email=current_user.email).first()):
        print("true")
        arr=[]
        i=0
        movies=Movie.query.all()
        for movie in movies:
            arr.append(movie.title)
            i+=1
        form = DeleteMovieForm()
        if form.validate_on_submit():
        #hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            #movie=Movie.query.filter_by(title=form.moviename.data).first()
            movie = Movie.query.filter_by(title=form.moviename.data).first()

            if movie:
                screenings=Screening.query.filter_by(movie_id=movie.id).all()
                for screening in screenings:
                    reserves=Reserved.query.filter_by(screening_id=screening.id)
                    for reserve in reserves:
                        db.session.delete(reserve)
                    db.session.delete(screening)
                costs=Cost.query.filter_by(movie_name=movie.title).all()
                for cost in costs:
                    db.session.delete(cost)                
                db.session.delete(movie)
                db.session.commit()
                flash('Movie deleted', 'success')
                return redirect(url_for('home')) 
            else:
                flash('Please check the values', 'danger')
        return render_template('deletemovie.html', form=form, movies=movies,arr=arr,l=len(arr))
    else:
        print(current_user.email)
        return render_template('errored.html')

@app.route("/addshow",methods=['GET','POST'])
@login_required
def addshow():
    if(Admin.query.filter_by(email=current_user.email).first()):
        print("true")
        arr=[]
        arr2=[]
        i=0
        screenings=Screening.query.all()
        for screening in screenings:
            arr.append(screening.nowshowing.title)
            arr2.append(screening.timing)
            i+=1
        form = AddShowForm()
        if form.validate_on_submit():
        #hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            movie=Movie.query.filter_by(title=form.moviename.data).first()
            if movie:
                s=Screening.query.filter_by(timing=form.showtime.data).first()
                if s:
                    flash('Please check the values', 'danger')
                else:
                    screening = Screening(timing=form.showtime.data,movie_id=movie.id)
                    db.session.add(screening)
                    db.session.commit()
                    flash('Showtime added', 'success')
                    return redirect(url_for('home'))

            else:
                flash('Please check the values', 'danger')
        return render_template('addshow.html', form=form,screenings=screenings,arr=arr,arr2=arr2,l=len(arr))
    else:
        print(current_user.email)
        return render_template('errored.html')

@app.route("/deleteshow",methods=['GET','POST'])
@login_required
def deleteshow():
    if(Admin.query.filter_by(email=current_user.email).first()):
        print("true")
        arr=[]
        arr2=[]
        i=0
        screenings=Screening.query.all()
        for screening in screenings:
            arr.append(screening.nowshowing.title)
            arr2.append(screening.timing)
            i+=1
        form = DeleteShowForm()
        if form.validate_on_submit():
        #hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            #movie=Movie.query.filter_by(title=form.moviename.data).first()
            screening = Screening.query.filter_by(timing=form.showtime.data).first()

            if screening:                
                res=Reserved.query.filter_by(screening_id=screening.id).all()
                for r in res:
                    db.session.delete(r)                    
                db.session.delete(screening)
                db.session.commit()
                flash('Showtime deleted', 'success')
                return redirect(url_for('home')) 
            else:
                flash('Please check the values', 'danger')
        return render_template('deleteshow.html', form=form, screenings=screenings,arr=arr,arr2=arr2,l=len(arr))
    else:
        print(current_user.email)
        return render_template('errored.html')

@app.route("/updateshow",methods=['GET','POST'])
@login_required
def updateshow():
    if(Admin.query.filter_by(email=current_user.email).first()):
        print("true")
        arr=[]
        arr2=[]
        i=0
        screenings=Screening.query.all()
        for screening in screenings:
            arr.append(screening.nowshowing.title)
            arr2.append(screening.timing)
            i+=1
        form = UpdateShowForm()
        if form.validate_on_submit():
        #hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            movie=Movie.query.filter_by(title=form.moviename.data).first()
            screening = Screening.query.filter_by(timing=form.showtime.data).first()

            if screening and movie:                
                screening.movie_id=movie.id
                db.session.commit()
                flash('Showtime updated', 'success')
                return redirect(url_for('home')) 
            else:
                flash('Please check the values', 'danger')
        return render_template('updateshow.html', form=form, screenings=screenings,arr=arr,arr2=arr2,l=len(arr))
    else:
        print(current_user.email)
        return render_template('errored.html')


