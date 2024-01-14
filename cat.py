import sys
import os
import random
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtGui import QCursor

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
        self.enable_chase = False
        self.initUI()
        self.center_on_screen()
        self.y_pos = 100
        self.movement_speed = 10
        self.x, self.y = 1300, 720
        self.move(self.x, self.y)

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

    def chase_cursor(self):
        self.timer.start(80)
        cursor_pos = QCursor.pos()
        screen_geometry = QDesktopWidget().screenGeometry()

        # Calculate the direction to move (x and y)
        x_direction = 1 if cursor_pos.x() > self.x else -1
        y_direction = 1 if cursor_pos.y() > self.y_pos else -1

        # Update state based on x direction
        if cursor_pos.x() != self.x:
            self.current_state = MOVING_NEGATIVE if x_direction == 1 else MOVING_POSITIVE
            new_x = self.x + x_direction * self.movement_speed
            self.x = max(0, min(screen_geometry.width() - self.width(), new_x))

        # Update y position
        if cursor_pos.y() != self.y_pos:
            new_y_pos = self.y_pos + y_direction * self.movement_speed
            self.y_pos = max(0, min(screen_geometry.height() - self.height(), new_y_pos))

        # Move the window
        self.move(self.x, self.y_pos)

        # Check if the cat has reached the cursor
        if abs(cursor_pos.x() - self.x) <= self.movement_speed and abs(cursor_pos.y() - self.y_pos) <= self.movement_speed:
            self.current_state = IDLE  # Cat has reached the cursor
            self.enable_chase = False
            self.timer.start(800)

        self.update_animation()
    
    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.update_animation()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(800)  # Timer tick every second

    def update_animation(self):
        gif_path = self.get_image_path(self.current_state)
        self.movie = QMovie(gif_path)
        self.setMovie(self.movie)
        self.movie.start()

    def get_image_path(self, state):
        base_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'kitten_gif/')  # Update with actual path
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

        if self.enable_chase:
            self.chase_cursor()
        elif self.current_state == IDLE and self.state_duration > 300 and not self.enable_chase:  # 5 minutes
            if self.enable_chase:
                self.chase_cursor()
            # If the cat is at the right edge, only allow moving left
            if self.x + self.width() >= 1440:
                self.current_state = MOVING_POSITIVE
            # If the cat is at the left edge, only allow moving right
            elif self.x <= 0:
                self.current_state = MOVING_NEGATIVE
            else:
                self.current_state = random.choice([IDLE_TO_SLEEP, MOVING_POSITIVE, MOVING_NEGATIVE])
            self.state_duration = 0

        elif self.current_state == SLEEPING and self.state_duration > 120:  # 2 minutes
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

        if self.enable_chase:
            self.chase_cursor()
        self.update_animation()

    def move_window(self):
        self.setGeometry(self.x, self.y, self.width(), self.height())
