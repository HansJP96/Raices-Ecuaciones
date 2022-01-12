# Method of Fixed Point
from tkinter import ttk, Toplevel, Canvas, CENTER, NO, END, messagebox

from Eval_funcPF import function_FxP
from Assistant import Sci_format


def FixedPoint_Method(gx, init_val, tol, window=None, increaser=0, result_incre=0):
    try:
        f_gx, result_numberBool = function_FxP(gx, increaser=increaser, result_incre=result_incre)
        diff_gx, result_numberBool = function_FxP(gx, True, increaser=increaser, result_incre=result_incre)
        if f_gx is False or diff_gx is False:
            return 0, 0, 0, 0, False, result_numberBool
    except TypeError:
        print("si es que no existe valores a almacenar")
        return 0, 0, 0, 0, False, True

    iterable = [1]
    xR = [init_val]
    gprim_x = [round(diff_gx(xR[-1]), 6)]
    g_xR = [round(f_gx(xR[-1]), 6)]
    rel_Err = [1000]
    counter = 0

    while rel_Err[-1] >= tol:
        xR.append(round(f_gx(xR[-1]), 6))
        gprim_x.append(round(diff_gx(xR[-1]), 6))
        g_xR.append(round(f_gx(xR[-1]), 6))

        if gprim_x[-1] > 1 and gprim_x[-1] > gprim_x[-2]:
            counter += 1
            if counter == 3:
                if __name__ == "__main__":
                    print("El metodo no converge")
                    break
                else:
                    Found_func = False
                    print("no converge aqui")
                    return iterable, xR, gprim_x, rel_Err, Found_func, result_numberBool

        if iterable[-1] == 1:
            rel_Err.append(1000)
        else:
            if iterable[-1] == 2:
                if xR[-2] == 0:
                    rel_Err[-1] = 100.0
                else:
                    rel_Err[-1] = (round(abs((xR[-2] - xR[-3]) / xR[-2]) * 100, 6))
                rel_Err[-2] = "-"
                if xR[-1] == 0:
                    rel_Err.append(100.0)
                else:
                    rel_Err.append(round(abs((xR[-1] - xR[-2]) / xR[-1]) * 100, 6))
            else:
                if xR[-1] == 0:
                    rel_Err.append(100.0)
                else:
                    rel_Err.append(round(abs((xR[-1] - xR[-2]) / xR[-1]) * 100, 6))
        if xR.count(xR[-1]) > 2:
            return 0, 0, 0, 0, False, result_numberBool
        iterable.append(iterable[-1] + 1)

    Found_func = True

    return iterable, xR, gprim_x, rel_Err, Found_func, result_numberBool


