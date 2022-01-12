import sympy
from sympy import zoo, nan


def function(eq):
    equat = "f(x)=" + eq
    variables, eq_object = equat.split("=", 1)
    # eq_object = eq_object.rstrip('; ')
    args = sympy.sympify(variables).args
    function_target = sympy.sympify(eq_object)

    def f_func(*passed_args):
        argdict = dict(zip(args, passed_args))
        result = function_target.subs(argdict)
        result = zeroDiv_problem(result)
        return float(result)

    return f_func


def zeroDiv_problem(function_result):
    if function_result.has(zoo):
        return nan
    return function_result

# v="(667.38/x)*(1-E**(-0.146843*x))-40"
# a=function(v)
# print(a)
