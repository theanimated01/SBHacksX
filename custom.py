import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QCheckBox
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap

# Global variables
quit_app = False
user_pref = {}

class CustomizationWindow(QWidget):
    topicEntered = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Purrformance')
        self.setGeometry(100, 100, 600, 400)  # Adjusted size of the window

        main_layout = QHBoxLayout()
    
        # Left side layout
        left_layout = QVBoxLayout()

        # Add stretch to push everything to center
        left_layout.addStretch(1)
        
        # Create a QLabel for the image
        image_label = QLabel(self)
        # Load the image
        pixmap = QPixmap(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'kitten_gif/idle.gif'))
        image_label.setPixmap(pixmap)
        # Optional: Resize the label to fit the image
        image_label.resize(pixmap.width(), pixmap.height())

        # Add the image label to the left layout
        left_layout.addWidget(image_label)

        left_layout.addStretch(1)

        # Save button
        quit_button = QPushButton('Quit Kitten', self)
        quit_button.clicked.connect(self.Quit)
        left_layout.addWidget(quit_button)

        # Add left layout to main layout
        main_layout.addLayout(left_layout)

        # Right side layout
        right_layout = QVBoxLayout()

        topic_label = QLabel('Topic That You Are Going To Be Working On:', self)
        right_layout.addWidget(topic_label)

        self.lineEdit = QLineEdit()
        right_layout.addWidget(self.lineEdit)

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
        QApplication.instance().quit()

    def saveSettings(self):
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

def get_user_pref():
    global user_pref
    return user_pref    

def get_quit_status():
    global quit_app
    return quit_app

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CustomizationWindow()
    sys.exit(app.exec_())