def FixedPoint_Results(window, screen_w, screen_h, equation, tolerance):
    def table_data():  # This create a treeview table to show method values
        end_line = ""
        # To update table values on window screen (delete previous values)
        for content in table_B.get_children():
            table_B.delete(content)
        window_FixPoint.update()
        ################################################################

        # To get method solution and put it on the table
        eq = equation.get()
        init1 = entry_initV.get()
        tol1 = tolerance.get()
        if init1 == "" or tol1 == "":
            messagebox.showerror(title="Error en Parametros",
                                 message="Por favor verifique si Valor Inicial o Tolerancia contienen datos.",
                                 parent=window_FixPoint)
            return
        else:
            try:
                init1 = float(init1)
                tol1 = float(tol1)
                if float(tol1) == 0:
                    messagebox.showerror(title="Tolerancia Inaceptable",
                                         message="Evite colocar la tolerancia igual a 0.",
                                         parent=window_FixPoint)
                    return
            except ValueError:
                messagebox.showwarning(title="Parametros Invalidos",
                                       message="Verifique que los parametros Valor Inicial y Tolerancia sean numeros "
                                               "reales.",
                                       parent=window_FixPoint)
                return
        ite = 0
        xR = 0
        gprim_x = 0
        Err = 0
        try:
            Found_func = False
            increase = -1
            result_incre = 0
            while Found_func is False:
                ite, xR, gprim_x, Err, Found_func, result_final = FixedPoint_Method(eq, init1, tol1, window_FixPoint,
                                                                                    increase, result_incre=result_incre)
                if result_final is False:
                    result_incre += 1
                else:
                    increase += 1
                    result_incre = 0
        # except ZeroDivisionError:
        #     messagebox.showerror(title="Error de Metodo",
        #                          message="No seleccione limites cuyo valor absoluto sea el mismo.",
        #                          parent=window_FixPoint)
        #     return
        except IndexError:
            messagebox.showerror(title="Error de Convergencia",
                                 message="El metodo de Punto Fijo no es adecuado para encontrar la raiz de la "
                                         "ecuacion.\n "
                                         "Por favor intente con otro valor inicial o un metodo diferente.",
                                 parent=window_FixPoint)
        except TypeError:  # This cause (ite, xR, grpim_x, Err) are not filled at broken function FixPoint_Method (if
            # Zerodivision occurs the function continue and throws error in console, this prevent that)
            return
        try:
            for row in range(len(ite)):
                root_value = Sci_format(xR[row])
                diff_value = Sci_format(gprim_x[row])

                if row == len(ite) - 1:
                    end_line = table_B.insert("", END, values=(ite[row], root_value, diff_value, Err[row]),
                                              tags=("last",))
                    table_B.tag_configure("last", background="greenyellow")  # Allows set bg color for the last value
                else:
                    end_line = table_B.insert("", END, values=(ite[row], root_value, diff_value, Err[row]))
        except TypeError:
            pass  # This error its handle above but finish here

        table_B.see(end_line)
        ################################################################

        return

    # Toplevel window settings
    window_FixPoint = Toplevel(window)
    window_FixPoint.geometry(f"610x400+{int(screen_w) + 100}+{int(screen_h) + 60}")
    window_FixPoint.title("Metodo de Punto Fijo")
    window_FixPoint.configure(bg="beige")
    ################################################################

    label_initV = ttk.Label(window_FixPoint, text="Valor Inicial :", background="beige")
    label_initV.grid(row=0, column=0, padx=5, pady=10, rowspan=3)
    entry_initV = ttk.Entry(window_FixPoint)
    entry_initV.grid(row=0, column=1, padx=5, pady=5, rowspan=3,sticky="W")

    run_method = ttk.Button(window_FixPoint, text="Ejecutar",width=7, command=table_data)
    run_method.grid(row=0, column=2, rowspan=3)

    bar_sep = Canvas(window_FixPoint, height=2, width=595, background="darkgrey", bd=0, highlightthickness=0,
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
    table_B = ttk.Treeview(window_FixPoint, style="T.Treeview", selectmode="extended", height=13,
                           columns=("#1", "#2", "#3", "#4"),
                           yscrollcommand=True)
    table_B.grid(row=3, column=0, columnspan=10, pady=48, padx=60)
    table_B["show"] = "headings"
    table_B.heading("#1", text="Iteracion", anchor=CENTER)
    table_B.heading("#2", text="Valor Raiz", anchor=CENTER)
    table_B.heading("#3", text="|g'(x)|", anchor=CENTER)
    table_B.heading("#4", text="Error Relativo", anchor=CENTER)
    table_B.column("#1", minwidth=0, width=120, anchor=CENTER, stretch=NO)
    table_B.column("#2", minwidth=0, width=120, anchor=CENTER, stretch=NO)
    table_B.column("#3", minwidth=0, width=120, anchor=CENTER, stretch=NO)
    table_B.column("#4", minwidth=0, width=120, anchor=CENTER, stretch=NO)
    ################################################################

    return

# q = "33369.0*x*E**(0.146843*x)/(2000.0*x*E**(0.146843*x) + 33369.0)"
# m = "(667.38/x)*(1-E**(-0.146843*x))-40"
# w, e, s, r = FixedPoint_Method(q, 10, 0.01)
# print(w)
# print(e)
# print(s)
# print(r)
