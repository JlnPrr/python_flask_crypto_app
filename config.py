import sqlite3
import os.path
import flask_app
import requests
from datetime import datetime
from time import strftime
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import time
import matplotlib.pyplot as plt
import pprint

# Active le mode debug
DEBUG = True
global returned_value
global cursor
global connection
global val
val = 3


# Ouverture du fichier de la database SQLite 3
def open_database():
    global cursor
    global connection
    location = os.path.join('/home/JlnPrr/mysite/database/database.db')
    print(location)
    connection = sqlite3.connect(location)
    print('Opened database successfully')
    cursor = connection.cursor()


# Utilsation de l'API CoinMarketCAP pour 3 types de crypto
def tracking_add(item):
    global returned_value
    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    parameters = {
        'id': '1,1027,52',
        'convert': 'EUR'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'db1037d9-b37a-4dee-8178-238435d0d2b1',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        val1 = str(round((data['data']['1']['quote']['EUR']['price']), 2))
        val2 = str(round((data['data']['1027']['quote']['EUR']['price']), 2))
        val3 = str(round((data['data']['52']['quote']['EUR']['price']), 2))

        if item == 'BTC':
            returned_value = val1
        elif item == 'ETH':
            returned_value = val2
        elif item == 'XRP':
            returned_value = val3
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    return returned_value


# Calcul de la valeur totale du portfeuille
def portfolio_amount():
    open_database()
    sum_request = cursor.execute("SELECT sum(price_purchase) FROM portfolio").fetchall()
    print(sum_request[0][0])
    sum_value = round(sum_request[0][0], 2)
    connection.close()
    return sum_value


# Calcul de l'evolution statistique des cryptos
def cryptos_evolution():
    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    parameters = {
        'slug': 'bitcoin,ethereum,ripple',
        'convert': 'EUR'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'db1037d9-b37a-4dee-8178-238435d0d2b1',
    }

    session = Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters)

    btc_symbol = json.loads(response.text)['data']['1']['symbol']
    eth_symbol = json.loads(response.text)['data']['1027']['symbol']
    xrp_symbol = json.loads(response.text)['data']['52']['symbol']

    btc_slug = json.loads(response.text)['data']['1']['slug']
    eth_slug = json.loads(response.text)['data']['1027']['slug']
    xrp_slug = json.loads(response.text)['data']['52']['slug']

    btc_percent_change_1h = json.loads(response.text)['data']['1']['quote']['EUR']['percent_change_1h']
    eth_percent_change_1h = json.loads(response.text)['data']['1027']['quote']['EUR']['percent_change_1h']
    xrp_percent_change_1h = json.loads(response.text)['data']['52']['quote']['EUR']['percent_change_1h']

    btc_names = f"{btc_symbol}({btc_slug})"
    btc_1h = str(btc_percent_change_1h)
    btc_percent = btc_1h[0:4]

    eth_names = f"{eth_symbol}({eth_slug})"
    eth_1h = str(eth_percent_change_1h)
    eth_percent = eth_1h[0:4]

    xrp_names = f"{xrp_symbol}({xrp_slug})"
    xrp_1h = str(xrp_percent_change_1h)
    xrp_percent = xrp_1h[0:4]

    return [btc_names, btc_percent, eth_names, eth_percent, xrp_names, xrp_percent]


# Creation des entrées dans la table tracking
def tracking_create():
    open_database()
    now = datetime.now()
    day_date = str(now.strftime("%Y-%m-%d %H:%M:%S"))
    print(day_date)
    cursor.execute(
        """INSERT INTO tracking (crypto_name,crypto_code,crypto_price,tracking_date) VALUES ('Bitcoin', 'BTC', '""" +
        tracking_add('BTC') + """', '""" + day_date + """')""").fetchall()
    cursor.execute(
        """INSERT INTO tracking (crypto_name,crypto_code,crypto_price,tracking_date) VALUES ('Ethereum', 'ETH', '""" +
        tracking_add('ETH') + """', '""" + day_date + """')""").fetchall()
    cursor.execute(
        """INSERT INTO tracking (crypto_name,crypto_code,crypto_price,tracking_date) VALUES ('Ripple', 'XRP', '""" +
        tracking_add('XRP') + """', '""" + day_date + """')""").fetchall()
    connection.commit()
    connection.close()


def portfolio_insert(quantity, price_purchase, select_add):
    global val
    open_database()
    now = datetime.now()
    day_date = str(now.strftime("%Y-%m-%d %H:%M:%S"))
    print(day_date)
    a_p = str(round(float(quantity), 2))
    print(a_p)
    portfolio_tracking_id = str(int(select_add))
    print(portfolio_tracking_id)
    print(price_purchase)
    cursor.execute(
        """
        INSERT INTO portfolio (crypto_quantity,date_purchase,price_purchase,portfolio_tracking_id)
        VALUES
        ('""" + a_p + """', '""" + day_date + """', '""" + price_purchase + """', '""" + portfolio_tracking_id + """')
        ON CONFLICT (id_portfolio) DO UPDATE SET portfolio_tracking_id = portfolio_tracking_id + 1
        """).fetchall()
    connection.commit()
    val = 1
    connection.close()
    return val


# Supression dans la table portfolio
def portfolio_remove(quantity, select_remove):
    global val
    #val = 3
    open_database()
    r_p = str(round(float(quantity), 2))
    print(r_p)
    p_i = str(int(select_remove))
    print(p_i)
    c_q = cursor.execute("""SELECT sum(crypto_quantity) FROM portfolio WHERE
    portfolio_tracking_id = '""" + p_i + """'""").fetchall()
    print(c_q[0][0])
    if float(c_q[0][0]) > float(r_p):
        cursor.execute(
            """
            UPDATE portfolio SET crypto_quantity = (crypto_quantity - '""" + r_p + """'),
            price_purchase = (price_purchase - ((price_purchase * '""" + r_p + """') / crypto_quantity))
            WHERE crypto_quantity > '""" + r_p + """' AND portfolio_tracking_id = '""" + p_i + """'""").fetchall()
        connection.commit()
        val = 1
    elif float(c_q[0][0]) == float(r_p):
        #cursor.execute("""DELETE FROM portfolio WHERE portfolio_tracking_id = '""" + p_i + """'""").fetchall()
        val = 2
    else:
        #print("Quantité supérieure au montant disponible")
        val = 3
    connection.commit()
    connection.close()
    return val



global num


# Selectionne le nombre de lignes
def select_tracking_rows(num):
    open_database()
    total_rows = cursor.execute("""SELECT count(*) from tracking""").fetchall()
    print(total_rows[0][0])
    nums = str(num)
    print(nums)
    offset_value = str(total_rows[0][0] - num)
    print(offset_value)
    tab = cursor.execute(
        """SELECT crypto_code, crypto_price, tracking_date from tracking LIMIT '""" + nums
        + """' OFFSET """ + offset_value).fetchall()
    print(tab)
    return tab


# Affiche les lignes groupées
def select_tracking_rows_group(numb):
    open_database()
    total_rows = cursor.execute("""SELECT count(*) from tracking""").fetchall()
    print(total_rows[0][0])
    nums = str(numb)
    print(nums)
    offset_value = str(total_rows[0][0] - numb)
    print(offset_value)
    tab_g = cursor.execute(
        """SELECT crypto_code, crypto_price from tracking GROUP BY crypto_code LIMIT '""" + nums
        + """' OFFSET """ + offset_value).fetchall()
    print(tab_g)
    return tab_g

