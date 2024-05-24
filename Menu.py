from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QStackedWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from View import View
from ADM import ADM

class Menu(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create a central widget and a stacked widget
        self.stackedWidget = QStackedWidget(self)
        self.setCentralWidget(self.stackedWidget)

        # Define mainMenuWidget as an instance attribute
        self.mainMenuWidget = QWidget()
        mainVLayout = QVBoxLayout(self.mainMenuWidget)

        # Title Label
        titleLabel = QLabel("Auto Planner")
        titleLabel.setFont(QFont('Arial', 24, QFont.Bold))  # Set font type, size, and weight
        titleLabel.setAlignment(Qt.AlignCenter)  # Center the text

        # View Button
        viewButton = QPushButton("View")
        viewButton.setFixedSize(200, 50)
        viewButton.clicked.connect(self.showView)
        viewHLayout = QHBoxLayout()
        viewHLayout.addStretch(1)
        viewHLayout.addWidget(viewButton)
        viewHLayout.addStretch(1)

        # Add/Manage Button
        admButton = QPushButton("Add/Manage")
        admButton.setFixedSize(200, 50)
        admButton.clicked.connect(self.showADM)
        admHLayout = QHBoxLayout()
        admHLayout.addStretch(1)
        admHLayout.addWidget(admButton)
        admHLayout.addStretch(1)

        # Layout organization
        mainVLayout.addStretch(1)
        mainVLayout.addWidget(titleLabel)
        mainVLayout.addSpacing(20)
        mainVLayout.addLayout(viewHLayout)
        mainVLayout.addSpacing(30)
        mainVLayout.addLayout(admHLayout)
        mainVLayout.addStretch(1)

        # View and ADM Widgets
        self.viewWidget = View(self.showMainMenu)
        self.admWidget = ADM(self.showMainMenu)

        # Add widgets to stacked widget
        self.stackedWidget.addWidget(self.mainMenuWidget)
        self.stackedWidget.addWidget(self.viewWidget)
        self.stackedWidget.addWidget(self.admWidget)

        # Set window parameters
        self.setGeometry(300, 300, 1920, 1080)
        self.setWindowTitle('CarsoPlanner')
        self.show()

    def showView(self):
        self.stackedWidget.setCurrentWidget(self.viewWidget)

    def showADM(self):
        self.stackedWidget.setCurrentWidget(self.admWidget)

    def showMainMenu(self):
        self.stackedWidget.setCurrentWidget(self.mainMenuWidget)
