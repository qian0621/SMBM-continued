import shelve
from flask import redirect, render_template, request, session
from app import app
from user_classes import *
from classes_Nas import *

def loggedIn():
    return 'userInfo' in session
def notLoggedIn():
    return notLoggedIn()
def cannotView():
    return 'You are not allowed to view this page!'


def page(accountType, render):
    if not loggedIn():
        session['message'] = notLoggedIn()
        return redirect('/login')
    elif session['userInfo'].role == accountType:
        return render
    session['message'] = cannotView()
    return redirect('login')

# Customer Pages


@app.route('/redeemRewards', methods=['GET', 'POST'])
def redeemRewards():
    def f():
        if request.method == 'POST':
            for RewardType in Reward.__subclasses__():
                if RewardType.voucher == request.form['reward']:
                    reward = RewardType(session['userInfo'])
            session['userInfo'].rewards.append(reward)
            session['userInfo'].update_db()
        return render_template('redeemRewards.html', customer=session['userInfo'], reward=Reward)
    return page('Customer', f())

@app.route('/rewardsHistory')
def rewardsHistory():
    return page('Customer', render_template('rewardsHistory.html',rewards=session['userInfo'].rewards, rewardLoop=range(len(session['userInfo'].rewards))))


@app.route('/profile')
def profile():
    return page('Customer', render_template('profile.html',profile=session['userInfo']))


# Staff Pages

@app.route('/manageCustomers')
def manageRewards():
    with shelve.open('storage/users') as db:
        return page('Staff', render_template('manageCustomers.html', customers=db))


@app.route('/manageStaff')
def manageStaff():
    with shelve.open('storage/users') as db:
        return page('Staff', render_template('manageCustomers.html', staffs=db))


@app.route('/search/<name>')
def specificSearch(name):
    # Prevent access without login & staff role
    if not loggedIn():
        session['message'] = notLoggedIn()
        return redirect('/login')
    # If user presses search without a customer name, redirect them back to the main page
    elif name == '':
        return redirect('/search')
    elif session['userInfo'].role == 'Staff':
        with shelve.open('storage/users') as db:
            try:
                return render_template('search.html', user=db[name], search=True, rewardLoop=range(len(db[name].rewards))if db[name].role == 'Customer' and len(db[name].rewards) != 0 else [])
            except KeyError:
                session['message'] = f'A customer with the name of {name} does not exist!'
                return redirect('/search')
    session['message'] = cannotView()
    return redirect('/login')


@app.route('/search')
def search():
    # Prevent access without login & staff role
    if not loggedIn():
        session['message'] = notLoggedIn()
        return redirect('/login')
    elif session['userInfo'].role == 'Staff':
        try:
            message = session['message']
            del session['message']
            return render_template('search.html', message=message)
        except KeyError:
            return render_template('search.html')
    session['message'] = cannotView()
    return redirect('/login')
