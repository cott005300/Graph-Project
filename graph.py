from logging import INFO
import re
import math
from tkinter.constants import ANCHOR, CENTER, X
from typing import Text
import matplotlib
import sys
import os
from tkinter import PhotoImage, Scale, Scrollbar, Toplevel, simpledialog

import time
import numpy as np
import sympy
from PIL import Image, ImageTk
from Sketch import sketch

from sort import sort
from SUVAT_maths import SUVAT
from make_list import make_list

from numpy import imag, select
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import style
from matplotlib import pyplot as plt

import tkinter as tk
from tkinter import Label, ttk

from fractions import Fraction
from decimal import Decimal
from math import ceil, degrees, e, sqrt as sqrt
sys.setrecursionlimit(5000)
#print(sys.getrecursionlimit())

style.use("ggplot")
ctrlmenu = None
f = Figure(figsize=(6,6), dpi=100) 
s = f.add_subplot(111)
canvas = FigureCanvasTkAgg(f)

#(bulk comment = 'ctr' +  '/')
#enter key to use
 # go = True
 # while go:
 #     key = time.time()/math.sin(0.13)/1000000000
 #     key = f'{key:.9}'
 #     password = simpledialog.askstring("Sign in", "Key:") 
 #     print(password)
 #     if password == key[-3:]:
 #         go = False
 #         break
 #     if password == None:
 #         sys.exit()

#s.set_title("Cartesian coordinate system")

limit = 40
l1 = s.plot([-limit,limit],[0,0], "black")
l2 = s.plot([0,0],[-limit,limit], "black")
canvas.draw()

# σ Σ x̄ ²
graph = ""
org_graph = ""
graph_type = ""
roots = []
turning_points = []
colours = ["red","orange","lime","green","dodgerblue","blue","pink","purple","saddlebrown"]
colour_index = 0
graph_storage = []
x = []
y = []
x_range = []
axes_type = None


def colour_change():
    global colour_index
    global ctrlmenu
    if colour_index < len(colours)-1:
        colour_index +=1
    else:
        colour_index = 0

    if colours[colour_index] == "dodgerblue":
        ctrlmenu.entryconfig(0,label="Swap Colour: light blue")
    elif colours[colour_index] == "saddlebrown":
        ctrlmenu.entryconfig(0,label="Swap Colour: brown")
    else:
        ctrlmenu.entryconfig(0,label="Swap Colour: "+colours[colour_index])

def popupmesg(title, msg):
    popup = tk.Tk()
    popup.wm_title(title)
    root = popup
    if title[0] == "y":
        frame = tk.LabelFrame(popup, fg=colours[colour_index-1], text=org_graph, font=(12))
        frame.pack(expand=True, fill="both", padx=5, pady=5)
        root = frame
    label = ttk.Label(root, text=msg, font=("Verdana", 10))
    label.pack(side="top", fill="x", padx=20, pady=10)
    B1 = ttk.Button(root, text="okay", command= popup.destroy)
    B1.pack(pady=10)
    return

def clear_axis(MBset):
    global colour_index
    global limit
    global l1, l2
    colour_index = 0
    s.clear()
    if MBset:
        limit = 2
        s.axis([-2.1,2.1,-2.1,2.1])
        s.set_xlabel('Real')
        s.set_ylabel('Imaginary')
    else:
        limit = 40
        l1 = s.plot([-limit,limit],[0,0], "black")
        l2 = s.plot([0,0],[-limit,limit], "black")
        s.set_ylim([0-(1.05*limit), 0+(1.05*limit)])
        s.set_xlim([0-(1.05*limit), 0+(1.05*limit)])
    graph_storage = []
    canvas.draw()

def axis_pos():
    global limit
    posinx = simpledialog.askstring("Axes Position", "Type X axes position")
    if posinx == None:
            return
    posiny= simpledialog.askstring("Axes Position", "Type Y axes position")
    try:
        posinx = float(posinx)
        posiny = float(posiny)
        if posinx > limit or posinx < -limit or posiny > limit or posiny < -limit:
            raise
    except:
        return
    s.set_ylim([posiny-(1.05*limit), posiny+(1.05*limit)])
    s.set_xlim([posinx-(1.05*limit), posinx+(1.05*limit)])
    canvas.draw()

def axis_size(limitIn):
    global l1, l2
    global limit
    if limitIn == 0:
        limitIn = simpledialog.askstring("Axes Size", "Type an axes size")
    try:
        limit = float(limitIn)
        if limitIn == 0:
            raise
    except:
        return
    s.axis([(1.05*-limit), (1.05*limit), (1.05*-limit), (1.05*limit)])
    line = l1.pop(0)
    line.remove()
    line = l2.pop(0)
    line.remove()
    l1 = s.plot([-limit,limit],[0,0], "black")
    l2 = s.plot([0,0],[-limit,limit], "black")
    canvas.draw()


class main(tk.Tk):                                                          #inhertit from tk
    def __init__(self, *args, **kwargs):                                    #initailisation, arguments, key word arguments (variables / disctionaries)
        global ctrlmenu
        tk.Tk.__init__(self,*args,**kwargs)

        tk.Tk.iconbitmap(self, default="p icon.ico")
        tk.Tk.wm_title(self, "Peter's graph")

        container = tk.Frame(self)                                          #edge of window
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)    
        container.grid_columnconfigure(0, weight=1)

        def Turtle():
            popupmesg("Turtle Controls", "'Click & drag' turtle to draw \n'Click' to draw straight lines\
                                    \n'Right click' to clear \n'Space bar' for pen up \n'h' to hide turtle\
                                    \n'Z' for undo \n'Enter' for colour change")
            pagemenu.entryconfig(1,state="disabled")
            sketch.press()
        
        def label():
            labelx = simpledialog.askstring("Axes label", "X label")
            if labelx == None:
                return
            s.set_xlabel(labelx)
            labely = simpledialog.askstring("Axes label", "Y label")
            if labely == None:
                canvas.draw()
                return
            s.set_ylabel(labely)
            canvas.draw()

        def StopWatch():
            popup = tk.Tk()
            popup.wm_title("Stop Watch")
            popup.geometry("190x200")
            popup.stop = False
            popup.h = "00"
            popup.m = "00"
            popup.s = "00"
            popup.ms = "0"            

            def start1():
                popup.stop = False
                start()

            def start():
                if popup.stop == False:
                    time.sleep(0.09104)
                    popup.ms = str(int(popup.ms) + 1)
                    if int(popup.ms) > 9:
                        popup.ms = str(0)
                        popup.s = str(int(popup.s) + 1)
                        if int(popup.s) > 59:
                            popup.s = "00"
                            popup.m = str(int(popup.m) + 1)
                            if int(popup.m) > 59:
                                popup.m = "00"
                                popup.h = str(int(popup.h) + 1)

                    label.config(text = popup.h+':'+popup.m+':'+popup.s+'.'+popup.ms)
                    popup.update()
                    start()

            def Stop():
                popup.stop = True
            
            def clear():
                popup.h = "00"
                popup.m = "00"
                popup.s = "00"
                popup.ms = "0"
                label.config(text = popup.h+':'+popup.m+':'+popup.s+'.'+popup.ms)
                popup.update()

            def Exit():
                popup.stop = True
                popup.destroy()

            frame = tk.LabelFrame(popup, fg=colours[colour_index-1])
            frame.grid(column=0, row=0, padx=5, pady=15, columnspan=2)
            
            label = ttk.Label(frame, text='00:00:00.0', font=("Verdana", 15))
            label.grid(column=0, row=0, padx=5, pady=5)
            StartButt = ttk.Button(popup, text="Start", command= lambda: start1())
            StartButt.grid(row=1, column=0, pady=10, padx=5)
            StopButt = ttk.Button(popup, text="Stop", command= Stop)
            StopButt.grid(row=1, column=1, padx=10)
            ClearButt = ttk.Button(popup, text="Reset", command= clear)
            ClearButt.grid(row=2, column=1)
            B1 = ttk.Button(popup, text="Exit", command= Exit)
            B1.grid(column=0, row=3, pady=20, columnspan=2)

        def undo():
            if graph_storage:
                temp1 = graph_storage[-1]
                temp1.pop(0).remove()
                del graph_storage[-1]
                canvas.draw()

        menubar = tk.Menu(container)
        ctrlmenu = tk.Menu(menubar, tearoff=0)
        ctrlmenu.add_command(label="Swap Colour: "+str(colours[colour_index]), command= colour_change)
        ctrlmenu.add_command(label="Undo", command= undo)
        ctrlmenu.add_command(label="Axes Size", command= lambda: axis_size(0))
        ctrlmenu.add_command(label="Axes Position", command= axis_pos)
        ctrlmenu.add_command(label="Axes Labels", command= label)
        ctrlmenu.add_command(label="Axes Reset", command= lambda: clear_axis(False))
        ctrlmenu.add_separator()
        ctrlmenu.add_command(label="Restart", command=lambda: os.execl(sys.executable, sys.executable, *sys.argv))
        ctrlmenu.add_command(label="Exit", command=sys.exit)
        menubar.add_cascade(label="Controls", menu=ctrlmenu)

        pagemenu = tk.Menu(menubar, tearoff=0)
        pagemenu.add_command(label="Home", command= lambda: self.show_frame(StartPage))
        pagemenu.add_command(label="Stop Watch", command= StopWatch)
        pagemenu.add_command(label="Sketch", command= Turtle)
        menubar.add_cascade(label="Pages", menu=pagemenu)

        tk.Tk.config(self, menu=menubar)

        self.frames = {}

        for F in (StartPage, PageTwo, GraphPage, sortPage, circlePage, PointPage, wavePage, simulPage, Scatter, BarChartPage, statsPage, SUVATPage, calculator, ComplexPage2, complexPointPage, ComplexCiclePage, half_line_Page,PbisectorPage, MBsetPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")                      #north, south, east, west

        self.show_frame(StartPage)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        #
        # 238174
        #frame.configure(bg='ghostwhite')
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def Real():
            global axes_type
            if axes_type != "Real":
                clear_axis(False)
                s.set_xlabel('X')
                s.set_ylabel('Y')
                canvas.draw()
            axes_type = "Real"
            controller.show_frame(PageTwo)
            
            
        def Complex():
            global axes_type
            if axes_type != "Complex":
                clear_axis(False)
                s.set_xlabel('Real')
                s.set_ylabel('Imaginary')
                canvas.draw()
            axes_type = "Complex"
            controller.show_frame(ComplexPage2)


        #self.configure(background='dodgerblue')
        label = ttk.Label(self, text="Home", font=("Verdana", 12))
        label.pack(pady=10, padx=25)
        button2 = ttk.Button(self, text="Cartesian Grid", command=Real) 
        button2.pack(pady=15)
        button3 = ttk.Button(self, text="Argand Digaram", command=Complex) 
        button3.pack(pady = 15)
        button7 = ttk.Button(self, text="Calculator", command=lambda:controller.show_frame(calculator) )
        button7.pack(pady = 15)
        button5 = ttk.Button(self, text="Statistics", command=lambda:controller.show_frame(statsPage) )         #lambda allows you to pass things into function
        button5.pack(pady = 15)
        button6 = ttk.Button(self, text="SUVAT", command=lambda:controller.show_frame(SUVATPage) )
        button6.pack(pady = 15)
        button4 = ttk.Button(self, text="Sort Algorithms", command=lambda:controller.show_frame(sortPage) )
        button4.pack(pady=15)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill="both", expand=True)
        canvas._tkcanvas.pack(side=tk.TOP, fill="both", expand=True)


