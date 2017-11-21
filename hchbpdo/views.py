import datetime
from datetime import date

from django.shortcuts import render

from hchbpdo.forms import PdoForm

seed_date = date(2017, 10, 13)

ACCRUAL_RATE = 9.232

def get_next_rollover(for_date):
    # Get next April 30
    today = date.today()
    if today.month >= 5:
        return date(today.year + 1, 4, 30)
    else:
        return date(today.year, 4, 30)

def paychecks_between(start_date, end_date):
    dates = []
    date_iter = seed_date
    while date_iter < end_date:
        if date_iter > start_date:
            dates.append(date_iter)
        date_iter += datetime.timedelta(weeks=2)
    return dates

def pdo(request):
    today = date.today()
    if request.method == 'POST':
        form = PdoForm(request.POST)
        if form.is_valid():
            end_date = form.cleaned_data['target_date']
            paychecks_remaining = len(paychecks_between(today, end_date))
            starting_balance = form.cleaned_data['balance']
            scheduled_hours = form.cleaned_data['days'] * 8
            eoy_balance = starting_balance + (paychecks_remaining * ACCRUAL_RATE) - scheduled_hours
            if eoy_balance > 40:
                waste = eoy_balance - 40
            return render(request, 'result.html', locals())

    else:
        form = PdoForm(initial={'target_date': get_next_rollover(today)})
    return render(request, 'form.html', {
        'form': form,
    })
