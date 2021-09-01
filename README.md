# LSE_FLask_App
Python Flask based web app using Chart.js dashboard displaying an efficient financial portfolio.
Stock tickers can be added and removed from the portfolio, and a new efficient portfolio will be calculated using Harry Markowitz's efficient frontier method.

# Extending the LSE_App
This is an extension to the LSE_App based on the tkinter gui package. I have patched the backend python from that program into a new GUI using the python flask package.
The new gui uses uses CSS, HTML and chart.js. Using this tech stack provides a more sophisticated and clean GUI than tKinter. 

#inverno
The gui was heavily inspired by the https://github.com/werew/inverno.
Whilst inverno produces a static file that presents stock data entered with a .csv file, LSE_Flask_App is designed to give advice on stock weightings given a set of tickers.

#improvements
Addition of a login system would theoretically enable the program to be used as a real-world webpage. 

