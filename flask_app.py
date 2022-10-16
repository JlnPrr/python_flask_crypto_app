from flask import Flask, render_template, redirect, request, flash
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import time


app = Flask(__name__)
app.secret_key = "+gT'xv^3t+U*7>K9$U7=h)qQ;Zb>Gs"


# ROUTES
# Affiche la page index
@app.route('/', methods=['POST', 'GET'])
def index():
    from config import portfolio_amount
    from config import cryptos_evolution

    portfolio_sum = portfolio_amount()
    evolutions = cryptos_evolution()
    return render_template('index.html', amount=str(portfolio_sum),
                           btc_names=evolutions[0], btc_percent=evolutions[1],
                           eth_names=evolutions[2], eth_percent=evolutions[3],
                           xrp_names=evolutions[4], xrp_percent=evolutions[5],)


# Affiche la page add
@app.route('/add', methods=['POST', 'GET'])
def add():
    global val1
    val1 = 3
    if request.method == 'POST':
        select_add = request.form.get('select_add')
        quantity = request.form.get('quantity')
        price = request.form.get('price')
        print(select_add)
        print(quantity)
        print(price)
        if select_add == 'Bitcoin':
            select_add = 1
        elif select_add == "Ethereum":
            select_add = 2
        elif select_add == "Ripple":
            select_add = 3
        from config import portfolio_insert
        val1 = portfolio_insert(quantity, price, select_add)
    if val1 == 1:
        flash("Transaction réussie")
    elif val1 == 2:
        flash("Transaction impossible")
    else:
        flash("Remplisser les champs puis Validez")
    return render_template('add.html')


# Affiche la page remove
@app.route('/remove', methods=['POST', 'GET'])
def remove():
    global val2
    val2 = 3
    if request.method == 'POST':
        select_remove = request.form.get('select_remove')
        quantity = request.form.get('amount_remove')
        print(select_remove)
        print(quantity)
        if select_remove == 'Bitcoin':
            select_remove = 1
        elif select_remove == "Ethereum":
            select_remove = 2
        elif select_remove == "Ripple":
            select_remove = 3
        from config import portfolio_remove
        val2 = portfolio_remove(quantity, select_remove)
    if val2 == 1:
        flash("Transaction réussie")
    elif val2 == 2:
        flash("Transaction impossible")
    else:
        flash("Remplisser les champs puis Validez")
    return render_template('remove.html')


# Affiche la page graph
@app.route('/graph')
def graph():
    # from config import graph_insert
    # graph_insert()
    return render_template('graph.html')


#if __name__ == '__main__':
 #   app.run(debug=True)

