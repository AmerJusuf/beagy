from scheduling.income import Income


class Task:
    def __init__(self, name, period, runtime, start_time, max_time):
        self.name = name
        self.period = period
        self.runtime = runtime
        self.start_time = start_time
        self.incomes = []
        self.max_time = max_time
        self.generate_incomes()

    def generate_incomes(self):
        current = self.start_time
        while current < self.max_time:
            self.incomes.append(Income(current, self.runtime))
            current += self.period

    def get_next_income(self, current_time):
        for income in self.incomes:
            if income.start_time <= current_time and income.executed < income.duration:
                return income
        return None

    def get_period(self):
        return self.period
