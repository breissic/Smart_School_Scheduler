from datetime import datetime, timedelta
from database import TaskDatabase


def fetch_tasks():
    db = TaskDatabase()
    tasks = db.get_tasks()
    db.close()
    return tasks
def workload_algorithm():
    tasks = fetch_tasks()

