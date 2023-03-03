import hashlib
import json
import shelve
from classes_Nas import Reward

from flask import session


class Account:
    count: int

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.passwordhash: str
        self.password = password
        self.set_id()

    password = property()

    @password.setter
    def password(self, password):
        self.passwordhash = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest() == self.passwordhash

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
    def set_count(cls):
        with open('storage/config.json', 'r') as config:
            config_data = json.load(config)
        cls.count = config_data['Account.count']

    def update_db(self):
        with shelve.open('storage/users') as usersDB:
            usersDB[self.name] = self

    def update_session(self):
        session['userInfo'] = self


class Staff(Account):
    def __init__(self, name, email, password):
        super().__init__(name, email, password)
        self.role = 'Staff'


class Customer(Account):
    role = 'Customer'
    registerTemplate = 'registerCustomer.html'
    current_points = 2  # Points rewarded for account creation
    used_points = 0     # when accessed and modified from instance will become instance attribute

    def __init__(self, name, email, password):
        super().__init__(name, email, password)
        self.rewards = []

    def add_points(self, points: int):
        """db and session updates"""
        self.current_points += points
        self.update_db()
        self.update_session()

    def use_points(self, points: int):
        """updates both Customer.current_points and Customer.used_points, db and session updates"""
        if points > self.current_points:
            raise ValueError('Not enough points')
        self.current_points -= points
        self.used_points += points
        self.update_db()
        self.update_session()

    @property                   # access like an attribute:
    def total_points(self):     # instance.total_points
        return self.current_points + self.used_points

    def claimReward(self, reward: Reward):
        self.rewards.append(reward)
        self.use_points(reward.points)
        self.update_session()
        self.update_db()

    def useReward(self, reward):
        assert reward in self.rewards, 'Reward does not exist'
        self.rewards.remove(reward)
        self.update_db()
        self.update_session()


Account.set_count()
