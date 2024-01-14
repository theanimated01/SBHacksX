import sys
import random
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QDesktopWidget

# State constants
IDLE = 0
SLEEPING = 1
MOVING_POSITIVE = 2
MOVING_NEGATIVE = 3
IDLE_TO_SLEEP = 4
SLEEP_TO_IDLE = 5

class CatWindow(QLabel):
    def __init__(self):
        super().__init__()
        self.current_state = IDLE
        self.state_duration = 0
        self.initUI()
        self.center_on_screen()

        # Attributes for draggable window
        self.is_dragging = False
        self.drag_position = None

    def center_on_screen(self):
        screen_geometry = QDesktopWidget().screenGeometry()
        screen_width = screen_geometry.width()
        self.x = (screen_width - self.width()) // 2
    
    # Mouse press event handler
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    # Mouse move event handler
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.is_dragging:
            new_pos = event.globalPos() - self.drag_position
            self.move(new_pos)
            self.x = new_pos.x()  # Update the x-coordinate
            event.accept()

    # Mouse release event handler
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = False
            self.x = self.pos().x()  # Update the x-coordinate to the new position
            event.accept()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.update_animation()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)  # Timer tick every second

    def update_animation(self):
        gif_path = self.get_image_path(self.current_state)
        self.movie = QMovie(gif_path)
        self.setMovie(self.movie)
        self.movie.start()

    def get_image_path(self, state):
        base_path = '/Users/zeel/Desktop/SBHACKS/toon-cat-free/Gif Walking Cat/'  # Update with actual path
        if state == IDLE:
            return base_path + 'idle.gif'
        elif state == SLEEPING:
            return base_path + 'sleep.gif'
        elif state == MOVING_POSITIVE:
            return base_path + 'walking_positive.gif'
        elif state == MOVING_NEGATIVE:
            return base_path + 'walking_negative.gif'
        elif state == IDLE_TO_SLEEP:
            return base_path + 'idle_to_sleep.gif'
        elif state == SLEEP_TO_IDLE:
            return base_path + 'sleep_to_idle.gif'

    def update(self):
        self.state_duration += 1

        # Movement speed (pixels per update)
        movement_speed = 25

        if self.current_state == IDLE and self.state_duration > 3:  # 5 minutes
            # If the cat is at the right edge, only allow moving left
            if self.x + self.width() >= 1440:
                self.current_state = MOVING_POSITIVE
            # If the cat is at the left edge, only allow moving right
            elif self.x <= 0:
                self.current_state = MOVING_NEGATIVE
            else:
                self.current_state = random.choice([IDLE_TO_SLEEP, MOVING_POSITIVE, MOVING_NEGATIVE])
            self.state_duration = 0

        elif self.current_state == SLEEPING and self.state_duration > 2:  # 2 minutes
            self.current_state = SLEEP_TO_IDLE
            self.state_duration = 0

        elif self.current_state in [IDLE_TO_SLEEP, SLEEP_TO_IDLE]:
            self.current_state = SLEEPING if self.current_state == IDLE_TO_SLEEP else IDLE
            self.state_duration = 0

        elif self.current_state in [MOVING_POSITIVE, MOVING_NEGATIVE]:
            if self.state_duration > 4:  # Small walks for 4 seconds
                self.current_state = random.choice([IDLE, MOVING_POSITIVE, MOVING_NEGATIVE])
                self.state_duration = 0
            else:
                # Move the window
                if self.current_state == MOVING_POSITIVE:
                    self.x -= movement_speed
                elif self.current_state == MOVING_NEGATIVE:
                    self.x += movement_speed
                self.move_window()

        self.update_animation()

    def move_window(self):
        self.setGeometry(self.x, self.y(), self.width(), self.height())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CatWindow()
    window.show()
    sys.exit(app.exec_())
