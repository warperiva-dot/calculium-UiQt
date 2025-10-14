import Main 
from PySide6.QtWidgets import QApplication , QPushButton , QLabel 
from PySide6.QtCore import QFile 
from PySide6.QtUiTools import QUiLoader

app = QApplication()

loader = QUiLoader()

file = QFile('Calculation.ui')

window = loader.load(file)
file.close()




window.show()
app.exec_()