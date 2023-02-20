import hashlib
import json
import shelve

from flask import session


class Account:
    count = 0

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.set_id()

    def check_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest() == self.passwordhash

    def set_password(self, password):
        self.passwordhash = hashlib.sha256(password.encode()).hexdigest()

    password = property(None, set_password)

    def set_id(self):
        self.id = self.count
        self.__class__.count += 1
        with open("storage/config.json", "r+") as config_file:
            config = json.load(config_file)
            config["Account.count"] = self.count
            json.dump(config, config_file)
            config_file.seek(0)
            json.dump(config, config_file)
            config_file.truncate()

    @classmethod
    def update_count(cls):
        with open('storage/config.json', 'r') as config:
            config_data = json.load(config)
        cls.count = config_data['Account.count']

    def update_db(self):
        with shelve.open('storage/users') as usersDB:
            usersDB[self.name] = self


class Staff(Account):
    def __init__(self, name, email, password):
        super().__init__(name, email, password)
        self.role = 'Staff'


class Customer(Account):
    role = 'Customer'
    registerTemplate = 'registerCustomer.html'
    current_points = 2  # Points rewarded for account creation, when accessed and modified from instance will become instance attribute

    def __init__(self, name, email, password):
        super().__init__(name, email, password)
        self.used_points = 0
        self.rewards = []
# [{'voucher': 'Opening Sale: 50% off workshop', 'redeemDate': '28/2/2023', 'used': False},

    def add_points(self, points):
        self.current_points += points
        # Ways to get points:
        # Tour: 3
        # Workshop: 8

    def use_points(self, points):
        self.current_points -= points
        self.used_points += points

    @property                   # access like an attribute:
    def total_points(self):     # instance.total_points
        return self.current_points + self.used_points

    def addRewards(self, points):
        if points > self.total_points:
            return 'Not enough points'
        match points:
            case 5: self.rewards.append("$1 off any dish in café")
            case 9: self.rewards.append("$2 off any dish in café")
            case 15: self.rewards.append("10% off for guided tour")
            case 25: self.rewards.append("20% off for guided tour")
            case 17: self.rewards.append("10% off for workshop")
            case 30: self.rewards.append("20% off for workshop")
            case _: return ValueError
        session['userInfo'] = self

    def delRewards(self, reward):
        if reward not in self.rewards:
            return 'This reward does not exist'
        self.rewards.remove(reward)


Account.update_count()
