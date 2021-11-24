import turtle
import math
import time
from timer import timer as s
from find_roots import Roots

turtle.Screen().setup(840,840,-100,50)                                                          #make scrren the right size (allowing for header and things)
turtle.Screen().title("Peter's graph!")
colour = ['red','orange','light blue','blue','light green','green','pink','purple']             #these are the graph colours
colour_index = 0
MSredScale = [[80,"BlueViolet"],[45,"dark blue"],[35,"blue"],[32,"blue4"],[30,"blue3"],[28,"blue2"],[25,"blue1"],[15,"green4"],[14,"green3"],[13,"green2"],[12,"green1"],[11,"GreenYellow"],[10,"yellow3"],[9,"yellow2"],[8,"yellow"],[7,"yellow1"],[6,"orange1"],[5,"orange"],[4,"dark orange"],[3,"OrangeRed1"],[2,"OrangeRed2"],[1,"red1"],[0,"red2"],[-1,"red3"]]
MSblueScale = [[50,"light sky blue"],[40,"sky blue"],[30,"powder blue"],[25,"light steel blue"],[18,"cornflower blue"],[15,"steel blue"],[10,"royal blue"],[7,"blue1"],[6,"blue2"],[5,"blue"],[4,"medium blue"],[3,"blue3"],[2,"blue4"],[1,"dark blue"],[0,"navy"],[-1,"midnight blue"]]
x = 0                                                                                           #these store the points drawn (so i can 'undo')
y = 0
Status = ""                                                                                     #this is my command input
a = 0
b = 0
c = 0
d = 0
a2 = 0
b2 = 0
c2 = 0
d2 = 0
c3 = 0
d3 = 0
Nroots = 0                                                                                      #this is how many roots there are to find
roots = [0.0, 0.0, 0.0]                                                                         #these are the found roots
tim = turtle.Turtle()                                                                           #my 2 turtles :)
tom = turtle.Turtle()
tum = turtle.Turtle("turtle")
tom.shape("turtle")
tim.shape("turtle")
pen_status = "down"
hide_status = "hidden"
Axis = 400                                                                                      #size of axis grid to (0,0)
scale = Axis / 20
linear = False
quadratic = False                                                                               #type of graph
cubic = False
pi = math.pi
mandelbrotSet = False

def draw_axis():                                                                                #draws grid
    global colour_index
    global scale
    if mandelbrotSet == False:
        tom.reset()                                                                             #reset / clear
        tim.reset()
        tum.reset()
        tim.width(4)
        tom.width(4)
    else:
        tim.color("white")
        tom.color("white")
        tim.width(3)
        tom.width(3)
    tom.shape("turtle")
    tim.shape("turtle")
    tim.speed(-1)                                                                               #max speed
    tom.speed(-1)
    tom.hideturtle()        
    tim.hideturtle()
    tum.hideturtle()
    tim.penup()
    tom.penup()
    tim.setpos(0,Axis)
    tom.setpos(-Axis,0)
    tom.pendown()                                                                               #draws axis
    tim.pendown()
    for _ in range(0,int((Axis*2)/scale)):
        #y axis
        tim.setpos(tim.xcor()-8, tim.ycor())
        if tim.ycor() != 0 and tim.ycor() != -20:                                               #this avoids 0's clashing at origin
            tim.pu()
            tim.setpos(tim.xcor()-5, tim.ycor()-7)
            tim.write(int(tim.ycor()+7),align="right",font=("Arial",7,"normal"))
            tim.setpos(0,tim.ycor()+7)
            tim.pd()
        else:
            tim.setpos(0,tim.ycor())
        tim.setpos(0,tim.ycor()-scale)  
        #x axis
        tom.setpos(tom.xcor() ,tom.ycor()-8)
        tom.up()
        tom.setpos(tom.xcor() ,tom.ycor()-18)
        tom.write(int(tom.xcor()),align="center",font=("Arial",7,"normal"))
        tom.setpos(tom.xcor(), 0)
        tom.pd()
        tom.setpos(tom.xcor()+scale,0)  
    tom.setpos(tom.xcor(), tom.ycor()-8)                                                        #have to draw the last scale line seperately
    tom.up()
    tom.setpos(tom.xcor() ,tom.ycor()-18)
    tom.write(int(tom.xcor()),align="center",font=("Arial",7,"normal"))
    tom.setpos(tom.xcor(), 0)
    tom.pendown()
    tim.setpos(tim.xcor()-8, tim.ycor())
    tim.pu()
    tim.setpos(tim.xcor()-5, tim.ycor()-7)
    tim.write(int(tim.ycor()+7),align="right",font=("Arial",7,"normal"))
    tim.setpos(0,tim.ycor()+7)
    tim.pd()
    colour_index = -1
    tom.width(2)                                                                                #sets graph line width
    tim.width(2)

