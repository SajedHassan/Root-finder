from sympy import *
import math
from numpy import arange


class BrigeVeta:

    num_of_iteration = 0

    # pass a function to me
    def __init__(self, function_formula, initial_x, ai, max_iterations, precision, x=Symbol('x')):
        self.function_formula = function_formula
        self.initial_x = initial_x
        self.ai = ai
        self.X = x
        self.max_iterations = max_iterations
        if max_iterations == 0:
            self.max_iterations = 50
        self.precision = precision
        if precision == 0:
            self.precision = 0.0001

    # def verify_there_is_a_root(self):
    #     function_value_at_upper_bound = self.function_formula.subs(self.X, self.upper_bound)
    #     function_value_at_lower_bound = self.function_formula.subs(self.X, self.lower_bound)
    #
    #     print(function_value_at_lower_bound)
    #     print(function_value_at_upper_bound)
    #
    #     if function_value_at_lower_bound * function_value_at_upper_bound < 0:
    #         return true

    def compute_root(self):

        table = [[[]]]
        fxi = float(self.function_formula.subs(self.X, self.initial_x))

        # create the table1
        table1 = [['i', 'Xi', 'F(Xi)', 'relative_error']]
        row = [0, self.initial_x, fxi, None]
        table1.append(row)
        max_pow = len(self.ai) - 1
        j = 0

        while True:

            i = max_pow
            j = j + 1

            # create table2
            table2 = [['i', 'ai', 'bi', 'ci']]
            row = [max_pow, self.ai[0], self.ai[0], self.ai[0]]
            table2.append(row)

            i = i - 1
            bi = ci = self.ai[0]
            k = 1
            while i >= 0:

                bi = bi * self.initial_x + self.ai[k]
                if i > 0:
                    ci = ci * self.initial_x + bi
                    temp = ci
                else:
                    temp = None

                # add Row2 to the table2
                row = [i, self.ai[k], bi, temp]
                table2.append(row)

                k = k + 1
                i = i - 1

            print(table2)
            table.append(table2)

            iterative_x = self.initial_x - (bi / ci)
            relative_error = (iterative_x - self.initial_x) / iterative_x

            fxi = float(self.function_formula.subs(self.X, iterative_x))

            # add Row1 to the table1
            row = [j, iterative_x, fxi, math.fabs(relative_error)]
            table1.append(row)

            # break when reach max iteration or precision
            if (math.fabs(relative_error) <= self.precision) | (i >= self.max_iterations):
                break

            self.initial_x = iterative_x

        print (table1)
        table.append(table1)
        return table, iterative_x

    def get_x_y(self):

        x = arange(-50.0, 50.0, 1.0)
        y = self.function_formula.evalf(subs={self.X: x})
        return x, y