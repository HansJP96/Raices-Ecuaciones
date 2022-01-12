import os
import tkinter
from idlelib.tooltip import Hovertip
from tkinter import ttk, Button, messagebox, Canvas

from PIL import ImageTk, Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure, SubplotParams
from ttkthemes import themed_tk

from Assistant import Graph_function, Graph_aspect, Lim_window, Assert_lim
from M_Biseccion import Bisection_Results
from M_FalsaPos_M import FalsePos_Results
from M_PuntoFijo import FixedPoint_Results

thisdir = os.path.dirname(__file__)
help_icon_dir = os.path.join(thisdir, 'images', 'help_icon.png')
graph_icon_dir = os.path.join(thisdir, 'images', 'graph_icon.png')


def graph_function(x_low=-5, x_high=5, option_plot=False, window=None):  # Function to plot the input equation
    if option_plot is False:
        Graph_function(x_low, x_high, function=entry_equation.get(), figure_object=graph_x,
                       canvas_frame=canvas, main_window=root)
    else:
        try:
            lower, top = Assert_lim(second_window=window, low=x_low, high=x_high)
            Graph_function(lower, top, function=entry_equation.get(), figure_object=graph_x,
                           canvas_frame=canvas, main_window=window)
        except TypeError:
            pass


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


def limits_window():
    plot_button2, low, high, window2 = Lim_window(root, screen_width, screen_height)
    plot_button2.config(command=lambda: graph_function(x_low=low.get(), x_high=high.get(),
                                                       option_plot=True, window=window2))


# Initiation of tkinter window
root = themed_tk.ThemedTk()
root.get_themes()
root.set_theme("radiance")
root.title("Raices de Ecuaciones")
root.configure(bg="beige")
################################################################

# A way to center tkinter window on screen
root_width = 920
root_height = 610
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
to_centerx = screen_width / 2 - root_width / 2
to_centery = screen_height / 2 - root_height / 2

root.geometry(f"{root_width}x{root_height}+{int(to_centerx)}+{int(to_centery) - 20}")
################################################################
# To put background color of all ttk object to the same color as background color of window (radiance theme cause color
# alteration)
style_backgttk = ttk.Style()
style_backgttk.theme_settings("radiance", {
    "TButton": {"configure":
                    {"background": "beige"},
                "map":
                    {"background": [("active", "beige")]}
                },
    "TLabelframe": {"configure":
                        {"background": "beige"},
                    "map":
                        {"background": [("active", "beige")]}
                    },
    "TLabelframe.Label": {"configure":
                              {"background": "beige",
                               "font": ("Helvetica", 12, "bold")},
                          "map":
                              {"background": [("active", "beige")]}
                          }
})
# Another method is:
# style_backgttk.configure("TButton", background="beige")
# style_backgttk.map("TButton", background=[("active", "beige")])
############################################################

frame_1 = ttk.Labelframe(root, text="Entrada para Ecuaciones")
frame_1.grid(row=0, column=0, padx=10, pady=10)

frame_2 = ttk.Labelframe(root, text="Metodos")
frame_2.grid(row=1, column=0, padx=10, pady=10)

frame_closed = ttk.LabelFrame(frame_2, text="Cerrados")
frame_closed.grid(row=3, column=0, padx=8, pady=5, sticky="N")

frame_open = ttk.Labelframe(frame_2, text="Abiertos")
frame_open.grid(row=3, column=1, padx=8, pady=5, sticky="N")

frame_3 = ttk.LabelFrame(root, text="Metodo Grafico")
frame_3.grid(row=0, column=1, padx=10, pady=10, rowspan=2)

# In frame_1:
label_equation = ttk.Label(frame_1, text=" Escriba la ecuacion : ", font=("Helvetica", 18, "bold"), borderwidth=5,
                           relief="sunken")
label_equation.grid(row=0, column=0, pady=5, columnspan=2)

entry_equation = ttk.Entry(frame_1, width=30, font=("Helvetica", 14))
entry_equation.grid(row=1, column=1, padx=5, pady=5, sticky="W")

graph_Button = ttk.Button(frame_1, text="Graficar", width=7, command=graph_function)
graph_Button.grid(row=2, column=0, columnspan=2, padx=0, ipadx=5)

label_fx = ttk.Label(frame_1, text="F(x) =")
label_fx.config(background="beige", font=("font name", 12, "bold"))
label_fx.grid(row=1, column=0, sticky="E", padx=5)

# The way to adjust an image (png,etc) to a specific size (this case on button frame)
help_pic = Image.open(help_icon_dir)
resized_help = help_pic.resize((30, 30), Image.ANTIALIAS)
help_icon = ImageTk.PhotoImage(resized_help)