def colour_change():                                                                            #changes graph colour
    global colour_index
    if colour_index < len(colour)-1:
        colour_index = colour_index + 1
    else:
        colour_index = 0
    tim.color(colour[colour_index])
    tom.color(colour[colour_index])
    
def draw_polynomial():                                                                          #takes care of drawing the graph
    global Nroots
    global linear
    global quadratic
    global cubic
    global roots
    global colour_index
    global a
    global b
    global c
    global d
    linear = False
    quadratic = False
    cubic = False
    step = 0.5
    TPx1 = 0
    TPx2 = 0
    TPy1 = 0
    TPy2 = 0
    tim.penup()
    tom.penup()
    try:
        a = float(turtle.Screen().textinput("Polynomial","y = ax^3 + bx^2 + cx + d \n\n a = "))                                                                   
        b = float(turtle.Screen().textinput("Polynomial","y = "+str(a)+"x^3 + bx^2 + cx + d \n\n b = "))
        c = float(turtle.Screen().textinput("Polynomial","y = "+str(a)+"x^3 + "+str(b)+"x^2 + cx + d \n\n c = "))
        d = float(turtle.Screen().textinput("Polynomial","y = "+str(a)+"x^3 + "+str(b)+"x^2 + "+str(c)+"x + d \n\n d = "))
    except:
        print("Try again!")
        turtle.Screen().textinput("ERROR","I can't take that as an input\nPlease try again")
        return
    if a == 0 and b == 0 and c == 0 and d == 0:                                                 #decides what type of grapgh it is
        try:
            X = float(turtle.Screen().textinput("Linear","x = "))
            #print("Linear (|)")
            if X < Axis and X >-Axis:
                colour_change()
                tim.setpos(X,0)
                tom.setpos(X,0)
                tim.pd()
                tom.pd()
                tim.setpos(X,Axis)
                tom.setpos(X,-Axis)
                tim.penup()
                tom.penup()
                return
        except:
            print("can't take that value")
            turtle.Screen().textinput("ERROR","I can't take that as an input\nPlease try again")
            return
    elif a == 0 and b == 0:
        if str(c)[0] == "0":
            step = 6
            Nroots = 0
        else:
            step = 0.8
            Nroots = 1
        linear = True
        
    elif a ==0 and b != 0:
        if str(b)[0] == "-":
            print("Quadratic (n)")
        else:
            print("Quadratic (U)")
        quadratic = True
        Nroots = 2
        step = 0.5
        
    elif a != 0:
        print("Cubic (~)")
        cubic = True
        Nroots = 3
        Nroots2 = 3
        step = 0.1        
    #finds where to start drawing (turning pont(s)? the roots? Y-intercept?)
    #if linear... / or -
    if linear == True:
        roots[0] = Roots.linear(c,d)
        turtle.Screen().textinput("Linear", "y = "+str(a)+"x^3 + "+str(b)+"x^2 + "+str(c)+"x + "+str(d)+"\n\nX = "+str(roots[0]))
        if d <= Axis and d >= -Axis:
            tim.setpos(0,d)
            tom.setpos(0,d)
        elif Nroots == 0:                                                                       #checks if it has roots
            if roots[0] < 400 and roots[0] > -400:
                tim.setpos(roots[0],0)
                tom.setpos(roots[0],0)
        else:
            print("Graph not on axis :(")
            turtle.Screen().textinput("ERROR","I can't take that as an input\nPlease try again")
            return
    #if quadratic... U
    elif quadratic == True: 
        TPx = -c/(2*b)                                                                          #x turning point
        TPy = (b*((TPx)**2))+(c*(TPx))+d                                                        #y turning point
        print("Turnig point = (",TPx,",",TPy,")")
        roots[0], roots[1] = Roots.quadratic(b,c,d)
        if TPx<=Axis and TPx>=-Axis and TPy<=Axis and TPy>=-Axis:                               #draw grapgh from turnig point?
            tim.setpos(TPx,TPy)
            tom.setpos(TPx,TPy)
        elif Nroots < 2:                                                                        #draw grapgh from roots?
            if roots[0] <= 400 and roots[0] >= -400:
                tim.setpos(roots[0],0)
                tom.setpos(roots[0],0)
            elif roots[1] <= 400 and roots[1] >= -400:
                tim.setpos(roots[1],0)
                tom.setpos(roots[1],0)
        elif d <= Axis and d >= -Axis:                                                          #draw grapgh from y intercept?
            print("came here")
            tim.setpos(0,d)
            tom.setpos(0,d)
            draw_graph(step,False)
            tim.setpos(TPx*2,d)
            tom.setpos(TPx*2,d)
            colour_index = colour_index - 1
        else:
            print("Turning point, nor roots, nor y intercpet fit on axis :(")
        turtle.Screen().textinput("Quadratic","y = "+str(a)+"x^3 + "+str(b)+"x^2 + "+str(c)+"x + "+str(d)+" \n\nTurning point = ("+str(TPx)+" , "+str(TPy)+") \n\nX = "+str(roots[0])+"\nX = "+str(roots[1]))
    #if cubic... ~
    elif cubic == True:
        dy_div_dx()
        if (c2**2) - (4*b2*d2) >= 0:     #((4*(b**2)) - (12*a*c)) >= 0:                         #determinant of dy/dx (checks if there'es a turning point)
            TPx1 = ((-2*b)+math.sqrt((4*(b**2))-(12*(a*c))))/(6*a)
            TPx2 = ((-2*b)-math.sqrt((4*(b**2))-(12*(a*c))))/(6*a)                              #finds turning points
            TPy1 = a*((TPx1)**3) + b*((TPx1)**2) + (c*(TPx1)) + d
            TPy2 = a*((TPx2)**3) + b*((TPx2)**2) + (c*(TPx2)) + d
            if TPx1 == TPx2 and TPy1 == TPy2:
                Nroots = 1
                Nroots2 = 1
                print("Point of inflection = (",TPx1,",",TPy1,")")
            elif TPy1 == 0 or TPy2 == 0:
                if TPy1 == 0 and TPx1 == 0:
                    print("One turnig point = (",TPx1,",",TPy1,")")
                    print("Second turnig point = (",TPx2,",",TPy2,")")
                    print("x = 0  (x2)")
                    Nroots = 1
                    Nroots2 = 1
                elif TPy2 == 0 and TPx2 == 0:
                    print("One turnig point = (",TPx1,",",TPy1,")")
                    print("Second turnig point = (",TPx2,",",TPy2,")")
                    print("x = 0  (x2)")
                    Nroots = 1
                    Nroots2 = 1
                else:
                    Nroots = 2                                                                  #turning point on axis, so only 2 roots to find
                    Nroots2 = 2
            else:       
                print("One turnig point = (",TPx1,",",TPy1,")")
                print("Second turnig point = (",TPx2,",",TPy2,")")
                if TPy1 > 0 and TPy2 > 0:
                   Nroots = 1
                   Nroots2 = 1
                if TPy1 < 0 and TPy2 < 0:
                   Nroots = 1
                   Nroots2 = 1
                else:
                    Nroots = 3
                    Nroots2 = 3
        else:
            print("No turnig points (gradient never = 0) ")
            Nroots = 1
        roots= Roots.cubic(a,b,c,d, Nroots)
        if Nroots2 == 1:
            turtle.Screen().textinput("Cubic","y = "+str(a)+"x^3 + "+str(b)+"x^2 + "+str(c)+"x + "+str(d)+" \n\nTurning point 1 = ("+str(TPx1)+" , "+str(TPy1)+")\nTurning point 2 = ("+str(TPx2)+" , "+str(TPy2)+")\n\nX = "+str(roots[0]))
        elif Nroots2 == 2:
            turtle.Screen().textinput("Cubic","y = "+str(a)+"x^3 + "+str(b)+"x^2 + "+str(c)+"x + "+str(d)+" \n\nTurning point 1 = ("+str(TPx1)+" , "+str(TPy1)+")\nTurning point 2 = ("+str(TPx2)+" , "+str(TPy2)+")\n\nX = "+str(roots[0])+"\nX = "+str(roots[1]))
        elif Nroots2 == 3:
            turtle.Screen().textinput("Cubic","y = "+str(a)+"x^3 + "+str(b)+"x^2 + "+str(c)+"x + "+str(d)+" \n\nTurning point 1 = ("+str(TPx1)+" , "+str(TPy1)+")\nTurning point 2 = ("+str(TPx2)+" , "+str(TPy2)+")\n\nX = "+str(roots[0])+"\nX = "+str(roots[1])+"\nX = "+str(roots[2]))
        if not(TPy1 > Axis and TPy2 < Axis) and not(TPy1 < -Axis and TPy2 > -Axis):             #checks weather any TPs overlap boundry
            if not(TPy1 < Axis and TPy2 > Axis) and not(TPy1 > -Axis and TPy2 < -Axis):
                if roots[0] <= 400 and roots[0] >= -400:                                        #draw grapgh from root 1?
                    tim.setpos(roots[0],0)
                    tom.setpos(roots[0],0)                        
                elif roots[1] <= 400 and roots[1] >= -400:                                      #draw grapgh from root 2?
                    tim.setpos(roots[1],0)
                    tom.setpos(roots[1],0)
                elif roots[2] <= 400 and roots[2] >= -400:                                      #draw grapgh from root 3?
                    tim.setpos(roots[2],0)
                    tom.setpos(roots[2],0)
                elif TPx1<=Axis and TPy1<=Axis and TPx1>=-Axis and TPy1>=-Axis:                 #draw graph form turnig point
                    tim.setpos(TPx1,TPy1)
                    tom.setpos(TPx1,TPy1)
                elif TPx2<=Axis and TPy2<=Axis and TPx2>=-Axis and TPy2>=-Axis:
                    tim.setpos(TPx2,TPy2)
                    tom.setpos(TPx2,TPy2)  
                elif d <= Axis and d >= -Axis:                                                  #last resort check Y intercept
                    tim.setpos(0,d)
                    tom.setpos(0,d)
            else:
                print("doesn't fit this on Axis :(")
                turtle.Screen().textinput("ERROR","I can't take that as an input\nPlease try again")
                return
        else:
            print("doesn't fit this on Axis :(")
            turtle.Screen().textinput("ERROR","I can't take that as an input\nPlease try again")
            return
    else:
        print("I can't make this graphs yet...")
        turtle.Screen().textinput("ERROR","I can't take that as an input\nPlease try again")
        return
    colour_change()
    draw_graph(step,False)                                                                      #draws grpgh ~ U / -
    
