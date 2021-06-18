from timer import timer as t
passes = 0

class sort():

    def start(sort_type, items, show, comp):
        global passes
        passes = 0
        Type = ""
        before = t.get_time()
        if sort_type == 1:
            Type = "Bubble"
            sorted_list = sort.bubble(items, show)
        elif sort_type == 2:
            Type = "Insertion"
            sorted_list = sort.insertion(items, show)
        elif sort_type == 3:
            Type = "Merge"
            sorted_list = sort.merge(items, show)
        elif sort_type == 4:
            Type = "Quick"
            sorted_list = sort.quick_sort(items, 0, len(items)-1)
        after = t.get_time()
        secs, mins, hrs = t.TotalTime(before, after)

        return mins, secs, passes



    def bubble(items, show):
        global passes
        swapped = True
        n = len(items)
        while n > 0 and swapped == True:
            n -= 1
            passes += 1
            swapped = False
            for i in range (0, n):
                passes += 1
                if items[i] > items[i+1]:
                    temp = items[i]
                    items[i] = items[i+1]
                    items[i+1] = temp
                    swapped = True
        return items


    def insertion(items, show):
        global passes
        n = len(items)
        for i in range (1,n):
            a = items[i]
            b = i
            passes += 1
            while b > 0 and items[b-1] > a:
                passes += 1
                items[b] = items[b-1]
                b -= 1
            items[b] = a
        return items

    def merge(alist, show):
        global passes
        if len(alist)>1:
            mid = len(alist)//2
            lefthalf = alist[:mid]
            righthalf = alist[mid:]

            sort.merge(lefthalf,show)
            sort.merge(righthalf,show)
            passes +=1 
            i=0
            j=0
            k=0
            while i < len(lefthalf) and j < len(righthalf):
                passes += 1
                if lefthalf[i] <= righthalf[j]:
                    alist[k]=lefthalf[i]
                    i += 1
                else:
                    alist[k]=righthalf[j]
                    j += 1
                k=k+1
            while i < len(lefthalf):
                passes += 1
                alist[k]=lefthalf[i]
                i += 1
                k += 1
            while j < len(righthalf):
                passes += 1
                alist[k]=righthalf[j]
                j += 1
                k += 1
        return alist

    def pivot(array, start, end):
        global passes
        pivot = array[start]
        low = start + 1
        high = end
        while True:
            passes += 1
            while low <= high and array[high] >= pivot:
                passes += 1
                high = high - 1
            while low <= high and array[low] <= pivot:
                passes += 1
                low = low + 1
            if low <= high:
                array[low], array[high] = array[high], array[low]
            else:
                break
        array[start], array[high] = array[high], array[start]
        return high
    
    def quick_sort(array, start, end):
        if start >= end:
            return
        p = sort.pivot(array, start, end)
        sort.quick_sort(array, start, p-1)
        sort.quick_sort(array, p+1, end) 
        return array