graph_pic = Image.open(graph_icon_dir)
resized_graph = graph_pic.resize((65, 65), Image.ANTIALIAS)
graph_icon = ImageTk.PhotoImage(resized_graph)
################################################################

help_button = Button(frame_1, image=help_icon, highlightthickness=5, bd=0, background="beige", command=help_text,
                     cursor="hand2")
help_button.grid(row=2, column=0, sticky="NW", padx=25, columnspan=2)
float_helpButton = Hovertip(help_button, "Ayuda para ingresar \nuna ecuacion", hover_delay=100)

graphIcon_button = Button(frame_1, image=graph_icon, highlightthickness=0, bd=1, background="beige",
                          command=limits_window,
                          cursor="hand2")
graphIcon_button.grid(row=2, column=1, sticky="E", padx=50, ipadx=5)
float_graphIconButton = Hovertip(graphIcon_button, "Seleccione los limites \npara graficar", hover_delay=100)

label_note_eq = ttk.Label(frame_1, text=" Nota : La variable a utilizar en la ecuacion debe ser ' x '.",
                          borderwidth=10,
                          relief="solid", foreground="red")
label_note_eq.grid(row=4, column=0, padx=5, pady=10, columnspan=2)
################################################################

# In frame_2:
# To create the two orange(coral) bars to enclose all method button
square_line1 = Canvas(frame_2, height=2, width=350, background="coral", bd=0, highlightthickness=0, borderwidth=8,
                      relief="raised")
square_line1.grid(row=0, column=0, pady=5, columnspan=2)
# square_line1.place(x=50, y=270)  # Top bar

square_line2 = Canvas(frame_2, height=2, width=350, background="coral", bd=0, highlightthickness=0, borderwidth=8,
                      relief="raised")
square_line2.grid(row=4, column=0, pady=5, columnspan=2)
# square_line2.place(x=50, y=550)  # Bottom bar
################################################################

label_MSelection = ttk.Label(frame_2, text="Seleccione el metodo para encontrar la raiz:", background="beige")
label_MSelection.grid(row=1, column=0, columnspan=2)

label_tol = ttk.Label(frame_2, text="Tolerancia(%) = ", background="beige")
label_tol.grid(row=2, column=0, columnspan=2, ipadx=50)

entry_tol = ttk.Entry(frame_2, width=10)
entry_tol.grid(row=2, column=1, sticky="W", padx=10)
float_entryTol = Hovertip(entry_tol, text="Ingrese la tolerancia \nmaxima aceptable", hover_delay=100)

# From here all the method button are placed
# In frame_closed
m_Bisection = ttk.Button(frame_closed, text="Biseccion", command=activate_Bisection, width=18)
m_Bisection.grid(row=0, padx=5, pady=3)

m_FalsaPos = ttk.Button(frame_closed, text="Falsa Posicion Mod.", command=activate_FalsePos, width=18)
m_FalsaPos.grid(row=1, padx=5, pady=3)

# In frame_open
m_FixPoint = ttk.Button(frame_open, text="Punto Fijo", command=activate_FixPoint, width=18)
m_FixPoint.grid(row=2, padx=5, pady=3)
################################################################


# Code for add a graph draw on window mode --Figure,FigureCanvasTkAgg,NavigationToolbar2Tk are the most important--

#  Figure is responsible of the size white frame where graph is placed (figsize is the size frame, dpi relate to zoom?¿)
fig = Figure(figsize=(6, 6), dpi=70, edgecolor="beige", facecolor="beige", linewidth=4,
             subplotpars=SubplotParams(0.15))
graph_x = fig.add_subplot(1, 1, 1)  # Add the graph in the frame
Graph_aspect(graph_x)

# I'm not sure about this but it allows to draw the graph in the white frame
canvas = FigureCanvasTkAgg(fig, master=frame_3)
canvas.get_tk_widget().configure(highlightcolor="red")
canvas.draw()
canvas.get_tk_widget().grid()

# This allows to place the toolbar buttons to handle the graph
# In frame_3:
toolbar_frame = tkinter.Frame(frame_3)
toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
toolbar.update()
toolbar.configure(background="beige")
toolbar._message_label.config(background="beige")
# toolbar._message_label.pack_configure(side=tkinter.LEFT)
# for button in toolbar.winfo_children():
#     button.configure(background="dark gray")
canvas.get_tk_widget().grid(row=0, padx=5, pady=5)
toolbar_frame.grid(row=1)
################################################################

root.mainloop()