def draw_graph(step,dashed):                                                                    #this is the function needed to draw graph
    global a
    global b
    global c
    global d
    global a2
    global b2
    global c2
    global d2
    global scale
    dash_step = False
    tim_drawing = True
    tom_drawing = True
    tim_step = 0
    tom_step = 0
    tim.pendown()
    tom.pendown()                                                                               #goes along X axis plotting the calculated y value
##    if not(a == 0 and b == 0 and c == 0):
##        dy_div_dx()
    while tom_drawing or tim_drawing:
        if dashed == True and str(round(tim.xcor()/(scale),2))[-2] == "0":                      #makes dashed line
            if dash_step == False:
                dash_step = True
                tim.pendown()
                tom.pendown()  
            elif dash_step == True:
                dash_step = False
                tim.penup()
                tom.penup()
##        if tim.xcor() != 0 and not(a == 0 and b == 0 and c == 0):         #constant  speed
##            tim_step = ( 1/ ( b2*(tim.xcor()**2) + (c2*(tim.xcor())) + d2) ) * step
##        if tom.xcor() != 0 and not(a == 0 and b == 0 and c == 0):
##            tom_step = -( 1/ ( b2*(tom.xcor()**2) + (c2*(tom.xcor())) + d2) ) * step           
##        else:
        tim_step = step
        tom_step = step
        if tim.xcor() < Axis and tim.ycor() < Axis and tim.xcor() >-Axis and tim.ycor() > -Axis:
            tim.setpos(tim.xcor()+tim_step, (a*((tim.xcor()+step)**3))+(b*((tim.xcor()+tim_step)**2))+(c*(tim.xcor()+tim_step))+d)
        else:
            tim_drawing = False
        if tom.xcor() < Axis and tom.ycor() < Axis and tom.xcor() >-Axis and tom.ycor() > -Axis:
            tom.setpos(tom.xcor()-tom_step, (a*((tom.xcor()-tom_step)**3))+(b*((tom.xcor()-tom_step)**2))+(c*(tom.xcor()-tom_step))+d)
        else:
            tom_drawing = False
    tim.pu()
    tom.pu()

