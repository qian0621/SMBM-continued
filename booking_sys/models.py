from datetime import time, date
import shelve
import json
from user_classes import *
from flask import session, flash, request, url_for
from yagmail import SMTP

mailer = SMTP('ninaqing2005@gmail.com', 'syyqlvyooeejeafj')


class Booking:
    count: int
    count_storage = "storage/config.json"
    storage = 'storage/bookings'
    slot_storage = 'storage/slots'
    points = 3

    def __init__(self, day: str, event: str, tickets: dict, requests: str,
                 timeslot: time | tuple[time, time] | None = None,
                 customer: Account | None = None, name: str | None = None, email: str | None = None):

        # Booking(day='2023-02-12',
        #         event='Guided Tour',
        #         tickets={'Concession': 2, 'Child': 1},
        #         requests='Is this museum child proof?',
        #         timeslot=(time(14), time(14, 45)),
        #         email='ignoredandsilent@gmail.com')

        self.name = None
        self.email = None
        self.customer = customer
        self.dbkey = None

        if self.customer:
            self.name = customer.name
            self.email = customer.email
            self.dbkey = self.name
            if self.customer.role == 'Customer':
                self.add_points()

        if name:
            self.name = name

        if email:
            self.email = email
            if not self.name:
                self.name = email

        if not self.dbkey:
            if self.name:
                self.dbkey = self.name
            else:
                raise ValueError("No customer identifier")

        self.event = event
        self.date = day
        self.time = timeslot
        self.tickets = tickets
        self.requests = requests
        self.id: int
        self.set_id()
        self.store()
        self.fillupslot()

    @property
    def pax(self):
        return sum(self.tickets.values())

    def url(self, **kwargs):
        return url_for('.abooking', customerName=self.dbkey, bookingid=self.id, **kwargs)

    @property
    def timestring(self):
        if type(self.time) == time:
            return "{:%I:%M %p}".format(*self.time)
        else:  # tuple
            return "{:%I:%M %p} - {:%I:%M %p}".format(*self.time)

    def set_id(self):
        self.id = self.count
        self.__class__.count += 1
        with open(self.count_storage, "r+") as config_file:
            config = json.load(config_file)
            config["Booking.count"] = self.count
            config_file.seek(0)
            json.dump(config, config_file)
            config_file.truncate()

    def store(self):
        with shelve.open(self.storage, writeback=True) as bookings:
            # customer: their bookings
            if self.dbkey not in bookings:
                bookings[self.dbkey] = [self]
            else:
                bookings[self.dbkey].append(self)

    def add_points(self):
        assert self.customer and self.customer.role == 'Customer', 'Points are only avaliable for logged in customers'
        self.customer.add_points(self.points)

    def fillupslot(self):
        with shelve.open(self.slot_storage, writeback=True) as slotsDB:
            slotsDB[self.date].availability[self.time] -= self.pax

    def freeupslot(self):
        with shelve.open(self.slot_storage, writeback=True) as slotsDB:
            slotsDB[self.date].availability[self.time] += self.pax

    def mail(self):
        body = f"<p>Hi <strong>{self.name}</strong>,</p>" \
               f"<p>You have made a {self.event} booking</p>" \
               "<h4>Booking Details</h4><dl>" \
               f"<dt>ID:</dt><dd>{self.id}</dd>" \
               f"<dt>Date:</dt><dd>{self.date}</dd>" \
               f"<dt>Time:</dt><dd>{self.timestring}</dd>" \
               f"<dt>Tickets:</dt><dd>{self.tickets}</dd>" \
               f"<dt>Requests:</dt><dd>{self.requests}</dd></dl>" \
               f"<p>The meeting point is at the Museum Cafe, look for any staff in the Cafe and show this email or <a href='{request.host_url}{self.url()[1:]}'>your booking</a>. You may purchase your admission ticket at the Museum Cafe by Cash/Grabpay. After receiving your ticket please remain seated at the Museum Cafe, the owner will lead you to the Museum.</p>" \
               "<p>Please don't be late, as it will affect another participant, so we will start on time or your tour might be shorter than usual, thank you for your understanding.</p>" \
               "<p>See you there!<br>" \
               "SMBM Team</p>" \
               "<address>Singapore Musical Box Museum<br>" \
               "168 Telok Ayer Street Singapore 068619<br>" \
               "Tel: +65 6221 0102 | Fax: +65 6221 0103<br>" \
               f"Website: <a href='{request.host_url}{url_for('home')[1:]}'>SMBM</a></address>"
        print(body)
        try:
            mailer.send(to={self.email: self.name},
                        subject=f'Your {self.event} Booking',
                        contents=body)
        except Exception as e:
            print(e)
            return 'Booking email failed to send. ' \
                   '<button class="btn btn-link btn-sm link-light ms-2" id="resend">Retry?</button>'
        else:
            return 'Booking email sent!'

    @classmethod
    def set_count(cls):
        with open(cls.count_storage, 'r') as config:
            config_data = json.load(config)
        cls.count = config_data['Booking.count']

    def info(self, **kwargs):
        return {'bookinfo': {'Booking No.': self.id,
                             'Booking Type': self.event,
                             'Date': self.date,
                             'Time Slot': self.timestring},
                'customer': {'Under the name of': self.name,
                             'Email': self.email},
                'tickets': self.tickets,
                'requests': self.requests,
                'url': self.url(**kwargs)}


Booking.set_count()
