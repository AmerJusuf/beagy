


class Scheduler:
    def __init__(self, tasks, period, runtime, max_time):
        self.tasks = tasks
        self.current_time = 0 + runtime
        self.period = period
        self.runtime = runtime
        self.max_time = max_time
        self.sort_tasks_by_priority()
        self.completed_tasks = {task.name: [] for task in tasks}

    def add_task(self, task):
        self.tasks.append(task)

    def run_rm(self):
        time_to_next_scheduling = self.period + self.runtime
        while self.current_time < self.max_time:
            for task in self.tasks:
                income = task.get_next_income(self.current_time)
                if income is not None:
                    current_runtime = min(time_to_next_scheduling, income.get_runnable_time()) # period + runtime idot futhat (ekkor jon a kovetkezo utemezes)
                    income.increase_executed(current_runtime)
                    self.completed_tasks[task.name].append((self.current_time, self.current_time + current_runtime))
                    break
            self.current_time += time_to_next_scheduling

    def sort_tasks_by_priority(self):
        self.tasks.sort(key=lambda x: x.get_period())

    def get_joined_scheduled_tasks(self):
        EPSILON = 0.001
        result = {}

        for task_name, intervals in self.completed_tasks.items():
            if not intervals:
                result[task_name] = []
                continue

            # Sort intervals by start time
            sorted_intervals = sorted(intervals, key=lambda x: x[0])
            merged = [sorted_intervals[0]]

            for current in sorted_intervals[1:]:
                previous = merged[-1]

                # Check if current interval starts approximately where previous ends
                if abs(previous[1] - current[0]) <= EPSILON:
                    # Merge intervals by updating end time of previous interval
                    merged[-1] = (previous[0], current[1])
                else:
                    merged.append(current)

            result[task_name] = merged

        return result


