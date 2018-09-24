import datetime
import logging
import os
import sys

from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FloatField, DateField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'replace-me-in-production'
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)


ACCRUAL_RATE = float(os.environ.get('ACCRUAL_RATE') or '9.232')

def get_next_rollover(for_date):
    # Get next April 30
    today = datetime.date.today()
    if today.month >= 5:
        return datetime.date(today.year + 1, 4, 30)
    else:
        return datetime.date(today.year, 4, 30)

class PdoForm(FlaskForm):
    balance = FloatField('Current balance (in hours)', default=0)
    scheduled = FloatField("Scheduled PDO (in hours)", default=0)
    target_date = DateField("Target Date", default=get_next_rollover(datetime.date.today()), format='%m/%d/%Y', validators=[DataRequired()])
    submit = SubmitField("Calculate")

def paychecks_between(start_date, end_date):
    dates = []
    date_iter = datetime.date(2018, 1, 5)
    while date_iter < end_date:
        if date_iter > start_date:
            dates.append(date_iter)
        date_iter += datetime.timedelta(weeks=2)
    return dates

@app.route('/', methods=['GET', 'POST'])
def home():
    today = datetime.date.today()
    form = PdoForm()
    
    if form.validate_on_submit():
        app.logger.debug('Form Valid')

        end_date = form.target_date.data
        paychecks_remaining = len(paychecks_between(today, end_date))
        starting_balance = form.balance.data
        scheduled_hours = form.scheduled.data
        balance = starting_balance + (paychecks_remaining * ACCRUAL_RATE) - scheduled_hours
        waste = balance - 40 if balance > 40 else 0

        return render_template('result.html', starting_balance=starting_balance,
            scheduled_hours=scheduled_hours, paychecks_remaining=paychecks_remaining,
            balance=balance, waste=waste, end_date=end_date)
    return render_template('form.html', form=form)
