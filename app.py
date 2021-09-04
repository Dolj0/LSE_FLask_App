from flask import Flask, render_template, request
from db import Database
from port_function import port_function
import pandas as pd
import datetime

def manage_db(stock):
   db = Database('port.db')
   current_db = populate_df(db)
   print(current_db)
   if stock in current_db[1].values:
      if len(current_db[1]) > 2:
         print(stock + ' is in db')
         all_rows = current_db[current_db[1] == stock]
         first_row = all_rows.iloc[0]
         print(first_row[0])
         db.remove(int(first_row[0]))
      else:
         print("A portfolio cannot consist of less than 2 stocks")
   else:
      print("new stock is not in df")
      db.insert(stock, "%")
      
def gen_portfolio():
   db = Database('port.db')
   portfolios = port_function()
   max_sharpe_allocation, rp, sdp, sharpe_ratio= portfolios.max_sharpe()
   rows = db.fetch()
   for each in rows:
      db.remove(each[0])
   for each in max_sharpe_allocation:
      db.insert(each, max_sharpe_allocation[each]['allocation'])
   db = Database('port.db')
   df = populate_df(db)
   weight_df = pd.DataFrame(df[2].values, index=df[1].values)
   weight_df[0] = weight_df[0].div(100)        
   number_of_holdings = len(df.index)
   past_ret = portfolios.get_returns()
   #Multiplies the past returns of each stock by their weighting in the current portfolio
   returns_df = past_ret.dot(weight_df)
   #Groups the weighted retuns by year and month, and gets the mean return throughout the month
   #Robustness if built into the port_function constructor, the below just recalls it if an error arises (Probobably not best practise)
   try:
      returns_df = returns_df.groupby(by=[returns_df.index.year, returns_df.index.month]).sum()
   except:
      rp, sdp, sharpe_ratio, number_of_holdings, labels, values, labels_pie, values_pie, values_bar = gen_portfolio()
      return rp, sdp, sharpe_ratio, number_of_holdings, labels, values, labels_pie, values_pie, values_bar

   new_index = []
   for each in returns_df.index:
      month = datetime.datetime.strptime(str(each[1]), "%m")
      new_index.append(str(month.strftime("%b")) + " " + str(each[0]))

   rp = ("{:.2f}".format(rp)) 
   sdp = ("{:.2f}".format(sdp)) 
   sharpe_ratio = ("{:.2f}".format(sharpe_ratio))  

   labels = list(new_index)
   values = list(returns_df[0].values)
   
   labels_pie = list(df[1].values)
   values_pie = list(df[2].values)
   values_bar = list(portfolios.get_avg_returns().values)
  
   return rp, sdp, sharpe_ratio, number_of_holdings, labels, values, labels_pie, values_pie, values_bar

def populate_df(db):
   #takes all values from database and puts them into a dataframe

   stock_list = []
   for row in db.fetch():
            stock_list.append(row)
   df = pd.DataFrame(stock_list)
   return df


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])

def home():

   average_returns, volatility, sharpe_ratio, number_of_stocks, labels, values, labels_pie, values_pie, values_bar = gen_portfolio()

   if request.method == 'POST':
      stock = request.form['ticker']
      manage_db(stock)
      average_returns, volatility, sharpe_ratio, number_of_stocks, labels, values, labels_pie, values_pie, values_bar =gen_portfolio()
      return render_template('index.html', average_returns=average_returns, volatility=volatility, sharpe_ratio=sharpe_ratio, number_of_stocks=number_of_stocks, labels=labels, values=values, labels_pie=labels_pie, values_pie=values_pie, values_bar=values_bar)   
   else:
      return render_template('index.html', average_returns=average_returns, volatility=volatility, sharpe_ratio=sharpe_ratio, number_of_stocks=number_of_stocks, labels=labels, values=values, labels_pie=labels_pie, values_pie=values_pie, values_bar=values_bar)
   

if __name__ == '__main__':
   app.run()
