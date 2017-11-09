import datetime
from datetime import date

from django.shortcuts import render

from hchbpdo.forms import PdoForm

seed_date = date(2017, 10, 13)

ACCRUAL_RATE = 9.232

def gen_year(year):
    dates = []
    date_iter = seed_date
    while date_iter.year < year + 1:
        if date_iter.year == year and date_iter > date.today():
            dates.append(date_iter)
        date_iter += datetime.timedelta(weeks=2)
    return dates


def pdo(request):
    if request.method == 'POST':
        form = PdoForm(request.POST)
        if form.is_valid():
            paychecks_remaining = len(gen_year(date.today().year))
            starting_balance = form.cleaned_data['balance']
            scheduled_hours = form.cleaned_data['days'] * 8
            eoy_balance = starting_balance + (paychecks_remaining * ACCRUAL_RATE) - scheduled_hours
            if eoy_balance > 40:
                waste = eoy_balance - 40
            return render(request, 'result.html', locals())

    else:
        form = PdoForm()
    return render(request, 'form.html', {
        'form': form,
    })