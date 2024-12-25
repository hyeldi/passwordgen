import sys
import os
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRectF, QPointF
from PyQt5.QtGui import QMovie, QPixmap, QColor
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QVBoxLayout, QPushButton, QFrame, QLabel, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, 
    QWidget, QLineEdit, QMessageBox, QHBoxLayout, QGraphicsOpacityEffect, QApplication, QDesktopWidget
)
import sqlite3
import random
import string
class PasswordManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: white;")
        self.setWindowTitle("Password Manager")
        self.setGeometry(100, 100, 560, 540)  
        

        self.db_connection = sqlite3.connect("passwords.db")
        self.create_table()

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.move_to_tv()

        self.init_ui()

    def start_celebration_effect(self):
        for _ in range(30): 
            x = random.randint(0, 400)
            y = random.randint(-100, 0)
            self.create_confetti(x, y)

    def create_confetti(self, x, y):
       
        color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        confetti = QGraphicsEllipseItem(0, 0, 10, 10)
        confetti.setBrush(color)
        confetti.setPen(Qt.NoPen)
        confetti.setPos(x, y)

        self.scene.addItem(confetti)

        
        animation = QPropertyAnimation(confetti, b'pos')
        animation.setDuration(3000)
        animation.setStartValue(QPointF(x, y))
        animation.setEndValue(QPointF(x, 400 + random.randint(0, 50)))
        animation.finished.connect(lambda: self.scene.removeItem(confetti)) 
        animation.start()

    def create_table(self):
        cursor = self.db_connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                app_name TEXT NOT NULL,
                password TEXT NOT NULL
    
                
            )
        """)
        self.db_connection.commit()

    def init_ui(self):
        self.welcome_screen = self.create_welcome_screen()
        self.generate_password_screen = self.create_generate_password_screen()
        self.generate_email_screen = self.create_generate_email_screen()
        self.generated_password_screen = self.create_generated_password_screen()

        self.central_widget.addWidget(self.welcome_screen)
        self.central_widget.addWidget(self.generate_password_screen)
        self.central_widget.addWidget(self.generate_email_screen)
        self.central_widget.addWidget(self.generated_password_screen)

        self.central_widget.setCurrentWidget(self.welcome_screen)

    def create_welcome_screen(self):
        screen = QWidget()
        layout = QVBoxLayout()

        welcome_label = QLabel("Welcome to Password/Email Offline Generator", alignment=Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(welcome_label)

        generate_btn = QPushButton("Generate Password")
        generate_btn.setStyleSheet(self.stylize_button("black"))
        generate_btn.clicked.connect(lambda: self.show_loader(self.generate_password_screen))
        layout.addWidget(generate_btn)

        generatee_btn = QPushButton("Generate Email")
        generatee_btn.setStyleSheet(self.stylize_button("black"))
        generatee_btn.clicked.connect(lambda: self.show_loader(self.generate_email_screen))
        layout.addWidget(generatee_btn)

        view_passwords_btn = QPushButton("View Generated Emails/Passwords")
        view_passwords_btn.setStyleSheet(self.stylize_button("blue"))
        view_passwords_btn.clicked.connect(lambda: self.show_loader(self.generated_password_screen, refresh=True))
        layout.addWidget(view_passwords_btn)

        

       
        image_label = QLabel()
        pixmap = QPixmap("welcome_image.jpg").scaled(600, 400, Qt.KeepAspectRatio)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)

        image_label = QLabel()
        pixmap = QPixmap("").scaled(400, 300, Qt.KeepAspectRatio)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)

        screen.setLayout(layout)
        return screen

    def create_generate_password_screen(self):
        screen = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Select an App to Generate Password For:", alignment=Qt.AlignCenter)
        label.setStyleSheet("font-size: 16px; margin-bottom: 10px;")
        layout.addWidget(label)

       
        divider1 = QFrame()
        divider1.setFrameShape(QFrame.HLine)
        divider1.setFrameShadow(QFrame.Sunken)
        divider1.setStyleSheet("color: gray; margin-bottom: 20px;")
        layout.addWidget(divider1)

        apps = {
            "Google": "blue",
            "Facebook": "blue",
            "Instagram": "blue",
            "Twitter": "blue",
            "LinkedIn": "blue",
            "WhatsApp": "blue",
            "Spotify": "blue",
            "Amazon": "blue",
        }

        for app, color in apps.items():
            btn = QPushButton(app)
            btn.setStyleSheet(self.stylize_button(color))
            btn.clicked.connect(lambda checked, app=app: self.generate_password(app))
            layout.addWidget(btn)

        
        divider2 = QFrame()
        divider2.setFrameShape(QFrame.HLine)
        divider2.setFrameShadow(QFrame.Sunken)
        divider2.setStyleSheet("color: gray; margin-top: 20px;")
        layout.addWidget(divider2)

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(self.stylize_button("black"))
        back_btn.clicked.connect(lambda: self.show_loader(self.welcome_screen))
        layout.addWidget(back_btn)
        image_label = QLabel()

    

        pixmap = QPixmap("").scaled(600, 400, Qt.KeepAspectRatio)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)


        screen.setLayout(layout)
        return screen

    def create_generate_email_screen(self):
        screen = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Click on Generate Email to proceed", alignment=Qt.AlignCenter)
        label.setStyleSheet("font-size: 16px; margin-bottom: 10px;")
        layout.addWidget(label)

       
        divider1 = QFrame()
        divider1.setFrameShape(QFrame.HLine)
        divider1.setFrameShadow(QFrame.Sunken)
        divider1.setStyleSheet("color: gray; margin-bottom: 20px;")
        layout.addWidget(divider1)

        apps = {
            "Generate Email": "blue",
        }

        for app, color in apps.items():
            btn = QPushButton(app)
            btn.setStyleSheet(self.stylize_button(color))
            btn.clicked.connect(lambda checked, app=app: self.generate_email(app))
            layout.addWidget(btn)

       
        divider2 = QFrame()
        divider2.setFrameShape(QFrame.HLine)
        divider2.setFrameShadow(QFrame.Sunken)
        divider2.setStyleSheet("color: gray; margin-top: 20px;")
        layout.addWidget(divider2)

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(self.stylize_button("black"))
        back_btn.clicked.connect(lambda: self.show_loader(self.welcome_screen))
        layout.addWidget(back_btn)

        image_label = QLabel()
        pixmap = QPixmap("").scaled(600, 400, Qt.KeepAspectRatio)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)

        screen.setLayout(layout)
        return screen

    


    def generate_password(self, app_name):
        password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=12))
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO passwords (app_name, password) VALUES (?, ?)", (app_name, password))
        self.db_connection.commit()

        self.show_generated_password_screen(app_name, password)

    def generate_email(self, app_name):

        username = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        domain = 'email'
        email = f'{username}@{domain}.com'
        
        

        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO passwords (app_name, password) VALUES (?, ?)", (email, email)) 
        self.db_connection.commit()
       
        self.show_generated_email_screen(app_name, email)

    def show_generated_password_screen(self, app_name, password):
        screen = QWidget()
        layout = QVBoxLayout()

        label = QLabel(f"Password for {app_name}:", alignment=Qt.AlignCenter)
        label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(label)

        

        password_field = QLineEdit(password)
        password_field.setReadOnly(True)
        password_field.setStyleSheet("font-size: 14px;")
        layout.addWidget(password_field)

        copy_btn = QPushButton("Copy Password 📋")
        copy_btn.setStyleSheet(self.stylize_button("green"))
        copy_btn.clicked.connect(lambda: (self.copy_to_clipboard(password)))
        layout.addWidget(copy_btn)

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(self.stylize_button("black"))
        back_btn.clicked.connect(lambda: self.show_loader(self.generate_password_screen))
        layout.addWidget(back_btn)

        image_label = QLabel()
        pixmap = QPixmap("").scaled(400, 300, Qt.KeepAspectRatio)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)

        screen.setLayout(layout)
        self.central_widget.addWidget(screen)
        self.show_loader(screen)

    def show_generated_email_screen(self, app_name, email):
        screen = QWidget()
        layout = QVBoxLayout()

        label = QLabel(f"Email address:", alignment=Qt.AlignCenter)
        label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(label)

        

        email_field = QLineEdit(email)
        email_field.setReadOnly(True)
        email_field.setStyleSheet("font-size: 14px;")
        layout.addWidget(email_field)

       
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: black;")
        layout.addWidget(line)

        copy_btn = QPushButton("Copy email 📋")
        copy_btn.setStyleSheet(self.stylize_button("green"))
        copy_btn.clicked.connect(lambda: self.copy_to_clipboard(email))
        layout.addWidget(copy_btn)

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(self.stylize_button("black"))
        back_btn.clicked.connect(lambda: self.show_loader(self.generate_email_screen))
        layout.addWidget(back_btn)

        image_label = QLabel()
        pixmap = QPixmap("").scaled(400, 300, Qt.KeepAspectRatio)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)

        screen.setLayout(layout)
        self.central_widget.addWidget(screen)
        self.show_loader(screen)


    def stylize_button(self, color):
        return f"""
            QPushButton {{
                font-size: 16px;
                font-weight: bold;
                padding: 12px 20px;
                border-radius: 10px;
                background-color: {color};
                color: white;
            }}
            QPushButton:hover {{
                background-color: light{color};
            }}
        """

    def copy_to_clipboard(self, text):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        QMessageBox.information(self, "Copied", "Password copied to clipboard!")

    def create_generated_password_screen(self):
        self.generated_password_screen = QWidget()
        self.generated_password_layout = QVBoxLayout()

        label = QLabel("Generated Passwords:", alignment=Qt.AlignCenter)
        label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.generated_password_layout.addWidget(label)

        self.refresh_password_list()

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(self.stylize_button("black"))
        back_btn.clicked.connect(lambda: self.show_loader(self.welcome_screen))
        self.generated_password_layout.addWidget(back_btn)

        self.generated_password_screen.setLayout(self.generated_password_layout)
        return self.generated_password_screen

    def refresh_password_list(self):
        for i in reversed(range(self.generated_password_layout.count() - 1)):
            widget = self.generated_password_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        cursor = self.db_connection.cursor()
        cursor.execute("SELECT app_name, password FROM passwords")
        rows = cursor.fetchall()

        for app_name, password in rows:
            row_widget = QWidget()
            row_layout = QHBoxLayout()

            app_label = QLabel(app_name)
            app_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 2px 10px;")
           
            row_layout.addWidget(app_label)

            password_field = QLineEdit("*" * len(password))
            password_field.setReadOnly(True)
            password_field.setFixedWidth(150)
            row_layout.addWidget(password_field)

            toggle_btn = QPushButton("👁")
            toggle_btn.setCheckable(True)
            toggle_btn.setFixedSize(30, 30)
            toggle_btn.toggled.connect(lambda checked, field=password_field, pwd=password: field.setText(pwd if checked else "*" * len(pwd)))
            row_layout.addWidget(toggle_btn)

            row_widget.setLayout(row_layout)
            self.generated_password_layout.insertWidget(self.generated_password_layout.count() - 1, row_widget)


    def show_loader(self, target_widget, refresh=False):
        loader_screen = QWidget()
        loader_layout = QVBoxLayout()
        loader_label = QLabel("↻ 𝙇𝙤𝙖𝙙𝙞𝙣𝙜... ↻", alignment=Qt.AlignCenter)
        loader_label.setStyleSheet("font-size: 16px; font-weight: bold; ")
        loader_layout.addWidget(loader_label)
        loader_screen.setLayout(loader_layout)
        self.central_widget.addWidget(loader_screen)
        self.central_widget.setCurrentWidget(loader_screen)

        QTimer.singleShot(1000, lambda: self.switch_to_widget(target_widget, refresh))

    def switch_to_widget(self, target_widget, refresh):
        if refresh:
            self.refresh_password_list()
        self.central_widget.setCurrentWidget(target_widget)

    def closeEvent(self, event):
        self.db_connection.close()
        super().closeEvent(event)

    def move_to_tv(self):
       
        desktop = QDesktopWidget()
        screen_count = desktop.screenCount()

        if screen_count > 1:
           
            screen_geometry = desktop.screenGeometry(1)
            
            
            screen_center_x = screen_geometry.left() + (screen_geometry.width() // 2)
            screen_center_y = screen_geometry.top() + (screen_geometry.height() // 2)
            
            
            window_width = self.width()
            window_height = self.height()

           
            window_x = screen_center_x - (window_width // 2)
            window_y = screen_center_y - (window_height // 2)
            
          
            self.move(window_x, window_y)
        else:
            print("TV screen not detected. Defaulting to the primary screen.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordManagerApp()
    window.show()
    sys.exit(app.exec_())

