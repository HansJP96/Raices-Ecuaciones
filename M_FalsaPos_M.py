# Method of False Position
from tkinter import ttk, Toplevel, Canvas, CENTER, NO, END, messagebox

from Eval_funcion import function


def FalsePos_Method(fx, low, up, tol, window=None):  # Mathematical method process, window is to generate messagebox
    iterable = [1]
    xL = [low]
    xU = [up]
    xR = []
    f_xL = [round(fx(xL[-1]), 6)]
    f_xU = [round(fx(xU[-1]), 6)]
    rel_Err = [1000]
    while fx(xL[-1]) * fx(xU[-1]) > 0:
        if __name__ == "__main__":
            xL[0] = float(input("Ingrese Limite Inferior:\t"))
            xU[0] = float(input("Ingrese Limite Superior:\t"))
        else:
            messagebox.showerror(title="Fuera de Rango",
                                 message="Los limites seleccionados no encierran la raiz.\nPor favor, escoja otros"
                                         "limites.",
                                 parent=window)
            return
    skip_U = 0
    skip_L = 0
    booster = 0  # This variable works to decrease iteration number (not reference on books, maybe patent)
    while rel_Err[-1] >= tol:
        xR.append(round(xU[-1] - (f_xU[-1] * ((xL[-1]) - xU[-1])) / (f_xL[-1] - f_xU[-1]), 6))
        if fx(xL[-1]) * fx(xR[-1]) < 0:
            xU.append(round(xR[-1], 6))
            xL.append(round(xL[-1], 6))
            f_xU.append(round(fx(xU[-1]), 6))
            f_xL.append(round(fx(xL[-1]), 6))
            skip_U = 0
            skip_L = skip_L + 1
            if skip_L >= 2:
                if skip_L == 2:
                    booster = 0
                f_xL[-1] = round(f_xL[-1] / (2 + booster), 6)
                booster += 1
        elif fx(xL[-1]) * fx(xR[-1]) > 0:
            xL.append(round(xR[-1], 6))
            xU.append(round(xU[-1], 6))
            f_xL.append(round(fx(xL[-1]), 6))
            f_xU.append(round(fx(xU[-1]), 6))
            skip_L = 0
            skip_U = skip_U + 1
            if skip_U >= 2:
                if skip_U == 2:
                    booster = 0
                f_xU[-1] = round(f_xU[-1] / (2 + booster), 6)
                booster += 1
        elif fx(xL[-1]) * fx(xR[-1]) == 0:
            pass

        if iterable[-1] == 1:
            rel_Err.append(1000)
        else:
            if iterable[-1] == 2:
                rel_Err[-1] = (round(abs((xR[-1] - xR[-2]) / xR[-1]) * 100, 6))
                rel_Err[-2] = "-"
            else:
                rel_Err.append(round(abs((xR[-1] - xR[-2]) / xR[-1]) * 100, 6))

        iterable.append(iterable[-1] + 1)

    iterable.pop()
    xL.pop()
    xU.pop()

    return iterable, xL, xU, xR, rel_Err


def FalsePos_Results(window, screen_w, screen_h, equation, tolerance):  # As a function allows to be called from GUI
    def table_data():  # This create a treeview table to show method values
        end_line = ""
        # To update table values on window screen (delete previous values)
        for content in table_B.get_children():
            table_B.delete(content)
        window_FalsePos.update()
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
                                 parent=window_FalsePos)
            return
        else:
            try:
                low1 = float(low1)
                up1 = float(up1)
                tol1 = float(tol1)
                if float(tol1) == 0:
                    messagebox.showerror(title="Tolerancia Inaceptable",
                                         message="Evite colocar la tolerancia igual a 0.",
                                         parent=window_FalsePos)
                    return
            except ValueError:
                messagebox.showwarning(title="Parametros Invalidos",
                                       message="Verifique que los parametros sean numeros reales.",
                                       parent=window_FalsePos)
                return
        try:
            ite, xL, xU, xR, Err = FalsePos_Method(function(eq), low1, up1, tol1, window_FalsePos)
        except ZeroDivisionError:
            messagebox.showerror(title="Error de Metodo",
                                 message="No seleccione limites cuyo valor absoluto sea el mismo.",
                                 parent=window_FalsePos)
            return
        except TypeError:  # This cause (ite, xL, xU, xR, Err) are not filled at broken function FalsePos_Method (if
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
        ################################################################

        return

    # Toplevel window settings
    window_FalsePos = Toplevel(window)
    window_FalsePos.geometry(f"610x400+{int(screen_w) + 100}+{int(screen_h) + 60}")
    window_FalsePos.title("Metodo de de Falsa Posicion Modificado")
    window_FalsePos.configure(bg="beige")
    ################################################################

    label_low = ttk.Label(window_FalsePos, text="Limite Inferior :", background="beige")
    label_low.grid(row=0, column=0, padx=5, pady=10)
    entry_low = ttk.Entry(window_FalsePos)
    entry_low.grid(row=0, column=1, padx=5, pady=5)

    label_up = ttk.Label(window_FalsePos, text="Limite Superior :", background="beige")
    label_up.grid(row=1, column=0, padx=5, pady=5)
    entry_up = ttk.Entry(window_FalsePos)
    entry_up.grid(row=1, column=1, pady=5)

    run_method = ttk.Button(window_FalsePos, text="Ejecutar", command=table_data)

    run_method.grid(row=0, column=2)

    bar_sep = Canvas(window_FalsePos, height=2, width=595, background="darkgrey", bd=0, highlightthickness=0,
                     borderwidth=8,
                     relief="raised")
    bar_sep.place(x=0, y=70)

    # To select a color for a row with color names instead color hex like "#E1E1E1"
    styletree = ttk.Style()
    styletree.configure('T.Treeview')

    def fixed_map(option):  # This maybe allows you to change the hex color to name color (need more investigation)
        return [elm for elm in style.map('Treeview', query_opt=option) if elm[:2] != ('!disabled', '!selected')]

    style = ttk.Style()
    style.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))
    ################################################################

    # Table format of data method
    table_B = ttk.Treeview(window_FalsePos, style="T.Treeview", selectmode="extended", height=13,
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
# a = "(667.38/x)*(1-E**(-0.146843*x))-40"
# "x**2+3*x-x**3" necesito mirar esta
# a = "x**10 -1"
# a = "x**3+x-1"
# a="x**3+4*x**2-10"
# f = function(a)
# a, b, function, d, e = FalsePos_Method(f, 1, 2, 0.00003)
#
# print(a)
# print(b)
# print(function)
# print(d)
# print(e)
