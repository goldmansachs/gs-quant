"""
Copyright 2019 Goldman Sachs.
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

from gs_quant.base import *
from gs_quant.common import *
import datetime
from typing import Dict, Optional, Tuple, Union
from dataclasses import dataclass, field
from dataclasses_json import LetterCase, config, dataclass_json
from gs_quant.instrument.core import Instrument, resolution_safe


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class AssetRef(Instrument):
    buy_sell: Optional[BuySell] = None
    product_code: Optional[ProductCode] = None
    size: Optional[float] = None
    asset_id: Optional[str] = None
    number_of_options: Optional[float] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Cross_Asset)
    type_: Optional[AssetType] = field(init=False, default=AssetType.Any, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Bond(Instrument):
    buy_sell: Optional[BuySell] = None
    identifier: Optional[str] = None
    identifier_type: Optional[UnderlierType] = None
    size: Optional[float] = None
    settlement_date: Optional[Union[datetime.date, str]] = None
    settlement_currency: Optional[Currency] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Cross_Asset)
    type_: Optional[AssetType] = field(init=False, default=AssetType.Bond, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Cash(Instrument):
    currency: Optional[Currency] = None
    payment_date: Optional[datetime.date] = None
    notional_amount: Optional[Union[float, str]] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Cash)
    type_: Optional[AssetType] = field(init=False, default=AssetType.Cash, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CommodOTCOptionPeriod(Instrument):
    start: Optional[Union[datetime.date, str]] = None
    end: Optional[Union[datetime.date, str]] = None
    quantity: Optional[Union[float, str]] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Commod)
    type_: Optional[AssetType] = field(init=False, default=AssetType.OptionPeriod, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CommodOTCSwapLeg(Instrument):
    fixing_currency: Optional[CurrencyName] = None
    leg_description: Optional[str] = None
    contract: Optional[str] = None
    fixing_currency_source: Optional[str] = None
    underlier: Optional[str] = None
    quantity_multiplier: Optional[int] = None
    fixed_price: Optional[Union[float, str]] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Commod)
    type_: Optional[AssetType] = field(init=False, default=AssetType.SwapLeg, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CommodSwap(Instrument):
    commodity: Optional[str] = None
    quantity: Optional[Union[float, str]] = None
    contract: Optional[str] = None
    fixing_currency_source: Optional[str] = None
    start: Optional[Union[datetime.date, str]] = None
    floating_type: Optional[str] = None
    number_of_periods: Optional[int] = None
    quantity_unit: Optional[str] = None
    fixed_price: Optional[Union[float, str]] = None
    settlement: Optional[str] = None
    fixing_currency: Optional[CurrencyName] = None
    fixed_price_unit: Optional[str] = None
    commodity_reference_price: Optional[str] = None
    end: Optional[Union[datetime.date, str]] = None
    quantity_period: Optional[Period] = None
    strategy: Optional[str] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Commod)
    type_: Optional[AssetType] = field(init=False, default=AssetType.Swap, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class EqAutoroll(Instrument):
    underlier: Optional[Union[float, str]] = None
    expiration_date: Optional[Union[datetime.date, str]] = None
    first_fixing_date: Optional[Union[datetime.date, str]] = None
    last_fixing_date: Optional[Union[datetime.date, str]] = None
    fixing_frequency: Optional[str] = None
    trigger_level: Optional[float] = None
    buffer_level: Optional[float] = None
    local_return_cap: Optional[float] = None
    upside_leverage: Optional[float] = None
    initial_fixing_override: Optional[float] = None
    notional: Optional[Union[float, str]] = None
    business_day_calendar: Optional[str] = None
    payment_currency: Optional[Currency] = None
    settlement_delay: Optional[str] = None
    underlier_type: Optional[UnderlierType] = None
    buy_sell: Optional[BuySell] = None
    premium: Optional[float] = None
    premium_payment_date: Optional[Union[datetime.date, str]] = None
    premium_currency: Optional[Currency] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Equity)
    type_: Optional[AssetType] = field(init=False, default=AssetType.Autoroll, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class EqBinary(Instrument):
    underlier: Optional[Union[float, str]] = None
    buy_sell: Optional[BuySell] = None
    option_type: Optional[OptionType] = None
    expiration_date: Optional[Union[datetime.date, str]] = None
    settlement_date: Optional[Union[datetime.date, str]] = None
    strike_price: Optional[Union[float, str]] = None
    notional_amount: Optional[Union[float, str]] = None
    currency: Optional[str] = None
    premium: Optional[Union[float, str]] = None
    premium_settlement_date: Optional[Union[datetime.date, str]] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Equity)
    type_: Optional[AssetType] = field(init=False, default=AssetType.Binary, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class EqCliquet(Instrument):
    return_style: Optional[str] = 'Rate of Return'
    last_valuation_date: Optional[datetime.date] = None
    notional_amount: Optional[Union[float, str]] = None
    underlier_type: Optional[UnderlierType] = None
    underlier: Optional[Union[float, str]] = None
    payment_frequency: Optional[str] = 'Maturity'
    global_cap: Optional[float] = 1000000.0
    first_valuation_date: Optional[datetime.date] = None
    currency: Optional[Currency] = None
    global_floor: Optional[float] = -1000000.0
    strike_price: Optional[float] = None
    return_type: Optional[str] = 'Sum'
    valuation_period: Optional[str] = None
    expiration_date: Optional[Union[datetime.date, str]] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Equity)
    type_: Optional[AssetType] = field(init=False, default=AssetType.Cliquet, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class EqConvertibleBond(Instrument):
    underlier: Optional[Union[float, str]] = None
    underlier_type: Optional[UnderlierType] = None
    premium_settlement_date: Optional[Union[datetime.date, str]] = None
    ref_currency: Optional[Currency] = None
    buy_sell: Optional[BuySell] = None
    quantity: Optional[float] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Equity)
    type_: Optional[AssetType] = field(init=False, default=AssetType.Convertible, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class EqForward(Instrument):
    underlier: Optional[Union[float, str]] = None
    underlier_type: Optional[UnderlierType] = None
    expiration_date: Optional[Union[datetime.date, str]] = None
    forward_price: Optional[float] = None
    number_of_shares: Optional[int] = 1
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Equity)
    type_: Optional[AssetType] = field(init=False, default=AssetType.Forward, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class EqFuture(Instrument):
    total_quantity: float = None
    identifier: Optional[str] = None
    identifier_type: Optional[UnderlierType] = None
    underlier: Optional[str] = None
    multiplier: Optional[float] = None
    expiration_date: Optional[Union[datetime.date, str]] = None
    buy_sell: Optional[BuySell] = None
    quantity: Optional[float] = None
    currency: Optional[Currency] = None
    traded_price: Optional[float] = 0.0
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Equity)
    type_: Optional[AssetType] = field(init=False, default=AssetType.Future, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class EqOption(Instrument):
    underlier: Optional[Union[float, str]] = None
    expiration_date: Optional[Union[datetime.date, str]] = None
    strike_price: Optional[Union[float, str]] = None
    option_type: Optional[OptionType] = None
    option_style: Optional[OptionStyle] = None
    number_of_options: Optional[Union[float, str]] = None
    exchange: Optional[str] = None
    multiplier: Optional[float] = None
    settlement_date: Optional[Union[datetime.date, str]] = None
    settlement_currency: Optional[Currency] = None
    premium: Optional[float] = 0.0
    premium_payment_date: Optional[Union[datetime.date, str]] = None
    valuation_time: Optional[ValuationTime] = None
    method_of_settlement: Optional[OptionSettlementMethod] = None
    underlier_type: Optional[UnderlierType] = None
    buy_sell: Optional[BuySell] = None
    premium_currency: Optional[Currency] = None
    trade_as: Optional[TradeAs] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Equity)
    type_: Optional[AssetType] = field(init=False, default=AssetType.Option, metadata=config(field_name='type'))

    def scale_in_place(self, scaling: Optional[float] = None):
        if self.unresolved is None:
            raise RuntimeError('Can only scale resolved instruments')
        if scaling is None or scaling == 1:
            return
    
        if scaling < 0:
            flip_dict = {BuySell.Buy: BuySell.Sell, BuySell.Sell: BuySell.Buy}
            self.buy_sell = flip_dict[self.buy_sell]
            
        self.number_of_options *= abs(scaling)
        return


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class EqOptionLeg(Instrument):
    method_of_settlement: Optional[OptionSettlementMethod] = None
    premium_payment_date: Optional[Union[datetime.date, str]] = None
    buy_sell: Optional[BuySell] = None
    option_style: Optional[OptionStyle] = None
    multiplier: Optional[float] = None
    number_of_options: Optional[float] = None
    settlement_date: Optional[Union[datetime.date, str]] = None
    valuation_time: Optional[ValuationTime] = None
    option_type: Optional[OptionType] = None
    settlement_currency: Optional[Currency] = None
    premium: Optional[float] = None
    premium_currency: Optional[Currency] = None
    trade_as: Optional[TradeAs] = None
    exchange: Optional[str] = None
    strike_price: Optional[Union[float, str]] = None
    expiration_date: Optional[Union[datetime.date, str]] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Equity)
    type_: Optional[AssetType] = field(init=False, default=AssetType.OptionLeg, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class EqStock(Instrument):
    identifier: Optional[str] = None
    identifier_type: Optional[UnderlierType] = None
    buy_sell: Optional[BuySell] = None
    traded_price: Optional[float] = 0.0
    currency: Optional[Currency] = None
    quantity: Optional[float] = None
    settlement_date: Optional[datetime.date] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Equity)
    type_: Optional[AssetType] = field(init=False, default=AssetType.Single_Stock, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class EqSynthetic(Instrument):
    underlier: Union[float, str] = None
    expiry: str = None
    currency: Optional[Currency] = None
    swap_type: Optional[str] = 'Eq Swap'
    buy_sell: Optional[BuySell] = None
    underlier_type: Optional[UnderlierType] = None
    effective_date: Optional[datetime.date] = None
    num_of_underlyers: Optional[float] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Equity)
    type_: Optional[AssetType] = field(init=False, default=AssetType.Synthetic, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class EqVarianceSwap(Instrument):
    underlier: Optional[Union[float, str]] = None
    underlier_type: Optional[UnderlierType] = None
    expiration_date: Optional[Union[datetime.date, str]] = None
    strike_price: Optional[Union[float, str]] = None
    variance_cap: Optional[float] = None
    settlement_date: Optional[Union[datetime.date, str]] = None
    premium: Optional[Union[float, str]] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Equity)
    type_: Optional[AssetType] = field(init=False, default=AssetType.VarianceSwap, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FXBinary(Instrument):
    pair: Optional[str] = None
    buy_sell: Optional[BuySell] = None
    option_type: Optional[OptionType] = None
    notional_amount: Optional[Union[float, str]] = None
    notional_currency: Optional[Currency] = None
    strike_price: Optional[Union[float, str]] = None
    settlement_date: Optional[Union[datetime.date, str]] = None
    expiration_date: Optional[Union[datetime.date, str]] = None
    expiration_time: Optional[str] = None
    premium: Optional[Union[float, str]] = None
    premium_currency: Optional[Currency] = None
    premium_payment_date: Optional[str] = None
    settlement_rate_option: Optional[str] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.FX)
    type_: Optional[AssetType] = field(init=False, default=AssetType.Binary, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FXDoubleKnockout(Instrument):
    pair: Optional[str] = None
    buy_sell: Optional[BuySell] = None
    option_type: Optional[OptionType] = None
    notional_amount: Optional[Union[float, str]] = None
    notional_currency: Optional[Currency] = None
    strike_price: Optional[Union[float, str]] = None
    settlement_date: Optional[Union[datetime.date, str]] = None
    settlement_currency: Optional[Currency] = None
    settlement_rate_option: Optional[str] = None
    method_of_settlement: Optional[OptionSettlementMethod] = None
    expiration_date: Optional[Union[datetime.date, str]] = None
    expiration_time: Optional[str] = None
    premium: Optional[Union[float, str]] = None
    premium_currency: Optional[Currency] = None
    premium_payment_date: Optional[str] = None
    knock_in_or_out: Optional[InOut] = None
    lower_barrier_level: Optional[Union[float, str]] = None
    upper_barrier_level: Optional[Union[float, str]] = None
    knockout_convention: Optional[KnockoutConvention] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.FX)
    type_: Optional[AssetType] = field(init=False, default=AssetType.DoubleKnockout, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FXDoubleOneTouch(Instrument):
    pair: Optional[str] = None
    buy_sell: Optional[BuySell] = None
    notional_amount: Optional[Union[float, str]] = None
    notional_currency: Optional[Currency] = None
    settlement_date: Optional[Union[datetime.date, str]] = None
    settlement_currency: Optional[Currency] = None
    settlement_rate_option: Optional[str] = None
    method_of_settlement: Optional[OptionSettlementMethod] = None
    expiration_date: Optional[Union[datetime.date, str]] = None
    expiration_time: Optional[str] = None
    premium: Optional[Union[float, str]] = None
    premium_currency: Optional[Currency] = None
    premium_payment_date: Optional[str] = None
    lower_barrier_level: Optional[Union[float, str]] = None
    upper_barrier_level: Optional[Union[float, str]] = None
    payout_type: Optional[PayoutType] = None
    knockout_convention: Optional[KnockoutConvention] = None
    touch_or_no_touch: Optional[TouchNoTouch] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.FX)
    type_: Optional[AssetType] = field(init=False, default=AssetType.DoubleTouch, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FXEuropeanKnockout(Instrument):
    pair: Optional[str] = None
    buy_sell: Optional[BuySell] = None
    option_type: Optional[OptionType] = None
    notional_amount: Optional[Union[float, str]] = None
    notional_currency: Optional[Currency] = None
    strike_price: Optional[Union[float, str]] = None
    settlement_date: Optional[Union[datetime.date, str]] = None
    settlement_currency: Optional[Currency] = None
    expiration_date: Optional[str] = None
    expiration_time: Optional[str] = None
    premium: Optional[Union[float, str]] = None
    premium_currency: Optional[Currency] = None
    premium_payment_date: Optional[str] = None
    settlement_rate_option: Optional[str] = None
    method_of_settlement: Optional[OptionSettlementMethod] = None
    barrier_level: Optional[Union[float, str]] = None
    knock_up_or_down: Optional[UpDown] = None
    knock_in_or_out: Optional[InOut] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.FX)
    type_: Optional[AssetType] = field(init=False, default=AssetType.EuropeanKnockout, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FXForward(Instrument):
    pair: Optional[str] = None
    settlement_date: Optional[Union[datetime.date, str]] = None
    forward_rate: Optional[Union[float, str]] = None
    notional_amount: Optional[Union[float, str]] = None
    notional_currency: Optional[Currency] = None
    notional_amount_in_other_currency: Optional[Union[float, str]] = None
    buy_sell: Optional[BuySell] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.FX)
    type_: Optional[AssetType] = field(init=False, default=AssetType.Forward, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FXKnockout(Instrument):
    pair: Optional[str] = None
    buy_sell: Optional[BuySell] = None
    option_type: Optional[OptionType] = None
    notional_amount: Optional[Union[float, str]] = None
    notional_currency: Optional[Currency] = None
    strike_price: Optional[Union[float, str]] = None
    settlement_date: Optional[Union[datetime.date, str]] = None
    settlement_currency: Optional[Currency] = None
    settlement_rate_option: Optional[str] = None
    method_of_settlement: Optional[OptionSettlementMethod] = None
    expiration_date: Optional[Union[datetime.date, str]] = None
    expiration_time: Optional[str] = None
    premium: Optional[Union[float, str]] = None
    premium_currency: Optional[Currency] = None
    premium_payment_date: Optional[str] = None
    knock_in_or_out: Optional[InOut] = None
    knock_up_or_down: Optional[UpDown] = None
    barrier_level: Optional[Union[float, str]] = None
    knockout_convention: Optional[KnockoutConvention] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.FX)
    type_: Optional[AssetType] = field(init=False, default=AssetType.Knockout, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FXMultiCrossBinaryLeg(Instrument):
    pair: Optional[str] = None
    option_type: Optional[OptionType] = None
    strike_price: Optional[Union[float, str]] = None
    fixing_source: Optional[str] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.FX)
    type_: Optional[AssetType] = field(init=False, default=AssetType.MultiCrossBinaryLeg, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FXOneTouch(Instrument):
    pair: Optional[str] = None
    buy_sell: Optional[BuySell] = None
    notional_amount: Optional[Union[float, str]] = None
    notional_currency: Optional[Currency] = None
    strike_price: Optional[Union[float, str]] = None
    settlement_date: Optional[Union[datetime.date, str]] = None
    settlement_currency: Optional[Currency] = None
    settlement_rate_option: Optional[str] = None
    method_of_settlement: Optional[OptionSettlementMethod] = None
    expiration_date: Optional[Union[datetime.date, str]] = None
    expiration_time: Optional[str] = None
    premium: Optional[Union[float, str]] = None
    premium_currency: Optional[Currency] = None
    premium_payment_date: Optional[str] = None
    knock_up_or_down: Optional[UpDown] = None
    knockout_convention: Optional[KnockoutConvention] = None
    touch_or_no_touch: Optional[TouchNoTouch] = None
    payout_type: Optional[PayoutType] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.FX)
    type_: Optional[AssetType] = field(init=False, default=AssetType.OneTouch, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FXOption(Instrument):
    pair: Optional[str] = None
    buy_sell: Optional[BuySell] = None
    option_type: Optional[OptionType] = None
    notional_amount: Optional[Union[float, str]] = None
    notional_currency: Optional[Currency] = None
    notional_amount_in_other_currency: Optional[Union[float, str]] = None
    strike_price: Optional[Union[float, str]] = None
    settlement_date: Optional[Union[datetime.date, str]] = None
    settlement_currency: Optional[Currency] = None
    settlement_rate_option: Optional[str] = None
    method_of_settlement: Optional[OptionSettlementMethod] = None
    expiration_date: Optional[Union[datetime.date, str]] = None
    expiration_time: Optional[str] = None
    premium: Optional[Union[float, str]] = None
    premium_currency: Optional[Currency] = None
    premium_payment_date: Optional[str] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.FX)
    type_: Optional[AssetType] = field(init=False, default=AssetType.Option, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FXOptionLeg(Instrument):
    buy_sell: Optional[BuySell] = None
    option_type: Optional[OptionType] = None
    notional_amount: Optional[Union[float, str]] = None
    notional_currency: Optional[Currency] = None
    notional_amount_in_other_currency: Optional[Union[float, str]] = None
    strike_price: Optional[Union[float, str]] = None
    expiration_date: Optional[Union[datetime.date, str]] = None
    settlement_date: Optional[Union[datetime.date, str]] = None
    premium: Optional[Union[float, str]] = None
    premium_currency: Optional[Currency] = None
    premium_payment_date: Optional[str] = None
    settlement_currency: Optional[Currency] = None
    settlement_rate_option: Optional[str] = None
    method_of_settlement: Optional[OptionSettlementMethod] = None
    expiration_time: Optional[str] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.FX)
    type_: Optional[AssetType] = field(init=False, default=AssetType.OptionLeg, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FXShiftingBermForward(Instrument):
    pair: Optional[str] = None
    buy_sell: Optional[BuySell] = None
    notional_amount: Optional[Union[float, str]] = None
    notional_currency: Optional[Currency] = None
    notional_amount_in_other_currency: Optional[Union[float, str]] = None
    strike_price: Optional[Union[float, str]] = None
    settlement_date: Optional[Union[datetime.date, str]] = None
    settlement_currency: Optional[Currency] = None
    expiration_date: Optional[Union[datetime.date, str]] = None
    window_start_date: Optional[str] = None
    exercise_decision_freq: Optional[str] = None
    premium: Optional[Union[float, str]] = None
    premium_currency: Optional[Currency] = None
    premium_payment_date: Optional[str] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.FX)
    type_: Optional[AssetType] = field(init=False, default=AssetType.ShiftingBermForward, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FXTarfScheduleLeg(Instrument):
    profit_strike: Optional[Union[float, str]] = None
    loss_strike: Optional[Union[float, str]] = None
    fixing_date: Optional[Union[datetime.date, str]] = None
    payment_date: Optional[Union[datetime.date, str]] = None
    notional_amount: Optional[Union[float, str]] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.FX)
    type_: Optional[AssetType] = field(init=False, default=AssetType.TarfScheduleLeg, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FXVolatilitySwap(Instrument):
    pair: Optional[str] = None
    buy_sell: Optional[BuySell] = None
    strike_vol: Optional[Union[float, str]] = None
    notional_currency: Optional[Currency] = None
    notional_amount: Optional[Union[float, str]] = None
    first_fixing_date: Optional[Union[datetime.date, str]] = None
    last_fixing_date: Optional[Union[datetime.date, str]] = None
    settlement_date: Optional[Union[datetime.date, str]] = None
    fixing_source: Optional[str] = None
    fixing_frequency: Optional[str] = None
    annualization_factor: Optional[float] = None
    calculate_mean_return: Optional[float] = 0.0
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.FX)
    type_: Optional[AssetType] = field(init=False, default=AssetType.VolatilitySwap, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Forward(Instrument):
    currency: Optional[Currency] = None
    expiration_date: Optional[Union[datetime.date, str]] = None
    notional_amount: Optional[Union[float, str]] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Cash)
    type_: Optional[AssetType] = field(init=False, default=AssetType.Forward, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class IRBondFuture(Instrument):
    buy_sell: Optional[BuySell] = None
    notional_amount: Optional[Union[float, str]] = None
    underlier: Optional[Union[float, str]] = None
    currency: Optional[Currency] = None
    expiration_date: Optional[Union[datetime.date, str]] = None
    exchange: Optional[str] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Rates)
    type_: Optional[AssetType] = field(init=False, default=AssetType.BondFuture, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class IRCap(Instrument):
    termination_date: Optional[Union[datetime.date, str]] = None
    notional_currency: Optional[Currency] = None
    notional_amount: Optional[Union[float, str]] = None
    effective_date: Optional[Union[datetime.date, str]] = None
    floating_rate_option: Optional[str] = None
    floating_rate_designated_maturity: Optional[str] = None
    floating_rate_frequency: Optional[str] = None
    floating_rate_day_count_fraction: Optional[DayCountFraction] = None
    floating_rate_business_day_convention: Optional[BusinessDayConvention] = None
    cap_rate: Optional[Union[float, str]] = None
    premium: Optional[Union[float, str]] = None
    premium_payment_date: Optional[Union[datetime.date, str]] = None
    fee: Optional[float] = 0.0
    fee_currency: Optional[Currency] = None
    fee_payment_date: Optional[Union[datetime.date, str]] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Rates)
    type_: Optional[AssetType] = field(init=False, default=AssetType.Cap, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class IRFloor(Instrument):
    termination_date: Optional[Union[datetime.date, str]] = None
    notional_currency: Optional[Currency] = None
    notional_amount: Optional[Union[float, str]] = None
    effective_date: Optional[Union[datetime.date, str]] = None
    floating_rate_option: Optional[str] = None
    floating_rate_designated_maturity: Optional[str] = None
    floating_rate_frequency: Optional[str] = None
    floating_rate_day_count_fraction: Optional[DayCountFraction] = None
    floating_rate_business_day_convention: Optional[BusinessDayConvention] = None
    floor_rate: Optional[Union[float, str]] = None
    premium: Optional[Union[float, str]] = None
    premium_payment_date: Optional[Union[datetime.date, str]] = None
    fee: Optional[float] = 0.0
    fee_currency: Optional[Currency] = None
    fee_payment_date: Optional[Union[datetime.date, str]] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Rates)
    type_: Optional[AssetType] = field(init=False, default=AssetType.Floor, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class InflationSwap(Instrument):
    pay_or_receive: Optional[PayReceive] = None
    termination_date: Optional[Union[datetime.date, str]] = None
    notional_currency: Optional[Currency] = None
    effective_date: Optional[Union[datetime.date, str]] = None
    notional_amount: Optional[Union[float, str]] = None
    index: Optional[str] = None
    floating_rate_business_day_convention: Optional[BusinessDayConvention] = None
    fixed_rate: Optional[Union[float, str]] = None
    fixed_rate_business_day_convention: Optional[BusinessDayConvention] = None
    fee: Optional[float] = 0.0
    base_cpi: Optional[float] = None
    clearing_house: Optional[SwapClearingHouse] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Rates)
    type_: Optional[AssetType] = field(init=False, default=AssetType.InflationSwap, metadata=config(field_name='type'))

    def scale_in_place(self, scaling: Optional[float] = None):
        if self.unresolved is None:
            raise RuntimeError('Can only scale resolved instruments')
        if scaling is None or scaling == 1:
            return
    
        if scaling < 0:
            flip_dict = {PayReceive.Pay: PayReceive.Receive, PayReceive.Receive: PayReceive.Pay}
            self.pay_or_receive = flip_dict[self.pay_or_receive]
            self.fee *= -1
        self.notional_amount *= abs(scaling)
        return


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class InstrumentsRepoIRDiscreteLock(Instrument):
    buy_sell: Optional[BuySell] = None
    underlier: Optional[Union[float, str]] = None
    underlier_type: Optional[UnderlierType] = None
    settlement_date: Optional[Union[datetime.date, str]] = None
    notional_amount: Optional[Union[float, str]] = None
    currency: Optional[Currency] = None
    spot_clean_price: Optional[float] = None
    settlement: Optional[str] = None
    repo_rate: Optional[float] = None
    forward_clean_price: Optional[float] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Repo)
    type_: Optional[AssetType] = field(init=False, default=AssetType.Bond_Forward, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CDIndex(Instrument):
    buy_sell: Optional[BuySell] = None
    clearinghouse: Optional[SwapClearingHouse] = None
    effective_date: Optional[Union[datetime.date, str]] = None
    settlement_date: Optional[Union[datetime.date, str]] = None
    notional_amount: Optional[Union[float, str]] = None
    notional_currency: Optional[Currency] = None
    first_payment_date: Optional[Union[datetime.date, str]] = None
    first_roll_date: Optional[Union[datetime.date, str]] = None
    fee: Optional[float] = 0.0
    fee_currency: Optional[Currency] = None
    fee_payment_date: Optional[Union[datetime.date, str]] = None
    termination_date: Optional[Union[datetime.date, str]] = None
    index_family: Optional[str] = None
    index_for_basis: Optional[str] = None
    index_series: Optional[float] = None
    index_version: Optional[float] = None
    isda_docs: Optional[str] = field(default='2014', metadata=config(field_name='ISDADocs'))
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Credit)
    type_: Optional[AssetType] = field(init=False, default=AssetType.Index, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CDIndexOption(Instrument):
    automatic_exercise: Optional[float] = 0.0
    buy_sell: Optional[BuySell] = None
    clearinghouse: Optional[SwapClearingHouse] = None
    notional_currency: Optional[Currency] = None
    earliest_exercise_time: Optional[str] = None
    earliest_exercise_time_centre: Optional[str] = None
    effective_date: Optional[Union[datetime.date, str]] = None
    exercise_date_business_day_convention: Optional[BusinessDayConvention] = 'Following'
    exercise_holidays: Optional[str] = None
    expiration_date: Optional[Union[datetime.date, str]] = None
    expiration_time: Optional[str] = None
    expiration_time_centre: Optional[str] = None
    premium: Optional[float] = 0.0
    premium_currency: Optional[Currency] = None
    premium_payment_date: Optional[Union[datetime.date, str]] = None
    first_payment_date: Optional[Union[datetime.date, str]] = None
    first_roll_date: Optional[Union[datetime.date, str]] = None
    index_family: Optional[str] = None
    index_for_basis: Optional[str] = None
    index_series: Optional[float] = None
    index_version: Optional[float] = None
    isda_docs: Optional[str] = field(default='2014', metadata=config(field_name='ISDADocs'))
    termination_date: Optional[Union[datetime.date, str]] = None
    option_type: Optional[OptionType] = None
    method_of_settlement: Optional[OptionSettlementMethod] = None
    notional_amount: Optional[Union[float, str]] = None
    fixed_rate: Optional[float] = None
    strike: Optional[Union[float, str]] = None
    strike_type: Optional[str] = 'Spread'
    settlement_date: Optional[Union[datetime.date, str]] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Credit)
    type_: Optional[AssetType] = field(init=False, default=AssetType.IndexOption, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CommodOTCOptionLeg(Instrument):
    option_type: Optional[OptionType] = None
    fixing_currency: Optional[CurrencyName] = None
    premium: Optional[CommodPrice] = None
    leg_description: Optional[str] = None
    contract: Optional[str] = None
    fixing_currency_source: Optional[str] = None
    strike: Optional[Union[float, str]] = None
    underlier: Optional[str] = None
    premium_settlement: Optional[str] = None
    quantity_multiplier: Optional[int] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Commod)
    type_: Optional[AssetType] = field(init=False, default=AssetType.OptionLeg, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CommodOTCSwap(Instrument):
    quantity: Optional[Union[float, str]] = None
    legs: Optional[Tuple[CommodOTCSwapLeg, ...]] = None
    start: Optional[Union[datetime.date, str]] = None
    end: Optional[Union[datetime.date, str]] = None
    number_of_periods: Optional[int] = None
    quantity_unit: Optional[str] = None
    quantity_period: Optional[Period] = None
    strategy: Optional[str] = None
    settlement: Optional[str] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Commod)
    type_: Optional[AssetType] = field(init=False, default=AssetType.SwapStrategy, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CommodOption(Instrument):
    commodity: Optional[str] = None
    number_of_periods: Optional[int] = None
    quantity_unit: Optional[str] = None
    currency_summary: Optional[CurrencyName] = None
    option_types: Optional[Tuple[str, ...]] = None
    settlement: Optional[str] = None
    option_type: Optional[str] = None
    strike_unit: Optional[str] = None
    strikes: Optional[Tuple[str, ...]] = None
    end: Optional[Union[datetime.date, str]] = None
    buy_sells: Optional[Tuple[str, ...]] = None
    underlier_short_name: Optional[str] = None
    settlement_frequency: Optional[str] = None
    buy_sell: Optional[BuySell] = None
    strike_currency: Optional[CurrencyName] = None
    quantity: Optional[Union[float, str]] = None
    contract: Optional[str] = None
    fixing_currency_source: Optional[str] = None
    strike: Optional[str] = None
    start: Optional[Union[datetime.date, str]] = None
    floating_type: Optional[str] = None
    fixing_currency: Optional[CurrencyName] = None
    commodity_reference_price: Optional[str] = None
    quantity_period: Optional[str] = None
    strategy: Optional[str] = None
    premium: Optional[str] = None
    period_details: Optional[Tuple[CommodOTCOptionPeriod, ...]] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Commod)
    type_: Optional[AssetType] = field(init=False, default=AssetType.Option, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CommodVolVarSwap(Instrument):
    notional_currency: Optional[CurrencyName] = None
    notional: Optional[float] = 1.0
    floating_rate_is_capped: Optional[str] = None
    end_date: Optional[Union[datetime.date, str]] = None
    margined: Optional[float] = None
    market_disruption_agreement: Optional[str] = None
    mean_rule: Optional[CommodMeanRule] = None
    divisor: Optional[str] = None
    fixed_mean: Optional[float] = None
    first_fixing: Optional[Union[float, str]] = None
    floating_rate_cap: Optional[float] = None
    fx_fixing_source: Optional[str] = None
    annualization_factor: Optional[float] = None
    buy_sell: Optional[BuySell] = None
    contract: Optional[str] = None
    strike: Optional[Union[float, str]] = None
    swap_type: Optional[str] = None
    settlement_date: Optional[Union[datetime.date, str]] = None
    fixing_currency: Optional[CurrencyName] = None
    asset_fixing_source: Optional[str] = None
    sampling_frequency: Optional[str] = None
    variance_convention: Optional[VarianceConvention] = None
    extra_sampling_calendars: Optional[str] = '--Blank--'
    asset: Optional[str] = None
    start_date: Optional[Union[datetime.date, str]] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Commod)
    type_: Optional[AssetType] = field(init=False, default=AssetType.VolVarSwap, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class EqOptionStrategy(Instrument):
    underlier: Union[float, str] = None
    strategy: str = None
    legs: Tuple[EqOptionLeg, ...] = None
    underlier_type: Optional[UnderlierType] = None
    expiration_date: Optional[Union[datetime.date, str]] = None
    strike_price: Optional[Union[float, str]] = None
    option_type: Optional[OptionType] = None
    option_style: Optional[OptionStyle] = None
    number_of_options: Optional[float] = None
    multiplier: Optional[float] = None
    settlement_date: Optional[Union[datetime.date, str]] = None
    settlement_currency: Optional[Currency] = None
    premium: Optional[float] = None
    premium_payment_date: Optional[Union[datetime.date, str]] = None
    valuation_time: Optional[ValuationTime] = None
    method_of_settlement: Optional[OptionSettlementMethod] = None
    buy_sell: Optional[BuySell] = None
    premium_currency: Optional[Currency] = None
    exchange: Optional[str] = None
    trade_as: Optional[TradeAs] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Equity)
    type_: Optional[AssetType] = field(init=False, default=AssetType.OptionStrategy, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FRA(Instrument):
    buy_sell: Optional[BuySell] = None
    clearing_house: Optional[SwapClearingHouse] = None
    clearing_legally_binding: Optional[float] = None
    day_count_fraction: Optional[DayCountFraction] = None
    fee: Optional[float] = 0.0
    fee_currency: Optional[Currency] = None
    fee_payment_date: Optional[Union[datetime.date, str]] = None
    fixed_rate: Optional[Union[float, str]] = None
    frequency: Optional[str] = None
    calendar: Optional[str] = None
    rate_option: Optional[str] = None
    maturity: Optional[Union[datetime.date, str]] = None
    notional_currency: Optional[Currency] = None
    payment_delay: Optional[str] = None
    roll_convention: Optional[str] = None
    notional_amount: Optional[Union[float, str]] = None
    spread: Optional[Union[float, str]] = None
    effective_date: Optional[Union[datetime.date, str]] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Rates)
    type_: Optional[AssetType] = field(init=False, default=AssetType.FRA, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FXMultiCrossBinary(Instrument):
    legs: Tuple[FXMultiCrossBinaryLeg, ...] = None
    buy_sell: Optional[BuySell] = None
    notional_amount: Optional[Union[float, str]] = None
    notional_currency: Optional[Currency] = None
    settlement_date: Optional[Union[datetime.date, str]] = None
    expiration_date: Optional[Union[datetime.date, str]] = None
    expiration_time: Optional[str] = None
    premium: Optional[Union[float, str]] = None
    premium_currency: Optional[Currency] = None
    premium_payment_date: Optional[str] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.FX)
    type_: Optional[AssetType] = field(init=False, default=AssetType.MultiCrossBinary, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FXOptionStrategy(Instrument):
    pair: Optional[str] = None
    buy_sell: Optional[BuySell] = None
    strategy_name: Optional[str] = None
    legs: Optional[Tuple[FXOptionLeg, ...]] = None
    option_type: Optional[OptionType] = None
    notional_amount: Optional[Union[float, str]] = None
    notional_currency: Optional[Currency] = None
    notional_amount_in_other_currency: Optional[Union[float, str]] = None
    strike_price: Optional[Union[float, str]] = None
    settlement_date: Optional[Union[datetime.date, str]] = None
    settlement_currency: Optional[Currency] = None
    settlement_rate_option: Optional[str] = None
    method_of_settlement: Optional[OptionSettlementMethod] = None
    expiration_date: Optional[Union[datetime.date, str]] = None
    expiration_time: Optional[str] = None
    premium: Optional[Union[float, str]] = None
    premium_currency: Optional[Currency] = None
    premium_payment_date: Optional[str] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.FX)
    type_: Optional[AssetType] = field(init=False, default=AssetType.OptionStrategy, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class FXTarf(Instrument):
    pair: Optional[str] = None
    new_or_unwind: Optional[NewOrUnwind] = None
    notional_amount: Optional[Union[float, str]] = None
    notional_currency: Optional[Currency] = None
    profit_strike: Optional[Union[float, str]] = None
    loss_strike: Optional[Union[float, str]] = None
    settlement_date: Optional[Union[datetime.date, str]] = None
    settlement_currency: Optional[Currency] = None
    fixing_rate_option: Optional[str] = None
    method_of_settlement: Optional[OptionSettlementMethod] = None
    expiration_date: Optional[Union[datetime.date, str]] = None
    premium: Optional[Union[float, str]] = None
    premium_currency: Optional[Currency] = None
    premium_payment_date: Optional[str] = None
    long_or_short: Optional[LongShort] = None
    european_knock_in: Optional[Union[float, str]] = None
    number_of_expiry: Optional[Union[float, str]] = None
    coupon_frequency: Optional[str] = None
    first_fixing_date: Optional[Union[datetime.date, str]] = None
    leverage_ratio: Optional[Union[float, str]] = None
    target_type: Optional[TargetType] = None
    target: Optional[Union[float, str]] = None
    schedules: Optional[Tuple[FXTarfScheduleLeg, ...]] = None
    target_adj_notional_or_strike: Optional[NotionalOrStrike] = None
    payment_on_hitting_target: Optional[TargetPaymentType] = None
    settlement_rate_option: Optional[str] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.FX)
    type_: Optional[AssetType] = field(init=False, default=AssetType.Tarf, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class IRAssetSwapFxdFlt(Instrument):
    asw_type: Optional[AswType] = None
    clearing_house: Optional[SwapClearingHouse] = None
    fee: Optional[float] = None
    fee_currency: Optional[Currency] = None
    fee_payment_date: Optional[Union[datetime.date, str]] = None
    fixed_rate_day_count_fraction: Optional[DayCountFraction] = None
    fixed_first_stub: Optional[Union[datetime.date, str]] = None
    fixed_rate_frequency: Optional[str] = None
    fixed_holidays: Optional[str] = None
    fixed_rate_business_day_convention: Optional[BusinessDayConvention] = None
    fixed_rate: Optional[Union[float, str]] = None
    floating_rate_currency: Optional[Currency] = None
    floating_rate_day_count_fraction: Optional[DayCountFraction] = None
    floating_first_stub: Optional[Union[datetime.date, str]] = None
    floating_rate_frequency: Optional[str] = None
    floating_rate_fx: Optional[float] = None
    floating_holidays: Optional[str] = None
    floating_maturity: Optional[Union[datetime.date, str]] = None
    floating_rate_business_day_convention: Optional[BusinessDayConvention] = None
    identifier: Optional[str] = None
    identifier_type: Optional[str] = None
    floating_rate_option: Optional[str] = None
    floating_rate_designated_maturity: Optional[str] = None
    termination_date: Optional[Union[datetime.date, str]] = None
    pay_or_receive: Optional[PayReceive] = None
    roll_convention: Optional[str] = None
    notional_amount: Optional[Union[float, str]] = None
    floating_rate_spread: Optional[Union[float, str]] = None
    traded_clean_price: Optional[float] = 100.0
    settlement_date: Optional[Union[datetime.date, str]] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Rates)
    type_: Optional[AssetType] = field(init=False, default=AssetType.AssetSwapFxdFlt, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class IRAssetSwapFxdFxd(Instrument):
    asw_type: Optional[AswType] = None
    buy_sell: Optional[BuySell] = None
    fee: Optional[float] = None
    fee_currency: Optional[Currency] = None
    fee_payment_date: Optional[Union[datetime.date, str]] = None
    fixed_rate_day_count_fraction: Optional[DayCountFraction] = None
    fixed_first_stub: Optional[Union[datetime.date, str]] = None
    fixed_rate_frequency: Optional[str] = None
    fixed_holidays: Optional[str] = None
    fixed_rate_business_day_convention: Optional[BusinessDayConvention] = None
    fixed_rate: Optional[Union[float, str]] = None
    coupon: Optional[Union[float, str]] = None
    fixed_rate_currency: Optional[Currency] = None
    asset_day_count_fraction: Optional[DayCountFraction] = None
    asset_first_stub: Optional[Union[datetime.date, str]] = None
    asset_frequency: Optional[str] = None
    asset_holidays: Optional[str] = None
    asset_business_day_convention: Optional[BusinessDayConvention] = None
    identifier: Optional[str] = None
    identifier_type: Optional[str] = None
    asset_maturity: Optional[Union[datetime.date, str]] = None
    fixed_maturity: Optional[Union[datetime.date, str]] = None
    roll_convention: Optional[str] = None
    notional_amount: Optional[Union[float, str]] = None
    fixed_amount: Optional[Union[float, str]] = None
    clean_price: Optional[float] = 100.0
    settlement_date: Optional[Union[datetime.date, str]] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Rates)
    type_: Optional[AssetType] = field(init=False, default=AssetType.AssetSwapFxdFxd, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class IRBasisSwap(Instrument):
    termination_date: Optional[Union[datetime.date, str]] = None
    notional_amount: Optional[Union[float, str]] = None
    notional_currency: Optional[Currency] = None
    effective_date: Optional[Union[datetime.date, str]] = None
    principal_exchange: Optional[PrincipalExchange] = None
    payer_spread: Optional[Union[float, str]] = None
    payer_rate_option: Optional[str] = None
    payer_designated_maturity: Optional[str] = None
    payer_frequency: Optional[str] = None
    payer_day_count_fraction: Optional[DayCountFraction] = None
    payer_business_day_convention: Optional[BusinessDayConvention] = None
    receiver_spread: Optional[Union[float, str]] = None
    receiver_rate_option: Optional[str] = None
    receiver_designated_maturity: Optional[str] = None
    receiver_frequency: Optional[str] = None
    receiver_day_count_fraction: Optional[DayCountFraction] = None
    receiver_business_day_convention: Optional[BusinessDayConvention] = None
    fee: Optional[float] = 0.0
    fee_currency: Optional[Currency] = None
    fee_payment_date: Optional[Union[datetime.date, str]] = None
    clearing_house: Optional[SwapClearingHouse] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Rates)
    type_: Optional[AssetType] = field(init=False, default=AssetType.BasisSwap, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class IRBondOption(Instrument):
    underlier: Optional[Union[float, str]] = None
    notional_amount: Optional[Union[float, str]] = None
    expiration_date: Optional[Union[datetime.date, str]] = None
    option_type: Optional[OptionType] = None
    effective_date: Optional[Union[datetime.date, str]] = None
    strike: Optional[Union[float, str]] = None
    strike_type: Optional[BondStrikeType] = None
    premium: Optional[Union[float, str]] = None
    premium_payment_date: Optional[Union[datetime.date, str]] = None
    fee: Optional[float] = 0.0
    fee_currency: Optional[Currency] = None
    fee_payment_date: Optional[Union[datetime.date, str]] = None
    settlement: Optional[SettlementType] = None
    underlier_type: Optional[UnderlierType] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Rates)
    type_: Optional[AssetType] = field(init=False, default=AssetType.BondOption, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class IRCMSOption(Instrument):
    cap_floor: Optional[str] = None
    termination_date: Optional[Union[datetime.date, str]] = None
    notional_currency: Optional[Currency] = None
    notional_amount: Optional[Union[float, str]] = None
    effective_date: Optional[Union[datetime.date, str]] = None
    strike: Optional[Union[float, str]] = None
    index: Optional[str] = None
    multiplier: Optional[float] = None
    premium: Optional[Union[float, str]] = None
    premium_payment_date: Optional[Union[datetime.date, str]] = None
    fee: Optional[float] = 0.0
    fee_currency: Optional[Currency] = None
    fee_payment_date: Optional[Union[datetime.date, str]] = None
    buy_sell: Optional[BuySell] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Rates)
    type_: Optional[AssetType] = field(init=False, default=AssetType.CMSOption, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class IRCMSOptionStrip(Instrument):
    cap_floor: Optional[str] = None
    termination_date: Optional[Union[datetime.date, str]] = None
    notional_currency: Optional[Currency] = None
    notional_amount: Optional[Union[float, str]] = None
    effective_date: Optional[Union[datetime.date, str]] = None
    strike: Optional[Union[float, str]] = None
    index: Optional[str] = None
    floating_rate_frequency: Optional[str] = None
    floating_rate_day_count_fraction: Optional[DayCountFraction] = None
    floating_rate_business_day_convention: Optional[BusinessDayConvention] = None
    reset_delay: Optional[str] = None
    multiplier: Optional[float] = None
    premium: Optional[Union[float, str]] = None
    premium_payment_date: Optional[Union[datetime.date, str]] = None
    fee: Optional[float] = 0.0
    fee_currency: Optional[Currency] = None
    fee_payment_date: Optional[Union[datetime.date, str]] = None
    buy_sell: Optional[BuySell] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Rates)
    type_: Optional[AssetType] = field(init=False, default=AssetType.CMSOptionStrip, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class IRCMSSpreadOption(Instrument):
    cap_floor: Optional[str] = None
    termination_date: Optional[Union[datetime.date, str]] = None
    notional_currency: Optional[Currency] = None
    notional_amount: Optional[Union[float, str]] = None
    effective_date: Optional[Union[datetime.date, str]] = None
    strike: Optional[Union[float, str]] = None
    index1_tenor: Optional[str] = None
    index2_tenor: Optional[str] = None
    premium: Optional[Union[float, str]] = None
    premium_payment_date: Optional[Union[datetime.date, str]] = None
    fee: Optional[float] = 0.0
    fee_currency: Optional[Currency] = None
    fee_payment_date: Optional[Union[datetime.date, str]] = None
    buy_sell: Optional[BuySell] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Rates)
    type_: Optional[AssetType] = field(init=False, default=AssetType.CMSSpreadOption, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class IRCMSSpreadOptionStrip(Instrument):
    cap_floor: Optional[str] = None
    termination_date: Optional[Union[datetime.date, str]] = None
    notional_currency: Optional[Currency] = None
    notional_amount: Optional[Union[float, str]] = None
    effective_date: Optional[Union[datetime.date, str]] = None
    strike: Optional[Union[float, str]] = None
    index1: Optional[str] = None
    index2: Optional[str] = None
    floating_rate_frequency: Optional[str] = None
    floating_rate_day_count_fraction: Optional[DayCountFraction] = None
    floating_rate_business_day_convention: Optional[BusinessDayConvention] = None
    reset_delay: Optional[str] = None
    premium: Optional[Union[float, str]] = None
    premium_payment_date: Optional[Union[datetime.date, str]] = None
    fee: Optional[float] = 0.0
    fee_currency: Optional[Currency] = None
    fee_payment_date: Optional[Union[datetime.date, str]] = None
    buy_sell: Optional[BuySell] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Rates)
    type_: Optional[AssetType] = field(init=False, default=AssetType.CMSSpreadOptionStrip, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class IRFixedLeg(Instrument):
    buy_sell: Optional[BuySell] = None
    fixed_rate_day_count_fraction: Optional[DayCountFraction] = None
    fixed_first_stub: Optional[Union[datetime.date, str]] = None
    fixed_rate_frequency: Optional[str] = None
    fixed_holidays: Optional[str] = None
    fixed_last_stub: Optional[Union[datetime.date, str]] = None
    fixed_rate_business_day_convention: Optional[BusinessDayConvention] = None
    fixed_rate: Optional[Union[float, str]] = None
    termination_date: Optional[Union[datetime.date, str]] = None
    notional_currency: Optional[Currency] = None
    principal_exchange: Optional[PrincipalExchange] = None
    roll_convention: Optional[str] = None
    notional_amount: Optional[Union[float, str]] = None
    effective_date: Optional[Union[datetime.date, str]] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Rates)
    type_: Optional[AssetType] = field(init=False, default=AssetType.FixedLeg, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class IRFloatLeg(Instrument):
    buy_sell: Optional[BuySell] = None
    floating_rate_for_the_initial_calculation_period: Optional[float] = None
    floating_rate_day_count_fraction: Optional[DayCountFraction] = None
    floating_first_stub: Optional[Union[datetime.date, str]] = None
    floating_rate_frequency: Optional[str] = None
    floating_holidays: Optional[str] = None
    floating_last_stub: Optional[Union[datetime.date, str]] = None
    floating_rate_business_day_convention: Optional[BusinessDayConvention] = None
    floating_rate_option: Optional[str] = None
    floating_rate_designated_maturity: Optional[str] = None
    termination_date: Optional[Union[datetime.date, str]] = None
    notional_currency: Optional[Currency] = None
    principal_exchange: Optional[PrincipalExchange] = None
    roll_convention: Optional[str] = None
    notional_amount: Optional[Union[float, str]] = None
    floating_rate_spread: Optional[Union[float, str]] = None
    effective_date: Optional[Union[datetime.date, str]] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Rates)
    type_: Optional[AssetType] = field(init=False, default=AssetType.FloatLeg, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class IRSwap(Instrument):
    pay_or_receive: Optional[PayReceive] = None
    termination_date: Optional[Union[datetime.date, str]] = None
    notional_currency: Optional[Currency] = None
    notional_amount: Optional[Union[float, str]] = None
    effective_date: Optional[Union[datetime.date, str]] = None
    principal_exchange: Optional[PrincipalExchange] = None
    floating_rate_for_the_initial_calculation_period: Optional[float] = None
    floating_rate_option: Optional[str] = None
    floating_rate_designated_maturity: Optional[str] = None
    floating_rate_spread: Optional[Union[float, str]] = None
    floating_rate_frequency: Optional[str] = None
    floating_rate_day_count_fraction: Optional[DayCountFraction] = None
    floating_rate_business_day_convention: Optional[BusinessDayConvention] = None
    fixed_rate: Optional[Union[float, str]] = None
    fixed_rate_frequency: Optional[str] = None
    fixed_rate_day_count_fraction: Optional[DayCountFraction] = None
    fixed_rate_business_day_convention: Optional[BusinessDayConvention] = None
    fee: Optional[float] = 0.0
    fee_currency: Optional[Currency] = None
    fee_payment_date: Optional[Union[datetime.date, str]] = None
    clearing_house: Optional[SwapClearingHouse] = None
    fixed_first_stub: Optional[Union[datetime.date, str]] = None
    floating_first_stub: Optional[Union[datetime.date, str]] = None
    fixed_last_stub: Optional[Union[datetime.date, str]] = None
    floating_last_stub: Optional[Union[datetime.date, str]] = None
    fixed_holidays: Optional[str] = None
    floating_holidays: Optional[str] = None
    roll_convention: Optional[str] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Rates)
    type_: Optional[AssetType] = field(init=False, default=AssetType.Swap, metadata=config(field_name='type'))

    def scale_in_place(self, scaling: Optional[float] = None):
        if self.unresolved is None:
            raise RuntimeError('Can only scale resolved instruments')
        if scaling is None or scaling == 1:
            return
    
        if scaling < 0:
            flip_dict = {PayReceive.Pay: PayReceive.Receive, PayReceive.Receive: PayReceive.Pay}
            self.pay_or_receive = flip_dict[self.pay_or_receive]
            self.fee *= -1
        self.notional_amount *= abs(scaling)
        return


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class IRSwaption(Instrument):
    pay_or_receive: Optional[PayReceive] = None
    termination_date: Optional[Union[datetime.date, str]] = None
    notional_currency: Optional[Currency] = None
    effective_date: Optional[Union[datetime.date, str]] = None
    notional_amount: Optional[Union[float, str]] = None
    expiration_date: Optional[Union[datetime.date, str]] = None
    floating_rate_option: Optional[str] = None
    floating_rate_designated_maturity: Optional[str] = None
    floating_rate_spread: Optional[float] = None
    floating_rate_frequency: Optional[str] = None
    floating_rate_day_count_fraction: Optional[DayCountFraction] = None
    floating_rate_business_day_convention: Optional[BusinessDayConvention] = None
    fixed_rate_frequency: Optional[str] = None
    fixed_rate_day_count_fraction: Optional[DayCountFraction] = None
    fixed_rate_business_day_convention: Optional[BusinessDayConvention] = None
    strike: Optional[Union[float, str]] = None
    premium: Optional[Union[float, str]] = None
    premium_payment_date: Optional[Union[datetime.date, str]] = None
    fee: Optional[float] = 0.0
    fee_currency: Optional[Currency] = None
    fee_payment_date: Optional[Union[datetime.date, str]] = None
    clearing_house: Optional[SwapClearingHouse] = None
    settlement: Optional[SwapSettlement] = None
    buy_sell: Optional[BuySell] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Rates)
    type_: Optional[AssetType] = field(init=False, default=AssetType.Swaption, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class IRXccySwap(Instrument):
    termination_date: Optional[Union[datetime.date, str]] = None
    notional_amount: Optional[float] = None
    effective_date: Optional[Union[datetime.date, str]] = None
    principal_exchange: Optional[PrincipalExchange] = None
    payer_currency: Optional[Currency] = None
    payer_spread: Optional[Union[float, str]] = None
    payer_rate_option: Optional[str] = None
    payer_designated_maturity: Optional[str] = None
    payer_frequency: Optional[str] = None
    payer_day_count_fraction: Optional[DayCountFraction] = None
    payer_business_day_convention: Optional[BusinessDayConvention] = None
    receiver_currency: Optional[Currency] = None
    receiver_spread: Optional[Union[float, str]] = None
    receiver_rate_option: Optional[str] = None
    receiver_designated_maturity: Optional[str] = None
    receiver_frequency: Optional[str] = None
    receiver_day_count_fraction: Optional[DayCountFraction] = None
    receiver_business_day_convention: Optional[BusinessDayConvention] = None
    fee: Optional[float] = 0.0
    fee_currency: Optional[Currency] = None
    fee_payment_date: Optional[Union[datetime.date, str]] = None
    initial_fx_rate: Optional[float] = None
    payer_first_stub: Optional[Union[datetime.date, str]] = None
    receiver_first_stub: Optional[Union[datetime.date, str]] = None
    payer_last_stub: Optional[Union[datetime.date, str]] = None
    receiver_last_stub: Optional[Union[datetime.date, str]] = None
    payer_holidays: Optional[str] = None
    receiver_holidays: Optional[str] = None
    notional_reset_side: Optional[PayReceive] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Rates)
    type_: Optional[AssetType] = field(init=False, default=AssetType.XccySwapMTM, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class IRXccySwapFixFix(Instrument):
    termination_date: Optional[Union[datetime.date, str]] = None
    notional_amount: Optional[float] = None
    receiver_notional_amount: Optional[float] = None
    effective_date: Optional[Union[datetime.date, str]] = None
    principal_exchange: Optional[PrincipalExchange] = None
    payer_currency: Optional[Currency] = None
    payer_rate: Optional[Union[float, str]] = None
    payer_frequency: Optional[str] = None
    payer_day_count_fraction: Optional[DayCountFraction] = None
    payer_business_day_convention: Optional[BusinessDayConvention] = None
    receiver_currency: Optional[Currency] = None
    receiver_rate: Optional[Union[float, str]] = None
    receiver_frequency: Optional[str] = None
    receiver_day_count_fraction: Optional[DayCountFraction] = None
    receiver_business_day_convention: Optional[BusinessDayConvention] = None
    fee: Optional[float] = 0.0
    fee_currency: Optional[Currency] = None
    fee_payment_date: Optional[Union[datetime.date, str]] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Rates)
    type_: Optional[AssetType] = field(init=False, default=AssetType.XccySwapFixFix, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class IRXccySwapFixFlt(Instrument):
    pay_or_receive: Optional[PayReceive] = None
    termination_date: Optional[Union[datetime.date, str]] = None
    notional_amount: Optional[Union[float, str]] = None
    effective_date: Optional[Union[datetime.date, str]] = None
    principal_exchange: Optional[PrincipalExchange] = None
    floating_rate_currency: Optional[Currency] = None
    floating_rate_for_the_initial_calculation_period: Optional[float] = None
    floating_rate_option: Optional[str] = None
    floating_rate_designated_maturity: Optional[str] = None
    floating_rate_spread: Optional[Union[float, str]] = None
    floating_rate_frequency: Optional[str] = None
    floating_rate_day_count_fraction: Optional[DayCountFraction] = None
    floating_rate_business_day_convention: Optional[BusinessDayConvention] = None
    fixed_rate_currency: Optional[Currency] = None
    fixed_rate: Optional[Union[float, str]] = None
    fixed_rate_frequency: Optional[str] = None
    fixed_rate_day_count_fraction: Optional[DayCountFraction] = None
    fixed_rate_business_day_convention: Optional[BusinessDayConvention] = None
    fee: Optional[float] = 0.0
    fee_currency: Optional[Currency] = None
    fee_payment_date: Optional[Union[datetime.date, str]] = None
    fixed_first_stub: Optional[Union[datetime.date, str]] = None
    floating_first_stub: Optional[Union[datetime.date, str]] = None
    fixed_last_stub: Optional[Union[datetime.date, str]] = None
    floating_last_stub: Optional[Union[datetime.date, str]] = None
    fixed_holidays: Optional[str] = None
    floating_holidays: Optional[str] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Rates)
    type_: Optional[AssetType] = field(init=False, default=AssetType.XccySwapFixFlt, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class IRXccySwapFltFlt(Instrument):
    termination_date: Optional[Union[datetime.date, str]] = None
    notional_amount: Optional[Union[float, str]] = None
    effective_date: Optional[Union[datetime.date, str]] = None
    principal_exchange: Optional[PrincipalExchange] = None
    payer_currency: Optional[Currency] = None
    payer_spread: Optional[Union[float, str]] = None
    payer_rate_option: Optional[str] = None
    payer_designated_maturity: Optional[str] = None
    payer_frequency: Optional[str] = None
    payer_day_count_fraction: Optional[DayCountFraction] = None
    payer_business_day_convention: Optional[BusinessDayConvention] = None
    receiver_currency: Optional[Currency] = None
    receiver_spread: Optional[Union[float, str]] = None
    receiver_rate_option: Optional[str] = None
    receiver_designated_maturity: Optional[str] = None
    receiver_frequency: Optional[str] = None
    receiver_day_count_fraction: Optional[DayCountFraction] = None
    receiver_business_day_convention: Optional[BusinessDayConvention] = None
    fee: Optional[float] = 0.0
    fee_currency: Optional[Currency] = None
    fee_payment_date: Optional[Union[datetime.date, str]] = None
    payer_first_stub: Optional[Union[datetime.date, str]] = None
    receiver_first_stub: Optional[Union[datetime.date, str]] = None
    payer_last_stub: Optional[Union[datetime.date, str]] = None
    receiver_last_stub: Optional[Union[datetime.date, str]] = None
    payer_holidays: Optional[str] = None
    receiver_holidays: Optional[str] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Rates)
    type_: Optional[AssetType] = field(init=False, default=AssetType.XccySwap, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CommodOTCOption(Instrument):
    buy_sell: Optional[BuySell] = None
    quantity: Optional[Union[float, str]] = None
    start: Optional[Union[datetime.date, str]] = None
    number_of_periods: Optional[int] = None
    quantity_unit: Optional[str] = None
    settlement: Optional[str] = None
    premium_summary: Optional[Union[float, str]] = None
    legs: Optional[Tuple[CommodOTCOptionLeg, ...]] = None
    end: Optional[Union[datetime.date, str]] = None
    quantity_period: Optional[Period] = None
    strategy: Optional[str] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Commod)
    type_: Optional[AssetType] = field(init=False, default=AssetType.OptionStrategy, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class InvoiceSpread(Instrument):
    buy_sell: Optional[BuySell] = None
    notional_amount: Optional[Union[float, str]] = None
    underlier: Optional[Union[float, str]] = None
    swap: Optional[IRSwap] = None
    future: Optional[IRBondFuture] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Rates)
    type_: Optional[AssetType] = field(init=False, default=AssetType.InvoiceSpread, metadata=config(field_name='type'))


@resolution_safe
@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class CSLPython(Instrument):
    class_name: Optional[str] = None
    denominated: Optional[Currency] = None
    double_params: Optional[Tuple[CSLDouble, ...]] = None
    date_params: Optional[Tuple[CSLDate, ...]] = None
    string_params: Optional[Tuple[CSLString, ...]] = None
    simple_schedule_params: Optional[Tuple[CSLSimpleSchedule, ...]] = None
    schedule_params: Optional[Tuple[CSLSchedule, ...]] = None
    currency_params: Optional[Tuple[CSLCurrency, ...]] = None
    stock_params: Optional[Tuple[CSLStock, ...]] = None
    index_params: Optional[Tuple[CSLIndex, ...]] = None
    fx_cross_params: Optional[Tuple[CSLFXCross, ...]] = None
    double_array_params: Optional[Tuple[CSLDoubleArray, ...]] = None
    date_array_params: Optional[Tuple[CSLDateArray, ...]] = None
    string_array_params: Optional[Tuple[CSLStringArray, ...]] = None
    simple_schedule_array_params: Optional[Tuple[CSLSimpleScheduleArray, ...]] = None
    schedule_array_params: Optional[Tuple[CSLScheduleArray, ...]] = None
    currency_array_params: Optional[Tuple[CSLCurrencyArray, ...]] = None
    stock_array_params: Optional[Tuple[CSLStockArray, ...]] = None
    index_array_params: Optional[Tuple[CSLIndexArray, ...]] = None
    fx_cross_array_params: Optional[Tuple[CSLFXCrossArray, ...]] = None
    asset_class: Optional[AssetClass] = field(init=False, default=AssetClass.Cross_Asset)
    type_: Optional[AssetType] = field(init=False, default=AssetType.CSL, metadata=config(field_name='type'))
