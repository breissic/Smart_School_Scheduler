from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QListWidget, QLineEdit, QFormLayout, \
    QTextEdit, QComboBox, QSpinBox, QDateEdit, QMessageBox, QStackedWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize, QDate
from database import TaskDatabase  # Import the TaskDatabase class


class ADM(QWidget):
    def __init__(self, home_callback, update_view_callback):
        super().__init__()
        self.db = TaskDatabase()  # Initialize the database
        self.home_callback = home_callback
        self.update_view_callback = update_view_callback  # Callback to update the view
        self.current_task_id = None  # Track the currently selected task's ID
        self.is_adding_task = False  # Track whether we are adding a new task
        self.initUI()
        self.loadTasks()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Top bar layout for home button
        topBarLayout = QHBoxLayout()
        homeButton = QPushButton()
        homeButton.setIcon(QIcon('home.png'))
        homeButton.setIconSize(QSize(40, 40))
        homeButton.clicked.connect(self.home_callback)
        topBarLayout.addWidget(homeButton, alignment=Qt.AlignRight)  # Right align the home button
        layout.addLayout(topBarLayout)

        # Main horizontal layout
        mainLayout = QHBoxLayout()

        # Left column for tasks
        leftLayout = QVBoxLayout()
        addTaskButton = QPushButton("Add Task")
        addTaskButton.clicked.connect(self.startAddTask)
        leftLayout.addWidget(addTaskButton)

        # List for displaying tasks
        self.taskList = QListWidget()
        self.taskList.currentItemChanged.connect(self.taskSelected)
        leftLayout.addWidget(self.taskList)

        # Right area for task details
        self.detailsWidget = QWidget()  # A widget to hold the details layout
        self.detailsLayout = QVBoxLayout(self.detailsWidget)
        self.nameEdit = QLineEdit()
        self.descriptionEdit = QTextEdit()
        self.descriptionEdit.setMaximumHeight(100)

        # SpinBox for the number of days to devote to the task
        self.daysSpinBox = QSpinBox()
        self.daysSpinBox.setMinimum(1)
        self.daysSpinBox.setMaximum(30)
        self.daysSpinBox.setFixedWidth(100)

        # Dropdown for workload level
        self.workloadComboBox = QComboBox()
        self.workloadComboBox.addItems(["Light", "Moderate", "Heavy"])
        self.workloadComboBox.setFixedWidth(150)

        # Date picker for due date
        self.dueDateEdit = QDateEdit()
        self.dueDateEdit.setCalendarPopup(True)
        self.dueDateEdit.setDate(QDate.currentDate())

        # Save button
        saveButton = QPushButton("Save Task")
        saveButton.clicked.connect(self.saveTask)

        # Complete button
        completeButton = QPushButton("Complete Task")
        completeButton.clicked.connect(self.completeTask)

        # Cancel button
        cancelButton = QPushButton("Cancel")
        cancelButton.clicked.connect(self.cancelTask)

        formLayout = QFormLayout()
        formLayout.addRow("Name:", self.nameEdit)
        formLayout.addRow("Description:", self.descriptionEdit)
        formLayout.addRow("Days to Devote:", self.daysSpinBox)
        formLayout.addRow("Workload Level:", self.workloadComboBox)
        formLayout.addRow("Due Date:", self.dueDateEdit)
        formLayout.addRow("", saveButton)
        formLayout.addRow("", completeButton)
        formLayout.addRow("", cancelButton)
        self.detailsLayout.addLayout(formLayout)

        # Stacked widget to switch between empty and details view
        self.rightPanel = QStackedWidget()
        self.emptyWidget = QLabel("Select a task or click 'Add Task' to begin.")
        self.rightPanel.addWidget(self.emptyWidget)
        self.rightPanel.addWidget(self.detailsWidget)
        self.rightPanel.setCurrentWidget(self.emptyWidget)

        # Combine layouts
        mainLayout.addLayout(leftLayout, 1)
        mainLayout.addWidget(self.rightPanel, 4)

        layout.addLayout(mainLayout)
        # Set the main layout
        self.setLayout(layout)

    def loadTasks(self):
        self.taskList.clear()
        tasks = self.db.get_tasks()
        for task in tasks:
            self.taskList.addItem(f"{task['id']}: {task['name']}")
        # print("Tasks loaded:", [task['name'] for task in tasks])  # Debugging statement

    def startAddTask(self):
        self.is_adding_task = True
        self.current_task_id = None
        self.nameEdit.clear()
        self.descriptionEdit.clear()
        self.daysSpinBox.setValue(1)
        self.workloadComboBox.setCurrentIndex(0)
        self.dueDateEdit.setDate(QDate.currentDate())
        self.rightPanel.setCurrentWidget(self.detailsWidget)  # Show the details view
        # print("Started adding a new task")  # Debugging statement

    def taskSelected(self, current, previous):
        if current and not self.is_adding_task:
            task_id, task_name = current.text().split(": ")
            task = self.db.get_task_by_id(int(task_id))
            self.current_task_id = task_id
            self.nameEdit.setText(task['name'])
            self.descriptionEdit.setText(task['description'])
            self.daysSpinBox.setValue(task['days'])
            self.workloadComboBox.setCurrentText(task['workload'])
            self.dueDateEdit.setDate(QDate.fromString(task['due_date'], 'yyyy-MM-dd'))
            self.rightPanel.setCurrentWidget(self.detailsWidget)  # Show the details view
            print(f"Task selected: {task['name']} with ID: {self.current_task_id}")  # Debugging statement
        elif not current:
            self.rightPanel.setCurrentWidget(self.emptyWidget)  # Show the empty view
            # print("No task selected, showing empty view")  # Debugging statement

    def saveTask(self):
        if not self.nameEdit.text().strip():
            QMessageBox.warning(self, "Error", "Task name cannot be empty.")
            return

        name = self.nameEdit.text()
        description = self.descriptionEdit.toPlainText()
        days = self.daysSpinBox.value()
        workload = self.workloadComboBox.currentText()
        due_date = self.dueDateEdit.date().toString('yyyy-MM-dd')

        # print(f"Saving task with ID: {self.current_task_id}")  # Debugging statement

        if self.is_adding_task:
            task_id = self.db.add_task(name, description, days, workload, due_date)
            self.taskList.addItem(f"{task_id}: {name}")
            self.is_adding_task = False
            # print(f"Added new task with ID: {task_id}")  # Debugging statement
        elif self.current_task_id:
            self.db.update_task(int(self.current_task_id), name, description, days, workload, due_date)
            current_item = self.taskList.currentItem()
            if current_item:
                current_item.setText(f"{self.current_task_id}: {name}")
            # print(f"Updated task with ID: {self.current_task_id}")  # Debugging statement
        else:
            QMessageBox.warning(self, "Error", "No task selected.")
            # print("Error: No task selected")  # Debugging statement

        self.update_view_callback()  # Update the view
        self.rightPanel.setCurrentWidget(self.emptyWidget)  # Show the empty view
        self.clearSelection()

    def completeTask(self):
        # print(f"Completing task with ID: {self.current_task_id}")  # Debugging statement
        if self.current_task_id:
            self.db.delete_task(int(self.current_task_id))
            current_item = self.taskList.currentItem()
            if current_item:
                self.taskList.takeItem(self.taskList.row(current_item))
            self.update_view_callback()  # Update the view
            self.rightPanel.setCurrentWidget(self.emptyWidget)  # Show the empty view
            self.clearSelection()  # Clear selection and reset state
            self.loadTasks()  # Reload tasks to ensure the list is updated
            # print("Task completed and removed")  # Debugging statement
        else:
            QMessageBox.warning(self, "Error", "No task selected.")
            # print("Error: No task selected")  # Debugging statement

    def cancelTask(self):
        self.rightPanel.setCurrentWidget(self.emptyWidget)  # Show the empty view
        self.is_adding_task = False

        # Clear the selection and reset it to ensure proper state
        self.clearSelection()
        # print("Task addition cancelled")  # Debugging statement

    def clearSelection(self):
        self.taskList.clearSelection()
        self.taskList.setCurrentItem(None)
        self.current_task_id = None
        # print("Selection cleared")  # Debugging statement

    def loadTask(self, task):
        self.is_adding_task = False
        self.current_task_id = task['id']
        self.nameEdit.setText(task['name'])
        self.descriptionEdit.setText(task['description'])
        self.daysSpinBox.setValue(task['days'])
        self.workloadComboBox.setCurrentText(task['workload'])
        self.dueDateEdit.setDate(QDate.fromString(task['due_date'], 'yyyy-MM-dd'))
        self.rightPanel.setCurrentWidget(self.detailsWidget)  # Show the details view
        # print(f"Loaded task with ID: {self.current_task_id}")  # Debugging statement

    def closeEvent(self, event):
        self.db.close()
        event.accept()
