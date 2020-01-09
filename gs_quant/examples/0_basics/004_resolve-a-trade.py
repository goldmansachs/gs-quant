""""

Calling the `resolve()` method will resolve any relative parameters to absolute values and
fill in unspecified parameters

`resolve()` will change the state of the instrument object in place by default unless argument `in_place' is False
`resolve` can be used to "fix" the instrument parameters when evaluating pricing & risk.

"""

from gs_quant.common import PayReceive, Currency  # import constants
from gs_quant.instrument import IRSwap  # import instruments
from gs_quant.session import Environment, GsSession  # import sessions

client_id = None  # Supply your application id
client_secret = None  # Supply your client secret
scopes = ('run_analytics',)
GsSession.use(Environment.PROD, client_id, client_secret, scopes)

my_swap = IRSwap(PayReceive.Pay, '5y', Currency.USD)  # 5y USD payer
print(my_swap.resolve(in_place=False).as_dict())
