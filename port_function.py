
from math import e
from tkinter import messagebox
from numpy.core.fromnumeric import reshape
from db import Database
import yfinance as yf
import datetime
import investpy
import pandas as pd
import numpy as np
import scipy.optimize as sco
import matplotlib.pyplot as plt

class port_function:
    def __init__(self):
        db = Database('port.db')
        rows= db.fetch()
        tickerlist = []
        for each in rows:
            tickerlist.append(each[1])
        initial_list = list(dict.fromkeys(tickerlist))
        data = yf.download(tickers=initial_list, period="10y", group_by='ticker', auto_adjust = True, interval = "1d")
        
        missing = list(yf.shared._ERRORS.keys())
        missing_str =  "\n".join(str(x) for x in missing)
        if missing:
            messagebox.showerror("Required Fields", f'No data found for following tickers: {missing_str}')
        returns = pd.DataFrame(index = data.index)
        self.tick = []
        for each in initial_list:
            if each not in missing:
                self.tick.append(each)
        for each in self.tick:
                returns[each]=data[each]["Close"].pct_change()

        self.returns = returns
        self.mean_returns = returns.mean()
        self.cov_matrix = returns.cov()
        self.risk_free_rate = self.risk_free()

    #Get risk free
    def risk_free(self):    
        ten_year = datetime.datetime.now() - datetime.timedelta(days=10*365)
        ten_year_date = str(ten_year.strftime('%d/%m/%Y'))
        today = str(datetime.datetime.now().strftime('%d/%m/%Y'))
        search_result=investpy.bonds.get_bond_historical_data(bond="U.K. 3M", from_date=ten_year_date, to_date=today, interval="Monthly")
        search_result["Close%"] = search_result["Close"]/100
        risk_free_rate = search_result["Close%"].mean()/12
        return risk_free_rate

    def ftse_stats(self):
        ftse = yf.download(tickers="^FTSE", period="10y", auto_adjust=True, interval="1d")
        returns = ftse["Close"].pct_change()
        returns = returns*100
        mean_ftse_returns = returns.mean()
        std_ftse_returns = returns.std()
        
        return(mean_ftse_returns, std_ftse_returns)
        



    def max_sharpe(self):
        max_sharpe = self.max_sharpe_ratio()
        sdp, rp = self.portfolio_annualised_performance(max_sharpe['x'], self.mean_returns, self.cov_matrix)
        sharpe_ratio = (rp-self.risk_free_rate)/sdp
        max_sharpe_allocation = pd.DataFrame(max_sharpe.x, index=self.tick, columns=['allocation'])
        max_sharpe_allocation.allocation = [round(i*100,2) for i in max_sharpe_allocation.allocation]
        max_sharpe_allocation = max_sharpe_allocation.T

        return (max_sharpe_allocation, rp, sdp, sharpe_ratio)
          
    def min_vol(self):
        min_vol = self.min_variance()
        sdp_min, rp_min = self.portfolio_annualised_performance(min_vol['x'], self.mean_returns, self.cov_matrix)
        sharpe_ratio_min = (rp_min-self.risk_free_rate)/sdp_min
        min_vol_allocation = pd.DataFrame(min_vol.x, index=self.tick, columns=['allocation'])
        min_vol_allocation.allocation = [round(i*100,2) for i in min_vol_allocation.allocation]
        min_vol_allocation = min_vol_allocation.T

        return (min_vol_allocation, rp_min, sdp_min, sharpe_ratio_min)

    def max_sharpe_ratio(self):
        num_assets = len(self.mean_returns)
        args = (self.mean_returns, self.cov_matrix, self.risk_free_rate)
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) -1 })
        bound = (0.0,1.0)
        bounds = tuple(bound for asset in range(num_assets))
        result = sco.minimize(self.neg_sharpe_ratio, num_assets*[1./num_assets,], args=args,
                        method='SLSQP', bounds=bounds, constraints=constraints)
        return result

    def neg_sharpe_ratio(self, weights, mean_returns, cov_matrix, risk_free_rate):
        p_var, p_ret = self.portfolio_annualised_performance(weights, mean_returns, cov_matrix)
        return -(p_ret - risk_free_rate)/p_var

    def min_variance(self):
        num_assets = len(self.mean_returns)
        args = (self.mean_returns, self.cov_matrix)
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bound = (0.0, 1.0)
        bounds = tuple(bound for asset in range(num_assets))
        result = sco.minimize(self.portfolio_volatility, num_assets*[1./num_assets], args=args,
                            method='SLSQP', bounds=bounds, constraints=constraints)
        return result

    def portfolio_volatility(self, weights, mean_returns, cov_matrix):
        return self.portfolio_annualised_performance(weights, mean_returns, cov_matrix)[0]

    def portfolio_annualised_performance(self, weights, mean_returns, cov_matrix):
        returns = np.sum(mean_returns*weights) * 252
        std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
        return std, returns

    def get_ef(self):
        max_sharpe_allocation, rp, sdp, sharpe_ratio = self.max_sharpe()
        min_vol_allocation, rp_min, sdp_min, sharpe_ratio_min = self.min_vol()
        an_vol = np.std(self.returns) * np.sqrt(252)
        an_rt = self.mean_returns * 252
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.scatter(an_vol,an_rt,marker='o',s=200)

        for i, txt in enumerate(self.tick):
            ax.annotate(txt, (an_vol[i],an_rt[i]), xytext=(10,0), textcoords='offset points')
        ax.scatter(sdp,rp,marker='*',color='r',s=500, label='Maximum Sharpe ratio')
        ax.scatter(sdp_min,rp_min,marker='*',color='g',s=500, label='Minimum volatility')

        target = np.linspace(rp_min, 0.34, 50)
        efficient_portfolios = self.efficient_frontier(self.mean_returns, self.cov_matrix, target)
        ax.plot([p['fun'] for p in efficient_portfolios], target, linestyle='-.', color='black', label='efficient frontier')

        x_vals = np.array(ax.get_xlim())
        y_vals = self.risk_free_rate + sharpe_ratio*x_vals
        ax.plot(x_vals, y_vals, linestyle='-', color='red', label='CAL')

        ax.set_title('Portfolio Optimization with Individual Stocks')
        ax.set_xlabel('annualised volatility')
        ax.set_ylabel('annualised returns')
        ax.legend(labelspacing=0.8)
        fig.savefig('portfolio.png', dpi=fig.dpi)

    def efficient_frontier(self, mean_returns, cov_matrix, returns_range):
        efficients = []
        for ret in returns_range:
            efficients.append(self.efficient_return(mean_returns, cov_matrix, ret))
        return efficients
    
    def efficient_return(self, mean_returns, cov_matrix, target):
        num_assets = len(mean_returns)
        args = (mean_returns, cov_matrix)

        def portfolio_return(weights):
            return self.portfolio_annualised_performance(weights, mean_returns, cov_matrix)[1]

        constraints = ({'type': 'eq', 'fun': lambda x: portfolio_return(x) - target},
                    {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0,1) for asset in range(num_assets))
        result = sco.minimize(self.portfolio_volatility, num_assets*[1./num_assets,], args=args, method='SLSQP', bounds=bounds, constraints=constraints)
        return result


