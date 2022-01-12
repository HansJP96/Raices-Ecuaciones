# Bisection Method
from tkinter import ttk, Toplevel, Canvas, CENTER, NO, END, messagebox

from Eval_funcion import function


# from sympy import Symbol, sin, asin, sinh, asinh, cos, acos, cosh, acosh, tan, atan, tanh, atanh, cot, acot, coth, \
#     acoth, sec, asec, sech, asech, csc, acsc, csch, acsch, E, sqrt

def Bisection_Method(fx, low, up, tol, window=None):  # Mathematical method process, window is to generate messagebox
    iterable = [1]
    xL = [low]
    xU = [up]
    xR = []
    rel_Err = []
    while fx(low) * fx(up) > 0:
        if __name__ == "__main__":
            xL[0] = float(input("Ingrese Limite Inferior:\t"))
            xU[0] = float(input("Ingrese Limite Superior:\t"))
        else:
            messagebox.showerror(title="Fuera de Rango",
                                 message="Los limites seleccionados no encierran la raiz.\nPor favor, escoja otros"
                                         "limites.",
                                 parent=window)
            return

    rel_Err.append(round(abs((xU[0] - xL[0]) / (xU[0] + xL[0])) * 100, 6))

    while rel_Err[-1] >= tol:
        xR.append(round((xL[-1] + xU[-1]) / 2, 6))
        if fx(xL[-1]) * fx(xR[-1]) < 0:
            xU.append(round(xR[-1], 6))
            xL.append(round(xL[-1], 6))
        elif fx(xL[-1]) * fx(xR[-1]) > 0:
            xL.append(round(xR[-1], 6))
            xU.append(round(xU[-1], 6))
        elif fx(xL[-1]) * fx(xR[-1]) == 0:
            pass

        if iterable[-1] == 1:
            pass
        else:
            rel_Err.append(round(abs((xR[-1] - xR[-2]) / xR[-1]) * 100, 6))

        iterable.append(iterable[-1] + 1)

    iterable.pop()
    xL.pop()
    xU.pop()

    return iterable, xL, xU, xR, rel_Err


def Bisection_Results(window, screen_w, screen_h, equation, tolerance):  # As a function allows to be called from GUI
    def table_data():  # This create a treeview table to show method values
        end_line = ""
        # To update table values on window screen (delete previous values)
        for content in table_B.get_children():
            table_B.delete(content)
        window_Bisection.update()
        ################################################################

        # To get method solution and put it on the table
        eq = equation.get()
        low1 = entry_low.get()
        up1 = entry_up.get()
        tol1 = tolerance.get()
        if low1 == "" or up1 == "" or tol1 == "":
            messagebox.showerror(title="Error en Parametros",
                                 message="Por favor verifique si los parametros Limite Inferior, Limite Superior o "
                                         "Tolerancia contienen datos.",
                                 parent=window_Bisection)
            return
        else:
            try:
                low1 = float(low1)
                up1 = float(up1)
                tol1 = float(tol1)
                if float(tol1) == 0:
                    messagebox.showerror(title="Tolerancia Inaceptable",
                                         message="Evite colocar la tolerancia igual a 0.",
                                         parent=window_Bisection)
                    return
            except ValueError:
                messagebox.showwarning(title="Parametros Invalidos",
                                       message="Verifique que los parametros sean numeros reales.",
                                       parent=window_Bisection)
                return
        try:
            ite, xL, xU, xR, Err = Bisection_Method(function(eq), low1, up1, tol1, window_Bisection)
        except ZeroDivisionError:
            messagebox.showerror(title="Error de Metodo",
                                 message="No seleccione limites cuyo valor absoluto sea el mismo.",
                                 parent=window_Bisection)
            return
        except TypeError:   # This cause (ite, xL, xU, xR, Err) are not filled at broken function Bisection_Method (if
            # Zerodivision occurs the function continue and throws error in console, this prevent that)
            return

        for row in range(len(ite)):
            if row == len(ite) - 1:
                end_line = table_B.insert("", END, values=(ite[row], xL[row], xU[row], xR[row], Err[row]),
                                          tags=("last",))
                table_B.tag_configure("last", background="greenyellow")  # Allows set bg color for the last value
            else:
                end_line = table_B.insert("", END, values=(ite[row], xL[row], xU[row], xR[row], Err[row]))
        table_B.see(end_line)
        ###########

        return

    # Toplevel window settings
    window_Bisection = Toplevel(window)
    window_Bisection.geometry(f"610x400+{int(screen_w) + 100}+{int(screen_h) + 60}")
    window_Bisection.title("Metodo de Biseccion")
    window_Bisection.configure(bg="beige")
    ################################################################

    label_low = ttk.Label(window_Bisection, text="Limite Inferior :", background="beige")
    label_low.grid(row=0, column=0, padx=5, pady=10)
    entry_low = ttk.Entry(window_Bisection)
    entry_low.grid(row=0, column=1, padx=5, pady=5)

    label_up = ttk.Label(window_Bisection, text="Limite Superior :", background="beige")
    label_up.grid(row=1, column=0, padx=5, pady=5)
    entry_up = ttk.Entry(window_Bisection)
    entry_up.grid(row=1, column=1, pady=5)

    run_method = ttk.Button(window_Bisection, text="Ejecutar", command=table_data)
    run_method.grid(row=0, column=2)

    bar_sep = Canvas(window_Bisection, height=2, width=595, background="darkgrey", bd=0, highlightthickness=0,
                     borderwidth=8,
                     relief="raised")
    bar_sep.place(x=0, y=70)

    # To select a color for a row with color names instead color hex like "#E1E1E1"
    styletree = ttk.Style()
    styletree.configure('T.Treeview')

    def fixed_map(option):  # This maybe allows you to change the hex color (need more investigation)
        return [elm for elm in style.map('Treeview', query_opt=option) if elm[:2] != ('!disabled', '!selected')]

    style = ttk.Style()
    style.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))
    ################################################################

    # Table format (treeview) of data method
    table_B = ttk.Treeview(window_Bisection, style="T.Treeview", selectmode="extended", height=13,
                           columns=("#1", "#2", "#3", "#4", "#5"),
                           yscrollcommand=True)
    table_B.grid(row=3, column=0, columnspan=10, pady=16, padx=5)
    table_B["show"] = "headings"
    table_B.heading("#1", text="Iteracion", anchor=CENTER)
    table_B.heading("#2", text="Limite Inferior", anchor=CENTER)
    table_B.heading("#3", text="Limite Superior", anchor=CENTER)
    table_B.heading("#4", text="Raiz Calculada", anchor=CENTER)
    table_B.heading("#5", text="Error Relativo", anchor=CENTER)
    table_B.column("#1", minwidth=0, width=120, anchor=CENTER, stretch=NO)
    table_B.column("#2", minwidth=0, width=120, anchor=CENTER, stretch=NO)
    table_B.column("#3", minwidth=0, width=120, anchor=CENTER, stretch=NO)
    table_B.column("#4", minwidth=0, width=120, anchor=CENTER, stretch=NO)
    table_B.column("#5", minwidth=0, width=118, anchor=CENTER, stretch=NO)
    ################################################################

    return

# a=(667.38/x)*(1-E**(-0.146843*x))-40
# a="x**10-1"
# # equation = input("Escriba la ecuacion: ")
# f = function(a)
# a, b, function, d, e = Bisection_Method(f, 0, 1.3, 0.01)
# print(a)
# print(b)
# print(function)
# print(d)
# print(e)

# f = function(equation)
# print(f(4))
