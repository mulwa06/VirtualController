from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor
import sys
import win32gui, win32con
import threading
from pynput import mouse
import time, keyboard

# Global variables
clicked = False
clicked_button = None
button_string = []

def check_clicked():
    """Thread function to check the clicked state."""
    global clicked, clicked_button
    while True:
        if clicked and clicked_button is not None:
            clicked_button.button_excecutable()  # Call the button's executable function
       
        time.sleep(0.1)  # Sleep to prevent high CPU usage

class action_button:
    def __init__(self, window, pos, label) -> None:
        self.x = pos[0]
        self.y = pos[1]
        self.label = label
        self.top = self.y
        self.bottom = self.y + window.action_button_height
        self.left = self.x
        self.right = self.x + window.action_button_width

    def clicked(self, click_pos):
        global clicked, clicked_button, button_string  # Use global variables
        if click_pos[1] >= self.top and click_pos[1] <= self.bottom:
            if click_pos[0] >= self.left and click_pos[0] <= self.right:
                clicked = True  # Set clicked to True
                clicked_button = self  # Set the clicked button
                button_string.append(self.label.lower())
                self.button_excecutable()

    def button_excecutable(self):
        print("Clicked ", self.label)
        keyboard.press(self.label.lower())

class TransparentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.x, self.y, self.width, self.height = 100, 100, 800, 600
        # Set up the window
        self.setWindowTitle("Emulator Test")
        self.setGeometry(self.x, self.y, self.width, self.height)  # x, y, width, height
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # Action buttons info
        self.action_buttons = dict()
        self.action_button_width = 50
        self.action_button_height = 50

        # Add buttons
        self.new_action_button((500, 500), "W")
        self.new_action_button((600, 500), "A")

    def new_action_button (self, pos, label):
        new_button = action_button(self, pos, label)
        self.button = QPushButton(label, self)  # Text on the button
        self.button.setGeometry(pos[0], pos[1], self.action_button_width, self.action_button_height)  # x, y, width, height
        self.button.setStyleSheet("background-color: white; color: black; font-size: 16px;")
        self.action_buttons[label] = new_button

    def action_buttons_locations(self):
        action_buttons_right = 0
        action_buttons_bottom = 0
        action_buttons_top = self.y + self.height
        action_buttons_left = self.x + self.width

        for button in self.action_buttons.values():
            # Update the topmost button
            if button.top < action_buttons_top:
                action_buttons_top = button.top
            
            # Update the leftmost button
            if button.left < action_buttons_left:
                action_buttons_left = button.left
            
            # Update the rightmost button
            if button.right > action_buttons_right:
                action_buttons_right = button.right
            
            # Update the bottommost button
            if button.bottom > action_buttons_bottom:
                action_buttons_bottom = button.bottom

        return {"top": action_buttons_top, "bottom": action_buttons_bottom, "left": action_buttons_left, "right": action_buttons_right}

    def paintEvent(self, event):
        # Draw a transparent background
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 100))  # Semi-transparent black

# finding click postion
def postitive_id(postion, window):
    location = window.action_buttons_locations()
    print(location)
    if postion[1] >= location["top"] and postion[1] <= location["bottom"]:
        if postion[0] >= location["left"] and postion[0] <= location["right"]:
            for button in window.action_buttons.values():
                button.clicked(postion)

# Mouse listener callback
def on_click(x, y, button, pressed):
    global clicked  # Use global variable
    if pressed:
        # print(f"Mouse down at ({x}, {y}) with {button}")
        postitive_id((x - 100, y - 100), window)  # Adjust for window position
    else:
        # print(f"Mouse up at ({x}, {y}) with {button}")

        global clicked ,clicked_button, button_string
        if len(button_string) >= 1:
            keyboard.release(button_string[-1])
        clicked = False  # Reset clicked to False on mouse up
        clicked_button = None  # Reset clicked_button

def start_mouse_listener():
    # Run the mouse listener in a separate thread
    with mouse.Listener(on_click=on_click) as listener:
        print("Mouse listener is running...")
        listener.join()

def make_window_click_through(window_title):
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd:
        exstyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, exstyle | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)
    else:
        print("Window not found!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TransparentWindow()
    window.show()

    # Start the mouse listener in a separate thread
    listener_thread = threading.Thread(target=start_mouse_listener, daemon=True)
    listener_thread.start()

    # Start the thread to check the clicked state
    check_thread = threading.Thread(target=check_clicked, daemon=True)
    check_thread.start()

    make_window_click_through("Emulator Test")
    sys.exit(app.exec_())
