from flask import Flask,render_template,redirect,url_for
from forms import WeatherForm
import requests
import os
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'helloworld'

def api_key():
    api_ke = os.environ.get('api_key')
    return api_ke

def weather_api_loader(city,api_id):
    api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_id}'
    r = requests.get(api_url)
    return r.content

@app.route('/',methods=['GET','POST'])
@app.route('/home',methods=['GET','POST'])
def home():
    form = WeatherForm()
    if form.validate_on_submit():
        city = form.input_.data
        Source = weather_api_loader(city,api_key())
        data = json.loads(Source)
        code = data['cod']
        if code == int('404'):
            return "NO CITY EXISTS BY THIS NAME"
        else:
            name = data['name']
            weather = data['weather'][0]
            main = data['main']
            visibility = data['visibility']
            wind = data['wind']
            sunrise = data['sys']['sunrise']
            sunset = data['sys']['sunset']
            main_ = data['weather'][0]['main']
            return render_template('display.html',name=name,weather=weather,main=main,visibility=visibility,wind=wind,sunrise=sunrise,sunset=sunset,main_=main_)
    return render_template('home.html', form=form)

if __name__ =='__main__':
    app.run(debug=True)