class PageTwo(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Graph Controls", font=("Verdana", 12))
        label.pack(pady=10, padx=10)
        
        point_button = ttk.Button(self, text="Point", command=lambda: controller.show_frame(PointPage))
        point_button.pack(pady=5)
        circle_button = ttk.Button(self, text="Circle", cursor="circle", command=lambda: controller.show_frame(circlePage))
        circle_button.pack(pady=5)
        Polynomial_button= ttk.Button(self, text="Function", command=lambda: controller.show_frame(GraphPage))                #lambda allows you to pass things into function
        Polynomial_button.pack(pady=5)
        ttk.Button(self, text="Simultaneous", command=lambda: controller.show_frame(simulPage)).pack(pady=5)
        wave_button = ttk.Button(self, text="Wave", command=lambda: controller.show_frame(wavePage))                #lambda allows you to pass things into function
        wave_button.pack(pady=5)
        Rline_button = ttk.Button(self, text="Scatter graph", command=lambda: controller.show_frame(Scatter))
        Rline_button.pack(pady=5)
        BarButton = ttk.Button(self, text="Bar Graph", command=lambda: controller.show_frame(BarChartPage))
        BarButton.pack(pady=5)
        Home_button = ttk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))                #lambda allows you to pass things into function
        Home_button.pack(pady=25)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill="both", expand=True)
        canvas._tkcanvas.pack(side=tk.TOP, fill="both", expand=True)


class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        global canvas
        global graph

        def check_box(self):
            if self.Details.get() == 0:
                self.Details.set(1)
            else:
                self.Details.set(0)
        
        def button1_command(self):
            global roots
            global graph
            global org_graph
            global turning_points
            global x, y
            checkVars.check_polynomial(checkVars, graphIn)
            if draw.polynomial(draw, False):
                graphIn.delete(0, tk.END)
                if self.Details.get() == 1:
                    a, b, c, d, graph_type = graph_details.details()
                    if roots:
                        roots_string = "\n              ".join([str(item) for item in roots])
                        if turning_points:
                            turning_points_string = "\n                          ".join([str(item) for item in turning_points])
                            popupmesg(org_graph ,"Graph type = "+graph_type+"\na = "+str(a)+"  b = "+str(b)+"  c = "+str(c)+"  d = "+str(d)+"\n\nRoot(s) = " + roots_string + "\n \n" + "Turning point(s) = " + turning_points_string) 
                        else:
                            popupmesg(org_graph ,"Graph type = "+graph_type+"\na = "+str(a)+"  b = "+str(b)+"  c = "+str(c)+"  d = "+str(d)+"\n\nRoots = " + roots_string) 
                    elif turning_points:
                        turning_points_string = "\n                          ".join([str(item) for item in turning_points])
                        popupmesg(org_graph ,"Graph type = "+graph_type+"\na = "+str(a)+"  b ="+str(b)+"  c = "+str(c)+"  d = "+str(d)+"\n\nTurning point(s) = " + turning_points_string)
                controller.show_frame(PageTwo)
            else:
                popupmesg(" ","Please try again")          

        tk.Frame.__init__(self, parent)

        #text inputs
        graphIn = ttk.Entry(self, width="23")
        graphLabel = ttk.Label(self, text="f(x)       =", font=("Verdana", 10))

        self.Details = tk.IntVar()
        tick = tk.Checkbutton(self, text="Show details", variable=self.Details, onvalue=True, command=lambda: check_box(self))
        button1 = ttk.Button(self, text="Enter", command=lambda: button1_command(self))
        button2 = ttk.Button(self, text="Back", command=lambda: controller.show_frame(PageTwo))
        
        graphLabel.grid(row=0,column=0, pady=25)
        graphIn.grid(row=0,column=1, pady=25)

        tick.grid(row=1, column=1, pady=5)
        button1.grid(row=2,column=1, pady=5)
        button2.grid(row=2,column=0, pady=5, padx=60)

class circlePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def button_command():
            Bool, r, cx, cy =  checkVars.circle(checkVars, rIn, cxIn, cyIn)
            if Bool == True:
                draw.circle(draw, r, -cx, -cy, "cartesian")
                controller.show_frame(PageTwo)

        rIn = ttk.Entry(self, width="10")
        cxIn = ttk.Entry(self, width="10")
        cyIn = ttk.Entry(self, width="10")

        rlabel = ttk.Label(self, text="Radius         =", font=("Verdana", 9))
        cxlabel = ttk.Label(self, text="Centre X      =", font=("Verdana", 9))
        cylabel = ttk.Label(self, text="Centre Y      =", font=("Verdana", 9))
        button1 = ttk.Button(self, text="Enter", command=button_command)
        button2 = ttk.Button(self, text="Back", command=lambda: controller.show_frame(PageTwo))

        #label.grid(row=0,column=0)
        rlabel.grid(row=1,column=0, padx=65, pady=0)
        cxlabel.grid(row=2,column=0, padx=65, pady=0)
        cylabel.grid(row=3,column=0, padx=65, pady=0)
        rIn.grid(row=1,column=1, padx=5, pady=5)
        cxIn.grid(row=2,column=1, padx=5, pady=5)
        cyIn.grid(row=3,column=1, padx=5, pady=5)
        button1.grid(row=6,column=1, pady=10)
        button2.grid(row=6,column=0, pady=10)

class PointPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def button_command(X_pointin, Y_pointin):
            if draw.point(X_pointin.get(), Y_pointin.get()):  
                X_pointin.delete(0, tk.END)
                Y_pointin.delete(0, tk.END)  
                controller.show_frame(PageTwo)


        X_pointin = ttk.Entry(self, width="10")
        Y_pointin = ttk.Entry(self, width="10")
        Xlabel = ttk.Label(self, text="X         =", font=("Verdana", 9))
        Ylabel = ttk.Label(self, text="Y         =", font=("Verdana", 9))
        button1 = ttk.Button(self, text="Enter", command=lambda: button_command(X_pointin, Y_pointin))
        button2 = ttk.Button(self, text="Back", command=lambda: controller.show_frame(PageTwo))

        Xlabel.grid(row=0,column=0, padx=65, pady=5)
        Ylabel.grid(row=1,column=0, padx=65, pady=5)
        X_pointin.grid(row=0,column=1, padx=5, pady=5)
        Y_pointin.grid(row=1,column=1, padx=5, pady=5)
        button1.grid(row=2,column=1, pady=10)
        button2.grid(row=2,column=0, pady=10)

class wavePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def check_box(self):
            if self.x100.get() == 0:
                self.x100.set(1)
            else:
                self.x100.set(0)
            #print(self.x100.get())

        def button_command(self,type):
            if self.x100.get() == 1:
                m = 100
                #tick.deselect()
            else:
                m = 1
            draw.wave(type, m)
            controller.show_frame(PageTwo)
            
        self.x100 = tk.IntVar()
        sin_button = ttk.Button(self, text="Sine", command=lambda: button_command(self,"Sine"))         #cursor="dot",
        cos_button = ttk.Button(self, text="Cosine", command=lambda: button_command(self,"Cosine"))
        tan_button = ttk.Button(self, text="Tangent", command=lambda: button_command(self,"Tangent"))
        tick = tk.Checkbutton(self, text="x100", variable=self.x100, command=lambda: check_box(self))
        button2 = ttk.Button(self, text="Back", command=lambda: controller.show_frame(PageTwo))

        sin_button.pack(pady=10)
        cos_button.pack(pady=10)
        tan_button.pack(pady=10)
        tick.pack(pady=10)
        button2.pack(pady=20)

class simulPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def check_box(tab):
            if tab == "tab1":
                if Draw.get() == False:
                    Draw.set(True)
                else:
                    Draw.set(False)
            elif tab == "tab2":
                if Draw2.get() == False:
                    Draw2.set(True)
                else:
                    Draw2.set(False)


        def button_command(tab):
            global graph
            global org_graph

            if tab == "tab1":
                x1 = X1_pointin.get()
                y1 = Y1_pointin.get()
                c1 = const1_pointin.get()
                x2 = X2_pointin.get()
                y2 = Y2_pointin.get()
                c2 = const2_pointin.get()

            elif tab == "tab2":
                x1 = X1_pointin2.get()  #x squared
                y1 = Y1_pointin2.get()  #x
                c1 = Z1_pointin2.get()  #constant
                c2 = 0
                x2 = X2_pointin2.get()
                y2 = Y2_pointin2.get()

            try:
                x1 = float(x1)
                y1 = float(y1)
                c1 = float(c1)
                x2 = float(x2)
                y2 = float(y2)
                c2 = float(c2)
            except:
                popupmesg("!", "Can't take that")
                return
            if tab == "tab1":
                X, Y = solve_lin(x1, c1, y1, x2, c2, y2)
                if Draw.get() == True:
                    graph = str(x1/y1)+"*x +"+str(c1/y1)
                    org_graph = str(y1)+"y="+str(x1)+"x +"+str(c1)
                    draw.polynomial(draw, False)
                    graph = str(x2/y2)+"*x +"+str(c2/y2)
                    org_graph = str(y2)+"y="+str(x2)+"x +"+str(c2)
                    draw.polynomial(draw, False)
                    draw.point(round(X, 2), round(Y,2))

            elif tab == "tab2":
                solve_quad(x1, y1, c1,  x2, y2)
                if Draw2.get() == True:
                    graph = str(x1)+"*(x)**2 +"+str(y1)+"*x +"+str(c1)
                    org_graph = "y ="+str(x1)+"x² +"+str(y1)+"x +"+str(c1)
                    draw.polynomial(draw, False)
                    graph = str(x2)+"*x +"+str(y2)
                    org_graph = "y="+str(x2)+"x +"+str(y2)
                    draw.polynomial(draw, False)
                    #draw.point(round(X, 2), round(Y,2))
            
        def button_command2():
            values = []
            values.append(X1in.get())
            values.append(X2in.get())
            values.append(X3in.get())
            values.append(Y1in.get())
            values.append(Y2in.get())
            values.append(Y3in.get())
            values.append(Z1in.get())
            values.append(Z2in.get())
            values.append(Z3in.get())
            values.append(C1in.get())
            values.append(C2in.get())
            values.append(C3in.get())
            for i in range(0,len(values)):
                if values[i] == "":
                    values[i] = 0
                try:
                    values[i] = float(values[i])
                except:
                    popupmesg("!", "Can't take that")
                    return

            x,y, z = sympy.symbols('x,y,z')
            eq1 = sympy.Eq(values[0]*x + values[3]*y + values[6]*z, values[9])
            eq2 = sympy.Eq(values[2]*x + values[4]*y + values[7]*z, values[10])
            eq3 = sympy.Eq(values[3]*x + values[5]*y + values[8]*z, values[11])
            result = sympy.solve([eq1,eq2, eq3],(x,y,z))

            answer.config(text="Coords or intersection:\n"+str(result[x])+"\n"+str(result[y])+"\n"+str(result[z])) 


        def solve_lin(a, b, c, d, e, f):
            #A = np.array([[x1,-y1], [x2,-y2]])
            #B = np.array([-c1,-c2])
            #D = np.linalg.inv(A)
            #E = np.dot(D,B)
            #Xsolution.config(text="X = "+str(E[0]))
            #Ysolution.config(text="Y = "+str(E[1]))
            x,y = sympy.symbols('x,y')
            eq1 = sympy.Eq(a*x + b, c*y)
            eq2 = sympy.Eq(d*x + e, f*y)
            result = sympy.solve([eq1,eq2],(x,y))
            Xsolution.config(text=str(result))
            return result[x], result[y]

        def solve_quad(a, b, c, d, e):
            x,y = sympy.symbols('x,y')
            eq1 = sympy.Eq(a*x**2 + b*x + c, y)
            eq2 = sympy.Eq(d*x + e, y)
            result = sympy.solve([eq1,eq2],(x,y))
            solution2.config(text="Coords or intersection:\n"+str(result[0])+"\n"+str(result[1]))      #ext(iter(result.values()))
                        
        def clear(tab):
            if tab == "tab1" or tab == "back":
                X1_pointin.delete(0, tk.END)
                X2_pointin.delete(0, tk.END)
                Y1_pointin.delete(0, tk.END)
                Y2_pointin.delete(0, tk.END)
                const1_pointin.delete(0, tk.END)
                const2_pointin.delete(0, tk.END)
                Xsolution.config(text="")
                Y1_pointin.insert(0, "1")
                Y2_pointin.insert(0, "1")
                Draw.set(False)

            if tab == "tab2" or tab == "back":
                X1_pointin2.delete(0, tk.END)
                X2_pointin2.delete(0, tk.END)
                Y1_pointin2.delete(0, tk.END)
                Y2_pointin2.delete(0, tk.END)
                Z1_pointin2.delete(0, tk.END)
                solution2.config(text="")
                Draw2.set(False)

            if tab == "tab3" or tab == "back":
                X1in.delete(0, tk.END)
                X2in.delete(0, tk.END)
                X3in.delete(0, tk.END)
                Y1in.delete(0, tk.END)
                Y2in.delete(0, tk.END)
                Y3in.delete(0, tk.END)
                Z1in.delete(0, tk.END)
                Z2in.delete(0, tk.END)
                Z3in.delete(0, tk.END)
                C1in.delete(0, tk.END)
                C2in.delete(0, tk.END)
                C3in.delete(0, tk.END)

        def back():
            controller.show_frame(PageTwo)

        tabContorle = ttk.Notebook(self)
        tab1 = ttk.Frame(tabContorle)
        tab2 = ttk.Frame(tabContorle)
        tab3 = ttk.Frame(tabContorle)
        tabContorle.add(tab1, text="Linear")
        tabContorle.add(tab2, text="Quadratic")
        tabContorle.add(tab3, text="System")
        tabContorle.pack(expand=1, fill="both")
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill="both", expand=True)
        canvas._tkcanvas.pack(side=tk.TOP, fill="both", expand=True)

        ##################### tab 1 #####################################
        ttk.Label(tab1, text="X", font=("Verdana", 9)).grid(row=0,column=1, padx=5, pady=5)
        ttk.Label(tab1, text="Const", font=("Verdana", 9)).grid(row=0,column=2, padx=5, pady=5)
        ttk.Label(tab1, text="Y", font=("Verdana", 9)).grid(row=0,column=4, padx=5, pady=5)
        ttk.Label(tab1, text="=", font=("Verdana", 9)).grid(row=1,column=3, padx=8, pady=5)
        ttk.Label(tab1, text="=", font=("Verdana", 9)).grid(row=2,column=3, padx=8, pady=5)
        X1_pointin = ttk.Entry(tab1, width="10")
        Y1_pointin = ttk.Entry(tab1, width="10")
        const1_pointin = ttk.Entry(tab1, width="10")
        X2_pointin = ttk.Entry(tab1, width="10")
        Y2_pointin = ttk.Entry(tab1, width="10")
        const2_pointin = ttk.Entry(tab1, width="10")
        Xsolution = ttk.Label(tab1, text="")
        ttk.Separator(tab1, orient='vertical').grid(row=0, column=0, rowspan=5, padx=15)
        Draw = tk.BooleanVar()
        tick = tk.Checkbutton(tab1, text="Draw",onvalue=True, offvalue=False, variable=Draw, command=lambda: check_box("tab1"))
        ttk.Button(tab1, text="Enter", command= lambda: button_command("tab1")).grid(row=6, column=4, pady=20)
        ttk.Button(tab1, text="Clear", command=lambda: clear("tab1")).grid(row=6, column=3)
        ttk.Button(tab1, text="Back", command=back).grid(row=6, column=1)
  
        X1_pointin.grid(row=1,column=1, padx=5, pady=5)
        Y1_pointin.grid(row=1,column=4, padx=5, pady=5)
        const1_pointin.grid(row=1,column=2, padx=5, pady=5)
        X2_pointin.grid(row=2,column=1, padx=5, pady=5)
        Y2_pointin.grid(row=2,column=4, padx=5, pady=5)
        const2_pointin.grid(row=2,column=2, padx=5,pady=5)
        tick.grid(row=5 , column= 4)
        Xsolution.grid(row=3 , column=1, columnspan=3, pady=8, sticky="W")

        Y1_pointin.insert(0, "1")
        Y2_pointin.insert(0, "1")
        ###############################################################

        ############## tab 2 #########################################
        ttk.Label(tab2, text="X²", font=("Verdana", 9)).grid(row=0,column=1, padx=5, pady=5, sticky="S")
        ttk.Label(tab2, text="X", font=("Verdana", 9)).grid(row=0,column=2, padx=5, pady=5, sticky="S")
        ttk.Label(tab2, text="Const", font=("Verdana", 9)).grid(row=0,column=3, padx=5, pady=5, sticky="S")
        ttk.Label(tab2, text="Const", font=("Verdana", 9)).grid(row=2,column=2, padx=5, pady=5, sticky="S")
        ttk.Label(tab2, text="X", font=("Verdana", 9)).grid(row=2,column=1, padx=5, pady=5, sticky="S")
        ttk.Label(tab2, text="= Y", font=("Verdana", 9)).grid(row=1,column=4, padx=8, pady=5)
        ttk.Label(tab2, text="= Y", font=("Verdana", 9)).grid(row=3,column=3, padx=8, pady=5)
        X1_pointin2 = ttk.Entry(tab2, width="10")
        Y1_pointin2 = ttk.Entry(tab2, width="10")
        Z1_pointin2 = ttk.Entry(tab2, width="10")
        X2_pointin2 = ttk.Entry(tab2, width="10")
        Y2_pointin2 = ttk.Entry(tab2, width="10")
        solution2 = ttk.Label(tab2, text="")
        ttk.Separator(tab2, orient='vertical').grid(row=0, column=0, rowspan=5, padx=15)
        Draw2 = tk.BooleanVar()
        tick2 = tk.Checkbutton(tab2, text="Draw",onvalue=True, offvalue=False, variable=Draw2, command=lambda: check_box("tab2"))
        ttk.Button(tab2, text="Enter", command= lambda: button_command("tab2")).grid(row=7, column=4, pady=20)
        ttk.Button(tab2, text="Clear", command=lambda: clear("tab2")).grid(row=7, column=3)
        ttk.Button(tab2, text="Back", command=back).grid(row=7, column=1)
        tick2.grid(row=6 , column= 4)
  
        X1_pointin2.grid(row=1,column=1, padx=5, pady=5)
        Y1_pointin2.grid(row=1,column=2, padx=5, pady=5)
        Z1_pointin2.grid(row=1,column=3, padx=5, pady=5)
        X2_pointin2.grid(row=3,column=1, padx=5, pady=5)
        Y2_pointin2.grid(row=3,column=2, padx=5, pady=5)
        solution2.grid(row=4 , column=1, columnspan=4, pady=8, sticky="W")
        #################################################################
    
        ############## tab 3 ###########################################
        ttk.Label(tab3, text="X", font=("Verdana", 9)).grid(row=0,column=0, padx=5, pady=5, sticky="S")
        ttk.Label(tab3, text="Y", font=("Verdana", 9)).grid(row=0,column=1, padx=5, pady=5, sticky="S")
        ttk.Label(tab3, text="Z", font=("Verdana", 9)).grid(row=0,column=2, padx=5, pady=5, sticky="S")
        ttk.Label(tab3, text="=   Cont", font=("Verdana", 9)).grid(row=0,column=3, padx=5, pady=5, sticky="W")

        X1in = ttk.Entry(tab3, width="10")
        X2in = ttk.Entry(tab3, width="10")
        X3in = ttk.Entry(tab3, width="10")
        Y1in = ttk.Entry(tab3, width="10")
        Y2in = ttk.Entry(tab3, width="10")
        Y3in = ttk.Entry(tab3, width="10")
        Z1in = ttk.Entry(tab3, width="10")
        Z2in = ttk.Entry(tab3, width="10")
        Z3in = ttk.Entry(tab3, width="10")
        C1in = ttk.Entry(tab3, width="10")
        C2in = ttk.Entry(tab3, width="10")
        C3in = ttk.Entry(tab3, width="10")
        answer = ttk.Label(tab3, text="", font=("Verdana", 9))

        X1in.grid(row=1, column=0, pady=5, padx=5)
        X2in.grid(row=2, column=0, pady=5, padx=5)
        X3in.grid(row=3, column=0, pady=5, padx=5)
        Y1in.grid(row=1, column=1, pady=5, padx=5)
        Y2in.grid(row=2, column=1, pady=5, padx=5)
        Y3in.grid(row=3, column=1, pady=5, padx=5)
        Z1in.grid(row=1, column=2, pady=5, padx=5)
        Z2in.grid(row=2, column=2, pady=5, padx=5)
        Z3in.grid(row=3, column=2, pady=5, padx=5)
        C1in.grid(row=1, column=3, pady=5, padx=18, sticky="E")
        C2in.grid(row=2, column=3, pady=5, padx=18, sticky="E")
        C3in.grid(row=3, column=3, pady=5, padx=18, sticky="E")
        answer.grid(row=4, column=0, columnspan=4, pady=5, sticky="W")

        ttk.Button(tab3, text="Enter", command= lambda: button_command2()).grid(row=5, column=3, pady=20,padx=5)
        ttk.Button(tab3, text="Clear", command=lambda: clear("tab3")).grid(row=5, column=2,padx=5)
        ttk.Button(tab3, text="Back", command=back).grid(row=5, column=0, padx=5)
        ##################################################


