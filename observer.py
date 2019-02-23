class Subscriber:

    def __init__(self, name):
        self.name = name

    def update(self, message):
        print ("{} just got this: {} as a message".format(self.name, message))


class Publisher:

    def __init__(self):
        self.subscribers = set()

    def register(self, sub):
        self.subscribers.add(sub)

    def dispatch(self, message):
        for subscriber in self.subscribers:
            subscriber.update("I just watched mary Jeam")