def dy_div_dx():
    global a
    global b
    global c
    global d
    global a2
    global b2
    global c2
    global d2
    global c2
    global d3
    d2 = c                                                                                      #first dirirative
    c2 = 2*b
    b2 = 3*a
    #c3 = 2*b2                                                                                   #second dirirative
    #d3 = c2

def draw_circle():
    try:
##        r = float(input("radius = "))                                                         #get inputs: radius & centre (x,y)
##        Cx = float(input("X centre = "))
##        Cy = float(input("Y centre = "))
        r = float(turtle.Screen().textinput("Circle","Radius:"))
        Cx = float(turtle.Screen().textinput("Circle","X centre:"))
        Cy = float(turtle.Screen().textinput("Circle","Y centre:"))
    except:
        print("I can't take that!")
        turtle.Screen().textinput("ERROR","I can't take that as an input\nPlease try again")
        return
    if r > 400 or r < 0:                                                                        #checks if inputs are valid
        print("radius not on axis")
        turtle.Screen().textinput("ERROR","I can't take that as an input\nPlease try again")
        return
    if Cx > 400 or Cx <-400 or Cy>400 or Cy <-400:
        print("centre not on axis")
        turtle.Screen().textinput("ERROR","I can't take that as an input\nPlease try again")
        return
    colour_change()                                                                             #draws circle  
    tim.penup()
    tim.setpos(Cx,Cy-r)
    tim.setheading(0)
    tim.pendown()
    tim.circle(r)                                                                               #I know, I cheated! :(
    tim.penup()
    tim.setpos(0,0)
    tom.penup()                                                                                 #draws midpoint
    tom.setpos(Cx,Cy-1)
    tom.pendown()
    tom.begin_fill()
    tom.circle(1)
    tom.end_fill()
    tom.penup()
    tom.setpos(0,0)

