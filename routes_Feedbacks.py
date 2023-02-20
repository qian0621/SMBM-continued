from flask import request, redirect, url_for, render_template,session
from feedbackform import CreateFeedbackForm
import shelve, Feedback
from app import app
from feedbacks_validation import feedback_validation,update_feedback_validation

@app.route('/feedbacks', methods=['GET', 'POST'])
def create_feedback():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        feedbacks = request.form['feedback']
        submit,validate=feedback_validation(name,email,feedbacks)
        if submit:
            return validate
        else:
            feedbacks_dict = {}
            db = shelve.open('storage/feedback.db', 'c')
            try:
                feedbacks_dict = db['Feedbacks']
            except:
                print("Error in retrieving Feedbacks from feedback.db.")
            feedback = Feedback.Feedback(name, email,feedbacks)

            # for id
            latestid=1
            for key in feedbacks_dict:
                user = feedbacks_dict.get(key)
                latestid=user.get_feedback_id()+1
                
            feedback.set_feedback_id(latestid)
            feedbacks_dict[latestid] = feedback

            db['Feedbacks'] = feedbacks_dict
            db.close()
            return redirect(url_for('retrieve_feedbacks'))
    
    return render_template('feedback.html')




@app.route('/retrieve_feedbacks')
def retrieve_feedbacks():
    feedbacks_dict = {}
    # if db doesn't exist,there'll be error---> bug
    # bug need to fix here
    try:
        db = shelve.open('storage/feedback.db', 'r')
        feedbacks_dict = db['Feedbacks']
        db.close()
    except:
        feedbacks_dict = {}
    feedback_list = []
    for key in feedbacks_dict:
        user = feedbacks_dict.get(key)
        feedback_list.append(user)

    return render_template('retrieveFeedback.html', count=len(feedback_list), feedback_list=feedback_list)


@app.route('/updateFeedback/<int:id>', methods=['GET', 'POST'])
def update_feedback(id):
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        feedbacks = request.form['feedback']
        submit,validate=update_feedback_validation(name,email,feedbacks)
        if submit:
            return validate
        else:
            feedbacks_dict = {}
            db = shelve.open('storage/feedback.db', 'w')
            feedbacks_dict = db['Feedbacks']

            feedback = feedbacks_dict.get(id)
            feedback.set_name(name)
            feedback.set_email(email)
            feedback.set_feedbacks(feedbacks)

            db['Feedbacks'] = feedbacks_dict
            db.close()

            return redirect(url_for('retrieve_feedbacks'))
    else:
        feedbacks_dict = {}
        try:
            db = shelve.open('storage/feedback.db', 'r')
            feedbacks_dict = db['Feedbacks']
            db.close()
            feedback = feedbacks_dict.get(id)
        except:
            print("Error in retrieving Feedbacks from feedback.db.")
        

        current_user=session['userInfo']
        current_name=current_user.name
        current_email=current_user.email
        name = feedback.get_name()
        email = feedback.get_email()
        feedbacks = feedback.get_feedbacks()

        if current_name==name and current_email==email:
            return render_template('updateFeedback.html',name=name,email=email,feedback=feedbacks)
        else:
            errormess="You can't update other's"
            try:
                db = shelve.open('storage/feedback.db', 'r')
                feedbacks_dict = db['Feedbacks']
                db.close()
            except:
                feedbacks_dict = {}
            feedback_list = []
            for key in feedbacks_dict:
                user = feedbacks_dict.get(key)
                feedback_list.append(user)
            return render_template('retrieveFeedback.html', count=len(feedback_list), feedback_list=feedback_list,errormess=errormess)

        return render_template('updateFeedback.html',name=name,email=email,feedback=feedbacks)

@app.route('/delete_feedback/<int:id>', methods=['GET', 'POST'])
def delete_feedback(id):
    feedbacks_dict = {}
    current_user=session['userInfo']
    current_name=current_user.name
    current_email=current_user.email
    db = shelve.open('storage/feedback.db', 'w')
    feedbacks_dict = db['Feedbacks']
    temp=feedbacks_dict.pop(id)
    if current_name==temp.get_name() and current_email==temp.get_email():
        db['Feedbacks'] = feedbacks_dict
    else:
        errormess="You can't delete other's Feedbacks!"
        try:
            db = shelve.open('storage/feedback.db', 'r')
            feedbacks_dict = db['Feedbacks']
            db.close()
        except:
            feedbacks_dict = {}
        feedback_list = []
        for key in feedbacks_dict:
            user = feedbacks_dict.get(key)
            feedback_list.append(user)
        return render_template('retrieveFeedback.html', count=len(feedback_list), feedback_list=feedback_list,errormess=errormess)
    db.close()

    return redirect(url_for('retrieve_feedbacks'))
