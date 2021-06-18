import random
import string

class make_list():

    def Random(data, comp, list_len, list_range):
        items = []
        if data == 1:
            for i in range (0, list_len):
                items.append(random.randint(0,list_range))
        if comp != 1:
            print("random list = ", items)
        return items



    def Input(data):
        n = int(input("number of items in list = "))
        items = []
        for i in range (0,n):
            if data == 1:
                items.append(int(input(f"{(i+1)} = ")) )
            else:
                items.append(str(input(f"{(i+1)} = ")) )
        print("List =", items)
        return items