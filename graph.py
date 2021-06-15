from logging import INFO
import re
import math
import matplotlib
import sys
import os
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import style
from matplotlib import pyplot as plt

import tkinter as tk
from tkinter import Label, ttk

from math import sqrt as sqrt

style.use("ggplot")
f = Figure(figsize=(6,6), dpi=100) 
#f = Figure() 
s = f.add_subplot(111)
canvas = FigureCanvasTkAgg(f)
#s.set_title("Cartesian coordinate system")
limit = 200
s.plot([-limit,limit],[0,0], "black")
s.plot([0,0],[-limit,limit], "black")
canvas.draw()

#a, b, c, d = "", "", "", ""
graph = ""
org_graph = ""
graph_type = ""
roots = []
turning_points = []
colours = ["red","orange","yellow","green","blue","pink"]
colour_index = 0
x = []
y = []
x_range = []

def colour_change():
    global colour_index
    if colour_index < len(colours)-1:
        colour_index +=1
    else:
        colour_index = 0

def popupmesg(title, msg):
    popup = tk.Tk()
    popup.wm_title(title)
    label = ttk.Label(popup, text=msg, font=("Verdana", 10))
    label.pack(side="top", fill="x", padx=20, pady=10)
    B1 = ttk.Button(popup, text="okay", command= popup.destroy)
    B1.pack(pady=10)
    return
    #popup.mainloop()

def clear_axis():
    global colour_index
    global limit
    colour_index = 0
    s.clear()
    s.plot([-limit,limit],[0,0], "black")
    s.plot([0,0],[-limit,limit], "black")
    canvas.draw()

class main(tk.Tk):                                                          #inhertit from tk
    
    def __init__(self, *args, **kwargs):                                    #initailisation, arguments, key word arguments (variables / disctionaries)
        tk.Tk.__init__(self,*args,**kwargs)

        tk.Tk.iconbitmap(self, default="p icon.ico")
        tk.Tk.wm_title(self, "Peter's graph")

        container = tk.Frame(self)                                          #edge of window
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Clear graph", command= clear_axis)
        filemenu.add_separator()
        filemenu.add_command(label="Restart", command=lambda: os.execl(sys.executable, sys.executable, *sys.argv))
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="Controls", menu=filemenu)

        tk.Tk.config(self, menu=menubar)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, GraphPage, circlePage, PointPage, wavePage, Scatter, ComplexPage2, complexPointPage, ComplexCiclePage, half_line_Page, MBsetPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")                      #north, south, east, west

        self.show_frame(StartPage)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def Real():
            clear_axis()
            controller.show_frame(PageTwo)
        def Complex():
            clear_axis()
            controller.show_frame(ComplexPage2)

        label = ttk.Label(self, text="Home", font=("Verdana", 12))
        label.pack(pady=10, padx=10)
        button2 = ttk.Button(self, text="Cartesian Grid", command=Real)                 #lambda allows you to pass things into function
        button2.pack(pady=10)
        button3 = ttk.Button(self, text="Argand Digaram", command=Complex)                 #lambda allows you to pass things into function
        button3.pack(pady=10)
        button1 = ttk.Button(self, text="Help", command=lambda: controller.show_frame(PageOne))                 #lambda allows you to pass things into function
        button1.pack(pady=20)


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Help Page", font=("Verdana", 12))
        label.pack(padx = 10, pady=10)
        label2 = ttk.Label(self, text="This page is where you can find help \n Good Luck!", font=("Verdana", 8))
        label2.pack(padx = 10, pady=20)
        button1 = ttk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))                #lambda allows you to pass things into function
        button1.pack(pady = 30)

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        clear_axis()
        label = ttk.Label(self, text="Graph Controls", font=("Verdana", 12))
        label.pack(pady=10, padx=10)
        
        point_button = ttk.Button(self, text="Point", command=lambda: controller.show_frame(PointPage))
        point_button.pack(pady=5)
        circle_button = ttk.Button(self, text="Circle", cursor="circle", command=lambda: controller.show_frame(circlePage))
        circle_button.pack(pady=5)
        Polynomial_button= ttk.Button(self, text="Polynomial", command=lambda: controller.show_frame(GraphPage))                #lambda allows you to pass things into function
        Polynomial_button.pack(pady=5)
        wave_button = ttk.Button(self, text="Wave", command=lambda: controller.show_frame(wavePage))                #lambda allows you to pass things into function
        wave_button.pack(pady=5)
        Rline_button = ttk.Button(self, text="Scatter graph", command=lambda: controller.show_frame(Scatter))
        Rline_button.pack(pady=5)
        Home_button = ttk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))                #lambda allows you to pass things into function
        Home_button.pack(pady=25)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill="both", expand=True)
        canvas._tkcanvas.pack(side=tk.TOP, fill="both", expand=True)


