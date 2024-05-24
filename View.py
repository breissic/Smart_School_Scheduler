from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QFrame, QGridLayout
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize, QDate


class View(QWidget):
    def __init__(self, home_callback):
        super().__init__()
        self.home_callback = home_callback
        self.currentDate = QDate.currentDate()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Top bar layout for navigation and home button
        topBarLayout = QHBoxLayout()

        # Back week navigation button
        backWeekButton = QPushButton()
        backWeekButton.setIcon(QIcon('backarrow.png'))
        backWeekButton.setIconSize(QSize(30, 30))
        backWeekButton.clicked.connect(self.showPreviousWeek)
        topBarLayout.addWidget(backWeekButton)

        # Next week navigation button
        nextWeekButton = QPushButton()
        nextWeekButton.setIcon(QIcon('arrow.png'))
        nextWeekButton.setIconSize(QSize(30, 30))
        nextWeekButton.clicked.connect(self.showNextWeek)
        topBarLayout.addWidget(nextWeekButton)

        # Spacer to push home button to the right
        topBarLayout.addStretch(1)

        # Home button
        homeButton = QPushButton()
        homeButton.setIcon(QIcon('home.png'))
        homeButton.setIconSize(QSize(40, 40))
        homeButton.clicked.connect(self.home_callback)
        topBarLayout.addWidget(homeButton, alignment=Qt.AlignRight)

        layout.addLayout(topBarLayout)

        # Calendar grid for weekly view
        self.calendarGrid = QGridLayout()
        self.calendarGrid.setSpacing(0)
        daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for i, day in enumerate(daysOfWeek):
            # Day headers
            dayLabel = QLabel(day)
            dayLabel.setFont(QFont('Arial', 12, QFont.Bold))
            dayLabel.setAlignment(Qt.AlignCenter)
            self.calendarGrid.addWidget(dayLabel, 0, i)

        self.updateWeekView()
        layout.addLayout(self.calendarGrid)

        # Set the main layout for the widget
        self.setLayout(layout)

    def updateWeekView(self):
        # Clear previous day widgets
        for i in range(7):  # Ensure to start clearing from the second row
            widget = self.calendarGrid.itemAtPosition(1, i)
            if widget:
                widget.widget().deleteLater()

        # Find Monday of the current week
        monday = self.currentDate.addDays(-self.currentDate.dayOfWeek() + 1)
        for i in range(7):  # Display the week starting from Monday
            day = monday.addDays(i)
            # Create a frame for each day to hold more information later
            dayFrame = QFrame()
            dayFrame.setFrameShape(QFrame.Box)
            dayFrame.setLineWidth(1)
            dayLayout = QVBoxLayout(dayFrame)
            dayLabel = QLabel(day.toString('dd MMM'))
            dayLabel.setAlignment(Qt.AlignTop | Qt.AlignCenter)
            dayLayout.addWidget(dayLabel)
            dayLayout.addStretch(1)  # Push the label to the top
            self.calendarGrid.addWidget(dayFrame, 1, i)

    def showPreviousWeek(self):
        self.currentDate = self.currentDate.addDays(-7)
        self.updateWeekView()

    def showNextWeek(self):
        self.currentDate = self.currentDate.addDays(7)
        self.updateWeekView()

