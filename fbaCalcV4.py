#FBA Profit Calc V4
#By: Nicholas Hershy

#Total Amazon Fees estimated to 30%
AMZN_FEES = 0.30 #constant

class MoneyObject:
	#----------starting attributes-----------
	#wholesaleCostPerItem: float 
	#quantityBulkBuy: float
	#wholesaleShipping: float
	#retailPrice: float
	#monthlySoftwareFee: float
	#monthlyMarketingCosts: float
	#avgSalesMonth: float
	#------------static attributes-------------
	#costPerUnit: float
	#profitPerUnit: float
	#profitMargin: float
	#monthlyRevenue: float
	#monthlyCost: float
	#monthlyProfit: float
	#initialSunkenCost: float
	#daysWillLast: float
	#monthsWillLast: float
	#-------------dynamic attributes--------------
	#monthCounter: int
	#daysCounter: int
	#accumulatedDebt: float
	#walkAwayProfit: float
	#ROI: float (ROI = (Net Profit / Cost of Investment) x 100)
	#adjustedWalkAwayProfit: float #this adjusts if negative walk-away profit occurs
	#-------------constructor--------------------------
	def __init__(self, wholesaleCostPerItem, quantityBulkBuy, wholesaleShipping, retailPrice, monthlySoftwareFee, monthlyMarketingCosts, avgSalesMonth):
		self.wholesaleCostPerItem = wholesaleCostPerItem
		self.quantityBulkBuy = quantityBulkBuy
		self.wholesaleShipping = wholesaleShipping
		self.retailPrice = retailPrice
		self.monthlySoftwareFee = monthlySoftwareFee
		self.monthlyMarketingCosts = monthlyMarketingCosts
		self.avgSalesMonth = avgSalesMonth
		#---------------calc static values---------------------------------
		self.amznFeePercentage = AMZN_FEES
		self.costPerUnit = (self.wholesaleCostPerItem) + (self.wholesaleShipping / self.quantityBulkBuy)
		self.profitPerUnit = self.retailPrice - self.costPerUnit
		self.profitMargin = self.profitPerUnit / self.costPerUnit * 100
		self.monthlyRevenue = self.retailPrice * self.avgSalesMonth
		self.monthlyCost = (self.monthlyRevenue * self.amznFeePercentage) + self.monthlySoftwareFee + self.monthlyMarketingCosts
		self.monthlyProfit = self.monthlyRevenue - self.monthlyCost
		self.initialSunkenCost = (self.wholesaleCostPerItem * self.quantityBulkBuy) + self.wholesaleShipping
		self.daysWillLast = self.quantityBulkBuy / self.avgSalesMonth * 30.0
		self.monthsWillLast = self.daysWillLast / 30.0
		#----------------- set other attributes--------------------------
		self.monthCounter = 0
		self.daysCounter = int(self.daysWillLast)
		self.accumulatedDebt = self.initialSunkenCost
		self.partialMonthlyPercentage = 0.0
		self.walkAwayProfit = 0.0
		self.ROI = 0.0
		self.adjustedWalkAwayProfit = 0.0
	#-------------------print static values--------------------------
	def print_static_vals(self):
		print("------------------------------------")
		print("Profit margin: ", str(round(self.profitMargin,2)), '%')
		print("Cost per item: ", str(round(self.costPerUnit,2)))
		print("Profit per item: ", str(round(self.profitPerUnit,2)))
		print("Monthly cost: ", str(round(self.monthlyCost,2)))
		print("Monthly revenue: ", str(round(self.monthlyRevenue,2)))
		print("Monthly profit: ", str(round(self.monthlyProfit,2)))
		print("Initial sunken cost: ", str(round(self.initialSunkenCost,2)))
		print("Days bulk buy will last: ", str(round(self.daysWillLast,2)))
		print("Months bulk buy will last: ", str(round(self.monthsWillLast,2)))
		print("------------------------------------")
	#------------calculate values for partial month----------------------
	def partial_month_calc(self):
		print(" (PARTIAL month of ", self.daysCounter, " days)")
		self.partialMonthlyPercentage = float(self.daysCounter) / 30.0
		self.accumulatedDebt += (self.monthlySoftwareFee + self.monthlyMarketingCosts) * self.partialMonthlyPercentage
		self.accumulatedDebt -= (self.monthlyProfit * self.partialMonthlyPercentage)
		self.daysCounter = 0
	#-------------calc values for full month ---------------------------
	def full_month_calc(self):
		self.daysCounter -= 30
		self.accumulatedDebt += (self.monthlySoftwareFee + self.monthlyMarketingCosts)
		self.accumulatedDebt -= self.monthlyProfit
	#----------------calc end of each month totals--------------------------
	def calc_end_of_month(self):
		if self.accumulatedDebt > 0:
			print(" LOST ", str(round(self.accumulatedDebt,2)), "this month")
		else:
			print(" EARNED ", str(round((self.accumulatedDebt * -1.0),2)), "this month")
			self.walkAwayProfit += (self.accumulatedDebt * -1.0)
			self.accumulatedDebt = 0.0 #zero out the debt once it has been paid off
	#------------------run monthly simulation--------------------------
	def run_monthly_simulation(self):
		while self.daysCounter > 0:
			self.monthCounter += 1
			print("******** MONTH ", self.monthCounter, "  ESTIMATES ********")
			if self.daysCounter < 30: #if partial month
				self.partial_month_calc()
			else:
				self.full_month_calc()
			self.calc_end_of_month()
	#-----------------if made money or lost money---------------------
	def if_made_or_lost(self):
		if self.walkAwayProfit == 0:
			return (self.accumulatedDebt * -1.0)
		else:
			return self.walkAwayProfit
	#--------------------calc ROI ---------------------------------------
	def calc_ROI(self):
		#ROI = (Net Profit / Cost of Investment) x 100
		self.ROI = (self.if_made_or_lost() / self.initialSunkenCost) * 100
	#------------calc ROI and walkAwayProfit after simulation completed-------------
	def calc_final_values(self):
		self.calc_ROI()
		self.adjustedWalkAwayProfit = self.if_made_or_lost()
	#------------------print final results------------------------------
	def print_final_results(self):
		perMonth = self.adjustedWalkAwayProfit / self.monthsWillLast
		print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
		print(" ROI: ", str(round(self.ROI,2)), "%")
		print(" Walk-Away Profit: ", str(round(self.adjustedWalkAwayProfit,2)))
		print(" An average of ", str(round(perMonth,2)), "was made per month")

#-----------------gathering inputs-------------------------
#initial sunken costs
wholesaleCostPerItem = float(input("Wholesale cost per item: "))
quantityBulkBuy = float(input("Total quantity (# units bought) of bulk buy: "))
wholesaleShipping = float(input("Wholesale shipping cost (per bulk buy): "))
#estimated retail selling price
retailPrice = float(input("Estimated retail selling price per item: "))
#other monthly fees
monthlySoftwareFee = float(input("Monthly software fee: "))
monthlyMarketingCosts = float(input("Estimated monthly marketing fees: "))
#estimated sales per month
avgSalesMonth = float(input("Est./avg. sales per month: "))
#--------------------------------------------------------------

#--------------instantiate MoneyObject-----------------
moneyObj = MoneyObject(wholesaleCostPerItem, quantityBulkBuy, wholesaleShipping, retailPrice, monthlySoftwareFee, monthlyMarketingCosts, avgSalesMonth)

moneyObj.print_static_vals()
moneyObj.run_monthly_simulation()
moneyObj.calc_final_values()
moneyObj.print_final_results()