class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        global canvas
        global graph #a, b, c, d 

        def check_box(self):
            if self.Details.get() == 0:
                self.Details.set(1)
            else:
                self.Details.set(0)
            #print(self.Details.get())
        
        def button1_command(self):
            global roots
            global graph
            global org_graph
            global turning_points
            global x, y
            checkVars.check_polynomial(checkVars, graphIn) #aIn, bIn, cIn, dIn)
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
        #aIn = ttk.Entry(self, width="20")
        #bIn = ttk.Entry(self, width="20")
        #cIn = ttk.Entry(self, width="20")
        #dIn = ttk.Entry(self, width="20")
        graphLabel = ttk.Label(self, text="f(x)       =", font=("Verdana", 10))
        #aLabel = ttk.Label(self, text="a = ", font=("Verdana", 8))
        #bLabel = ttk.Label(self, text="b = ", font=("Verdana", 8))
        #cLabel = ttk.Label(self, text="c = ", font=("Verdana", 8))
        #dLabel = ttk.Label(self, text="d = ", font=("Verdana", 8))
        self.Details = tk.IntVar()
        tick = tk.Checkbutton(self, text="Show details", variable=self.Details, onvalue=True, command=lambda: check_box(self))
        button1 = ttk.Button(self, text="Enter", command=lambda: button1_command(self))
        button2 = ttk.Button(self, text="Back", command=lambda: controller.show_frame(PageTwo))
        
        graphLabel.grid(row=0,column=0, pady=25)
        #aLabel.grid(row=2,column=0)
        #bLabel.grid(row=3,column=0)
        #cLabel.grid(row=4,column=0)
        #dLabel.grid(row=5,column=0)
        graphIn.grid(row=0,column=1, pady=25)
        #aIn.grid(row=2,column=1, pady=5)
        #bIn.grid(row=3,column=1, pady=5)
        #cIn.grid(row=4,column=1, pady=5)
        #dIn.grid(row=5,column=1, pady=5)
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

        #label = ttk.Label(self, text="Circle", font=("Verdana", 10))

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
                draw.Scatter()
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


class ComplexPage2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        clear_axis()
        label = ttk.Label(self, text="Argand Diagram Controls", font=("Verdana", 12))
        label.pack(pady=10, padx=10)

        point_button = ttk.Button(self, text="Compelx number", command=lambda: controller.show_frame(complexPointPage))
        point_button.pack(pady=5)
        circle_button = ttk.Button(self, text="Circle", cursor="circle", command=lambda: controller.show_frame(ComplexCiclePage))
        circle_button.pack(pady=5)
        HalfLine_button= ttk.Button(self, text="Half Line", command=lambda: controller.show_frame(half_line_Page))      
        HalfLine_button.pack(pady=5)
        bisector_button= ttk.Button(self, text="Perpendicular Bisector", command=lambda: controller.show_frame(ComplexPage2))      
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
                print("Bad")
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
                s.plot([-limit, limit], [b,b], "black",linestyle="dashed")
                s.plot(x, y, colours[colour_index],label= "arg(z-("+str(-a)+" + "+str(-b)+"i))="+tlablel)
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


class MBsetPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def check_box(self):
            if self.axes.get() == 0:
                self.axes.set(1)
            else:
                self.axes.set(0)
        
        def slider_changed(self):
            current_value_label.configure(text=str(round(slider.get(),1)))

        def button_command(self):
            global x, y
            global limit
            res = round(slider.get(),1)
            try:
                if res == "":
                    res = 0
                res = float(res)
                s.clear()
            except:
                popupmesg("!", "I can't take that")
                return

            MB_colours = [[0,"darkred"],[1,"firebrick"],[2,"red"],[3,"orangered"],[4,"darkorange"],[5,"orange"],[6,"gold"],[7,"khaki"],[8,"darkkhaki"],[9,"olive"],[10,"olivedrab"],[11,"forestgreen"],[12,"green"],[13,"darkgreen"],[14,"seagreen"],[15,"mediumseagreen"],[28,"cadetblue"],[30,"steelblue"],[32,"dodgerblue"],[35,"blue"],[45,"darkblue"],[80,"darkslateblue"]]
            colour = "maroon"
            colour_before = ""
            y = 0
            X = -limit - res
            Yprev = 0
            while X <= (limit - res):                                                                 #x loop starting at -400 each time
                progress['value'] = (((X+200)/400)*100)
                self.update_idletasks()
                X += res
                Y = -limit
                while Y < limit:                                                                   #y loop starting at -400 each time
                    Y += res
                    Xscale = X / 100                                                                # /200 for scale- should be between -2 &2  , not -400 & 400
                    Yscale = Y / 100
                    ans = complex(0,0)                                                              #reset ans
                    for i in range(0,100):                                                          #The number of iterations - the more, the more accurate
                        ans = ( ans**2 + complex(Xscale, Yscale) )                                      
                        if (ans.real**2) + (ans.imag**2) >= 4:                                      #checks weather stable or not. As anything that leaves a circle with radius 2 is unstable
                            stable = False
                            found_colour = False
                            for z in range(0,len(MB_colours)):
                                if MB_colours[len(MB_colours)-1-z][0] < i:
                                    colour = MB_colours[len(MB_colours)-1-z][1]
                                    found_colour = True
                                    break
                            if found_colour == False:
                                colour ="maroon"
                            break
                        else:
                            stable = True
                    if stable == True:
                        colour = "black"
                    if colour_before != colour:                                         #only draw new line when colour has changed
                        s.plot([X-res, X],[Yprev-res,Y], colour_before, linewidth=1.1*res)
                        colour_before = colour
                        Yprev = Y
                    if Y >= limit:                                                                    #stops overlaping colours when y resets to -400
                        s.plot([X, X],[Yprev,limit], colour_before, linewidth=1.1*res)
                        Yprev = -limit

            canvas.draw()
            if self.axes.get() == 1:
                s.plot([-limit,limit],[0,0], "White", linestyle ="dashed")
                s.plot([0,0],[-limit,limit], "White",linestyle="dashed")
                canvas.draw()
            progress['value'] = 0 
            self.update_idletasks()
            slider.set(3)
            controller.show_frame(ComplexPage2)

        label = ttk.Label(self, text="Resolution:", font=("Verdana", 9))
        self.current_value = tk.IntVar()
        slider = ttk.Scale(self, from_=0.1, to=5,  orient='horizontal', variable=self.current_value, command=lambda x: slider_changed(self), value=3)
        current_value_label = ttk.Label(self, text='3')
        self.axes = tk.IntVar()
        tick = tk.Checkbutton(self, text="Draw Axes", variable=self.axes, command=lambda: check_box(self))
        button1 = ttk.Button(self, text="Draw", command=lambda: button_command(self))
        button2 = ttk.Button(self, text="Back", command=lambda: controller.show_frame(ComplexPage2))
        progress = ttk.Progressbar(self, orient ='horizontal',length = 100, mode = 'determinate')

        label.grid(row=0, column=0, padx = 55, pady = 15)
        slider.grid(row=0, column=1, pady=8)
        current_value_label.grid(row=0, column=2, padx=10)
        tick.grid(row=1,column=1, pady=10)
        button1.grid(row=2,column=1, pady=8)
        button2.grid(row=2,column=0, pady=8)
        progress.grid(row=3, column=1,pady=8)


