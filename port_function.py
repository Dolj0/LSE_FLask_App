
from math import e

from numpy.core.fromnumeric import reshape
from db import Database
import yfinance as yf
import datetime
import investpy
import pandas as pd
import numpy as np
import scipy.optimize as sco


class port_function:
    def __init__(self):
        db = Database('port.db')
        rows= db.fetch()

        tickerlist = []
        for each in rows:
            tickerlist.append(each[1].upper())
        initial_list = list(dict.fromkeys(tickerlist))

        data = yf.download(tickers=initial_list, period="10y", group_by='ticker', auto_adjust = True, interval = "1d")
        
        missing = list(yf.shared._ERRORS.keys())

        returns = pd.DataFrame(index = data.index)
        self.tick = []

        for each in initial_list:
            if each.upper() not in missing:
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
        
    def get_returns(self):
        return(self.returns)

    def get_avg_returns(self):
        return(self.mean_returns)

    def max_sharpe(self):
        max_sharpe = self.max_sharpe_ratio()
        sdp, rp = self.portfolio_annualised_performance(max_sharpe['x'], self.mean_returns, self.cov_matrix)
        sharpe_ratio = (rp-self.risk_free_rate)/sdp
        max_sharpe_allocation = pd.DataFrame(max_sharpe.x, index=self.tick, columns=['allocation'])
        max_sharpe_allocation.allocation = [round(i*100,2) for i in max_sharpe_allocation.allocation]
        max_sharpe_allocation = max_sharpe_allocation.T

        return (max_sharpe_allocation, rp, sdp, sharpe_ratio)

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


    def portfolio_volatility(self, weights, mean_returns, cov_matrix):
        return self.portfolio_annualised_performance(weights, mean_returns, cov_matrix)[0]

    def portfolio_annualised_performance(self, weights, mean_returns, cov_matrix):
        returns = np.sum(mean_returns*weights) * 252
        std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
        return std, returns

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


