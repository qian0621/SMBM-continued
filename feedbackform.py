from wtforms import Form, StringField, TextAreaField, validators
from wtforms.fields import EmailField

class CreateFeedbackForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    feedbacks = TextAreaField('Feedbacks', [validators.Optional()])
