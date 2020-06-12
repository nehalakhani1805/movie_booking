from bs4 import BeautifulSoup
from urllib.request import urlopen
from imdb import IMDb
import requests
from random import seed
import sqlite3
import pandas as pd
import re

import pickle
from flaskblog import creating_model
from math import isnan
from warnings import filterwarnings
from flaskblog import db 
from flaskblog.models import User, Admin, Movie, Seat, Screening, Reserved, Cost

filterwarnings("ignore")
lm,IMDB,feature_columns=creating_model.create_model()
imdb_obj = IMDb()
proxy = {"https": "185.56.209.114:51386"}
s = requests.Session()
s.proxies = {"http": "http://50.203.239.28:80"}
seed(1)

def cost(predicted_movie_rating):
    premium_cost=0
    if(predicted_movie_rating>0 and predicted_movie_rating<3):
        premium_cost=100
    elif(predicted_movie_rating>=3 and predicted_movie_rating<6):
        premium_cost=120
    elif(predicted_movie_rating>=6 and predicted_movie_rating<8):
        premium_cost=160
    elif(predicted_movie_rating>=8 and predicted_movie_rating<=10):
        premium_cost=200
    return premium_cost

def add(name, year):
    # Load the data of the new movie whose rating is to be found.
    link = imdb_obj.get_imdbURL(imdb_obj.search_movie(name)[0])
    movie_object = imdb_obj.get_movie(imdb_obj.search_movie(name)[0].movieID)
    content = s.get(link).content
    soup = BeautifulSoup(content.decode('utf-8', 'ignore'), 'lxml')
    # Need to find the name of director, writer, cast and the genres of the movie as well as
    # its runtime, production house and description.
    movie_name=name
    director = None
    writer = None
    cast = []
    genres = []
    runtime = None
    pred_runtime=None
    production_house = None
    movie_desc = None
    actors = ""
    genre_string = ""
    imdb_rating=None
    premium_cost = None
    recliner_cost = None
    classic_cost = None
    date_of_release=""

    # Find duration of movie.
    try:
        runtime = int(movie_object['runtimes'][0])
        pred_runtime=runtime
    except:
        # runtime = IMDB['Runtime (Minutes)'].mean()
        runtime=110
    # Finding actual IMDB Rating if available.
    try:
        imdb_rating = float(soup.find('div', class_='ratingValue').find('span').string)
    except:
        imdb_rating = None
    # Find the director, writer, star actors of the movie.
    try:
        divs = soup.find_all('div', class_="credit_summary_item")
        count = 0
        for div in divs:
            if (count == 0):
                try:
                    director = div.find('a').string
                except:
                    dummy = None
            if (count == 1):
                try:
                    writer = div.find('a').string
                except:
                    dummy = None
            if (count == 2):
                try:
                    list_of_a_tags = div.find_all('a')
                    for a in list_of_a_tags:
                        if (a.string == "See full cast & crew"):
                            break
                        actors += a.string + ","
                except:
                    dummy = None
            count += 1
        try:
            actors = actors[0:len(actors) - 1]
        except:
            dummy = None
            actors = None
    except:
        dummy = None
        actors = None

    try:
        cast = actors.split(",")
    except:
        print("Cast not found")
    # Find the genres of the movie.
    try:
        genrediv = soup.find('div', class_='subtext')
        list_of_a_tags = genrediv.find_all('a')
        for a in list_of_a_tags:
            if (re.findall(r"\d{4}", a.string)):
                break
            genre_string += a.string + ','
        try:
            genre_string = genre_string[0:len(genres) - 1]
        except:
            dummy = None
            genre_string = None
    except:
        dummy = None
        genre_string = None
    try:
        genres = genre_string.split(',')
    except:
        print("Genres not found")
    # Find the Production House.
    try:
        divs = soup.find('div', id='titleDetails').find_all('div', class_='txt-block')
        h4_count = 0
        for div in divs:
            if (h4_count > 12):
                break
            if (div.find('h4', class_='inline').string == "Production Co:"):
                production_house = div.find('a').string.strip()
            h4_count += 1
    except:
        dummy = None

    try:
        movie_desc = soup.find('div', class_="summary_text").string.strip()
    except:
        print("Description not found.")

    try:
        date_of_release_div = soup.find('div',class_="subtext")
        list_of_a_tags = date_of_release_div.find_all('a')
        for a in list_of_a_tags:
            if(re.findall(r"\d{4}",a.string)):
                string=a.string.split(" ")
                for i in range(0,3):
                    date_of_release+=string[i]
                    if(i!=2):
                        date_of_release+="-"
    except:
        print("Error in accessing date.")

    predicted_movie_rating = creating_model.predict(year, pred_runtime, genres, cast, production_house,director, writer, IMDB, feature_columns, lm)
    predicted_movie_rating = round(predicted_movie_rating,2)
    premium_cost = cost(predicted_movie_rating)
    recliner_cost = premium_cost+25
    classic_cost = premium_cost-15
    error=str(round((abs(imdb_rating-predicted_movie_rating)/imdb_rating)*100,2))+"%"
    print("Predicted rating=",predicted_movie_rating,", Error=",error,", Cost of normal ticket=",premium_cost)
    #"Never Rarely Sometimes Always", "Dolittle", "Underwater", "Knives Out", "I Still Believe", "Birds of Prey"
    '''
    The DBA needs to access these variables:
    1) movie_name
    2) runtime
    3) director
    4) writer
    5) actors
    6) production_house
    7) genre_string
    8) movie_desc
    9) premium_cost, recliner_cost, classic_cost
    '''
    m1=Movie(title=movie_name, date_released= date_of_release,content=movie_desc,director=director, cast=actors, duration=runtime, genre=genre_string)
    db.session.add(m1)
    c1=Cost(movie_name=movie_name,seat_type="Recliner",cost=recliner_cost)
    c2=Cost(movie_name=movie_name,seat_type="Premium",cost=premium_cost)
    c3=Cost(movie_name=movie_name,seat_type="Classic",cost=classic_cost)
    db.session.add(c1)
    db.session.add(c2)
    db.session.add(c3)
    db.session.commit()

def main():
    print("Add movie initialised.")

if __name__ == '__main__':
    main()
if __name__!='__main__':
    main()

