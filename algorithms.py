import math
from dataclasses import dataclass
from typing import List, Dict, Tuple
from display import display_schedule, display_gantt_chart
import tkinter as tk
from tkinter import ttk

@dataclass
class Task:
    name: str
    period: float
    runtime: float
    start_time: float
    priority: int
    elapsed: float = 0

    def is_runnable(self, current_time: float) -> bool:
        return self.elapsed < self.runtime and self.start_time <= current_time

    def update_elapsed(self, duration: float) -> None:
        self.elapsed = round(self.elapsed + duration, 1)

    def reset_elapsed(self) -> None:
        self.elapsed = 0

    def get_remaining_runtime(self) -> float:
        return self.runtime - self.elapsed

class TaskScheduler:
    def __init__(self, tasks: List[Task], max_time: float):
        self.tasks = tasks
        self.max_time = max_time
        self.incomes = self._generate_incomes()
        self.completed_tasks = {task.name: [] for task in tasks}

    def _generate_incomes(self) -> Dict[str, List[float]]:
        incomes = {}
        for task in self.tasks:
            income_list = []
            current_income = task.start_time

            while current_income <= self.max_time:
                income_list.append(current_income)
                current_income += task.period

            incomes[task.name] = income_list
        return incomes

    def _get_next_task_run(self, current_time: float) -> Tuple[float, Task]:
        next_runs = []
        next_tasks = []

        if current_time == 59.10000000000001:
            a = 0

        for task in self.tasks:
            task_incomes = self.incomes[task.name]

            for i, income in enumerate(task_incomes):
                if i == 0 and current_time < income:
                    next_runs.append(income)
                    next_tasks.append(task)
                    break

                if i < len(task_incomes) - 1:
                    next_income = task_incomes[i + 1]
                    if income <= current_time < next_income:
                        next_runs.append(task_incomes[i + 1])
                        next_tasks.append(task)
                        break
        if len(next_runs) == 0:
            a = 0
        next_run = min(next_runs)
        next_task = next_tasks[next_runs.index(next_run)]
        return next_run, next_task

    def _update_task_elapsed_times(self, current_time: float, last_iteration_time: float) -> None:
        for task in self.tasks:
            for income in self.incomes[task.name]:
                if last_iteration_time < income <= current_time:
                    task.reset_elapsed()
                    break


    def _merge_consecutive_intervals(self, completed_tasks: Dict[str, List[List[float]]]) -> Dict[str, List[List[float]]]:
        """
        Merges consecutive intervals for the same task.
        Example: [[0, 0.4], [0.4, 0.5]] becomes [[0, 0.5]]
        """
        merged_tasks = {task_name: [] for task_name in completed_tasks}

        for task_name, intervals in completed_tasks.items():
            if not intervals:
                continue

            # Sort intervals by start time
            sorted_intervals = sorted(intervals, key=lambda x: x[0])

            current_interval = list(sorted_intervals[0])  # Convert to list to make it mutable

            for interval in sorted_intervals[1:]:
                # If current interval's end time equals next interval's start time
                if abs(current_interval[0] + current_interval[1] - interval[0]) < 0.0001:  # Using small epsilon for float comparison
                    # Extend current interval
                    current_interval[1] += interval[1]
                else:
                    # Add the completed interval and start a new one
                    merged_tasks[task_name].append(current_interval)
                    current_interval = list(interval)

            # Add the last interval
            merged_tasks[task_name].append(current_interval)

        return merged_tasks

    def _get_runnable_tasks(self, current_time: float) -> List[Task]:
        return [task for task in self.tasks if task.is_runnable(current_time)]

    def _get_highest_priority_task(self, runnable_tasks: List[Task]) -> Task:
        if not runnable_tasks:
            return self.tasks[-1]  # Return Empty task
        return min(runnable_tasks, key=lambda x: x.priority)

    def _calculate_actual_duration(self, current_time: float, task: Task, next_run: float) -> float:
        max_possible_duration = task.runtime - task.elapsed
        time_until_next_run = next_run - current_time
        actual_duration = min(time_until_next_run, max_possible_duration)
        return round(actual_duration, 1)

    def schedule_rate_monotonic(self) -> Dict[str, List[List[float]]]:
        current_time = 0
        last_iteration_time = 0

        while current_time < self.max_time:

            # Update elapsed times based on income periods
            self._update_task_elapsed_times(current_time, last_iteration_time)

            # Get runnable tasks and highest priority task
            runnable_tasks = self._get_runnable_tasks(current_time)
            current_task = self._get_highest_priority_task(runnable_tasks)

            # Calculate next run time and duration
            next_run, _ = self._get_next_task_run(current_time)
            actual_duration = self._calculate_actual_duration(current_time, current_task, next_run)

            # Update task state and record completion
            current_task.update_elapsed(actual_duration)
            self.completed_tasks[current_task.name].append([round(current_time, 1), actual_duration])

            # Prepare for next iteration
            last_iteration_time = current_time
            current_time += actual_duration
            current_time = round(current_time, 1)
            print(current_time)

        return self._merge_consecutive_intervals(self.completed_tasks)

