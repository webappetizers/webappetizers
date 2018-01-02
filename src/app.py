from flask import Flask, render_template
from pymongo import MongoClient
import os


client = MongoClient('mongodb://localhost:27017')
print("Created client")
db = client.streets_db
print("Connected to streets_db")
streets = db.streets

app = Flask(__name__)
from views import *

# os.environ['TODO_DB_1_PORT_27017_TCP_ADDR']



if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)