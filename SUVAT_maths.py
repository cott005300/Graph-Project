import math


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
            
            if not(s):
                sb = False
            else:
                sb = True
                s = float(s)
                
            if not(u) and u != 0:
                ub = False
                
            else:
                ub = True
                u = float(u)
                
            if not(v) and u != 0:
                vb = False
            else:
                vb = True
                v = float(v)
                
            if not(a):
                ab = False
            else:
                ab = True
                a = float(a)
                
            if not(t):
                tb = False
            else:
                tb = True
                t = float(t)
            
        s = S
        u = U
        v = V
        a = A
        t = T
        
        counter = 0
        checkList()

        while sb==False or ub==False or vb==False or ab==False or tb==False:
            counter += 1
            ####
                
            if vb==False and ub==True and ab==True and tb==True:  
                v = u + (a*t)

                #print("-I used", equation_1)
                checkList()

            if vb==True and ub==False and ab==True and tb==True: 
                u = v - (a*t)
                #print("-I used", equation_1)
                checkList()

            if vb==True and ub==True and ab==False and tb==True: 
                a = (v-u)/t
                #print("-I used", equation_1)
                checkList()

            if vb==True and ub==True and ab==True and tb==False: 
                t = (v - u) / a
                #print("-I used", equation_1)
                checkList()

            ###

            if sb==False and ub==True and vb==True and tb==True:
                s = 0.5*t*(u+v)
                #print("-I used", equation_2)
                sdone = True
                checkList()
                
            if sb==True and ub==False and vb==True and tb==True:
                u = ((2*s)/t)-v
                #print("-I used", equation_2)
                checkList()

            if sb==True and ub==True and vb==False and tb==True:
                v = ((2*s)/t)-u
                #print("-I used", equation_2)
                checkList()

            if sb==True and ub==True and vb==True and tb==False:
                t = s/(0.5*(u+v))
                #print("-I used", equation_2)
                checkList()


            ###


            if sb==False and ub==True and tb==True and ab==True:
                s = (u*t)+(0.5*a*(t**2))
                #print("-I used", equation_3)
                checkList()

            if sb==True and ub==False and tb==True and ab==True:
                u = (s-(0.5*a*(t**2)))/t
                #print("-I used", equation_3)
                checkList()

            if sb==True and ub==True and tb==False and ab==True:
                if s == 0:
                    #print("T = 0")
                    t = (-1*u) / (0.5*a)                    
                elif s != 0:                        
                    t = (((u*-1) + math.sqrt(abs((u**2)-(4*(0.5*a)*(-1*s))))) / a)
                    #print("T =", (((u*-1) - math.sqrt(abs((u**2)-(4*(0.5*a)*(-1*s))))) / a))
                #print("T =", t)
                #print("-I tried to use", equation_3)
                checkList()

            if sb==True and ub==True and tb==True and ab==False:
                a = (s-(u*t))/(0.5*(t**2))
                #print("-I used", equation_3)
                adone = True
                checkList()

            ####

            if vb==False and ub==True and ab==True and sb==True:
                v = math.sqrt(abs((u**2)+(2*a*s)))
                #print("-I used", equation_4)
                checkList()

            if vb==True and ub==False and ab==True and sb==True:
                u = math.sqrt(abs((v**2)-(2*a*s)))
                #print("-I used", equation_4)
                checkList()

            if vb==True and ub==True and ab==False and sb==True:
                a = ((v^2)-(u**2))/(2*s)
                #print("-I used", equation_4)
                checkList()

            if vb==True and ub==True and ab==True and sb==False:
                s = ((v^2)-(u**2))/(2*a)
                #rint("-I used", equation_4)
                checkList()
                
            ####
                
            if vb==True and ab==True and sb==False and tb==True:
                s = (v*t)-(0.5*a*(t**2))
                #print("I used", equation_5)
                checkList()


            if vb==False and ab==True and sb==True and tb==True:
                v = (s-(0.5*a*(t**2)))/t
                #print("I used", equation_5)
                checkList()

            if vb==True and ab==False and sb==True and tb==True:
                a = (s-(v*t))/(-0.5*(t*2))
                #print("I used", equation_5)
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
                #print("-I just used s = d / t")
                checkList()
            
            if ub==True and sb==False and tb==True:
                s = u * t
                #print("-I just used s = d / t")
                checkList()

            if ub==True and sb==False and tb==True:
                t = s / u
                #print("-I just used s = d / t")
                checkList()



            
            if ub==False or sb==False or vb==False or ab==False or tb==False and counter>10:
                return None

        return s, u, v, a, t