class Scatter(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global x, y

        def check_box(self):
            if self.rline.get() == 0:
                self.rline.set(1)
            else:
                self.rline.set(0)

        def button_command(self):
            global x, y
            global limit
            xIn = X_pointin.get()
            yIn = Y_pointin.get()
            if len(x) > 50:
                x = []
                y = []
            try:
                if xIn == "":
                    xIn = 0
                if yIn == "":
                    yIn = 0
                if float(xIn) > limit or float(xIn) < -limit or float(yIn) > limit or float(yIn)<-limit:
                    raise
                x.append(float(xIn))
                y.append(float(yIn))
            except:
                popupmesg("!", "I can't take that")
                return
            X_pointin.delete(0, tk.END)
            Y_pointin.delete(0, tk.END)
            xtemp = ""
            ytemp = ""
            for z in range(0, len(x)):
                xtemp += str(x[z])+"\n"
                ytemp += str(y[z])+"\n"
            Xpoints.config(text="X Points\n"+str(xtemp))
            Ypoints.config(text="Y Points\n"+str(ytemp))

        def button3_command(self):
            global x, y
            if len(x) >= 2 or len(y) >= 2:
                draw.Scatter("x")
                Xpoints.config(text="")
                Ypoints.config(text="")
                if self.rline.get() == 1:
                    xytemp = []
                    for z in range(0, len(x)):
                        xytemp.append([x[z], y[z]])
                    graph_details.Rline()
                    draw.polynomial(draw, True)
                    popupmesg("Regression Line", "Points: "+"\n          ".join([str(item) for item in xytemp]) +"\n\n"+org_graph)
                x = []
                y = []
                controller.show_frame(PageTwo)
            else:
                popupmesg("!", "Need more points")

        def back_command(self):
            global x, y
            x = []
            y = []
            Xpoints.config(text="")
            Ypoints.config(text="")
            controller.show_frame(PageTwo)

        x = []
        y = []
        X_pointin = ttk.Entry(self, width="10")
        Y_pointin = ttk.Entry(self, width="10")
        Xlabel = ttk.Label(self, text="X         =", font=("Verdana", 9))
        Ylabel = ttk.Label(self, text="Y         =", font=("Verdana", 9))
        Xpoints = ttk.Label(self, text="", font=("Verdana", 9))
        Ypoints = ttk.Label(self, text="", font=("Verdana", 9))
        button1 = ttk.Button(self, text="Enter", command=lambda: button_command(self))
        button2 = ttk.Button(self, text="Back", command=lambda: back_command(self))
        button3 = ttk.Button(self, text="Finish", command= lambda: button3_command(self))
        self.rline = tk.IntVar()
        tick = tk.Checkbutton(self, text="Linear squares regreesion line\n(Line of best fit)", variable=self.rline, command=lambda: check_box(self))

        Xlabel.grid(row=0,column=0, padx=65, pady=5)
        Ylabel.grid(row=1,column=0, padx=65, pady=5)
        X_pointin.grid(row=0,column=1, padx=5, pady=5)
        Y_pointin.grid(row=1,column=1, padx=5, pady=5)
        button1.grid(row=2,column=1, pady=10)
        button2.grid(row=2,column=0, pady=10)
        button3.grid(row=4,column=1, pady=5)
        tick.grid(row=4,column=0, pady=5)
        Ypoints.grid(row=3,column=1, pady=5)
        Xpoints.grid(row=3,column=0, pady=5)

class BarChartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global x, y

        def check_box(self):
            if self.show_lbs.get() == False:
                self.show_lbs.set(True)
            else:
                self.show_lbs.set(False)

        def button_command(self):
            global x, y
            global limit
            yIn = Y_pointin.get()
            try:
                if yIn == "":
                    yIn = 0
                if float(yIn) > limit or float(yIn)<-limit:
                    raise
                if x:
                    x.append(x[-1]+18)
                else:
                    x.append(12)
                y.append(float(yIn))
            except:
                popupmesg("!", "I can't take that")
                return
            Y_pointin.delete(0, tk.END)
            ytemp = ""
            for z in range(0, len(y)):
                ytemp += str(y[z])+"\n"
            Ylabel.config(text=str(len(y)+1)+". Bar Height =")
            Ypoints.config(text="Bar Height\n"+str(ytemp))

        def button3_command(self):
            global x, y
            if draw.bar_graph(self.show_lbs.get(), XAxeslabelIn.get(), YAxeslabelIn.get()):
                Ypoints.config(text="")
                Ylabel.config(text="1. Bar height =")
                XAxeslabelIn.delete(0, tk.END)
                YAxeslabelIn.delete(0, tk.END)
                controller.show_frame(PageTwo)
            else:
                popupmesg("!", "Need more bars")

        def back_command(self):
            global x, y
            x = []
            y = []
            Ypoints.config(text="")
            Ylabel.config(text="1. Bar height =")
            XAxeslabelIn.delete(0, tk.END)
            YAxeslabelIn.delete(0, tk.END)
            Y_pointin.delete(0, tk.END)
            controller.show_frame(PageTwo)

        x = []
        y = []
        Y_pointin = ttk.Entry(self, width="10")
        Ylabel = ttk.Label(self, text="1. Bar height =", font=("Verdana", 9))
        Ypoints = ttk.Label(self, text="", font=("Verdana", 8))

        XAxeslabel = ttk.Label(self, text="X Axis Label = ", font=("Verdana", 9))
        opt = ttk.Label(self, text="(Optional)", font=("Verdana", 8))
        YAxeslabel = ttk.Label(self, text="Y Axis Label = ", font=("Verdana", 9))
        XAxeslabelIn = ttk.Entry(self, width="15")
        YAxeslabelIn = ttk.Entry(self, width="15")

        button1 = ttk.Button(self, text="Enter", command=lambda: button_command(self))
        self.show_lbs = tk.BooleanVar()
        tick = tk.Checkbutton(self, text="Add Bar Labels",onvalue=True, offvalue=False, variable=self.show_lbs, command=lambda: check_box(self))
        button2 = ttk.Button(self, text="Back", command=lambda: back_command(self))
        button3 = ttk.Button(self, text="Finish", command= lambda: button3_command(self))
        self.rline = tk.IntVar()

        Ylabel.grid(row=0,column=0, padx=60, pady=5)
        Y_pointin.grid(row=0,column=1, padx=5, pady=5)
        button1.grid(row=1,column=1, pady=10)
        button2.grid(row=1,column=0, padx=60, pady=10)
        Ypoints.grid(row=2,column=1, padx = 10, pady=10)
        XAxeslabel.grid(row=3,column=0, padx=60, pady=10)
        YAxeslabel.grid(row=5,column=0, padx=60, pady=10)
        XAxeslabelIn.grid(row=3,column=1, pady=1)
        opt.grid(row=4, column=1, pady=1)
        YAxeslabelIn.grid(row=5,column=1, pady=1)
        button3.grid(row=6,column=1, pady=15)
        tick.grid(row=6, column=0)


class ComplexPage2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Argand Diagram Controls", font=("Verdana", 12))
        label.pack(pady=10, padx=10)

        point_button = ttk.Button(self, text="Compelx number", command=lambda: controller.show_frame(complexPointPage))
        point_button.pack(pady=5)
        circle_button = ttk.Button(self, text="Circle", cursor="circle", command=lambda: controller.show_frame(ComplexCiclePage))
        circle_button.pack(pady=5)
        HalfLine_button= ttk.Button(self, text="Half Line", command=lambda: controller.show_frame(half_line_Page))      
        HalfLine_button.pack(pady=5)
        bisector_button= ttk.Button(self, text="Perpendicular Bisector", command=lambda: controller.show_frame(PbisectorPage))      
        bisector_button.pack(pady=5)
        MBset_button= ttk.Button(self, text="Mandelbrot Set", command=lambda: controller.show_frame(MBsetPage))      
        MBset_button.pack(pady=5)
        Home_button = ttk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))
        Home_button.pack(pady=25)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill="both", expand=True)
        canvas._tkcanvas.pack(side=tk.TOP, fill="both", expand=True)

class complexPointPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def check_box(self, which):
            if which == 1:
                if self.Details.get() == 0:
                    self.Details.set(1)
                else:
                    self.Details.set(0)
            elif which == 2: 
                if self.Vector.get() == 0:
                    self.Vector.set(1)
                else:
                    self.Vector.set(0)

        def button_command(self, X_pointin, Y_pointin):
            try:
                x = float(X_pointin.get())
                y = float(Y_pointin.get())
            except:
                popupmesg("!","Can't plot that")
            if self.Details.get() == 1:
                pi = math.pi
                modulus = math.sqrt((x**2) + (y**2))
                if str(x)[0] == "-" and str(y)[0] == "-":                    #finds which quadrant of 'argand diagram' the complex number is in
                    argument = -(pi-math.atan(abs(y)/abs(x)))
                elif str(x)[0] == "-" and str(y)[0] != "-":
                    argument = pi-math.atan(abs(y)/abs(x))
                elif str(x)[0] != "-" and str(y)[0] == "-":
                    argument = -math.atan(abs(y)/abs(x)) 
                elif str(x)[0] != "-" and str(y)[0]!= "-":
                    argument = math.atan(abs(y)/abs(x))
                else:
                    argument = None
                popupmesg("z = "+str(x)+" + "+str(y)+"i", "Modulus = "+str(modulus)+"\n\nArgument (Degrees) = "+str((argument/pi)*180)+"\nArgument (Radians) = "+str(argument)+"\n\nz = "+str(round(modulus, 1))+"(cos"+str(round(argument, 2))+" + isin"+str(round(argument, 2))+")")
            if draw.point(X_pointin.get(), Y_pointin.get()):
                if self.Vector.get() == 1:
                    x = [float(X_pointin.get()), 0]
                    y = [float(Y_pointin.get()), 0] 
                    s.plot(x, y, colours[colour_index-1],linestyle='dashed')
                    canvas.draw()
                X_pointin.delete(0, tk.END)
                Y_pointin.delete(0, tk.END)
                controller.show_frame(ComplexPage2)

        X_pointin = ttk.Entry(self, width="10")
        Y_pointin = ttk.Entry(self, width="10")
        Xlabel = ttk.Label(self, text="Real       =", font=("Verdana", 9))
        Ylabel = ttk.Label(self, text="Imaginary =", font=("Verdana", 9))
        self.Details = tk.IntVar()
        tick = tk.Checkbutton(self, text="Show details", variable=self.Details, command=lambda: check_box(self,1))
        self.Vector = tk.IntVar()
        tick2 = tk.Checkbutton(self, text="Draw vector", variable=self.Vector, command=lambda: check_box(self,2))
        button1 = ttk.Button(self, text="Enter", command=lambda: button_command(self, X_pointin, Y_pointin))
        button2 = ttk.Button(self, text="Back", command=lambda: controller.show_frame(ComplexPage2))

        Xlabel.grid(row=0,column=0, padx=65, pady=5)
        Ylabel.grid(row=1,column=0, padx=65, pady=5)
        X_pointin.grid(row=0,column=1, padx=5, pady=5)
        Y_pointin.grid(row=1,column=1, padx=5, pady=5)
        tick.grid(row=2, column=1, pady=12)
        tick2.grid(row=2, column=0, pady=12)
        button1.grid(row=3,column=1)
        button2.grid(row=3,column=0)

class ComplexCiclePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def button_command():
            Bool, r, a, b =  checkVars.circle(checkVars, rIn, aIn, bIn)
            if Bool == True:
                draw.circle(draw, r, -a, -b, "complex")
                controller.show_frame(ComplexPage2)

        label = ttk.Label(self, text="|z - (a + bi)| = r", font=("Verdana", 10))

        rIn = ttk.Entry(self, width="10")
        aIn = ttk.Entry(self, width="10")
        bIn = ttk.Entry(self, width="10")

        rlabel = ttk.Label(self, text="r      =", font=("Verdana", 9))
        alabel = ttk.Label(self, text="a      =", font=("Verdana", 9))
        blabel = ttk.Label(self, text="b      =", font=("Verdana", 9))
        button1 = ttk.Button(self, text="Enter", command=button_command)
        button2 = ttk.Button(self, text="Back", command=lambda: controller.show_frame(ComplexPage2))

        label.grid(row=0,column=0)
        rlabel.grid(row=1,column=0, padx=65, pady=0)
        alabel.grid(row=2,column=0, padx=65, pady=0)
        blabel.grid(row=3,column=0, padx=65, pady=0)
        rIn.grid(row=1,column=1, padx=5, pady=5)
        aIn.grid(row=2,column=1, padx=5, pady=5)
        bIn.grid(row=3,column=1, padx=5, pady=5)
        button1.grid(row=6,column=1, pady=10)
        button2.grid(row=6,column=0, pady=10)

class half_line_Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def check_box(self):
            if self.Unit.get() == 0:
                self.Unit.set(1)
            else:
                self.Unit.set(0)

        def button_command():
            global limit
            global x, y
            x = []
            y = []
            neg = False     #negative
            try:
                if aIn.get() == "":
                    a = 0
                if bIn.get() == "":
                    b = 0
                else:
                    a = float(aIn.get())
                    b = float(bIn.get())
                t = float(thetaIn.get())
                if a > limit or a < -limit or b > limit or b<-limit:
                    raise
                if self.Unit.get() == 0:     #degrees
                    tlablel = str(t)+"°"
                    t = (t/180) *math.pi
                else:
                    tlablel = str(t)+"rad"
                if t > (1.5*math.pi) or (t < 0 and t> -(math.pi*0.5)):
                    neg = True
                    t = -((2*math.pi) - t)
                elif t > math.pi or (t < 0 and t > -(math.pi)):
                    neg = True
                    t = t - math.pi
                elif t > (0.5*math.pi) or (t < 0 and t > -(0.5*math.pi)):
                    neg = False
                    t = -(math.pi - t)
                m = math.tan(t)     #gradient of line
                c = ((-m)*a) + b    #y intercept
                for X in range(-limit,limit):
                    Y = ((m)*(X)) + c
                    if neg == False and not(Y > limit) and  not(Y < -limit) and not(Y <= b):   
                        x.append(X)
                        y.append(Y)
                    elif neg == True and not(Y > limit) and  not(Y < -limit) and not(Y >= b):
                        x.append(X)
                        y.append(Y)
                graph_storage.append(s.plot([-limit, limit], [b,b], "black",linestyle="dashed"))
                graph_storage.append(s.plot(x, y, colours[colour_index],label= "arg(z-("+str(-a)+" + "+str(-b)+"i))="+tlablel))
                s.legend(bbox_to_anchor=(0,1.02,1,.102), loc=3, ncol=2, borderaxespad=0)
                canvas.draw()
                colour_change()
                aIn.delete(0, tk.END)
                bIn.delete(0, tk.END)
                thetaIn.delete(0, tk.END)
                controller.show_frame(ComplexPage2)
            except:
                popupmesg("!","I can't take that")

        label = ttk.Label(self, text="arg(z - (a + bi)) =  θ", font=("Verdana", 10))

        thetaIn = ttk.Entry(self, width="10")
        aIn = ttk.Entry(self, width="10")
        bIn = ttk.Entry(self, width="10")

        thetalabel = ttk.Label(self, text="θ      =", font=("Verdana", 9))
        alabel = ttk.Label(self, text="a      =", font=("Verdana", 9))
        blabel = ttk.Label(self, text="b      =", font=("Verdana", 9))
        button1 = ttk.Button(self, text="Enter", command=button_command)
        button2 = ttk.Button(self, text="Back", command=lambda: controller.show_frame(ComplexPage2))
        self.Unit = tk.IntVar()
        tick = tk.Checkbutton(self, text="Radians", variable=self.Unit, command=lambda: check_box(self))

        label.grid(row=0,column=0)
        thetalabel.grid(row=1,column=0, padx=65, pady=0)
        tick.grid(row=1, column = 3, padx= 10)
        alabel.grid(row=2,column=0, padx=65, pady=5)
        blabel.grid(row=3,column=0, padx=65, pady=5)
        thetaIn.grid(row=1,column=1, padx=5, pady=5)
        aIn.grid(row=2,column=1, padx=5, pady=5)
        bIn.grid(row=3,column=1, padx=5, pady=5)
        button1.grid(row=6,column=1, pady=10)
        button2.grid(row=6,column=0, pady=10)

class PbisectorPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def button_command(self):
            global colour_index
            global graph
            global org_graph
            try:
                if X_pointin.get() == "":
                    X_pointin.insert(0,"0")
                if Y_pointin.get() == "":
                    Y_pointin.insert(0,"0")
                if X2_pointin.get() == "":
                    X2_pointin.insert(0,"0")
                if Y2_pointin.get() == "":
                    Y2_pointin.insert(0,"0")
                X = float(X_pointin.get())
                Y = float(Y_pointin.get())
                X2 = float(X2_pointin.get())
                Y2 = float(Y2_pointin.get())
                if X>limit or X<-limit or Y>limit or Y<-limit or X2>limit or X2<-limit or Y2>limit or Y2<-limit:
                    raise
            except:
                popupmesg("!","Can't take that")
                return

            s.scatter([X,X2], [Y,Y2], s=28, marker="x",c=colours[colour_index])
            #colour_index -= 1

            m = (Y - Y2) / (X - X2)
            m = -((m)**-1)
            mdptx = (X+X2)/2
            mdpty = (Y+Y2)/2
            graph = "("+str(m)+"*((x)-"+str(mdptx)+"))+"+str(mdpty)
            org_graph = "y="+str(round(m,2))+"x + "+str(round((-mdptx*m)+mdpty,2))
            draw.polynomial(draw, False)
            colour_index -= 1
            graph_storage.append(s.plot([X,X2],[Y,Y2],colours[colour_index], linestyle="dashed"))
            canvas.draw()
            X_pointin.delete(0, tk.END)
            Y_pointin.delete(0, tk.END)
            X2_pointin.delete(0, tk.END)
            Y2_pointin.delete(0, tk.END)
            colour_change()
            controller.show_frame(ComplexPage2)


        label = ttk.Label(self, text="|z-(a+bi)| = |z-(b+ci)|", font=("Verdana", 9))
        X_pointin = ttk.Entry(self, width="10")
        Y_pointin = ttk.Entry(self, width="10")
        Xlabel = ttk.Label(self, text="a    =", font=("Verdana", 9))
        Ylabel = ttk.Label(self, text="b    =", font=("Verdana", 9))
        X2_pointin = ttk.Entry(self, width="10")
        Y2_pointin = ttk.Entry(self, width="10")
        X2label = ttk.Label(self, text="c   =", font=("Verdana", 9))
        Y2label = ttk.Label(self, text="d   =", font=("Verdana", 9))
        button1 = ttk.Button(self, text="Enter", command=lambda: button_command(self))
        button2 = ttk.Button(self, text="Back", command=lambda: controller.show_frame(ComplexPage2))

        label.grid(row=0,column=1, pady=10)
        Xlabel.grid(row=1,column=0, padx=65, pady=5)
        Ylabel.grid(row=2,column=0, padx=65, pady=5)
        X_pointin.grid(row=1,column=1, padx=5, pady=5)
        Y_pointin.grid(row=2,column=1, padx=5, pady=5)
        ttk.Separator(self, orient='vertical').grid(row=3, column=0, columnspan=1, pady=10)
        X2label.grid(row=4,column=0, padx=65, pady=5)
        Y2label.grid(row=5,column=0, padx=65, pady=5)
        X2_pointin.grid(row=4,column=1, padx=5, pady=5)
        Y2_pointin.grid(row=5,column=1, padx=5, pady=5)
        button1.grid(row=6,column=1, pady=25)
        button2.grid(row=6,column=0, pady=2)

class MBsetPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def check_box(self, which):
            if which == "axes":
                if self.axes.get() == 0:
                    self.axes.set(1)
                else:
                    self.axes.set(0)
            elif which == "red":
                if self.red.get() == 0:
                    self.red.set(1)
                else:
                    self.red.set(0)
            elif which == "blue":
                if self.blue.get() == 0:
                    self.blue.set(1)
                else:
                    self.blue.set(0)
        
        def slider_changed(self):
            current_value_label.configure(text=str(round(slider.get(),1)))

        def button_command(self):
            global x, y
            global limit
            if self.red.get() == 0 and self.blue.get() == 0:
                tick_red.flash()
                tick_blue.flash()
                tick_red.flash()
                tick_blue.flash()
                return
            if self.red.get() == 1 and self.blue.get() == 1:
                tick_red.flash()
                tick_blue.flash()
                tick_red.flash()
                tick_blue.flash()
                return

            if self.red.get() == 1:
                scheme = "red"
                colour = "maroon"
            elif self.blue.get() == 1:
                scheme = "blue"
                colour = "midnightblue"

            res = round(slider.get(),1)
            try:
                if res == "":
                    res = 0
                res = float(res)
                res = res/100
                clear_axis(True)
            except:
                popupmesg("!", "I can't take that")
                return

            MB_colours_red = [[80,"indigo"],[45,"darkblue"],[35,"blue"],[32,"dodgerblue"],[30,"steelblue"],[28,"cadetblue"],[25,"mediumaquamarine"],[15,"mediumseagreen"],[14,"seagreen"],[13,"darkgreen"],[12,"green"],[11,"forestgreen"],[10,"olivedrab"],[9,"olive"],[8,"darkkhaki"],[7,"khaki"],[6,"gold"],[5,"orange"],[4,"darkorange"],[3,"orangered"],[2,"red"],[1,"brown"],[0,"darkred"]  ]
            MB_colours_blue = [ [50,"aquamarine"],[40,"turquoise"],[30,"mediumturquoise"],[25,"darkturquoise"],[18,"deepskyblue"],[15,"dodgerblue"],[10,"cornflowerblue"],[7,"royalblue"],[4,"blue"],[3,"mediumblue"],[2,"darkblue"],[1,"navy"],[0,"midnightblue"] ]
            colour_before = ""
            y = -limit
            X = -limit - res
            Yprev = 0
            while X <= (limit - res):                                                                 #x loop starting at -400 each time
                progress['value'] = (((X+limit)/(2*limit))*100)
                self.update_idletasks()
                X += res
                Y = -limit
                while Y < limit:                                                                   #y loop starting at -400 each time
                    Y += res
                    ans = complex(0,0)                                                              #reset ans
                    for i in range(0,100):                                                          #The number of iterations - the more, the more accurate
                        ans = ( ans**2 + complex(X, Y) )                                      
                        if (ans.real**2) + (ans.imag**2) >= 4:                                      #checks weather stable or not. As anything that leaves a circle with radius 2 is unstable
                            stable = False
                            found_colour = False
                            if scheme == "red":
                                for z in range(0,len(MB_colours_red)):
                                    if MB_colours_red[z][0] < i:
                                        colour = MB_colours_red[z][1]
                                        found_colour = True
                                        break
                                if found_colour == False:
                                    colour ="maroon"
                            elif scheme == "blue":
                                for z in range(0,len(MB_colours_blue)):
                                    if MB_colours_blue[z][0] < i:
                                        colour = MB_colours_blue[z][1]
                                        break
                            break
                        else:
                            stable = True
                    if stable == True:
                        colour = "black"
                    if colour_before != colour:                                         #only draw new line when colour has changed
                        #print(colour_before)
                        s.plot([X-res, X],[Yprev-res,Y], colour_before, linewidth=100.1*res)
                        colour_before = colour
                        Yprev = Y
                    if Y >= limit:                                                                    #stops overlaping colours when y resets to -400
                        s.plot([X, X],[Yprev,limit], colour_before, linewidth=100.1*res)
                        Yprev = -limit

            canvas.draw()
            if self.axes.get() == 1:
                s.plot([-limit,limit],[0,0], "White", linestyle ="dashed")
                s.plot([0,0],[-limit,limit], "White",linestyle="dashed")
                canvas.draw()
            progress['value'] = 0 
            self.update_idletasks()
            slider.set(3)
            self.axis.set(0)
            self.red.set(0)
            self.blue.set(0)
            controller.show_frame(ComplexPage2)

        label = ttk.Label(self, text="Line Width:", font=("Verdana", 9))
        self.current_value = tk.IntVar()
        slider = ttk.Scale(self, from_=0.1, to=5,  orient='horizontal', variable=self.current_value, command=lambda x: slider_changed(self), value=3)
        current_value_label = ttk.Label(self, text='3')
        self.axes = tk.IntVar()
        self.red = tk.IntVar()
        self.blue = tk.IntVar()
        tick_red = tk.Checkbutton(self, text="Red", selectcolor="red", variable=self.red, command=lambda: check_box(self, "red"))
        tick_blue = tk.Checkbutton(self, text="Blue", selectcolor="royalblue", variable=self.blue, command=lambda: check_box(self, "blue"))
        tick = tk.Checkbutton(self, text="Draw Axes", variable=self.axes, command=lambda: check_box(self,"axes"))
        button1 = ttk.Button(self, text="Draw", command=lambda: button_command(self))
        button2 = ttk.Button(self, text="Back", command=lambda: controller.show_frame(ComplexPage2))
        progress = ttk.Progressbar(self, orient ='horizontal',length = 100, mode = 'determinate')

        label.grid(row=0, column=0, padx = 55, pady = 15)
        slider.grid(row=0, column=1, pady=8)
        current_value_label.grid(row=0, column=2, padx=10)
        tick_red.grid(row=1,column=0, pady=10)
        tick_blue.grid(row=1,column=1, pady=10)
        tick.grid(row=2,column=1, pady=10)
        button1.grid(row=3,column=1, pady=8)
        button2.grid(row=3,column=0, pady=8)
        progress.grid(row=4, column=1,pady=8)


class statsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def check_box(self, which):
            if which == 1:  
                if self.boxplot.get() == False:
                    self.boxplot.set(True)
                else:
                    self.boxplot.set(False)
            elif which == 2:
                if self.CF.get() == False:
                    self.CF.set(True)
                else:
                    self.CF.set(False)

        def  button_command(self, x_pointin, f_pointin):
            global x, y
            if self.counter > 20:
                popupmesg("!", "Too many numbers")
                x_pointin.delete(0, tk.END)
                f_pointin.delete(0, tk.END)
                return

            X = str(x_pointin.get())
            f = str(f_pointin.get())
            if not(X):
                X = 0
            if not(f):
                f = 1
            try:
                X = float(X)
                f = float(f)
                if X.is_integer():
                    X = int(X)
                if f.is_integer():
                    f = int(f)
                x.append(X)
                y.append(f)
                table.insert(parent="", index="end", iid=self.counter-1, text=str(self.counter),values=(X, f))
                self.counter += 1
                x_pointin.delete(0, tk.END)
                f_pointin.delete(0, tk.END)
                try:
                    x_pointin.insert(0,str(  int(x[-1] + abs(x[-1] - x[-2])))  )
                except:
                    x_pointin.insert(0,str(X + 1))
            except:
                popupmesg("!", "Can't take that")

        def finish():
            global x, y
            Zx = 0      #fx
            Zf = 0      #n
            Zx2 = 0     #fx²
            for z in range(0,len(x)):
            #sum of f
                Zf += y[z]
            #sum of x
                Zx += y[z]*(x[z])
            #sum of fx squared
                Zx2 += y[z]*(x[z])**2
            #mean
            mean = Zx / Zf
            #variance
            variance = (Zx2 / Zf) - (mean**2)
            #SD
            SD = variance**0.5
            #Q1 position
            Q1pos = (Zf)*0.25
            #median or Q2 posistion
            Q2pos = (Zf)*0.5
            #Q3 position
            Q3pos = (Zf)*0.75
            # Q1, Q2, Q3
            Q1 = ""
            Q2 = ""
            Q3 = ""
            CF = 0 #cumulative frequency
            for i in range (0,len(y)):
                CF += y[i]
                if not(Q1) and CF > Q1pos:
                    Q1 = x[i]
                if not(Q2) and CF > Q2pos:
                    Q2 = x[i]
                if not(Q3) and CF > Q3pos:
                    Q3 = x[i]
            #inter quartile range
            IQR = Q3 - Q2

            # σ Σ x̄ ²
            popupmesg("Stats", "x̄ = "+str(mean)+"\nΣx = "+str(Zx)+"\nΣx² = "+str(Zx2)+"\nσ² = "+str(variance)+"\nσ = "+str(SD)+"\nΣf (n) = "+str(Zf)+"\nQ1 = "+str(Q1)+"\nQ2 = "+str(Q2)+"\nQ3 = "+str(Q3)+"\nIQR = "+str(IQR))
            
            if self.boxplot.get() == True:
                all = []
                for i in range (0,len(x)):
                    for _ in range(0,int(y[i])):
                        all.append(x[i])

                s.boxplot(all, vert=False, whis=20, widths=1.9)
                canvas.draw()

                max = 0
                for i in range(0, len(all)):
                    if all[i] > max:
                        max = all[i]
                    s.set_ylim([0, 1.5])
                    s.set_xlim([0, max*0.05])
                

            if self.CF.get() == True:
                all = []
                sum = 0
                for i in range (0,len(y)):
                    sum += y[i]
                    all.append(sum)

                for i in range(0, len(all)):
                    if all[i] > limit:
                        limittemp = all[i]
                if limittemp == None:
                    s.set_ylim([0, limit])
                    s.set_xlim([0, limit])
                else:
                    s.set_ylim([0, limittemp*1.05])
                    s.set_xlim([0, limit])

                graph_storage.append( s.plot(x,all, marker=".") )
                canvas.draw()
            all = []

            clear(self, False)

        def undo(self):
            global x, y
            if x:
                table.delete(self.counter-2)
                del x[-1]
                del y[-1]
                x_pointin.delete(0, tk.END)
                if x:
                    x_pointin.insert(0,str(x[-1]+1))
                self.counter -= 1
        
        def clear(self, clr):
            global x, y
            x = []
            y = []
            self.CF.set(False)
            self.boxplot.set(False)
            tick.deselect()
            tick2.deselect()
            self.counter = 1
            x_pointin.delete(0, tk.END)
            f_pointin.delete(0, tk.END)
            if clr == True:
                for i in table.get_children():
                    table.delete(i)

        self.counter = 1
        table = ttk.Treeview(self)
        table["columns"] = ("x", "f")
        table.column("#0", width=60, minwidth=35,anchor=CENTER)
        table.column("x", anchor=CENTER, minwidth=40, width=70)
        table.column("f", anchor=CENTER, minwidth=40, width=90)

        table.heading("#0", text="Input", anchor=CENTER)
        table.heading("x", anchor=CENTER, text="x")
        table.heading("f", anchor=CENTER, text="f")

        xlabel = ttk.Label(self, text="x =").grid(row=0, column=0,pady=5)           #, padx = 20, sticky="E")
        x_pointin = ttk.Entry(self, width="10")
        x_pointin.grid(row=0, column=1,pady=5)
        flabel = ttk.Label(self, text="f =").grid(row=1, column=0,pady=5)
        f_pointin = ttk.Entry(self, width="10")
        f_pointin.grid(row=1, column=1,pady=5)
        button1 = ttk.Button(self, text="Enter", command=lambda:button_command(self, x_pointin,f_pointin)).grid(row=2, column=1,pady=8)
        button4 = ttk.Button(self, text="Undo last", command=lambda:undo(self)).grid(row=2, column=0)
        button6 = ttk.Button(self, text="Clear", command=lambda:clear(self, True)).grid(row=3, column=0)
        table.grid(row=4, column=0, columnspan=2,padx=65, pady=10)
        self.boxplot = tk.BooleanVar()
        tick = tk.Checkbutton(self, text="Draw Boxplot", variable=self.boxplot, command=lambda: check_box(self, 1))
        tick.grid(row=5, column=0)
        self.CF = tk.BooleanVar()
        tick2 = tk.Checkbutton(self, text="Cumulative frequency", variable=self.CF, command=lambda: check_box(self, 2))
        tick2.grid(row=5, column=1, columnspan=2)
        button2 = ttk.Button(self, text="Finish", command=finish).grid(row=6, column=1)
        button3 = ttk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage)).grid(row=6, column=0)


