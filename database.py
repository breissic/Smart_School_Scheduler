import sqlite3

class TaskDatabase:
    def __init__(self, db_name="tasks.db"):
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row  # Access columns by name
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                days INTEGER NOT NULL,
                workload TEXT NOT NULL,
                due_date TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def add_task(self, name, description, days, workload, due_date):
        self.cursor.execute(
            "INSERT INTO tasks (name, description, days, workload, due_date) VALUES (?, ?, ?, ?, ?)",
            (name, description, days, workload, due_date)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def get_tasks(self):
        self.cursor.execute("SELECT id, name, description, days, workload, due_date FROM tasks")
        return self.cursor.fetchall()

    def get_task_by_id(self, task_id):
        self.cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        return self.cursor.fetchone()

    def update_task(self, task_id, name, description, days, workload, due_date):
        self.cursor.execute(
            "UPDATE tasks SET name = ?, description = ?, days = ?, workload = ?, due_date = ? WHERE id = ?",
            (name, description, days, workload, due_date, task_id)
        )
        self.conn.commit()

    def delete_task(self, task_id):
        self.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()
