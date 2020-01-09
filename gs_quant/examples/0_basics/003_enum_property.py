"""
Some available properties are enums available in the common modules.
'Currency' is an enum. To see possible values in Pycharm type'Currency. and in Jupyter, use autocomplete (tab)
"""

from gs_quant.common import PayReceive, Currency  # import constants
from gs_quant.instrument import IRSwap  # import instruments
from gs_quant.session import Environment, GsSession  # import sessions

client_id = None  # Supply your application id
client_secret = None  # Supply your client secret
scopes = ('run_analytics',)
GsSession.use(Environment.PROD, client_id, client_secret, scopes)

my_swap = IRSwap(PayReceive.Pay, '5y', Currency.AED)  # 5y USD payer
list(Currency)  # enumerate values of Currency enum
