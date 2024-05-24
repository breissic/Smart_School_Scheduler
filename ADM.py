from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QListWidget,
                             QStackedWidget, QLineEdit, QFormLayout, QTextEdit, QComboBox, QSpinBox)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize

class ADM(QWidget):
    def __init__(self, home_callback):
        super().__init__()
        self.home_callback = home_callback
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)

        # Left column for tasks
        leftLayout = QVBoxLayout()
        addTaskButton = QPushButton("Add Task")
        addTaskButton.clicked.connect(self.addTask)
        leftLayout.addWidget(addTaskButton)

        # List for displaying tasks
        self.taskList = QListWidget()
        self.taskList.currentItemChanged.connect(self.taskSelected)  # Connect to a slot to handle task selection
        leftLayout.addWidget(self.taskList)

        # Right area for task details
        self.detailsLayout = QVBoxLayout()
        self.nameEdit = QLineEdit()
        self.descriptionEdit = QTextEdit()
        self.descriptionEdit.setMaximumHeight(100)  # Limit the height of the description box

        # SpinBox for the number of days to devote to the task
        self.daysSpinBox = QSpinBox()
        self.daysSpinBox.setMinimum(1)  # Minimum number of days
        self.daysSpinBox.setMaximum(30)  # Arbitrary maximum
        self.daysSpinBox.setFixedWidth(100)  # Set a fixed width to make it less prominent

        # Dropdown for workload level
        self.workloadComboBox = QComboBox()
        self.workloadComboBox.addItems(["Light", "Moderate", "Heavy"])
        self.workloadComboBox.setFixedWidth(150)  # Set a fixed width to make it more balanced

        formLayout = QFormLayout()
        formLayout.addRow("Name:", self.nameEdit)
        formLayout.addRow("Description:", self.descriptionEdit)
        formLayout.addRow("Days to Devote:", self.daysSpinBox)
        formLayout.addRow("Workload Level:", self.workloadComboBox)
        self.detailsLayout.addLayout(formLayout)

        # Combine layouts
        layout.addLayout(leftLayout, 1)  # 1/5 of the space
        layout.addLayout(self.detailsLayout, 4)  # Remaining space

        # Set the main layout
        self.setLayout(layout)

    def addTask(self):
        # Placeholder function for adding a new task
        taskName = "New Task"  # Placeholder name
        self.taskList.addItem(taskName)

    def taskSelected(self, current, previous):
        # Placeholder function to handle task selection
        # Fill in the form with the selected task details
        if current:
            self.nameEdit.setText(current.text())
            self.descriptionEdit.setText("Task Description here...")  # Placeholder
            self.daysSpinBox.setValue(1)  # Default value
            self.workloadComboBox.setCurrentIndex(0)  # Default to 'Light'

    def saveTask(self):
        # Placeholder function to save task details
        pass