# Feedback class
class Feedback:
    count_id = 0

    # initializer method
    def __init__(self, name, email, feedbacks):
        Feedback.count_id += 1
        self.__feedback_id = Feedback.count_id
        self.__name = name
        self.__email = email
        self.__feedbacks = feedbacks

    # accessor methods
    def get_feedback_id(self):
        return self.__feedback_id

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_feedbacks(self):
        return self.__feedbacks

    # mutator methods
    def set_feedback_id(self, feedback_id):
        self.__feedback_id = feedback_id

    def set_name(self, name):
        self.__name = name

    def set_email(self, email):
        self.__email = email

    def set_feedbacks(self, feedbacks):
        self.__feedbacks = feedbacks
