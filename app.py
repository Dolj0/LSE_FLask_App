from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/')
def home():

   average_returns = 4.19
   volatility = 0.59
   sharpe_ratio = 1.01
   number_of_stocks = 4

   labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "leMang"]
   values = [0, 10000, 5000, 15000, 10000, 20000, 15000, 25000, 20000, 30000, 25000, 40000, 34000]

   labels_pie = ["GOOG", "AAPL", "PRAT", "AMZN"]
   values_pie = [30, 30, 15, 25]

   return render_template('index.html', average_returns=average_returns, volatility=volatility, sharpe_ratio=sharpe_ratio, number_of_stocks=number_of_stocks, labels=labels, values=values, labels_pie=labels_pie, values_pie=values_pie)

if __name__ == '__main__':
   app.run()