# Updated PyQt code snippet with additional options and a dividing line.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QCheckBox, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QSpinBox
from PyQt5.QtCore import pyqtSignal

#Global variables
quit_app = False
user_pref = {}

class CustomizationWindow(QWidget):
    topicEntered = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Kitten Customization')
        self.setGeometry(100, 100, 600, 200)  # Adjusted size of the window

        main_layout = QHBoxLayout()

        # Left side layout
        left_layout = QVBoxLayout()

        # Checkbox for "Attack Tab" option
        # self.attack_tab_checkbox = QCheckBox('Allow Goose To Attack Tab', self)
        # left_layout.addWidget(self.attack_tab_checkbox)

        # Frame rate option
        topic_label = QLabel('Topic That You Are Going To Be Working On:', self)
        left_layout.addWidget(topic_label)

        self.lineEdit = QLineEdit()
        topic_box_layout = QVBoxLayout()
        topic_box_layout.addWidget(self.lineEdit)
        # self.frame_rate_spin_box.setRange(60, 90)  # Range for frame rate
        left_layout.addLayout(topic_box_layout)
        
        # Add left layout to main layout
        main_layout.addLayout(left_layout)

        left_layout.addStretch(1)

        # Save button
        quit_button = QPushButton('Quit Kitten', self)
        quit_button.clicked.connect(self.Quit)
        left_layout.addWidget(quit_button)

        # Vertical line as a divider
        divider = QFrame()
        divider.setFrameShape(QFrame.VLine)
        divider.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(divider)

        # Right side layout (existing content)
        right_layout = QVBoxLayout()

        # Header label
        header_label = QLabel('Choose Websites For Studying', self)
        right_layout.addWidget(header_label)

        # Checkboxes for common unproductive websites
        self.netflix_checkbox = QCheckBox('Netflix', self)
        right_layout.addWidget(self.netflix_checkbox)

        self.youtube_checkbox = QCheckBox('YouTube', self)
        right_layout.addWidget(self.youtube_checkbox)

        self.social_media_checkbox = QCheckBox('Social Media', self)
        right_layout.addWidget(self.social_media_checkbox)

        self.shopping_checkbox = QCheckBox('Shopping', self)
        right_layout.addWidget(self.shopping_checkbox)

        # Save button
        save_button = QPushButton('Save Settings', self)
        save_button.clicked.connect(self.saveSettings)
        right_layout.addWidget(save_button)

        # Add right layout to main layout
        main_layout.addLayout(right_layout)

        # Set the main layout on the window
        self.setLayout(main_layout)

    def Quit(self):
        global quit_app
        quit_app = True
        QApplication.instance().quit()  # Quit the application

    def saveSettings(self):
        # Logic to process and save the settings
        global user_pref
        topic = self.lineEdit.text()
        netflix = self.netflix_checkbox.isChecked()
        youtube = self.youtube_checkbox.isChecked()
        social_media = self.social_media_checkbox.isChecked()
        shopping = self.shopping_checkbox.isChecked()
        user_pref = { 
            "Topic": topic, 
            "Netflix": netflix, 
            "YouTube": youtube,
            "Social Media": social_media, 
            "Shopping": shopping
        }
        if topic:
            self.topicEntered.emit()
        print(f'Topic: {topic}, Netflix: {netflix}, YouTube: {youtube}, Social Media: {social_media}, Shopping: {shopping}')
        # Add your logic to save these settings or perform actions based on these settings

def get_user_pref():
    global user_pref
    return user_pref    

def get_quit_status():
    global quit_app
    return quit_app