def draw_point():
    global x
    global y
    global colour_index
    if x > 400 or x <-400 or y>400 or y <-400:                                                  #checks if point is on Axis
        print("Point not on axis")
        turtle.Screen().textinput("ERROR","I can't take that as an input\nPlease try again")
        return
    tim.color("black")           
    tim.fillcolor(colour[colour_index])
    tim.penup()
    tim.width(1)
    tim.setpos(x,y-2)
    tim.pendown()
    tim.begin_fill()
    tim.circle(2)
    tim.end_fill()
    if (x <=-50 or x >=20) and (y <=-35 or y >= 0):                                                #doesnt write coordinate if point too close to axis
        if x%2 == 0 or (x+1)%2 == 0:
            x = int(x)
        else:
            x = round(x,2)
        if y%2 == 0 or (y+1)%2 == 0:
            y = int(y)
        else:
            y = round(y,2)
        tim.write((x,y),align="center",font=("Arial",7,"normal"))
    tim.width(2)
    tim.penup()
    tim.color(colour[colour_index])
    tim.setpos(0,0)
    
def specail():                                                                                  #it's a surprise!!!
        tim.clear()                                                                             #what will it do???
        tim.hideturtle()                                                                        #you're going to have to try it...
        tom.color("light blue")
        tom.pu()
        tom.setpos(0,80)
        tom.pd()
        tom.write("Peter is amazing!",False,align="center",font=("Arial",60,"bold"))
        time.sleep(5)
        tom.pu()
        tom.setpos(0,0)
        time.sleep(10)
        draw_axis()

def draw_wave():                                                                                #draws sine / cosine / tangent wave
    global Status
    print("Grapgh 100x bigger \nso e.g. sin(30) = 50, not 0.5")
    step = 1
    tim_drawing = True
    tom_drawing = True
    t = True
    x = 0
    y = 0
    i = 0
    colour_change()
    if y+100 < Axis and y+100 > -Axis:
        tom.pu()
        tim.pu()
        if Status == "sin" or Status == "sine":
            tom.setpos(0,0)
            tim.setpos(0,0)
        elif Status == "cos" or Status == "cosine":
            tom.setpos(0,100)
            tim.setpos(0,100)
        elif Status == "tan" or Status == "tangent":
            tom.setpos(0,0)
            tim.setpos(0,0)
            step = 0.2
        tim.pendown()
        tom.pendown()
        while tom_drawing or tim_drawing:                                                       #remember to convert form radians to degrees
            if Status == "sin" or Status == "sine":
                if tim.xcor() <= Axis and tim.ycor() <= Axis and tim.xcor() >=-Axis and tim.ycor() >= -Axis:
                    tim.setpos( tim.xcor()+step, 100*(math.sin((tim.xcor()+step)*(math.pi/180))) )  
                else:
                    tim_drawing = False
                if tom.xcor() <= Axis and tom.ycor() <= Axis and tom.xcor() >=-Axis and tom.ycor() >= -Axis:
                    tom.setpos( tom.xcor()-step, 100*(math.sin((tom.xcor()+step)*(math.pi/180))) )
                else:
                    tom_drawing = False
            elif Status == "cos" or Status == "cosine":
                if tim.xcor() <= Axis and tim.ycor() <= Axis and tim.xcor() >=-Axis and tim.ycor() >= -Axis:
                    tim.setpos( tim.xcor()+step, 100*(math.cos((tim.xcor()+step)*(math.pi/180))) )
                else:
                    tim_drawing = False
                if tom.xcor() <= Axis and tom.ycor() <= Axis and tom.xcor() >=-Axis and tom.ycor() >= -Axis:
                    tom.setpos( tom.xcor()-step, 100*(math.cos((tom.xcor()-step)*(math.pi/180))) )
                else:
                    tom_drawing = False
            elif Status == "tan" or Status == "tangent":
                if not(tim.ycor() < Axis and tim.ycor() > -Axis) and tim.xcor() < Axis:
                    while t:
                        x = tim.xcor() + i                                                      #look for next y value on grapgh
                        y = 100*(math.tan(x*(math.pi/180)))         
                        if not( ((x-90)/180).is_integer() ):                                    #don't get error at asyemptotes                            
                            if  not(y <=Axis and y >= -Axis):
                                i = i + step
                            else:
                                tim.pu()
                                tom.pu()
                                tim.setpos(x,y)
                                tom.setpos(-x,-y)
                                tim.pd()
                                tom.pd()
                                t = False
                    t = True
                else:
                    if tim.xcor() <= Axis and tim.ycor() <= Axis and tim.xcor() >=-Axis and tim.ycor() >= -Axis:
                        tim.setpos( tim.xcor()+step, 100*(math.tan((tim.xcor()+step)*(math.pi/180))) )
                    else:
                        tim_drawing = False
                    if tom.xcor() <= Axis and tom.ycor() <= Axis and tom.xcor() >=-Axis and tom.ycor() >= -Axis:
                        tom.setpos( tom.xcor()-step, 100*(math.tan((tom.xcor()-step)*(math.pi/180))) )
                    else:
                        tom_drawing = False
        tim.pu()
        tom.pu()
    else:
        print("won't fit on Axis")
        turtle.Screen().textinput("ERROR","I can't take that as an input\nPlease try again")
        draw_wave()

