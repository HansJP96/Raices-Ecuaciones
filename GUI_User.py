import math
import os
import tkinter
from idlelib.tooltip import Hovertip
from tkinter import ttk, Button, messagebox, Canvas, Toplevel

import numpy
from PIL import ImageTk, Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure, SubplotParams
from numpy import linspace, array
from scipy.interpolate import make_interp_spline
from ttkthemes import themed_tk

from Eval_funcion import function
from M_Biseccion import Bisection_Results
from M_FalsaPos_M import FalsePos_Results
from M_PuntoFijo import FixedPoint_Results


thisdir = os.path.dirname(__file__)
help_icon_dir = os.path.join(thisdir, 'images', 'help_icon.png')
graph_icon_dir = os.path.join(thisdir, 'images', 'graph_icon.png')


def graph_function(lower_x=-5, higher_x=5, topStep=1, toplevel_option=False):  # Function to plot the input equation
    try:
        equation = entry_equation.get()
        graph_x.clear()
        global x_value, y_value
        x_value = []
        y_value = []

        if equation == "":
            messagebox.showwarning(message="No se ha ingresado ecuacion.")
        else:
            f = function(equation)
            x = higher_x
            x_neg = lower_x
            zero_proof = []
            counter_change = 0
            iter_count = 0
            step = topStep
            if toplevel_option is False:
                while True:
                    for var in range(x_neg, x, 1):
                        if len(zero_proof) < 1:
                            zero_proof.append(f(var))
                        else:
                            zero_proof.append(f(var))
                            if math.isnan(zero_proof[-1]):
                                zero_proof.pop(-1)
                            if ((zero_proof[-1] < 0) and (zero_proof[-2] < 0)) or (
                                    zero_proof[-1] > 0 and zero_proof[-2] > 0):
                                pass
                            else:
                                counter_change += 1
                    if counter_change == 0:
                        x = x * 3
                        x_neg = x_neg * 3
                        zero_proof.clear()
                    else:
                        x = x * 2
                        x_neg = x_neg * 2
                        break
                    iter_count += 1
                    if iter_count == 6:
                        messagebox.showerror(title="Error de Convergencia", message="La ecuacion insertada no presenta "
                                                                                    "raices reales.\n")
                        return

            graph_x.set_xlim([x_neg, x])
            for value in range(x_neg, x, step):
                x_value.append(value)
                y_value.append(f(value))
                if math.isnan(y_value[-1]):
                    x_value.pop()
                    y_value.pop()

            # To get a smoothed curve for the graph
            x_lin = array(x_value)
            y_lin = array(y_value)

            x_smooth = linspace(min(x_lin), max(x_lin), 300)  # Create 300? points between min and max (another values?)
            spline = make_interp_spline(x_lin, y_lin, k=3)  # Make a splin, k is for grade of smoothness
            y_smooth = spline(x_smooth)  # Need to verify, maybe smooth the y values for x smoothed values
            ################################################################

            # graph_x.plot(x_value, y_value, color="red")
            graph_x.plot(x_smooth, y_smooth, color="red")
            graph_x.axhline(0, color='black')
            graph_x.axvline(0, color='black')
            graph_x.set_xlabel('x', fontsize=16)
            graph_x.set_ylabel('F(x)', fontstyle="oblique", fontsize=16)
            graph_x.grid()

            canvas.draw()

    except ZeroDivisionError:
        messagebox.showwarning(title="Advertencia: Fallo en Expresiones",
                               message="Por favor verifique lo siguiente:\n\n"
                                       "# Utilizar como unica variable la letra x (minuscula).\n"
                                       "# Hay funciones o constantes mal indicadas.")
    except ValueError:
        messagebox.showwarning(title="Advertencia: Error de Sintaxis",
                               message="La ecuacion esta mal representada, por favor verifique lo siguiente:\n\n"
                                       "# Uso incorrecto de los parentesis.\n"
                                       "# Uso incorrecto de signos matematicos.")
    return


def activate_Bisection():  # Call bisection method from M_Biseccion module
    Bisection_Results(root, to_centerx, to_centery, entry_equation, entry_tol)
    return