class checkVars():
    def check_polynomial(self, graphIn): #aIn, bIn, cIn, dIn):
        global graph #a, b, c, d 
        global limit
        global org_graph
        graph = graphIn.get()
        org_graph = "y = " + graphIn.get()
        #a = aIn.get()
        #b = bIn.get()
        #c = cIn.get()
        #d = dIn.get()
        #if a == "":
        #    a = 0
        #if b == "":
        #    b = 0
        #if c == "":
        #    c = 0
        #if d == "":
        #    d = 0
        #aIn.delete(0, tk.END)
        #bIn.delete(0, tk.END)
        #cIn.delete(0, tk.END)
        #dIn.delete(0, tk.END)
        
        index = 0
        #for _ in range (0, len(graph)):
        while index < len(graph):
            if graph[index] == "x":
                graph = graph[:index] + "(" + graph[index:]
                graph = graph[:index+2] + ")" + graph[index+2:]
                index += 1
            index +=1

        #for i in range (0, len(graph)-1):
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
        #try:
         #   a = float(a)
          #  b = float(b)
           # c = float(c)
            #d = float(d)
        #return True
        #except:
        #    popupmesg("Can't accpet that!")
        #    return False 

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
        global graph #a,b,c,d
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
            #ny = (a*(nx**3))+(b*(nx**2))+(c*nx)+d
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
        #if a.is_integer():
            #a = int(a)
        #if b.is_integer():
         #   b = int(b)
       # if c.is_integer():
        #    c = int(c)
        #if d.is_integer():
         #   d = int(d)
        
        #if a == 0 and b ==0 and c ==0:
        #    lble1 = "y = "+str(d)
        #elif a==0 and b ==0:
        #    lble1 = "y="+str(c)+"x+"+str(d)
        #elif a == 0:
        #    lble1 = "y="+str(b)+"x^2+"+str(c)+"x+"+str(d)
        #else:
        #    lble1 = "y="+str(a)+"x^3+"+str(b)+"x^2+"+str(c)+"x+"+str(d)
        if dashed:
            s.plot(x,y, colours[colour_index], label=org_graph, linestyle='dashed')
        else:
            s.plot(x,y, colours[colour_index], label=org_graph)
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
                lble = "x^2 + y^2 = "+str(r)
            elif cx !=0 or cy != 0:
                lble = "(x+"+str(cx)+")^2+(y+"+str(cy)+")^2="+str(r) 
        org_graph = lble

        s.plot(x,y, colours[colour_index], label=lble)
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
            if X_point > 200 or X_point < -200 or Y_point > 200 or Y_point < -200:
                raise                   #leave 'try' statement and enter 'except' statement
            if X_point.is_integer():
                X_point = int(X_point)
            if Y_point.is_integer():
                Y_point = int(Y_point)
            s.scatter(X_point, Y_point, c=colours[colour_index], s=30,label="("+str(X_point)+","+str(Y_point)+")")
            s.legend(bbox_to_anchor=(0,1.02,1,.102), loc=3, ncol=2, borderaxespad=0)
            canvas.draw()
            colour_change()
            return True
        except:
           popupmesg(" ! ","Can't take that!")
           return False

    def Scatter():
        global x, y
        s.scatter(x, y, s=35, marker="P")
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
                if temp2 == "2":
                    if graph_type == "" or graph_type == "linear":
                        graph_type = "quadratic"
                elif temp2 == "3":
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

            elif abcd[i][temp1+2] == "2":   #if not linear
                for j in range(0, len(abcd[i][:temp1-3])):
                    if abcd[i][j].isnumeric():
                        b += abcd[i][j]
                if not(b):
                    b = "1"
                if abcd[i][0] == "-":
                    b = b[:0] + "-" + b[0:]

            elif abcd[i][temp1+2] == "3":
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
        c = round((Sxy / Sxx),5)
        d = round((Y-(c*X)),5)
        if str(c)[0] == "-":
            org_graph = "y = "+str(d)+str(c)+"x"
        else:
            org_graph = "y = "+str(d)+" + "+str(c)+"x"
        graph = str(c)+"*(x) +"+str(d)

app = main()
app.geometry("360x440+825+1")
app.mainloop()
