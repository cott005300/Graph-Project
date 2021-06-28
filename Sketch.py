import turtle

pen_status = "down"
hide_status = "hidden"

class sketch():
      
    def press(Pass):
        
        turtle.Screen().setup(500,600,-100,50)                                                          #make scrren the right size (allowing for header and things)
        turtle.Screen().title("Peter's turtle sketch")

        tum = turtle.Turtle("turtle")

        #pen_status = "down"
        tum.pensize(2)
        tum.setpos(0,0)
        #turtle.Screen().textinput("Inputs", "'Esc' = Exit this mode\n'\n'Right click' = clear\n'space' = pen up/down\n'h' = hides turtle\n'z' = undoes last point")
        tum.showturtle()

        def clean(x,y):
            tum.clear()
        def dragging(x,y):
            tum.ondrag(None)
            tum.setheading(tum.towards(x,y))
            tum.setpos(x,y)
            tum.ondrag(dragging)
        def back():
            for _ in range(0,7):
                tum.undo()
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
        def goto(x, y):
            tum.setheading(tum.towards(x,y))
            tum.setpos(x,y)

        turtle.Screen().listen()
        tum.ondrag(dragging)
        turtle.Screen().onscreenclick(clean, 3)
        turtle.Screen().onscreenclick(goto, 1)
        turtle.Screen().onkey(penup, 'space')
        turtle.Screen().onkey(hide, 'h')
        turtle.Screen().onkey(back, 'z')
        turtle.Screen().mainloop()

