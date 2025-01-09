# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
from flask import render_template, redirect, request, session, url_for, copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from .utils.database.database  import database
from werkzeug.datastructures   import ImmutableMultiDict


from pprint import pprint
import json
import random
import functools
from . import socketio
db = database()


#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "email" not in session:
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)
    return secure_function

def getUser():
	return session['email'] if 'email' in session else 'Unknown'

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/logout')
def logout():
	session.pop('email', default=None)
	return redirect('/home')



@app.route('/processlogin', methods=["POST", "GET"])
def processlogin():
    # Extract form data or JSON data
    if request.form:
        form_fields = {key: request.form.getlist(key)[0] for key in request.form.keys()}
    elif request.json:
        form_fields = request.json
    else:
        return json.dumps({'success': 0})

    email = form_fields.get('email')
    password = form_fields.get('password')

    if not email or not password:
        return json.dumps({'success': 0})

    encrypted_password = db.onewayEncrypt(password)
    is_authenticated = db.authenticate(email, encrypted_password)

    if is_authenticated['success'] == 1:
        session['email'] = email
        return json.dumps({'success': 1})
    else:
        return json.dumps({'success': 0})

    


#######################################################################################
# CHATROOM RELATED
#######################################################################################
# Chatroom
@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html', user=getUser())

#Routes for when user joins chatroom, if its owner, the text is blue and right justified, else its grey and left justified
@socketio.on('joined', namespace='/chat')
def joined(message):
    join_room('main')
    if getUser() == 'owner@email.com':
        emit('status', {'msg': getUser() + ' has entered the room.', 'style': 'width: 100%;color:blue;text-align: right;padding-top:7px'}, room='main')
    else:
        emit('status', {'msg': getUser() + ' has entered the room.', 'style': 'width: 100%;color:grey;text-align: left;padding-top:7px'}, room='main')
#Routes for when user sends a message, if its owner, the text is blue and right justified, else its grey and left justified
@socketio.on('text', namespace='/chat')
def text(message):
    join_room('main')
    # Determine the sender's styling
    if getUser() == 'owner@email.com':  
        style = 'width: 100%; color: blue; text-align: right'
    else:
        style = 'width: 100%; color: gray; text-align: left'
    
    emit('message', {
        'msg': getUser() + ': ' + message['text'],
        'style': style
    }, room='main')

#Routes for when user leaves chatroom, if its owner, the text is blue and right justified, else its grey and left justified
@socketio.on('left', namespace='/chat')
def left(message):
    leave_room('main')
    if getUser() == 'owner@email.com':
        emit('status', {'msg': getUser() + ' has left the room.', 'style': 'width: 100%;color:blue;text-align: right'}, room='main')
    else:
       emit('status', {'msg': getUser() + ' has left the room.', 'style': 'width: 100%;color:grey;text-align: left'}, room='main')
    

#######################################################################################
# OTHER
#######################################################################################

@app.route('/')
def root():
	return redirect('/home') #Controls behavior of website

@app.route('/home')
def home():
    x = random.choice(['I am 20 years old.', 'I am on MSU Jawani.', 'I previously interned at Mercedes-Benz Financial Services.'])
    return render_template('home.html', fun_fact=x)

#Routes for resume page
@app.route('/resume')
def resume():
    resume_data = db.getResumeData()
    pprint(resume_data)  
    return render_template('resume.html', resume_data=resume_data)

#Routes for projects page
@app.route('/projects')
def projects():
    return render_template('projects.html')
#Routes for piano page
@app.route('/piano')
def piano():
    return render_template('piano.html')

#Processed all the feedback from input and stores into feedback database with SQL Insert Query
@app.route('/processfeedback', methods=['POST'])
def processfeedback():
    feedback_data = request.form
    db.query(
        "INSERT INTO feedback (name, email, comment) VALUES (%s, %s, %s)",
        (feedback_data['name'], feedback_data['email'], feedback_data['comment'])
    )
    all_feedback = db.query("SELECT * FROM feedback")
    return render_template('processfeedback.html', feedback=all_feedback) #Prints out information in feedback page

@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r
