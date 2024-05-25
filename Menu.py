import sys
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QMenu, QStackedWidget, QWidget, QVBoxLayout, \
    QLabel, QPushButton, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from View import View
from ADM import ADM


class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.stackedWidget = QStackedWidget(self)
        self.setCentralWidget(self.stackedWidget)

        self.mainMenuWidget = QWidget()
        mainVLayout = QVBoxLayout(self.mainMenuWidget)

        titleLabel = QLabel("Auto Planner")
        titleLabel.setFont(QFont('Arial', 24, QFont.Bold))
        titleLabel.setAlignment(Qt.AlignCenter)

        viewButton = QPushButton("View")
        viewButton.setFixedSize(200, 50)
        viewButton.clicked.connect(self.showView)

        admButton = QPushButton("Add/Manage")
        admButton.setFixedSize(200, 50)
        admButton.clicked.connect(self.showADM)

        viewHLayout = QHBoxLayout()
        viewHLayout.addStretch(1)
        viewHLayout.addWidget(viewButton)
        viewHLayout.addStretch(1)

        admHLayout = QHBoxLayout()
        admHLayout.addStretch(1)
        admHLayout.addWidget(admButton)
        admHLayout.addStretch(1)

        mainVLayout.addStretch(1)
        mainVLayout.addWidget(titleLabel)
        mainVLayout.addSpacing(20)
        mainVLayout.addLayout(viewHLayout)
        mainVLayout.addSpacing(30)
        mainVLayout.addLayout(admHLayout)
        mainVLayout.addStretch(1)

        self.viewWidget = View(self.showMainMenu, self.showTaskInADM)
        self.admWidget = ADM(self.showMainMenu, self.updateView)  # Pass the updateView callback

        self.stackedWidget.addWidget(self.mainMenuWidget)
        self.stackedWidget.addWidget(self.viewWidget)
        self.stackedWidget.addWidget(self.admWidget)

        self.setGeometry(300, 300, 1920, 1080)
        self.setWindowTitle('Auto Planner')
        self.show()

    def showView(self):
        self.stackedWidget.setCurrentWidget(self.viewWidget)

    def showADM(self):
        self.stackedWidget.setCurrentWidget(self.admWidget)

    def showMainMenu(self):
        self.stackedWidget.setCurrentWidget(self.mainMenuWidget)

    def showTaskInADM(self, task):
        print(f"Navigating to ADM with task: {task['name']}")
        self.admWidget.loadTask(task)  # Implement loadTask method in ADM to display the task
        self.showADM()

    def updateView(self):
        self.viewWidget.refreshSchedule()  # Refresh the view widget schedule