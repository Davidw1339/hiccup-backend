from flask import Flask, request
from pymongo import MongoClient
import json
client = MongoClient("mongodb://david:admin@ds145405.mlab.com:45405/hiccup")

app = Flask(__name__)

db = client.hiccup

@app.route('/')
def index():
    return "Hi dudes, come check out my insta"

@app.route('/up_vote', methods=['POST'])
def up_vote():
    idnum = request.form['id']
    upvotes = request.form['up']
    print "upvotes", upvotes
    db.livepoll.update({"id":idnum}, { "$set": {"up": upvotes}}, upsert=True)
    return "success"
@app.route('/down_vote', methods=['POST'])
def down_vote():
    idnum = request.form['id']
    downvotes = request.form['down']
    db.livepoll.update({"id":idnum}, { "$set": {"down": downvotes}}, upsert=False)
    return "success"

@app.route('/add_event', methods=['POST'])
def add_event():
    text = request.form['text']
    time = request.form['time']
    event = db.events.insert_one({
        "text": text,
        "time": time
    })
    return "done"

@app.route('/get_event', methods=['GET'])
def get_event():
    cursor = db.events.find()
    json_arr = []
    for event in cursor:
        json_arr.append({
            'text': event['text'],
            'time': event['time']
        })
    return json.dumps(json_arr);


@app.route('/add_announce', methods=['POST'])
def add_announce():
    text = request.form['text']
    time = request.form['time']
    announcement = db.announcements.insert_one({
        "text": text,
        "time": time
    })
    return "done"

@app.route('/get_announce', methods=['GET'])
def get_announce():
    cursor = db.announcements.find()
    json_arr = []
    for announcement in cursor:
        json_arr.append({
            'text': announcement['text'],
            'time': announcement['time']
        })
    return json.dumps(json_arr);

@app.route('/add_poll', methods=['POST'])
def add_poll():
    title = request.form['title']
    text = request.form['text']
    idnum = request.form['id']
    poll = db.livepoll.insert_one({
        "id": idnum,
        "title": title,
        "text": text,
        "up": "0",
        "down": "0"
    })
    return "done"

@app.route('/get_poll', methods=['GET'])
def get_poll():
    cursor = db.livepoll.find()
    json_arr = []
    for poll in cursor:
        json_arr.append({
            'title': poll['title'],
            'text': poll['text'],
            'up': poll['up'],
            'down': poll['down']
        })
    return json.dumps(json_arr);

@app.route('/add_message', methods=['POST'])
def add_message():
    email = request.form['username']
    text = request.form['text']
    message = db.livefeed.insert_one({
        "email": email,
        "text": text
    })
    return "done"
    # return message

@app.route('/get_messages', methods=['GET'])
def get_messages():
    cursor = db.livefeed.find()
    json_arr = []
    for message in cursor:
        json_arr.append({
            'email': message['email'],
            'text': message['text']
        })
    return json.dumps(json_arr);


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
    category = request.form['type']
    print "The category is", category
    # category = "hacker"
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
