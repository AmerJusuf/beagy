from algorithms import display_timeline_gui
from display import display_gantt_chart, display_schedule
from scheduling.rm_scheduler import Scheduler
from scheduling.task import Task


def main():
    tasks = [
        #TODO: Task(name, period, runtime, start_time, priority)
        #Task("Server Task", 2, 0.5, 0, 6),
        Task("Task 1", 8, 2, 3.1, 64),
        Task("Task 2", 16, 3, 4.2, 64),
        Task("Task 3", 32, 4, 1.3, 64),
        Task("Task 4", 64, 15, 0.4, 64),
       # Task("Empty", 10000, 3000, 0, 5) ## Ne módosítds ide kerülnek a kihasználatlan processzoridők
    ]
    scheduler = Scheduler(tasks, 2, 0.5, 64)
    scheduler.run_rm()
    joined_tasks = scheduler.get_joined_scheduled_tasks()
    print(joined_tasks)
    display_timeline_gui(joined_tasks)
    display_schedule(joined_tasks)

if __name__ == "__main__":
    main()