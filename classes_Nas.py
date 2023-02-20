from datetime import date
from flask import session
import shelve
from hashlib import sha256
import json


class Reward:
    voucher: str
    points: int
    count: int

    def __init__(self, customer):
        self.date = date.today()
        self.used = False
        self.customer = customer
        self.deductpoints(customer)
        self.id: int
        self.set_id()

    def deductpoints(self, customer):
        customer.use_points(self.points)
        customer.update_db()

    @property
    def code(self):
        return hashlib.sha256(self.voucher.encode()).hexdigest()[:5]

    @classmethod
    def set_count(cls):
        with open('storage/config.json', 'r') as config:
            config_data = json.load(config)
        cls.count = config_data['Reward.count']

    def set_id(self):
        self.id = self.count
        self.__class__.count += 1
        with open("storage/config.json", "r+") as config_file:
            config = json.load(config_file)
            config["Reward.count"] = self.count
            config_file.seek(0)
            json.dump(config, config_file)
            config_file.truncate()


Reward.set_count()


class Guidedtour10(Reward):
    voucher = "10% off for guided tour"
    code = "a1674"
    points = 15

    @staticmethod
    def discount(subtotal):
        return -(subtotal * 0.1)


class Guidedtour20(Reward):
    voucher = "20% off for guided tour"
    points = 25

    @staticmethod
    def discount(subtotal):
        return -(subtotal * 0.2)


class Cafe1(Reward):
    voucher = "$1 off any dish in café "
    points = 5

    @staticmethod
    def discount(subtotal):
        return -1


class Cafe2off(Reward):
    voucher = "$2 off any dish in café"
    points = 9

    @staticmethod
    def discount(subtotal):
        return -2


class Workshop10(Reward):
    voucher = "10% off for workshop"
    points = 17

    @staticmethod
    def discount(subtotal):
        return -(subtotal * 0.1)


class Workshop20(Reward):
    voucher = "20% off for workshop"
    points = 30

    @staticmethod
    def discount(subtotal):
        return -(subtotal * 0.2)