def regression_line():
    global x
    global y
    global a
    global b
    global c
    global d
    global colour_index
    step = 1    #cannot change this
    colour_change()
    Xpoints = []
    Ypoints = []
    index = 1
    X = 0
    Y = 0
    Sxy = 0
    Sxx = 0
    #print("Type 'd' or 'done' in when finished")
    while True:
        #print("Point", index)
        x = turtle.Screen().textinput("Regression line","Type 'd' or 'done' in when finished\n\nPoint"+str(index)+"\n\nx = ")
        y = turtle.Screen().textinput("Regression line","Type 'd' or 'done' in when finished\n\nPoint"+str(index)+"\n\ny = ")
        if x == "d" or x == "done" or y == "d" or y == "done":
            break
        try:
            x = float(x)
            y = float(y)
            if x > 400 or x <-400 or y>400 or y <-400:                                          #checks if point is on Axis
                print("point not on axis")
                return
            Xpoints.append(x)
            Ypoints.append(y)
            draw_point()
        except:
            turtle.Screen().textinput("ERROR","I can't take that as an input\nPlease try again")
            return
        index += 1
    if len(Xpoints) <= 1 or len(Ypoints) <= 1:
        return
    
    for x in range(0,len(Xpoints)):
        X += Xpoints[x]                                                                         #sums
        Y += Ypoints[x]
    X = X / len(Xpoints)                                                                        #avgs
    Y = Y / len(Ypoints)
    for p in range(0,len(Xpoints)):
        Sxy += (Xpoints[p]-X)*(Ypoints[p]-Y)
        Sxx += (Xpoints[p]-X)**2
    c = Sxy / Sxx
    d = Y-(c*X)
    if str(c)[0] == "-":
        turtle.Screen().textinput("Refression line","y = "+str(d)+" "+str(c)+"x \n\n Press enter")
        #print("y =",d, c,"x")
    else:
        turtle.Screen().textinput("Regression line","y = "+str(d)+" + "+str(c)+"x \n\n Press enter")
        #print("y =",d,"+",c,"x")
    tim.pu()
    tom.pu()
    if d <= Axis and d >= -Axis:                                                                #check Y intercept
        tim.setpos(0,d)
        tom.setpos(0,d)
    elif X < Axis and X > -Axis and Y > -Axis and Y < Axis:                                     #check average point
        tim.setpos(X,Y)
        tom.setpos(X,Y)
    else:
        print("can't draw this line of these axis")
        return
    a = 0
    b = 0
    draw_graph(step, True)

def complex_numbers():
    global x
    global y
    argument = 0
    colour_change()
    print("z = a + bi")
    try:
        x = float(turtle.Screen().textinput("Complex Numbers","z = a + bi\na = "))
        y = float(turtle.Screen().textinput("Complex Numbers","z = "+str(x)+" + bi\nb = "))
    except:
        turtle.Screen().textinput("ERROR","I can't take that as an input\nPlease try again")
        return
    draw_point()
    print("modulus =", math.sqrt((x**2) + (y**2)) )
    if str(x)[0] == "-" and str(y)[0] == "-":                                                   #finds which quadrant of 'argand diagram' the complex number is in
        argument = -(pi-math.atan(y/x))
    elif str(x)[0] == "-" and str(y)[0] != "-":
        argument = pi-math.atan(y/x)
    elif str(x)[0] != "-" and str(y)[0] == "-":
        argument = -math.atan(y/x) 
    elif str(x)[0] != "-" and str(y)[0]!= "-":
        argument = math.atan(y/x)
    else:
        print("error?!?")
    print("argument =", argument,"    -->   in radians")
    print("argument =", (argument/pi)*180,"    -->   in degrees")
    turtle.Screen().textinput("Complex Numbers","z = "+str(x)+" + "+str(y)+"i\n\nModulus = "+str(math.sqrt((x**2) + (y**2)))+"\n\nArgument ="+str(argument)+"  -->   in radians\nArgument ="+str((argument/pi)*180)+"  -->   in degrees\n")

