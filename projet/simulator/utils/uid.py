class UID:
    def __init__(self):
        self.state = 0

    def get(self):
        self.state += 1
        return self.state
