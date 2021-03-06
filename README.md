# LSE_FLask_App
this program is a flask based app using a Chart.js dashboard which displays a financial portfolio.
Stock tickers can be added and removed from the portfolio, and a new efficient portfolio will be calculated using Harry Markowitz's efficient frontier method.

## Extending the LSE_App
This is an extension to the LSE_App which is based on the tkinter gui package. I have patched the backend python from that program into a new GUI using the python flask package.
The new GUI uses uses CSS, HTML and chart.js. Using this tech stack provides a more sophisticated and clean result than that of tKinter. 

## Inverno
My GUI was inspired by Inverno --> https://github.com/werew/inverno.
Whilst inverno produces a HTML file that presents stock data entered with a .csv file, LSE_Flask_App is a CRUD web application designed to give advice on stock weightings given a set of tickers.

## Example

![GitHub Logo](https://github.com/Dolj0/LSE_FLask_App/blob/main/Efficient%20Portfolio%20Example.png)

## Future Recommendations
* Addition of a login system would theoretically enable the program to be used as a real-world webapp. 
* This app could be added to the Inverno app to provide the dashboard with portfolio recommendations.

