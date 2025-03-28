"""
Copyright 2020 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""

import datetime
from enum import Enum
from typing import Union, Optional

import pandas as pd
from pandas import Series

from gs_quant.data import DataContext, Dataset
from gs_quant.errors import MqValueError
from gs_quant.markets.securities import AssetIdentifier, Asset
from gs_quant.target.common import AssetClass, AssetType
from gs_quant.timeseries import RelativeDate
from gs_quant.timeseries.helper import plot_measure
from gs_quant.timeseries.measures import ExtendedSeries


class EstimateItem(Enum):
    EPS = 'Earnings Per Share'
    EPS_C = 'Consolidated EPS'
    EPS_P = 'Standalone Earnings Per Share'
    SALES = 'Sales'
    SALES_C = 'Consolidated Sales'
    SALES_P = 'Standalone Sales'
    DPS = 'Declared Dividends Per Share'
    CFPS = 'Cash Flow Per Share'
    PRICE_TGT = 'Target Price'
    EPS_LTG = 'Long Term Growth'
    AFFO = 'Adjusted Funds From Operations'
    ASSETS = 'Total Assets'
    BFNG = 'Net Income Reported'
    BPS = 'Book Value Per Share'
    BPS_TANG = 'Tangible Book Value Per Share'
    CAPEX = 'Capital Expenditure'
    CF_FIN = 'Cash Flow From Financing'
    CF_INV = 'Cash Flow From Investing'
    CF_OP = 'Cash Flow From Operations'
    CURRENT_ASSETS = 'Current Assets'
    CURRENT_LIABILITIES = 'Current Liabilities'
    DEFREVENUE_LT = 'Deferred Revenue Long Term'
    DEFREVENUE_ST = 'Deferred Revenue Short Term'
    DEP_AMORT = 'Depreciation and Amortization'
    EBIT = 'EBIT'
    EBIT_ADJ = 'BEIT Adjusted'
    EBIT_C = 'Consolidated EBIT'
    EBIT_P = 'Standalone EBIT'
    EBITA = 'EBITA'
    EBITDA = 'EBITDA'
    EBITDA_ADJ = 'EBITDA Adjusted'
    EBITDA_REP = 'EBITDA Reported'
    EBITDAR = 'EBITDAR'
    EBITR = 'EBIT Reported'
    EPS_EX_XORD = 'Earnings Per Share Excluding Exceptionals'
    EPS_GAAP = 'Reported Earnings Per Share'
    EPS_NONGAAP = 'Earnings Per Share Non GAAP'
    EPSAD = 'Diluted Adjusted EPS'
    EPSRD = 'Diluted Reported EPS'
    FCF = 'Free Cash Flow'
    FCFPS = 'Free Cash Flow Per Share'
    FFO = 'Funds From Operations'
    G_A_EXP = 'General and Administrative Expense'
    GW_TOT = 'Total Goodwill'
    HEPSB = 'Headline Basic EPS'
    HEPSD = 'Headline Diluted EPS'
    INC_GROSS = 'Gross Income'
    INT_EXP = 'Interest Expense'
    INVENTORIES = 'Inventories'
    MAINT_CAPEX = 'Maintenance CAPEX'
    NDT = 'Net Debt'
    NET = 'Net Profit'
    NET_C = 'Consolidated Net Income'
    NET_P = 'Standalone Net Income'
    NET_SALES = 'Net Sales'
    NETBG = 'Net Profit Adjusted'
    ORGANICGROWTH = 'Organic Growth'
    PTI = 'Pre Tax Profit'
    PTI_C = 'Consolidated Pretax Income'
    PTIAG = 'Pre Tax Profit Reported'
    PTP_P = 'Standalone Pretax Income'
    PTPA = 'Pre Tax Income Adjusted'
    RD_EXP = 'Research and Development'
    REV_TOT = 'Total Revenues'
    S_M_EXP = 'Selling and Marketing Expense'
    SGA = 'Selling, General and Administrative Expense'
    SH_EQUITY = 'Shareholders Equity'
    SOE = 'Stock Option Expense'
    TAX_EXPENSE = 'Tax Expense'
    TOTAL_DEBT = 'Total Debt'


class EstimateStatistic(Enum):
    MEAN = 'Mean'
    MEDIAN = 'Median'
    HIGH = 'High'
    LOW = 'Low'
    ACTUAL = 'Actual'


class EstimateBasis(Enum):
    ANN = 'Annual'
    QTR = 'Quarterly'
    SEMI = 'Semi annual'
    NTM = 'Next Twelve Months'
    STM = 'Second Twelve Months'


class FundamentalBasis(Enum):  # todo: add LTM as a choice and routing logic to LTM global datasets
    ANN = 'Annual'
    QTR = 'Quarterly'
    SEMI = 'Semi annual'


class FundamentalBasicItem(Enum):
    SALES = "Sales/Revenue"
    NON_INT_INC = "Non Interest Income"
    OPER_EXP_OTH = "Other Operating Expense"
    OPER_INC = "Operating Income"
    LOAN_LOSS_PROV = "Loan Loss Provision"
    PTX_XORD_CHRG = "Extraordinary Charge Pretax"
    PTX_INC = "Pretax Income"
    MIN_INT_EXP = "Minority Interest Expense"
    NET_INCOME = "Net Income (incl. Discontinued Operations)"
    CASH_ST = "Cash & Short Term Investments"
    CASH_DUE_FR_BK = "Total Cash & Due from Banks"
    PREM_RECEIV = "Premium Balance Receivables"
    INVEN = "Inventories"
    ASSETS_OTH_INTANG = "Other Assets"
    ASSETS = "Total Assets"
    LIABS_CURR = "Total Current Liabilities"
    PAY_ACCT = "Accounts Payable"
    INS_LIABS_POL = "Insurance Policy Liabilities (Insurance)"
    PROV_RISK = "Provision for Risks & Charges"
    LIABS_XMIN_INT_ACCUM = "Liabilities (excl. Minority Interest)"
    COM_EQ = "Common Equity (Total)"
    DEBT_LT_CONV = "Convertible Debt"
    TIER1_CAP = "Tier 1 Capital"
    INT_PAY = "Interest Payable"
    SECS_INVEST = "Investment Securities"
    DEP_EXP_CF = "Depreciation Depletion & Amortization (Cash Flow)"
    NON_CASH = "Other Funds"
    XORD_CF = "Extraordinary Item"
    ACQ_BUS_CF = "Net Assets from Acquisitions"
    LOAN_DECR_CF = "Decrease in Loans"
    INVEST_ACTIV_CF = "Investing Activities Other Uses"
    DIV_CF = "Cash Dividends Paid"
    DEPS_INCR_CF = "Increase in Deposits"
    CHG_CASH_CF = "Net Change in Cash"
    EBIT_OPER_PS = "Operating Profit Per Share"
    BPS = "Book Value Per Share"
    COM_SHS_OUT_EPS_DIL = "Common Shares Used to Calculate EPS Fully Diluted"
    PRICE_CLOSE_FP = "Market Price Fiscal Period Close"
    ACTG_STANDARD = "Code indicating the accounting standards that the company follows"
    CONSOL_NET_INC = "Consolidated Net Income"
    INCR_FED_HOME_ADV_CF = "Federal Home Loan Advances Increase (Decrease)"
    COM_SHS_OUT_EPS = "Common Shares Used to Calculate EPS"
    NOTES_RECEIV_LT = "Long Term Note Receivable"
    DFD_TAX = "Deferred Taxes"
    LIABS_SHLDRS_EQ = "Liabilities & Stockholders' Equity Total"
    INVEST_AFF = "Investment in Unconsolidated Subsidiaries"
    INVEST_RE = "Real Estate Assets"
    RSRV_NONEQ = "Non Equity Reserves"
    RECEIV_ST = "Total Accounts Receivable"
    DPS_GROSS = "Dividends Per Share Gross"
    RSRV_CHG = "Reserves Increase (Decrease)"
    DFD_TAX_CR = "Deferred Tax Liabilities"
    COM_EQ_RETAIN_EARN = "Retained Earnings"
    INVEN_LIFO = "Inventories LIFO Reserve"
    LOAN_CHG_CF = "Proceeds from Loans"
    DEP_CHG_CF = "Change in Deposits"
    DPS_ALL = "Dividends Per Share Normal, Extra, and Special Dividends"
    MISC_NET_OTH = "Other After Tax Income (Expense)"
    INT_INC = "Interest Income"
    GROSS_INC = "Gross Income"
    OPER_EXP_TOT = "Operating Expenses Total"
    INT_EXP_TOT = "Total Interest Expense Banks"
    NON_INT_EXP = "Non Interest Expense"
    PTX_XORD_CR = "Extraordinary Credit Pretax"
    INC_TAX = "Income Taxes"
    EQ_AFF_INC = "Equity in Earnings of Affiliates"
    DIV_PFD = "Preferred Dividends"
    CASH_ONLY = "Cash Only"
    BK_INVEST_TOT = "Total Investments Banks"
    RECEIV_TOT = "Total Accounts Receivable"
    ASSETS_CURR = "Total Current Assets"
    INTANG = "Intangible Assets"
    DEPS = "Total Deposits"
    DEBT_ST = "Short Term Debt (incl. Current Portion of LTD)"
    ACCR_EXP_XPAYR = "Accrued Expenses (Excl. Accrued Payroll)"
    DEBT_LT = "Long Term Debt"
    DFD_TAX_ITC = "Deferred Taxes"
    PFD_STK = "Preferred Stock Carrying Value"
    DEBT = "Total Debt"
    SHLDRS_EQ = "Total Shareholders' Equity"
    TIER2_CAP = "Tier 2 Capital"
    SECS_CUSTODY = "Securities In Custody"
    NET_INC_CF = "Net Income (Cash Flow)"
    DFD_TAX_CF = "Deferred Taxes & Investment Tax Credit"
    FUNDS_OPER_GROSS = "Funds from Operations"
    WKCAP_CHG = "Changes in Working Capital"
    LOAN_INCR_CF = "Increase in Loans"
    SALE_ASSETS_BUS_CF = "Sale of Fixed Assets & Businesses"
    INVEST_SOURCES_CF = "Investing Activities Other Sources"
    DEPS_DECR_CF = "Decrease in Deposits"
    FOR_EXCH_CF = "Exchange Rate Effect"
    DPS = "Dividends Per Share"
    EPS_REPORTED = "Earnings Per Share As Reported"
    COM_SHS_OUT_EPS_BASIC = "Common Shares Used to Calculate EPS Basic"
    COM_SHS_OUT = "Common Shares Outstanding"
    INVEST_YLD_5YAVG = "Yield On Investment 5 Year Average"
    FY_LENGTH_DAYS = "Fiscal Period Length Days"
    EQ_TOT = "Total Equity"
    EPS_BASIC = "EPS Basic Before Extraordinaries"
    EXP_TOT = "Total Expense"
    PAY_TAX = "Income Tax Payable"
    MIN_INT_ACCUM = "Accumulated Minority Interest Total"
    LOAN_NET = "Net Loans"
    CUST_ACCEPT = "Customer Liability on Acceptances"
    PPE_NET = "Net Property Plant & Equipment"
    DEPS_CUST = "Total Customer Deposits"
    ADJ_NET_OTH = "Other After Tax Adjustments"
    DIV_PAY_OUT_PS = "Dividend Payout Per Share"
    DFD_TAX_DB = "Deferred Tax Assets"
    RECEIV_INT = "Interest Receivables"
    CASH_RESTR = "Restricted Cash"
    RENT_INC = "Rental Income"
    INVEST_ACTIV_OTH = "Other Funds"
    ASSETS_NONPERF = "Total Non Performing Assets"
    BK_COM_EQ_TIER1_TOT = "Common Equity Tier 1 Total"


class FundamentalBasicDerivedItem(Enum):
    COGS = "Cost of Goods Sold (COGS) including Depreciation & Amortization"
    INT_EXP_NET = "Interest Expense"
    NET_INC_BASIC = "Net Income Avail to Common Basic"
    NON_OPER_INC = "Non Operating Income (Expense)"
    SGA_OTH_EXP = "Selling, General & Admin. Expense & Other"
    OPER_INC_AFT_INT = "Operating Income After Interest Expense"
    ASSETS_CURR_OTH = "Other Current Assets"
    ASSETS_OTH = "Tangible Other Assets"
    LIABS = "Total Liabilities"
    CAPEX = "Capital Expenditures (Total)"
    INVEST_USES_CF = "Other Uses"
    STK_CHG_CF = "Change in Capital Stock"
    FIN_ACTIV_OTH_CF = "Other Funds"
    MISC_FUNDS_CF = "Miscellaneous Funds"
    EPS_DIL_BEF_UNUSUAL = "EPS Diluted Before Unusual Expense"
    COM_EQ_ASSETS = "Common Equity % Total Assets"
    DEBT_ASSETS = "Total Debt % Total Assets"
    GROSS_MGN = "Gross Profit Margin"
    NET_MGN = "Net Margin"
    PAY_OUT_RATIO = "Dividend Payout (% Earnings) Total Dollar"
    ROA = "Return On Average Assets"
    ROTC = "Return On Average Total Capital"
    NET_DEBT = "Net Debt"
    INT_INC_NET = "Net Interest Income"
    TURN_RATE = "Turnover Rate"
    EPS_DIL = "EPS Fully Diluted"
    LIABS_CURR_OTH = "Other Current Liabilities"
    PBK = "Price To Book Value Closing Price As Of Last Trading Day"
    PE = "Price To Earnings Closing Price As Of Fiscal Period End"
    EBIT_OPER = "EBIT (Operating Income)"
    ENTRPR_VAL = "Enterprise Value Using Diluted Shares"
    FREE_CF_MINUS_DIV = "Free Cash Flow to Equity Minus Dividends"
    EARN_PERST = "Earnings Persistence"
    UNUSUAL_EXP = "Unusual Expense"
    NET_INC = "Net Income"
    INT_INC_AFT_PROV = "Net Interest Income after Loan Loss Provision"
    LOSS_CLAIM_RSRV = "Losses, Claims & Reserves"
    OPER_INC_BEF_INT = "Operating Income Before Interest Expense"
    ASSET_TURN = "Asset Turnover"
    INVEST_ADV = "Total Investments and Advances"
    LIABS_OTH = "Other Liabilities"
    OPER_CF = "Net Operating Cash Flow"
    INVEST_PURCH_SALE_CF = "Purchase/Sale of Investments"
    INVEST_CF = "Net Investing Cash Flow"
    DEBT_CF = "Issuance/Reduction of Debt, Net"
    FIN_CF = "Net Financing Cash Flow"
    FREE_CF_FCFE = "Free Cash Flow to Equity"
    CAPEX_SALES = "Capital Expenditure % Total Sales"
    CURR_RATIO = "Current Ratio"
    EBITDA_OPER = "EBITDA"
    MKT_VAL = "Market Value using Period End Price"
    OPER_MGN = "Operating Margin"
    QUICK_RATIO = "Quick Ratio"
    ROE = "Return On Average Total Equity"
    TCAP = "Total Capital"
    PTX_MGN = "Pretax Margin"
    INT_MGN = "Net Interest Margin"
    BPS_TANG = "Book Value Per Share Tangible"
    SGA = "Selling, General & Administrative Expense"
    SALES_PS = "Sales Per Share"
    PCF = "Price to Cash Flow Ratio Closing Price as of Fiscal Period End"
    PSALES = "Price To Sales Closing Price As Of Last Trading Day"
    NET_INC_AFT_XORD = "Net Income After Extraordinary Items"


class FundamentalAdvancedItem(Enum):
    ACCR_EXP_CF = "Other Accruals"
    AMORT_CF = "Amortization of Intangible Assets"
    AMORT_INTANG = "Amortization of Intangibles"
    ASSETS_OTH_TANG = "Tangible Other Assets"
    AUD_FEES = "Auditor Fees"
    BONDS_BELOW_INVGR = "Bonds Below Investment Grade"
    COM_EQ_APIC = "Additional Paid In Capital / Capital Surplus (incl. Deferred Compensation)"
    COM_EQ_GL = "Unrealized Gain/Loss Marketable Securities"
    COM_EQ_OTH_COMPR_ADJ_OTH = "Accumulated Other Comp Income Other Adjustments"
    COM_EQ_UNEARN_COMP = "Comprehensive Income Unearned Compensation"
    COM_SHS_OUT_SECS = "Common Shares Outstanding Security"
    COM_SHS_TRADE_WK = "Common Shares Traded Weekly"
    COMMISS_INC = "Commission & Fee Income"
    CURN_DOC = "Code representing the currency in which the company's financial statements are presented"
    DEBT_LT_NON_CONV = "Non Convertible Debt"
    DEP_EXP = "Depreciation"
    DEP_EXP_XAMORT_CF = "Depreciation/Depletion (excl. Amortization)"
    DEPS_FOR = "Foreign Office Deposits"
    DEPS_UNSPEC = "Unspecified Deposits"
    DFD_TAX_ASSETS_ST = "Deferred Income Tax Current Asset"
    DISC_OPER_INC = "Discontinued Operations"
    DIV_PFD_CF = "Preferred Dividends (Cash Flow)"
    DPS_SECS = "Dividends Per Share Security"
    EPS = "Earnings Per Share Fiscal Period"
    EPS_CONTIN_OPER = "Earnings Per Share from Continuing Operations Fiscal"
    EPS_SECS = "Earnings Per Share Security"
    EPS_XORD = "Earnings Per Share incl. Extraordinary Items Fiscal"
    FED_FUNDS = "Federal Funds Sold"
    FOR_EXCH_BS = "Exchange Rate Used For Translating Balance Sheet"
    FOR_EXCH_IS = "Exchange Rate used for Translating Income Statement & Cash Flow"
    GW = "Net Goodwill"
    GW_GROSS = "Goodwill Gross"
    INC_TAX_CURR_FOR = "Income Tax Current Foreign"
    INC_TAX_DFD_FOR = "Income Tax Deferred Foreign"
    INS_INVEST_INC = "Total Investment Income (Insurance)"
    INS_LIABS_OTH = "Other Insurance Liabilities"
    INS_RSRV = "Insurance Reserves (Insurance)"
    INT_EXP_FED_REPOS = "Interest Expense Federal Funds"
    INT_INC_DEPS = "Interest Income Bank Deposits"
    INT_INC_FED_REPOS = "Interest Income Government Securities"
    INT_INC_OTH = "Other Interest or Dividend Income"
    INTANG_OTH_GROSS = "Other Intangible Assets Gross"
    INVEN_FG = "Inventories Finished Goods"
    INVEN_WIP = "Inventories Work In Progress"
    INVEST_BONDS = "Bonds"
    INVEST_EQ = "Total Equity Securities Investment"
    INVEST_INC = "Investment Income"
    INVEST_MTGE = "Mortgage, Policy & Other Loans"
    INVEST_PFD_NRED = "Non Redeemable Preferred Stock"
    INVEST_SUB = "Investment In Unconsolidated Subsidiaries"
    LABOR_EXP = "Labor & Related Expense"
    LIABS_PS = "Long Term Liabilities Per Share"
    LOAN_BK = "Interbank Loans"
    LOAN_COMML_INDL = "Commercial & Industrial Loans"
    LOAN_FOR = "Foreign Loans"
    LOAN_LOSS_ACT = "Net Loan Losses"
    LOAN_NONPERF = "Non Performing Loans"
    MATL_EXP = "Material Expense"
    MIN_PENS_LIABS_ADJ = "Minimum Pension Liability Adjustment"
    NET_CAP_REQUIRE = "Net Capital Requirement"
    OPER_EXP = "Total Operating Expense (Financial Services)"
    OPER_INC_INTL = "International Operating Income"
    OPT_WRNT_CF = "Proceeds from Stock Options"
    PAY_ACCT_CF = "Accounts Payable (Cash Flow)"
    PAY_TAX_DFD_TAX = "Income Tax Payable Plus Short Term Deferred Tax"
    PFD_STK_ESOP_GTD = "ESOP Guarantees Preferred Stock"
    PFD_STK_RED = "Redeemable Preferred Stock"
    PPE_DEP_BLDG = "Accumulated Depreciation Buildings"
    PPE_DEP_EQUIP = "Accumulated Depreciation Machinery & Equipment"
    PPE_DEP_LEASED_PROP = "Accumulated Depreciation Leased Property"
    PPE_DEP_OTH = "Accumulated Depreciation Other Property, Plant, & Equip"
    PPE_DEP_TRANS_EQUIP = "Accumulated Depreciation Transportation Equipment"
    PPE_GROSS_CONSTR = "Property, Plant, & Equipment Construction in Progress"
    PPE_GROSS_LAND = "Property, Plant, & Equipment Land & Improvements"
    PPE_GROSS_LEASES = "Property, Plant, & Equipment Leases"
    PPE_GROSS_SOFT_EQUIP = "Property, Plant, & Equipment Computer Software and Equipment"
    PREM_UNEARN = "Unearned Premiums"
    REAL_GAIN = "Securities Gain"
    RECEIV_NET = "Accounts Receivables, Net"
    RESTRUCT_PS = "Restructuring Exp Per Share Net Of Tax Fiscal"
    RSRV_APPR_OTH = "Other Appropriated Reserves"
    RSRV_UNAPPR = "Unappropriated (Free) Reserves"
    SALES_UNCON = "Unconsolidated/Parent Company Sales"
    SECS_GAIN = "Securities Gain"
    SECS_OTH = "Other Securities"
    SECS_TREAS = "Treasury Securities"
    SHS_CLOSELY_HELD_PCT = "Closely Held Shares (%)"
    STK_SPLIT_RATIO = "Stock Split/Dividend Ratio"
    TOT_INVEST_RET = "Total Investment Return"
    TRADE_INC = "Trading Account Income"
    TREAS_STK = "Treasury Stock Common (incl. ESOP)"
    TRUST_INC = "Trust Income"
    VOLUME_TRADE = "Trading Volume"
    WKCAP_ASSETS_OTH = "Other Asset/Liabilities"
    XORD_PS = "Extraordinary Credit/Charge Per Share"
    CASH_GENERIC = "Cash & Equivalents Generic"
    REINS_ADJ_RSRV = "Reinsurance & Adjustment Reserves"
    COMPR_INC_PENS_LIABS = "Comprehensive Income Pension Liability"
    GW_IMPAIR = "Impairment Of Goodwill"
    OPER_LEASE_EXP = "Rental/Operating Lease Expense"
    PENS_ASSETS_BONDS = "Pension Plan Asset Allocation % Bonds"
    PENS_ASSETS_LT = "Pension Long Term Assets"
    PENS_ASSETS_PROP = "Pension Plan –Asset Allocation % Property"
    PENS_BNFIT_OBLIG_PROJ = "Pension Projected Benefit Obligation"
    PENS_COST_INT = "Pension Interest Cost"
    PENS_COST_SERV_PRIOR = "Pension Prior Service Costs"
    PENS_DISCOUNT_RATE = "Pension Discount Rate"
    PENS_EXP_NPP_NET_OTH = "Pension Other Periodic Pension (Income)/Expense"
    PENS_GAIN_SETTLE = "Pension Gains/(Losses) from Settlements"
    PENS_LIABS_NET = "Pension Net Liability/(Asset)"
    PENS_ROA = "Pension Expected Return on Plan Assets for Period"
    PENS_ROA_LT = "Pension Expected Long Term Rate of Return on Assets"
    PPE_IMPAIR = "Property, Plant & Equipment Impairment"
    ITC = "Income Tax Credits"
    CAP_RATIO_TIER1 = "Capital Adequacy Ratio Tier 1 Capital"
    COMP_SOFT = "Computer Software"
    OPER_LEASE_COMMIT_5YR = "Lease Commitments Over 5 Years"
    OPER_LEASE_COMMIT_YR2 = "Lease Commitments Year 2"
    OPER_LEASE_COMMIT_YR4 = "Lease Commitments Year 4"
    STK_OPT_EXP = "Stock Option Compensation Expense"
    PRICE_SECS = "Market Price Year End"
    PBK_SECS = "Price to Book Security Level"
    BPS_SECS = "Books Value Per Share Security Level"
    HLTH_FUNDED_STATUS = "Healthcare Data Funded Status"
    DEBT_BONDS_CONV_SR = "Bonds Senior Convertible"
    DEBT_BONDS_CONV_SUBORD_JR = "Bonds Junior Subordinated Convertible"
    DEBT_BONDS_COVERED = "Bonds Covered"
    DEBT_BONDS_MTGE1 = "Bonds First Mortgage"
    DEBT_BONDS_OTH = "Bonds Other Borrowings"
    DEBT_BONDS_SECURE_LIEN2 = "Bonds Sec. 2nd Lien"
    DEBT_BONDS_SUBORD = "Bonds Subordinated"
    DEBT_BONDS_SUBORD_SR = "Bonds Senior Subordinated"
    DEBT_CDO = "Collateralized Debt Obligations"
    DEBT_LOAN_ADV_FFCB = "FFCB Advances"
    DEBT_LOAN_FACIL_DIP = "Term Loans DIP Facility"
    DEBT_LOAN_OTH = "Loans Other Borrowings"
    DEBT_LOAN_SECURE_LIEN1 = "Term Loans Sec. 1st Lien"
    DEBT_LOAN_SECURE_LIEN3 = "Term Loans Sec. 3rd Lien"
    DEBT_LOAN_TOT = "Total Term Loans"
    DEBT_LOAN_UNSEC_DELAY_DRAW = "Term Loans Unsecured Delayed Drawdown"
    DEBT_LT_CONV_PFD = "Preferreds Convertible (LT Debt)"
    DEBT_LT_REVOLV_FACIL_AB = "Asset Backed Facility"
    DEBT_LT_REVOLV_SECURE = "Revolvers Sec. Line"
    DEBT_LT_REVOLV_SECURE_CURR = "Short Term Revolver (LT Debt) Secured"
    DEBT_LT_REVOLV_TOT = "Total Revolving Credit"
    DEBT_LT_REVOLV_UNSECURE_CP = "Commercial Paper (LT Debt) Unsecured"
    DEBT_LT_REVLV_UNSEC_FCL_OTH = "Revolvers Other Unsecured Facility"
    DEBT_NOTES_BONDS_TOT = "Total Notes/Bonds"
    DEBT_NOTES_SURPLUS_SUBORD = "Bonds Subordinate Surplus Notes"
    DEBT_OTH_CAPL = "Capital Leases"
    DEBT_OTH_TOT = "Total Other Debt"
    DEBT_RECEIV_CR_CARD = "Credit Card Receivables"
    DEBT_RECEIV_MTGE_COMML = "Commercial Mortgage Receivables"
    DEBT_RECEIV_OTH = "Other Receivables"
    DEBT_REVOLV_UNSECURE_CURR = "Short Term Borrowings from LT Unsecured Revolvers"
    DEBT_ST_ADJ = "Adjustments Short Term"
    DEBT_ST_ADV_FHLB = "ST FHLB Advances"
    DEBT_ST_CURR_PORT = "Current Portion of LTD"
    DEBT_ST_NOTES_PAY = "Notes Payable"
    DEBT_ST_REPOS = "Repurchase Agreements"
    DEBT_ST_SECURE_OTH = "Other Borrowings Secured"
    DEBT_ST_STN_BANK = "Bank STN's"
    DEBT_ST_UNSECURE_OTH = "Other Borrowings Unsecured"
    DEBT_TRUST_PFD = "Preferreds Trust"
    IMPAIR_PPE = "Fixed Asset Impairment"
    XCEPT_PROV = "Exceptional Provisions"
    GW_WDOWN = "Goodwill Write Off"
    IMPAIR_INTANG_OTH = "Other Intangible Asset Impairment"
    OTH_UNUSUAL_EXP = "Other Unusual Expense"
    INT_INC_NON_OPER = "Non Operating Interest Income"
    MISC_EXP_NON_OPER = "Other Income (Expense)"
    INT_CAP = "Interest Capitalized"
    PREP_EXP = "Prepaid Expenses"
    PPE_GROSS = "Property, Plant, & Equipment Gross"
    PAY_DIV = "Dividends Payable"
    LIABS_CURR_MISC = "Miscellaneous Current Liabilities"
    INVEST_SALE_CF = "Sale/Maturity of Investments"
    STK_PURCH_CF = "Repurchase of Common & Preferred Stock"
    DEBT_ST_CF = "Change in Current Debt"
    CAPEX_OTH = "Capital Expenditures (Other Assets)"
    DEBT_LT_REDUCT_CF = "Reduction of LT Debt"
    FIN_SOURCES_CF = "Other Financing Activities (Sources)"
    DFD_INC = "Deferred Income"
    INVEST_PURCH_CF = "Purchase of Investments"
    DEP_AMORT_EXP = "Depreciation & Amortization"
    OPER_INC_OTH = "Other Operating Income"
    ORDINARY_INC = "Ordinary Income Japan"
    HLTH_PBO = "Healthcare –Projected Benefit Obligation"
    HLTH_UNREC_SERV_COST = "Healthcare Unrecognized Prior Service Cost"
    HLTH_ROA_EXPECTED = "Healthcare Expected Return on Plan Assets"
    HLTH_ROA_LT = "Healthcare Expected Long Term Return Rate on Pension Assets"
    HLTH_INT_COST = "Healthcare Interest Cost"
    HLTH_GL_SETTLE = "Healthcare Gain/(Loss) from Settlements"
    HLTH_NPP_EXP = "Health Care Expense"
    DEBT_ST_LT_TOT = "Total Debt"
    DEBT_ST_TOT = "Total Short Term Debt"
    LOAN_LOSS_RECOV = "Loan Losses Recoveries"
    PREM_EARN = "Premiums Earned"
    STK_OPT_CF = "Stock Based Compensation (Cash Flow)"
    PENS_ASSETS_BEG_BAL = "Beg Balance Assets"
    PENS_ASSETS_INT_INC = "Interest Income/Expected Return on Pension Assets"
    PENS_BNFIT_GL_ACTRL = "Actuarial LS/(GN)"
    PENS_ASSETS_CONTR = "Contributions"
    PENS_BNFIT_PTCP_CONTR = "Benefits Participant Contributions"
    PENS_BNFIT_PAID = "Benefits Paid"
    PENS_BNFIT_ACQ_DVST = "Pension Benefits Acquisition/(Divestiture)"
    PENS_EXCH_RATE_DIFF = "Pension Assets Exchange Rate Difference"
    PENS_BNFIT_EXCHRATE_DIFF = "Benefits Exchange Rate Diff"
    PENS_BNFIT_OTH_CHG = "Other Benefits Changes"
    PENS_ASSETS_TOTAL = "Asset Allocation (%) Total"
    PENS_BNFT_SRVCST_PRIOR_CURR = "Pension Benefits Current/Prior Service Cost"
    PENS_BNFIT_SERVCOST_PRIOR = "Benefits Prior Service Cost"
    PENS_BNFIT_INT_COST = "Benefits Interest Cost"
    APBO_ALLOC_CCE = "APBO Allocation % Cash & Cash Equivalents"
    APBO_ALLOC_DEBT = "APBO Asset Allocation % Debt"
    APBO_ALLOC_OTH = "APBO Asset Allocation % Other"
    HLTH_CONTR = "APBO Contributions"
    HLTH_PTCP_CONTR = "APBO Health Participant Contributions"
    HLTH_BNFIT_PAID = "APBO Health Benefits Paid"
    HLTH_ACQ_DVST = "APBO Health Acquisition/Divestiture"
    HLTH_CRTL_SETTLE_AMEND = "APBO Health Curtail/Settle/Amend"
    HLTH_EXCH_RATE_DIFF = "APBO Health Exchange Rate Difference"
    HLTH_OTH_CHG = "APBO Health Other Changes"
    HLTH_ACTRL_GL = "APBO Health Actuarial GN/(LS)"
    HLTH_ACT_RET_ASSET = "APBO Actual Return Assets"
    HLTH_APBO_SRVCST_PRIOR_CURR = "APBO Current/Prior Service Cost"
    HLTH_APBO_SERVCOST_PRIOR = "APBO Prior Service Cost"
    HLTH_SERV_COST_TOT = "APBO Service Cost Total"
    HLTH_GL_ACTRL = "APBO Actuarial LS/(GN)"
    UNREAL_GL_TOT = "Unrealized Investment Gain/Loss"
    DFD_INC_CURR = "Deferred Income Current"
    TAX_CHG_EFF = "Effect of Tax Code Changes"
    GA_EXP = "General & Administrative Expense"
    MKT_EXP = "Marketing Expense"
    LIABS_OPER_LEASE_CURR = "Operating Lease Liabilities Current Portion"
    PPE_NET_OWNED = "Property, Plant and Equipment Owned net"
    DEBT_LT_XLEASE = "Long Term Debt Excluding Lease Liabilities"
    AMORT_EXP_LEASE = "Amortization of Leased Assets"
    FRANK_BAL_CF = "Franking Balance for Australian Companies"
    OPER_LEASE_COMMIT_2YR_5YR = "Operating Lease Commitments 2 to 5 Years"
    DIR_FIN_LEASE = "Sales and Direct Financing Leases"
    ACCEL_DEP = "Accelerated Depreciation"
    EARLY_TERM_CONTRACT = "Early Termination of Contracts"
    UNREAL_GL_PROP = "Unrealized Gain/Loss Investment Property"
    UNREAL_GL_DERIV = "Unrealized Gain/Loss Hedges/Derivatives"
    UNREAL_GL_OTH = "Unrealized Gain/Loss Other Intangibles"
    ACTG_CHG_PS = "Accounting Change Per Share Cum Effect Fiscal"
    AMORT_DFD_CHRG = "Amortization of Deferred Charges"
    ASSETS_INTL = "International Assets"
    ASSETS_SEP_ACCTS = "Separate & Variable Account Assets"
    BDEBT = "Bad Debt / Doubtful Accounts"
    CAP_LEASE = "Capitalized Lease Obligations"
    COM_EQ_FOR_EXCH = "Cumulative Translation Adjustment"
    COM_EQ_HEDG_GL = "Comprehensive Income Hedging Gain/Loss"
    COM_EQ_PAR = "Common Stock Par/Carry Value"
    COM_SHS_AUTH = "Number Of Shares Authorized"
    COM_SHS_TRADE = "Shares Total Common Traded"
    COM_STK_ESOP = "ESOP Debt Guarantee"
    COST_DEBT = "Weighted Cost Of Debt"
    DEBT_LT_CURR = "Current Portion Of Long Term Debt"
    DEBT_LT_XCAP = "Long Term Debt Excluding Capitalized Leases"
    DEP_EXP_UNCON = "Unconsolidated/Parent Company Depreciation"
    DEPS_DEMAND = "Demand Deposits"
    DEPS_SAV = "Savings/Time Deposits"
    DFD_CHRG = "Deferred Charges"
    DFD_TAX_XITC_CF = "Deferred Taxes (excl. Investment Tax Credits)"
    DISC_OPER_PS = "Discontinued Operations Per Share Total"
    EMP_NUM = "Number of employees"
    EPS_AFT_XORD = "Earnings Per Share After Extraordinary Items"
    EPS_HEADLINE_UK = "Headline Earnings Per Share U.K."
    EPS_UNCON = "Unconsolidated/Parent Company Earnings Per Share"
    EQUIP_EXP = "Equipment Expense"
    FOR_CURN_ADJ = "Foreign Currency Adjustment (Net)"
    FOR_EXCH_INC = "Foreign Exchange Gains"
    GAIN_SALE_ASSETS_NET = "Gains/Loss On Disposal Of Assets"
    GW_AMORT = "Accumulated Goodwill Amortization"
    INC_TAX_CURR_DOM = "Income Tax Current Domestic"
    INC_TAX_DFD_DOM = "Income Tax Deferred Domestic (incl. local)"
    INC_UNEARN = "Unearned Income"
    INS_INVEST_TOT = "Total Investment Assets (Insurance)"
    INS_LT_RSRV = "Long Term Insurance Reserves"
    INT_EXP_DEPS = "Interest Expense On Bank Deposits"
    INT_EXP_OTH_BORR = "Other Borrowed Funds"
    INT_INC_FED_FUNDS = "Interest Income Federal Funds"
    INT_INC_LOAN = "Interest Income Loans"
    INTANG_OTH_AMORT = "Accumulated Other Intangible Amortization"
    INVEN_CF = "Inventories (Cash Flow)"
    INVEN_MATL = "Inventories Raw Materials"
    INVEST = "Investments Total"
    INVEST_COM_EQ = "Common Stocks"
    INVEST_FIX_INC = "Total Fixed Income Securities Investment"
    INVEST_LT_OTH = "Other Investments"
    INVEST_OTH = "Other Investments"
    INVEST_PFD_RED = "Redeemable Preferred Stock"
    ITC_CF = "Investment Tax Credits"
    LIABS_CURR_DFD_TAX = "Short Term Deferred Income Tax"
    LIFE_INS = "Life Insurance In Force"
    LOAN_BRKR = "Broker & Financial Institution Loans"
    LOAN_CONS = "Consumer & Installment Loans"
    LOAN_LEASE_FIN = "Lease Financing Loans"
    LOAN_MTGE = "Real Estate Mortgage Loans"
    LOAN_OTH = "Unspecified/Other Loans"
    MBS = "Mortgage Backed Securities"
    MON_CORRECT = "Monetary Correction"
    NUM_SHRHLDRS = "Number of Shareholders"
    OPER_INC_BEF_DEP = "Operating Income Before Depreciation And Amortization"
    OPER_PROV = "Operating Provisions"
    PAR_PS = "Par Value"
    PAY_TAX_CF = "Income Taxes Payable"
    PFD_STK_ESOP = "Preferred Stock Issues for ESOP"
    PFD_STK_NRED = "Non Redeemable Preferred Stock"
    POL_CLAIMS = "Policy Claims"
    PPE_DEP_CONSTR = "Accumulated Depreciation Construction in Progress"
    PPE_DEP_LAND = "Accumulated Depreciation Land & Improvements"
    PPE_DEP_LEASES = "Accumulated Depreciation Leases"
    PPE_DEP_SOFT_EQUIP = "Accumulated Depreciation Computer Software and Equipment"
    PPE_GROSS_BLDG = "Property, Plant, & Equipment Buildings"
    PPE_GROSS_EQUIP = "Property, Plant, & Equipment Machinery & Equipment"
    PPE_GROSS_LEASED_PROP = "Property, Plant, & Equipment Leased Property"
    PPE_GROSS_OTH = "Other Property, Plant & Equipment"
    PPE_GROSS_TRANS_EQUIP = "Property, Plant, & Equipment Transportation Equipment"
    PREM_WRITTEN = "Net Premiums Written"
    RECEIV_CF = "Accounts Receivable"
    RESTRUCT_EXP = "Restructuring Expense"
    RESTRUCT_PS_PTAX = "Restructuring Expense Per Share Pretax"
    RSRV_REVAL = "Revaluation Reserves"
    SALES_INTL = "International Sales"
    SECS_FED = "Federal Agency Securities"
    SECS_MUNI = "State & Municipal Securities"
    SECS_RESALE = "Securities Bought Under Resale Agreements"
    SHS_CLOSELY_HELD = "Shares Number Of Closely Held"
    STK_SALE_XOPT_CF = "Other Proceeds from Sale/Issuance of Stock"
    TAX_NON_INC = "Taxes Other than Income Taxes"
    TRADE_ACCT = "Trading Account Securities"
    TREAS_SHS = "Treasury Shares Number of Common Reacquired"
    TRUST_COMMISS_INC = "Trust & Fiduciary Income, Commissions & Fees"
    US_GAAP_AVAIL = "U.S. Information Available GAAP"
    VOLUME_WK_AVG = "Trading Volume (Weekly Average)"
    WKCAP_PS = "Working Capital Per Share"
    XORD_PS_PTAX = "Extraordinary Credit/Charge Per Share Pretax"
    ASSETS_RISK_WGHT = "Risk Weighted Assets"
    INVEN_PROG_PAYMT = "Inventories Progress Payments & Other"
    FIX_ASSETS_IMPAIR = "Impairment Of Financial Fixed Assets"
    INTANG_OTH_IMPAIR = "Impairment Of Other Intangibles"
    RESTATE_IND = "Flag indicating whether restated data exists"
    PENS_ABO = "Pension Accumulated Benefit Obligation"
    PENS_ASSETS_EQ = "Pension Plan Asset Allocation % Equities"
    PENS_ASSETS_OTH = "Pension Plan Asset Allocation % Other"
    PENS_ASSETS_VAL = "Pension Fair Value of Plan Assets"
    PENS_BNFIT_RETIR_POST = "Pension/Post Retirement Benefits"
    PENS_COST_SERV = "Pension Service Costs"
    PENS_COST_SERV_PRIOR_UNREC = "Pension Unrecognized Prior Service Cost"
    PENS_EXP_NPP_NET = "Pension Expense"
    PENS_FUND_ADJ_OTH = "Pension Other Adjustments To Funded Status For Net Pension/Post"
    PENS_GAIN_UNREC = "Pension Unrecognized Net Actuarial Gain/Loss"
    PENS_LIABS_UNFUNDED = "Unfunded Pension Liability (Supplementary)"
    PENS_ROA_ACT = "Pension Actual Return on Plan Assets"
    PENS_FUNDED_STATUS = "Pension Funded Status"
    TAX_CF = "Cash Taxes Paid"
    ACTG_CHG = "Cumulative Effect of Accounting Change"
    CAP_RATIO_TOT = "Capital Adequacy Ratio Total Capital"
    INT_CF = "Interest Paid (Cash Flow)"
    OPER_LEASE_COMMIT_YR1 = "Lease Commitments Year 1"
    OPER_LEASE_COMMIT_YR3 = "Lease Commitments Year 3"
    OPER_LEASE_COMMIT_YR5 = "Lease Commitments Year 5"
    STK_OPT_EXP_ADJ = "Stock Option Based Compensation Exp Adjusted To Net Income"
    MKT_VAL_SECS = "Market Value Security Level"
    PE_SECS = "Price to Earnings Security Level"
    HLTH_BNFIT_UNFUNDED = "Healthcare Data Unfunded Defined Benefits"
    DEBT_BONDS_CONV_JR = "Bonds Junior Convertible"
    DEBT_BONDS_CONV_SUBORD = "Bonds Subordinated Convertible"
    DEBT_BONDS_CONV_SUBORD_SR = "Bonds Senior Subordinated Convertible"
    DEBT_BONDS_JR = "Bonds Junior"
    DEBT_BONDS_MUNI = "Bonds Municipal (Taxable)"
    DEBT_BONDS_SECURE_LIEN1 = "Bonds Sec. 1st Lien"
    DEBT_BONDS_SECURE_LIEN3 = "Bonds Sec. 3rd Lien"
    DEBT_BONDS_SUBORD_JR = "Bonds Junior Subordinated"
    DEBT_BONDS_UNSECURE_SR = "Bonds Senior Unsecured"
    DEBT_GTD_FDIC = "FDIC Guaranteed Debt (TLGP)"
    DEBT_LOAN_ADV_FHLB = "FHLB Advances"
    DEBT_LOAN_MTGE = "Mortgage Loans"
    DEBT_LOAN_SECURE_DELAY_DRAW = "Term Loans Sec. Delayed Drawdown"
    DEBT_LOAN_SECURE_LIEN2 = "Term Loans Sec. 2nd Lien"
    DEBT_LOAN_SECURE_PLACE_PRIV = "Private Placement Notes Secured"
    DEBT_LOAN_UNSECURE = "Term Loans Unsecured"
    DEBT_LOAN_UNSEC_PLACE_PRIV = "Private Placement Notes Unsecured"
    DEBT_LT_REPOS = "Repurchase Agreement (LT Debt)"
    DEBT_LT_REVOLV_FACIL_DIP = "Revolvers DIP Facility"
    DEBT_LT_REVOLV_SECURE_CP = "Commercial Paper (LT Debt) Secured"
    DEBT_LT_REVLV_SEC_FACIL_OTH = "Revolvers Other Sec. Facility"
    DEBT_LT_REVOLV_UNSECURE = "Revolvers Unsecured"
    DEBT_LT_REVLV_UNSEC_CURR = "Short Term Revolver (LT Debt) Unsecured"
    DEBT_LT_STRAIGHT_PFD = "Preferreds Straight (LT Debt)"
    DEBT_NOTES_SURPLUS_SR = "Bonds Senior Surplus Notes"
    DEBT_OTH_ADJ = "Adjustments Other"
    DEBT_OTH_LT_CURR = "Current Portion of LTD"
    DEBT_RECEIV_AUTO = "Auto Receivables"
    DEBT_RECEIV_EQUIP_TRUST = "Equipment Trust Receivables"
    DEBT_RECEIV_MTGE_RES = "Residential Mortgage Receivables"
    DEBT_REVOLV_SECURE_CURR = "Short Term Borrowings from LT Sec. Rev."
    DEBT_SEC_FACIL_SWING_SBRD = "Swing Line Sub Facility Secured"
    DEBT_ST_ADV_FFCB = "ST FFCB Advances"
    DEBT_ST_BORR_FED_RSRV = "Federal Reserve Borrowings (TAF)"
    DEBT_ST_GTD_FDIC_CP = "Commercial Paper FDIC Gtd. (TLGP)"
    DEBT_ST_PURCH_FED_FUNDS = "Fed Funds Purchased"
    DEBT_ST_SECURE_ABS_CP = "Commercial Paper Secured (ABS)"
    DEBT_ST_SECURE_REVOLV = "Short Term Revolver Secured"
    DEBT_ST_UNSECURE_CP = "Commercial Paper Unsecured"
    DEBT_ST_UNSECURE_REVOLV = "Short Term Revolver Unsecured"
    DEBT_UNSEC_FACIL_SWING_SBRD = "Swing Line Sub Facility Unsecured"
    FIN_ASSETS_IMPAIR = "Financial Asset Impairment"
    REORG_RESTRUCT_EXP = "Reorganization and Restructuring Expense"
    LEGAL_CLAIM_EXP = "Legal Claim Expense"
    UNREAL_INVEST_GL = "Unrealized Investment Gain/Loss"
    DISC_OPER = "Discontinued Operations"
    EQ_AFF_INC_PTX = "Equity in Earnings of Affiliates"
    INT_EXP_DEBT = "Gross Interest Expense"
    XORD_ITEMS = "Extraordinary Gains/Losses from Sale of Asset"
    ASSETS_CURR_MISC = "Miscellaneous Current Assets"
    PPE_DEP = "Accumulated Depreciation"
    ACCR_PAYR = "Accrued Payroll"
    DFD_TAX_RSRV = "Deferred Tax Liability Untaxed Reserves"
    DIV_COM_CF = "Common Dividends"
    STK_SALE_CF = "Sale of Common & Preferred Stock"
    CAPEX_FIX = "Capital Expenditures (Fixed Assets)"
    DEBT_LT_ISS_CF = "Issuance of LT Debt"
    FIN_USES_CF = "Other Financing Activities (Uses)"
    LIABS_OTH_XDFD_REV = "Other Liabilities (excluding Deferred Revenue)"
    LOAN_RSRV = "Loan Loss Allowances (Reserves)"
    COGS_XDEP = "COGS excluding D&A"
    RD_EXP = "Research & Development"
    INVEST_ST_OTH = "Total Short Term Investments"
    HLTH_ASSETS_PLAN_FAIR_VAL = "Healthcare Fair Value of Plan Assets"
    HLTH_ABO = "Healthcare Accumulated Benefit Obligation"
    HLTH_ROA_ACT = "Healthcare Actual Return on Plan Assets"
    HLTH_DISCOUNT_RATE = "Healthcare Discount Rate"
    HLTH_SERV_COST = "Healthcare Service Costs"
    HLTH_AMORT_SERV_COST = "Healthcare Amortization of Prior Service Costs"
    HLTH_OTH_NPP_EXP = "Healthcare Net Periodic Plan Expense, Other"
    DEBT_LT_NET = "Net Long Term Debt"
    DEBT_LT_TOT = "Total Long Term Debt"
    LOAN_LOSS_NET = "Loan Losses Net"
    LOSS_CLAIM_EXP = "Losses, Benefits & Adjustments"
    UNDERWRITING_EXP = "Underwriting & Commissions"
    UPD_TYPE = "Data update indicator for preliminary or final results"
    PENS_BNFIT_PBO_BB = "Beg Balance PBO"
    PENS_ASSETS_ACTRL_GL = "Actuarial GN/(LS)"
    PENS_ASSETS_ACT_RET = "Actual Return Assets"
    PENS_ASSETS_EMPLR_CONTR = "Assets Employer Contributions"
    PENS_ASSETS_BNFIT_PAID = "Assets Benefits Paid"
    PENS_ASSETS_ACQ_DVST = "Pension Assets Acquisition/(Divestiture)"
    PENS_ASSETS_AMEND = "Pension Assets Curtailment/Settlement/Amendment"
    PENS_COST_EXCH_RATE_DIFF = "Pension Benefit Cost Exchange Rate Difference"
    PENS_ASSETS_OTH_CHG = "Other Changes"
    PENS_BNFIT_SETTLE = "Curtailment/Settlement"
    PENS_ASSETS_CCE = "Asset Allocation (%) CCE"
    PENS_BNFIT_SERVCOST_CURR = "Pension Benefits Current Service Cost"
    PENS_COST_SERV_TOT = "Service Cost Total"
    PENS_COST_FIN = "Finance Cost/(Income)"
    APBO_ALLOC_EQ = "APBO Asset Allocation % Equity"
    APBO_ALLOC_PROP = "APBO Asset Allocation % Property"
    APBO_ALLOC_TOT = "APBO Asset Allocation Total"
    HLTH_EMPLR_CONTR = "APBO Health Employer Contributions"
    HLTH_APBO_PTCP_CONTR = "APBO Participant Contribution"
    HLTH_APBO_BNFIT_PAID = "APBO Benefits Paid"
    HLTH_APBO_ACQ_DIV = "APBO Acquisition/Divestiture"
    HLTH_APBO_CURTAILM_SETTLEM = "APBO Curtailments/Settlements"
    HLTH_APBO_EXCH_RATE_DIFF = "APBO Exchange Rate Difference"
    HLTH_APBO_OTH_CHG = "APBO Other Changes"
    HLTH_APBO_ACTRL_GL = "APBO Actuarial LS/(GN)"
    HLTH_APBO_LIAB_BB = "APBO Beg Balance Liabilities"
    HLTH_APBO_SERVCOST_CURR = "APBO Current Service Cost"
    HLTH_APBO_INT_COST = "APBO Interest Cost"
    HLTH_FIN_COST = "APBO Finance Cost/(Inc)"
    HLTH_PERIOD_EXCH_RATE_DIFF = "APBO Exchange Rate Difference Period"
    ADV_EXP = "Advertising Expense"
    SALE_PPE_CF = "Sale of Property, Plant, and Equipment"
    ACQ_PROCESS_RD = "Acquired In Process R&D"
    SELL_EXP = "Selling & Marketing Expense"
    LIABS_OPER_LEASE = "Operating Lease Liabilities"
    ASSETS_LEASE_NET = "Operating Lease Right of Use Assets"
    DEBT_ST_XOPER = "Short Term Debt and Current Portion of Long Term Debt Excluding Lease Liabilities"
    DEBT_LT_XOPER = "Long Term Debt excl Operating Lease Liabilities"
    INT_EXP_LEASE = "Interest Expense on Leased Assets"
    ASSETS_NONPERF_OTH = "Other Non Performing Assets"
    OPER_LEASE_COMMIT_TOT = "Total Operating Lease Commitments"
    DEBT_OTH_CF = "Other Cash Flow Debt"
    CALAMITOUS_EVENT = "Calamitous Event"
    EPS_HEADLINE_UK_DIL = "Diluted Headline Earnings Per Share"
    UNREAL_GL_BIO_ASSETS = "Unrealized Gain/Loss Biological Assets"
    UNREAL_GL_INVEST = "Unrealized Gain/Loss Investments"


class FundamentalAdvancedDerivedItem(Enum):
    ACCR_EXP = "Accrued Expenses"
    ASSETS_EQ = "Assets To Equity (End Of Period)"
    ASSETS_OTH_TOT = "Other Assets Total"
    BNFIT_LOSS_RSRV_TCAP = "Benefit & Loss Reserves % Of Total Capital"
    CAPEX_5YGR = "Capital Spending 5Yr Growth Rate"
    CAPEX_FIX_ASSETS = "Capital Expenditure % Gross Fixed Assets"
    CASH_CURR_ASSETS = "Cash & Equivalents % Total Current Assets"
    CASH_DIV_COVG_RATIO = "Cash Dividend Coverage Ratio"
    CASH_SECS_DEPS = "Cash & Securities % Total Deposits"
    CF_SALES = "Cash Flow/Sales"
    COGS_SALES = "Cost of Goods Sold % Sales"
    COM_EQ_GR = "Equity 1 Year Annual Growth"
    DEBT_COM_EQ = "Debt (Total) % Common Equity"
    DEBT_EQ = "Total Debt % Total Equity"
    DEBT_ST_X_CURR_PORT = "Short Term Debt"
    DEP_ACCUM_FIX_ASSETS = "Accumulated Depreciation % Gross Fixed Assets"
    DFD_TAX_ASSETS_LT = "Deferred Income Tax Non Current Asset"
    DIV_YLD = "Dividend Yield Close"
    DPS_GR = "Dividends Per Share 1 Year Annual Growth"
    EARN_ASSETS_EFF = "Efficiency Of Earning Assets"
    EARN_YLD = "Earnings Yield Close"
    EBIT_OPER_ROA = "Return On Average Assets (EBIT)"
    EBITDA_OPER_MGN = "EBITDA Margin"
    EMP_GR = "Employees 1 Year Annual Growth"
    ENTRPR_VAL_EBITDA_OPER = "Enterprise Value To EBITDA"
    EPS_BASIC_GR = "EPS Basic Before Extras % Change"
    FED_REPOS_ASSET = "Federal Funds Sold & Securities Purchased"
    EBIT_OPER_FIX_CHRG_COVG = "Fixed Charge Coverage Ratio"
    FOR_ASSETS_PCT = "Foreign Assets % Total Assets"
    FOR_INC_PCT = "Foreign Income % Total Income"
    FOR_ROA = "Foreign Return On Assets"
    FREE_PS_CF = "Cash Flow Per Share (Diluted) Free"
    INC_ADJ = "Income Adjustment"
    INC_TAX_CURR = "Income Tax Current Total"
    INS_RSRV_GR = "Insurance Reserves 1 Year Annual Growth"
    INT_EXP_IB_LIABS = "Interest Expense (Total) % Interest Bearing Liabilities"
    INT_INC_AVG_DEPS = "Net Interest Income % Average Deposits"
    INTANG_OTH = "Net Other Intangibles"
    INVEN_DAYS = "Inventories Days Held"
    INVEST_ASSETS_DEPS = "Invested Assets % Total Deposits"
    INVEST_ASSETS_LOAN_DEPS = "Invested Assets & Loans % Total Deposits"
    INVEST_CAP = "Invested Capital Total"
    INVEST_LT = "Long Term Investments"
    INVEST_ST_TOT = "Total Short Term Investments"
    INVEST_YLD = "Yield On Investment"
    LOAN_LOSS_ACTUAL_RSRV = "Actual Loan Losses % Reserves For Loan Losses"
    LOAN_LOSS_PCT = "Net Loan Losses % Total Loans"
    LOAN_LOSS_RSRV_ASSETS = "Loan Loss Reserves % Total Assets"
    LOAN_LOSS_RSRV_TCAP = "Loan Loss Reserves % Total Capital"
    LOSS_EXP_RATIO = "Loss & Expense Ratios Combined"
    LTD_COM_EQ = "Long Term Debt % Common Equity"
    MIN_INT_TCAP = "Minority Interest % Total Capital"
    MKT_VAL_PUBLIC = "Market Capitalization Public."
    NET_INC_BASIC_AFT_XORD = "Net Income Avail To Common Basic After Extraordinaries"
    NET_INC_BEF_XORD_GR = "Net Income Before Extras 1 Year Growth"
    NET_INC_DIL_AFT_XORD = "Net Income Avail To Common Fully Diluted After Extraordinaries"
    NET_INT_INC_EARN_ASSETS = "Net Interest Income % Earning Assets"
    NON_INT_INC_REV = "Non Interest Income % Total Revs"
    NONPERF_LOAN_COM_EQ = "Non Performing Loans % Common Equity"
    NONPERF_LOAN_PCT = "Non Performing Loans % Total Loans"
    OPER_INC_AFT_UNUSUAL = "Operating Income After Unusual Items"
    OPER_INC_PREM_EARN = "Operating Income % Premiums Earned"
    OPER_INC_TCAP = "Operating Income % Total Capital"
    PAY_ACCT_SALES = "Accounts Payable/Sales"
    PPE_NET_BLDG = "Net Property, Plant & Equipment Buildings"
    PPE_NET_EQUIP = "Net Property, Plant & Equipment Machinery & Equipment"
    PPE_NET_LEASED_PROP = "Net Property, Plant & Equipment Leased Property"
    PPE_NET_OTH = "Net Property, Plant & Equipment Other Property, Plant, & Equipment"
    PPE_NET_TRANS_EQUIP = "Net Property, Plant & Equipment Transportation Equipment"
    RD_SALES = "Research & Development % Sales"
    RECEIV_GROSS = "Accounts Receivables, Gross"
    RECEIV_TURN = "Receivables Turnover"
    REINVEST_RATE = "Reinvestment Rate"
    ROCE = "Return On Common Equity"
    ROIC = "Return On Average Invested Capital"
    SALES_GR = "Sales Net 1 Year Growth"
    SALES_PER_EMP = "Sales Per Employee"
    SALES_WKCAP = "Sales (Net ) / Working Capital"
    SECS_RE_CAP = "Equity Securities & Real Estate % Capital"
    SGA_OTH = "Other Selling, General & Administrative Expense"
    SHS_FLOAT = "Shares Outstanding Less Closely Held Shares (Float)"
    TAX_RATE = "Tax Rate"
    TCAP_DEPS = "Capital (Total) % Total Deposits"
    UNEARN_PREM_TCAP = "Unearned Premium % Total Capital"
    UT_GROSS_INC = "Gross Income Income Before Interest Charges"
    UT_OPERATION_EXP = "Operation Expenses Total"
    WKCAP_PCT = "Working Capital % Total Capital"
    XORD_DISC = "Extraordinaries & Discontinued Operations"
    INVEST_RECEIV_LT = "Investments & Long Term Receivables"
    EBIT_BEF_UNUSUAL = "Earnings Before Interest, Taxes & Unusual Expense"
    EPS_DIL_AFT_XORD = "EPS Diluted After Extraordinaries"
    PBK_TANG = "Price To Tangible Book Value"
    PFCF = "Price To Free Cash Flow"
    PSALES_DIL = "Price To Sales Diluted"
    TANG_ASSETS_DEBT = "Tangible Assets To Total Debt"
    NET_INC_DIL_BEF_UNUSUAL = "Net Income Before Unusual Expense"
    LENDING_MISC = "Miscellaneous Lending"
    TANG_FIX_ASSETS_XRE = "Tangible Fixed Assets"
    TRADE_INC_NET = "Net Trading Income"
    BK_OPER_EXP_OTH = "Bank Other Operating Expense"
    BK_OPER_INC_TOT = "Bank Total Operating Income"
    COMMISS_INC_NET = "Net Commission Income"
    LOAN_GROSS = "Gross Loans"
    LOAN_DEPS = "Loans (Total) % Total Deposits"
    CF_ROIC = "Cash Flow Return on Average Invested Capital"
    LIABS_DISC_OPER = "Total Liabilities of Discontinued Operations"
    FSCORE = "Piotroski F Score"
    IMPAIR = "Impairments Total"
    RESTRUCT_DEBT = "Restructuring of Debt"
    ASSETS_COM_EQ = "Assets To Common Equity"
    ASSETS_GR = "Year Growth"
    ASSETS_PER_EMP = "Assets Per Employee"
    BPS_GR = "Assets Total 1 Year Growth"
    CAPEX_ASSETS = "Capital Expenditure % Total Assets"
    CAPEX_PS_CF = "Capital Expenditures Per Share"
    CASH_DIV_CF = "Cash Dividends/Cash Flow"
    CASH_ROCE = "Cash Earnings Return On Equity"
    CF_PS_GR = "Cash Flow Per Share 1 Year Growth"
    CLAIMS_NET_PREM = "Claims & Claim Expense % Net Premiums Written"
    COM_EQ_DEPS = "Equity % Total Deposits"
    COM_EQ_TCAP = "Equity % Total Capital"
    DEBT_ENTRPR_VAL = "Total Debt To Enterprise Value"
    DEBT_LT_CF = "Change in Long Term Debt"
    DEMAND_DEPS_PCT = "Demand Deposits % Total Deposits"
    DEPS_ASSETS = "Deposits (Total) % Total Assets"
    DIL_ADJ = "Dilution Adjustment"
    DIV_YLD_SECS = "Dividend Yield Security"
    EARN_ASSETS_AVAIL_FUNDS = "Earning Assets % Total Available Funds"
    EARN_ASSETS_PCT = "Earning Assets % Total Assets"
    EBIT_OPER_MGN = "EBIT Margin"
    EBITDA_CF = "EBITDA (From Cash Flow)"
    EFF_INT_RATE = "Interest Rate Estimated Average"
    ENTRPR_VAL_EBIT_OPER = "Enterprise Value To EBIT"
    ENTRPR_VAL_SALES = "Enterprise Value To Sales"
    EXP_RATIO = "Expense Ratio"
    FIX_ASSETS_COM_EQ = "Fixed Assets % Common Equity"
    FOR_ASSET_TURN = "Foreign Asset Turnover"
    FOR_DEPS_PCT = "Foreign Office Deposits % Total Deposits"
    FOR_NET_MGN = "Foreign Income Margin"
    FOR_SALES_PCT = "Foreign Sales % Total Sales"
    GROSS_CF_DEBT = "Cash Flow (Gross) % Total Debt"
    INC_SUND = "Sundry Revenue/Income"
    INC_TAX_DFD = "Deferred Income Taxes"
    EBIT_OPER_INT_COVG = "Pretax Interest Coverage Ratio"
    INT_EXP_OTH = "Other Interest Expense Banks"
    INT_INC_EARN_ASSETS = "Interest Income (Total) % Earning Assets"
    INVEN_CURR_ASSETS = "Inventories % Total Current Assets"
    INVEN_TURN = "Inventory Turnover"
    INVEST_ASSETS_LIABS = "Invested Assets % Liabilities"
    INVEST_ASSETS_PCT = "Invested Assets % Total Assets"
    INVEST_INC_INVEST_ASSETS = "Investment Income % Invested Assets"
    INVEST_PROP = "Investment Property"
    INVEST_TCAP = "Investments (Total) % Total Capital"
    LOAN_GR = "Loans 1 Year Growth Rate"
    LOAN_LOSS_COVG = "Loan Loss Coverage Ratio"
    LOAN_LOSS_PROV_PCT = "Loan Losses Provision % Total Loans"
    LOAN_LOSS_RSRV_PCT = "Loan Losses Reserves % Total Loans"
    LOAN_TCAP = "Loans (Total) / Total Capital"
    LOSS_RATIO = "Loss Ratio"
    LTD_TCAP = "Long Term Debt % Total Capital"
    MKT_VAL_GR = "Market Value 1 Year Growth"
    NET_CF_DEBT = "Cash Flow (Net) % Total Debt"
    NET_INC_BASIC_BEFT_XORD = "Income Before Extraordinary Items Available For Common"
    NET_INC_DIL = "Net Income Avail To Common Fully Diluted"
    NET_INC_PER_EMP = "Net Income/Employee Most Recent Fy"
    NET_MGN_GR = "Net Margin 1 Year Growth Rate"
    NON_OPER_EXP = "Non Operating Expense"
    NONPERF_LOAN_LOSS_RSRV = "Non Performing Loans % Loan Loss Reserves"
    OPER_CF_FIX_CHRG = "Operating Cash Flow To Fixed Charges (Interest & Dividend)"
    OPER_INC_GR = "Year Growth"
    OPER_INC_PREM_WRITTEN = "Operating Income 1 Year Growth"
    OPER_PS_NET_CF = "Cash Flow From Operations Per Share Net"
    PFD_STK_TCAP = "Preferred Stock % Total Capital"
    PPE_NET_CONSTR = "Net Property, Plant & Equipment Construction In Progress"
    PPE_NET_LAND = "Net Property, Plant & Equipment Land & Improvements"
    PPE_NET_LEASES = "Net Property, Plant & Equipment Leases"
    PPE_NET_SOFT_EQUIP = "Net Property, Plant & Equipment Computer Software And Equipment"
    PREM_WRITTEN_COM_EQ = "Net Premium Written % Equity"
    RECEIV_CURR_ASSETS = "Receivables % Current Assets"
    RECEIV_ST_OTH = "Other Receivables"
    RECEIV_TURN_DAYS = "Accounts Receivables Days"
    ROA_PTX = "Return On Average Assets Pretax"
    ROEA = "Return On Earning Assets"
    SALES_FIX_ASSETS = "Sales (Net) / Gross Fixed Assets"
    SALES_INVEN_TURN = "Sales To Inventory Turnover"
    SALES_PS_GR = "Sales Per Share 1 Year Growth"
    SAV_DEPS_PCT = "Savings Deposits % Total Deposits"
    SECS_RE_INVEST_ASSETS = "Equity Securities & Real Estate % Invested Assets"
    SGA_SALES = "Selling, General & Admin Expense % Sales"
    SPEC_ITEMS = "Special Items"
    TCAP_ASSETS = "Capital (Total) % Total Assets"
    TOT_DEBT_TCAP_STD = "Total Debt % Total Capital"
    US_GAAP_ADJ = "U.S. GAAP Adjustment"
    UT_NON_OPER_INC_OTH = "Nonoperating Income (Net) Other"
    WKCAP = "Working Capital"
    XORD = "Extraordinary Items (Including Accounting Change)"
    ZSCORE = "ALTMAN'S Z SCORE"
    DEBT_SERV = "Debt Service Ratio Including ST Debt Pretax"
    EBITDA_BEF_UNUSUAL = "EBITDA Before Unusual Expenses"
    EPS_DIL_GR = "EPS Diluted Before Extras % Change"
    PE_DIL = "Price To Earnings Diluted"
    PFCF_DIL = "Price To Free Cash Flow"
    STD_DEBT = "Short Term Debt % Total Debt"
    PAY_TURN_DAYS = "Days of Payables Outstanding"
    INT_INC_MISC = "Miscellaneous Interest Income"
    RE_INVEST = "Real Estate Investment"
    FIN_INVEST_TOT = "Total Investments for Financial"
    BK_OPER_INC_OTH = "Bank Other Operating Income"
    BK_OPER_EXP_TOT = "Bank Total Operating Expense"
    BK_NON_OPER_INC = "Bank Non Operating Income Expense"
    ACCT_PAY_OPER = "Creditors"
    LOAN_ASSETS = "Loans (Total) % Total Assets"
    ASSETS_DISC_OPER = "Total Assets of Discontinued Operations"
    UPD_TYPE = "Data update indicator for preliminary or final results"
    LIABS_LEASE = "Capital and Operating Lease Obligations"
    FCF_YLD = "Free Cash Flow Yield"
    OTH_XCEPT_CHRG = "Exceptional Charges Other"


fundamental_basic_dict = {item.name: item.value for item in FundamentalBasicItem}
fundamental_basic_derived_dict = {item.name: item.value for item in FundamentalBasicDerivedItem}
fundamental_advanced_dict = {item.name: item.value for item in FundamentalAdvancedItem}
fundamental_advanced_derived_dict = {item.name: item.value for item in FundamentalAdvancedDerivedItem}

FundamentalMetric = Enum('FundamentalMetric',
                         {**fundamental_basic_dict,
                          **fundamental_basic_derived_dict,
                          **fundamental_advanced_dict,
                          **fundamental_advanced_derived_dict
                          }
                         )


class FundamentalFormat(Enum):
    RESTATED = 'Restated'
    NON_RESTATED = 'Non Restated'


class RatingType(Enum):
    BUY = 'Buy'
    OVERWEIGHT = 'Overweight'
    HOLD = 'Hold'
    UNDERWEIGHT = 'Underweight'
    SELL = 'Sell'
    NONE = 'No Recommendations'
    TOTAL = 'Total'
    SCORE = 'Numeric Score'


class FiscalPeriod:
    """
    Create an abosolute fiscal period with year and period.

    :param y: year
    :param p: period
    :return: fiscal period object

    **Usage**

    The year combined with period can determine the fiscal period of the estimate.

    **Examples**

    Year is :math:`2025` and period is :math:`2`:

    >>> FiscalPeriod(2025, 2)

    """

    def __init__(self, y: Union[int, str, None] = None, p: Union[int, str, None] = None):
        self.y = y
        self.p = p

    def as_dict(self):
        return {
            'y': self.y,
            'p': self.p
        }

    @classmethod
    def from_dict(cls, obj):
        return FiscalPeriod(y=obj.get('y'), p=obj.get('p'))


BASIC_MEASURES = [EstimateItem.EPS,
                  EstimateItem.EPS_C,
                  EstimateItem.EPS_P,
                  EstimateItem.SALES,
                  EstimateItem.SALES_C,
                  EstimateItem.SALES_P,
                  EstimateItem.DPS,
                  EstimateItem.CFPS,
                  EstimateItem.PRICE_TGT,
                  EstimateItem.EPS_LTG]

LT_MEASURES = [EstimateItem.PRICE_TGT, EstimateItem.EPS_LTG]

BASIS_TO_DATASET = {EstimateBasis.ANN: 'AF',
                    EstimateBasis.QTR: 'QF',
                    EstimateBasis.SEMI: 'SAF',
                    EstimateBasis.NTM: 'NTM',
                    EstimateBasis.STM: 'NTM'}

BASIS_TO_FIELD = {
    EstimateBasis.ANN: 'Af',
    EstimateBasis.QTR: 'Qf',
    EstimateBasis.SEMI: 'Saf',
    EstimateBasis.NTM: 'Ntm',
    EstimateBasis.STM: 'Stm'
}

FF_BASIS_TO_DATASET = {FundamentalBasis.ANN: 'AF',
                       FundamentalBasis.QTR: 'QF',
                       FundamentalBasis.SEMI: 'SAF'}

FF_BASIS_TO_FIELD = {FundamentalBasis.ANN: 'Af',
                     FundamentalBasis.QTR: 'Qf',
                     FundamentalBasis.SEMI: 'Saf'}

RATING_TO_FIELD = {
    RatingType.BUY: 'feBuy',
    RatingType.OVERWEIGHT: 'feOver',
    RatingType.HOLD: 'feHold',
    RatingType.UNDERWEIGHT: 'feUnder',
    RatingType.SELL: 'feSell',
    RatingType.NONE: 'feNoRec',
    RatingType.TOTAL: 'feTotal',
    RatingType.SCORE: 'feMark'}


@plot_measure((AssetClass.Equity,), (AssetType.Single_Stock,))  # TO DO add query type
def factset_estimates(asset: Asset, metric: EstimateItem = EstimateItem.EPS,
                      statistic: EstimateStatistic = EstimateStatistic.MEAN,
                      report_basis: EstimateBasis = EstimateBasis.ANN,
                      period: Union[int, FiscalPeriod, None] = 1,
                      *, source: str = None, real_time: bool = False, request_id: Optional[str] = None) -> Series:
    """
    FactSet estimates for single stocks.

    :param asset: asset object loaded from security master
    :param metric: metric for estimate e.g. EPS
    :param statistic: type of estimate to show e.g. Mean
    :param report_basis: reporting basis of the estimate e.g. Annual
    :param period: rolling window for the estimate e.g. 1 period ahead or fixed non-rolling window e.g.
            FiscalPeriod(2025, 2)
    :param source: name of function caller: default source = None
    :param real_time: whether to retrieve intraday data instead of EOD, real time is currently not supported
    :param request_id: service request id, if any
    :return: FactSet Estimates
    """
    if not isinstance(report_basis, EstimateBasis):
        raise MqValueError('Invalid Estimate Basis argument')

    start, end = DataContext.current.start_date, DataContext.current.end_date
    start_new = RelativeDate('-1y', base_date=start).apply_rule()
    basic = 'BASIC' if metric in BASIC_MEASURES else 'ADVANCED'
    column_prefix = '' if metric in BASIC_MEASURES else 'Adv'
    consensus = 'CONH' if statistic != EstimateStatistic.ACTUAL else 'ACT'
    basis_ds = 'LT' if metric in LT_MEASURES else BASIS_TO_DATASET[report_basis]
    basis_cl = 'Lt' if metric in LT_MEASURES else BASIS_TO_FIELD[report_basis]
    if report_basis in [EstimateBasis.NTM, EstimateBasis.STM]:
        ds_id = f'FE_{basis_ds}'
    else:
        ds_id = f'FE_{basic}_{consensus}_{basis_ds}_GLOBAL'
    ds = Dataset(ds_id)
    bbid = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
    try:
        df = ds.get_data(bbid=bbid, start=start_new, end=end,
                         feItem=metric.name)
    except Exception as e:
        raise MqValueError(f'Could not query dataset {ds_id} because of {e}')
    if df.empty:
        raise MqValueError(f'No data found for {metric.value} for {asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)}')

    df.reset_index(inplace=True)
    if statistic == EstimateStatistic.ACTUAL:
        if report_basis in [EstimateBasis.NTM, EstimateBasis.STM]:
            raise MqValueError('NTM and STM are not supported for actual values')
        elif metric in LT_MEASURES:
            raise MqValueError(f'No actual data for {metric.value}')
        else:
            df = df[['feFpEnd', 'feValue']]
            df.rename(columns={'feFpEnd': 'date'}, inplace=True)
            df['date'] = pd.to_datetime(df['date'])
            column = 'feValue'
    elif report_basis not in [EstimateBasis.NTM, EstimateBasis.STM]:
        if metric in LT_MEASURES:
            pass
        elif isinstance(period, int):
            df = df[df['fePerRel'] == period]
        else:
            if report_basis == EstimateBasis.ANN:
                fiscal_period_start = datetime.datetime(period.y, 1, 1)
                fiscal_period_end = datetime.datetime(period.y, 12, 31)
            elif report_basis == EstimateBasis.QTR:
                if isinstance(period.p, int) and period.p not in [1, 2, 3, 4]:
                    raise MqValueError('Period number has to be one of 1,2,3 or 4 for quarterly basis')
                elif period.p is None:
                    raise MqValueError(
                        'Please specify the period as an integer between 1 and 4 like FiscalPeriod(2022, 4) '
                        'for 2022Q4 estimate')
                fiscal_period_start = datetime.datetime(period.y, (period.p - 1) * 3 + 1, 1)
                fiscal_period_end = fiscal_period_start + pd.DateOffset(months=3) - pd.DateOffset(days=1)
                fiscal_period_end = pd.to_datetime(fiscal_period_end)
            elif report_basis == EstimateBasis.SEMI:
                if isinstance(period.p, int) and period.p not in [1, 2]:
                    raise MqValueError('Period number has to be 1 or 2 for semi-annual basis')
                elif period.p is None:
                    raise MqValueError(
                        'Please specify the period as 1 or 2 like FiscalPeriod(2022, 2) for 2022H2 estimate')
                fiscal_period_start = datetime.datetime(period.y, (period.p - 1) * 6 + 1, 1)
                fiscal_period_end = fiscal_period_start + pd.DateOffset(months=6) - pd.DateOffset(days=1)
                fiscal_period_end = pd.to_datetime(fiscal_period_end)
            df['feFpEnd'] = pd.to_datetime(df['feFpEnd'])
            df = df[(df['feFpEnd'] >= fiscal_period_start) & (df['feFpEnd'] <= fiscal_period_end)]
            if df.empty:
                raise MqValueError('No Data returned for selected fiscal period')

        df.fillna({'consEndDate': end}, inplace=True)
        df['date_range'] = df.apply(lambda row: pd.date_range(row['date'], row['consEndDate']), axis=1)
        df = df.explode('date_range').drop(columns=['date', 'consEndDate']).rename(
            columns={'date_range': 'date'})
        column = f'fe{column_prefix}{statistic.value}{basis_cl}'
    else:
        df['date'] = pd.to_datetime(df['date'])
        column = f'fe{statistic.value}{basis_cl}'

    df = df[df['date'] >= pd.to_datetime(start)]
    df = df.sort_values(by='date', ascending=True).set_index('date')
    series = ExtendedSeries(df[column], name=statistic.value)
    series.dataset_ids = ds.id

    return series


@plot_measure((AssetClass.Equity,), (AssetType.Single_Stock,))  # TO DO add query type
def factset_fundamentals(asset: Asset,
                         metric: FundamentalMetric = FundamentalMetric.EPS_BASIC,
                         report_basis: FundamentalBasis = FundamentalBasis.ANN,
                         report_format: FundamentalFormat = FundamentalFormat.NON_RESTATED,
                         *, source: str = None, real_time: bool = False, request_id: Optional[str] = None) -> Series:
    """
    FactSet fundamentals for single stocks.

    :param asset: asset object loaded from security master
    :param metric: metric for estimate e.g. EPS
    :param report_basis: reporting basis of the estimate e.g. Annual
    :param report_format: restated or non-restated
    :param source: name of function caller: default source = None
    :param real_time: whether to retrieve intraday data instead of EOD, real time is currently not supported
    :param request_id: service request id, if any
    :return: FactSet Fundamentals
    """
    start, end = DataContext.current.start_date, DataContext.current.end_date
    start_new = RelativeDate('-1y', base_date=start).apply_rule()

    basic = 'BASIC' if metric.name in {**fundamental_basic_dict, **fundamental_basic_derived_dict} else 'ADVANCED'
    derived = '_DER' if metric.name in {**fundamental_basic_derived_dict, **fundamental_advanced_derived_dict} else ''

    if report_format == FundamentalFormat.RESTATED:
        restated = '_R'
    else:
        restated = ''
    ds_id = f'FF_{basic}{derived}{restated}_{FF_BASIS_TO_DATASET[report_basis]}_GLOBAL'
    ds = Dataset(ds_id)
    df = ds.get_data(bbid=asset.get_identifier(AssetIdentifier.BLOOMBERG_ID), start=start_new, end=end)
    if df.empty:
        raise MqValueError(f'No data found for {metric.value} for {asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)}')
    df.reset_index(inplace=True)
    column = 'ff' + metric.name.replace('_', ' ').title().replace(' ', '')
    df = df[['date', column]]
    date_range = pd.date_range(start=start_new, end=end, freq='D')
    date_df = pd.DataFrame({'date': date_range})
    df = pd.merge(date_df, df, on='date', how='left')
    df[column] = df[column].fillna(method='ffill')
    df = df[df['date'] >= pd.to_datetime(start)]
    df = df.sort_values(by='date', ascending=True).set_index('date')
    series = ExtendedSeries(df[column], name=metric.value)
    series.dataset_ids = ds.id

    return series


@plot_measure((AssetClass.Equity,), (AssetType.Single_Stock,))  # TO DO add query type
def factset_ratings(asset: Asset,
                    rating_type: RatingType = RatingType.BUY,
                    *, source: str = None, real_time: bool = False, request_id: Optional[str] = None) -> Series:
    """
    FactSet consensus ratings for single stocks, shows number of brokers for the rating type
    or a standardized numeric value representing the consensus of broker recommendations.

    :param asset: asset object loaded from security master
    :param rating_type: type of broker rating e.g. Buy
    :param source: name of function caller: default source = None
    :param real_time: whether to retrieve intraday data instead of EOD, real time is currently not supported
    :param request_id: service request id, if any
    :return: FactSet Ratings

    """
    start, end = DataContext.current.start_date, DataContext.current.end_date
    start_new = RelativeDate('-1y', base_date=start).apply_rule()
    ds_id = 'FE_BASIC_CONH_REC_GLOBAL'
    ds = Dataset(ds_id)
    df = ds.get_data(bbid=asset.get_identifier(AssetIdentifier.BLOOMBERG_ID), start=start_new, end=end)
    df.reset_index(inplace=True)
    df.fillna({'consEndDate': end}, inplace=True)
    df['date_range'] = df.apply(lambda row: pd.date_range(row['date'], row['consEndDate']), axis=1)
    df = df.explode('date_range').drop(columns=['date', 'consEndDate']).rename(
        columns={'date_range': 'date'})
    df = df[df['date'] >= pd.to_datetime(start)]
    df = df.sort_values(by='date', ascending=True).set_index('date')
    series = ExtendedSeries(df[RATING_TO_FIELD[rating_type]], name=rating_type.value)
    series.dataset_ids = ds.id

    return series