class TaskTimelineGUI:
    def __init__(self, completed_tasks: Dict[str, List[List[float]]]):
        # Initialize window
        self.window = tk.Tk()
        self.window.title("Task Timeline")
        self.window.geometry("600x400")

        # Create main frame with scrollbar
        main_frame = tk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)

        # Create canvas with scrollbar
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack scrollbar components
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Style configuration
        style = ttk.Style()
        style.configure("Header.TLabel", font=('Arial', 10, 'bold'))
        style.configure("Row.TLabel", font=('Arial', 10))

        # Create headers
        header_frame = ttk.Frame(self.scrollable_frame)
        header_frame.pack(fill="x", pady=(0, 5))

        ttk.Label(header_frame, text="Task Name", width=30, style="Header.TLabel").pack(side="left", padx=5)
        ttk.Label(header_frame, text="Runtime (ms)", width=20, style="Header.TLabel").pack(side="left", padx=5)

        # Add separator after header
        ttk.Separator(self.scrollable_frame, orient='horizontal').pack(fill='x', pady=5)

        # Convert and sort timeline data
        timeline_data = []
        for task_name, intervals in completed_tasks.items():
            for start_time, duration in intervals:
                end_time = round(start_time + duration, 1)
                timeline_data.append((task_name, start_time, end_time))

        timeline_data.sort(key=lambda x: x[1])  # Sort by start time

        # Create rows for each task execution
        for i, (task_name, start_time, end_time) in enumerate(timeline_data):
            row_frame = ttk.Frame(self.scrollable_frame)
            row_frame.pack(fill="x", pady=2)

            # Configure row background
            row_bg = '#f0f0f0' if i % 2 == 0 else 'white'
            row_frame.configure(style='Row.TFrame')

            ttk.Label(
                row_frame,
                text=task_name,
                width=30,
                style="Row.TLabel",
                background=row_bg
            ).pack(side="left", padx=5)

            time_text = f"{start_time:.1f} - {end_time:.1f}"
            ttk.Label(
                row_frame,
                text=time_text,
                width=20,
                style="Row.TLabel",
                background=row_bg
            ).pack(side="left", padx=5)

            # Add separator after each row
            ttk.Separator(self.scrollable_frame, orient='horizontal').pack(fill='x')

def display_timeline_gui(completed_tasks: Dict[str, List[List[float]]]):
    """
    Display the task timeline in a GUI window.

    Args:
        completed_tasks: Dictionary with task names as keys and list of [start_time, duration] as values
    """
    app = TaskTimelineGUI(completed_tasks)
    app.window.mainloop()

# Example usage in your main code:
def main():
    # Your existing Task and TaskScheduler code here...
    tasks = [    #TODO: Task(name, period, runtime, start_time, priority)
        Task("Server Task", 10, 0.5, 0, 0),
        Task("Task 1", 40, 10, 35.1, 1),
        Task("Task 2", 80, 15, 20.2, 2),
        Task("Task 3", 160, 20, 25.3, 3),
        Task("Task 4", 320, 75, 0.4, 4),
        Task("Empty", 10000, 3000, 0, 5) ## Ne módosítds ide kerülnek a kihasználatlan processzoridők
    ]
    # TODO: LNKO a max time-hoz
    scheduler = TaskScheduler(tasks, max_time=320)
    completed_times = scheduler.schedule_rate_monotonic()

    empty_time_sum = 0
    for time in completed_times["Empty"]:
        empty_time_sum += time[1]

    print(f"Empty time sum: {empty_time_sum}")

    # Display the GUI
    display_timeline_gui(completed_times)
    display_schedule(completed_times)

if __name__ == "__main__":
    main()

