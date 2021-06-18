from timer import timer as t

class search():

    def binary(items, find):
        found = False
        first = 0
        last = len(items) - 1
        before = t.get_time()
        while first <= last and found == False:
            mdpt = int( first + (last - first)/2 ) 
            if items[mdpt] == find:
                found = True
            elif items[mdpt] < find:
                first = mdpt + 1
            else:
                last = mdpt - 1
        after = t.get_time()
        secs, mins, hrs = t.TotalTime(before, after)
        if found == True:
            print("Found", find)
        else:
            print("Not Found")
        print("Took", hrs,"hrs ", mins,"mins ", secs,"secs ")


    def linear(items, find):
        index = 0
        found = False
        before = t.get_time()
        while found == False and index < len(items):
            if items[index] == find:
                found = True
            else:
                index += 1
        after = t.get_time()
        secs, mins, hrs = t.TotalTime(before, after)
        if found == True:
            print("Found", items[index])
        else:
            print("Not Found")
        print("Took", hrs,"hrs ", mins,"mins ", secs,"secs ")