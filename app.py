from pymongo import MongoClient
import certifi
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
import os

load_dotenv()
mongodbUri = os.environ.get('mongodbUri')

ca = certifi.where()
client = MongoClient(mongodbUri, tlsCAFile=ca)
db = client.indieground

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/result", methods=["GET"])
def movie_get():
    movie_list = list(db.movies.find({}, {'_id': False}))
    return jsonify({'movies': movie_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