def activate_FalsePos():  # Call false position method from M_FalsaPos_M module
    FalsePos_Results(root, to_centerx, to_centery, entry_equation, entry_tol)
    return


def activate_FixPoint():  # Call false position method from M_PuntoFijo module
    FixedPoint_Results(root, to_centerx, to_centery, entry_equation, entry_tol)
    return


def help_text():  # Just a guide to input an equation in a correct way
    messagebox.showinfo(title="¿Como introducir una ecuacion?",
                        message="# La ecuacion a ingresar debe contener maximo una variable identificada como 'x'"
                                " por lo que su expresion matematica debe estar en funcion de x.\n\n"
                                "# Los decimales se representan mediante el punto (.).\n"
                                "# Las operaciones de multiplicacion debe representarse correctamente con el simbolo "
                                "(*).\n\n "
                                "  Ejemplo: 2x (forma incorrecta) => 2*x (forma correcta).\n\n"
                                "# La representacion de potencias viene dado por ** (doble signo de multiplicacion).\n"
                                "  Ejemplo: x**2 => x^2 o como se leeria 'x al cuadrado'.\n\n"
                                "# Las funciones trigometricas se escriben tal como se ha definido su abreviacion y su"
                                "valor objetivo debe ir siempre entre parentesis.\n"
                                "Ejemplo:\n"
                                "         sin(x) => Funcion Seno (se aplico su abreviacion como sin).\n"
                                "         cos(x) => Funcion Coseno.\n"
                                "         tan(x) => Funcion Tangente.\n"
                                "         csc(x) => Funcion Cosecante.\n"
                                "         sec(x) => Funcion Secante.\n"
                                "         cot(x) => Funcion Cotangente.\n"
                                "  Asi mismo es posible usar las funciones inversas e hiperbolicas:\n"
                                "  asin, sinh, asinh, acos, cosh, acosh, atan, tanh, atanh,acot, coth,\n"
                                "  acoth, asec, sech, asech, acsc, csch, acsch.\n\n"
                                "# Las constantes pi y euler se expresan como (pi) y (E), respectivamente.\n\n"
                                "# La raiz cuadrada se puede expresar mediante sqrt() o tambien es posible expresar "
                                "cualquier tipo de radicacion en su forma de potencia.\n "
                                "  Ejemplo:\n"
                                "          sqrt(x) = x**(1/2) | sqrt(4) = 4**(1/2).\n"
                                "          x**(1/3) => Raiz Cubica")
    return


