from turtle import heading
import pandas as pd
# import os
from geopy.geocoders import Nominatim
import pickle
from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)

# picFolder = os.path.join('static', 'images')

# app.config['UPLOAD_FOLDER'] = picFolder

# @app.route("/Package")
# def index():
#     images = os.listdir('static/images')
#     images = ['images/' + image for image in images]
#     return render_template("Package.html", images=images)

@app.route("/")
def home():
    return render_template('index.html')


@app.route('/Mumbai')
def Mumbai():
    return render_template('Mumbai.html')

@app.route("/Hotel", methods=['post'])
def login():
    lo = request.form['location']
    rat = request.form['rate']
    ra = request.form['range']
    res = kmean(lo, rat, ra)
    return render_template('Package.html', res=res)


def kmean(input_city, price, rating):
    bin = [0,1000,2000,3000,4000,5000,6000,7000,8000]
    rating_bin=[0,1,2,3,4,5]
    loaded_model = pickle.load(open('kmeans.sav', 'rb'))
    geolocator = Nominatim(user_agent="specify")
    lo = geolocator.geocode(input_city + ' India ')
    result = loaded_model.predict(pd.DataFrame(
        {"longitude": [lo.longitude], "latitude": [lo.latitude]}))
    unpickled_df = pd.read_pickle("df.pkl")
    clust = result[0]
    opCities = unpickled_df.loc[unpickled_df['Cluster_ind'] == clust, [
        'Title', 'City', 'price', 'Special', 'Discount', 'Rating', 'price_bin', 'rating_bin']]
    p = pd.cut([int(price)], bin)
    r = pd.cut([int(rating)], rating_bin)
    op = opCities.loc[opCities['price_bin'] == p[0], [
        'Title', 'City', 'price', 'Special', 'Discount', 'Rating', 'rating_bin']]
    res = op.loc[op['rating_bin'] == r[0], [
        'Title', 'City', 'price', 'Special', 'Discount', 'Rating']]
    res = res.reset_index()
    res.dropna()
    res.head(5)
    return res.values.tolist()

if __name__ == "__main__":
    app.run(debug=True)
