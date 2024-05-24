from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QListWidget,
                             QLineEdit, QFormLayout, QTextEdit, QComboBox, QSpinBox, QMessageBox, QStackedWidget)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from database import TaskDatabase  # Import the TaskDatabase class

class ADM(QWidget):
    def __init__(self, home_callback):
        super().__init__()
        self.db = TaskDatabase()  # Initialize the database
        self.home_callback = home_callback
        self.current_task_id = None  # Track the currently selected task's ID
        self.is_adding_task = False  # Track whether we are adding a new task
        self.initUI()
        self.loadTasks()

    def initUI(self):
        layout = QHBoxLayout(self)

        # Top bar layout for home button
        topBarLayout = QHBoxLayout()
        homeButton = QPushButton()
        homeButton.setIcon(QIcon('home.png'))
        homeButton.setIconSize(QSize(40, 40))
        homeButton.clicked.connect(self.home_callback)
        topBarLayout.addWidget(homeButton, alignment=Qt.AlignRight)  # Right align the home button
        layout.addLayout(topBarLayout)

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

        # Save button
        saveButton = QPushButton("Save Task")
        saveButton.clicked.connect(self.saveTask)

        # Complete button
        completeButton = QPushButton("Complete Task")
        completeButton.clicked.connect(self.completeTask)

        formLayout = QFormLayout()
        formLayout.addRow("Name:", self.nameEdit)
        formLayout.addRow("Description:", self.descriptionEdit)
        formLayout.addRow("Days to Devote:", self.daysSpinBox)
        formLayout.addRow("Workload Level:", self.workloadComboBox)
        formLayout.addRow("", saveButton)
        formLayout.addRow("", completeButton)
        self.detailsLayout.addLayout(formLayout)

        # Stacked widget to switch between empty and details view
        self.rightPanel = QStackedWidget()
        self.emptyWidget = QLabel("Select a task or click 'Add Task' to begin.")
        self.rightPanel.addWidget(self.emptyWidget)
        self.rightPanel.addWidget(self.detailsWidget)
        self.rightPanel.setCurrentWidget(self.emptyWidget)

        # Combine layouts
        layout.addLayout(leftLayout, 1)
        layout.addWidget(self.rightPanel, 4)

        # Set the main layout
        self.setLayout(layout)

    def loadTasks(self):
        tasks = self.db.get_tasks()
        for task in tasks:
            self.taskList.addItem(f"{task['id']}: {task['name']}")

    def startAddTask(self):
        self.is_adding_task = True
        self.current_task_id = None
        self.nameEdit.clear()
        self.descriptionEdit.clear()
        self.daysSpinBox.setValue(1)
        self.workloadComboBox.setCurrentIndex(0)
        self.rightPanel.setCurrentWidget(self.detailsWidget)  # Show the details view

    def taskSelected(self, current, previous):
        if current:
            self.is_adding_task = False
            task_id, task_name = current.text().split(": ")
            task = self.db.get_task_by_id(int(task_id))
            self.current_task_id = task_id
            self.nameEdit.setText(task['name'])
            self.descriptionEdit.setText(task['description'])
            self.daysSpinBox.setValue(task['days'])
            self.workloadComboBox.setCurrentText(task['workload'])
            self.rightPanel.setCurrentWidget(self.detailsWidget)  # Show the details view

    def saveTask(self):
        name = self.nameEdit.text()
        description = self.descriptionEdit.toPlainText()
        days = self.daysSpinBox.value()
        workload = self.workloadComboBox.currentText()

        if self.is_adding_task:
            if name == "" or name == " ":
                QMessageBox.warning(self, "Error", "Task must have a name")
                return
            task_id = self.db.add_task(name, description, days, workload)
            self.taskList.addItem(f"{task_id}: {name}")
            self.is_adding_task = False
        elif self.current_task_id:
            if name == "" or name == " ":
                QMessageBox.warning(self, "Error", "Task must have a name")
                return
            self.db.update_task(int(self.current_task_id), name, description, days, workload)
            # Update the task name in the list
            current_item = self.taskList.currentItem()
            current_item.setText(f"{self.current_task_id}: {name}")
        else:
            QMessageBox.warning(self, "Error", "No task selected.")

    def completeTask(self):
        if self.current_task_id:
            self.db.delete_task(int(self.current_task_id))
            self.taskList.takeItem(self.taskList.currentRow())
            self.rightPanel.setCurrentWidget(self.emptyWidget)  # Show the empty view
            self.current_task_id = None
        else:
            QMessageBox.warning(self, "Error", "No task selected.")

    def closeEvent(self, event):
        self.db.close()
        event.accept()