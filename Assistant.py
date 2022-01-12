# Multipurpose module to optimize code

from tkinter import messagebox, Toplevel, ttk

from matplotlib.figure import Figure
from numpy import linspace
from sympy import Symbol, lambdify, SympifyError
from sympy.testing.pytest import ignore_warnings


def Graph_function(lower_x=-5, higher_x=5, function=None, figure_object=Figure.add_subplot, main_window=None,
                   canvas_frame=None):
    try:
        if function == "":
            messagebox.showerror(tittle="Error de Procesamiento", message="No se ha ingresado ecuacion.",
                                 parent=main_window)
            return

        graph = figure_object
        graph.clear()

        x = Symbol("x")
        x_min = lower_x  #
        x_max = higher_x  #
        flag_stop = False
        f = lambdify(x, function, "numpy")
        no_rootCounter = 0
        axis_x = 0
        func = 0
        while flag_stop is False:
            points = int(abs(x_min - x_max) / 0.1)
            axis_x = linspace(x_min, x_max, points, endpoint=True)
            with ignore_warnings(RuntimeWarning):
                func = f(axis_x)

            min_y = min(func)
            max_y = max(func)

            if min_y * max_y <= 0:
                flag_stop = True

            if flag_stop is False:
                x_min *= 2
                x_max *= 2
            no_rootCounter += 1
            if no_rootCounter == 15:
                messagebox.showerror(title="Error de Convergencia",
                                     message="La ecuacion insertada no presenta raices reales\n "
                                             "o su raiz es exactamente 0.",
                                     parent=main_window)
                break

        Graph_aspect(graph)
        graph.plot(axis_x, func, color="red")
        graph.relim()
        if no_rootCounter < 15:
            if isinstance(main_window, Toplevel):
                graph.axes.autoscale()
            else:
                graph.set_ylim(x_min * 10, x_max * 10)
        else:
            graph.set_ylim(-100, 100)
            graph.set_xlim(-100, 100)

        canvas_frame.draw()

    except SympifyError:
        messagebox.showwarning(title="Advertencia: Error de Sintaxis",
                               message="La ecuacion esta mal representada, por favor verifique lo siguiente:\n\n"
                                       "* Uso incorrecto de los parentesis.\n"
                                       "* Uso incorrecto de signos matematicos.",
                               parent=main_window)
    except NameError as err_var:
        name = str(err_var.args[0])
        first_aphos = name.find("'")
        second_aphos = name.find("'", first_aphos + 1)
        name = name[first_aphos + 1:second_aphos]
        messagebox.showwarning(title="Advertencia: Error en Expresion",
                               message="Por favor verifique lo siguiente:\n\n"
                                       "* Utilizar como unica variable la letra x (minuscula).\n"
                                       "* Hay funciones o constantes mal indicadas.\n\n"
                                       f"El error se encuentra en la expresion '{name}'.",
                               parent=main_window)

    except TypeError:
        messagebox.showwarning(title="Advertencia: Expresion no Soportada",
                               message="Por favor verifique que la ecuacion ingresada\n"
                                       " se encuentre correctamente expresada.",
                               parent=main_window)


def Graph_aspect(figure_graph=Figure.add_subplot):
    graph = figure_graph
    graph.axhline(0, color='black')
    graph.axvline(0, color='black')
    graph.set_xlabel('x', fontsize=16)
    graph.set_ylabel('F(x)', fontstyle="oblique", fontsize=16)
    graph.grid()


def Lim_window(main_window, main_width, main_height):
    limit_window = Toplevel(main_window)
    limit_window.title("Dominio para la Funcion")
    limit_window.configure(background="beige")

    window_width = 500
    window_height = 130
    centerx = main_width / 2 - window_width / 2
    centery = main_height / 2 - window_height / 2
    limit_window.geometry(f"{window_width}x{window_height}+{int(centerx) - 280}+{int(centery) - 100}")

    label_style = ttk.Style()
    label_style.configure("BW.TLabel", background="beige")
    label_style.map("BW.TLabel", background=[("active", "beige")])

    info_text = ttk.Label(limit_window,
                          text="Establezca el dominio de la funcion digitando sus limites a continuacion :\n"
                               "        (Todos los campos deben llenarse con numeros enteros)",
                          style="BW.TLabel")
    info_text.grid(row=0, column=0, columnspan=5, padx=10, pady=5)

    lower_x = ttk.Label(limit_window, text="Limite Inferior =", style="BW.TLabel")
    lower_x.grid(row=1, column=0, pady=5)

    lower_entry = ttk.Entry(limit_window)
    lower_entry.grid(row=1, column=1, pady=5)

    higher_x = ttk.Label(limit_window, text="Limite Superior =", style="BW.TLabel")
    higher_x.grid(row=2, column=0, pady=5)

    higher_entry = ttk.Entry(limit_window)
    higher_entry.grid(row=2, column=1, pady=5)

    plot_button2 = ttk.Button(limit_window, text="Plot")
    plot_button2.grid(row=1, column=2, rowspan=2)

    return plot_button2, lower_entry, higher_entry, limit_window


def Assert_lim(second_window, low, high):
    val = [["Limite Inferior", low], ["Limite Superior", high]]
    i = 0

    try:
        for i in range(len(val)):
            val[i][1] = float(val[i][1])
        if val[0][1] >= val[1][1]:
            messagebox.showwarning(title="Limites Erroneos",
                                   message="El Limite Inferior es mayor o igual al Limite Superior.\n"
                                           "Cerciorese que los valores correspondan a lo indicado.",
                                   parent=second_window)
            return
        return val[0][1], val[1][1]

    except ValueError:
        if val[i][1] == "":
            messagebox.showwarning(title="Valor Vacio", message=f"No se digito valor alguno para {val[i][0]}.",
                                   parent=second_window)

        elif " " in val[i][1]:
            messagebox.showwarning(title="Error en Numero",
                                   message=f"El valor para {val[i][0]} contiene al menos un espacio "
                                           f"entre digitos.",
                                   parent=second_window)

        elif val[i][1].isupper() or val[i][1].islower() or val[i][1].count(".") >= 2 or \
                val[i][1].count("+", 1) >= 1 or val[i][1].count("-", 1) >= 1:
            messagebox.showwarning(title="Valor Invalido",
                                   message=f"El valor para {val[i][0]} no es un numero real.\n\n"
                                           f"Modifique el valor a un Numero Entero.",
                                   parent=second_window)

        elif not val[i][1].isalnum() and (val[i][1].count(".") <= 1) and (
                val[i][1].startswith(("+", "-", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"))):
            messagebox.showwarning(title="Numero no Valido",
                                   message=f"El valor para {val[i][0]} contiene uno o varios caracteres "
                                           f"desconcidos.\n\n"
                                           f"Modifique el valor a un Numero Entero.",
                                   parent=second_window)

        else:
            messagebox.showwarning(title="Error de Validacion",
                                   message=f"El valor de {val[i][0]} contiene datos que imposibilitan su "
                                           f"procesamiento.\n "
                                           "Por favor verifique que los datos ingresados sea correcto.",
                                   parent=second_window)


def Sci_format(number: float) -> str:
    """
    Convert float number to scientific String number with max 5 decimals.
    
    :param number: Eg. 1.000.000
    :return: 1.0e+06
    """
    if number > 999999:
        number = "{:.5e}".format(number)
    return number
