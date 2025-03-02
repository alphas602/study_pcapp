import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QComboBox
)
from PyQt5.QtCore import Qt
from datetime import datetime

class ExpenseTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("家計管理アプリ")
        self.setGeometry(100, 100, 600, 400)
        
        self.initUI()
        self.records = []

    def initUI(self):
        # メインレイアウト
        main_layout = QVBoxLayout()

        # 入力フォーム
        form_layout = QHBoxLayout()

        self.date_input = QLineEdit(datetime.now().strftime("%Y-%m-%d"))
        self.date_input.setPlaceholderText("日付 (YYYY-MM-DD)")

        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("カテゴリ (例: 食費, 交通費)")

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("金額")

        self.type_input = QComboBox()
        self.type_input.addItems(["支出", "収入"])

        form_layout.addWidget(self.date_input)
        form_layout.addWidget(self.category_input)
        form_layout.addWidget(self.amount_input)
        form_layout.addWidget(self.type_input)

        main_layout.addLayout(form_layout)

        # ボタン
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("追加")
        self.add_button.clicked.connect(self.add_record)

        self.delete_button = QPushButton("削除")
        self.delete_button.clicked.connect(self.delete_record)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)

        main_layout.addLayout(button_layout)

        # テーブル表示
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["日付", "カテゴリ", "金額", "タイプ"])
        main_layout.addWidget(self.table)

        # 合計表示
        self.total_label = QLabel("合計: 0 円")
        main_layout.addWidget(self.total_label)

        self.setLayout(main_layout)

    def add_record(self):
        date = self.date_input.text()
        category = self.category_input.text()
        amount = self.amount_input.text()
        record_type = self.type_input.currentText()

        if not date or not category or not amount:
            return

        try:
            amount = float(amount)
        except ValueError:
            return

        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        self.table.setItem(row_position, 0, QTableWidgetItem(date))
        self.table.setItem(row_position, 1, QTableWidgetItem(category))
        self.table.setItem(row_position, 2, QTableWidgetItem(str(amount)))
        self.table.setItem(row_position, 3, QTableWidgetItem(record_type))

        self.records.append((date, category, amount, record_type))
        self.update_total()

    def delete_record(self):
        selected_rows = self.table.selectionModel().selectedRows()
        for index in sorted(selected_rows, reverse=True):
            self.table.removeRow(index.row())
            del self.records[index.row()]

        self.update_total()

    def update_total(self):
        total = 0
        for record in self.records:
            amount = record[2]
            if record[3] == "支出":
                total -= amount
            else:
                total += amount

        self.total_label.setText(f"合計: {total:.2f} 円")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExpenseTracker()
    window.show()
    sys.exit(app.exec_())
