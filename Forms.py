import datetime
from wtforms import Form, SelectField, validators, IntegerField, DecimalField
from wtforms.fields import DateField
from wtforms.validators import NumberRange


class PricingForm(Form):
    date = DateField('Date of Slot', default=datetime.date.today())
    adultPrice = IntegerField('Adult ($)', validators=[NumberRange(min=0, max=100, message='Price out of range'), validators.DataRequired()],default=10)
    concessionPrice = IntegerField('Concession ($)', validators=[NumberRange(min=0, max=100, message='Price out of range'), validators.DataRequired()], default=6)
    childPrice = IntegerField('Child ($)', validators=[NumberRange(min=0, max=100, message='')], default=0)

    availability1 = IntegerField('10AM', validators=[NumberRange(min=0, max=10, message='Availibility must be between 0 and 10')], default=10)

    availability2 = IntegerField('11AM', validators=[NumberRange(min=0, max=10, message='Availibility must be between 0 and 10')], default=10)

    availability3 = IntegerField('2PM', validators=[NumberRange(min=0, max=10, message='Availibility must be between 0 and 10')], default=10)

    availability4 = IntegerField('3PM', validators=[NumberRange(min=0, max=10, message='Availibility must be between 0 and 10')], default=10)

    availability5 = IntegerField('4PM', validators=[NumberRange(min=0, max=10, message='Availibility must be between 0 and 10')], default=10)