def mandelbrot_set():
    global mandelbrotSet
    global MSredScale
    global MSblueScale
    colour = "red3"
    colour_before = ""
    y = 0
    stable = False
    coloured = False
    circular = False
    ans = 0
    c = turtle.Screen().textinput("Mandelbrot Set","Which colour scheme?\n red, blue or black")
    if c == "black":
        coloured = False
    elif c == "red":
        coloured = True
        WhichColour = "red"
    elif c == "blue":
        coloured = True
        WhichColour = "blue"   
    else:
        turtle.Screen().textinput("ERROR","I can't take that as an input\nPlease try again")
        return
    circle = turtle.Screen().textinput("Mandelbrot Set","Circular?\nyes or no? ")
    if circle == "yes" or circle == "y":
        circular = True
    elif circle == "n" or circle == "no":
        circular = False
    else:
        turtle.Screen().textinput("ERROR","I can't take that as an input\nPlease try again")
        return
    res = turtle.Screen().textinput("Mandelbrot Set","Resolution = ")
    try:
        res = float(res)                                                                        #checks for valid input
    except:
        turtle.Screen().textinput("ERROR","I can't take that as an input\nPlease try again")
        return
    if res <= 0.5:                                                                              #0.51 is the smallest it can be due to overlapping lines
        res = 0.51
    tim.pensize(res)
    tom.pensize(res)
    x = -400
    x -= res                                                                                    #so that x starts at 0
    tim.clear()
    tom.clear()
    tum.clear()
    try:
        before = s.get_time()
        while x <= (400 - res):                                                                 #x loop starting at -400 each time
            x += res
            if circular == False:
                y = -res
            elif circular == True:
                y = -math.sqrt((400**2) - ((x)**2))
            if circular == True:
                ylimit = math.sqrt((400**2) - (x**2))
            else:
                ylimit = 400
            while y < ylimit:                                                                   #y loop starting at -400 each time
                y += res
                Xscale = x / 200                                                                # /200 for scale- should be between -2 &2  , not -400 & 400
                Yscale = y / 200
                # Xscale = 0.285                                                             # /200 for scale- should be between -2 &2  , not -400 & 400
                #Yscale = 0
                ans = complex(0,0)                                                              #reset ans
                for i in range(0,100):                                                          #The number of iterations - the more, the more accurate
                    ans = ( ans**2 + complex(Xscale, Yscale) )                                      
                    if (ans.real**2) + (ans.imag**2) >= 4:                                      #checks weather stable or not. As anything that leaves a circle with radius 2 is unstable
                        stable = False
                        if coloured == True:
                            if WhichColour == "red":
                                for c in range (0,len(MSredScale)):
                                    if i > MSredScale[c][0]:
                                        colour = MSredScale[c][1]
                                        break
                            if WhichColour == "blue":
                                for c in range (0,len(MSblueScale)):
                                    if i > MSblueScale[c][0]:
                                        colour = MSblueScale[c][1]
                                        break
                        break
                    else:
                        stable = True
                if stable == True:
                    colour = "black"
                if stable == False and coloured == False:
                    colour = "white"
                if colour_before != colour or y >= 400:                                         #only draw new line when colour has changed
                    tim.color(colour_before)
                    tom.color(colour_before)
                    colour_before = colour
                    #tom.setpos(x,tom.ycor()-res)                                               #This stops lines overlapping but creates white spaces
                    #tim.setpos(x,tim.ycor()+res)
                    tim.pd()
                    tom.pd()
                    tom.setpos(x,-y)
                    tim.setpos(x,y)
                    tom.pu()
                    tim.pu()
                if y >= 400 and circular == False:                                                                    #stops overlaping colours when y resets to -400
                    tom.setpos(x+res, 0)
                    tim.setpos(x+res, 0)
                    colour_before = ""
                if circular == True and y >= math.sqrt((400**2) - ((x)**2)):
                    tom.setpos(x+res, 0)
                    tim.setpos(x+res, 0)
                    colour_before = ""
    except:
        pass
    after = s.get_time()
    secs, mins, hrs = s.TotalTime(before, after)
    axis = turtle.Screen().textinput("Mandelbrot Set","That took: "+str(hrs)+"hrs "+str(mins)+"mins "+str(secs)+"secs\n\nDraw Axis?")
    mandelbrotSet = True
    if axis == "yes" or axis == "y":
        draw_axis()


