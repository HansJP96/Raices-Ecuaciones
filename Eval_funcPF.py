# Function evaluation for Fixed Point Method (only)
from sympy import LambertW, I
import sympy
from numpy import absolute

global expressions

def function_FxP(eq, diff=False, increaser=-1, result_incre=0):
    y = sympy.Symbol("y")
    diff_function = ""

    equat = "f(x)=" + eq
    variables, eq_object = equat.split("=", 1)
    # eq_object = eq_object.rstrip('; ')
    args = sympy.sympify(variables).args  # args[0] refers to symbol x
    base_function = sympy.sympify(eq_object).simplify().expand()

    add_function = sympy.Add(base_function, args[0])
    sep_functions = base_function.args
    # len_clFuncions = len(sep_functions)
    print(sep_functions)

    function_target = ""
    monomial_shifter = ""
    result_number = True

    if increaser == -1:
        function_target = add_function
    else:
        if sep_functions[increaser].is_real:
            # function_target = add_function # This because empty return throw an execution error
            return
        else:
            monomial = sep_functions[increaser]
            if monomial == args[0]:
                function_shifter = sympy.Add(base_function, -args[0])
                function_shifter = sympy.Add(function_shifter, y)
            elif monomial == -args[0]:
                function_shifter = sympy.Add(base_function, args[0])
                function_shifter = sympy.Add(function_shifter, -y)
            else:
                monomial_shifter = monomial.subs(args[0], y)
                # function_shifter = base_function.subs(monomial, monomial_shifter) was used now no
                function_shifter = base_function.xreplace({monomial: monomial_shifter})

            print(monomial)
            print(monomial_shifter)
            print(function_shifter)
            function_target = sympy.solve(function_shifter, y)
            # print(function_target)
            count_function = len(function_target)
            # print(count_function)
            if count_function > 1:
                function_target = function_target[result_incre].simplify()
                result_number = False
                if result_incre + 1 == count_function:
                    result_number = True
            else:
                function_target = function_target[-1].simplify()

    print(function_target)

    if invalid_data(function_target) is True:
        function_target = add_function
        return False, result_number

    if diff:
        diff_function = function_target.diff(args[0])
        # print(diff_function)

    # print(function_target)
    # print(diff_function)

    def f_func(*passed_args):
        if diff:
            argdict = dict(zip(args, passed_args))
            result = diff_function.subs(argdict)
            if invalid_data(result) is True or result.is_real is False:
                return False
            else:
                result = absolute(float(result))
                return result.real
        else:
            argdict = dict(zip(args, passed_args))
            result = function_target.subs(argdict)
            if invalid_data(result) is True or result.is_real is False:
                return False
            else:
                result = float(result)
                return result.real

    return f_func, result_number


def invalid_data(function_result):
    flag = False
    if function_result.has(I):
        flag = True
    elif function_result.has(LambertW):
        flag = True

    return flag

# v = "(667.38/x)*(1-E**(-0.146843*x))-40"
# a, b = function_FxP(v, True)
# print(a(4))
# s="-667.38*exp(-0.146843*x)/x"
# a,b= function_FxP(s,increaser=1,result_incre=0)
# print(a)
# print(b)