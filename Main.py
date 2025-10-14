from sympy import diff, lambdify
from decimal import Decimal

def count_decimals_from_float(x: float) -> int:
    d = Decimal(str(x))
    if d == 0:
        return 0
    return max(0, -d.as_tuple().exponent)

class Solver:
    def __init__(self):
        self.method = None
        self.n_digits = None
        self.user_input = None
        self.min_max_values = None # [a, b]
        self.accuracy = None

    def give_info(self, inp, start_end, accuracy):
        self.user_input = inp.replace("^", "**")
        self.min_max_values = start_end
        self.accuracy = round(accuracy, 6)
        self.n_digits = count_decimals_from_float(self.accuracy)

class ChordSolver(Solver):
    def __init__(self):
        super().__init__()
        self.previous_value = None
        self.func = None
        self.f_a = None
        self.f_b = None

    def give_info(self, inp, start_end, accuracy):
        super().give_info(inp, start_end, accuracy)
        self.func = lambdify("x", self.user_input)
        self.f_a = self.func(self.min_max_values[0])
        self.f_b = self.func(self.min_max_values[1])

    def get_x(self):
        a = self.min_max_values[0]
        b = self.min_max_values[1]
        x = a - (((b - a) * self.f_a)/(self.f_b - self.f_a))
        f_x = self.func(x)
        if f_x < 0:
            self.previous_value = a
            self.min_max_values[0] = x
            self.f_a = f_x
        else:
            self.previous_value = b
            self.min_max_values[1] = x
            self.f_b = f_x
        return x

    def compare_by_round(self) -> bool:
        for value in self.min_max_values:
            return round(value, self.n_digits) == round(self.previous_value, self.n_digits)
        return False

    def compute(self):
        x = self.get_x()
        while not self.compare_by_round():
            x = self.get_x()
            print(f"preX={x} {self.min_max_values[0]}, {self.min_max_values[1]}, {self.accuracy}")
        else:
            print(f"X={x}")
        print(self.n_digits)
        return x, self.n_digits

class TangentSolver(Solver):
    def __init__(self):
        super().__init__()
        self.func_xxx = None
        self.func_xx = None
        self.func_x = None
        self.previous_x = None
        self.current_x = None
        self.f_x = None # f(x)
        self.f_xx = None # f'(x)

    def give_info(self, inp, start_end, accuracy):
        self.user_input = inp.replace("^", "**")
        self.min_max_values = start_end
        self.accuracy = round(accuracy, 6)
        self.n_digits = count_decimals_from_float(self.accuracy)
        self.current_x = self.min_max_values[0]
        self.func_x = lambdify("x", self.user_input)
        self.func_xx = lambdify("x", diff(self.user_input, 'x'))
        self.func_xxx = lambdify("x", diff(self.user_input, 'x', 2))

    def compare_by_round(self) -> bool:
        return round(self.current_x, self.n_digits) == round(self.previous_x, self.n_digits)

    def func_x(self):
        while not self.compare_by_round():
            self.previous_x = self.current_x
            self.current_x = self.current_x - (self.f_x / self.f_xx)

    def check_func(self) -> bool:
        found = False
        bl = self.func_x(self.current_x) < 0 and self.func_xxx(self.current_x) < 0
        bl2 = self.func_x(self.current_x) > 0 and self.func_xxx(self.current_x) > 0
        self.func_xx(self.current_x)
        if bl or bl2:
            found = True
        elif self.current_x > self.min_max_values[1]*2:
            print("Too many iterations")
            raise StopIteration
        else:
            self.current_x += self.accuracy
        return found

    def compute(self):
        found = False
        while not found:
            found = self.check_func()
        return self.current_x, self.n_digits

class CombinedSolver(ChordSolver, TangentSolver):
    def __init__(self):
        super().__init__()

    def give_info(self, inp, start_end, accuracy):
        super().give_info(inp, start_end, accuracy)

    def compute(self):
        self.check_func()
        x1 = self.get_x()
        while not super().compare_by_round():
            x1 = self.get_x()
            x2 = self.func_x(self.current_x)
            print(x1, x2)
        return x1, self.n_digits

chord_solver = ChordSolver()
tangent_solver = TangentSolver()
combined_selver = CombinedSolver()
