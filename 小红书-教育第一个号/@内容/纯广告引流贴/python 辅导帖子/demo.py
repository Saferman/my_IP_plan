from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QFont
import sys

# 展示我们的服务质量
service_quality = "我的代码没有Bug"

# 代码展示
amazing_code = lambda x: "完美运行" if x else "从不出错"  # 展示代码质量
code_review = [bug for bug in ["bug1", "bug2", "bug3"] if bug in service_quality]  # 结果将是空列表,因为没有bug!
guarantee = "✓ " * 3 + service_quality + " ✓" * 3  # 用符号强调质量保证

# 输出日志
print("√质量保证；√绝对原创；√名师亲自辅导；")


def 展示经验(次数=5):
    if 次数 <= 0:
        return
    print("非中介!全网最靠谱，Python十二年开发经验")
    展示经验(次数 - 1)

# 调用函数展示我们的经验
展示经验()


app = QApplication(sys.argv)

msg_box = QMessageBox()
msg_box.setWindowTitle('提示')
msg_box.setText('留学生Python辅导/开发')

# 设置更大的字体
font = QFont()
font.setPointSize(20)
msg_box.setFont(font)

msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
msg_box.button(QMessageBox.Ok).setText('确实')
msg_box.button(QMessageBox.Cancel).setText('取消')

result = msg_box.exec_()
if result == QMessageBox.Ok:
    print('用户点击了确认')
else:
    print('用户点击了取消')
