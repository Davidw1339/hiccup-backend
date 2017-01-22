from flask import Flask, request
from pymongo import MongoClient
client = MongoClient("mongodb://david:admin@ds145405.mlab.com:45405/hiccup")

app = Flask(__name__)

db = client.hiccup

@app.route('/add_message', methods=['POST'])
def add_message():
    email = request.form['username']
    text = request.form['text']
    message = db.livefeed.insert_one({
        "email": email,
        "text": text
    })
    return message

@app.route('/login', methods=['GET'])
def login():
    email = request.args.get('email')
    password = request.args.get('password')
    user = db.users.find_one({"email": email, "password": password})
    if user:
        return user['type']
    return "no-auth"

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    cursor = db.users.find({"email": email})
    if cursor:
        for user in cursor:
            return "already-registered"

    password = request.form['password']
    # category = request.form['type']
    category = "hacker"
    print email, password
    user = db.users.insert_one(
    {
        "email": email,
        "password": password,
        "type": category
    })
    if(user):
        return "registered"
    return "no-register"
