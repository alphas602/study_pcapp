import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QCalendarWidget, QListWidget, QPushButton, QVBoxLayout, QWidget, QInputDialog
from PyQt6.QtCore import QDate
import sqlite3

class CalendarApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("予定表アプリ")
        self.setGeometry(100, 100, 400, 400)
        
        self.initUI()
        self.initDB()
    
    def initUI(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.calendar = QCalendarWidget()
        self.calendar.selectionChanged.connect(self.load_events)
        layout.addWidget(self.calendar)
        
        self.event_list = QListWidget()
        layout.addWidget(self.event_list)
        
        self.add_event_button = QPushButton("予定を追加")
        self.add_event_button.clicked.connect(self.add_event)
        layout.addWidget(self.add_event_button)
        
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def initDB(self):
        self.conn = sqlite3.connect("schedule.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                event TEXT
            )
        """)
        self.conn.commit()
    
    def load_events(self):
        self.event_list.clear()
        selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        self.cursor.execute("SELECT event FROM events WHERE date = ?", (selected_date,))
        events = self.cursor.fetchall()
        for event in events:
            self.event_list.addItem(event[0])
    
    def add_event(self):
        selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        text, ok = QInputDialog.getText(self, "予定を追加", "予定を入力してください:")
        if ok and text:
            self.cursor.execute("INSERT INTO events (date, event) VALUES (?, ?)", (selected_date, text))
            self.conn.commit()
            self.load_events()
    
    def closeEvent(self, event):
        self.conn.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalendarApp()
    window.show()
    sys.exit(app.exec())