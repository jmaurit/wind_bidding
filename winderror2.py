#winderror2.py
#question of interest is:
# from perspective of a wind power producer - should they go on the elbas versus leaving any imbalance
#to the regulating market.  
# they go on Elbas or they leave it to the Balancing market??

#

#ipython --pylab

import numpy as np
import matplotlib.pyplot as plt
import sys

import os
import shutil
import csv

os.chdir("/Users/johannesmauritzen/Google Drive/winderror2")

#import data on wind:

def get_balance(capacity): 
	"""return error"""
	balance = np.random.normal(loc=0, scale=capacity/4, size=1)
	sign=balance/abs(balance)
	if abs(balance)>capacity:
		return capacity*sign
	else:
		return balance

def get_spot_price():
	"""returns spot price"""
	return np.random.normal(loc=30, scale=10, size=1)

def get_exp_elbas_price():
	"""returns elbas price"""
	spot_price = get_spot_price()
	return (spot_price + np.random.normal(loc=0, scale=4, size=1))

def get_exp_system_balance():
	"""returns system balance"""
	return np.random.normal(loc=0, scale=300, size=1)

def get_exp_reg_price_up():
	"""returns regulation price - up"""
	spot_price = get_spot_price()
	return spot_price + abs(np.random.normal(loc=0, scale=4, size=1))

def get_exp_reg_price_down():
	"""returns regulation price - down"""
	spot_price = get_spot_price()
	return spot_price - abs(np.random.normal(loc=0, scale=4, size=1))

def get_elbas_transaction_cost():
	return 0.0

def get_theta(balance, capacity):
	return 0.5

class Generator(object):
	#inputs the size, and price data and outputs a market decision
	def __init__(self, capacity):
		self.capacity = capacity

	def ExpectedRevenue(self):
		balance = get_balance(self.capacity)
		price = get_spot_price()
		exp_elbas_price = get_exp_elbas_price()
		exp_reg_price_up = get_exp_reg_price_up()
		exp_reg_price_down = get_exp_reg_price_down()
		elbas_transaction_cost = get_elbas_transaction_cost()

		#theta - probability of positive system imbalance (down-regulation)
		theta = get_theta(balance, self.capacity)
		#expected revenue from balancing market
		if balance > 0.0:
			exp_revenue_bal = theta*exp_reg_price_down*balance + (1.0-theta)*price*balance
		else:
			exp_revenue_bal = theta*price*balance +  (1.0-theta)*exp_reg_price_up*balance 


		#expected revenue from Elbas market
		#Distribution
		exp_revenue_elbas = exp_elbas_price*balance - elbas_transaction_cost

		if exp_revenue_bal > exp_revenue_elbas:
			return {"Market":"Balancing", "revenue": exp_revenue_bal[0]}
		else:
			return {"Market":"Elbas", "revenue":exp_revenue_elbas[0]}

		#return



g1 = Generator(30.0)
elbas_revenue = []
balance_revenue = []

for i in range(1,10000):
	revenue=g1.ExpectedRevenue()
	if revenue["Market"]=="Elbas":
		elbas_revenue.append(revenue["revenue"])
	else:
		balance_revenue.append(revenue["revenue"])
		
plt.hist(elbas_revenue, bins=100, label="Elbas Trade")
plt.hist(balance_revenue, bins= 100, label="Balancing Market Trade")
plt.legend()
plt.xlabel("Value of Trade")
plt.ylabel("Trades")
plt.title("Uncorrelated Balance")
plt.ylim([0,400])
plt.savefig("figures/elbas_model_a")


