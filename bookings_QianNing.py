from app import app
from flask import render_template, request, redirect, url_for, session, jsonify, abort, flash
import shelve
from products_Sixuan import Slots
from datetime import date, time, datetime, timedelta
from re import match
from booking import Booking
import json
# from classes_Nas import Reward


@app.route('/bookings', methods=['GET', 'POST'])
def makebooking():
    errors = {}
    datetimetime = request.args.get('slot')
    if datetimetime:                                    # desired time slot submitted
        if validslotformat(datetimetime):
            slotinfo = checkslotavail(datetimetime)     # {date:str, timeslot:tuple}, {left:int, ticketypes:dict}
            print(slotinfo)
            if slotinfo:                                # slot available
                return booktickets(slotinfo)            # POST form booking details
            else:                                       # slot unavailable
                errors['slot'] = 'Sorry, the time slot you picked is no longer available. Please choose another'
        else:                                           # invalid datetimetime format
            errors['slot'] = 'Sorry, there was a date time format error. Please try again'                                          # load pick timeslot form
    availinfo = dbtoslotform()
    if availinfo:
        return render_template('makebooking.html',      # 1st load or error reload
                               **availinfo,
                               errors=errors)
    else:
        return render_template('makebooking.html',      # no slots available
                               avaliable=availinfo,
                               errors=errors)


def booktickets(slotinfo):
    errors = {}
    prevsubmit = {}
    if request.method == 'POST':
        prevsubmit = request.form
        print(prevsubmit)
        if not ('Adult' in prevsubmit or 'Concession' in prevsubmit or 'Child' in prevsubmit):
            errors['cart'] = 'Your cart is empty, please pick a Concession or Adult ticket before checkout'
        elif not ('Adult' in prevsubmit or 'Concession' in prevsubmit):
            errors['cart'] = 'Children under 7 need to be accompanied by an adult, ' \
                             'please buy at least 1 Adult or Concession ticket'
        else:
            tickets = {}
            ticketcount = 0
            for key, value in prevsubmit.items():
                if key in slotinfo['slotinfo']['Ticket Types']:
                    if key in tickets:
                        errors[key] = 'Submitted data is malformed, please try again'
                    else:
                        if value.isdigit():
                            quantity = int(value)
                            if quantity > 0:
                                ticketcount += quantity
                                tickets[key] = quantity
                                if ticketcount > slotinfo['slotinfo']['Slots left']:
                                    errors['soldout'] = True
                        if key not in tickets:
                            errors[key] = 'Invalid value, please enter a positive integer'
                elif key == 'claimed':
                    if value:
                        claims = json.loads(value)
                        customerAcc = session['userInfo']
                        for claim in claims:
                            claimed = False
                            for reward in customerAcc.rewards:
                                if str(reward.id) == claim:
                                    customerAcc.rewards.remove(reward)
                                    customerAcc.update_db()
                                    claimed = True
                                    break
                            if not claimed:
                                errors['cart'] = f'Sorry, the reward you claimed is not available, please remove from cart'
                                break
            if not errors:
                customer = session.get('userInfo')
                if customer:
                    customerid = {'customer': customer}
                else:
                    customerid = {'email': ''}
                madebooking = Booking(day=slotinfo['bookinfo']['Date'],
                                      event=slotinfo['bookinfo']['Booking Type'],
                                      tickets=tickets,
                                      requests=prevsubmit['requests'],
                                      timeslot=slotinfo['bookinfo']['Time Slot'],
                                      **customerid)
                flash(madebooking.mail(), 'noti')
                return redirect(url_for('abooking', customerName=madebooking.name, bookingid=madebooking.id))
    print(errors)   # ticketype, claim
    slotinfo['bookinfo']['Time Slot'] = "{:%I:%M %p} - {:%I:%M %p}".format(*slotinfo['bookinfo']['Time Slot'])
    return render_template('bookingtickets.html',
                           **slotinfo,
                           tickets={},
                           form=prevsubmit,
                           errors=errors,
                           customerAcc=('userInfo' in session and session['userInfo'].role == 'Customer'))


@app.route('/bookings/voucher')
def cal_voucher():
    if 'voucher' not in request.args or 'subtotal' not in request.args:
        abort(400, "url parameters 'voucher' and 'subtotal' not there")
    voucher = request.args['voucher']
    for reward in session['userInfo'].rewards:
        if reward.voucher == voucher:
            print(str(reward.discount(int(request.args['subtotal']))))
            return str(reward.discount(int(request.args['subtotal'])))
    # user does not have reward
    abort(403, 'You do not have ' + voucher)


@app.route('/bookings/mybookings')
def mybookings():
    # hardcoding
    filters = request.args
    print(filters)
    if 'userInfo' not in session:
        abort(401)
    with shelve.open('storage/bookings') as bookingsDB:
        # MAKE SURE 'Qian Ning' IN bookings shelve, OR KeyError: b'Qian Ning' WILL HAPPEN
        bookings = bookingsDB.get(session['userInfo'].name, [])
    return render_template('viewbookings.html', **filterbookings(bookings, filters))