class calculator(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def check_box(self):
            if self.degrees.get() == False:
                self.degrees.set(True)
            else:
                self.degrees.set(False)

        def enter(sumIn):
            sum = sumIn.get()
            try:
                sum = sum.replace("x", "*")
                sum = sum.replace("^", "**")
                sum = sum.replace("g", "9.80665")
                sum = sum.replace("h", "6.62607004e-34")
                sum = sum.replace("e", "math.e")
                sum = sum.replace("pi", "math.pi")
                sum = sum.replace("log(", "math.log(")
            
                if self.ans:
                    sum = sum.replace("ans", self.ans)

                if self.degrees.get() == True:      #performs the calculation in degrees
                    self.SinAns = sum.find("sin(")      #have to convert angle to radians before calculation
                    self.CosAns = sum.find("cos(")
                    self.TanAns = sum.find("tan(")
                    if self.SinAns != -1:
                        calc = sctCalc(sum, self.SinAns+3, len(sum))
                        exec("self.SinAns = "+calc)
                        self.SinAns = np.deg2rad(float(self.SinAns))
                        sum = sum.replace(str(calc), "("+str(self.SinAns)+")")

                    if self.CosAns != -1:
                        calc = sctCalc(sum, self.CosAns+3, len(sum))
                        exec("self.CosAns = "+calc)
                        self.CosAns = np.deg2rad(float(self.CosAns))
                        sum = sum.replace(str(calc), "("+str(self.CosAns)+")")

                    if self.TanAns != -1:
                        calc = sctCalc(sum, self.TanAns+3, len(sum))
                        exec("self.TanAns = "+calc)
                        self.TanAns = np.deg2rad(float(self.TanAns))
                        sum = sum.replace(str(calc), "("+str(self.TanAns)+")")
                sum = sum.replace("sin(", "math.sin(")
                sum = sum.replace("cos(", "math.cos(")
                sum = sum.replace("tan(", "math.tan(")

                exec("self.ans = str("+sum+")")
                ansLable.config(text="Answer = "+self.ans)

            except:
                ansLable.config(text="Answer = Stupid")

        def sctCalc(sum, StartPos, length):
            calc = ""
            brkt = 0
            for i in range(StartPos, length):
                if sum[i] == "(":
                    brkt += 1
                if sum[i] == ")":
                    brkt -=1
                if brkt < 0:
                    break
                calc += sum[i]
            return calc

        def SD():
            if ansLable.cget("text").find(".") == -1:
                ansLable.config(text="Answer = "+self.ans)
            else:
                ansLable.config(text="Answer = "+str(Fraction(Decimal(self.ans))))

        def brackets():
            
            temp = sumIn.get()
            if not(temp):
                return

            temp = temp.replace("**", "^")
            temp = temp.replace("*", "x")
            if temp[0] != "(":
                temp = temp[:0] + "(" +temp[0:]
                n = len(temp)
                temp = temp[:n] + ")" +temp[n:]
            
            i = 0
            while i < len(sumIn.get()):

                pos1 = temp.find("+")
                if pos1 != -1 and temp[pos1-1] != ")":
                    temp = temp[:pos1] + ")" +temp[pos1:]
                    temp = temp[:pos1+2] + "(" +temp[pos1+2:]

                pos2 = temp.find("-")
                if pos2 != -1 and temp[pos2-1] != ")":
                    temp = temp[:pos2] + ")" +temp[pos2:]
                    temp = temp[:pos2+2] + "(" +temp[pos2+2:]

                pos3 = temp.find("x")
                if pos3 != -1 and temp[pos3-1] != ")":
                    temp = temp[:pos3] + ")" +temp[pos3:]
                    temp = temp[:pos3+2] + "(" +temp[pos3+2:]
                
                pos4 = temp.find("/")
                if pos4 != -1 and temp[pos4-1] != ")":
                    temp = temp[:pos4] + ")" +temp[pos4:]
                    temp = temp[:pos4+2] + "(" +temp[pos4+2:]

                i += 1

            sumIn.delete(0, tk.END)
            sumIn.insert(0, temp)

        def clear():
            sumIn.delete(0, tk.END)
            ansLable.config(text="Answer =          ")
            

        tabContorle = ttk.Notebook(self)
        tab1 = ttk.Frame(tabContorle)
        tab2 = ttk.Frame(tabContorle)
        tab3 = ttk.Frame(tabContorle)
        tabContorle.add(tab1, text="Calculator")
        tabContorle.add(tab2, text="Constants")
        tabContorle.add(tab3, text="Formulas")
        tabContorle.pack(expand=1, fill="both")

        frame = tk.LabelFrame(tab1, width=380)
        frame.grid(row=4, column=0, columnspan=10, padx=20, pady=10, sticky="W")

        self.ans = None
        self.SinAns = 0
        self.CosAns = 0
        self.TanAns = 0
        self.degrees = tk.BooleanVar()
        tick = tk.Checkbutton(tab1, text="Degrees", variable=self.degrees, onvalue=True, offvalue=False,  command=lambda: check_box(self))
        tick.grid(row=0, column=1)
        tick.select()
        self.degrees.set(True)
        ttk.Separator(tab1, orient='vertical').grid(row=1, column=0, columnspan=2, pady=20)
        sumIn = ttk.Entry(tab1, width="25", font=(12),)
        sumIn.grid(row=2, column=0, padx = 20, pady = 2)
        Lable1 = ttk.Label(tab1, text="(Don't forget brackets)", font=("Areial",7)).grid(row = 3, column=0, sticky="N")
        ansLable = ttk.Label(frame, text="Answer =          ", font=(11))
        ansLable.grid(row=0, column=0,pady=5, padx=5, columnspan=2, sticky="W") 
        ttk.Button(tab1, text="=", command=lambda: enter(sumIn)).grid(row=2, column=1, sticky="W")
        ttk.Button(tab1, text="AC", command= clear).grid(row=3, column=1, pady=15, sticky="W")
        ttk.Button(tab1, text="S ↔ D", command= SD).grid(row=5, column=1, sticky="W")
        ttk.Button(tab1, text="Backets", command=brackets).grid(row=6, column=1, sticky="W")
        ttk.Button(tab1, text="Back", command=lambda: controller.show_frame(StartPage)).grid(row=5, column=0, pady=35, padx=20, sticky="W")

        label2 = ttk.Label(tab2, font=(10), text="g = 9.80665 \npi = "+str(math.pi)+\
                                                "\ne = "+str(math.e)+" \nh = 6.62607004e-34\
                                                \nsin, cos and tan \nans (for previus answer)\
                                                \n\n(You can use these in the calculator) ").pack(padx=50, pady = 30)    

        image1 = Image.open("all equations.png")
        resize_image = image1.resize((340, 410))
        img= ImageTk.PhotoImage(master=tab3, image=resize_image)
        label1 = Label(tab3, image=img)
        label1.image = img
        label1.pack()
                

class SUVATPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def enter(self, S_pointin, U_pointin, V_pointin, A_pointin, T_pointin):
            s = S_pointin.get()
            u = U_pointin.get()
            v = V_pointin.get()
            a = A_pointin.get()
            t = T_pointin.get()
            try:
                s, u, v, a, t = SUVAT.calculate(s, u, v, a, t)
                clear()
                S_pointin.insert(0, str(s))
                U_pointin.insert(0, str(u))
                V_pointin.insert(0, str(v))
                A_pointin.insert(0, str(a))
                T_pointin.insert(0, str(t))
                #popupmesg("SUVAT", "S = "+str(s)+"\nU = "+str(u)+"\nV = "+str(v)+"\nA = "+str(a)+"\nT = "+str(t))
            except:
                popupmesg("!", "I can't take that")
        
        def clear():
            S_pointin.delete(0, tk.END)
            U_pointin.delete(0, tk.END)
            V_pointin.delete(0, tk.END)
            A_pointin.delete(0, tk.END)
            T_pointin.delete(0, tk.END)

        def back():
            clear()
            controller.show_frame(StartPage)

        Slabel = ttk.Label(self, text="S =").grid(row=0, column=0, padx=65, pady=10)
        Ulabel = ttk.Label(self, text="U =").grid(row=1, column=0,pady=10) 
        Vlabel = ttk.Label(self, text="V =").grid(row=2, column=0,pady=10) 
        Alabel = ttk.Label(self, text="A =").grid(row=3, column=0,pady=10) 
        Tlabel = ttk.Label(self, text="T =").grid(row=4, column=0,pady=10)
        S_pointin = ttk.Entry(self, width="15")
        U_pointin = ttk.Entry(self, width="15")
        V_pointin = ttk.Entry(self, width="15")
        A_pointin = ttk.Entry(self, width="15")
        T_pointin = ttk.Entry(self, width="15")
        S_pointin.grid(row=0, column=1,pady=10)
        U_pointin.grid(row=1, column=1,pady=10)
        V_pointin.grid(row=2, column=1,pady=10)
        A_pointin.grid(row=3, column=1,pady=10)
        T_pointin.grid(row=4, column=1,pady=10)

        button1 = ttk.Button(self, text="Clear", command=clear).grid(row=5, column=0, pady=20, padx=65)
        button2 = ttk.Button(self, text="Enter", command=lambda: enter(self, S_pointin, U_pointin, V_pointin, A_pointin, T_pointin)).grid(row=5, column=1, pady=20)
        button3 = ttk.Button(self, text="Back", command=back).grid(row=6, column=0)


class sortPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def sort_compere(self):
            global x, y
            try:
                if int(lengthIn.get()) > 3200 or float(lengthIn.get()) < 0:
                    raise
                items = make_list.Random(1, 1, int(lengthIn.get()), int(rangeIn.get()))
                m1, s1, p1 = sort.start(1, items, 2, 1)
                m2, s2, p2 = sort.start(2, items, 2, 1)
                m3, s3, p3 = sort.start(3, items, 2, 1)
                m4, s4, p4 = sort.start(4, items, 2, 1)
                x = [25, 75, 125, 175]
                clear_axis(False)
            except:
                popupmesg("!", "Can't take that")
                return
            if self.option_var.get() == "Passes":
                y = [p1, p2, p3, p4]
                draw.bar_graph(True, "Bubble, Insertion, Merge, Quick           ", "Passes")
            elif self.option_var.get() == "Time":
                y = [((m1*60)+s1)*10, ((m2*60)+s2*10), ((m3*60)+s3*10), ((m4*60)+s4)*10 ] 
                draw.bar_graph(True, "Bubble, Insertion, Merge, Quick", "Time (secs x10)")
            lengthIn.delete(0, tk.END)
            rangeIn.delete(0, tk.END)
            controller.show_frame(StartPage)
        
        lengthLbl = ttk.Label(self, text="Length of List =")
        lengthIn = ttk.Entry(self, width="10")
        rangeLbl = ttk.Label(self, text="Range =")
        rangeIn = ttk.Entry(self, width="10")

        measurelbl = ttk.Label(self, text="Measure: ")
        self.options = ("Passes", "Time")
        self.option_var = tk.StringVar()
        option_menu = ttk.OptionMenu(self, self.option_var, self.options[0],*self.options)

        button1 = ttk.Button(self, text="Compare", command=lambda: sort_compere(self))
        button2 = ttk.Button(self, text="Back", command=controller.show_frame(StartPage))

        lengthLbl.grid(row=0,column=0,padx = 60, pady=10)
        rangeLbl.grid(row=1,column=0, pady=10)
        rangeIn.grid(row=1,column=1, pady=10)
        lengthIn.grid(row=0,column=1, pady=10)
        measurelbl.grid(row=2, column=0)
        option_menu.grid(row=2, column=1, pady=10, padx=5)
        button1.grid(row=3,column=1, pady=20)
        button2.grid(row=3,column=0, pady=20)


class checkVars():
    def check_polynomial(self, graphIn):
        global graph
        global limit
        global org_graph
        graph = graphIn.get()
        org_graph = "y = " + graphIn.get()
        org_graph = org_graph.replace("pi", "π")
        
        index = 0
        while index < len(graph):
            if graph[index] == "x":
                graph = graph[:index] + "(" + graph[index:]
                graph = graph[:index+2] + ")" + graph[index+2:]
                index += 1
            index +=1

        i = 0
        while i < len(graph)-1:
            if graph[i].isdigit():
                if graph[i+1] == "(":
                    graph = graph[:i+1] + "*" + graph[i+1:]
            i += 1

        graph = graph.replace("^", "**")

        #adds 'spaces' inbertween parts
        for z in range(0,len(graph)):
            if graph[z] == "+" and graph[z-1] != " ":
                graph = graph[:z] + " " + graph[z:]

            if graph[z] == "-" and graph[z-1] != " ":
                if not(graph[z-1] == "*" and graph[z-2] == "*"):    #this is for negative powers
                    graph = graph[:z] + " " + graph[z:]

        graph = graph.replace("e", "math.e")
        graph = graph.replace("pi", "math.pi")
        graph = graph.replace("log(", "math.log(")
        graph = graph.replace("sin(", "math.sin(")
        graph = graph.replace("cos(", "math.cos(")
        graph = graph.replace("tan(", "math.tan(")

    def circle(self, rIn, cxIn, cyIn):
        global limit
        r = rIn.get()
        cx = cxIn.get()
        cy = cyIn.get()
        if r == "":
            r = 0
        if cx == "":
            cx = 0
        if cy == "":
            cy = 0
        try:
            r = float(r)
            cx = float(cx)
            cy = float(cy)
            if r > 0:
                if r <= limit:
                    rIn.delete(0, tk.END)
                    cxIn.delete(0, tk.END)
                    cyIn.delete(0, tk.END)
                    return True, r, cx,cy
                else:
                    popupmesg("!","Radius to big")
            popupmesg(" ! ","Radius must be \ngreater then 0")
            return False, None, None, None

        except:
            popupmesg(" ! ","Can't take that!")
            return False, None, None, None


class draw():
    def polynomial(self, dashed):
        global graph
        global limit
        global roots
        global org_graph
        global x_range
        global turning_points
        global x, y
        x = []
        y = []
        step = 0.01
        nx = -limit

        graph_copy = graph
        roots = []
        turning_points = []
        x_range = []
        while nx < limit:
            graph_copy = graph.replace("x", str(nx))
            try:
                ny = float(eval(graph_copy))
    
                if ny < limit and ny > -limit:
                    x.append(nx)
                    y.append(ny)
            except:
                pass
            nx += step
        if not(x) or not(y):
            return False
        x_range.append(x[0])
        x_range.append(x[-1])

        if dashed:
            graph_storage.append( s.plot(x,y, colours[colour_index], label=org_graph, linestyle='dashed') )
        else:
            graph_storage.append( s.plot(x,y, colours[colour_index], label=org_graph) )
        s.legend(bbox_to_anchor=(0,1.02,1,.102), loc=3, ncol=2, borderaxespad=0)
        canvas.draw()
        colour_change()
        return True

    def circle(self, r, cx, cy, type):
        global canvas
        global colour_index
        global limit
        global graph, org_graph
        global x_range
        global x, y
        graph = "((("+str(r)+")**2)-((x)**2)-(2*"+str(cx)+"*x)-(("+str(cx)+")**2))**0.5 -"+str(cy)
        x = []
        y = []
        real = False
        step = 0.005
        nx = -limit
        while nx < limit:
            try:
                ny = sqrt( ((r)**2) - ((nx)**2) - (2*cx*nx) - ((cx)**2) ) - cy
                real = True
            except:
                real = False
            if real == True and ny < limit and ny > -limit :
                x.append(nx)
                y.append(ny)
            nx += step

        x_range.append(x[0])
        x_range.append(x[-1])

        nx = limit
        while nx > -limit:
            try:
                ny = -(sqrt( ((r)**2) - ((nx)**2) - (2*cx*nx) - ((cx)**2) ) ) - cy
                real = True
            except:
                real = False
            if real == True and ny < limit and ny > -limit :
                x.append(nx)
                y.append(ny)
            nx -= step
        r = r**2
        if (r).is_integer():
            r = int(r)
        if cx.is_integer():
            cx = int(cx)
        if cy.is_integer():
            cy = int(cy)

        if type == "complex":
            lble = "|z - ("+str(cx)+"+"+str(cy)+") = "+str(r)
        else:    
            if cx ==0 and cy == 0:            
                lble = "x² + y² = "+str(r)
            elif cx !=0 or cy != 0:
                lble = "(x+"+str(cx)+")²+(y+"+str(cy)+")²="+str(r) 
        org_graph = lble
        s.scatter(-cx, -cy, s=15, marker="D")
        graph_storage.append((s.plot(x,y, colours[colour_index], label=lble)))
        s.legend(bbox_to_anchor=(0,1.02,1,.102), loc=3, ncol=2, borderaxespad=0)
        canvas.draw()
        colour_change()

    def point(X_pointin, Y_pointin):
        try:
            X_point = X_pointin
            Y_point = Y_pointin
            if X_point == "":
                X_point = 0
            if Y_point == "":
                Y_point = 0
            X_point = float(X_point)
            Y_point = float(Y_point)
            if X_point > limit or X_point < -limit or Y_point > limit or Y_point < -limit:
                raise                   #leave 'try' statement and enter 'except' statement
            if X_point.is_integer():
                X_point = int(X_point)
            if Y_point.is_integer():
                Y_point = int(Y_point)
            graph_storage.append(s.scatter(X_point, Y_point, c=colours[colour_index], s=30,label="("+str(X_point)+","+str(Y_point)+")"))
            s.legend(bbox_to_anchor=(0,1.02,1,.102), loc=3, ncol=2, borderaxespad=0)
            canvas.draw()
            colour_change()
            return True
        except:
           popupmesg(" ! ","Can't take that!")
           return False

    def Scatter(shape):
        global x, y
        s.scatter(x, y, s=35, marker=shape)
        canvas.draw()

    def wave(type, m):
        global limit
        global x, y
        x = []
        y = []
        X = -limit
        Y = 0
        step = 0.01
        if type == "Sine":                
            while X < limit:
                y.append(m*(math.sin((X)*(math.pi/180))))
                x.append(X)
                X += step

        elif type == "Cosine":
            while X < limit:
                y.append(m*(math.cos((X)*(math.pi/180))))
                x.append(X)
                X += step
        elif type == "Tangent":
            while X < limit:
                Y = m*(math.tan((X)*(math.pi/180)))
                if Y < limit and Y > -limit:
                    y.append(Y)
                    x.append(X)
                elif x and y:
                    s.plot(x,y,colours[colour_index])
                    x = []
                    y = []
                X += step
            if x and y:
                s.plot(x,y,colours[colour_index], label="Tangent")
                s.legend(bbox_to_anchor=(0,1.02,1,.102), loc=3, ncol=2, borderaxespad=0)
                canvas.draw()
            s.plot([90,90], [limit, -limit],"black",linestyle='dashed')
            s.plot([-90,-90],[limit, -limit],"black",linestyle='dashed')
            colour_change()
            canvas.draw()
            return
        else:
            return
        s.plot(x,y, colours[colour_index], label=type)
        s.legend(bbox_to_anchor=(0,1.02,1,.102), loc=3, ncol=2, borderaxespad=0)
        canvas.draw()
        colour_change()
        x = []
        y = []

    def bar_graph(showlbs, XAxeslabel, YAxeslabel):
        global x, y
        global colours, colour_index
        limittemp = None
        if y:
            #clear_axis(False)
            for i in range(0, len(y)):
                if y[i] > limit:
                    limittemp = y[i]
            if limittemp == None:
                s.set_ylim([0, limit])
                s.set_xlim([0, limit])
            else:
                s.set_ylim([0, limittemp*1.05])
                s.set_xlim([0, limit])
            s.set_xlabel(XAxeslabel)
            s.set_ylabel(YAxeslabel)
            s.bar(x,y,width=10,align="center",color=colours[colour_index])

            if showlbs == True:
                for i in range(len(x)): 
                    s.text(x = x[i], y = y[i]+1, s = round(y[i],1), size = 8, ha="center")
            canvas.draw()
            colour_change()
            x = []
            y = []
            return True
        else:
            return False


class graph_details():
    def details():
        global graph
        global graph_type
        a = ""
        b = ""
        c = ""
        d = ""
        abcd = []       #used to store a,b,c and d parts of function
        abcd = re.split("\s", graph)
        graph_type = ""
        for pos in range(0,len(abcd)):
            temp = abcd[pos].find("**")        #find out weather this part is square or not, e.g. 2x^2
            if temp == -1:
                if graph_type == "":
                    graph_type = "linear"
            else:
                temp2 = str(abcd[pos])[temp+2]     #position of power e.g. x**'3'
                if temp2 == "2" and str(abcd[pos])[temp-2] == "x":
                    if graph_type == "" or graph_type == "linear":
                        graph_type = "quadratic"
                elif temp2 == "3" and str(abcd[pos])[temp-2] == "x" :
                    if graph_type == "" or  graph_type == "quadratic" or graph_type == "linear":
                        graph_type = "cubic"
                else:
                    graph_type = "other"

        #print(abcd)
        #find individual values for a, b, c and d. right now they look like: 2*(x)**2
        #in the example we need to seperate the '2' out.
        for i in range(0, len(abcd)):
            temp1 = abcd[i].find("**")      #if linear or not?
            if temp1 == -1:                 #temp --> temporary variable
                temp = abcd[i].find("x")
                if temp == -1:              #can't find x
                    for j in range(0, len(abcd[i])):
                        d += abcd[i][j]
                    d = d.replace("+", "")

                else:                       #can find x
                    for j in range(0, len(abcd[i][:temp1-2])):
                        if abcd[i][j].isnumeric():
                            c += abcd[i][j]
                    if not(c):              #if no coefficeint, must be = 1
                        c = "1"
                    if abcd[i][0] == "-":   #add '-' sign if neccessary
                        c = c[:0] + "-" + c[0:]

            elif abcd[i][temp1+2] == "2" and abcd[i][temp1-2]== "x":   #if not linear
                for j in range(0, len(abcd[i][:temp1-3])):
                    if abcd[i][j].isnumeric():
                        b += abcd[i][j]
                if not(b):
                    b = "1"
                if abcd[i][0] == "-":
                    b = b[:0] + "-" + b[0:]

            elif abcd[i][temp1+2] == "3" and abcd[i][temp1-2]== "x":
                for j in range(0, len(abcd[i][:temp1-3])):
                    if abcd[i][j].isnumeric():
                        a += abcd[i][j]
                if not(a):
                    a = "1"
                if abcd[i][0] == "-":
                    a = a[:0] + "-" + a[0:]
        if not(a):                          #if no value = 0
            a = 0
        else:
            a = int(a)                      #if is value = integer, not string
        if not(b):
            b= 0
        else:
            b = int(b)
        if not(c):
            c = 0
        else:
            c = int(c)
        if not(d):
            d = 0
        else:
            d = int(d)
 
        #print("a =",a, " b =",b, " c =", c, " d =",d)
        #print(graph_type)

        if graph_type == "linear":
            graph_details.linear(c, d)
        elif graph_type == "quadratic":
            graph_details.quadratic(b,c,d)
        elif graph_type == "cubic":
            graph_details.cubic(a,b,c,d)
        else:
            graph_details.search_roots()
            graph_details.search_TP()

        return a, b, c, d, graph_type

    def search_roots():
        global graph
        global roots
        global x_range
        roots = []
        step = 0.001
        nx = x_range[0]
        ny_sgn1 = ""
        ny_sgn2 = ""

        while nx < x_range[1]:                          #was < limit
            graph_copy = graph.replace("x", str(nx))
            try:
                ny = float(eval(graph_copy))
                ny_sgn1 = str(ny)[0]
                if ny_sgn1 != "-":
                    ny_sgn1 = "+"
                if ny_sgn1 == "-" and ny_sgn2 == "+":
                    roots.append(round(nx,5))
                if ny_sgn1 == "+" and ny_sgn2 == "-":
                    roots.append(round(nx,5))
                ny_sgn2 = ny_sgn1
            except:
                pass
            nx += step

    def search_TP():
        global graph
        global turning_points
        global x_range
        turning_points = []
        step = 0.001
        nx = x_range[0]
        ny_1 = 0
        ny_2 = 0
        ny_3 = 0

        while nx < x_range[1]:                          #was < limit
            try:
                graph_copy = graph.replace("x", str(nx))
                ny_1 = float(eval(graph_copy))

                graph_copy = graph.replace("x", str(nx+step))
                ny_2 = float(eval(graph_copy))

                graph_copy = graph.replace("x", str(nx+step+step))
                ny_3 = float(eval(graph_copy))

                if ny_2 > ny_1:
                    if ny_3 < ny_2:
                        turning_points.append([round(nx,5),round(((ny_2+ny_3)/2),5)])
                if ny_2 < ny_1:
                    if ny_3 > ny_2:
                        turning_points.append([round(nx,5),round(((ny_2+ny_3)/2),5)])
            except:
                pass
            nx += step

    def linear(m,c):
        global graph
        global roots
        roots = []
        turning_points = []

        if c != 0:
            roots.append(-c/m)
        else:
            roots.append(0)

    def quadratic(a,b,c):
        global roots
        global turning_points
        roots = []
        turning_points = []

        TPx = -b/(2*a)
        TPy = (a*((TPx)**2))+(b*(TPx))+c  
        turning_points.append([TPx, TPy])
        if ((b**2) - (4*a*c)) >= 0:    
            roots.append((-b+(math.sqrt((b**2)-(4*(a*c))))) / (2*a))                            #quadratic formula
            roots.append((-b-(math.sqrt((b**2)-(4*(a*c))))) / (2*a))
        else:
            roots.append(0)
            roots.append(0)

    def cubic(a, b, c, d):
        global roots
        global turning_points
        roots = []
        turning_points = []
        pi = math.pi

        b2, c2, d2 = graph_details.dy_by_dx(a, b, c, d)
        if (c2**2) - (4*b2*d2) >= 0:          #determinant of dy/dx (checks if there's a turning point)
            TPx1 = ((-2*b)+math.sqrt((4*(b**2))-(12*(a*c))))/(6*a)
            TPx2 = ((-2*b)-math.sqrt((4*(b**2))-(12*(a*c))))/(6*a)                              #finds turning points
            TPy1 = a*((TPx1)**3) + b*((TPx1)**2) + (c*(TPx1)) + d
            TPy2 = a*((TPx2)**3) + b*((TPx2)**2) + (c*(TPx2)) + d
            turning_points.append([TPx1, TPy1])
            turning_points.append([TPx2, TPy2])
        else:
            graph_details.search_TP()

        def cube_root(x):                                                                               #had to do this because of this version of python
            if 0<=x: return x**(1./3.)
            return -(-x)**(1./3.)

        if b == 0 and d != 0:
            part1 = ((b**3)/(27*(a**3))) 
            part2 = ((b*c) / (6*(a**2)))
            part3 =  (d / (2*a))
            part4 = (c/(3*a))
            part5 = ((b**2)/(9*(a**2)))
            mainP1 = (-part1 + part2 - part3)
            mainP2 = (part4 - part5)**3
            a = mainP1
            b = (abs(mainP1**2 + mainP2))**(1/2)
            r = ( a**2 + b**2 )**(1/2)
            if a < 0:
                theta1 = pi - (math.atan((b)/(a)) / 3)    
            else:
                theta1 = math.atan((b)/(a)) / 3
            if theta1 > (5*pi)/6:                                                               #bottom right
                theta2 = 2*pi - (theta1 + ((2/3)*math.pi)) 
            elif theta1 < pi/3:                                                                 #top left       
                theta2 = pi - (theta1 + ((2/3)*math.pi))
            elif theta1 < (5*pi)/6 and theta1 > pi/3:                                           #bottom left
                theta2 = -( (2*pi) - (theta1 + ((2/3)*math.pi)) )                
            theta3 = (theta1 - ((2/3)*math.pi))
            z1 = ((r**(1/3))*(math.cos(theta1))) + ((r**(1/3))*(math.cos(theta1)))
            x1 = z1
            if a*-a == a:                                                                       #negative
                z2 = ((r**(1/3))*(math.cos(theta2))) + ((r**(1/3))*(math.cos(theta2)))
            else:                                                                               #positive
                z2 = -(((r**(1/3))*(math.cos(theta2))) + ((r**(1/3))*(math.cos(theta2))))
            x2 = z2
            z3 = ((r**(1/3))*(math.cos(theta3))) + ((r**(1/3))*(math.cos(theta3)))
            x3 = z3
            roots.append(x1)
            roots.append(x2)
            roots.append(x3)

        else:
            graph_details.search_roots()

    def dy_by_dx(a, b, c, d):
        return (3*a), (2*b), c

    def Rline():
        global x
        global y
        global graph
        global org_graph
        step = 1    #cannot change this
        Xpoints = []
        Ypoints = []
        index = 1
        X = 0
        Y = 0
        Sxy = 0
        Sxx = 0
        Xpoints = x
        Ypoints = y
        for z in range(0,len(Xpoints)):
            X += Xpoints[z]                                   #sums
            Y += Ypoints[z]
        X = X / len(Xpoints)                                  #avgs
        Y = Y / len(Ypoints)
        for p in range(0,len(Xpoints)):
            Sxy += (Xpoints[p]-X)*(Ypoints[p]-Y)
            Sxx += (Xpoints[p]-X)**2
        c = round((Sxy / Sxx),4)
        d = round((Y-(c*X)),4)
        if str(c)[0] == "-":
            org_graph = "y = "+str(d)+str(c)+"x"
        else:
            org_graph = "y = "+str(d)+" + "+str(c)+"x"
        graph = str(c)+"*(x) +"+str(d)


app = main()
app.geometry("360x440+825+1")
app.mainloop()
