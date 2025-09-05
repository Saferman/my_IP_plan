import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtCore import QSize




class GridWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('8x8 Grid with PyQt5')
        self.setGeometry(100, 100, 400, 400)  # 设置窗口大小

        self.grid = [[0 for _ in range(8)] for _ in range(8)]  # 初始化二维列表
        self.grid_layout = QVBoxLayout()

        for row in range(8):
            row_layout = QHBoxLayout()
            for col in range(8):
                button = QPushButton()
                button.setFixedSize(QSize(50, 50))  # 设置按钮大小
                if A[row][col] == 0:
                    button.setStyleSheet("background-color: white; border: 1px solid black;")
                else:
                    button.setStyleSheet("background-color: black; border: 1px solid black;")
                button.clicked.connect(lambda _, r=row, c=col: self.on_click(r, c))
                row_layout.addWidget(button)
            self.grid_layout.addLayout(row_layout)

        self.setLayout(self.grid_layout)

    def on_click(self, row, col):
        self.grid[row][col] = 1 if self.grid[row][col] == 0 else 0  # 切换0和1
        color = "black" if self.grid[row][col] == 1 else "white"
        self.findChild(QPushButton, f"button_{row}_{col}").setStyleSheet(f"background-color: {color}; border: 1px solid black;")



def main():
    app = QApplication(sys.argv)
    ex = GridWidget()
    ex.show()
    sys.exit(app.exec_())

# 实现一个数组里面有八个列表，每个列表有八个0
A = []



if __name__ == '__main__':
    main()