@app.route('/bookings/<string:customerName>/<int:bookingid>', methods=['GET', 'POST', 'DELETE'])
@app.route('/bookings/<string:customerName>/<int:bookingid>/<string:back>/<string:link>', methods=['GET', 'POST', 'DELETE'])
def abooking(customerName, bookingid, back='My Bookings', link='mybookings'):
    print(customerName, bookingid, back, link)
    if 'userInfo' in session and \
            (customerName == session['userInfo'].name or session['userInfo'].role == 'Staff'):
        with shelve.open('storage/bookings', writeback=True) as bookingdb:
            if customerName in bookingdb:
                for booking in bookingdb[customerName]:
                    if booking.id == bookingid:
                        if request.method == 'DELETE':
                            bookingdb[customerName].remove(booking)
                            booking.freeupslot()
                            flash('Booking Deleted!', 'noti')
                            return redirect(url_for(link))
                        elif request.method == 'GET':
                            return render_template('abooking.html',
                                                   back=(back, link),
                                                   **booking.info(back=back, link=link))
                        elif request.method == 'POST':
                            if request.form['action'] == 'mail':
                                return booking.mail()
            else:
                abort(404, f'{customerName} has no bookings')
    else:
        abort(403, "This booking is not yours")
    # if conditional in for loop not triggered
    abort(404, f'{customerName} does not have this booking')


@app.route('/bookings/all')
def allbookings():
    filters = request.args
    print(filters)
    if 'userInfo' in session and session['userInfo'].role == 'Staff':
        with shelve.open('storage/bookings') as bookingsDB:
            custbookings = [booking for acustbooking in bookingsDB.values() for booking in acustbooking]
        return render_template('viewbookings.html', staff=True, **filterbookings(custbookings, filters))
    else:
        abort(403, "Only staff allowed")


def validslotformat(string):
    # 2023-01-18.15:00:00_15:45:00
    pattern = r"^\d{4}-\d{2}-\d{2}\.\d{2}:\d{2}:\d{2}_\d{2}:\d{2}:\d{2}$"
    return match(pattern, string) is not None


def checkslotavail(string):
    pickedate, timerange = string.split('.')
    timerange = tuple([time.fromisoformat(startend) for startend in timerange.split('_')])
    if datetime.now() <= datetime.combine(date.fromisoformat(pickedate), timerange[0]):
        with shelve.open('storage/slots') as slotsDB:
            if pickedate in slotsDB:
                day = slotsDB[pickedate]
                dateslots = day.availability
                if timerange in dateslots:
                    slotsleft = dateslots[timerange]
                    if slotsleft > 0:
                        return {'bookinfo': {'Booking Type': 'Guided Tour', 'Date': pickedate, 'Time Slot': timerange},
                                'slotinfo': {'Slots left': slotsleft, 'Ticket Types': day.price}}
                    else:
                        print('Ran out of slots')
                else:
                    print('Time Slot not in day')
            else:
                print('Date not available for sale')
    else:
        print('Slot is over/has alr begun')


def dbtoslotform():
    availslots = {}
    now = datetime.now()
    with shelve.open('storage/slots') as slotsDB:
        for datestr, slots in slotsDB.items():
            currdate = date.fromisoformat(datestr)
            if now.date() <= currdate:
                day = {timeslot: left for timeslot, left in slots.availability.items()
                       if left > 0 and now < datetime.combine(currdate, timeslot[0])}
                if day:
                    availslots[datestr] = day
    if not availslots:
        return False
    dates = sorted(availslots.keys())
    firstdate = date.fromisoformat(dates[0])
    lastdate = date.fromisoformat(dates[-1])
    unavaliable = []
    curr_date = firstdate
    while curr_date <= lastdate:
        currstrdate = str(curr_date)
        if currstrdate not in dates:
            unavaliable.append(currstrdate)
        curr_date += timedelta(days=1)
    return {'datepicker': {'startDate': str(firstdate), 'endDate': str(lastdate), 'datesDisabled': unavaliable},
            'avaliable': availslots}


def filterbookings(bookings, filters):
    bookingcount = len(bookings)
    if bookings and filters:
        btype = filters.get('event', 'Select')
        print(btype)
        if btype != 'Select':
            bookings = [booking for booking in bookings if booking.event == btype]
            print(bookings)
        bdate = filters.get('date', '')
        print(bdate)
        if bdate:
            bookings = [booking for booking in bookings if booking.date == bdate]
            print(bookings)
        timeslot = filters.get('timeslot', 'Select')
        print(timeslot)
        if timeslot != 'Select':
            # todo: check format
            bookings = [booking for booking in bookings if booking.timestring == timeslot]
        customer = filters.get('customer', '')
        print(customer)
        if customer:
            bookings = [booking for booking in bookings if booking.name == customer]
    return {'filtered': (bookingcount != len(bookings)), 'form': filters, 'bookings': bookings}
