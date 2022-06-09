from crypt import methods
from flask import Flask, render_template, request, url_for
import requests
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weatherApp.db'

db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    cities = City.query.all()

    if request.method == 'POST':
        userCity = request.form['userCityInp']
        if userCity:
            if userCity not in cities:
                    city_obj = City(name=userCity)
                    db.session.add(city_obj)
                    db.session.commit()

    #print(city) 


    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=36dc62b4d6fd2d8bbb4b7964f91884be'

    weatherData = []

    for city in cities:

        r = requests.get(url.format(city.name)).json()



        weatherInfo = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weatherData.append(weatherInfo)
    
    print(weatherData)
    
    return render_template('index.html', weatherData=weatherData)


if __name__=="__main__":
    app.run(debug=True)
