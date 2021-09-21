import time

class timer():
    
    def get_time():
        return time.time()

    def TotalTime(t1, t2):
        totals = t2 - t1
        if totals > 60:
            totalm = int(totals / 60)
            totals = ((totals / 60) - int(totals / 60))*60
            if totalm > 60:
                totalh = int(totalm / 60)
                totalm = ((totalm / 60) - int(totalm / 60))*60

            else:
                totalh = 0
        else:
            totalm = 0
            totalh = 0
        return round(totals,2), round(totalm,2), totalh
