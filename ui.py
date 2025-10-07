import dearpygui.dearpygui as dpg
import re
from sympy import sympify, SympifyError
from main import chord_solver, tangent_solver, combined_selver

ALLOWED_PATTERN = re.compile(r"^[0-9x+\-*/^ ]*$")
methods = ("Chord", "Tangent", "Combined")

dpg.create_context()

def button_callback():
    combo_option = dpg.get_value("combo")
    print(combo_option)
    user_input = dpg.get_value("text")
    start_end = [dpg.get_value("start"), dpg.get_value("end")]
    accuracy = dpg.get_value("accuracy")
    try:
        sympify(user_input)
    except SympifyError:
        dpg.set_value("result", "Syntax Error")
        return
    if combo_option == methods[0]:
        chord_solver.give_info(user_input, start_end, accuracy)
        final_x, n_digits = chord_solver.compute()
    elif combo_option == methods[1]:
        tangent_solver.give_info(user_input, start_end, accuracy)
        final_x, n_digits =  tangent_solver.compute()
    else:
        combined_selver.give_info(user_input, start_end, accuracy)
        final_x, n_digits = combined_selver.compute()
    if final_x < 0:
        dpg.set_value("result", f"Negative, Can't solve")
    else:
        dpg.set_value("result", f"X = {final_x:.{n_digits}f}")
def validate_text_input(sender):
    text = dpg.get_value(sender)
    if not ALLOWED_PATTERN.match(text):
        filtered = "".join(ch for ch in text if ALLOWED_PATTERN.match(ch))
        dpg.set_value(sender, filtered)

with dpg.window(tag="Primary Window"):
    dpg.add_input_text(label="Equation", tag="text", default_value="x^4-2*x-4", callback=validate_text_input)
    dpg.add_combo(methods, default_value=methods[0], label="Method", tag="combo")
    dpg.add_input_float(label="Start (a)", tag="start", default_value=1)
    dpg.add_input_float(label="End (b)", tag="end", default_value=1.7)
    dpg.add_input_float(label="Accuracy", tag="accuracy", default_value=0.01, format="%.6f")

    dpg.add_text("X = None", tag='result')
    dpg.add_button(label="Calculate", callback=button_callback)

dpg.create_viewport(title='Calculium', width=600, height=200)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)

dpg.start_dearpygui()
dpg.destroy_context()