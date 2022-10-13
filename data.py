import schedule
import csv
import time
from datetime import datetime
now = datetime.now()
from config import portfolio_amount


montant = portfolio_amount()
date = now

fieldnames = ['Montant', 'Date']


def data():
    with open('data.csv', 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'Montant': montant, 'Date': date})


schedule.every().day.at("13:40").do(data)

while 1:
    schedule.run_pending()
    time.sleep(1)
