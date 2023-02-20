import re
from flask import render_template,session

def feedback_validation(name,email,feedback):
    submit=False
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    current_user=session['userInfo']
    current_name=current_user.name
    current_email=current_user.email
    name_error=''
    email_error=''
    feedback_error=''
    nei='is-valid'
    eei='is-valid'
    fei='is-valid'

    if name == '':
        submit=True
        nei='is-invalid'
        name_error="Name cannot be blank!"
        
    if name != current_name and name_error == "":
        submit=True
        nei='is-invalid'
        name_error="Not Current user name!"
        
    if email == '':
        submit=True
        eei='is-invalid'
        email_error="Email cannot be blank!"

    if not re.fullmatch(regex, email) and email_error=='':
        submit=True
        eei='is-invalid'
        email_error="Invalid email format!"    
    
    if email != current_email and email_error=='':
        submit=True
        eei='is-invalid'
        email_error="Not Current user email!"

    if feedback == '':
        submit=True
        fei='is-invalid'
        feedback_error="Feedback cannot be blank!"
        
    return submit,render_template('feedback.html',nei=nei,eei=eei,fei=fei,
                           feedback_error=feedback_error,name_error=name_error,email_error=email_error,
                           name=name,email=email,feedback=feedback)
 
def update_feedback_validation(name,email,feedback):
    submit=False
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    current_user=session['userInfo']
    current_name=current_user.name
    current_email=current_user.email
    name_error=''
    email_error=''
    feedback_error=''
    nei='is-valid'
    eei='is-valid'
    fei='is-valid'

    if name == '':
        submit=True
        nei='is-invalid'
        name_error="Name cannot be blank!"
        
    if name != current_name and name_error == "":
        submit=True
        nei='is-invalid'
        name_error="Not Current user name!"
        
    if email == '':
        submit=True
        eei='is-invalid'
        email_error="Email cannot be blank!"

    if not re.fullmatch(regex, email) and email_error=='':
        submit=True
        eei='is-invalid'
        email_error="Invalid email format!"    
    
    if email != current_email and email_error=='':
        submit=True
        eei='is-invalid'
        email_error="Not Current user email!"

    if feedback == '':
        submit=True
        fei='is-invalid'
        feedback_error="Feedback cannot be blank!"
        
    return submit,render_template('updateFeedback.html',nei=nei,eei=eei,fei=fei,
                           feedback_error=feedback_error,name_error=name_error,email_error=email_error,
                           name=name,email=email,feedback=feedback)
