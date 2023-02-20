from flask import render_template, session, request, redirect, url_for
import shelve
from app import app


class Messages:
    def __init__(self):
        self.history = []

    def send_message(self, message, sender):
        self.history.append({"message": message, "sender": sender})

    def get_history(self):
        return self.history

    def clear_history(self):
        self.history = []
 

@app.route('/chat')
def chat():
    try:
        current_user=session['userInfo']
        user_id=current_user.count 
        current_name=current_user.name
    except:
        return render_template('login.html')
    return render_template("chatbox.html",id=user_id,name=current_name)


@app.route('/chatStaff')
def chatStaff():
    return render_template("chatboxStaff.html")








