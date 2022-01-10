import math

equation_1 = "v = u + at\n"
equation_2 = "s = 1/2t(u + v)\n"
equation_3 = "s = ut + 1/2at^2\n"
equation_4 = "v^2 = u^2 + 2as\n"
equation_5 = "s = vt - 1/2vt^2\n"

class SUVAT():

    s = ""
    u = ""
    v = ""
    a = ""
    t = ""
    sb = False
    ub = False
    vb = False
    ab = False
    tb = False

    def calculate(S, U, V, A, T):
        global s, u, v, a, t
        global sb, ub, vb, ab, tb

        def checkList():
            global s, u, v, a, t
            global sb, ub, vb, ab, tb
            
            try:
                s = float(s)
                sb = True
            except:
                sb = False
                
            try:
                u = float(u)
                ub = True
            except:
                ub = False
                
            try:
                v = float(v)
                vb = True
            except:
                vb = False
                
            try:
                a = float(a)
                ab = True
            except:
                ab = False
                
            try:
                t = float(t)
                tb = True
            except:
                tb = False
        
        s = S
        u = U
        v = V
        a = A
        t = T
        equ = ""
        
        counter = 0
        checkList()

        while sb==False or ub==False or vb==False or ab==False or tb==False:
            counter += 1
            ####
                
            if vb==False and ub==True and ab==True and tb==True:  
                v = u + (a*t)

                equ += str(equation_1)
                checkList()

            if vb==True and ub==False and ab==True and tb==True: 
                u = v - (a*t)
                equ += str(equation_1)
                checkList()

            if vb==True and ub==True and ab==False and tb==True: 
                a = (v-u)/t
                equ += str(equation_1)
                checkList()

            if vb==True and ub==True and ab==True and tb==False: 
                t = (v - u) / a
                equ += str(equation_1)
                checkList()

            ###

            if sb==False and ub==True and vb==True and tb==True:
                s = 0.5*t*(u+v)
                equ += str(equation_2)
                sdone = True
                checkList()
                
            if sb==True and ub==False and vb==True and tb==True:
                u = ((2*s)/t)-v
                equ += str(equation_2)
                checkList()

            if sb==True and ub==True and vb==False and tb==True:
                v = ((2*s)/t)-u
                equ += str(equation_2)
                checkList()

            if sb==True and ub==True and vb==True and tb==False:
                t = s/(0.5*(u+v))
                equ += str(equation_2)
                checkList()


            ###


            if sb==False and ub==True and tb==True and ab==True:
                s = (u*t)+(0.5*a*(t**2))
                equ += str(equation_3)
                checkList()

            if sb==True and ub==False and tb==True and ab==True:
                u = (s-(0.5*a*(t**2)))/t
                equ += str(equation_3)
                checkList()

            if sb==True and ub==True and tb==False and ab==True:
                if s == 0:
                    #print("T = 0")
                    t = (-1*u) / (0.5*a)                    
                elif s != 0:                        
                    t = (((u*-1) + math.sqrt(abs((u**2)-(4*(0.5*a)*(-1*s))))) / a)
                    #print("T =", (((u*-1) - math.sqrt(abs((u**2)-(4*(0.5*a)*(-1*s))))) / a))
                #print("T =", t)
                equ += str(equation_3)
                checkList()

            if sb==True and ub==True and tb==True and ab==False:
                a = (s-(u*t))/(0.5*(t**2))
                equ += str(equation_3)
                adone = True
                checkList()

            ####

            if vb==False and ub==True and ab==True and sb==True:
                v = math.sqrt(abs((u**2)+(2*a*s)))
                equ += str(equation_4)
                checkList()

            if vb==True and ub==False and ab==True and sb==True:
                u = math.sqrt(abs((v**2)-(2*a*s)))
                equ += str(equation_4)
                checkList()

            if vb==True and ub==True and ab==False and sb==True:
                a = ((v^2)-(u**2))/(2*s)
                equ += str(equation_4)
                checkList()

            if vb==True and ub==True and ab==True and sb==False:
                s = ((v^2)-(u**2))/(2*a)
                equ += str(equation_4)
                checkList()
                
            ####
                
            if vb==True and ab==True and sb==False and tb==True:
                s = (v*t)-(0.5*a*(t**2))
                equ += str(equation_5)
                checkList()


            if vb==False and ab==True and sb==True and tb==True:
                v = (s-(0.5*a*(t**2)))/t
                equ += str(equation_5)
                checkList()

            if vb==True and ab==False and sb==True and tb==True:
                a = (s-(v*t))/(-0.5*(t*2))
                equ += str(equation_5)
                checkList()
                            
    ##
    ##        if vb==True and ab==True and sb==True and tb==False:
    ##            if s == 0:
    ##                print("T = 0")
    ##                t = (-1*u) / (0.5*a)                    
    ##            elif s != 0:                        
    ##                t = (((u*-1) + math.sqrt(abs((u**2)-(4*(0.5*a)*(-1*s))))) / a)
    ##                print("T =", (((u*-1) - math.sqrt(abs((u**2)-(4*(0.5*a)*(-1*s))))) / a))
    ##
    ##            print()"T =", t)
    ##            print("I used", equation_5)
    ##            checkList()




            ####

            if ub==False and sb==True and tb==True:
                u = s / t
                equ += "v = s / t\n"
                checkList()
            
            if ub==True and sb==False and tb==True:
                s = u * t
                equ += "v = s / t\n"
                checkList()

            if ub==True and sb==False and tb==True:
                t = s / u
                equ += "v = s / t\n"
                checkList()



            
            if ub==False or sb==False or vb==False or ab==False or tb==False and counter>10:
                return None

        return s, u, v, a, t, equ


