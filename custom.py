# Updated PyQt code snippet with additional options and a dividing line.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QCheckBox, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QSpinBox

class CustomizationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Genie Customization')
        self.setGeometry(100, 100, 600, 200)  # Adjusted size of the window

        main_layout = QHBoxLayout()

        # Left side layout
        left_layout = QVBoxLayout()

        # Checkbox for "Attack Tab" option
        self.attack_tab_checkbox = QCheckBox('Allow Goose To Attack Tab', self)
        left_layout.addWidget(self.attack_tab_checkbox)

        # Frame rate option
        frame_rate_layout = QHBoxLayout()
        frame_rate_label = QLabel('Frame Rate:', self)
        frame_rate_layout.addWidget(frame_rate_label)

        self.frame_rate_spin_box = QSpinBox(self)
        self.frame_rate_spin_box.setRange(60, 90)  # Range for frame rate
        frame_rate_layout.addWidget(self.frame_rate_spin_box)

        # Add frame rate horizontal layout to left vertical layout
        left_layout.addLayout(frame_rate_layout)
        
        # Add left layout to main layout
        main_layout.addLayout(left_layout)

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

    def saveSettings(self):
        # Logic to process and save the settings
        attack_tab = self.attack_tab_checkbox.isChecked()
        frame_rate = self.frame_rate_spin_box.value()
        netflix = self.netflix_checkbox.isChecked()
        youtube = self.youtube_checkbox.isChecked()
        social_media = self.social_media_checkbox.isChecked()
        shopping = self.shopping_checkbox.isChecked()
        print(f'Attack Tab: {attack_tab}, Frame Rate: {frame_rate}, Netflix: {netflix}, YouTube: {youtube}, Social Media: {social_media}, Shopping: {shopping}')
        # Add your logic to save these settings or perform actions based on these settings
    
    def getPrefrance(self):
        attack_tab = self.attack_tab_checkbox.isChecked()
        frame_rate = self.frame_rate_spin_box.value()
        netflix = self.netflix_checkbox.isChecked()
        youtube = self.youtube_checkbox.isChecked()
        social_media = self.social_media_checkbox.isChecked()
        shopping = self.shopping_checkbox.isChecked()
        user_pref = {
            "Attack Tab": attack_tab, 
            "Frame Rate": frame_rate, 
            "Netflix": netflix, 
            "YouTube": youtube,
            "Social Media": social_media, 
            "Shopping": shopping
        }
        return user_pref

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CustomizationWindow()
    ex.show()
    sys.exit(app.exec_())
