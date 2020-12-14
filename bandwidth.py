import time
import psutil
import csv
import os.path
from os import path
import datetime

# Can set time to more/less than 60 seconds
# Recommend making into Automation so it runs a few times a day
    # MacOS instructions: http://sickbeard.com/forums/viewtopic.php?f=3&t=87&start=60#p16053

def createCSV():
    csv_c = csv.writer(open('Bandwidth.csv', 'w'))
    csv_c.writerow(['Date', 'Time', 'Received', 'Sent', 'Total', 'Seconds'])

def updateCSV(sent, rec, seconds):
    csv_u = csv.writer(open("Bandwidth.csv", 'a'))
    csv_u.writerow([datetime.date.today(), datetime.datetime.now().strftime("%H:%M:%S"), rec, sent, rec + sent, int(seconds)])

def toGig(x):
    return x/1024./1024./1024.*8

def roundGigs(x):
    return "{:.3f}".format(toGig(x))

def monitor():
    totalSent = 0
    totalRec = 0

    sTime = time.time()
    while time.time() - sTime < 60:
        sent = psutil.net_io_counters().bytes_sent
        rec = psutil.net_io_counters().bytes_recv

        time.sleep(1)

        totalSent += psutil.net_io_counters().bytes_sent - sent
        totalRec += psutil.net_io_counters().bytes_recv - rec
    
    if not path.exists("./Bandwidth.csv"):
        createCSV()
    
    updateCSV(roundGigs(totalSent),roundGigs(totalRec), time.time() - sTime)

if __name__ == "__main__":
    monitor()
