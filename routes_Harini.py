from flask import abort, flash, redirect, render_template, request, session, url_for
from app import app
from user_classes import *
import hashlib
import shelve


def loggedIn():
    return 'userInfo' in session


@app.route('/register/<aType>', methods=['GET', 'POST'])
def register(aType):
    try:
        accountType = [classType for classType in Account.__subclasses__(
        )if classType.__name__ == aType.title()][0]
    except IndexError:
        abort(404)
    if request.method != 'POST':
        return render_template(f'register{"Staff" if "Staff" in str(accountType) else "Customer"}.html')
    name = request.form['name']
    password = request.form['password']
    if len(password) < 8 or len(password) > 15:
        flash('Password must be between 8 and 15 characters long.', 'noti')
        return redirect(request.url)
    if not all(char.isalnum() or char in '!@#$%^&*()_-+=' for char in password):
        flash('Password can only contain alphanumeric and special characters (!@#$%^&*()_-+=).', 'noti')
        return redirect(request.url)
    with shelve.open('storage/users') as db:
        db[name] = accountType(
            name, request.form['email'], password)

    return redirect('/login') \
        if not loggedIn() or session['userInfo'].role != 'Staff' \
        else redirect(f'/manage{aType.capitalize()}')


@app.route('/resetPassword', methods=['GET', 'POST'])
def resetPassword():
    if request.method != 'POST':
        return render_template('resetPassword.html')
    name = request.form['name']
    email = request.form['email']
    password = request.form['new_password']
    confirm_password = request.form['confirm_password']
    with shelve.open('storage/users', writeback=True) as db:
        if name not in db or db[name].email != email:
            flash('Invalid name/email', 'noti')
            return render_template('resetPassword.html')
        if password != confirm_password:
            flash('New & confirm password must match!', 'noti')
            return render_template('resetPassword.html')
        db[name].password = password
        flash('Your password has been successfully reset. Please login with your new password.', 'noti')
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method != 'POST':
        try:
            message = session['message']
            del session['message']
            return render_template('login.html', message=message)
        except KeyError:
            return render_template('login.html')
    # Get name and hashed password from inputs
    name = request.form.get('name')
    password = request.form.get('password')
    # Open the shelve database
    with shelve.open('storage/users') as db:
        try:
            user = db[name]
            # Invalid name/password
            if user.name == name and user.check_password(password):
                # Create a session for the user under userInfo
                session['userInfo'] = user
            else:
                flash('Invalid name/password', 'noti')
                return render_template('login.html')
            # return render_template('login.html', message='Invalid name/password')
        except KeyError:
            # Invalid name
            flash('Invalid name', 'noti')
            return render_template('login.html')
        # return render_template('login.html', message='Invalid name/password')
        return redirect('/')

@app.route('/logout')
def logout():
    # Remove user info from session
    flash(f'{session.pop("userInfo").name}, you have successfully logged out.', 'noti')
    return render_template('login.html')
    # return render_template('login.html', message=f'{session.pop("userInfo").name}, you have successfully logged out.')
