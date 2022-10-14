import schedule
import csv
import time
from datetime import datetime
now = datetime.now()
from config import portfolio_amount


montant = portfolio_amount()
date = now

fieldnames = ['Montant', 'Date']


# Ouvre, ou créer et ouvre le fichier csv
def data():
    with open('data.csv', 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'Montant': montant, 'Date': date})


#Toute les 24h à 13.40
schedule.every().day.at("13:40").do(data)

while 1:
    schedule.run_pending()
    time.sleep(1)


def test_1():
    tval = data()
    assert tval == None