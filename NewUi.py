from Main import chord_solver, tangent_solver, combined_solver
from PySide6.QtWidgets import QApplication , QMessageBox
from PySide6.QtCore import QFile 
from PySide6.QtUiTools import QUiLoader
from sympy import sympify, SympifyError

app = QApplication()
loader = QUiLoader()
file = QFile('Calculation.ui')
window = loader.load(file)
file.close()



methods = ("Хорд", "Касательных", "Комбинированный")


def solveButtonFunc(text, aStr , bStr , formul, acc): 
    accuracy = float(acc)
    a= float(aStr)
    b = float(bStr)
    around = [a,b]
    try:
        sympify(formul)
    except SyntaxError:
        window.SolveOutput.setMaxLength(35)
        window.SolveOutput.setText("Ошибка Формулы!")
        return
    except SympifyError:
        window.SolveOutput.setMaxLength(35)
        window.SolveOutput.setText("Ошибка Формулы!")
        return

    if text =="Хорд" :
        chord_solver.give_info(formul, around, accuracy)
        final_x, n_digits = chord_solver.compute()
        if final_x < 0 : 
            window.SolveOutput.setMaxLength(35)
            window.SolveOutput.setText("X Не найден! Корень меньше нуля")
        else : 
            n_digits = n_digits+5
            window.SolveOutput.setMaxLength(n_digits)
            window.SolveOutput.setText(f"X = {final_x}")
        
    elif text == "Касательных" : 
        tangent_solver.give_info(formul, around, accuracy)
        final_x, n_digits =  tangent_solver.compute()
        if final_x < 0 : 
            window.SolveOutput.setMaxLength(35)
            window.SolveOutput.setText("X Не найден! Корень меньше нуля")
        else : 
            n_digits = n_digits+5
            window.SolveOutput.setMaxLength(n_digits)
            window.SolveOutput.setText(f"X = {final_x}")

    else :
        combined_solver.give_info(formul, around, accuracy)
        final_x, n_digits =  combined_solver.compute()
        if final_x < 0 : 
            window.SolveOutput.setMaxLength(35)
            window.SolveOutput.setText("X Не найден! Корень меньше нуля")
        else : 
            n_digits = n_digits+5
            window.SolveOutput.setMaxLength(n_digits)
            window.SolveOutput.setText(f"X = {final_x}")
        
   
window.SolveButton.clicked.connect(
    lambda: solveButtonFunc(window.MethodComboBox.currentText(), window.StartDiapazoneField.text(), window.EndDiapazoneField.text() , window.FormulField.text(), window.AccTextField.text())
)

window.AccUpButton.clicked.connect(

lambda : window.AccTextField.setText(str((float(window.AccTextField.text())*0.1)))

)
window.AccDownButton.clicked.connect(
lambda : window.AccTextField.setText(str((float(window.AccTextField.text())*10)))
)

window.show()
app.exec_()