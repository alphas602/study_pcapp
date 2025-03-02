import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QCalendarWidget, QListWidget, QPushButton, QVBoxLayout, QWidget, QInputDialog
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QTextCharFormat, QColor, QPainter, QFont
import sqlite3

class CustomCalendarWidget(QCalendarWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.events = {}
    
    def set_events(self, events):
        self.events = events
        self.update()
    
    def paintCell(self, painter, rect, date):
        date_str = date.toString("yyyy-MM-dd")
        
        # 背景の塗りつぶし（選択時）
        if self.selectedDate() == date:
            painter.fillRect(rect, QColor("#ADD8E6"))  # 選択時に薄い青色
        
        # 曜日ごとの日付の色を設定
        if date.dayOfWeek() == 6:  # 土曜日は青
            date_color = QColor("blue")
        elif date.dayOfWeek() == 7:  # 日曜日は赤
            date_color = QColor("red")
        else:
            date_color = QColor("black")
        
        # 日付を左上に描画
        painter.setPen(date_color)
        painter.setFont(QFont("Arial", 10))
        painter.drawText(rect.x() + 2, rect.y() + 12, date.toString("d"))
        
        # 予定の描画（ハイライト付き）
        if date_str in self.events:
            painter.fillRect(rect.x() + 2, rect.y() + 18, rect.width() - 4, 14, QColor("#FFFF99"))  # 予定の背景を黄色でハイライト
            painter.setPen(QColor("blue"))
            painter.setFont(QFont("Arial", 8))
            text = self.events[date_str][:10] + ("..." if len(self.events[date_str]) > 10 else "")
            painter.drawText(rect.x() + 4, rect.y() + 28, text)

class CalendarApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("予定表アプリ")
        self.setGeometry(100, 100, 400, 400)
        
        self.initUI()
        self.initDB()
        self.load_events()
    
    def initUI(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.calendar = CustomCalendarWidget()
        self.calendar.selectionChanged.connect(self.load_selected_events)
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
        self.cursor.execute("SELECT date, event FROM events")
        events = self.cursor.fetchall()
        
        event_dict = {}
        for date, event in events:
            event_dict[date] = event_dict.get(date, "") + event + "\n"
        
        self.calendar.set_events(event_dict)
        self.load_selected_events()
    
    def load_selected_events(self):
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
