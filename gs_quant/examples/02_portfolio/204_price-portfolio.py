
# Price a portfolio to obtain instrument specific and portfolio level pricing


from gs_quant.common import PayReceive, Currency  # import constants
from gs_quant.instrument import IRSwaption  # import instruments
from gs_quant.markets.portfolio import Portfolio
from gs_quant.session import Environment, GsSession  # import sessions

client_id = None  # Supply your application id
client_secret = None  # Supply your client secret
scopes = ('run_analytics',)
GsSession.use(Environment.PROD, client_id, client_secret, scopes)

swaption1 = IRSwaption(PayReceive.Pay, '5y', Currency.EUR, expiration_date='3m', name='EUR-3m5y')
swaption2 = IRSwaption(PayReceive.Pay, '5y', Currency.EUR, expiration_date='6m', name='EUR-6m5y')
portfolio = Portfolio((swaption1, swaption2))

# price of individual instrument
price_result = portfolio.price()
print(price_result['EUR-3m5y'])

# price for entire portfolio
price_agg = price_result.aggregate()
print(price_agg)