def press():
    global x
    global y
    #pen_status = "down"
    tum.pensize(2)
    tum.setpos(0,0)
    turtle.Screen().textinput("Inputs", "'Esc' = Exit this mode\n'Left click' = coordinate\n'Right click' = clear\n'space' = pen up/down\n'h' = hides turtle\n'z' = undoes last point")
    tum.showturtle()
    def pos(X,Y):
        global x
        global y
        if not(X > 400 or Y > 400 or X <-400 or Y<-400):
            x = X
            y = Y
            draw_point()
    def leave():
        tum.hideturtle()
        main()
    def clean(x,y):
        tum.clear()
    def dragging(x,y):
        tum.ondrag(None)
        tum.setheading(tum.towards(x,y))
        tum.setpos(x,y)
        tum.ondrag(dragging)
    def back():
        for _ in range(0,7):
            tim.undo()
    def penup():
        global pen_status
        if pen_status == "down":
            pen_status = "up"
            tum.pu()
        elif pen_status == "up":
            pen_status = "down"
            tum.pd()
    def hide():
        global hide_status
        if hide_status == "show":
            hide_status = "hidden"
            tum.hideturtle()
        elif hide_status == "hidden":
            hide_status = "show"
            tum.showturtle()

    turtle.Screen().listen()
    tum.ondrag(dragging)
    turtle.Screen().onkey(leave, 'Escape')
    turtle.Screen().onscreenclick(pos, 1)
    turtle.Screen().onscreenclick(clean, 3)
    turtle.Screen().onkey(penup, 'space')
    turtle.Screen().onkey(hide, 'h')
    turtle.Screen().onkey(back, 'z')
    turtle.Screen().mainloop()
 
def main():
    global mandelbrotSet
    global x
    global y
    global Status
    while True:                                                                                    #main loop
    ##    try:
    ##        Status = input("Status: ")
    ##    except:
    ##        pass
        Status = turtle.Screen().textinput("Type one",my_list)
        if Status =="quit" or Status =="exit" or Status =="q":
            print("Bye then! :(")
            turtle.Screen().bye()
            quit()
        elif Status =="stop" or Status =="pause" or Status =="s" or Status == None:
            ans = turtle.Screen().textinput("? :( ?", "Are you sure you want to stop?")
            if ans == "yes" or ans == "y" or ans == "":
                break
            else:
                pass
        elif Status =="reset" or Status =="r" or Status =="clear" or Status =="undo":
            draw_axis()
        elif mandelbrotSet == True:
            mandelbrotSet = False
            draw_axis()
        elif Status == "ms" or Status == "mandelbrot set":
            mandelbrot_set()
        elif Status == "peter" or Status == "surprise" or Status == "specail" or Status == "surprise!":
            specail()
        elif Status == "sin" or Status == "cos" or Status == "cosine" or Status == "sine" or Status == "tan" or Status == "tangent":
            draw_wave()
        elif Status == "regression line" or Status == "rl":
            regression_line()
        elif Status == "point" or Status == "p" or Status == "P":
            try:
                x = float(turtle.Screen().textinput("Coordinate","X = "))
                y = float(turtle.Screen().textinput("Coordinate","Y = "))
            except:
                turtle.Screen().textinput("ERROR","I can't take that as an input\nPlease try again")
            draw_point()
            
        elif Status == "c" or Status == "circle" or Status == "C":
            draw_circle()
        elif Status == "cn" or Status == "complex number" or Status == "i":      
            complex_numbers()
        elif Status == "" or Status == "linear" or Status == "quadratic" or Status == "graph" or Status == "cubic":
            draw_polynomial()
        elif Status == "d" or Status == "draw" or Status == "plot":
            press()
        else:
            turtle.Screen().textinput("ERROR","I can't take that as an input\nPlease try again")
    return
my_list = "Inputs:\n'enter' = draws a: linear, quadratic or cubic\n'c' = draws a circle\n'sin' = draws a sine wave\n'cos' = draws a cosine wave\n'tan' = draws a tangent wave\n'p' = draws a point/coordinate)\n'd' = draw/plot\n'rl' = least squares regression line\n'cn' = complex numbers\n'ms' = mandelbrot set\n's' = stop\n'r' = reset axis\n'q' = quit\n'surprise' = !???! \n"
draw_axis()
main()
