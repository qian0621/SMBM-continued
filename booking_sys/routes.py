from flask import render_template, request, redirect, url_for, session, jsonify, abort, flash, Blueprint
import shelve
from products_Sixuan import Slots
from datetime import date, time, datetime, timedelta
from re import match
from booking_sys.models import Booking
import json
from errors import ShownError

booking_sys = Blueprint('booking_sys', __name__, template_folder='templates', static_folder='static')


@booking_sys.route('/', methods=['GET', 'POST'])
def makebooking():
    errors = {}
    datetimetime = request.args.get('slot')
    if datetimetime:                                    # desired time slot submitted
        try:
            slotinfo = getslotinfo(*strtodatetime(datetimetime))
            print(slotinfo)     # {date:str, timeslot:tuple}, {left:int, ticketypes:dict}
            return booktickets(slotinfo)            # POST form booking details
        except ShownError as e:
            errors[e.display_element_id] = e
    # load pick timeslot form
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
        try:
            tickets = procorder(prevsubmit, slotinfo)
        except ShownError as e:
            errors[e.display_element_id] = e
        else:
            if 'userInfo' in session:
                customerid = {'customer': session['userInfo']}
            else:
                customerid = {'email': ''}
            madebooking = Booking(day=slotinfo['bookinfo']['Date'],
                                  event=slotinfo['bookinfo']['Booking Type'],
                                  tickets=tickets,
                                  requests=prevsubmit['requests'],
                                  timeslot=slotinfo['bookinfo']['Time Slot'],
                                  **customerid)
            flash(madebooking.mail(), 'noti')
            return redirect(url_for('.abooking', customerName=madebooking.name, bookingid=madebooking.id))
    print(errors)   # ticketype, claim
    slotinfo['bookinfo']['Time Slot'] = "{:%I:%M %p} - {:%I:%M %p}".format(*slotinfo['bookinfo']['Time Slot'])
    return render_template('bookingtickets.html',
                           **slotinfo,
                           tickets={},
                           form=prevsubmit,
                           errors=errors,
                           customerAcc=('userInfo' in session and session['userInfo'].role == 'Customer'))


@booking_sys.route('/voucher')
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


@booking_sys.route('/mybookings')
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


@booking_sys.route('/<string:customerName>/<int:bookingid>', methods=['GET', 'POST', 'DELETE'])
@booking_sys.route('/<string:customerName>/<int:bookingid>/<string:back>/<string:link>', methods=['GET', 'POST', 'DELETE'])
def abooking(customerName, bookingid, back='My Bookings', link='.mybookings'):
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


@booking_sys.route('/all')
def allbookings():
    filters = request.args
    print(filters)
    if 'userInfo' in session and session['userInfo'].role == 'Staff':
        with shelve.open('storage/bookings') as bookingsDB:
            custbookings = [booking for acustbooking in bookingsDB.values() for booking in acustbooking]
        return render_template('viewbookings.html', staff=True, **filterbookings(custbookings, filters))
    else:
        abort(403, "Only staff allowed")


def strtodatetime(datetimetime: str) -> tuple[str, tuple[time, time]]:
    # 2023-01-18.15:00:00_15:45:00
    pattern = r"^\d{4}-\d{2}-\d{2}\.\d{2}:\d{2}:\d{2}_\d{2}:\d{2}:\d{2}$"
    if match(pattern, datetimetime) is not None:
        try:
            pickedate, timerange = datetimetime.split('.')
            timerange = tuple([time.fromisoformat(startend) for startend in timerange.split('_')])
            # ValueError: hour must be in 0..23
            return pickedate, timerange
        except ValueError as e:
            raise ShownError("Sorry, there was a date time format error. Please try again", e,
                             display_element_id='slot-error')
    else:
        raise ShownError("Sorry, there was a date time format error. Please try again",
                         display_element_id='slot-error')


def getslotinfo(datestr: str, timerange: tuple[time, time])\
        -> dict[str, dict[str, str | tuple[time, time]] | dict[str, int | dict[str, int]]]:
    try:
        pickedate = date.fromisoformat(datestr)
    except ValueError as e:  # ValueError: day is out of range for month
        raise ShownError("Sorry, there was a date time format error. Please try again", e,
                         display_element_id='slot-error')
    if datetime.now() <= datetime.combine(pickedate, timerange[0]):
        with shelve.open('storage/slots') as slotsDB:
            try:
                return slotsDB[datestr].slotinfo(timerange)
                # ShownError('Sorry, the time slot you picked has sold out. Please choose another')
                # ShownError('Sorry, the time slot you picked is not available on that date', e)
            except KeyError as e:   # if datestr not in slotsDB
                raise ShownError('Sorry, the date you picked is not available. Please pick another', e,
                                 display_element_id='slot-error')
    else:
        raise ShownError('Sorry, the slot you picked is over or has already begun. Please pick another',
                         display_element_id='slot-error')


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


def procorder(order, slotinfo):
    if not any([ticketype in order for ticketype in slotinfo['slotinfo']['Ticket Types']]):
        raise ShownError('Your cart is empty, please pick a Concession or Adult ticket before checkout',
                         display_element_id='cart-error')
    if not ('Adult' in order or 'Concession' in order):
        raise ShownError('Children under 7 need to be accompanied by an adult, '
                         'please buy at least 1 Adult or Concession ticket',
                         display_element_id='cart-error')
    tickets = {}
    ticketcount = 0
    for key, value in order.items():
        if key in slotinfo['slotinfo']['Ticket Types']:
            try:
                quantity = int(value)
                if quantity > 0:
                    ticketcount += quantity
                    tickets[key] = quantity
                    if ticketcount > slotinfo['slotinfo']['Slots left']:
                        raise ShownError(display_element_id='soldout')
                else:
                    raise ValueError("Value must be a positive integer")
            except ValueError as e:
                raise ShownError('Invalid value, please enter a positive integer', e,
                                 display_element_id=key)
        elif key == 'claimed':
            if value:
                try:
                    claims = json.loads(value)
                except json.decoder.JSONDecodeError as e:
                    raise ShownError('Sorry, there was a reward format error. Please try again', e,
                                     display_element_id='cart-error')
                try:
                    user = session['userInfo']
                    userewards = user.rewards
                except KeyError as e:
                    raise ShownError('You need to login to claim your rewards', e, display_element_id='cart-error')
                except AttributeError as e:
                    raise ShownError('Rewards are only available to customers', e, display_element_id='cart-error')
                for claim in claims:
                    claimed = False
                    for reward in userewards:
                        if str(reward.id) == claim:
                            userewards.remove(reward)
                            user.update_db()
                            claimed = True
                            break
                    if not claimed:
                        raise ShownError('Sorry, the reward you claimed is not available, please remove from cart',
                                         display_element_id='cart-error')
    return tickets


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