def change_limx():
    def assert_values():
        val = [["Limite Inferior", lower_entry.get()], ["Limite Superior", higher_entry.get()],
               ["Paso", step_entry.get()]]
        i = 0

        # To avoid some error in input cells like exchange of limits, Step less than 0 and not integer
        try:

            for i in range(len(val)):
                val[i][1] = int(val[i][1])
            if val[0][1] >= val[1][1]:
                messagebox.showwarning(title="Limites Erroneos",
                                       message="El Limite Inferior es mayor o igual al Limite Superior.\n"
                                               "Cerciorese que los valores correspondan a lo indicado.",
                                       parent=limit_window)
                return
            elif val[2][1] <= 0:
                messagebox.showwarning(title="Paso no Valido",
                                       message="El valor de Paso no puede ser menor o igual a 0.", parent=limit_window)
                return
            elif int(val[2][1]) > numpy.abs((int(val[1][1])) - (int(val[0][1]))) // 4 + 1:
                messagebox.showwarning(title="Fallo en Metodo Grafico",
                                       message=f"El valor de Paso ingresado no genera el numero de puntos minimo para "
                                               f"generar un grafico suavizado.\n "
                                               f"Para los limites seleccionados, es posible utilizar un Paso "
                                               f"maximo de {numpy.abs((int(val[1][1])) - (int(val[0][1]))) // 4 + 1}.",
                                       parent=limit_window)
                return

            graph_function(val[0][1], val[1][1] + val[2][1], val[2][1], True)

        except ValueError:
            if val[i][1] == "":
                messagebox.showwarning(title="Valor Vacio", message=f"No se digito valor alguno para {val[i][0]}.",
                                       parent=limit_window)

            elif " " in val[i][1]:
                messagebox.showwarning(title="Error en Numero",
                                       message=f"El valor para {val[i][0]} contiene al menos un espacio "
                                               f"entre digitos.",
                                       parent=limit_window)

            elif val[i][1].isupper() or val[i][1].islower() or val[i][1].count(".") >= 2 or \
                    val[i][1].count("+", 1) >= 1 or val[i][1].count("-", 1) >= 1:
                messagebox.showwarning(title="Valor Invalido",
                                       message=f"El valor para {val[i][0]} no es un numero real.\n"
                                               f"Modifique el valor a un Numero Entero.\n",
                                       parent=limit_window)

            elif len(val[i][1].split(".", 1)) == 2 and (
                    val[i][1].split(".", 1)[0].startswith(
                        ("+", "-", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"))) and \
                    val[i][1].split(".", 1)[1].isdigit():
                messagebox.showwarning(title="Numero no Valido",
                                       message=f"Se ha ingresado '{val[i][1]}' para {val[i][0]}.\nRecuerde que debe "
                                               f"ingresar solo Numeros Enteros.",
                                       parent=limit_window)

            elif not val[i][1].isalnum() and (val[i][1].count(".") <= 1) and (
                    val[i][1].startswith(("+", "-", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"))):
                messagebox.showwarning(title="Error Aritmetico",
                                       message=f"El valor para {val[i][0]} contiene uno o varios caracteres "
                                               f"desconcidos.\n "
                                               f"Modifique el valor a un Numero Entero.\n",
                                       parent=limit_window)

            else:
                messagebox.showwarning(title="Error de Validacion",
                                       message=f"El valor de {val[i][0]} contiene datos que imposibilitan su "
                                               f"procesamiento.\n "
                                               "Por favor verifique que los datos ingresados sea correcto.",
                                       parent=limit_window)
        ################################################################
        return

    limit_window = Toplevel(root)
    limit_window.title("Dominio de la Funcion")
    limit_window.configure(background="beige")

    window_width = 500
    window_height = 150
    centerx = root.winfo_screenwidth() / 2 - window_width / 2
    centery = root.winfo_screenheight() / 2 - window_height / 2
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

    step_label = ttk.Label(limit_window, text="Paso =", style="BW.TLabel")
    step_label.grid(row=3, column=0)

    step_entry = ttk.Entry(limit_window)
    step_entry.grid(row=3, column=1)

    plot_button2 = ttk.Button(limit_window, text="Plot", command=assert_values)
    plot_button2.grid(row=2, column=2)

    return


# Initiation of tkinter window
root = themed_tk.ThemedTk()
root.get_themes()
root.set_theme("radiance")
root.title("Raices de Ecuaciones")
root.configure(bg="beige")
################################################################

# A way to center tkinter window on screen
root_width = 850
root_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
to_centerx = screen_width / 2 - root_width / 2
to_centery = screen_height / 2 - root_height / 2

root.geometry(f"{root_width}x{root_height}+{int(to_centerx)}+{int(to_centery) - 20}")
################################################################

# root.minsize(800, 600)

label_equation = ttk.Label(root, text="  Escriba la ecuacion :  ", font=("Helvetica", 18, "bold"), borderwidth=5,
                           relief="sunken")
label_equation.grid(row=0, column=0, pady=10)

entry_equation = ttk.Entry(root, width=25, font=("Helvetica", 14))
entry_equation.grid(row=1, column=0, padx=10, pady=5)

# To put background color of all ttk object to the same color as background color of window (radiance theme cause color
# alteration)
style_backgttk = ttk.Style()
style_backgttk.configure("TButton", background="beige")
style_backgttk.map("TButton", background=[("active", "beige")])
################################################################

graph_Button = ttk.Button(root, text="Plot", width=5, command=graph_function)
graph_Button.grid(row=2, column=0, padx=10)

label_fx = ttk.Label(root, text="F(x) =")
label_fx.config(background="beige", font=("font name", 12, "bold"))
label_fx.place(x=10, y=105)

# The way to adjust an image (png,etc) to a specific size (this case on button frame)
help_pic = Image.open(help_icon_dir)
resized_help = help_pic.resize((30, 30), Image.ANTIALIAS)
help_icon = ImageTk.PhotoImage(resized_help)

graph_pic = Image.open(graph_icon_dir)
resized_graph = graph_pic.resize((65, 65), Image.ANTIALIAS)
graph_icon = ImageTk.PhotoImage(resized_graph)
################################################################

help_button = Button(root, image=help_icon, highlightthickness=5, bd=0, background="beige", command=help_text,
                     cursor="hand2")
help_button.place(x=27, y=130)
float_help = Hovertip(help_button, "Ayuda para ingresar \nuna ecuacion", hover_delay=100)

graphIcon_button = Button(root, image=graph_icon, highlightthickness=0, bd=1, background="beige", command=change_limx,
                          cursor="hand2")
graphIcon_button.place(x=260, y=140)
float_graph = Hovertip(graphIcon_button, "Seleccionar limites", hover_delay=100)

label_note_eq = ttk.Label(root, text="  Nota : La variable a utilizar en la ecuacion debe ser ' x '.", borderwidth=10,
                          relief="solid", foreground="red")
label_note_eq.grid(row=3, column=0, padx=10, pady=5)

# To create the two orange(coral) bars to enclose all method button
square_line1 = Canvas(root, height=2, width=300, background="coral", bd=0, highlightthickness=0, borderwidth=8,
                      relief="raised")
square_line1.place(x=50, y=270)  # Top bar
square_line2 = Canvas(root, height=2, width=300, background="coral", bd=0, highlightthickness=0, borderwidth=8,
                      relief="raised")
square_line2.place(x=50, y=550)  # Bottom bar
################################################################

label_MSelection = ttk.Label(root, text="Seleccione el metodo para encontrar la raiz:", background="beige")
label_MSelection.grid(row=4, column=0)

label_tol = ttk.Label(root, text="(Tolerancia(%)=            )", background="beige")
label_tol.place(x=115, y=312)
entry_tol = ttk.Entry(root, width=6)
entry_tol.place(x=225, y=312)

# From here all the method button are placed
m_Bisection = ttk.Button(root, text="Metodo de Biseccion", command=activate_Bisection, width=19)
m_Bisection.grid(row=5, column=0)

m_FalsaPos = ttk.Button(root, text="M. Falsa Posicion Mod.", command=activate_FalsePos, width=19)
m_FalsaPos.place(x=108, y=375)

m_FixPoint = ttk.Button(root, text="Metodo Punto Fijo", command=activate_FixPoint, width=19)
m_FixPoint.place(x=108, y=410)
################################################################

# Code for add a graph draw on window mode --Figure,FigureCanvasTkAgg,NavigationToolbar2Tk are the most important--
x_value = []
y_value = []
#  Figure is responsible of the size white frame where graph is placed (figsize is the size frame, dpi relate to zoom?¿)
fig = Figure(figsize=(6, 6), dpi=70, edgecolor="tomato", facecolor="azure", linewidth=4,
             subplotpars=SubplotParams(0.15))
graph_x = fig.add_subplot(1, 1, 1)  # Add the graph in the frame
graph_x.axhline(0, color='black')
graph_x.axvline(0, color='black')
graph_x.set_xlabel('x', fontsize=16)
graph_x.set_ylabel('F(x)', fontstyle="oblique", fontsize=16)
graph_x.grid()

# I'm not sure about this but it allows to draw the graph in the white frame
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().configure(highlightcolor="red")
canvas.draw()
canvas.get_tk_widget().grid()

# This allows to place the toolbar buttons to handle the graph
toolbar_frame = tkinter.Frame(root)
toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
toolbar.update()
toolbar.configure(background="beige")
toolbar._message_label.config(background="beige")
# toolbar._message_label.pack_configure(side=tkinter.LEFT)
# for button in toolbar.winfo_children():
#     button.configure(background="dark gray")
canvas.get_tk_widget().grid(row=0, column=2, rowspan=8, columnspan=8, padx=10, pady=10)
toolbar_frame.grid(row=8, column=2, rowspan=8, columnspan=8)
################################################################

root.mainloop()
