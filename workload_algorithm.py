from datetime import datetime, timedelta

from database import TaskDatabase


def fetch_tasks():
    db = TaskDatabase()
    tasks = db.get_tasks()
    db.close()
    return tasks


def normalize(v, mi, ma):
    if ma == mi:
        return 0
    return (v - mi) / (ma - mi)


def priority_score(tasks):
    if not tasks:
        return []

    max_time = max((datetime.strptime(task['due_date'], '%Y-%m-%d') - datetime.today()).days for task in tasks)
    max_days = max(task['days'] for task in tasks)
    w = 1.5  # workload weight
    u = 2.0  # urgency weight
    d = 1.25  # days to work weight
    priority_scores = []
    for task in tasks:
        workload = task['workload']
        wlscore = 0
        due_date = datetime.strptime(task['due_date'], '%Y-%m-%d')
        days_to_work = task['days']
        if workload == 'light':
            wlscore = 1
        elif workload == 'moderate':
            wlscore = 2
        elif workload == 'heavy':
            wlscore = 3
        diff = due_date - datetime.today()
        time_to_due = diff.days
        normalized_time_to_due = 1 - normalize(time_to_due, 0, max_time)
        normalized_days_to_work = 1 - normalize(days_to_work, 0, max_days)
        score = (w * wlscore + u * normalized_time_to_due + d * normalized_days_to_work) / (w + u + d)
        priority_scores.append((task, score))  # Return a tuple of task and score
    return priority_scores


def distribute_workdays(tasks_with_scores):
    # Sort tasks by priority score (higher scores first)
    tasks_with_scores.sort(key=lambda x: x[1], reverse=True)

    schedule = {}
    today = datetime.today().date()

    for task, score in tasks_with_scores:
        due_date = datetime.strptime(task['due_date'], '%Y-%m-%d').date()
        days_to_work = task['days']
        days_allocated = 0

        current_date = today

        while days_allocated < days_to_work and current_date < due_date:
            if current_date not in schedule:
                schedule[current_date] = []

            # Allocate the workday for the task if there is room
            if len(schedule[current_date]) < 3:  # Example limit: max 3 tasks per day
                schedule[current_date].append(task)
                days_allocated += 1

            current_date += timedelta(days=1)

        # Always mark the due date
        if due_date not in schedule:
            schedule[due_date] = []
        schedule[due_date].append(task)

    return schedule


def workload_algorithm():
    tasks = fetch_tasks()
    tasks_with_scores = priority_score(tasks)
    schedule = distribute_workdays(tasks_with_scores)
    return schedule
