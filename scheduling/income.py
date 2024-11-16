
class Income:
    def __init__(self, start: float, duration: float):
        self.start_time = start # belepesi idopont
        self.duration = duration
        self.executed = 0 # eddig lefutott
        self.runs = [] # futasok, from-to tombben

    def increase_executed(self, increment: float):
        self.executed += increment

    def get_runnable_time(self):
        return self.duration - self.executed