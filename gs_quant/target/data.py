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

from gs_quant.target.common import *
import datetime
from typing import Tuple, Union
from enum import Enum
from gs_quant.base import Base, EnumBase, InstrumentBase, camel_case_translate, get_enum_value


class DelayExclusionType(EnumBase, Enum):    
    
    """Type of the delay exclusion"""

    LAST_DAY_OF_THE_MONTH = 'LAST_DAY_OF_THE_MONTH'
    
    def __repr__(self):
        return self.value


class MarketDataMeasure(EnumBase, Enum):    
    
    Last = 'Last'
    Curve = 'Curve'
    Close_Change = 'Close Change'
    Previous_Close = 'Previous Close'
    
    def __repr__(self):
        return self.value


class MeasureEntityType(EnumBase, Enum):    
    
    """Entity type associated with a measure."""

    ASSET = 'ASSET'
    BACKTEST = 'BACKTEST'
    KPI = 'KPI'
    COUNTRY = 'COUNTRY'
    SUBDIVISION = 'SUBDIVISION'
    REPORT = 'REPORT'
    HEDGE = 'HEDGE'
    
    def __repr__(self):
        return self.value


class AdvancedFilter(Base):
        
    """Advanced filters for the Dataset."""

    @camel_case_translate
    def __init__(
        self,
        column: str,
        operator: str,
        value: float = None,
        values: Tuple[str, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.column = column
        self.value = value
        self.values = values
        self.operator = operator
        self.name = name

    @property
    def column(self) -> str:
        """Database column to match against."""
        return self.__column

    @column.setter
    def column(self, value: str):
        self._property_changed('column')
        self.__column = value        

    @property
    def value(self) -> float:
        """Numeric value to compare against. Cannot be used with 'in' and 'notIn'
           operators."""
        return self.__value

    @value.setter
    def value(self, value: float):
        self._property_changed('value')
        self.__value = value        

    @property
    def values(self) -> Tuple[str, ...]:
        """Values to compare against. Can only be used with 'in' and 'notIn' operators."""
        return self.__values

    @values.setter
    def values(self, value: Tuple[str, ...]):
        self._property_changed('values')
        self.__values = value        

    @property
    def operator(self) -> str:
        """Comparison operator."""
        return self.__operator

    @operator.setter
    def operator(self, value: str):
        self._property_changed('operator')
        self.__operator = value        


class DataGroup(Base):
        
    """Dataset grouped by context (key dimensions)"""

    @camel_case_translate
    def __init__(
        self,
        context: FieldValueMap = None,
        data: Tuple[FieldValueMap, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.context = context
        self.data = data
        self.name = name

    @property
    def context(self) -> FieldValueMap:
        """Context map for the grouped data (key dimensions)"""
        return self.__context

    @context.setter
    def context(self, value: FieldValueMap):
        self._property_changed('context')
        self.__context = value        

    @property
    def data(self) -> Tuple[FieldValueMap, ...]:
        """Array of grouped data objects"""
        return self.__data

    @data.setter
    def data(self, value: Tuple[FieldValueMap, ...]):
        self._property_changed('data')
        self.__data = value        


class DataSetCondition(Base):
        
    """Condition for Dataset Transformations and Filters."""

    @camel_case_translate
    def __init__(
        self,
        column: str,
        operator: str,
        value: float = None,
        values: Tuple[str, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.column = column
        self.value = value
        self.values = values
        self.operator = operator
        self.name = name

    @property
    def column(self) -> str:
        """Database column to match against."""
        return self.__column

    @column.setter
    def column(self, value: str):
        self._property_changed('column')
        self.__column = value        

    @property
    def value(self) -> float:
        """Numeric value to compare against. Cannot be used with 'in' and 'notIn'
           operators."""
        return self.__value

    @value.setter
    def value(self, value: float):
        self._property_changed('value')
        self.__value = value        

    @property
    def values(self) -> Tuple[str, ...]:
        """Values to compare against. Can only be used with 'in' and 'notIn' operators."""
        return self.__values

    @values.setter
    def values(self, value: Tuple[str, ...]):
        self._property_changed('values')
        self.__values = value        

    @property
    def operator(self) -> str:
        """Comparison operator."""
        return self.__operator

    @operator.setter
    def operator(self, value: str):
        self._property_changed('operator')
        self.__operator = value        


class DataSetDefaults(Base):
        
    """Default settings."""

    @camel_case_translate
    def __init__(
        self,
        start_seconds: float = None,
        end_seconds: float = None,
        delay_seconds: float = None,
        name: str = None
    ):        
        super().__init__()
        self.start_seconds = start_seconds
        self.end_seconds = end_seconds
        self.delay_seconds = delay_seconds
        self.name = name

    @property
    def start_seconds(self) -> float:
        """Default start date/time, in seconds before current time."""
        return self.__start_seconds

    @start_seconds.setter
    def start_seconds(self, value: float):
        self._property_changed('start_seconds')
        self.__start_seconds = value        

    @property
    def end_seconds(self) -> float:
        """Default end date/time, in seconds before current time."""
        return self.__end_seconds

    @end_seconds.setter
    def end_seconds(self, value: float):
        self._property_changed('end_seconds')
        self.__end_seconds = value        

    @property
    def delay_seconds(self) -> float:
        """Default market delay to apply, in seconds."""
        return self.__delay_seconds

    @delay_seconds.setter
    def delay_seconds(self, value: float):
        self._property_changed('delay_seconds')
        self.__delay_seconds = value        


class DataSetParameters(Base):
        
    """Dataset parameters."""

    @camel_case_translate
    def __init__(
        self,
        frequency: str,
        category: str = None,
        sub_category: str = None,
        methodology: str = None,
        coverage: str = None,
        coverages: Tuple[Union[AssetType, str], ...] = None,
        notes: str = None,
        history: str = None,
        sample_start: datetime.datetime = None,
        sample_end: datetime.datetime = None,
        published_date: datetime.datetime = None,
        history_date: datetime.datetime = None,
        asset_class: Union[AssetClass, str] = None,
        owner_ids: Tuple[str, ...] = None,
        approver_ids: Tuple[str, ...] = None,
        support_ids: Tuple[str, ...] = None,
        support_distribution_list: Tuple[str, ...] = None,
        plot: bool = None,
        coverage_enabled: bool = True,
        use_created_time_for_upload: bool = None,
        apply_entity_entitlements: bool = None,
        development_status: str = None,
        name: str = None
    ):        
        super().__init__()
        self.category = category
        self.sub_category = sub_category
        self.methodology = methodology
        self.coverage = coverage
        self.coverages = coverages
        self.notes = notes
        self.history = history
        self.sample_start = sample_start
        self.sample_end = sample_end
        self.published_date = published_date
        self.history_date = history_date
        self.frequency = frequency
        self.asset_class = asset_class
        self.owner_ids = owner_ids
        self.approver_ids = approver_ids
        self.support_ids = support_ids
        self.support_distribution_list = support_distribution_list
        self.plot = plot
        self.coverage_enabled = coverage_enabled
        self.use_created_time_for_upload = use_created_time_for_upload
        self.apply_entity_entitlements = apply_entity_entitlements
        self.development_status = development_status
        self.name = name

    @property
    def category(self) -> str:
        """Top level grouping."""
        return self.__category

    @category.setter
    def category(self, value: str):
        self._property_changed('category')
        self.__category = value        

    @property
    def sub_category(self) -> str:
        """Second level grouping."""
        return self.__sub_category

    @sub_category.setter
    def sub_category(self, value: str):
        self._property_changed('sub_category')
        self.__sub_category = value        

    @property
    def methodology(self) -> str:
        """Methodology of dataset."""
        return self.__methodology

    @methodology.setter
    def methodology(self, value: str):
        self._property_changed('methodology')
        self.__methodology = value        

    @property
    def coverage(self) -> str:
        """Coverage of dataset."""
        return self.__coverage

    @coverage.setter
    def coverage(self, value: str):
        self._property_changed('coverage')
        self.__coverage = value        

    @property
    def coverages(self) -> Tuple[Union[AssetType, str], ...]:
        """asset types coverage of dataset."""
        return self.__coverages

    @coverages.setter
    def coverages(self, value: Tuple[Union[AssetType, str], ...]):
        self._property_changed('coverages')
        self.__coverages = value        

    @property
    def notes(self) -> str:
        """Notes of dataset."""
        return self.__notes

    @notes.setter
    def notes(self, value: str):
        self._property_changed('notes')
        self.__notes = value        

    @property
    def history(self) -> str:
        """Period of time covered by dataset."""
        return self.__history

    @history.setter
    def history(self, value: str):
        self._property_changed('history')
        self.__history = value        

    @property
    def sample_start(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__sample_start

    @sample_start.setter
    def sample_start(self, value: datetime.datetime):
        self._property_changed('sample_start')
        self.__sample_start = value        

    @property
    def sample_end(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__sample_end

    @sample_end.setter
    def sample_end(self, value: datetime.datetime):
        self._property_changed('sample_end')
        self.__sample_end = value        

    @property
    def published_date(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__published_date

    @published_date.setter
    def published_date(self, value: datetime.datetime):
        self._property_changed('published_date')
        self.__published_date = value        

    @property
    def history_date(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__history_date

    @history_date.setter
    def history_date(self, value: datetime.datetime):
        self._property_changed('history_date')
        self.__history_date = value        

    @property
    def frequency(self) -> str:
        """Frequency of updates to dataset."""
        return self.__frequency

    @frequency.setter
    def frequency(self, value: str):
        self._property_changed('frequency')
        self.__frequency = value        

    @property
    def asset_class(self) -> Union[AssetClass, str]:
        """Asset classification of security. Assets are classified into broad groups which
           exhibit similar characteristics and behave in a consistent way under
           different market conditions"""
        return self.__asset_class

    @asset_class.setter
    def asset_class(self, value: Union[AssetClass, str]):
        self._property_changed('asset_class')
        self.__asset_class = get_enum_value(AssetClass, value)        

    @property
    def owner_ids(self) -> Tuple[str, ...]:
        """Users who own dataset."""
        return self.__owner_ids

    @owner_ids.setter
    def owner_ids(self, value: Tuple[str, ...]):
        self._property_changed('owner_ids')
        self.__owner_ids = value        

    @property
    def approver_ids(self) -> Tuple[str, ...]:
        """Users who can grant access to dataset."""
        return self.__approver_ids

    @approver_ids.setter
    def approver_ids(self, value: Tuple[str, ...]):
        self._property_changed('approver_ids')
        self.__approver_ids = value        

    @property
    def support_ids(self) -> Tuple[str, ...]:
        """Users who support dataset."""
        return self.__support_ids

    @support_ids.setter
    def support_ids(self, value: Tuple[str, ...]):
        self._property_changed('support_ids')
        self.__support_ids = value        

    @property
    def support_distribution_list(self) -> Tuple[str, ...]:
        """Distribution list who support dataset."""
        return self.__support_distribution_list

    @support_distribution_list.setter
    def support_distribution_list(self, value: Tuple[str, ...]):
        self._property_changed('support_distribution_list')
        self.__support_distribution_list = value        

    @property
    def plot(self) -> bool:
        """Whether dataset is intended for use in Plottool."""
        return self.__plot

    @plot.setter
    def plot(self, value: bool):
        self._property_changed('plot')
        self.__plot = value        

    @property
    def coverage_enabled(self) -> bool:
        """Whether coverage requests are available for the DataSet"""
        return self.__coverage_enabled

    @coverage_enabled.setter
    def coverage_enabled(self, value: bool):
        self._property_changed('coverage_enabled')
        self.__coverage_enabled = value        

    @property
    def use_created_time_for_upload(self) -> bool:
        """Whether the dataset uses createdTime to record the time at which the data got
           uploaded."""
        return self.__use_created_time_for_upload

    @use_created_time_for_upload.setter
    def use_created_time_for_upload(self, value: bool):
        self._property_changed('use_created_time_for_upload')
        self.__use_created_time_for_upload = value        

    @property
    def apply_entity_entitlements(self) -> bool:
        """Whether entity level entitlements are applied while querying the dataset and its
           coverage."""
        return self.__apply_entity_entitlements

    @apply_entity_entitlements.setter
    def apply_entity_entitlements(self, value: bool):
        self._property_changed('apply_entity_entitlements')
        self.__apply_entity_entitlements = value        

    @property
    def development_status(self) -> str:
        """The status of development of this dataset. Controls rate limit on query/upload."""
        return self.__development_status

    @development_status.setter
    def development_status(self, value: str):
        self._property_changed('development_status')
        self.__development_status = value        


class FieldFilterMapDataQuery(Base):
        
    @camel_case_translate
    def __init__(
        self,
        **kwargs
    ):        
        super().__init__()
        self.investment_rate = kwargs.get('investment_rate')
        self.starting_emma_legal_entity_id = kwargs.get('starting_emma_legal_entity_id')
        self.mdapi_class = kwargs.get('mdapi_class')
        self.total_notional_usd = kwargs.get('total_notional_usd')
        self.bid_unadjusted = kwargs.get('bid_unadjusted')
        self.aggressive_fills_percentage = kwargs.get('aggressive_fills_percentage')
        self.vehicle_type = kwargs.get('vehicle_type')
        self.total_fatalities_by_state = kwargs.get('total_fatalities_by_state')
        self.new_active = kwargs.get('new_active')
        self.daily_risk = kwargs.get('daily_risk')
        self.energy = kwargs.get('energy')
        self.sunshine_daily_forecast = kwargs.get('sunshine_daily_forecast')
        self.sentiment_score = kwargs.get('sentiment_score')
        self.correlation = kwargs.get('correlation')
        self.exposure = kwargs.get('exposure')
        self.size = kwargs.get('size')
        self.market_data_asset = kwargs.get('market_data_asset')
        self.buy75cents = kwargs.get('buy75cents')
        self.unadjusted_high = kwargs.get('unadjusted_high')
        self.source_importance = kwargs.get('source_importance')
        self.closing_yield = kwargs.get('closing_yield')
        self.wind = kwargs.get('wind')
        self.sc16 = kwargs.get('sc16')
        self.sc15 = kwargs.get('sc15')
        self.sc12 = kwargs.get('sc12')
        self.sc11 = kwargs.get('sc11')
        self.primary_vwap_in_limit_unrealized_bps = kwargs.get('primary_vwap_in_limit_unrealized_bps')
        self.display_name = kwargs.get('display_name')
        self.minutes_to_trade100_pct = kwargs.get('minutes_to_trade100_pct')
        self.sc14 = kwargs.get('sc14')
        self.cumulative_volume_in_shares = kwargs.get('cumulative_volume_in_shares')
        self.sc13 = kwargs.get('sc13')
        self.new_fatalities = kwargs.get('new_fatalities')
        self.buy50bps = kwargs.get('buy50bps')
        self.num_staffed_beds = kwargs.get('num_staffed_beds')
        self.upfront_payment = kwargs.get('upfront_payment')
        self.arrival_mid_realized_cash = kwargs.get('arrival_mid_realized_cash')
        self.sc10 = kwargs.get('sc10')
        self.sc05 = kwargs.get('sc05')
        self.a = kwargs.get('a')
        self.sc04 = kwargs.get('sc04')
        self.b = kwargs.get('b')
        self.sc07 = kwargs.get('sc07')
        self.c = kwargs.get('c')
        self.yield_to_maturity = kwargs.get('yield_to_maturity')
        self.sc06 = kwargs.get('sc06')
        self.address = kwargs.get('address')
        self.sc01 = kwargs.get('sc01')
        self.leg2_payment_frequency = kwargs.get('leg2_payment_frequency')
        self.sc03 = kwargs.get('sc03')
        self.sc02 = kwargs.get('sc02')
        self.geography_name = kwargs.get('geography_name')
        self.borrower = kwargs.get('borrower')
        self.settle_price = kwargs.get('settle_price')
        self.performance_contribution = kwargs.get('performance_contribution')
        self.sc09 = kwargs.get('sc09')
        self.mkt_class = kwargs.get('mkt_class')
        self.sc08 = kwargs.get('sc08')
        self.collateralization = kwargs.get('collateralization')
        self.future_month_u26 = kwargs.get('future_month_u26')
        self.future_month_u25 = kwargs.get('future_month_u25')
        self.future_month_u24 = kwargs.get('future_month_u24')
        self.future_month_u23 = kwargs.get('future_month_u23')
        self.future_month_u22 = kwargs.get('future_month_u22')
        self.statement_id = kwargs.get('statement_id')
        self.future_month_u21 = kwargs.get('future_month_u21')
        self.modified_duration = kwargs.get('modified_duration')
        self.short_rates_contribution = kwargs.get('short_rates_contribution')
        self.implied_normal_volatility = kwargs.get('implied_normal_volatility')
        self.solar_generation = kwargs.get('solar_generation')
        self.mtm_price = kwargs.get('mtm_price')
        self.swap_spread_change = kwargs.get('swap_spread_change')
        self.realized_arrival_performance_usd = kwargs.get('realized_arrival_performance_usd')
        self.portfolio_assets = kwargs.get('portfolio_assets')
        self.pricingdate = kwargs.get('pricingdate')
        self.tcm_cost_horizon3_hour = kwargs.get('tcm_cost_horizon3_hour')
        self.exchange_rate = kwargs.get('exchange_rate')
        self.potential_bed_cap_inc = kwargs.get('potential_bed_cap_inc')
        self.number_covered = kwargs.get('number_covered')
        self.number_of_positions = kwargs.get('number_of_positions')
        self.open_unadjusted = kwargs.get('open_unadjusted')
        self.strike_time = kwargs.get('strike_time')
        self.ask_price = kwargs.get('ask_price')
        self.event_id = kwargs.get('event_id')
        self.sectors = kwargs.get('sectors')
        self.additional_price_notation_type = kwargs.get('additional_price_notation_type')
        self.gross_investment_qtd = kwargs.get('gross_investment_qtd')
        self.annualized_risk = kwargs.get('annualized_risk')
        self.estimated_holding_time_short = kwargs.get('estimated_holding_time_short')
        self.midcurve_premium = kwargs.get('midcurve_premium')
        self.volume_composite = kwargs.get('volume_composite')
        self.sharpe_qtd = kwargs.get('sharpe_qtd')
        self.estimated_holding_time_long = kwargs.get('estimated_holding_time_long')
        self.external = kwargs.get('external')
        self.tracker_name = kwargs.get('tracker_name')
        self.sell50cents = kwargs.get('sell50cents')
        self.trade_price = kwargs.get('trade_price')
        self.cleared = kwargs.get('cleared')
        self.prime_id_numeric = kwargs.get('prime_id_numeric')
        self.buy8bps = kwargs.get('buy8bps')
        self.total_notional_local = kwargs.get('total_notional_local')
        self.cid = kwargs.get('cid')
        self.total_confirmed_senior_home = kwargs.get('total_confirmed_senior_home')
        self.ctd_fwd_price = kwargs.get('ctd_fwd_price')
        self.sink_factor = kwargs.get('sink_factor')
        self.temperature_forecast = kwargs.get('temperature_forecast')
        self.bid_high = kwargs.get('bid_high')
        self.pnl_qtd = kwargs.get('pnl_qtd')
        self.buy50cents = kwargs.get('buy50cents')
        self.sell4bps = kwargs.get('sell4bps')
        self.receiver_day_count_fraction = kwargs.get('receiver_day_count_fraction')
        self.auction_close_percentage = kwargs.get('auction_close_percentage')
        self.target_price = kwargs.get('target_price')
        self.bos_in_bps_description = kwargs.get('bos_in_bps_description')
        self.low_price = kwargs.get('low_price')
        self.adv22_day_pct = kwargs.get('adv22_day_pct')
        self.matched_maturity_swap_spread12m = kwargs.get('matched_maturity_swap_spread12m')
        self.price_range_in_ticks_label = kwargs.get('price_range_in_ticks_label')
        self.ticker = kwargs.get('ticker')
        self.notional_unit = kwargs.get('notional_unit')
        self.tcm_cost_horizon1_day = kwargs.get('tcm_cost_horizon1_day')
        self.approval = kwargs.get('approval')
        self.test_measure = kwargs.get('test_measure')
        self.option_lock_out_period = kwargs.get('option_lock_out_period')
        self.source_value_forecast = kwargs.get('source_value_forecast')
        self.leg2_spread = kwargs.get('leg2_spread')
        self.short_conviction_large = kwargs.get('short_conviction_large')
        self.ccg_name = kwargs.get('ccg_name')
        self.dollar_excess_return = kwargs.get('dollar_excess_return')
        self.gsn = kwargs.get('gsn')
        self.trade_end_date = kwargs.get('trade_end_date')
        self.receiver_rate_option = kwargs.get('receiver_rate_option')
        self.gss = kwargs.get('gss')
        self.percent_of_mediandv1m = kwargs.get('percent_of_mediandv1m')
        self.lendables = kwargs.get('lendables')
        self.sell75cents = kwargs.get('sell75cents')
        self.option_adjusted_spread = kwargs.get('option_adjusted_spread')
        self.option_adjusted_swap_spread = kwargs.get('option_adjusted_swap_spread')
        self.bos_in_ticks_label = kwargs.get('bos_in_ticks_label')
        self.position_source_id = kwargs.get('position_source_id')
        self.buy1bps = kwargs.get('buy1bps')
        self.buy3point5bps = kwargs.get('buy3point5bps')
        self.gs_sustain_region = kwargs.get('gs_sustain_region')
        self.absolute_return_wtd = kwargs.get('absolute_return_wtd')
        self.deployment_id = kwargs.get('deployment_id')
        self.asset_parameters_seniority = kwargs.get('asset_parameters_seniority')
        self.ask_spread = kwargs.get('ask_spread')
        self.flow = kwargs.get('flow')
        self.future_month_h26 = kwargs.get('future_month_h26')
        self.loan_rebate = kwargs.get('loan_rebate')
        self.future_month_h25 = kwargs.get('future_month_h25')
        self.period = kwargs.get('period')
        self.index_create_source = kwargs.get('index_create_source')
        self.future_month_h24 = kwargs.get('future_month_h24')
        self.future_month_h23 = kwargs.get('future_month_h23')
        self.future_month_h22 = kwargs.get('future_month_h22')
        self.future_month_h21 = kwargs.get('future_month_h21')
        self.non_usd_ois = kwargs.get('non_usd_ois')
        self.real_twi_contribution = kwargs.get('real_twi_contribution')
        self.mkt_asset = kwargs.get('mkt_asset')
        self.leg2_index_location = kwargs.get('leg2_index_location')
        self.twap_unrealized_bps = kwargs.get('twap_unrealized_bps')
        self.last_updated_message = kwargs.get('last_updated_message')
        self.loan_value = kwargs.get('loan_value')
        self.option_adjusted_ois_spread = kwargs.get('option_adjusted_ois_spread')
        self.total_return_price = kwargs.get('total_return_price')
        self.weighted_percent_in_model = kwargs.get('weighted_percent_in_model')
        self.init_loan_spread_required = kwargs.get('init_loan_spread_required')
        self.election_period = kwargs.get('election_period')
        self.funding_ask_price = kwargs.get('funding_ask_price')
        self.historical_beta = kwargs.get('historical_beta')
        self.bond_risk_premium_index = kwargs.get('bond_risk_premium_index')
        self.hit_rate_ytd = kwargs.get('hit_rate_ytd')
        self.gir_gsdeer_gsfeer = kwargs.get('gir_gsdeer_gsfeer')
        self.num_units = kwargs.get('num_units')
        self.asset_parameters_receiver_frequency = kwargs.get('asset_parameters_receiver_frequency')
        self.expense_ratio_gross_bps = kwargs.get('expense_ratio_gross_bps')
        self.relative_payoff_wtd = kwargs.get('relative_payoff_wtd')
        self.ctd_price = kwargs.get('ctd_price')
        self.pace_of_roll_now = kwargs.get('pace_of_roll_now')
        self.product = kwargs.get('product')
        self.leg2_return_type = kwargs.get('leg2_return_type')
        self.agent_lender_fee = kwargs.get('agent_lender_fee')
        self.dissemination_id = kwargs.get('dissemination_id')
        self.option_strike_price = kwargs.get('option_strike_price')
        self.precipitation_type = kwargs.get('precipitation_type')
        self.lower_bound = kwargs.get('lower_bound')
        self.arrival_mid_normalized = kwargs.get('arrival_mid_normalized')
        self.underlying_asset2 = kwargs.get('underlying_asset2')
        self.underlying_asset1 = kwargs.get('underlying_asset1')
        self.legal_entity = kwargs.get('legal_entity')
        self.performance_fee = kwargs.get('performance_fee')
        self.order_state = kwargs.get('order_state')
        self.actual_data_quality = kwargs.get('actual_data_quality')
        self.index_ratio = kwargs.get('index_ratio')
        self.queue_in_lots_label = kwargs.get('queue_in_lots_label')
        self.adv10_day_pct = kwargs.get('adv10_day_pct')
        self.long_conviction_medium = kwargs.get('long_conviction_medium')
        self.relative_hit_rate_wtd = kwargs.get('relative_hit_rate_wtd')
        self.daily_tracking_error = kwargs.get('daily_tracking_error')
        self.sell140cents = kwargs.get('sell140cents')
        self.sell10bps = kwargs.get('sell10bps')
        self.aggressive_offset_from_last = kwargs.get('aggressive_offset_from_last')
        self.longitude = kwargs.get('longitude')
        self.new_icu = kwargs.get('new_icu')
        self.market_cap = kwargs.get('market_cap')
        self.weighted_average_mid = kwargs.get('weighted_average_mid')
        self.cluster_region = kwargs.get('cluster_region')
        self.valoren = kwargs.get('valoren')
        self.average_execution_price = kwargs.get('average_execution_price')
        self.proceeds_asset_ois_swap_spread1m = kwargs.get('proceeds_asset_ois_swap_spread1m')
        self.payoff_wtd = kwargs.get('payoff_wtd')
        self.basis = kwargs.get('basis')
        self.investment_rate_trend = kwargs.get('investment_rate_trend')
        self.gross_investment_mtd = kwargs.get('gross_investment_mtd')
        self.hedge_id = kwargs.get('hedge_id')
        self.sharpe_mtd = kwargs.get('sharpe_mtd')
        self.tcm_cost_horizon8_day = kwargs.get('tcm_cost_horizon8_day')
        self.residual_variance = kwargs.get('residual_variance')
        self.restrict_internal_derived_data = kwargs.get('restrict_internal_derived_data')
        self.adv5_day_pct = kwargs.get('adv5_day_pct')
        self.midpoint_fills_percentage = kwargs.get('midpoint_fills_percentage')
        self.open_interest = kwargs.get('open_interest')
        self.turnover_composite_unadjusted = kwargs.get('turnover_composite_unadjusted')
        self.fwd_points = kwargs.get('fwd_points')
        self.relative_return_wtd = kwargs.get('relative_return_wtd')
        self.units = kwargs.get('units')
        self.payer_rate_option = kwargs.get('payer_rate_option')
        self.asset_classifications_risk_country_name = kwargs.get('asset_classifications_risk_country_name')
        self.ext_mkt_point3 = kwargs.get('ext_mkt_point3')
        self.matched_maturity_swap_spread = kwargs.get('matched_maturity_swap_spread')
        self.city_name = kwargs.get('city_name')
        self.hourly_bucket = kwargs.get('hourly_bucket')
        self.average_implied_volatility = kwargs.get('average_implied_volatility')
        self.total_hospitalized_with_symptoms = kwargs.get('total_hospitalized_with_symptoms')
        self.days_open_realized_cash = kwargs.get('days_open_realized_cash')
        self.adjusted_high_price = kwargs.get('adjusted_high_price')
        self.proceeds_asset_ois_swap_spread = kwargs.get('proceeds_asset_ois_swap_spread')
        self.ext_mkt_point1 = kwargs.get('ext_mkt_point1')
        self.direction = kwargs.get('direction')
        self.ext_mkt_point2 = kwargs.get('ext_mkt_point2')
        self.sub_region_code = kwargs.get('sub_region_code')
        self.asset_parameters_fixed_rate = kwargs.get('asset_parameters_fixed_rate')
        self.is_estimated_return = kwargs.get('is_estimated_return')
        self.value_forecast = kwargs.get('value_forecast')
        self.total_icu = kwargs.get('total_icu')
        self.position_source_type = kwargs.get('position_source_type')
        self.previous_close_unrealized_cash = kwargs.get('previous_close_unrealized_cash')
        self.minimum_denomination = kwargs.get('minimum_denomination')
        self.future_value_notional = kwargs.get('future_value_notional')
        self.participation_rate = kwargs.get('participation_rate')
        self.obfr = kwargs.get('obfr')
        self.buy9point5bps = kwargs.get('buy9point5bps')
        self.option_lock_period = kwargs.get('option_lock_period')
        self.es_momentum_percentile = kwargs.get('es_momentum_percentile')
        self.adv_percentage = kwargs.get('adv_percentage')
        self.leg1_averaging_method = kwargs.get('leg1_averaging_method')
        self.turnover_composite = kwargs.get('turnover_composite')
        self.forecast_date = kwargs.get('forecast_date')
        self.internal_index_calc_region = kwargs.get('internal_index_calc_region')
        self.position_type = kwargs.get('position_type')
        self.sub_asset_class = kwargs.get('sub_asset_class')
        self.short_interest = kwargs.get('short_interest')
        self.reference_period = kwargs.get('reference_period')
        self.adjusted_volume = kwargs.get('adjusted_volume')
        self.ctd_fwd_yield = kwargs.get('ctd_fwd_yield')
        self.sec_db = kwargs.get('sec_db')
        self.memory_used = kwargs.get('memory_used')
        self.bpe_quality_stars = kwargs.get('bpe_quality_stars')
        self.ctd = kwargs.get('ctd')
        self.intended_participation_rate = kwargs.get('intended_participation_rate')
        self.leg1_payment_type = kwargs.get('leg1_payment_type')
        self.trading_pnl = kwargs.get('trading_pnl')
        self.collateral_value_required = kwargs.get('collateral_value_required')
        self.buy45bps = kwargs.get('buy45bps')
        self.price_to_earnings_positive = kwargs.get('price_to_earnings_positive')
        self.forecast = kwargs.get('forecast')
        self.forecast_value = kwargs.get('forecast_value')
        self.pnl = kwargs.get('pnl')
        self.volume_in_limit = kwargs.get('volume_in_limit')
        self.is_territory = kwargs.get('is_territory')
        self.leg2_delivery_point = kwargs.get('leg2_delivery_point')
        self.tcm_cost_horizon4_day = kwargs.get('tcm_cost_horizon4_day')
        self.styles = kwargs.get('styles')
        self.short_name = kwargs.get('short_name')
        self.reset_frequency1 = kwargs.get('reset_frequency1')
        self.buy4bps = kwargs.get('buy4bps')
        self.reset_frequency2 = kwargs.get('reset_frequency2')
        self.other_price_term = kwargs.get('other_price_term')
        self.bid_gspread = kwargs.get('bid_gspread')
        self.open_price = kwargs.get('open_price')
        self.ps_id = kwargs.get('ps_id')
        self.hit_rate_mtd = kwargs.get('hit_rate_mtd')
        self.fair_volatility = kwargs.get('fair_volatility')
        self.dollar_cross = kwargs.get('dollar_cross')
        self.portfolio_type = kwargs.get('portfolio_type')
        self.currency = kwargs.get('currency')
        self.cluster_class = kwargs.get('cluster_class')
        self.sell50bps = kwargs.get('sell50bps')
        self.future_month_m21 = kwargs.get('future_month_m21')
        self.bid_size = kwargs.get('bid_size')
        self.arrival_mid = kwargs.get('arrival_mid')
        self.asset_parameters_exchange_currency = kwargs.get('asset_parameters_exchange_currency')
        self.candidate_name = kwargs.get('candidate_name')
        self.implied_lognormal_volatility = kwargs.get('implied_lognormal_volatility')
        self.vwap_in_limit_unrealized_cash = kwargs.get('vwap_in_limit_unrealized_cash')
        self.rating_moodys = kwargs.get('rating_moodys')
        self.future_month_m26 = kwargs.get('future_month_m26')
        self.future_month_m25 = kwargs.get('future_month_m25')
        self.future_month_m24 = kwargs.get('future_month_m24')
        self.future_month_m23 = kwargs.get('future_month_m23')
        self.future_month_m22 = kwargs.get('future_month_m22')
        self.flow_pct = kwargs.get('flow_pct')
        self.source = kwargs.get('source')
        self.asset_classifications_country_code = kwargs.get('asset_classifications_country_code')
        self.settle_drop = kwargs.get('settle_drop')
        self.data_set_sub_category = kwargs.get('data_set_sub_category')
        self.sell9point5bps = kwargs.get('sell9point5bps')
        self.quantity_bucket = kwargs.get('quantity_bucket')
        self.option_style_sdr = kwargs.get('option_style_sdr')
        self.oe_name = kwargs.get('oe_name')
        self.given = kwargs.get('given')
        self.leg2_day_count_convention = kwargs.get('leg2_day_count_convention')
        self.liquidity_score_sell = kwargs.get('liquidity_score_sell')
        self.delisting_date = kwargs.get('delisting_date')
        self.weight = kwargs.get('weight')
        self.accrued_interest = kwargs.get('accrued_interest')
        self.business_scope = kwargs.get('business_scope')
        self.wtd_degree_days = kwargs.get('wtd_degree_days')
        self.absolute_weight = kwargs.get('absolute_weight')
        self.measure = kwargs.get('measure')
        self.temperature_hourly_forecast = kwargs.get('temperature_hourly_forecast')
        self.iceberg_tip_rate_type = kwargs.get('iceberg_tip_rate_type')
        self.sharpe_ytd = kwargs.get('sharpe_ytd')
        self.wind_speed_forecast = kwargs.get('wind_speed_forecast')
        self.gross_investment_ytd = kwargs.get('gross_investment_ytd')
        self.yield_price = kwargs.get('yield_price')
        self.leg1_total_notional_unit = kwargs.get('leg1_total_notional_unit')
        self.issue_price = kwargs.get('issue_price')
        self.ask_high = kwargs.get('ask_high')
        self.expected_data_quality = kwargs.get('expected_data_quality')
        self.region_name = kwargs.get('region_name')
        self.value_revised = kwargs.get('value_revised')
        self.discretion_upper_bound = kwargs.get('discretion_upper_bound')
        self.adjusted_trade_price = kwargs.get('adjusted_trade_price')
        self.iso_subdivision_code_alpha2 = kwargs.get('iso_subdivision_code_alpha2')
        self.ctd_conversion_factor = kwargs.get('ctd_conversion_factor')
        self.proceeds_asset_swap_spread = kwargs.get('proceeds_asset_swap_spread')
        self.is_adr = kwargs.get('is_adr')
        self.issue_date = kwargs.get('issue_date')
        self.service_id = kwargs.get('service_id')
        self.yes = kwargs.get('yes')
        self.g_score = kwargs.get('g_score')
        self.market_value = kwargs.get('market_value')
        self.entity_id = kwargs.get('entity_id')
        self.notional_currency1 = kwargs.get('notional_currency1')
        self.net_debt_to_ebitda = kwargs.get('net_debt_to_ebitda')
        self.num_units_upper = kwargs.get('num_units_upper')
        self.notional_currency2 = kwargs.get('notional_currency2')
        self.in_limit_participation_rate = kwargs.get('in_limit_participation_rate')
        self.pressure_forecast = kwargs.get('pressure_forecast')
        self.paid = kwargs.get('paid')
        self.fixed_rate = kwargs.get('fixed_rate')
        self.short = kwargs.get('short')
        self.buy4point5bps = kwargs.get('buy4point5bps')
        self.sell30cents = kwargs.get('sell30cents')
        self.leg1_payment_frequency = kwargs.get('leg1_payment_frequency')
        self.cm_id = kwargs.get('cm_id')
        self.taxonomy = kwargs.get('taxonomy')
        self.buy45cents = kwargs.get('buy45cents')
        self.measures = kwargs.get('measures')
        self.seasonal_adjustment = kwargs.get('seasonal_adjustment')
        self.rank_wtd = kwargs.get('rank_wtd')
        self.underlyer = kwargs.get('underlyer')
        self.identifier = kwargs.get('identifier')
        self.price_unit = kwargs.get('price_unit')
        self.trade_report_ref_id = kwargs.get('trade_report_ref_id')
        self.subdivision_id = kwargs.get('subdivision_id')
        self.unadjusted_low = kwargs.get('unadjusted_low')
        self.buy160cents = kwargs.get('buy160cents')
        self.portfolio_id = kwargs.get('portfolio_id')
        self.z_spread = kwargs.get('z_spread')
        self.cap_floor_atm_fwd_rate = kwargs.get('cap_floor_atm_fwd_rate')
        self.es_percentile = kwargs.get('es_percentile')
        self.tdapi = kwargs.get('tdapi')
        self.location_code = kwargs.get('location_code')
        self.rcic = kwargs.get('rcic')
        self.name_raw = kwargs.get('name_raw')
        self.simon_asset_tags = kwargs.get('simon_asset_tags')
        self.hit_rate_qtd = kwargs.get('hit_rate_qtd')
        self.primary_volume_in_limit = kwargs.get('primary_volume_in_limit')
        self.precipitation_daily_forecast_percent = kwargs.get('precipitation_daily_forecast_percent')
        self.aum_end = kwargs.get('aum_end')
        self.premium = kwargs.get('premium')
        self.low = kwargs.get('low')
        self.cross_group = kwargs.get('cross_group')
        self.five_day_price_change_bps = kwargs.get('five_day_price_change_bps')
        self.holdings = kwargs.get('holdings')
        self.precipitation_daily_forecast = kwargs.get('precipitation_daily_forecast')
        self.price_method = kwargs.get('price_method')
        self.asset_parameters_fixed_rate_frequency = kwargs.get('asset_parameters_fixed_rate_frequency')
        self.ois_xccy = kwargs.get('ois_xccy')
        self.days_open = kwargs.get('days_open')
        self.buy110cents = kwargs.get('buy110cents')
        self.average_spread_bps = kwargs.get('average_spread_bps')
        self.buy55cents = kwargs.get('buy55cents')
        self.future_month_q26 = kwargs.get('future_month_q26')
        self.issue_size = kwargs.get('issue_size')
        self.future_month_q25 = kwargs.get('future_month_q25')
        self.future_month_q24 = kwargs.get('future_month_q24')
        self.future_month_q23 = kwargs.get('future_month_q23')
        self.future_month_q22 = kwargs.get('future_month_q22')
        self.pending_loan_count = kwargs.get('pending_loan_count')
        self.future_month_q21 = kwargs.get('future_month_q21')
        self.price_spot_stop_loss_unit = kwargs.get('price_spot_stop_loss_unit')
        self.price_range_in_ticks_description = kwargs.get('price_range_in_ticks_description')
        self.trade_volume = kwargs.get('trade_volume')
        self.primary_country_ric = kwargs.get('primary_country_ric')
        self.option_expiration_frequency = kwargs.get('option_expiration_frequency')
        self.is_active = kwargs.get('is_active')
        self.use_machine_learning = kwargs.get('use_machine_learning')
        self.growth_score = kwargs.get('growth_score')
        self.buffer_threshold = kwargs.get('buffer_threshold')
        self.buy120cents = kwargs.get('buy120cents')
        self.matched_maturity_swap_rate = kwargs.get('matched_maturity_swap_rate')
        self.primary_vwap = kwargs.get('primary_vwap')
        self.exchange_type_id = kwargs.get('exchange_type_id')
        self.basis_swap_rate = kwargs.get('basis_swap_rate')
        self.exchange_code = kwargs.get('exchange_code')
        self.group = kwargs.get('group')
        self.asset_parameters_termination_date = kwargs.get('asset_parameters_termination_date')
        self.estimated_spread = kwargs.get('estimated_spread')
        self.yield_change_on_day = kwargs.get('yield_change_on_day')
        self.auto_tags = kwargs.get('auto_tags')
        self.tcm_cost = kwargs.get('tcm_cost')
        self.sustain_japan = kwargs.get('sustain_japan')
        self.history_start_date = kwargs.get('history_start_date')
        self.bid_spread = kwargs.get('bid_spread')
        self.percentage_complete = kwargs.get('percentage_complete')
        self.hedge_tracking_error = kwargs.get('hedge_tracking_error')
        self.wind_speed_type = kwargs.get('wind_speed_type')
        self.strike_price = kwargs.get('strike_price')
        self.par_asset_swap_spread12m = kwargs.get('par_asset_swap_spread12m')
        self.trade_report_id = kwargs.get('trade_report_id')
        self.adjusted_open_price = kwargs.get('adjusted_open_price')
        self.country_id = kwargs.get('country_id')
        self.point = kwargs.get('point')
        self.pnl_mtd = kwargs.get('pnl_mtd')
        self.total_returns = kwargs.get('total_returns')
        self.lender = kwargs.get('lender')
        self.ann_return1_year = kwargs.get('ann_return1_year')
        self.ctd_fwd_dv01 = kwargs.get('ctd_fwd_dv01')
        self.eff_yield7_day = kwargs.get('eff_yield7_day')
        self.meeting_date = kwargs.get('meeting_date')
        self.calendar_spread_mispricing = kwargs.get('calendar_spread_mispricing')
        self.buy140cents = kwargs.get('buy140cents')
        self.price_notation2_type = kwargs.get('price_notation2_type')
        self.fund_focus = kwargs.get('fund_focus')
        self.relative_strike = kwargs.get('relative_strike')
        self.flagship = kwargs.get('flagship')
        self.additional_price_notation = kwargs.get('additional_price_notation')
        self.factor_category = kwargs.get('factor_category')
        self.equity_delta = kwargs.get('equity_delta')
        self.gross_weight = kwargs.get('gross_weight')
        self.listed = kwargs.get('listed')
        self.sell7bps = kwargs.get('sell7bps')
        self.earnings_record_type = kwargs.get('earnings_record_type')
        self.mean = kwargs.get('mean')
        self.ask_yield = kwargs.get('ask_yield')
        self.shock_style = kwargs.get('shock_style')
        self.methodology = kwargs.get('methodology')
        self.buy25cents = kwargs.get('buy25cents')
        self.amount_outstanding = kwargs.get('amount_outstanding')
        self.market_pnl = kwargs.get('market_pnl')
        self.sustain_asia_ex_japan = kwargs.get('sustain_asia_ex_japan')
        self.sell6point5bps = kwargs.get('sell6point5bps')
        self.neighbour_asset_id = kwargs.get('neighbour_asset_id')
        self.count_ideas_ytd = kwargs.get('count_ideas_ytd')
        self.simon_intl_asset_tags = kwargs.get('simon_intl_asset_tags')
        self.path = kwargs.get('path')
        self.vwap_unrealized_cash = kwargs.get('vwap_unrealized_cash')
        self.payoff_mtd = kwargs.get('payoff_mtd')
        self.bos_in_bps_label = kwargs.get('bos_in_bps_label')
        self.bos_in_bps = kwargs.get('bos_in_bps')
        self.point_class = kwargs.get('point_class')
        self.fx_spot = kwargs.get('fx_spot')
        self.restrict_named_individuals = kwargs.get('restrict_named_individuals')
        self.hedge_volatility = kwargs.get('hedge_volatility')
        self.tags = kwargs.get('tags')
        self.population = kwargs.get('population')
        self.underlying_asset_id = kwargs.get('underlying_asset_id')
        self.real_long_rates_contribution = kwargs.get('real_long_rates_contribution')
        self.pctprices_return = kwargs.get('pctprices_return')
        self.domain = kwargs.get('domain')
        self.buy80cents = kwargs.get('buy80cents')
        self.forward_tenor = kwargs.get('forward_tenor')
        self.average_price = kwargs.get('average_price')
        self.target_price_realized_bps = kwargs.get('target_price_realized_bps')
        self.leg2_fixed_rate = kwargs.get('leg2_fixed_rate')
        self.share_class_assets = kwargs.get('share_class_assets')
        self.annuity = kwargs.get('annuity')
        self.total_count = kwargs.get('total_count')
        self.quote_type = kwargs.get('quote_type')
        self.corporate_action_status = kwargs.get('corporate_action_status')
        self.pegged_tip_size = kwargs.get('pegged_tip_size')
        self.uid = kwargs.get('uid')
        self.es_policy_percentile = kwargs.get('es_policy_percentile')
        self.usd_ois = kwargs.get('usd_ois')
        self.term = kwargs.get('term')
        self.restrict_internal_gs_ntk = kwargs.get('restrict_internal_gs_ntk')
        self.tcm_cost_participation_rate100_pct = kwargs.get('tcm_cost_participation_rate100_pct')
        self.relative_universe = kwargs.get('relative_universe')
        self.measure_idx = kwargs.get('measure_idx')
        self.fred_id = kwargs.get('fred_id')
        self.twi_contribution = kwargs.get('twi_contribution')
        self.cloud_cover_type = kwargs.get('cloud_cover_type')
        self.delisted = kwargs.get('delisted')
        self.regional_focus = kwargs.get('regional_focus')
        self.volume_primary = kwargs.get('volume_primary')
        self.asset_parameters_payer_designated_maturity = kwargs.get('asset_parameters_payer_designated_maturity')
        self.buy30cents = kwargs.get('buy30cents')
        self.funding_bid_price = kwargs.get('funding_bid_price')
        self.series = kwargs.get('series')
        self.sell3bps = kwargs.get('sell3bps')
        self.settlement_price = kwargs.get('settlement_price')
        self.quarter = kwargs.get('quarter')
        self.sell18bps = kwargs.get('sell18bps')
        self.asset_parameters_floating_rate_option = kwargs.get('asset_parameters_floating_rate_option')
        self.realized_vwap_performance_bps = kwargs.get('realized_vwap_performance_bps')
        self.vote_share = kwargs.get('vote_share')
        self.servicing_cost_short_pnl = kwargs.get('servicing_cost_short_pnl')
        self.total_confirmed = kwargs.get('total_confirmed')
        self.economic_forecast = kwargs.get('economic_forecast')
        self.plot_id = kwargs.get('plot_id')
        self.cluster_description = kwargs.get('cluster_description')
        self.concentration_limit = kwargs.get('concentration_limit')
        self.wind_speed = kwargs.get('wind_speed')
        self.observation_hour = kwargs.get('observation_hour')
        self.signal = kwargs.get('signal')
        self.borrower_id = kwargs.get('borrower_id')
        self.data_product = kwargs.get('data_product')
        self.buy7point5bps = kwargs.get('buy7point5bps')
        self.limit_price = kwargs.get('limit_price')
        self.bm_prime_id = kwargs.get('bm_prime_id')
        self.data_type = kwargs.get('data_type')
        self.count = kwargs.get('count')
        self.conviction = kwargs.get('conviction')
        self.rfqstate = kwargs.get('rfqstate')
        self.benchmark_maturity = kwargs.get('benchmark_maturity')
        self.gross_flow_normalized = kwargs.get('gross_flow_normalized')
        self.buy14bps = kwargs.get('buy14bps')
        self.factor_id = kwargs.get('factor_id')
        self.future_month_v26 = kwargs.get('future_month_v26')
        self.sts_fx_currency = kwargs.get('sts_fx_currency')
        self.future_month_v25 = kwargs.get('future_month_v25')
        self.bid_change = kwargs.get('bid_change')
        self.month = kwargs.get('month')
        self.future_month_v24 = kwargs.get('future_month_v24')
        self.investment_wtd = kwargs.get('investment_wtd')
        self.future_month_v23 = kwargs.get('future_month_v23')
        self.future_month_v22 = kwargs.get('future_month_v22')
        self.future_month_v21 = kwargs.get('future_month_v21')
        self.expiration = kwargs.get('expiration')
        self.leg2_reset_frequency = kwargs.get('leg2_reset_frequency')
        self.controversy_score = kwargs.get('controversy_score')
        self.proceed_asset_swap_spread = kwargs.get('proceed_asset_swap_spread')
        self.concentration_level = kwargs.get('concentration_level')
        self.importance = kwargs.get('importance')
        self.asset_classifications_gics_sector = kwargs.get('asset_classifications_gics_sector')
        self.sts_asset_name = kwargs.get('sts_asset_name')
        self.net_exposure_classification = kwargs.get('net_exposure_classification')
        self.settlement_method = kwargs.get('settlement_method')
        self.receiver_designated_maturity = kwargs.get('receiver_designated_maturity')
        self.title = kwargs.get('title')
        self.x_ref_type_id = kwargs.get('x_ref_type_id')
        self.duration = kwargs.get('duration')
        self.load = kwargs.get('load')
        self.alpha = kwargs.get('alpha')
        self.company = kwargs.get('company')
        self.settlement_frequency = kwargs.get('settlement_frequency')
        self.dist_avg7_day = kwargs.get('dist_avg7_day')
        self.in_risk_model = kwargs.get('in_risk_model')
        self.daily_net_shareholder_flows_percent = kwargs.get('daily_net_shareholder_flows_percent')
        self.filled_notional_local = kwargs.get('filled_notional_local')
        self.ever_hospitalized = kwargs.get('ever_hospitalized')
        self.meeting_number = kwargs.get('meeting_number')
        self.mid_gspread = kwargs.get('mid_gspread')
        self.days_open_unrealized_bps = kwargs.get('days_open_unrealized_bps')
        self.long_level = kwargs.get('long_level')
        self.data_description = kwargs.get('data_description')
        self.temperature_type = kwargs.get('temperature_type')
        self.gsideid = kwargs.get('gsideid')
        self.repo_rate = kwargs.get('repo_rate')
        self.division = kwargs.get('division')
        self.cloud_cover_daily_forecast = kwargs.get('cloud_cover_daily_forecast')
        self.wind_speed_daily_forecast = kwargs.get('wind_speed_daily_forecast')
        self.asset_parameters_floating_rate_day_count_fraction = kwargs.get(
            'asset_parameters_floating_rate_day_count_fraction')
        self.trade_action = kwargs.get('trade_action')
        self.action = kwargs.get('action')
        self.ctd_yield = kwargs.get('ctd_yield')
        self.arrival_haircut_vwap_normalized = kwargs.get('arrival_haircut_vwap_normalized')
        self.price_component = kwargs.get('price_component')
        self.queue_clock_time_description = kwargs.get('queue_clock_time_description')
        self.asset_parameters_receiver_day_count_fraction = kwargs.get('asset_parameters_receiver_day_count_fraction')
        self.percent_mid_execution_quantity = kwargs.get('percent_mid_execution_quantity')
        self.delta_strike = kwargs.get('delta_strike')
        self.cloud_cover = kwargs.get('cloud_cover')
        self.asset_parameters_notional_currency = kwargs.get('asset_parameters_notional_currency')
        self.buy18bps = kwargs.get('buy18bps')
        self.value_actual = kwargs.get('value_actual')
        self.upi = kwargs.get('upi')
        self.collateral_currency = kwargs.get('collateral_currency')
        self.original_country = kwargs.get('original_country')
        self.field = kwargs.get('field')
        self.geographic_focus = kwargs.get('geographic_focus')
        self.days_open_realized_bps = kwargs.get('days_open_realized_bps')
        self.fx_risk_premium_index = kwargs.get('fx_risk_premium_index')
        self.skew = kwargs.get('skew')
        self.status = kwargs.get('status')
        self.notional_currency = kwargs.get('notional_currency')
        self.sustain_emerging_markets = kwargs.get('sustain_emerging_markets')
        self.leg1_designated_maturity = kwargs.get('leg1_designated_maturity')
        self.total_price = kwargs.get('total_price')
        self.on_behalf_of = kwargs.get('on_behalf_of')
        self.test_type = kwargs.get('test_type')
        self.accrued_interest_standard = kwargs.get('accrued_interest_standard')
        self.future_month_z26 = kwargs.get('future_month_z26')
        self.future_month_z25 = kwargs.get('future_month_z25')
        self.ccg_code = kwargs.get('ccg_code')
        self.short_exposure = kwargs.get('short_exposure')
        self.leg1_fixed_payment_currency = kwargs.get('leg1_fixed_payment_currency')
        self.arrival_haircut_vwap = kwargs.get('arrival_haircut_vwap')
        self.execution_days = kwargs.get('execution_days')
        self.recall_due_date = kwargs.get('recall_due_date')
        self.forward = kwargs.get('forward')
        self.strike = kwargs.get('strike')
        self.spread_limit = kwargs.get('spread_limit')
        self.product_scope = kwargs.get('product_scope')
        self.asset_parameters_issuer_type = kwargs.get('asset_parameters_issuer_type')
        self.currency1 = kwargs.get('currency1')
        self.currency2 = kwargs.get('currency2')
        self.previous_close_realized_bps = kwargs.get('previous_close_realized_bps')
        self.days_since_reported = kwargs.get('days_since_reported')
        self.event_status = kwargs.get('event_status')
        self.vwap_in_limit = kwargs.get('vwap_in_limit')
        self.fwd_duration = kwargs.get('fwd_duration')
        self.__return = kwargs.get('return_')
        self.is_pair_basket = kwargs.get('is_pair_basket')
        self.notional_amount = kwargs.get('notional_amount')
        self.pay_or_receive = kwargs.get('pay_or_receive')
        self.total_severe = kwargs.get('total_severe')
        self.unexecuted_notional_usd = kwargs.get('unexecuted_notional_usd')
        self.expected_residual_percentage = kwargs.get('expected_residual_percentage')
        self.maturity_date = kwargs.get('maturity_date')
        self.trace_adv_sell = kwargs.get('trace_adv_sell')
        self.event_name = kwargs.get('event_name')
        self.address_line2 = kwargs.get('address_line2')
        self.indication_of_other_price_affecting_term = kwargs.get('indication_of_other_price_affecting_term')
        self.unadjusted_bid = kwargs.get('unadjusted_bid')
        self.backtest_type = kwargs.get('backtest_type')
        self.gsdeer = kwargs.get('gsdeer')
        self.asset_parameters_issuer = kwargs.get('asset_parameters_issuer')
        self.g_regional_percentile = kwargs.get('g_regional_percentile')
        self.coverage_checked = kwargs.get('coverage_checked')
        self.ois_xccy_ex_spike = kwargs.get('ois_xccy_ex_spike')
        self.total_risk = kwargs.get('total_risk')
        self.mnav = kwargs.get('mnav')
        self.market_volume = kwargs.get('market_volume')
        self.swap_annuity = kwargs.get('swap_annuity')
        self.par_asset_swap_spread = kwargs.get('par_asset_swap_spread')
        self.curr_yield7_day = kwargs.get('curr_yield7_day')
        self.pressure = kwargs.get('pressure')
        self.short_description = kwargs.get('short_description')
        self.future_month_z24 = kwargs.get('future_month_z24')
        self.feed = kwargs.get('feed')
        self.future_month_z23 = kwargs.get('future_month_z23')
        self.mkt_point1 = kwargs.get('mkt_point1')
        self.future_month_z22 = kwargs.get('future_month_z22')
        self.future_month_z21 = kwargs.get('future_month_z21')
        self.future_month_z20 = kwargs.get('future_month_z20')
        self.asset_parameters_commodity_sector = kwargs.get('asset_parameters_commodity_sector')
        self.price_notation2 = kwargs.get('price_notation2')
        self.market_buffer_threshold = kwargs.get('market_buffer_threshold')
        self.price_notation3 = kwargs.get('price_notation3')
        self.mkt_point3 = kwargs.get('mkt_point3')
        self.mkt_point2 = kwargs.get('mkt_point2')
        self.leg2_type = kwargs.get('leg2_type')
        self.mkt_point4 = kwargs.get('mkt_point4')
        self.degree_days_type = kwargs.get('degree_days_type')
        self.sentiment = kwargs.get('sentiment')
        self.investment_income = kwargs.get('investment_income')
        self.group_type = kwargs.get('group_type')
        self.forward_point_imm = kwargs.get('forward_point_imm')
        self.twap = kwargs.get('twap')
        self.client_short_name = kwargs.get('client_short_name')
        self.group_category = kwargs.get('group_category')
        self.bid_plus_ask = kwargs.get('bid_plus_ask')
        self.foreign_ccy_rate = kwargs.get('foreign_ccy_rate')
        self.election_odds = kwargs.get('election_odds')
        self.wind_direction_forecast = kwargs.get('wind_direction_forecast')
        self.require_anon_client_name = kwargs.get('require_anon_client_name')
        self.pricing_location = kwargs.get('pricing_location')
        self.beta = kwargs.get('beta')
        self.last_returns_end_date = kwargs.get('last_returns_end_date')
        self.upfront_payment_date = kwargs.get('upfront_payment_date')
        self.sell1point5bps = kwargs.get('sell1point5bps')
        self.long_exposure = kwargs.get('long_exposure')
        self.sell4point5bps = kwargs.get('sell4point5bps')
        self.tcm_cost_participation_rate20_pct = kwargs.get('tcm_cost_participation_rate20_pct')
        self.venue_type = kwargs.get('venue_type')
        self.multi_asset_class_swap = kwargs.get('multi_asset_class_swap')
        self.delta_change_id = kwargs.get('delta_change_id')
        self.implementation_id = kwargs.get('implementation_id')
        self.leg1_fixed_payment = kwargs.get('leg1_fixed_payment')
        self.es_numeric_score = kwargs.get('es_numeric_score')
        self.in_benchmark = kwargs.get('in_benchmark')
        self.action_sdr = kwargs.get('action_sdr')
        self.count_ideas_qtd = kwargs.get('count_ideas_qtd')
        self.knock_out_price = kwargs.get('knock_out_price')
        self.ctd_asset_id = kwargs.get('ctd_asset_id')
        self.buy10bps = kwargs.get('buy10bps')
        self.precipitation = kwargs.get('precipitation')
        self.value_type = kwargs.get('value_type')
        self.beta_adjusted_net_exposure = kwargs.get('beta_adjusted_net_exposure')
        self.estimated_rod_volume = kwargs.get('estimated_rod_volume')
        self.sell14bps = kwargs.get('sell14bps')
        self.excess_return_price = kwargs.get('excess_return_price')
        self.fx_pnl = kwargs.get('fx_pnl')
        self.asset_classifications_gics_industry_group = kwargs.get('asset_classifications_gics_industry_group')
        self.lending_sec_id = kwargs.get('lending_sec_id')
        self.dollar_duration = kwargs.get('dollar_duration')
        self.equity_theta = kwargs.get('equity_theta')
        self.dv01 = kwargs.get('dv01')
        self.start_date = kwargs.get('start_date')
        self.mixed_swap = kwargs.get('mixed_swap')
        self.swaption_premium = kwargs.get('swaption_premium')
        self.snowfall = kwargs.get('snowfall')
        self.liquidity_bucket_buy = kwargs.get('liquidity_bucket_buy')
        self.mic = kwargs.get('mic')
        self.latitude = kwargs.get('latitude')
        self.mid = kwargs.get('mid')
        self.implied_repo = kwargs.get('implied_repo')
        self.long = kwargs.get('long')
        self.covered_bond = kwargs.get('covered_bond')
        self.region_code = kwargs.get('region_code')
        self.buy20cents = kwargs.get('buy20cents')
        self.long_weight = kwargs.get('long_weight')
        self.calculation_time = kwargs.get('calculation_time')
        self.liquidity_bucket_sell = kwargs.get('liquidity_bucket_sell')
        self.days_open_unrealized_cash = kwargs.get('days_open_unrealized_cash')
        self.temperature = kwargs.get('temperature')
        self.average_realized_variance = kwargs.get('average_realized_variance')
        self.rating_fitch = kwargs.get('rating_fitch')
        self.financial_returns_score = kwargs.get('financial_returns_score')
        self.year_or_quarter = kwargs.get('year_or_quarter')
        self.non_symbol_dimensions = kwargs.get('non_symbol_dimensions')
        self.commodities_forecast = kwargs.get('commodities_forecast')
        self.covid19_by_state = kwargs.get('covid19_by_state')
        self.percentage_expected_residual = kwargs.get('percentage_expected_residual')
        self.hospital_name = kwargs.get('hospital_name')
        self.buy90cents = kwargs.get('buy90cents')
        self.period_type = kwargs.get('period_type')
        self.asset_classifications_country_name = kwargs.get('asset_classifications_country_name')
        self.total_hospitalized = kwargs.get('total_hospitalized')
        self.pegged_refill_interval = kwargs.get('pegged_refill_interval')
        self.fatalities_probable = kwargs.get('fatalities_probable')
        self.administrative_region = kwargs.get('administrative_region')
        self.__open = kwargs.get('open_')
        self.cusip = kwargs.get('cusip')
        self.total_confirmed_by_state = kwargs.get('total_confirmed_by_state')
        self.wind_attribute = kwargs.get('wind_attribute')
        self.spread_option_atm_fwd_rate = kwargs.get('spread_option_atm_fwd_rate')
        self.net_exposure = kwargs.get('net_exposure')
        self.is_legacy_pair_basket = kwargs.get('is_legacy_pair_basket')
        self.issuer_type = kwargs.get('issuer_type')
        self.buy70cents = kwargs.get('buy70cents')
        self.strike_reference = kwargs.get('strike_reference')
        self.asset_count = kwargs.get('asset_count')
        self.is_order_in_limit = kwargs.get('is_order_in_limit')
        self.fundamental_metric = kwargs.get('fundamental_metric')
        self.quote_status_id = kwargs.get('quote_status_id')
        self.absolute_value = kwargs.get('absolute_value')
        self.closing_report = kwargs.get('closing_report')
        self.previous_total_confirmed = kwargs.get('previous_total_confirmed')
        self.long_tenor = kwargs.get('long_tenor')
        self.multiplier = kwargs.get('multiplier')
        self.buy40cents = kwargs.get('buy40cents')
        self.asset_count_priced = kwargs.get('asset_count_priced')
        self.vote_direction = kwargs.get('vote_direction')
        self.implied_repo_rate = kwargs.get('implied_repo_rate')
        self.settlement_currency = kwargs.get('settlement_currency')
        self.wtd_degree_days_forecast = kwargs.get('wtd_degree_days_forecast')
        self.indication_of_collateralization = kwargs.get('indication_of_collateralization')
        self.future_month_n26 = kwargs.get('future_month_n26')
        self.lending_partner_fee = kwargs.get('lending_partner_fee')
        self.future_month_n25 = kwargs.get('future_month_n25')
        self.future_month_n24 = kwargs.get('future_month_n24')
        self.primary_vwap_realized_bps = kwargs.get('primary_vwap_realized_bps')
        self.future_month_n23 = kwargs.get('future_month_n23')
        self.future_month_n22 = kwargs.get('future_month_n22')
        self.future_month_n21 = kwargs.get('future_month_n21')
        self.break_even_inflation = kwargs.get('break_even_inflation')
        self.pnl_ytd = kwargs.get('pnl_ytd')
        self.leg1_return_type = kwargs.get('leg1_return_type')
        self.tenor2 = kwargs.get('tenor2')
        self.reset_frequency = kwargs.get('reset_frequency')
        self.asset_parameters_payer_frequency = kwargs.get('asset_parameters_payer_frequency')
        self.degree_days_forecast = kwargs.get('degree_days_forecast')
        self.is_manually_silenced = kwargs.get('is_manually_silenced')
        self.buy3bps = kwargs.get('buy3bps')
        self.last_updated_by_id = kwargs.get('last_updated_by_id')
        self.legal_entity_acct = kwargs.get('legal_entity_acct')
        self.target_shareholder_meeting_date = kwargs.get('target_shareholder_meeting_date')
        self.pace_of_rollp0 = kwargs.get('pace_of_rollp0')
        self.controversy_percentile = kwargs.get('controversy_percentile')
        self.leg1_notional_currency = kwargs.get('leg1_notional_currency')
        self.expiration_date = kwargs.get('expiration_date')
        self.floating_rate_day_count_fraction = kwargs.get('floating_rate_day_count_fraction')
        self.call_last_date = kwargs.get('call_last_date')
        self.factor_return = kwargs.get('factor_return')
        self.passive_flow_ratio = kwargs.get('passive_flow_ratio')
        self.composite5_day_adv = kwargs.get('composite5_day_adv')
        self.marginal_contribution_to_risk = kwargs.get('marginal_contribution_to_risk')
        self.close_date = kwargs.get('close_date')
        self.temperature_hour_forecast = kwargs.get('temperature_hour_forecast')
        self.new_ideas_wtd = kwargs.get('new_ideas_wtd')
        self.asset_class_sdr = kwargs.get('asset_class_sdr')
        self.yield_to_worst = kwargs.get('yield_to_worst')
        self.closing_price = kwargs.get('closing_price')
        self.turnover_composite_adjusted = kwargs.get('turnover_composite_adjusted')
        self.comment = kwargs.get('comment')
        self.source_symbol = kwargs.get('source_symbol')
        self.ask_unadjusted = kwargs.get('ask_unadjusted')
        self.restrict_external_derived_data = kwargs.get('restrict_external_derived_data')
        self.ask_change = kwargs.get('ask_change')
        self.count_ideas_mtd = kwargs.get('count_ideas_mtd')
        self.end_date = kwargs.get('end_date')
        self.sunshine = kwargs.get('sunshine')
        self.contract_type = kwargs.get('contract_type')
        self.momentum_type = kwargs.get('momentum_type')
        self.specific_risk = kwargs.get('specific_risk')
        self.mdapi = kwargs.get('mdapi')
        self.payoff_qtd = kwargs.get('payoff_qtd')
        self.loss = kwargs.get('loss')
        self.midcurve_vol = kwargs.get('midcurve_vol')
        self.sell6bps = kwargs.get('sell6bps')
        self.trading_cost_pnl = kwargs.get('trading_cost_pnl')
        self.price_notation_type = kwargs.get('price_notation_type')
        self.price = kwargs.get('price')
        self.payment_quantity = kwargs.get('payment_quantity')
        self.redemption_date = kwargs.get('redemption_date')
        self.leg2_notional_currency = kwargs.get('leg2_notional_currency')
        self.sub_region = kwargs.get('sub_region')
        self.benchmark = kwargs.get('benchmark')
        self.tcm_cost_participation_rate15_pct = kwargs.get('tcm_cost_participation_rate15_pct')
        self.fiscal_year = kwargs.get('fiscal_year')
        self.recall_date = kwargs.get('recall_date')
        self.esg_metric_value = kwargs.get('esg_metric_value')
        self.internal = kwargs.get('internal')
        self.gender = kwargs.get('gender')
        self.asset_classifications_gics_industry = kwargs.get('asset_classifications_gics_industry')
        self.adjusted_bid_price = kwargs.get('adjusted_bid_price')
        self.low_unadjusted = kwargs.get('low_unadjusted')
        self.macs_secondary_asset_class = kwargs.get('macs_secondary_asset_class')
        self.confirmed_per_million = kwargs.get('confirmed_per_million')
        self.data_source_id = kwargs.get('data_source_id')
        self.integrated_score = kwargs.get('integrated_score')
        self.buy7bps = kwargs.get('buy7bps')
        self.arrival_mid_unrealized_cash = kwargs.get('arrival_mid_unrealized_cash')
        self.knock_in_price = kwargs.get('knock_in_price')
        self.event = kwargs.get('event')
        self.is_intraday_auction = kwargs.get('is_intraday_auction')
        self.location_name = kwargs.get('location_name')
        self.coupon = kwargs.get('coupon')
        self.percentage_auction_executed_quantity = kwargs.get('percentage_auction_executed_quantity')
        self.avg_yield7_day = kwargs.get('avg_yield7_day')
        self.original_dissemination_id = kwargs.get('original_dissemination_id')
        self.total_on_vent = kwargs.get('total_on_vent')
        self.twap_unrealized_cash = kwargs.get('twap_unrealized_cash')
        self.sts_credit_market = kwargs.get('sts_credit_market')
        self.ons_code = kwargs.get('ons_code')
        self.passive_touch_fills_percentage = kwargs.get('passive_touch_fills_percentage')
        self.seniority = kwargs.get('seniority')
        self.leg1_index = kwargs.get('leg1_index')
        self.high_unadjusted = kwargs.get('high_unadjusted')
        self.submission_event = kwargs.get('submission_event')
        self.tv_product_mnemonic = kwargs.get('tv_product_mnemonic')
        self.avg_trade_rate_label = kwargs.get('avg_trade_rate_label')
        self.last_activity_date = kwargs.get('last_activity_date')
        self.price_to_cash = kwargs.get('price_to_cash')
        self.buy10cents = kwargs.get('buy10cents')
        self.nav_spread = kwargs.get('nav_spread')
        self.venue_mic = kwargs.get('venue_mic')
        self.dollar_total_return = kwargs.get('dollar_total_return')
        self.block_unit = kwargs.get('block_unit')
        self.mid_spread = kwargs.get('mid_spread')
        self.istat_province_code = kwargs.get('istat_province_code')
        self.total_recovered_by_state = kwargs.get('total_recovered_by_state')
        self.repurchase_rate = kwargs.get('repurchase_rate')
        self.data_source = kwargs.get('data_source')
        self.total_being_tested = kwargs.get('total_being_tested')
        self.cleared_or_bilateral = kwargs.get('cleared_or_bilateral')
        self.metric_name = kwargs.get('metric_name')
        self.ask_gspread = kwargs.get('ask_gspread')
        self.forecast_hour = kwargs.get('forecast_hour')
        self.leg2_payment_type = kwargs.get('leg2_payment_type')
        self.cal_spread_mis_pricing = kwargs.get('cal_spread_mis_pricing')
        self.total_tested_negative = kwargs.get('total_tested_negative')
        self.rate366 = kwargs.get('rate366')
        self.platform = kwargs.get('platform')
        self.rate365 = kwargs.get('rate365')
        self.fixed_rate_frequency = kwargs.get('fixed_rate_frequency')
        self.rate360 = kwargs.get('rate360')
        self.is_continuous = kwargs.get('is_continuous')
        self.value = kwargs.get('value')
        self.payer_designated_maturity = kwargs.get('payer_designated_maturity')
        self.product_type = kwargs.get('product_type')
        self.mdv22_day = kwargs.get('mdv22_day')
        self.twap_realized_bps = kwargs.get('twap_realized_bps')
        self.test_measure_label = kwargs.get('test_measure_label')
        self.quantity = kwargs.get('quantity')
        self.report_id = kwargs.get('report_id')
        self.index_weight = kwargs.get('index_weight')
        self.macs_primary_asset_class = kwargs.get('macs_primary_asset_class')
        self.trader = kwargs.get('trader')
        self.leg2_price_type = kwargs.get('leg2_price_type')
        self.total_active = kwargs.get('total_active')
        self.gsid2 = kwargs.get('gsid2')
        self.matched_maturity_ois_swap_spread = kwargs.get('matched_maturity_ois_swap_spread')
        self.valuation_date = kwargs.get('valuation_date')
        self.restrict_gs_federation = kwargs.get('restrict_gs_federation')
        self.position_source = kwargs.get('position_source')
        self.tcm_cost_horizon6_hour = kwargs.get('tcm_cost_horizon6_hour')
        self.buy200cents = kwargs.get('buy200cents')
        self.vwap_unrealized_bps = kwargs.get('vwap_unrealized_bps')
        self.price_to_book = kwargs.get('price_to_book')
        self.isin = kwargs.get('isin')
        self.pl_id = kwargs.get('pl_id')
        self.last_returns_start_date = kwargs.get('last_returns_start_date')
        self.collateral_value_variance = kwargs.get('collateral_value_variance')
        self.year = kwargs.get('year')
        self.forecast_period = kwargs.get('forecast_period')
        self.call_first_date = kwargs.get('call_first_date')
        self.data_set_ids = kwargs.get('data_set_ids')
        self.economic_terms_hash = kwargs.get('economic_terms_hash')
        self.num_beds = kwargs.get('num_beds')
        self.sell20bps = kwargs.get('sell20bps')
        self.client_type = kwargs.get('client_type')
        self.percentage_close_executed_quantity = kwargs.get('percentage_close_executed_quantity')
        self.macaulay_duration = kwargs.get('macaulay_duration')
        self.available_inventory = kwargs.get('available_inventory')
        self.est1_day_complete_pct = kwargs.get('est1_day_complete_pct')
        self.relative_hit_rate_ytd = kwargs.get('relative_hit_rate_ytd')
        self.created_by_id = kwargs.get('created_by_id')
        self.market_data_type = kwargs.get('market_data_type')
        self.real_short_rates_contribution = kwargs.get('real_short_rates_contribution')
        self.metric_category = kwargs.get('metric_category')
        self.annualized_carry = kwargs.get('annualized_carry')
        self.value_previous = kwargs.get('value_previous')
        self.transmission_classification = kwargs.get('transmission_classification')
        self.avg_trade_rate = kwargs.get('avg_trade_rate')
        self.short_level = kwargs.get('short_level')
        self.version = kwargs.get('version')
        self.category_type = kwargs.get('category_type')
        self.policy_rate_expectation = kwargs.get('policy_rate_expectation')
        self.upload_date = kwargs.get('upload_date')
        self.block_off_facility = kwargs.get('block_off_facility')
        self.unrealized_vwap_performance_usd = kwargs.get('unrealized_vwap_performance_usd')
        self.pace_of_rollp75 = kwargs.get('pace_of_rollp75')
        self.earnings_per_share_positive = kwargs.get('earnings_per_share_positive')
        self.num_icu_beds = kwargs.get('num_icu_beds')
        self.bucket_volume_in_percentage = kwargs.get('bucket_volume_in_percentage')
        self.estimated_trading_cost = kwargs.get('estimated_trading_cost')
        self.eid = kwargs.get('eid')
        self.relative_return_qtd = kwargs.get('relative_return_qtd')
        self.assessed_test_measure = kwargs.get('assessed_test_measure')
        self.mkt_quoting_style = kwargs.get('mkt_quoting_style')
        self.expiration_tenor = kwargs.get('expiration_tenor')
        self.price_limit = kwargs.get('price_limit')
        self.market_model_id = kwargs.get('market_model_id')
        self.receiver_frequency = kwargs.get('receiver_frequency')
        self.realized_correlation = kwargs.get('realized_correlation')
        self.issue_status = kwargs.get('issue_status')
        self.collateral_value_actual = kwargs.get('collateral_value_actual')
        self.atm_fwd_rate = kwargs.get('atm_fwd_rate')
        self.tcm_cost_participation_rate75_pct = kwargs.get('tcm_cost_participation_rate75_pct')
        self.close = kwargs.get('close')
        self.es_product_impact_score = kwargs.get('es_product_impact_score')
        self.equity_vega = kwargs.get('equity_vega')
        self.executed_fill_quantity = kwargs.get('executed_fill_quantity')
        self.lender_payment = kwargs.get('lender_payment')
        self.five_day_move = kwargs.get('five_day_move')
        self.value_format = kwargs.get('value_format')
        self.wind_chill_forecast = kwargs.get('wind_chill_forecast')
        self.target_notional = kwargs.get('target_notional')
        self.fill_leg_id = kwargs.get('fill_leg_id')
        self.rationale = kwargs.get('rationale')
        self.realized_twap_performance_bps = kwargs.get('realized_twap_performance_bps')
        self.last_updated_since = kwargs.get('last_updated_since')
        self.total_tests = kwargs.get('total_tests')
        self.equities_contribution = kwargs.get('equities_contribution')
        self.simon_id = kwargs.get('simon_id')
        self.congestion = kwargs.get('congestion')
        self.notes = kwargs.get('notes')
        self.total_probable_senior_home = kwargs.get('total_probable_senior_home')
        self.event_category = kwargs.get('event_category')
        self.average_fill_rate = kwargs.get('average_fill_rate')
        self.unadjusted_open = kwargs.get('unadjusted_open')
        self.criticality = kwargs.get('criticality')
        self.bid_ask_spread = kwargs.get('bid_ask_spread')
        self.arrival_mid_unrealized_bps = kwargs.get('arrival_mid_unrealized_bps')
        self.option_type = kwargs.get('option_type')
        self.termination_date = kwargs.get('termination_date')
        self.queries_per_second = kwargs.get('queries_per_second')
        self.liquidity_type = kwargs.get('liquidity_type')
        self.credit_limit = kwargs.get('credit_limit')
        self.rank_qtd = kwargs.get('rank_qtd')
        self.combined_key = kwargs.get('combined_key')
        self.gir_fx_forecast = kwargs.get('gir_fx_forecast')
        self.effective_tenor = kwargs.get('effective_tenor')
        self.gir_commodities_forecast = kwargs.get('gir_commodities_forecast')
        self.relative_humidity_daily_forecast = kwargs.get('relative_humidity_daily_forecast')
        self.std30_days_subsidized_yield = kwargs.get('std30_days_subsidized_yield')
        self.annualized_tracking_error = kwargs.get('annualized_tracking_error')
        self.future_month_f26 = kwargs.get('future_month_f26')
        self.future_month_f25 = kwargs.get('future_month_f25')
        self.vol_swap = kwargs.get('vol_swap')
        self.future_month_f24 = kwargs.get('future_month_f24')
        self.heat_index_daily_forecast = kwargs.get('heat_index_daily_forecast')
        self.future_month_f23 = kwargs.get('future_month_f23')
        self.real_fci = kwargs.get('real_fci')
        self.block_trades_and_large_notional_off_facility_swaps = kwargs.get(
            'block_trades_and_large_notional_off_facility_swaps')
        self.future_month_f22 = kwargs.get('future_month_f22')
        self.buy1point5bps = kwargs.get('buy1point5bps')
        self.future_month_f21 = kwargs.get('future_month_f21')
        self.expiration_settlement_date = kwargs.get('expiration_settlement_date')
        self.absolute_return_qtd = kwargs.get('absolute_return_qtd')
        self.gross_exposure = kwargs.get('gross_exposure')
        self.volume = kwargs.get('volume')
        self.adv = kwargs.get('adv')
        self.short_conviction_medium = kwargs.get('short_conviction_medium')
        self.complete_test_measure = kwargs.get('complete_test_measure')
        self.exchange = kwargs.get('exchange')
        self.es_policy_score = kwargs.get('es_policy_score')
        self.roll_volume_std = kwargs.get('roll_volume_std')
        self.temperature_daily_forecast = kwargs.get('temperature_daily_forecast')
        self.relative_payoff_qtd = kwargs.get('relative_payoff_qtd')
        self.on_loan_percentage = kwargs.get('on_loan_percentage')
        self.twap_remaining_slices = kwargs.get('twap_remaining_slices')
        self.fair_variance = kwargs.get('fair_variance')
        self.hit_rate_wtd = kwargs.get('hit_rate_wtd')
        self.previous_close_realized_cash = kwargs.get('previous_close_realized_cash')
        self.realized_volatility = kwargs.get('realized_volatility')
        self.unexecuted_quantity = kwargs.get('unexecuted_quantity')
        self.proceeds_asset_swap_spread1m = kwargs.get('proceeds_asset_swap_spread1m')
        self.clone_parent_id = kwargs.get('clone_parent_id')
        self.wind_speed_hourly_forecast = kwargs.get('wind_speed_hourly_forecast')
        self.etf_flow_ratio = kwargs.get('etf_flow_ratio')
        self.asset_parameters_receiver_rate_option = kwargs.get('asset_parameters_receiver_rate_option')
        self.buy60cents = kwargs.get('buy60cents')
        self.security_sub_type_id = kwargs.get('security_sub_type_id')
        self.message = kwargs.get('message')
        self.sts_rates_country = kwargs.get('sts_rates_country')
        self.sell65cents = kwargs.get('sell65cents')
        self.horizon = kwargs.get('horizon')
        self.would_if_good_level = kwargs.get('would_if_good_level')
        self.buffer_threshold_required = kwargs.get('buffer_threshold_required')
        self.face_value = kwargs.get('face_value')
        self.roll_volume_hist = kwargs.get('roll_volume_hist')
        self.counter_party_status = kwargs.get('counter_party_status')
        self.composite22_day_adv = kwargs.get('composite22_day_adv')
        self.percentage_far_executed_quantity = kwargs.get('percentage_far_executed_quantity')
        self.loan_spread_required = kwargs.get('loan_spread_required')
        self.asset_class = kwargs.get('asset_class')
        self.sovereign_spread_contribution = kwargs.get('sovereign_spread_contribution')
        self.ric = kwargs.get('ric')
        self.rate_type = kwargs.get('rate_type')
        self.total_fatalities_senior_home = kwargs.get('total_fatalities_senior_home')
        self.loan_status = kwargs.get('loan_status')
        self.short_weight = kwargs.get('short_weight')
        self.geography_id = kwargs.get('geography_id')
        self.sell7point5bps = kwargs.get('sell7point5bps')
        self.nav = kwargs.get('nav')
        self.fiscal_quarter = kwargs.get('fiscal_quarter')
        self.version_string = kwargs.get('version_string')
        self.payoff_ytd = kwargs.get('payoff_ytd')
        self.market_impact = kwargs.get('market_impact')
        self.event_type = kwargs.get('event_type')
        self.fill_price = kwargs.get('fill_price')
        self.asset_count_long = kwargs.get('asset_count_long')
        self.sell180cents = kwargs.get('sell180cents')
        self.spot = kwargs.get('spot')
        self.application_id = kwargs.get('application_id')
        self.indicative_close_price = kwargs.get('indicative_close_price')
        self.swap_spread = kwargs.get('swap_spread')
        self.trading_restriction = kwargs.get('trading_restriction')
        self.asset_parameters_pay_or_receive = kwargs.get('asset_parameters_pay_or_receive')
        self.price_spot_entry_unit = kwargs.get('price_spot_entry_unit')
        self.unrealized_arrival_performance_bps = kwargs.get('unrealized_arrival_performance_bps')
        self.city = kwargs.get('city')
        self.pnl_wtd = kwargs.get('pnl_wtd')
        self.covariance = kwargs.get('covariance')
        self.bucket_volume_in_shares = kwargs.get('bucket_volume_in_shares')
        self.commodity_forecast = kwargs.get('commodity_forecast')
        self.valid = kwargs.get('valid')
        self.sts_commodity = kwargs.get('sts_commodity')
        self.initial_pricing_date = kwargs.get('initial_pricing_date')
        self.indication_of_end_user_exception = kwargs.get('indication_of_end_user_exception')
        self.wind_direction_hourly_forecast = kwargs.get('wind_direction_hourly_forecast')
        self.es_score = kwargs.get('es_score')
        self.__yield = kwargs.get('yield_')
        self.fatalities_underlying_conditions_present = kwargs.get('fatalities_underlying_conditions_present')
        self.price_range_in_ticks = kwargs.get('price_range_in_ticks')
        self.pace_of_rollp25 = kwargs.get('pace_of_rollp25')
        self.day_close_realized_usd = kwargs.get('day_close_realized_usd')
        self.pct_change = kwargs.get('pct_change')
        self.brightness_type = kwargs.get('brightness_type')
        self.future_month3_m = kwargs.get('future_month3_m')
        self.number_of_rolls = kwargs.get('number_of_rolls')
        self.iso_country_code_numeric = kwargs.get('iso_country_code_numeric')
        self.price_type = kwargs.get('price_type')
        self.realized_vwap_performance_usd = kwargs.get('realized_vwap_performance_usd')
        self.fuel_type = kwargs.get('fuel_type')
        self.bbid = kwargs.get('bbid')
        self.vega_notional_amount = kwargs.get('vega_notional_amount')
        self.fatalities_underlying_conditions_absent = kwargs.get('fatalities_underlying_conditions_absent')
        self.effective_date = kwargs.get('effective_date')
        self.capped = kwargs.get('capped')
        self.rating = kwargs.get('rating')
        self.option_currency = kwargs.get('option_currency')
        self.is_close_auction = kwargs.get('is_close_auction')
        self.volatility = kwargs.get('volatility')
        self.avg_vent_util = kwargs.get('avg_vent_util')
        self.underlying_asset_ids = kwargs.get('underlying_asset_ids')
        self.buy6point5bps = kwargs.get('buy6point5bps')
        self.vwap_in_limit_realized_cash = kwargs.get('vwap_in_limit_realized_cash')
        self.estimated_closing_auction_volume = kwargs.get('estimated_closing_auction_volume')
        self.sell2bps = kwargs.get('sell2bps')
        self.annual_risk = kwargs.get('annual_risk')
        self.eti = kwargs.get('eti')
        self.vwap_in_limit_realized_bps = kwargs.get('vwap_in_limit_realized_bps')
        self.rank_mtd = kwargs.get('rank_mtd')
        self.market_buffer = kwargs.get('market_buffer')
        self.future_month_j24 = kwargs.get('future_month_j24')
        self.future_month_j23 = kwargs.get('future_month_j23')
        self.oe_id = kwargs.get('oe_id')
        self.future_month_j22 = kwargs.get('future_month_j22')
        self.future_month_j21 = kwargs.get('future_month_j21')
        self.bbid_equivalent = kwargs.get('bbid_equivalent')
        self.init_buffer_threshold_required = kwargs.get('init_buffer_threshold_required')
        self.leg2_designated_maturity = kwargs.get('leg2_designated_maturity')
        self.matched_maturity_ois_swap_rate = kwargs.get('matched_maturity_ois_swap_rate')
        self.fair_price = kwargs.get('fair_price')
        self.participation_rate_in_limit = kwargs.get('participation_rate_in_limit')
        self.ext_mkt_class = kwargs.get('ext_mkt_class')
        self.price_currency = kwargs.get('price_currency')
        self.failed_count = kwargs.get('failed_count')
        self.leg1_index_location = kwargs.get('leg1_index_location')
        self.supra_strategy = kwargs.get('supra_strategy')
        self.day_count_convention = kwargs.get('day_count_convention')
        self.rounded_notional_amount1 = kwargs.get('rounded_notional_amount1')
        self.rounded_notional_amount2 = kwargs.get('rounded_notional_amount2')
        self.factor_source = kwargs.get('factor_source')
        self.future_month_j26 = kwargs.get('future_month_j26')
        self.lending_sec_type = kwargs.get('lending_sec_type')
        self.future_month_j25 = kwargs.get('future_month_j25')
        self.leverage = kwargs.get('leverage')
        self.forecast_day = kwargs.get('forecast_day')
        self.option_family = kwargs.get('option_family')
        self.generator_output = kwargs.get('generator_output')
        self.price_spot_stop_loss_value = kwargs.get('price_spot_stop_loss_value')
        self.kpi_id = kwargs.get('kpi_id')
        self.wind_generation = kwargs.get('wind_generation')
        self.percentage_mid_executed_quantity = kwargs.get('percentage_mid_executed_quantity')
        self.borrow_cost = kwargs.get('borrow_cost')
        self.knock_out_direction = kwargs.get('knock_out_direction')
        self.risk_model = kwargs.get('risk_model')
        self.asset_parameters_vendor = kwargs.get('asset_parameters_vendor')
        self.fair_value = kwargs.get('fair_value')
        self.pressure_hourly_forecast = kwargs.get('pressure_hourly_forecast')
        self.local_ccy_rate = kwargs.get('local_ccy_rate')
        self.end_user_exception = kwargs.get('end_user_exception')
        self.sell90cents = kwargs.get('sell90cents')
        self.execution_venue = kwargs.get('execution_venue')
        self.primary_vwap_in_limit_realized_bps = kwargs.get('primary_vwap_in_limit_realized_bps')
        self.approve_rebalance = kwargs.get('approve_rebalance')
        self.adjusted_close_price = kwargs.get('adjusted_close_price')
        self.lms_id = kwargs.get('lms_id')
        self.rebate_rate = kwargs.get('rebate_rate')
        self.sell130cents = kwargs.get('sell130cents')
        self.sell32bps = kwargs.get('sell32bps')
        self.pace_of_rollp50 = kwargs.get('pace_of_rollp50')
        self.price_move_vs_arrival = kwargs.get('price_move_vs_arrival')
        self.strike_relative = kwargs.get('strike_relative')
        self.pressure_type = kwargs.get('pressure_type')
        self.buy40bps = kwargs.get('buy40bps')
        self.price_notation = kwargs.get('price_notation')
        self.strategy = kwargs.get('strategy')
        self.issue_status_date = kwargs.get('issue_status_date')
        self.lender_income = kwargs.get('lender_income')
        self.pb_client_id = kwargs.get('pb_client_id')
        self.istat_region_code = kwargs.get('istat_region_code')
        self.sell9bps = kwargs.get('sell9bps')
        self.owner_id = kwargs.get('owner_id')
        self.composite10_day_adv = kwargs.get('composite10_day_adv')
        self.max_loan_balance = kwargs.get('max_loan_balance')
        self.idea_activity_type = kwargs.get('idea_activity_type')
        self.sell60cents = kwargs.get('sell60cents')
        self.idea_source = kwargs.get('idea_source')
        self.ever_on_vent = kwargs.get('ever_on_vent')
        self.buy15cents = kwargs.get('buy15cents')
        self.unadjusted_ask = kwargs.get('unadjusted_ask')
        self.contribution_name = kwargs.get('contribution_name')
        self.given_plus_paid = kwargs.get('given_plus_paid')
        self.last_fill_price = kwargs.get('last_fill_price')
        self.short_conviction_small = kwargs.get('short_conviction_small')
        self.upfront_payment_currency = kwargs.get('upfront_payment_currency')
        self.spot_settlement_date = kwargs.get('spot_settlement_date')
        self.matrix_order = kwargs.get('matrix_order')
        self.date_index = kwargs.get('date_index')
        self.payer_day_count_fraction = kwargs.get('payer_day_count_fraction')
        self.asset_classifications_is_primary = kwargs.get('asset_classifications_is_primary')
        self.break_even_inflation_change = kwargs.get('break_even_inflation_change')
        self.buy130cents = kwargs.get('buy130cents')
        self.dwi_contribution = kwargs.get('dwi_contribution')
        self.asset2_id = kwargs.get('asset2_id')
        self.average_fill_price = kwargs.get('average_fill_price')
        self.depth_spread_score = kwargs.get('depth_spread_score')
        self.sell10cents = kwargs.get('sell10cents')
        self.sub_account = kwargs.get('sub_account')
        self.buy65cents = kwargs.get('buy65cents')
        self.bond_cds_basis = kwargs.get('bond_cds_basis')
        self.vendor = kwargs.get('vendor')
        self.data_set = kwargs.get('data_set')
        self.notional_amount2 = kwargs.get('notional_amount2')
        self.notional_amount1 = kwargs.get('notional_amount1')
        self.queueing_time = kwargs.get('queueing_time')
        self.ann_return5_year = kwargs.get('ann_return5_year')
        self.volume_start_of_day = kwargs.get('volume_start_of_day')
        self.price_notation3_type = kwargs.get('price_notation3_type')
        self.asset_parameters_floating_rate_designated_maturity = kwargs.get(
            'asset_parameters_floating_rate_designated_maturity')
        self.executed_notional_local = kwargs.get('executed_notional_local')
        self.business_sponsor = kwargs.get('business_sponsor')
        self.unexplained = kwargs.get('unexplained')
        self.seasonal_adjustment_short = kwargs.get('seasonal_adjustment_short')
        self.metric = kwargs.get('metric')
        self.ask = kwargs.get('ask')
        self.close_price = kwargs.get('close_price')
        self.sell100cents = kwargs.get('sell100cents')
        self.buy180cents = kwargs.get('buy180cents')
        self.absolute_strike = kwargs.get('absolute_strike')
        self.sell3point5bps = kwargs.get('sell3point5bps')
        self.liquidity_score_buy = kwargs.get('liquidity_score_buy')
        self.payment_frequency = kwargs.get('payment_frequency')
        self.expense_ratio_net_bps = kwargs.get('expense_ratio_net_bps')
        self.metric_type = kwargs.get('metric_type')
        self.rank_ytd = kwargs.get('rank_ytd')
        self.leg1_spread = kwargs.get('leg1_spread')
        self.coverage_region = kwargs.get('coverage_region')
        self.absolute_return_ytd = kwargs.get('absolute_return_ytd')
        self.day_count_convention2 = kwargs.get('day_count_convention2')
        self.fwdtier = kwargs.get('fwdtier')
        self.degree_days = kwargs.get('degree_days')
        self.turnover_adjusted = kwargs.get('turnover_adjusted')
        self.price_spot_target_value = kwargs.get('price_spot_target_value')
        self.market_data_point = kwargs.get('market_data_point')
        self.num_of_funds = kwargs.get('num_of_funds')
        self.execution_id = kwargs.get('execution_id')
        self.turnover_unadjusted = kwargs.get('turnover_unadjusted')
        self.leg1_floating_index = kwargs.get('leg1_floating_index')
        self.hedge_annualized_volatility = kwargs.get('hedge_annualized_volatility')
        self.benchmark_currency = kwargs.get('benchmark_currency')
        self.futures_contract = kwargs.get('futures_contract')
        self.name = kwargs.get('name')
        self.aum = kwargs.get('aum')
        self.leg1_day_count_convention = kwargs.get('leg1_day_count_convention')
        self.cbs_code = kwargs.get('cbs_code')
        self.folder_name = kwargs.get('folder_name')
        self.api_usage = kwargs.get('api_usage')
        self.twap_interval = kwargs.get('twap_interval')
        self.unique_id = kwargs.get('unique_id')
        self.option_expiration_date = kwargs.get('option_expiration_date')
        self.swaption_atm_fwd_rate = kwargs.get('swaption_atm_fwd_rate')
        self.live_date = kwargs.get('live_date')
        self.corporate_action_type = kwargs.get('corporate_action_type')
        self.prime_id = kwargs.get('prime_id')
        self.description = kwargs.get('description')
        self.asset_classifications_is_country_primary = kwargs.get('asset_classifications_is_country_primary')
        self.rebate_rate_limit = kwargs.get('rebate_rate_limit')
        self.factor = kwargs.get('factor')
        self.days_on_loan = kwargs.get('days_on_loan')
        self.long_conviction_small = kwargs.get('long_conviction_small')
        self.sell40cents = kwargs.get('sell40cents')
        self.relative_payoff_ytd = kwargs.get('relative_payoff_ytd')
        self.gsfeer = kwargs.get('gsfeer')
        self.relative_hit_rate_qtd = kwargs.get('relative_hit_rate_qtd')
        self.wam = kwargs.get('wam')
        self.wal = kwargs.get('wal')
        self.quantityccy = kwargs.get('quantityccy')
        self.backtest_id = kwargs.get('backtest_id')
        self.dirty_price = kwargs.get('dirty_price')
        self.corporate_spread_contribution = kwargs.get('corporate_spread_contribution')
        self.relative_humidity_hourly_forecast = kwargs.get('relative_humidity_hourly_forecast')
        self.multiple_score = kwargs.get('multiple_score')
        self.beta_adjusted_exposure = kwargs.get('beta_adjusted_exposure')
        self.dividend_points = kwargs.get('dividend_points')
        self.brightness = kwargs.get('brightness')
        self.asset_parameters_receiver_designated_maturity = kwargs.get(
            'asset_parameters_receiver_designated_maturity')
        self.bos_in_ticks_description = kwargs.get('bos_in_ticks_description')
        self.test_id = kwargs.get('test_id')
        self.implied_correlation = kwargs.get('implied_correlation')
        self.normalized_performance = kwargs.get('normalized_performance')
        self.bytes_consumed = kwargs.get('bytes_consumed')
        self.swaption_vol = kwargs.get('swaption_vol')
        self.estimated_closing_volume = kwargs.get('estimated_closing_volume')
        self.issuer = kwargs.get('issuer')
        self.dividend_yield = kwargs.get('dividend_yield')
        self.market_type = kwargs.get('market_type')
        self.num_units_lower = kwargs.get('num_units_lower')
        self.source_origin = kwargs.get('source_origin')
        self.proceeds_asset_swap_spread3m = kwargs.get('proceeds_asset_swap_spread3m')
        self.total_quantity = kwargs.get('total_quantity')
        self.internal_user = kwargs.get('internal_user')
        self.sell40bps = kwargs.get('sell40bps')
        self.redemption_option = kwargs.get('redemption_option')
        self.notional_unit2 = kwargs.get('notional_unit2')
        self.notional_unit1 = kwargs.get('notional_unit1')
        self.sedol = kwargs.get('sedol')
        self.rounding_cost_pnl = kwargs.get('rounding_cost_pnl')
        self.mid_yield = kwargs.get('mid_yield')
        self.unexecuted_notional_local = kwargs.get('unexecuted_notional_local')
        self.sustain_global = kwargs.get('sustain_global')
        self.ending_date = kwargs.get('ending_date')
        self.proceeds_asset_swap_spread12m = kwargs.get('proceeds_asset_swap_spread12m')
        self.gross_investment_wtd = kwargs.get('gross_investment_wtd')
        self.ann_return3_year = kwargs.get('ann_return3_year')
        self.sharpe_wtd = kwargs.get('sharpe_wtd')
        self.discount_factor = kwargs.get('discount_factor')
        self.relative_return_mtd = kwargs.get('relative_return_mtd')
        self.price_change_on_day = kwargs.get('price_change_on_day')
        self.buy100cents = kwargs.get('buy100cents')
        self.forward_point = kwargs.get('forward_point')
        self.fci = kwargs.get('fci')
        self.recall_quantity = kwargs.get('recall_quantity')
        self.fx_positioning = kwargs.get('fx_positioning')
        self.gsid_equivalent = kwargs.get('gsid_equivalent')
        self.categories = kwargs.get('categories')
        self.ext_mkt_asset = kwargs.get('ext_mkt_asset')
        self.quoting_style = kwargs.get('quoting_style')
        self.error_message = kwargs.get('error_message')
        self.mid_price = kwargs.get('mid_price')
        self.proceeds_asset_swap_spread6m = kwargs.get('proceeds_asset_swap_spread6m')
        self.sts_em_dm = kwargs.get('sts_em_dm')
        self.embedded_option = kwargs.get('embedded_option')
        self.tcm_cost_horizon2_day = kwargs.get('tcm_cost_horizon2_day')
        self.age_band = kwargs.get('age_band')
        self.returns_enabled = kwargs.get('returns_enabled')
        self.run_id = kwargs.get('run_id')
        self.queue_in_lots = kwargs.get('queue_in_lots')
        self.tender_offer_expiration_date = kwargs.get('tender_offer_expiration_date')
        self.midcurve_annuity = kwargs.get('midcurve_annuity')
        self.lending_fund_nav_trend = kwargs.get('lending_fund_nav_trend')
        self.cloud_cover_forecast = kwargs.get('cloud_cover_forecast')
        self.tcm_cost_participation_rate5_pct = kwargs.get('tcm_cost_participation_rate5_pct')
        self.default_backcast = kwargs.get('default_backcast')
        self.news_on_intensity = kwargs.get('news_on_intensity')
        self.price_forming_continuation_data = kwargs.get('price_forming_continuation_data')
        self.adjusted_short_interest = kwargs.get('adjusted_short_interest')
        self.new_hospitalized = kwargs.get('new_hospitalized')
        self.asset_parameters_strike = kwargs.get('asset_parameters_strike')
        self.buy35cents = kwargs.get('buy35cents')
        self.leg2_total_notional = kwargs.get('leg2_total_notional')
        self.asset_parameters_effective_date = kwargs.get('asset_parameters_effective_date')
        self.ann_return10_year = kwargs.get('ann_return10_year')
        self.num_adult_icu_beds = kwargs.get('num_adult_icu_beds')
        self.days_to_expiration = kwargs.get('days_to_expiration')
        self.continuation_event = kwargs.get('continuation_event')
        self.wi_id = kwargs.get('wi_id')
        self.market_cap_category = kwargs.get('market_cap_category')
        self.historical_volume = kwargs.get('historical_volume')
        self.buy5cents = kwargs.get('buy5cents')
        self.event_start_date = kwargs.get('event_start_date')
        self.leg1_fixed_rate = kwargs.get('leg1_fixed_rate')
        self.equity_gamma = kwargs.get('equity_gamma')
        self.rpt_id = kwargs.get('rpt_id')
        self.gross_income = kwargs.get('gross_income')
        self.em_id = kwargs.get('em_id')
        self.asset_count_in_model = kwargs.get('asset_count_in_model')
        self.sts_credit_region = kwargs.get('sts_credit_region')
        self.min_temperature = kwargs.get('min_temperature')
        self.fill_type = kwargs.get('fill_type')
        self.fail_pct = kwargs.get('fail_pct')
        self.iso_country_code_alpha2 = kwargs.get('iso_country_code_alpha2')
        self.iso_country_code_alpha3 = kwargs.get('iso_country_code_alpha3')
        self.amount = kwargs.get('amount')
        self.lending_fund_acct = kwargs.get('lending_fund_acct')
        self.rebate = kwargs.get('rebate')
        self.election_type = kwargs.get('election_type')
        self.relative_hit_rate_mtd = kwargs.get('relative_hit_rate_mtd')
        self.implied_volatility = kwargs.get('implied_volatility')
        self.spread = kwargs.get('spread')
        self.variance = kwargs.get('variance')
        self.wtd_degree_days_daily_forecast = kwargs.get('wtd_degree_days_daily_forecast')
        self.swaption_annuity = kwargs.get('swaption_annuity')
        self.buy6bps = kwargs.get('buy6bps')
        self.g10_currency = kwargs.get('g10_currency')
        self.humidity_forecast = kwargs.get('humidity_forecast')
        self.relative_period = kwargs.get('relative_period')
        self.user = kwargs.get('user')
        self.customer = kwargs.get('customer')
        self.leg1_reset_frequency = kwargs.get('leg1_reset_frequency')
        self.queue_clock_time_label = kwargs.get('queue_clock_time_label')
        self.pace_of_rollp100 = kwargs.get('pace_of_rollp100')
        self.asset_classifications_gics_sub_industry = kwargs.get('asset_classifications_gics_sub_industry')
        self.dew_point_hourly_forecast = kwargs.get('dew_point_hourly_forecast')
        self.location_type = kwargs.get('location_type')
        self.facet_divisional_reporting_group_id = kwargs.get('facet_divisional_reporting_group_id')
        self.realized_twap_performance_usd = kwargs.get('realized_twap_performance_usd')
        self.swap_rate = kwargs.get('swap_rate')
        self.algo_execution_style = kwargs.get('algo_execution_style')
        self.client_contact = kwargs.get('client_contact')
        self.min_temperature_hour = kwargs.get('min_temperature_hour')
        self.trading_currency = kwargs.get('trading_currency')
        self.total_by_onset = kwargs.get('total_by_onset')
        self.agency_swap_spread = kwargs.get('agency_swap_spread')
        self.rank = kwargs.get('rank')
        self.mixed_swap_other_reported_sdr = kwargs.get('mixed_swap_other_reported_sdr')
        self.humidity = kwargs.get('humidity')
        self.data_set_category = kwargs.get('data_set_category')
        self.vwap_realized_bps = kwargs.get('vwap_realized_bps')
        self.buy9bps = kwargs.get('buy9bps')
        self.total_tested = kwargs.get('total_tested')
        self.fatalities_confirmed = kwargs.get('fatalities_confirmed')
        self.universe_id1 = kwargs.get('universe_id1')
        self.asset_parameters_payer_day_count_fraction = kwargs.get('asset_parameters_payer_day_count_fraction')
        self.universe_id2 = kwargs.get('universe_id2')
        self.bid_low = kwargs.get('bid_low')
        self.bucketize_price = kwargs.get('bucketize_price')
        self.fair_variance_volatility = kwargs.get('fair_variance_volatility')
        self.covid19 = kwargs.get('covid19')
        self.client_exposure = kwargs.get('client_exposure')
        self.leg2_total_notional_unit = kwargs.get('leg2_total_notional_unit')
        self.sell45cents = kwargs.get('sell45cents')
        self.gs_sustain_sub_sector = kwargs.get('gs_sustain_sub_sector')
        self.sinkable = kwargs.get('sinkable')
        self.is_real = kwargs.get('is_real')
        self.max_temperature_hour = kwargs.get('max_temperature_hour')
        self.leg2_averaging_method = kwargs.get('leg2_averaging_method')
        self.jsn = kwargs.get('jsn')
        self.sell160cents = kwargs.get('sell160cents')
        self.knock_in_direction = kwargs.get('knock_in_direction')
        self.day_close_unrealized_usd = kwargs.get('day_close_unrealized_usd')
        self.tenor = kwargs.get('tenor')
        self.pricing_convention = kwargs.get('pricing_convention')
        self.popularity = kwargs.get('popularity')
        self.floating_rate_option = kwargs.get('floating_rate_option')
        self.hedge_value_type = kwargs.get('hedge_value_type')
        self.asset_parameters_clearing_house = kwargs.get('asset_parameters_clearing_house')
        self.disclaimer = kwargs.get('disclaimer')
        self.payer_frequency = kwargs.get('payer_frequency')
        self.loan_fee = kwargs.get('loan_fee')
        self.deployment_version = kwargs.get('deployment_version')
        self.buy16bps = kwargs.get('buy16bps')
        self.trade_day_count = kwargs.get('trade_day_count')
        self.price_to_sales = kwargs.get('price_to_sales')
        self.new_ideas_qtd = kwargs.get('new_ideas_qtd')
        self.subdivision_name = kwargs.get('subdivision_name')
        self.adjusted_ask_price = kwargs.get('adjusted_ask_price')
        self.factor_universe = kwargs.get('factor_universe')
        self.arrival_rt = kwargs.get('arrival_rt')
        self.internal_index_calc_agent = kwargs.get('internal_index_calc_agent')
        self.excess_margin_value = kwargs.get('excess_margin_value')
        self.transaction_cost = kwargs.get('transaction_cost')
        self.central_bank_swap_rate = kwargs.get('central_bank_swap_rate')
        self.previous_new_confirmed = kwargs.get('previous_new_confirmed')
        self.unrealized_vwap_performance_bps = kwargs.get('unrealized_vwap_performance_bps')
        self.degree_days_daily_forecast = kwargs.get('degree_days_daily_forecast')
        self.position_amount = kwargs.get('position_amount')
        self.heat_index_hourly_forecast = kwargs.get('heat_index_hourly_forecast')
        self.ma_rank = kwargs.get('ma_rank')
        self.fx_positioning_source = kwargs.get('fx_positioning_source')
        self.implied_volatility_by_delta_strike = kwargs.get('implied_volatility_by_delta_strike')
        self.mq_symbol = kwargs.get('mq_symbol')
        self.num_total_units = kwargs.get('num_total_units')
        self.corporate_action = kwargs.get('corporate_action')
        self.leg1_price_type = kwargs.get('leg1_price_type')
        self.asset_parameters_payer_rate_option = kwargs.get('asset_parameters_payer_rate_option')
        self.sell20cents = kwargs.get('sell20cents')
        self.leg2_fixed_payment_currency = kwargs.get('leg2_fixed_payment_currency')
        self.g_regional_score = kwargs.get('g_regional_score')
        self.hard_to_borrow = kwargs.get('hard_to_borrow')
        self.sell5bps = kwargs.get('sell5bps')
        self.roll_vwap = kwargs.get('roll_vwap')
        self.wpk = kwargs.get('wpk')
        self.bespoke_swap = kwargs.get('bespoke_swap')
        self.asset_parameters_expiration_date = kwargs.get('asset_parameters_expiration_date')
        self.country_name = kwargs.get('country_name')
        self.carry = kwargs.get('carry')
        self.starting_date = kwargs.get('starting_date')
        self.loan_id = kwargs.get('loan_id')
        self.onboarded = kwargs.get('onboarded')
        self.liquidity_score = kwargs.get('liquidity_score')
        self.long_rates_contribution = kwargs.get('long_rates_contribution')
        self.source_date_span = kwargs.get('source_date_span')
        self.ann_yield6_month = kwargs.get('ann_yield6_month')
        self.underlying_data_set_id = kwargs.get('underlying_data_set_id')
        self.close_unadjusted = kwargs.get('close_unadjusted')
        self.value_unit = kwargs.get('value_unit')
        self.quantity_unit = kwargs.get('quantity_unit')
        self.adjusted_low_price = kwargs.get('adjusted_low_price')
        self.is_momentum = kwargs.get('is_momentum')
        self.long_conviction_large = kwargs.get('long_conviction_large')
        self.oad = kwargs.get('oad')
        self.rate = kwargs.get('rate')
        self.coupon_type = kwargs.get('coupon_type')
        self.client = kwargs.get('client')
        self.conviction_list = kwargs.get('conviction_list')
        self.passive_etf_ratio = kwargs.get('passive_etf_ratio')
        self.future_month_g26 = kwargs.get('future_month_g26')
        self.future_month_g25 = kwargs.get('future_month_g25')
        self.future_month_g24 = kwargs.get('future_month_g24')
        self.future_month_g23 = kwargs.get('future_month_g23')
        self.type_of_return = kwargs.get('type_of_return')
        self.future_month_g22 = kwargs.get('future_month_g22')
        self.servicing_cost_long_pnl = kwargs.get('servicing_cost_long_pnl')
        self.excess_margin_percentage = kwargs.get('excess_margin_percentage')
        self.future_month_g21 = kwargs.get('future_month_g21')
        self.total_mild = kwargs.get('total_mild')
        self.realized_arrival_performance_bps = kwargs.get('realized_arrival_performance_bps')
        self.precipitation_daily_forecast_inches = kwargs.get('precipitation_daily_forecast_inches')
        self.exchange_id = kwargs.get('exchange_id')
        self.leg2_fixed_payment = kwargs.get('leg2_fixed_payment')
        self.tcm_cost_horizon20_day = kwargs.get('tcm_cost_horizon20_day')
        self.realm = kwargs.get('realm')
        self.bid = kwargs.get('bid')
        self.hedge_value = kwargs.get('hedge_value')
        self.is_aggressive = kwargs.get('is_aggressive')
        self.floating_rate_designated_maturity = kwargs.get('floating_rate_designated_maturity')
        self.percentage_near_executed_quantity = kwargs.get('percentage_near_executed_quantity')
        self.order_id = kwargs.get('order_id')
        self.hospital_type = kwargs.get('hospital_type')
        self.day_close_realized_bps = kwargs.get('day_close_realized_bps')
        self.precipitation_hourly_forecast = kwargs.get('precipitation_hourly_forecast')
        self.market_cap_usd = kwargs.get('market_cap_usd')
        self.auction_fills_percentage = kwargs.get('auction_fills_percentage')
        self.high_price = kwargs.get('high_price')
        self.absolute_shares = kwargs.get('absolute_shares')
        self.fixed_rate_day_count_fraction = kwargs.get('fixed_rate_day_count_fraction')
        self.model = kwargs.get('model')
        self.unrealized_twap_performance_usd = kwargs.get('unrealized_twap_performance_usd')
        self.__id = kwargs.get('id_')
        self.maturity = kwargs.get('maturity')
        self.delta_change = kwargs.get('delta_change')
        self.index = kwargs.get('index')
        self.unrealized_arrival_performance_usd = kwargs.get('unrealized_arrival_performance_usd')
        self.iceberg_slippage = kwargs.get('iceberg_slippage')
        self.sell120cents = kwargs.get('sell120cents')
        self.future_month_x26 = kwargs.get('future_month_x26')
        self.asset_types = kwargs.get('asset_types')
        self.future_month_x25 = kwargs.get('future_month_x25')
        self.bcid = kwargs.get('bcid')
        self.mkt_point = kwargs.get('mkt_point')
        self.future_month_x24 = kwargs.get('future_month_x24')
        self.restriction_start_date = kwargs.get('restriction_start_date')
        self.touch_liquidity_score = kwargs.get('touch_liquidity_score')
        self.future_month_x23 = kwargs.get('future_month_x23')
        self.future_month_x22 = kwargs.get('future_month_x22')
        self.factor_category_id = kwargs.get('factor_category_id')
        self.security_type_id = kwargs.get('security_type_id')
        self.future_month_x21 = kwargs.get('future_month_x21')
        self.investment_ytd = kwargs.get('investment_ytd')
        self.leg2_notional = kwargs.get('leg2_notional')
        self.sell1bps = kwargs.get('sell1bps')
        self.sell200cents = kwargs.get('sell200cents')
        self.expected_completion_date = kwargs.get('expected_completion_date')
        self.spread_option_vol = kwargs.get('spread_option_vol')
        self.sell80cents = kwargs.get('sell80cents')
        self.inflation_swap_rate = kwargs.get('inflation_swap_rate')
        self.active_queries = kwargs.get('active_queries')
        self.sell45bps = kwargs.get('sell45bps')
        self.embeded_option = kwargs.get('embeded_option')
        self.event_source = kwargs.get('event_source')
        self.qis_perm_no = kwargs.get('qis_perm_no')
        self.settlement = kwargs.get('settlement')
        self.shareclass_id = kwargs.get('shareclass_id')
        self.feature2 = kwargs.get('feature2')
        self.feature3 = kwargs.get('feature3')
        self.sts_commodity_sector = kwargs.get('sts_commodity_sector')
        self.exception_status = kwargs.get('exception_status')
        self.overnight_news_intensity = kwargs.get('overnight_news_intensity')
        self.sales_coverage = kwargs.get('sales_coverage')
        self.feature1 = kwargs.get('feature1')
        self.tcm_cost_participation_rate10_pct = kwargs.get('tcm_cost_participation_rate10_pct')
        self.event_time = kwargs.get('event_time')
        self.position_source_name = kwargs.get('position_source_name')
        self.delivery_date = kwargs.get('delivery_date')
        self.interest_rate = kwargs.get('interest_rate')
        self.side = kwargs.get('side')
        self.dynamic_hybrid_aggressive_style = kwargs.get('dynamic_hybrid_aggressive_style')
        self.compliance_restricted_status = kwargs.get('compliance_restricted_status')
        self.borrow_fee = kwargs.get('borrow_fee')
        self.ever_icu = kwargs.get('ever_icu')
        self.no_worse_than_level = kwargs.get('no_worse_than_level')
        self.loan_spread = kwargs.get('loan_spread')
        self.tcm_cost_horizon12_hour = kwargs.get('tcm_cost_horizon12_hour')
        self.dew_point = kwargs.get('dew_point')
        self.research_commission = kwargs.get('research_commission')
        self.buy2bps = kwargs.get('buy2bps')
        self.asset_classifications_risk_country_code = kwargs.get('asset_classifications_risk_country_code')
        self.new_ideas_mtd = kwargs.get('new_ideas_mtd')
        self.var_swap_by_expiry = kwargs.get('var_swap_by_expiry')
        self.sell_date = kwargs.get('sell_date')
        self.aum_start = kwargs.get('aum_start')
        self.asset_parameters_settlement = kwargs.get('asset_parameters_settlement')
        self.max_temperature = kwargs.get('max_temperature')
        self.acquirer_shareholder_meeting_date = kwargs.get('acquirer_shareholder_meeting_date')
        self.count_ideas_wtd = kwargs.get('count_ideas_wtd')
        self.arrival_rt_normalized = kwargs.get('arrival_rt_normalized')
        self.report_type = kwargs.get('report_type')
        self.source_url = kwargs.get('source_url')
        self.estimated_return = kwargs.get('estimated_return')
        self.high = kwargs.get('high')
        self.source_last_update = kwargs.get('source_last_update')
        self.sunshine_forecast = kwargs.get('sunshine_forecast')
        self.quantity_mw = kwargs.get('quantity_mw')
        self.sell70cents = kwargs.get('sell70cents')
        self.sell110cents = kwargs.get('sell110cents')
        self.pnode_id = kwargs.get('pnode_id')
        self.humidity_type = kwargs.get('humidity_type')
        self.prev_close_ask = kwargs.get('prev_close_ask')
        self.level = kwargs.get('level')
        self.implied_volatility_by_expiration = kwargs.get('implied_volatility_by_expiration')
        self.asset_parameters_fixed_rate_day_count_fraction = kwargs.get(
            'asset_parameters_fixed_rate_day_count_fraction')
        self.es_momentum_score = kwargs.get('es_momentum_score')
        self.leg2_index = kwargs.get('leg2_index')
        self.net_weight = kwargs.get('net_weight')
        self.portfolio_managers = kwargs.get('portfolio_managers')
        self.bos_in_ticks = kwargs.get('bos_in_ticks')
        self.asset_parameters_coupon_type = kwargs.get('asset_parameters_coupon_type')
        self.expected_residual_quantity = kwargs.get('expected_residual_quantity')
        self.roll_date = kwargs.get('roll_date')
        self.dynamic_hybrid_speed = kwargs.get('dynamic_hybrid_speed')
        self.cap_floor_vol = kwargs.get('cap_floor_vol')
        self.target_quantity = kwargs.get('target_quantity')
        self.submitter = kwargs.get('submitter')
        self.no = kwargs.get('no')
        self.notional = kwargs.get('notional')
        self.es_disclosure_percentage = kwargs.get('es_disclosure_percentage')
        self.close_executed_quantity_percentage = kwargs.get('close_executed_quantity_percentage')
        self.twap_realized_cash = kwargs.get('twap_realized_cash')
        self.is_open_auction = kwargs.get('is_open_auction')
        self.leg1_type = kwargs.get('leg1_type')
        self.wet_bulb_temp_hourly_forecast = kwargs.get('wet_bulb_temp_hourly_forecast')
        self.cleanup_price = kwargs.get('cleanup_price')
        self.total = kwargs.get('total')
        self.filled_notional_usd = kwargs.get('filled_notional_usd')
        self.asset_id = kwargs.get('asset_id')
        self.test_status = kwargs.get('test_status')
        self.mkt_type = kwargs.get('mkt_type')
        self.yield30_day = kwargs.get('yield30_day')
        self.buy28bps = kwargs.get('buy28bps')
        self.proportion_of_risk = kwargs.get('proportion_of_risk')
        self.future_month_k23 = kwargs.get('future_month_k23')
        self.future_month_k22 = kwargs.get('future_month_k22')
        self.future_month_k21 = kwargs.get('future_month_k21')
        self.primary_entity_id = kwargs.get('primary_entity_id')
        self.cross = kwargs.get('cross')
        self.idea_status = kwargs.get('idea_status')
        self.contract_subtype = kwargs.get('contract_subtype')
        self.sri = kwargs.get('sri')
        self.fx_forecast = kwargs.get('fx_forecast')
        self.fixing_time_label = kwargs.get('fixing_time_label')
        self.is_etf = kwargs.get('is_etf')
        self.fill_id = kwargs.get('fill_id')
        self.excess_returns = kwargs.get('excess_returns')
        self.dollar_return = kwargs.get('dollar_return')
        self.order_in_limit = kwargs.get('order_in_limit')
        self.expiry_time = kwargs.get('expiry_time')
        self.return_on_equity = kwargs.get('return_on_equity')
        self.future_month_k26 = kwargs.get('future_month_k26')
        self.future_month_k25 = kwargs.get('future_month_k25')
        self.future_month_k24 = kwargs.get('future_month_k24')
        self.restriction_end_date = kwargs.get('restriction_end_date')
        self.queue_in_lots_description = kwargs.get('queue_in_lots_description')
        self.volume_limit = kwargs.get('volume_limit')
        self.objective = kwargs.get('objective')
        self.nav_price = kwargs.get('nav_price')
        self.leg1_underlying_asset = kwargs.get('leg1_underlying_asset')
        self.private_placement_type = kwargs.get('private_placement_type')
        self.hedge_notional = kwargs.get('hedge_notional')
        self.ask_low = kwargs.get('ask_low')
        self.intended_p_rate = kwargs.get('intended_p_rate')
        self.expiry = kwargs.get('expiry')
        self.avg_monthly_yield = kwargs.get('avg_monthly_yield')
        self.period_direction = kwargs.get('period_direction')
        self.prev_rpt_id = kwargs.get('prev_rpt_id')
        self.earnings_per_share = kwargs.get('earnings_per_share')
        self.strike_percentage = kwargs.get('strike_percentage')
        self.es_product_impact_percentile = kwargs.get('es_product_impact_percentile')
        self.vwap_realized_cash = kwargs.get('vwap_realized_cash')
        self.par_asset_swap_spread1m = kwargs.get('par_asset_swap_spread1m')
        self.prev_close_bid = kwargs.get('prev_close_bid')
        self.minimum_increment = kwargs.get('minimum_increment')
        self.tcm_cost_horizon16_day = kwargs.get('tcm_cost_horizon16_day')
        self.investment_mtd = kwargs.get('investment_mtd')
        self.settlement_date = kwargs.get('settlement_date')
        self.weighted_average_mid_normalized = kwargs.get('weighted_average_mid_normalized')
        self.sales_per_share = kwargs.get('sales_per_share')
        self.unadjusted_close = kwargs.get('unadjusted_close')
        self.loan_date = kwargs.get('loan_date')
        self.matched_maturity_swap_spread1m = kwargs.get('matched_maturity_swap_spread1m')
        self.collateral_percentage_actual = kwargs.get('collateral_percentage_actual')
        self.vwap_in_limit_unrealized_bps = kwargs.get('vwap_in_limit_unrealized_bps')
        self.metric_value = kwargs.get('metric_value')
        self.auto_exec_state = kwargs.get('auto_exec_state')
        self.total_recovered = kwargs.get('total_recovered')
        self.relative_return_ytd = kwargs.get('relative_return_ytd')
        self.tick_server = kwargs.get('tick_server')
        self.cumulative_volume_in_percentage = kwargs.get('cumulative_volume_in_percentage')
        self.real_time_restriction_status = kwargs.get('real_time_restriction_status')
        self.trade_type = kwargs.get('trade_type')
        self.settlement_type = kwargs.get('settlement_type')
        self.net_change = kwargs.get('net_change')
        self.number_of_underliers = kwargs.get('number_of_underliers')
        self.swap_type = kwargs.get('swap_type')
        self.forecast_type = kwargs.get('forecast_type')
        self.leg1_notional = kwargs.get('leg1_notional')
        self.sell_settle_date = kwargs.get('sell_settle_date')
        self.new_ideas_ytd = kwargs.get('new_ideas_ytd')
        self.management_fee = kwargs.get('management_fee')
        self.par_asset_swap_spread3m = kwargs.get('par_asset_swap_spread3m')
        self.sell36bps = kwargs.get('sell36bps')
        self.matched_maturity_swap_spread3m = kwargs.get('matched_maturity_swap_spread3m')
        self.source_id = kwargs.get('source_id')
        self.country = kwargs.get('country')
        self.vwap = kwargs.get('vwap')
        self.touch_spread_score = kwargs.get('touch_spread_score')
        self.rating_second_highest = kwargs.get('rating_second_highest')
        self.sell24bps = kwargs.get('sell24bps')
        self.frequency = kwargs.get('frequency')
        self.activity_id = kwargs.get('activity_id')
        self.estimated_impact = kwargs.get('estimated_impact')
        self.sell35cents = kwargs.get('sell35cents')
        self.loan_spread_bucket = kwargs.get('loan_spread_bucket')
        self.coronavirus_global_activity_tracker = kwargs.get('coronavirus_global_activity_tracker')
        self.underlyers = kwargs.get('underlyers')
        self.asset_parameters_pricing_location = kwargs.get('asset_parameters_pricing_location')
        self.event_description = kwargs.get('event_description')
        self.iceberg_max_size = kwargs.get('iceberg_max_size')
        self.asset_parameters_coupon = kwargs.get('asset_parameters_coupon')
        self.details = kwargs.get('details')
        self.sector = kwargs.get('sector')
        self.avg_bed_util_rate = kwargs.get('avg_bed_util_rate')
        self.buy20bps = kwargs.get('buy20bps')
        self.epidemic = kwargs.get('epidemic')
        self.mctr = kwargs.get('mctr')
        self.exchange_time = kwargs.get('exchange_time')
        self.historical_close = kwargs.get('historical_close')
        self.fips_code = kwargs.get('fips_code')
        self.buy32bps = kwargs.get('buy32bps')
        self.idea_id = kwargs.get('idea_id')
        self.comment_status = kwargs.get('comment_status')
        self.marginal_cost = kwargs.get('marginal_cost')
        self.client_weight = kwargs.get('client_weight')
        self.leg1_delivery_point = kwargs.get('leg1_delivery_point')
        self.sell5cents = kwargs.get('sell5cents')
        self.liq_wkly = kwargs.get('liq_wkly')
        self.unrealized_twap_performance_bps = kwargs.get('unrealized_twap_performance_bps')
        self.region = kwargs.get('region')
        self.temperature_hour = kwargs.get('temperature_hour')
        self.upper_bound = kwargs.get('upper_bound')
        self.sell55cents = kwargs.get('sell55cents')
        self.num_pedi_icu_beds = kwargs.get('num_pedi_icu_beds')
        self.bid_yield = kwargs.get('bid_yield')
        self.expected_residual = kwargs.get('expected_residual')
        self.option_premium = kwargs.get('option_premium')
        self.owner_name = kwargs.get('owner_name')
        self.par_asset_swap_spread6m = kwargs.get('par_asset_swap_spread6m')
        self.z_score = kwargs.get('z_score')
        self.sell12bps = kwargs.get('sell12bps')
        self.event_start_time = kwargs.get('event_start_time')
        self.matched_maturity_swap_spread6m = kwargs.get('matched_maturity_swap_spread6m')
        self.turnover = kwargs.get('turnover')
        self.price_spot_target_unit = kwargs.get('price_spot_target_unit')
        self.coverage = kwargs.get('coverage')
        self.g_percentile = kwargs.get('g_percentile')
        self.cloud_cover_hourly_forecast = kwargs.get('cloud_cover_hourly_forecast')
        self.lending_fund_nav = kwargs.get('lending_fund_nav')
        self.source_original_category = kwargs.get('source_original_category')
        self.percent_close_execution_quantity = kwargs.get('percent_close_execution_quantity')
        self.latest_execution_time = kwargs.get('latest_execution_time')
        self.arrival_mid_realized_bps = kwargs.get('arrival_mid_realized_bps')
        self.location = kwargs.get('location')
        self.scenario_id = kwargs.get('scenario_id')
        self.termination_tenor = kwargs.get('termination_tenor')
        self.queue_clock_time = kwargs.get('queue_clock_time')
        self.discretion_lower_bound = kwargs.get('discretion_lower_bound')
        self.tcm_cost_participation_rate50_pct = kwargs.get('tcm_cost_participation_rate50_pct')
        self.rating_linear = kwargs.get('rating_linear')
        self.previous_close_unrealized_bps = kwargs.get('previous_close_unrealized_bps')
        self.sub_asset_class_for_other_commodity = kwargs.get('sub_asset_class_for_other_commodity')
        self.forward_price = kwargs.get('forward_price')
        self.__type = kwargs.get('type_')
        self.strike_ref = kwargs.get('strike_ref')
        self.cumulative_pnl = kwargs.get('cumulative_pnl')
        self.short_tenor = kwargs.get('short_tenor')
        self.sell28bps = kwargs.get('sell28bps')
        self.fund_class = kwargs.get('fund_class')
        self.unadjusted_volume = kwargs.get('unadjusted_volume')
        self.buy36bps = kwargs.get('buy36bps')
        self.position_idx = kwargs.get('position_idx')
        self.wind_chill_hourly_forecast = kwargs.get('wind_chill_hourly_forecast')
        self.sec_name = kwargs.get('sec_name')
        self.implied_volatility_by_relative_strike = kwargs.get('implied_volatility_by_relative_strike')
        self.percent_adv = kwargs.get('percent_adv')
        self.leg1_total_notional = kwargs.get('leg1_total_notional')
        self.contract = kwargs.get('contract')
        self.payment_frequency1 = kwargs.get('payment_frequency1')
        self.payment_frequency2 = kwargs.get('payment_frequency2')
        self.bespoke = kwargs.get('bespoke')
        self.repo_tenor = kwargs.get('repo_tenor')
        self.sell15cents = kwargs.get('sell15cents')
        self.investment_qtd = kwargs.get('investment_qtd')
        self.heat_index_forecast = kwargs.get('heat_index_forecast')
        self.rating_standard_and_poors = kwargs.get('rating_standard_and_poors')
        self.quality_stars = kwargs.get('quality_stars')
        self.leg2_floating_index = kwargs.get('leg2_floating_index')
        self.source_ticker = kwargs.get('source_ticker')
        self.primary_vwap_unrealized_bps = kwargs.get('primary_vwap_unrealized_bps')
        self.gsid = kwargs.get('gsid')
        self.lending_fund = kwargs.get('lending_fund')
        self.sensitivity = kwargs.get('sensitivity')
        self.day_count = kwargs.get('day_count')
        self.sell16bps = kwargs.get('sell16bps')
        self.relative_break_even_inflation_change = kwargs.get('relative_break_even_inflation_change')
        self.sell25cents = kwargs.get('sell25cents')
        self.var_swap = kwargs.get('var_swap')
        self.buy5point5bps = kwargs.get('buy5point5bps')
        self.block_large_notional = kwargs.get('block_large_notional')
        self.sell2point5bps = kwargs.get('sell2point5bps')
        self.capacity = kwargs.get('capacity')
        self.sectors_raw = kwargs.get('sectors_raw')
        self.primary_vwap_in_limit = kwargs.get('primary_vwap_in_limit')
        self.shareclass_price = kwargs.get('shareclass_price')
        self.trade_size = kwargs.get('trade_size')
        self.price_spot_entry_value = kwargs.get('price_spot_entry_value')
        self.buy8point5bps = kwargs.get('buy8point5bps')
        self.symbol_dimensions = kwargs.get('symbol_dimensions')
        self.buy24bps = kwargs.get('buy24bps')
        self.observation = kwargs.get('observation')
        self.option_type_sdr = kwargs.get('option_type_sdr')
        self.scenario_group_id = kwargs.get('scenario_group_id')
        self.average_implied_variance = kwargs.get('average_implied_variance')
        self.avg_trade_rate_description = kwargs.get('avg_trade_rate_description')
        self.fraction = kwargs.get('fraction')
        self.asset_count_short = kwargs.get('asset_count_short')
        self.collateral_percentage_required = kwargs.get('collateral_percentage_required')
        self.sell5point5bps = kwargs.get('sell5point5bps')
        self.date = kwargs.get('date')
        self.zip_code = kwargs.get('zip_code')
        self.total_std_return_since_inception = kwargs.get('total_std_return_since_inception')
        self.source_category = kwargs.get('source_category')
        self.volume_unadjusted = kwargs.get('volume_unadjusted')
        self.passive_ratio = kwargs.get('passive_ratio')
        self.price_to_earnings = kwargs.get('price_to_earnings')
        self.order_depth = kwargs.get('order_depth')
        self.ann_yield3_month = kwargs.get('ann_yield3_month')
        self.net_flow_std = kwargs.get('net_flow_std')
        self.encoded_stats = kwargs.get('encoded_stats')
        self.buy5bps = kwargs.get('buy5bps')
        self.run_time = kwargs.get('run_time')
        self.ask_size = kwargs.get('ask_size')
        self.absolute_return_mtd = kwargs.get('absolute_return_mtd')
        self.std30_days_unsubsidized_yield = kwargs.get('std30_days_unsubsidized_yield')
        self.resource = kwargs.get('resource')
        self.average_realized_volatility = kwargs.get('average_realized_volatility')
        self.trace_adv_buy = kwargs.get('trace_adv_buy')
        self.new_confirmed = kwargs.get('new_confirmed')
        self.sell8bps = kwargs.get('sell8bps')
        self.bid_price = kwargs.get('bid_price')
        self.sell8point5bps = kwargs.get('sell8point5bps')
        self.target_price_unrealized_bps = kwargs.get('target_price_unrealized_bps')
        self.es_numeric_percentile = kwargs.get('es_numeric_percentile')
        self.leg2_underlying_asset = kwargs.get('leg2_underlying_asset')
        self.csa_terms = kwargs.get('csa_terms')
        self.relative_payoff_mtd = kwargs.get('relative_payoff_mtd')
        self.daily_net_shareholder_flows = kwargs.get('daily_net_shareholder_flows')
        self.buy2point5bps = kwargs.get('buy2point5bps')
        self.cai = kwargs.get('cai')
        self.executed_notional_usd = kwargs.get('executed_notional_usd')
        self.total_home_isolation = kwargs.get('total_home_isolation')
        self.station_name = kwargs.get('station_name')
        self.pass_pct = kwargs.get('pass_pct')
        self.opening_report = kwargs.get('opening_report')
        self.midcurve_atm_fwd_rate = kwargs.get('midcurve_atm_fwd_rate')
        self.precipitation_forecast = kwargs.get('precipitation_forecast')
        self.equity_risk_premium_index = kwargs.get('equity_risk_premium_index')
        self.fatalities_underlying_conditions_unknown = kwargs.get('fatalities_underlying_conditions_unknown')
        self.buy12bps = kwargs.get('buy12bps')
        self.clearing_house = kwargs.get('clearing_house')
        self.day_close_unrealized_bps = kwargs.get('day_close_unrealized_bps')
        self.sts_rates_maturity = kwargs.get('sts_rates_maturity')
        self.liq_dly = kwargs.get('liq_dly')
        self.contributor_role = kwargs.get('contributor_role')
        self.total_fatalities = kwargs.get('total_fatalities')

    @property
    def investment_rate(self) -> dict:
        return self.__investment_rate

    @investment_rate.setter
    def investment_rate(self, value: dict):
        self._property_changed('investment_rate')
        self.__investment_rate = value        

    @property
    def starting_emma_legal_entity_id(self) -> dict:
        return self.__starting_emma_legal_entity_id

    @starting_emma_legal_entity_id.setter
    def starting_emma_legal_entity_id(self, value: dict):
        self._property_changed('starting_emma_legal_entity_id')
        self.__starting_emma_legal_entity_id = value        

    @property
    def mdapi_class(self) -> dict:
        return self.__mdapi_class

    @mdapi_class.setter
    def mdapi_class(self, value: dict):
        self._property_changed('mdapi_class')
        self.__mdapi_class = value        

    @property
    def total_notional_usd(self) -> dict:
        return self.__total_notional_usd

    @total_notional_usd.setter
    def total_notional_usd(self, value: dict):
        self._property_changed('total_notional_usd')
        self.__total_notional_usd = value        

    @property
    def bid_unadjusted(self) -> dict:
        return self.__bid_unadjusted

    @bid_unadjusted.setter
    def bid_unadjusted(self, value: dict):
        self._property_changed('bid_unadjusted')
        self.__bid_unadjusted = value        

    @property
    def aggressive_fills_percentage(self) -> dict:
        return self.__aggressive_fills_percentage

    @aggressive_fills_percentage.setter
    def aggressive_fills_percentage(self, value: dict):
        self._property_changed('aggressive_fills_percentage')
        self.__aggressive_fills_percentage = value        

    @property
    def vehicle_type(self) -> dict:
        return self.__vehicle_type

    @vehicle_type.setter
    def vehicle_type(self, value: dict):
        self._property_changed('vehicle_type')
        self.__vehicle_type = value        

    @property
    def total_fatalities_by_state(self) -> dict:
        return self.__total_fatalities_by_state

    @total_fatalities_by_state.setter
    def total_fatalities_by_state(self, value: dict):
        self._property_changed('total_fatalities_by_state')
        self.__total_fatalities_by_state = value        

    @property
    def new_active(self) -> dict:
        return self.__new_active

    @new_active.setter
    def new_active(self, value: dict):
        self._property_changed('new_active')
        self.__new_active = value        

    @property
    def daily_risk(self) -> dict:
        return self.__daily_risk

    @daily_risk.setter
    def daily_risk(self, value: dict):
        self._property_changed('daily_risk')
        self.__daily_risk = value        

    @property
    def energy(self) -> dict:
        return self.__energy

    @energy.setter
    def energy(self, value: dict):
        self._property_changed('energy')
        self.__energy = value        

    @property
    def sunshine_daily_forecast(self) -> dict:
        return self.__sunshine_daily_forecast

    @sunshine_daily_forecast.setter
    def sunshine_daily_forecast(self, value: dict):
        self._property_changed('sunshine_daily_forecast')
        self.__sunshine_daily_forecast = value        

    @property
    def sentiment_score(self) -> dict:
        return self.__sentiment_score

    @sentiment_score.setter
    def sentiment_score(self, value: dict):
        self._property_changed('sentiment_score')
        self.__sentiment_score = value        

    @property
    def correlation(self) -> dict:
        return self.__correlation

    @correlation.setter
    def correlation(self, value: dict):
        self._property_changed('correlation')
        self.__correlation = value        

    @property
    def exposure(self) -> dict:
        return self.__exposure

    @exposure.setter
    def exposure(self, value: dict):
        self._property_changed('exposure')
        self.__exposure = value        

    @property
    def size(self) -> dict:
        return self.__size

    @size.setter
    def size(self, value: dict):
        self._property_changed('size')
        self.__size = value        

    @property
    def market_data_asset(self) -> dict:
        return self.__market_data_asset

    @market_data_asset.setter
    def market_data_asset(self, value: dict):
        self._property_changed('market_data_asset')
        self.__market_data_asset = value        

    @property
    def buy75cents(self) -> dict:
        return self.__buy75cents

    @buy75cents.setter
    def buy75cents(self, value: dict):
        self._property_changed('buy75cents')
        self.__buy75cents = value        

    @property
    def unadjusted_high(self) -> dict:
        return self.__unadjusted_high

    @unadjusted_high.setter
    def unadjusted_high(self, value: dict):
        self._property_changed('unadjusted_high')
        self.__unadjusted_high = value        

    @property
    def source_importance(self) -> dict:
        return self.__source_importance

    @source_importance.setter
    def source_importance(self, value: dict):
        self._property_changed('source_importance')
        self.__source_importance = value        

    @property
    def closing_yield(self) -> dict:
        return self.__closing_yield

    @closing_yield.setter
    def closing_yield(self, value: dict):
        self._property_changed('closing_yield')
        self.__closing_yield = value        

    @property
    def wind(self) -> dict:
        return self.__wind

    @wind.setter
    def wind(self, value: dict):
        self._property_changed('wind')
        self.__wind = value        

    @property
    def sc16(self) -> dict:
        return self.__sc16

    @sc16.setter
    def sc16(self, value: dict):
        self._property_changed('sc16')
        self.__sc16 = value        

    @property
    def sc15(self) -> dict:
        return self.__sc15

    @sc15.setter
    def sc15(self, value: dict):
        self._property_changed('sc15')
        self.__sc15 = value        

    @property
    def sc12(self) -> dict:
        return self.__sc12

    @sc12.setter
    def sc12(self, value: dict):
        self._property_changed('sc12')
        self.__sc12 = value        

    @property
    def sc11(self) -> dict:
        return self.__sc11

    @sc11.setter
    def sc11(self, value: dict):
        self._property_changed('sc11')
        self.__sc11 = value        

    @property
    def primary_vwap_in_limit_unrealized_bps(self) -> dict:
        return self.__primary_vwap_in_limit_unrealized_bps

    @primary_vwap_in_limit_unrealized_bps.setter
    def primary_vwap_in_limit_unrealized_bps(self, value: dict):
        self._property_changed('primary_vwap_in_limit_unrealized_bps')
        self.__primary_vwap_in_limit_unrealized_bps = value        

    @property
    def display_name(self) -> dict:
        return self.__display_name

    @display_name.setter
    def display_name(self, value: dict):
        self._property_changed('display_name')
        self.__display_name = value        

    @property
    def minutes_to_trade100_pct(self) -> dict:
        return self.__minutes_to_trade100_pct

    @minutes_to_trade100_pct.setter
    def minutes_to_trade100_pct(self, value: dict):
        self._property_changed('minutes_to_trade100_pct')
        self.__minutes_to_trade100_pct = value        

    @property
    def sc14(self) -> dict:
        return self.__sc14

    @sc14.setter
    def sc14(self, value: dict):
        self._property_changed('sc14')
        self.__sc14 = value        

    @property
    def cumulative_volume_in_shares(self) -> dict:
        return self.__cumulative_volume_in_shares

    @cumulative_volume_in_shares.setter
    def cumulative_volume_in_shares(self, value: dict):
        self._property_changed('cumulative_volume_in_shares')
        self.__cumulative_volume_in_shares = value        

    @property
    def sc13(self) -> dict:
        return self.__sc13

    @sc13.setter
    def sc13(self, value: dict):
        self._property_changed('sc13')
        self.__sc13 = value        

    @property
    def new_fatalities(self) -> dict:
        return self.__new_fatalities

    @new_fatalities.setter
    def new_fatalities(self, value: dict):
        self._property_changed('new_fatalities')
        self.__new_fatalities = value        

    @property
    def buy50bps(self) -> dict:
        return self.__buy50bps

    @buy50bps.setter
    def buy50bps(self, value: dict):
        self._property_changed('buy50bps')
        self.__buy50bps = value        

    @property
    def num_staffed_beds(self) -> dict:
        return self.__num_staffed_beds

    @num_staffed_beds.setter
    def num_staffed_beds(self, value: dict):
        self._property_changed('num_staffed_beds')
        self.__num_staffed_beds = value        

    @property
    def upfront_payment(self) -> dict:
        return self.__upfront_payment

    @upfront_payment.setter
    def upfront_payment(self, value: dict):
        self._property_changed('upfront_payment')
        self.__upfront_payment = value        

    @property
    def arrival_mid_realized_cash(self) -> dict:
        return self.__arrival_mid_realized_cash

    @arrival_mid_realized_cash.setter
    def arrival_mid_realized_cash(self, value: dict):
        self._property_changed('arrival_mid_realized_cash')
        self.__arrival_mid_realized_cash = value        

    @property
    def sc10(self) -> dict:
        return self.__sc10

    @sc10.setter
    def sc10(self, value: dict):
        self._property_changed('sc10')
        self.__sc10 = value        

    @property
    def sc05(self) -> dict:
        return self.__sc05

    @sc05.setter
    def sc05(self, value: dict):
        self._property_changed('sc05')
        self.__sc05 = value        

    @property
    def a(self) -> dict:
        return self.__a

    @a.setter
    def a(self, value: dict):
        self._property_changed('a')
        self.__a = value        

    @property
    def sc04(self) -> dict:
        return self.__sc04

    @sc04.setter
    def sc04(self, value: dict):
        self._property_changed('sc04')
        self.__sc04 = value        

    @property
    def b(self) -> dict:
        return self.__b

    @b.setter
    def b(self, value: dict):
        self._property_changed('b')
        self.__b = value        

    @property
    def sc07(self) -> dict:
        return self.__sc07

    @sc07.setter
    def sc07(self, value: dict):
        self._property_changed('sc07')
        self.__sc07 = value        

    @property
    def c(self) -> dict:
        return self.__c

    @c.setter
    def c(self, value: dict):
        self._property_changed('c')
        self.__c = value        

    @property
    def yield_to_maturity(self) -> dict:
        return self.__yield_to_maturity

    @yield_to_maturity.setter
    def yield_to_maturity(self, value: dict):
        self._property_changed('yield_to_maturity')
        self.__yield_to_maturity = value        

    @property
    def sc06(self) -> dict:
        return self.__sc06

    @sc06.setter
    def sc06(self, value: dict):
        self._property_changed('sc06')
        self.__sc06 = value        

    @property
    def address(self) -> dict:
        return self.__address

    @address.setter
    def address(self, value: dict):
        self._property_changed('address')
        self.__address = value        

    @property
    def sc01(self) -> dict:
        return self.__sc01

    @sc01.setter
    def sc01(self, value: dict):
        self._property_changed('sc01')
        self.__sc01 = value        

    @property
    def leg2_payment_frequency(self) -> dict:
        return self.__leg2_payment_frequency

    @leg2_payment_frequency.setter
    def leg2_payment_frequency(self, value: dict):
        self._property_changed('leg2_payment_frequency')
        self.__leg2_payment_frequency = value        

    @property
    def sc03(self) -> dict:
        return self.__sc03

    @sc03.setter
    def sc03(self, value: dict):
        self._property_changed('sc03')
        self.__sc03 = value        

    @property
    def sc02(self) -> dict:
        return self.__sc02

    @sc02.setter
    def sc02(self, value: dict):
        self._property_changed('sc02')
        self.__sc02 = value        

    @property
    def geography_name(self) -> dict:
        return self.__geography_name

    @geography_name.setter
    def geography_name(self, value: dict):
        self._property_changed('geography_name')
        self.__geography_name = value        

    @property
    def borrower(self) -> dict:
        return self.__borrower

    @borrower.setter
    def borrower(self, value: dict):
        self._property_changed('borrower')
        self.__borrower = value        

    @property
    def settle_price(self) -> dict:
        return self.__settle_price

    @settle_price.setter
    def settle_price(self, value: dict):
        self._property_changed('settle_price')
        self.__settle_price = value        

    @property
    def performance_contribution(self) -> dict:
        return self.__performance_contribution

    @performance_contribution.setter
    def performance_contribution(self, value: dict):
        self._property_changed('performance_contribution')
        self.__performance_contribution = value        

    @property
    def sc09(self) -> dict:
        return self.__sc09

    @sc09.setter
    def sc09(self, value: dict):
        self._property_changed('sc09')
        self.__sc09 = value        

    @property
    def mkt_class(self) -> dict:
        return self.__mkt_class

    @mkt_class.setter
    def mkt_class(self, value: dict):
        self._property_changed('mkt_class')
        self.__mkt_class = value        

    @property
    def sc08(self) -> dict:
        return self.__sc08

    @sc08.setter
    def sc08(self, value: dict):
        self._property_changed('sc08')
        self.__sc08 = value        

    @property
    def collateralization(self) -> dict:
        return self.__collateralization

    @collateralization.setter
    def collateralization(self, value: dict):
        self._property_changed('collateralization')
        self.__collateralization = value        

    @property
    def future_month_u26(self) -> dict:
        return self.__future_month_u26

    @future_month_u26.setter
    def future_month_u26(self, value: dict):
        self._property_changed('future_month_u26')
        self.__future_month_u26 = value        

    @property
    def future_month_u25(self) -> dict:
        return self.__future_month_u25

    @future_month_u25.setter
    def future_month_u25(self, value: dict):
        self._property_changed('future_month_u25')
        self.__future_month_u25 = value        

    @property
    def future_month_u24(self) -> dict:
        return self.__future_month_u24

    @future_month_u24.setter
    def future_month_u24(self, value: dict):
        self._property_changed('future_month_u24')
        self.__future_month_u24 = value        

    @property
    def future_month_u23(self) -> dict:
        return self.__future_month_u23

    @future_month_u23.setter
    def future_month_u23(self, value: dict):
        self._property_changed('future_month_u23')
        self.__future_month_u23 = value        

    @property
    def future_month_u22(self) -> dict:
        return self.__future_month_u22

    @future_month_u22.setter
    def future_month_u22(self, value: dict):
        self._property_changed('future_month_u22')
        self.__future_month_u22 = value        

    @property
    def statement_id(self) -> dict:
        return self.__statement_id

    @statement_id.setter
    def statement_id(self, value: dict):
        self._property_changed('statement_id')
        self.__statement_id = value        

    @property
    def future_month_u21(self) -> dict:
        return self.__future_month_u21

    @future_month_u21.setter
    def future_month_u21(self, value: dict):
        self._property_changed('future_month_u21')
        self.__future_month_u21 = value        

    @property
    def modified_duration(self) -> dict:
        return self.__modified_duration

    @modified_duration.setter
    def modified_duration(self, value: dict):
        self._property_changed('modified_duration')
        self.__modified_duration = value        

    @property
    def short_rates_contribution(self) -> dict:
        return self.__short_rates_contribution

    @short_rates_contribution.setter
    def short_rates_contribution(self, value: dict):
        self._property_changed('short_rates_contribution')
        self.__short_rates_contribution = value        

    @property
    def implied_normal_volatility(self) -> dict:
        return self.__implied_normal_volatility

    @implied_normal_volatility.setter
    def implied_normal_volatility(self, value: dict):
        self._property_changed('implied_normal_volatility')
        self.__implied_normal_volatility = value        

    @property
    def solar_generation(self) -> dict:
        return self.__solar_generation

    @solar_generation.setter
    def solar_generation(self, value: dict):
        self._property_changed('solar_generation')
        self.__solar_generation = value        

    @property
    def mtm_price(self) -> dict:
        return self.__mtm_price

    @mtm_price.setter
    def mtm_price(self, value: dict):
        self._property_changed('mtm_price')
        self.__mtm_price = value        

    @property
    def swap_spread_change(self) -> dict:
        return self.__swap_spread_change

    @swap_spread_change.setter
    def swap_spread_change(self, value: dict):
        self._property_changed('swap_spread_change')
        self.__swap_spread_change = value        

    @property
    def realized_arrival_performance_usd(self) -> dict:
        return self.__realized_arrival_performance_usd

    @realized_arrival_performance_usd.setter
    def realized_arrival_performance_usd(self, value: dict):
        self._property_changed('realized_arrival_performance_usd')
        self.__realized_arrival_performance_usd = value        

    @property
    def portfolio_assets(self) -> dict:
        return self.__portfolio_assets

    @portfolio_assets.setter
    def portfolio_assets(self, value: dict):
        self._property_changed('portfolio_assets')
        self.__portfolio_assets = value        

    @property
    def pricingdate(self) -> dict:
        return self.__pricingdate

    @pricingdate.setter
    def pricingdate(self, value: dict):
        self._property_changed('pricingdate')
        self.__pricingdate = value        

    @property
    def tcm_cost_horizon3_hour(self) -> dict:
        return self.__tcm_cost_horizon3_hour

    @tcm_cost_horizon3_hour.setter
    def tcm_cost_horizon3_hour(self, value: dict):
        self._property_changed('tcm_cost_horizon3_hour')
        self.__tcm_cost_horizon3_hour = value        

    @property
    def exchange_rate(self) -> dict:
        return self.__exchange_rate

    @exchange_rate.setter
    def exchange_rate(self, value: dict):
        self._property_changed('exchange_rate')
        self.__exchange_rate = value        

    @property
    def potential_bed_cap_inc(self) -> dict:
        return self.__potential_bed_cap_inc

    @potential_bed_cap_inc.setter
    def potential_bed_cap_inc(self, value: dict):
        self._property_changed('potential_bed_cap_inc')
        self.__potential_bed_cap_inc = value        

    @property
    def number_covered(self) -> dict:
        return self.__number_covered

    @number_covered.setter
    def number_covered(self, value: dict):
        self._property_changed('number_covered')
        self.__number_covered = value        

    @property
    def number_of_positions(self) -> dict:
        return self.__number_of_positions

    @number_of_positions.setter
    def number_of_positions(self, value: dict):
        self._property_changed('number_of_positions')
        self.__number_of_positions = value        

    @property
    def open_unadjusted(self) -> dict:
        return self.__open_unadjusted

    @open_unadjusted.setter
    def open_unadjusted(self, value: dict):
        self._property_changed('open_unadjusted')
        self.__open_unadjusted = value        

    @property
    def strike_time(self) -> dict:
        return self.__strike_time

    @strike_time.setter
    def strike_time(self, value: dict):
        self._property_changed('strike_time')
        self.__strike_time = value        

    @property
    def ask_price(self) -> dict:
        return self.__ask_price

    @ask_price.setter
    def ask_price(self, value: dict):
        self._property_changed('ask_price')
        self.__ask_price = value        

    @property
    def event_id(self) -> dict:
        return self.__event_id

    @event_id.setter
    def event_id(self, value: dict):
        self._property_changed('event_id')
        self.__event_id = value        

    @property
    def sectors(self) -> dict:
        return self.__sectors

    @sectors.setter
    def sectors(self, value: dict):
        self._property_changed('sectors')
        self.__sectors = value        

    @property
    def additional_price_notation_type(self) -> dict:
        return self.__additional_price_notation_type

    @additional_price_notation_type.setter
    def additional_price_notation_type(self, value: dict):
        self._property_changed('additional_price_notation_type')
        self.__additional_price_notation_type = value        

    @property
    def gross_investment_qtd(self) -> dict:
        return self.__gross_investment_qtd

    @gross_investment_qtd.setter
    def gross_investment_qtd(self, value: dict):
        self._property_changed('gross_investment_qtd')
        self.__gross_investment_qtd = value        

    @property
    def annualized_risk(self) -> dict:
        return self.__annualized_risk

    @annualized_risk.setter
    def annualized_risk(self, value: dict):
        self._property_changed('annualized_risk')
        self.__annualized_risk = value        

    @property
    def estimated_holding_time_short(self) -> dict:
        return self.__estimated_holding_time_short

    @estimated_holding_time_short.setter
    def estimated_holding_time_short(self, value: dict):
        self._property_changed('estimated_holding_time_short')
        self.__estimated_holding_time_short = value        

    @property
    def midcurve_premium(self) -> dict:
        return self.__midcurve_premium

    @midcurve_premium.setter
    def midcurve_premium(self, value: dict):
        self._property_changed('midcurve_premium')
        self.__midcurve_premium = value        

    @property
    def volume_composite(self) -> dict:
        return self.__volume_composite

    @volume_composite.setter
    def volume_composite(self, value: dict):
        self._property_changed('volume_composite')
        self.__volume_composite = value        

    @property
    def sharpe_qtd(self) -> dict:
        return self.__sharpe_qtd

    @sharpe_qtd.setter
    def sharpe_qtd(self, value: dict):
        self._property_changed('sharpe_qtd')
        self.__sharpe_qtd = value        

    @property
    def estimated_holding_time_long(self) -> dict:
        return self.__estimated_holding_time_long

    @estimated_holding_time_long.setter
    def estimated_holding_time_long(self, value: dict):
        self._property_changed('estimated_holding_time_long')
        self.__estimated_holding_time_long = value        

    @property
    def external(self) -> dict:
        return self.__external

    @external.setter
    def external(self, value: dict):
        self._property_changed('external')
        self.__external = value        

    @property
    def tracker_name(self) -> dict:
        return self.__tracker_name

    @tracker_name.setter
    def tracker_name(self, value: dict):
        self._property_changed('tracker_name')
        self.__tracker_name = value        

    @property
    def sell50cents(self) -> dict:
        return self.__sell50cents

    @sell50cents.setter
    def sell50cents(self, value: dict):
        self._property_changed('sell50cents')
        self.__sell50cents = value        

    @property
    def trade_price(self) -> dict:
        return self.__trade_price

    @trade_price.setter
    def trade_price(self, value: dict):
        self._property_changed('trade_price')
        self.__trade_price = value        

    @property
    def cleared(self) -> dict:
        return self.__cleared

    @cleared.setter
    def cleared(self, value: dict):
        self._property_changed('cleared')
        self.__cleared = value        

    @property
    def prime_id_numeric(self) -> dict:
        return self.__prime_id_numeric

    @prime_id_numeric.setter
    def prime_id_numeric(self, value: dict):
        self._property_changed('prime_id_numeric')
        self.__prime_id_numeric = value        

    @property
    def buy8bps(self) -> dict:
        return self.__buy8bps

    @buy8bps.setter
    def buy8bps(self, value: dict):
        self._property_changed('buy8bps')
        self.__buy8bps = value        

    @property
    def total_notional_local(self) -> dict:
        return self.__total_notional_local

    @total_notional_local.setter
    def total_notional_local(self, value: dict):
        self._property_changed('total_notional_local')
        self.__total_notional_local = value        

    @property
    def cid(self) -> dict:
        return self.__cid

    @cid.setter
    def cid(self, value: dict):
        self._property_changed('cid')
        self.__cid = value        

    @property
    def total_confirmed_senior_home(self) -> dict:
        return self.__total_confirmed_senior_home

    @total_confirmed_senior_home.setter
    def total_confirmed_senior_home(self, value: dict):
        self._property_changed('total_confirmed_senior_home')
        self.__total_confirmed_senior_home = value        

    @property
    def ctd_fwd_price(self) -> dict:
        return self.__ctd_fwd_price

    @ctd_fwd_price.setter
    def ctd_fwd_price(self, value: dict):
        self._property_changed('ctd_fwd_price')
        self.__ctd_fwd_price = value        

    @property
    def sink_factor(self) -> dict:
        return self.__sink_factor

    @sink_factor.setter
    def sink_factor(self, value: dict):
        self._property_changed('sink_factor')
        self.__sink_factor = value        

    @property
    def temperature_forecast(self) -> dict:
        return self.__temperature_forecast

    @temperature_forecast.setter
    def temperature_forecast(self, value: dict):
        self._property_changed('temperature_forecast')
        self.__temperature_forecast = value        

    @property
    def bid_high(self) -> dict:
        return self.__bid_high

    @bid_high.setter
    def bid_high(self, value: dict):
        self._property_changed('bid_high')
        self.__bid_high = value        

    @property
    def pnl_qtd(self) -> dict:
        return self.__pnl_qtd

    @pnl_qtd.setter
    def pnl_qtd(self, value: dict):
        self._property_changed('pnl_qtd')
        self.__pnl_qtd = value        

    @property
    def buy50cents(self) -> dict:
        return self.__buy50cents

    @buy50cents.setter
    def buy50cents(self, value: dict):
        self._property_changed('buy50cents')
        self.__buy50cents = value        

    @property
    def sell4bps(self) -> dict:
        return self.__sell4bps

    @sell4bps.setter
    def sell4bps(self, value: dict):
        self._property_changed('sell4bps')
        self.__sell4bps = value        

    @property
    def receiver_day_count_fraction(self) -> dict:
        return self.__receiver_day_count_fraction

    @receiver_day_count_fraction.setter
    def receiver_day_count_fraction(self, value: dict):
        self._property_changed('receiver_day_count_fraction')
        self.__receiver_day_count_fraction = value        

    @property
    def auction_close_percentage(self) -> dict:
        return self.__auction_close_percentage

    @auction_close_percentage.setter
    def auction_close_percentage(self, value: dict):
        self._property_changed('auction_close_percentage')
        self.__auction_close_percentage = value        

    @property
    def target_price(self) -> dict:
        return self.__target_price

    @target_price.setter
    def target_price(self, value: dict):
        self._property_changed('target_price')
        self.__target_price = value        

    @property
    def bos_in_bps_description(self) -> dict:
        return self.__bos_in_bps_description

    @bos_in_bps_description.setter
    def bos_in_bps_description(self, value: dict):
        self._property_changed('bos_in_bps_description')
        self.__bos_in_bps_description = value        

    @property
    def low_price(self) -> dict:
        return self.__low_price

    @low_price.setter
    def low_price(self, value: dict):
        self._property_changed('low_price')
        self.__low_price = value        

    @property
    def adv22_day_pct(self) -> dict:
        return self.__adv22_day_pct

    @adv22_day_pct.setter
    def adv22_day_pct(self, value: dict):
        self._property_changed('adv22_day_pct')
        self.__adv22_day_pct = value        

    @property
    def matched_maturity_swap_spread12m(self) -> dict:
        return self.__matched_maturity_swap_spread12m

    @matched_maturity_swap_spread12m.setter
    def matched_maturity_swap_spread12m(self, value: dict):
        self._property_changed('matched_maturity_swap_spread12m')
        self.__matched_maturity_swap_spread12m = value        

    @property
    def price_range_in_ticks_label(self) -> tuple:
        return self.__price_range_in_ticks_label

    @price_range_in_ticks_label.setter
    def price_range_in_ticks_label(self, value: tuple):
        self._property_changed('price_range_in_ticks_label')
        self.__price_range_in_ticks_label = value        

    @property
    def ticker(self) -> dict:
        return self.__ticker

    @ticker.setter
    def ticker(self, value: dict):
        self._property_changed('ticker')
        self.__ticker = value        

    @property
    def notional_unit(self) -> dict:
        return self.__notional_unit

    @notional_unit.setter
    def notional_unit(self, value: dict):
        self._property_changed('notional_unit')
        self.__notional_unit = value        

    @property
    def tcm_cost_horizon1_day(self) -> dict:
        return self.__tcm_cost_horizon1_day

    @tcm_cost_horizon1_day.setter
    def tcm_cost_horizon1_day(self, value: dict):
        self._property_changed('tcm_cost_horizon1_day')
        self.__tcm_cost_horizon1_day = value        

    @property
    def approval(self) -> dict:
        return self.__approval

    @approval.setter
    def approval(self, value: dict):
        self._property_changed('approval')
        self.__approval = value        

    @property
    def test_measure(self) -> dict:
        return self.__test_measure

    @test_measure.setter
    def test_measure(self, value: dict):
        self._property_changed('test_measure')
        self.__test_measure = value        

    @property
    def option_lock_out_period(self) -> dict:
        return self.__option_lock_out_period

    @option_lock_out_period.setter
    def option_lock_out_period(self, value: dict):
        self._property_changed('option_lock_out_period')
        self.__option_lock_out_period = value        

    @property
    def source_value_forecast(self) -> dict:
        return self.__source_value_forecast

    @source_value_forecast.setter
    def source_value_forecast(self, value: dict):
        self._property_changed('source_value_forecast')
        self.__source_value_forecast = value        

    @property
    def leg2_spread(self) -> dict:
        return self.__leg2_spread

    @leg2_spread.setter
    def leg2_spread(self, value: dict):
        self._property_changed('leg2_spread')
        self.__leg2_spread = value        

    @property
    def short_conviction_large(self) -> dict:
        return self.__short_conviction_large

    @short_conviction_large.setter
    def short_conviction_large(self, value: dict):
        self._property_changed('short_conviction_large')
        self.__short_conviction_large = value        

    @property
    def ccg_name(self) -> dict:
        return self.__ccg_name

    @ccg_name.setter
    def ccg_name(self, value: dict):
        self._property_changed('ccg_name')
        self.__ccg_name = value        

    @property
    def dollar_excess_return(self) -> dict:
        return self.__dollar_excess_return

    @dollar_excess_return.setter
    def dollar_excess_return(self, value: dict):
        self._property_changed('dollar_excess_return')
        self.__dollar_excess_return = value        

    @property
    def gsn(self) -> dict:
        return self.__gsn

    @gsn.setter
    def gsn(self, value: dict):
        self._property_changed('gsn')
        self.__gsn = value        

    @property
    def trade_end_date(self) -> dict:
        return self.__trade_end_date

    @trade_end_date.setter
    def trade_end_date(self, value: dict):
        self._property_changed('trade_end_date')
        self.__trade_end_date = value        

    @property
    def receiver_rate_option(self) -> dict:
        return self.__receiver_rate_option

    @receiver_rate_option.setter
    def receiver_rate_option(self, value: dict):
        self._property_changed('receiver_rate_option')
        self.__receiver_rate_option = value        

    @property
    def gss(self) -> dict:
        return self.__gss

    @gss.setter
    def gss(self, value: dict):
        self._property_changed('gss')
        self.__gss = value        

    @property
    def percent_of_mediandv1m(self) -> dict:
        return self.__percent_of_mediandv1m

    @percent_of_mediandv1m.setter
    def percent_of_mediandv1m(self, value: dict):
        self._property_changed('percent_of_mediandv1m')
        self.__percent_of_mediandv1m = value        

    @property
    def lendables(self) -> dict:
        return self.__lendables

    @lendables.setter
    def lendables(self, value: dict):
        self._property_changed('lendables')
        self.__lendables = value        

    @property
    def sell75cents(self) -> dict:
        return self.__sell75cents

    @sell75cents.setter
    def sell75cents(self, value: dict):
        self._property_changed('sell75cents')
        self.__sell75cents = value        

    @property
    def option_adjusted_spread(self) -> dict:
        return self.__option_adjusted_spread

    @option_adjusted_spread.setter
    def option_adjusted_spread(self, value: dict):
        self._property_changed('option_adjusted_spread')
        self.__option_adjusted_spread = value        

    @property
    def option_adjusted_swap_spread(self) -> dict:
        return self.__option_adjusted_swap_spread

    @option_adjusted_swap_spread.setter
    def option_adjusted_swap_spread(self, value: dict):
        self._property_changed('option_adjusted_swap_spread')
        self.__option_adjusted_swap_spread = value        

    @property
    def bos_in_ticks_label(self) -> tuple:
        return self.__bos_in_ticks_label

    @bos_in_ticks_label.setter
    def bos_in_ticks_label(self, value: tuple):
        self._property_changed('bos_in_ticks_label')
        self.__bos_in_ticks_label = value        

    @property
    def position_source_id(self) -> dict:
        return self.__position_source_id

    @position_source_id.setter
    def position_source_id(self, value: dict):
        self._property_changed('position_source_id')
        self.__position_source_id = value        

    @property
    def buy1bps(self) -> dict:
        return self.__buy1bps

    @buy1bps.setter
    def buy1bps(self, value: dict):
        self._property_changed('buy1bps')
        self.__buy1bps = value        

    @property
    def buy3point5bps(self) -> dict:
        return self.__buy3point5bps

    @buy3point5bps.setter
    def buy3point5bps(self, value: dict):
        self._property_changed('buy3point5bps')
        self.__buy3point5bps = value        

    @property
    def gs_sustain_region(self) -> dict:
        return self.__gs_sustain_region

    @gs_sustain_region.setter
    def gs_sustain_region(self, value: dict):
        self._property_changed('gs_sustain_region')
        self.__gs_sustain_region = value        

    @property
    def absolute_return_wtd(self) -> dict:
        return self.__absolute_return_wtd

    @absolute_return_wtd.setter
    def absolute_return_wtd(self, value: dict):
        self._property_changed('absolute_return_wtd')
        self.__absolute_return_wtd = value        

    @property
    def deployment_id(self) -> dict:
        return self.__deployment_id

    @deployment_id.setter
    def deployment_id(self, value: dict):
        self._property_changed('deployment_id')
        self.__deployment_id = value        

    @property
    def asset_parameters_seniority(self) -> dict:
        return self.__asset_parameters_seniority

    @asset_parameters_seniority.setter
    def asset_parameters_seniority(self, value: dict):
        self._property_changed('asset_parameters_seniority')
        self.__asset_parameters_seniority = value        

    @property
    def ask_spread(self) -> dict:
        return self.__ask_spread

    @ask_spread.setter
    def ask_spread(self, value: dict):
        self._property_changed('ask_spread')
        self.__ask_spread = value        

    @property
    def flow(self) -> dict:
        return self.__flow

    @flow.setter
    def flow(self, value: dict):
        self._property_changed('flow')
        self.__flow = value        

    @property
    def future_month_h26(self) -> dict:
        return self.__future_month_h26

    @future_month_h26.setter
    def future_month_h26(self, value: dict):
        self._property_changed('future_month_h26')
        self.__future_month_h26 = value        

    @property
    def loan_rebate(self) -> dict:
        return self.__loan_rebate

    @loan_rebate.setter
    def loan_rebate(self, value: dict):
        self._property_changed('loan_rebate')
        self.__loan_rebate = value        

    @property
    def future_month_h25(self) -> dict:
        return self.__future_month_h25

    @future_month_h25.setter
    def future_month_h25(self, value: dict):
        self._property_changed('future_month_h25')
        self.__future_month_h25 = value        

    @property
    def period(self) -> dict:
        return self.__period

    @period.setter
    def period(self, value: dict):
        self._property_changed('period')
        self.__period = value        

    @property
    def index_create_source(self) -> dict:
        return self.__index_create_source

    @index_create_source.setter
    def index_create_source(self, value: dict):
        self._property_changed('index_create_source')
        self.__index_create_source = value        

    @property
    def future_month_h24(self) -> dict:
        return self.__future_month_h24

    @future_month_h24.setter
    def future_month_h24(self, value: dict):
        self._property_changed('future_month_h24')
        self.__future_month_h24 = value        

    @property
    def future_month_h23(self) -> dict:
        return self.__future_month_h23

    @future_month_h23.setter
    def future_month_h23(self, value: dict):
        self._property_changed('future_month_h23')
        self.__future_month_h23 = value        

    @property
    def future_month_h22(self) -> dict:
        return self.__future_month_h22

    @future_month_h22.setter
    def future_month_h22(self, value: dict):
        self._property_changed('future_month_h22')
        self.__future_month_h22 = value        

    @property
    def future_month_h21(self) -> dict:
        return self.__future_month_h21

    @future_month_h21.setter
    def future_month_h21(self, value: dict):
        self._property_changed('future_month_h21')
        self.__future_month_h21 = value        

    @property
    def non_usd_ois(self) -> dict:
        return self.__non_usd_ois

    @non_usd_ois.setter
    def non_usd_ois(self, value: dict):
        self._property_changed('non_usd_ois')
        self.__non_usd_ois = value        

    @property
    def real_twi_contribution(self) -> dict:
        return self.__real_twi_contribution

    @real_twi_contribution.setter
    def real_twi_contribution(self, value: dict):
        self._property_changed('real_twi_contribution')
        self.__real_twi_contribution = value        

    @property
    def mkt_asset(self) -> dict:
        return self.__mkt_asset

    @mkt_asset.setter
    def mkt_asset(self, value: dict):
        self._property_changed('mkt_asset')
        self.__mkt_asset = value        

    @property
    def leg2_index_location(self) -> dict:
        return self.__leg2_index_location

    @leg2_index_location.setter
    def leg2_index_location(self, value: dict):
        self._property_changed('leg2_index_location')
        self.__leg2_index_location = value        

    @property
    def twap_unrealized_bps(self) -> dict:
        return self.__twap_unrealized_bps

    @twap_unrealized_bps.setter
    def twap_unrealized_bps(self, value: dict):
        self._property_changed('twap_unrealized_bps')
        self.__twap_unrealized_bps = value        

    @property
    def last_updated_message(self) -> dict:
        return self.__last_updated_message

    @last_updated_message.setter
    def last_updated_message(self, value: dict):
        self._property_changed('last_updated_message')
        self.__last_updated_message = value        

    @property
    def loan_value(self) -> dict:
        return self.__loan_value

    @loan_value.setter
    def loan_value(self, value: dict):
        self._property_changed('loan_value')
        self.__loan_value = value        

    @property
    def option_adjusted_ois_spread(self) -> dict:
        return self.__option_adjusted_ois_spread

    @option_adjusted_ois_spread.setter
    def option_adjusted_ois_spread(self, value: dict):
        self._property_changed('option_adjusted_ois_spread')
        self.__option_adjusted_ois_spread = value        

    @property
    def total_return_price(self) -> dict:
        return self.__total_return_price

    @total_return_price.setter
    def total_return_price(self, value: dict):
        self._property_changed('total_return_price')
        self.__total_return_price = value        

    @property
    def weighted_percent_in_model(self) -> dict:
        return self.__weighted_percent_in_model

    @weighted_percent_in_model.setter
    def weighted_percent_in_model(self, value: dict):
        self._property_changed('weighted_percent_in_model')
        self.__weighted_percent_in_model = value        

    @property
    def init_loan_spread_required(self) -> dict:
        return self.__init_loan_spread_required

    @init_loan_spread_required.setter
    def init_loan_spread_required(self, value: dict):
        self._property_changed('init_loan_spread_required')
        self.__init_loan_spread_required = value        

    @property
    def election_period(self) -> dict:
        return self.__election_period

    @election_period.setter
    def election_period(self, value: dict):
        self._property_changed('election_period')
        self.__election_period = value        

    @property
    def funding_ask_price(self) -> dict:
        return self.__funding_ask_price

    @funding_ask_price.setter
    def funding_ask_price(self, value: dict):
        self._property_changed('funding_ask_price')
        self.__funding_ask_price = value        

    @property
    def historical_beta(self) -> dict:
        return self.__historical_beta

    @historical_beta.setter
    def historical_beta(self, value: dict):
        self._property_changed('historical_beta')
        self.__historical_beta = value        

    @property
    def bond_risk_premium_index(self) -> dict:
        return self.__bond_risk_premium_index

    @bond_risk_premium_index.setter
    def bond_risk_premium_index(self, value: dict):
        self._property_changed('bond_risk_premium_index')
        self.__bond_risk_premium_index = value        

    @property
    def hit_rate_ytd(self) -> dict:
        return self.__hit_rate_ytd

    @hit_rate_ytd.setter
    def hit_rate_ytd(self, value: dict):
        self._property_changed('hit_rate_ytd')
        self.__hit_rate_ytd = value        

    @property
    def gir_gsdeer_gsfeer(self) -> dict:
        return self.__gir_gsdeer_gsfeer

    @gir_gsdeer_gsfeer.setter
    def gir_gsdeer_gsfeer(self, value: dict):
        self._property_changed('gir_gsdeer_gsfeer')
        self.__gir_gsdeer_gsfeer = value        

    @property
    def num_units(self) -> dict:
        return self.__num_units

    @num_units.setter
    def num_units(self, value: dict):
        self._property_changed('num_units')
        self.__num_units = value        

    @property
    def asset_parameters_receiver_frequency(self) -> dict:
        return self.__asset_parameters_receiver_frequency

    @asset_parameters_receiver_frequency.setter
    def asset_parameters_receiver_frequency(self, value: dict):
        self._property_changed('asset_parameters_receiver_frequency')
        self.__asset_parameters_receiver_frequency = value        

    @property
    def expense_ratio_gross_bps(self) -> dict:
        return self.__expense_ratio_gross_bps

    @expense_ratio_gross_bps.setter
    def expense_ratio_gross_bps(self, value: dict):
        self._property_changed('expense_ratio_gross_bps')
        self.__expense_ratio_gross_bps = value        

    @property
    def relative_payoff_wtd(self) -> dict:
        return self.__relative_payoff_wtd

    @relative_payoff_wtd.setter
    def relative_payoff_wtd(self, value: dict):
        self._property_changed('relative_payoff_wtd')
        self.__relative_payoff_wtd = value        

    @property
    def ctd_price(self) -> dict:
        return self.__ctd_price

    @ctd_price.setter
    def ctd_price(self, value: dict):
        self._property_changed('ctd_price')
        self.__ctd_price = value        

    @property
    def pace_of_roll_now(self) -> dict:
        return self.__pace_of_roll_now

    @pace_of_roll_now.setter
    def pace_of_roll_now(self, value: dict):
        self._property_changed('pace_of_roll_now')
        self.__pace_of_roll_now = value        

    @property
    def product(self) -> dict:
        return self.__product

    @product.setter
    def product(self, value: dict):
        self._property_changed('product')
        self.__product = value        

    @property
    def leg2_return_type(self) -> dict:
        return self.__leg2_return_type

    @leg2_return_type.setter
    def leg2_return_type(self, value: dict):
        self._property_changed('leg2_return_type')
        self.__leg2_return_type = value        

    @property
    def agent_lender_fee(self) -> dict:
        return self.__agent_lender_fee

    @agent_lender_fee.setter
    def agent_lender_fee(self, value: dict):
        self._property_changed('agent_lender_fee')
        self.__agent_lender_fee = value        

    @property
    def dissemination_id(self) -> dict:
        return self.__dissemination_id

    @dissemination_id.setter
    def dissemination_id(self, value: dict):
        self._property_changed('dissemination_id')
        self.__dissemination_id = value        

    @property
    def option_strike_price(self) -> dict:
        return self.__option_strike_price

    @option_strike_price.setter
    def option_strike_price(self, value: dict):
        self._property_changed('option_strike_price')
        self.__option_strike_price = value        

    @property
    def precipitation_type(self) -> dict:
        return self.__precipitation_type

    @precipitation_type.setter
    def precipitation_type(self, value: dict):
        self._property_changed('precipitation_type')
        self.__precipitation_type = value        

    @property
    def lower_bound(self) -> dict:
        return self.__lower_bound

    @lower_bound.setter
    def lower_bound(self, value: dict):
        self._property_changed('lower_bound')
        self.__lower_bound = value        

    @property
    def arrival_mid_normalized(self) -> dict:
        return self.__arrival_mid_normalized

    @arrival_mid_normalized.setter
    def arrival_mid_normalized(self, value: dict):
        self._property_changed('arrival_mid_normalized')
        self.__arrival_mid_normalized = value        

    @property
    def underlying_asset2(self) -> dict:
        return self.__underlying_asset2

    @underlying_asset2.setter
    def underlying_asset2(self, value: dict):
        self._property_changed('underlying_asset2')
        self.__underlying_asset2 = value        

    @property
    def underlying_asset1(self) -> dict:
        return self.__underlying_asset1

    @underlying_asset1.setter
    def underlying_asset1(self, value: dict):
        self._property_changed('underlying_asset1')
        self.__underlying_asset1 = value        

    @property
    def legal_entity(self) -> dict:
        return self.__legal_entity

    @legal_entity.setter
    def legal_entity(self, value: dict):
        self._property_changed('legal_entity')
        self.__legal_entity = value        

    @property
    def performance_fee(self) -> dict:
        return self.__performance_fee

    @performance_fee.setter
    def performance_fee(self, value: dict):
        self._property_changed('performance_fee')
        self.__performance_fee = value        

    @property
    def order_state(self) -> dict:
        return self.__order_state

    @order_state.setter
    def order_state(self, value: dict):
        self._property_changed('order_state')
        self.__order_state = value        

    @property
    def actual_data_quality(self) -> dict:
        return self.__actual_data_quality

    @actual_data_quality.setter
    def actual_data_quality(self, value: dict):
        self._property_changed('actual_data_quality')
        self.__actual_data_quality = value        

    @property
    def index_ratio(self) -> dict:
        return self.__index_ratio

    @index_ratio.setter
    def index_ratio(self, value: dict):
        self._property_changed('index_ratio')
        self.__index_ratio = value        

    @property
    def queue_in_lots_label(self) -> tuple:
        return self.__queue_in_lots_label

    @queue_in_lots_label.setter
    def queue_in_lots_label(self, value: tuple):
        self._property_changed('queue_in_lots_label')
        self.__queue_in_lots_label = value        

    @property
    def adv10_day_pct(self) -> dict:
        return self.__adv10_day_pct

    @adv10_day_pct.setter
    def adv10_day_pct(self, value: dict):
        self._property_changed('adv10_day_pct')
        self.__adv10_day_pct = value        

    @property
    def long_conviction_medium(self) -> dict:
        return self.__long_conviction_medium

    @long_conviction_medium.setter
    def long_conviction_medium(self, value: dict):
        self._property_changed('long_conviction_medium')
        self.__long_conviction_medium = value        

    @property
    def relative_hit_rate_wtd(self) -> dict:
        return self.__relative_hit_rate_wtd

    @relative_hit_rate_wtd.setter
    def relative_hit_rate_wtd(self, value: dict):
        self._property_changed('relative_hit_rate_wtd')
        self.__relative_hit_rate_wtd = value        

    @property
    def daily_tracking_error(self) -> dict:
        return self.__daily_tracking_error

    @daily_tracking_error.setter
    def daily_tracking_error(self, value: dict):
        self._property_changed('daily_tracking_error')
        self.__daily_tracking_error = value        

    @property
    def sell140cents(self) -> dict:
        return self.__sell140cents

    @sell140cents.setter
    def sell140cents(self, value: dict):
        self._property_changed('sell140cents')
        self.__sell140cents = value        

    @property
    def sell10bps(self) -> dict:
        return self.__sell10bps

    @sell10bps.setter
    def sell10bps(self, value: dict):
        self._property_changed('sell10bps')
        self.__sell10bps = value        

    @property
    def aggressive_offset_from_last(self) -> dict:
        return self.__aggressive_offset_from_last

    @aggressive_offset_from_last.setter
    def aggressive_offset_from_last(self, value: dict):
        self._property_changed('aggressive_offset_from_last')
        self.__aggressive_offset_from_last = value        

    @property
    def longitude(self) -> dict:
        return self.__longitude

    @longitude.setter
    def longitude(self, value: dict):
        self._property_changed('longitude')
        self.__longitude = value        

    @property
    def new_icu(self) -> dict:
        return self.__new_icu

    @new_icu.setter
    def new_icu(self, value: dict):
        self._property_changed('new_icu')
        self.__new_icu = value        

    @property
    def market_cap(self) -> dict:
        return self.__market_cap

    @market_cap.setter
    def market_cap(self, value: dict):
        self._property_changed('market_cap')
        self.__market_cap = value        

    @property
    def weighted_average_mid(self) -> dict:
        return self.__weighted_average_mid

    @weighted_average_mid.setter
    def weighted_average_mid(self, value: dict):
        self._property_changed('weighted_average_mid')
        self.__weighted_average_mid = value        

    @property
    def cluster_region(self) -> tuple:
        return self.__cluster_region

    @cluster_region.setter
    def cluster_region(self, value: tuple):
        self._property_changed('cluster_region')
        self.__cluster_region = value        

    @property
    def valoren(self) -> dict:
        return self.__valoren

    @valoren.setter
    def valoren(self, value: dict):
        self._property_changed('valoren')
        self.__valoren = value        

    @property
    def average_execution_price(self) -> dict:
        return self.__average_execution_price

    @average_execution_price.setter
    def average_execution_price(self, value: dict):
        self._property_changed('average_execution_price')
        self.__average_execution_price = value        

    @property
    def proceeds_asset_ois_swap_spread1m(self) -> dict:
        return self.__proceeds_asset_ois_swap_spread1m

    @proceeds_asset_ois_swap_spread1m.setter
    def proceeds_asset_ois_swap_spread1m(self, value: dict):
        self._property_changed('proceeds_asset_ois_swap_spread1m')
        self.__proceeds_asset_ois_swap_spread1m = value        

    @property
    def payoff_wtd(self) -> dict:
        return self.__payoff_wtd

    @payoff_wtd.setter
    def payoff_wtd(self, value: dict):
        self._property_changed('payoff_wtd')
        self.__payoff_wtd = value        

    @property
    def basis(self) -> dict:
        return self.__basis

    @basis.setter
    def basis(self, value: dict):
        self._property_changed('basis')
        self.__basis = value        

    @property
    def investment_rate_trend(self) -> dict:
        return self.__investment_rate_trend

    @investment_rate_trend.setter
    def investment_rate_trend(self, value: dict):
        self._property_changed('investment_rate_trend')
        self.__investment_rate_trend = value        

    @property
    def gross_investment_mtd(self) -> dict:
        return self.__gross_investment_mtd

    @gross_investment_mtd.setter
    def gross_investment_mtd(self, value: dict):
        self._property_changed('gross_investment_mtd')
        self.__gross_investment_mtd = value        

    @property
    def hedge_id(self) -> dict:
        return self.__hedge_id

    @hedge_id.setter
    def hedge_id(self, value: dict):
        self._property_changed('hedge_id')
        self.__hedge_id = value        

    @property
    def sharpe_mtd(self) -> dict:
        return self.__sharpe_mtd

    @sharpe_mtd.setter
    def sharpe_mtd(self, value: dict):
        self._property_changed('sharpe_mtd')
        self.__sharpe_mtd = value        

    @property
    def tcm_cost_horizon8_day(self) -> dict:
        return self.__tcm_cost_horizon8_day

    @tcm_cost_horizon8_day.setter
    def tcm_cost_horizon8_day(self, value: dict):
        self._property_changed('tcm_cost_horizon8_day')
        self.__tcm_cost_horizon8_day = value        

    @property
    def residual_variance(self) -> dict:
        return self.__residual_variance

    @residual_variance.setter
    def residual_variance(self, value: dict):
        self._property_changed('residual_variance')
        self.__residual_variance = value        

    @property
    def restrict_internal_derived_data(self) -> dict:
        return self.__restrict_internal_derived_data

    @restrict_internal_derived_data.setter
    def restrict_internal_derived_data(self, value: dict):
        self._property_changed('restrict_internal_derived_data')
        self.__restrict_internal_derived_data = value        

    @property
    def adv5_day_pct(self) -> dict:
        return self.__adv5_day_pct

    @adv5_day_pct.setter
    def adv5_day_pct(self, value: dict):
        self._property_changed('adv5_day_pct')
        self.__adv5_day_pct = value        

    @property
    def midpoint_fills_percentage(self) -> dict:
        return self.__midpoint_fills_percentage

    @midpoint_fills_percentage.setter
    def midpoint_fills_percentage(self, value: dict):
        self._property_changed('midpoint_fills_percentage')
        self.__midpoint_fills_percentage = value        

    @property
    def open_interest(self) -> dict:
        return self.__open_interest

    @open_interest.setter
    def open_interest(self, value: dict):
        self._property_changed('open_interest')
        self.__open_interest = value        

    @property
    def turnover_composite_unadjusted(self) -> dict:
        return self.__turnover_composite_unadjusted

    @turnover_composite_unadjusted.setter
    def turnover_composite_unadjusted(self, value: dict):
        self._property_changed('turnover_composite_unadjusted')
        self.__turnover_composite_unadjusted = value        

    @property
    def fwd_points(self) -> dict:
        return self.__fwd_points

    @fwd_points.setter
    def fwd_points(self, value: dict):
        self._property_changed('fwd_points')
        self.__fwd_points = value        

    @property
    def relative_return_wtd(self) -> dict:
        return self.__relative_return_wtd

    @relative_return_wtd.setter
    def relative_return_wtd(self, value: dict):
        self._property_changed('relative_return_wtd')
        self.__relative_return_wtd = value        

    @property
    def units(self) -> dict:
        return self.__units

    @units.setter
    def units(self, value: dict):
        self._property_changed('units')
        self.__units = value        

    @property
    def payer_rate_option(self) -> dict:
        return self.__payer_rate_option

    @payer_rate_option.setter
    def payer_rate_option(self, value: dict):
        self._property_changed('payer_rate_option')
        self.__payer_rate_option = value        

    @property
    def asset_classifications_risk_country_name(self) -> dict:
        return self.__asset_classifications_risk_country_name

    @asset_classifications_risk_country_name.setter
    def asset_classifications_risk_country_name(self, value: dict):
        self._property_changed('asset_classifications_risk_country_name')
        self.__asset_classifications_risk_country_name = value        

    @property
    def ext_mkt_point3(self) -> dict:
        return self.__ext_mkt_point3

    @ext_mkt_point3.setter
    def ext_mkt_point3(self, value: dict):
        self._property_changed('ext_mkt_point3')
        self.__ext_mkt_point3 = value        

    @property
    def matched_maturity_swap_spread(self) -> dict:
        return self.__matched_maturity_swap_spread

    @matched_maturity_swap_spread.setter
    def matched_maturity_swap_spread(self, value: dict):
        self._property_changed('matched_maturity_swap_spread')
        self.__matched_maturity_swap_spread = value        

    @property
    def city_name(self) -> dict:
        return self.__city_name

    @city_name.setter
    def city_name(self, value: dict):
        self._property_changed('city_name')
        self.__city_name = value        

    @property
    def hourly_bucket(self) -> dict:
        return self.__hourly_bucket

    @hourly_bucket.setter
    def hourly_bucket(self, value: dict):
        self._property_changed('hourly_bucket')
        self.__hourly_bucket = value        

    @property
    def average_implied_volatility(self) -> dict:
        return self.__average_implied_volatility

    @average_implied_volatility.setter
    def average_implied_volatility(self, value: dict):
        self._property_changed('average_implied_volatility')
        self.__average_implied_volatility = value        

    @property
    def total_hospitalized_with_symptoms(self) -> dict:
        return self.__total_hospitalized_with_symptoms

    @total_hospitalized_with_symptoms.setter
    def total_hospitalized_with_symptoms(self, value: dict):
        self._property_changed('total_hospitalized_with_symptoms')
        self.__total_hospitalized_with_symptoms = value        

    @property
    def days_open_realized_cash(self) -> dict:
        return self.__days_open_realized_cash

    @days_open_realized_cash.setter
    def days_open_realized_cash(self, value: dict):
        self._property_changed('days_open_realized_cash')
        self.__days_open_realized_cash = value        

    @property
    def adjusted_high_price(self) -> dict:
        return self.__adjusted_high_price

    @adjusted_high_price.setter
    def adjusted_high_price(self, value: dict):
        self._property_changed('adjusted_high_price')
        self.__adjusted_high_price = value        

    @property
    def proceeds_asset_ois_swap_spread(self) -> dict:
        return self.__proceeds_asset_ois_swap_spread

    @proceeds_asset_ois_swap_spread.setter
    def proceeds_asset_ois_swap_spread(self, value: dict):
        self._property_changed('proceeds_asset_ois_swap_spread')
        self.__proceeds_asset_ois_swap_spread = value        

    @property
    def ext_mkt_point1(self) -> dict:
        return self.__ext_mkt_point1

    @ext_mkt_point1.setter
    def ext_mkt_point1(self, value: dict):
        self._property_changed('ext_mkt_point1')
        self.__ext_mkt_point1 = value        

    @property
    def direction(self) -> dict:
        return self.__direction

    @direction.setter
    def direction(self, value: dict):
        self._property_changed('direction')
        self.__direction = value        

    @property
    def ext_mkt_point2(self) -> dict:
        return self.__ext_mkt_point2

    @ext_mkt_point2.setter
    def ext_mkt_point2(self, value: dict):
        self._property_changed('ext_mkt_point2')
        self.__ext_mkt_point2 = value        

    @property
    def sub_region_code(self) -> dict:
        return self.__sub_region_code

    @sub_region_code.setter
    def sub_region_code(self, value: dict):
        self._property_changed('sub_region_code')
        self.__sub_region_code = value        

    @property
    def asset_parameters_fixed_rate(self) -> dict:
        return self.__asset_parameters_fixed_rate

    @asset_parameters_fixed_rate.setter
    def asset_parameters_fixed_rate(self, value: dict):
        self._property_changed('asset_parameters_fixed_rate')
        self.__asset_parameters_fixed_rate = value        

    @property
    def is_estimated_return(self) -> dict:
        return self.__is_estimated_return

    @is_estimated_return.setter
    def is_estimated_return(self, value: dict):
        self._property_changed('is_estimated_return')
        self.__is_estimated_return = value        

    @property
    def value_forecast(self) -> dict:
        return self.__value_forecast

    @value_forecast.setter
    def value_forecast(self, value: dict):
        self._property_changed('value_forecast')
        self.__value_forecast = value        

    @property
    def total_icu(self) -> dict:
        return self.__total_icu

    @total_icu.setter
    def total_icu(self, value: dict):
        self._property_changed('total_icu')
        self.__total_icu = value        

    @property
    def position_source_type(self) -> dict:
        return self.__position_source_type

    @position_source_type.setter
    def position_source_type(self, value: dict):
        self._property_changed('position_source_type')
        self.__position_source_type = value        

    @property
    def previous_close_unrealized_cash(self) -> dict:
        return self.__previous_close_unrealized_cash

    @previous_close_unrealized_cash.setter
    def previous_close_unrealized_cash(self, value: dict):
        self._property_changed('previous_close_unrealized_cash')
        self.__previous_close_unrealized_cash = value        

    @property
    def minimum_denomination(self) -> dict:
        return self.__minimum_denomination

    @minimum_denomination.setter
    def minimum_denomination(self, value: dict):
        self._property_changed('minimum_denomination')
        self.__minimum_denomination = value        

    @property
    def future_value_notional(self) -> dict:
        return self.__future_value_notional

    @future_value_notional.setter
    def future_value_notional(self, value: dict):
        self._property_changed('future_value_notional')
        self.__future_value_notional = value        

    @property
    def participation_rate(self) -> dict:
        return self.__participation_rate

    @participation_rate.setter
    def participation_rate(self, value: dict):
        self._property_changed('participation_rate')
        self.__participation_rate = value        

    @property
    def obfr(self) -> dict:
        return self.__obfr

    @obfr.setter
    def obfr(self, value: dict):
        self._property_changed('obfr')
        self.__obfr = value        

    @property
    def buy9point5bps(self) -> dict:
        return self.__buy9point5bps

    @buy9point5bps.setter
    def buy9point5bps(self, value: dict):
        self._property_changed('buy9point5bps')
        self.__buy9point5bps = value        

    @property
    def option_lock_period(self) -> dict:
        return self.__option_lock_period

    @option_lock_period.setter
    def option_lock_period(self, value: dict):
        self._property_changed('option_lock_period')
        self.__option_lock_period = value        

    @property
    def es_momentum_percentile(self) -> dict:
        return self.__es_momentum_percentile

    @es_momentum_percentile.setter
    def es_momentum_percentile(self, value: dict):
        self._property_changed('es_momentum_percentile')
        self.__es_momentum_percentile = value        

    @property
    def adv_percentage(self) -> dict:
        return self.__adv_percentage

    @adv_percentage.setter
    def adv_percentage(self, value: dict):
        self._property_changed('adv_percentage')
        self.__adv_percentage = value        

    @property
    def leg1_averaging_method(self) -> dict:
        return self.__leg1_averaging_method

    @leg1_averaging_method.setter
    def leg1_averaging_method(self, value: dict):
        self._property_changed('leg1_averaging_method')
        self.__leg1_averaging_method = value        

    @property
    def turnover_composite(self) -> dict:
        return self.__turnover_composite

    @turnover_composite.setter
    def turnover_composite(self, value: dict):
        self._property_changed('turnover_composite')
        self.__turnover_composite = value        

    @property
    def forecast_date(self) -> dict:
        return self.__forecast_date

    @forecast_date.setter
    def forecast_date(self, value: dict):
        self._property_changed('forecast_date')
        self.__forecast_date = value        

    @property
    def internal_index_calc_region(self) -> dict:
        return self.__internal_index_calc_region

    @internal_index_calc_region.setter
    def internal_index_calc_region(self, value: dict):
        self._property_changed('internal_index_calc_region')
        self.__internal_index_calc_region = value        

    @property
    def position_type(self) -> dict:
        return self.__position_type

    @position_type.setter
    def position_type(self, value: dict):
        self._property_changed('position_type')
        self.__position_type = value        

    @property
    def sub_asset_class(self) -> dict:
        return self.__sub_asset_class

    @sub_asset_class.setter
    def sub_asset_class(self, value: dict):
        self._property_changed('sub_asset_class')
        self.__sub_asset_class = value        

    @property
    def short_interest(self) -> dict:
        return self.__short_interest

    @short_interest.setter
    def short_interest(self, value: dict):
        self._property_changed('short_interest')
        self.__short_interest = value        

    @property
    def reference_period(self) -> dict:
        return self.__reference_period

    @reference_period.setter
    def reference_period(self, value: dict):
        self._property_changed('reference_period')
        self.__reference_period = value        

    @property
    def adjusted_volume(self) -> dict:
        return self.__adjusted_volume

    @adjusted_volume.setter
    def adjusted_volume(self, value: dict):
        self._property_changed('adjusted_volume')
        self.__adjusted_volume = value        

    @property
    def ctd_fwd_yield(self) -> dict:
        return self.__ctd_fwd_yield

    @ctd_fwd_yield.setter
    def ctd_fwd_yield(self, value: dict):
        self._property_changed('ctd_fwd_yield')
        self.__ctd_fwd_yield = value        

    @property
    def sec_db(self) -> dict:
        return self.__sec_db

    @sec_db.setter
    def sec_db(self, value: dict):
        self._property_changed('sec_db')
        self.__sec_db = value        

    @property
    def memory_used(self) -> dict:
        return self.__memory_used

    @memory_used.setter
    def memory_used(self, value: dict):
        self._property_changed('memory_used')
        self.__memory_used = value        

    @property
    def bpe_quality_stars(self) -> dict:
        return self.__bpe_quality_stars

    @bpe_quality_stars.setter
    def bpe_quality_stars(self, value: dict):
        self._property_changed('bpe_quality_stars')
        self.__bpe_quality_stars = value        

    @property
    def ctd(self) -> dict:
        return self.__ctd

    @ctd.setter
    def ctd(self, value: dict):
        self._property_changed('ctd')
        self.__ctd = value        

    @property
    def intended_participation_rate(self) -> dict:
        return self.__intended_participation_rate

    @intended_participation_rate.setter
    def intended_participation_rate(self, value: dict):
        self._property_changed('intended_participation_rate')
        self.__intended_participation_rate = value        

    @property
    def leg1_payment_type(self) -> dict:
        return self.__leg1_payment_type

    @leg1_payment_type.setter
    def leg1_payment_type(self, value: dict):
        self._property_changed('leg1_payment_type')
        self.__leg1_payment_type = value        

    @property
    def trading_pnl(self) -> dict:
        return self.__trading_pnl

    @trading_pnl.setter
    def trading_pnl(self, value: dict):
        self._property_changed('trading_pnl')
        self.__trading_pnl = value        

    @property
    def collateral_value_required(self) -> dict:
        return self.__collateral_value_required

    @collateral_value_required.setter
    def collateral_value_required(self, value: dict):
        self._property_changed('collateral_value_required')
        self.__collateral_value_required = value        

    @property
    def buy45bps(self) -> dict:
        return self.__buy45bps

    @buy45bps.setter
    def buy45bps(self, value: dict):
        self._property_changed('buy45bps')
        self.__buy45bps = value        

    @property
    def price_to_earnings_positive(self) -> dict:
        return self.__price_to_earnings_positive

    @price_to_earnings_positive.setter
    def price_to_earnings_positive(self, value: dict):
        self._property_changed('price_to_earnings_positive')
        self.__price_to_earnings_positive = value        

    @property
    def forecast(self) -> dict:
        return self.__forecast

    @forecast.setter
    def forecast(self, value: dict):
        self._property_changed('forecast')
        self.__forecast = value        

    @property
    def forecast_value(self) -> dict:
        return self.__forecast_value

    @forecast_value.setter
    def forecast_value(self, value: dict):
        self._property_changed('forecast_value')
        self.__forecast_value = value        

    @property
    def pnl(self) -> dict:
        return self.__pnl

    @pnl.setter
    def pnl(self, value: dict):
        self._property_changed('pnl')
        self.__pnl = value        

    @property
    def volume_in_limit(self) -> dict:
        return self.__volume_in_limit

    @volume_in_limit.setter
    def volume_in_limit(self, value: dict):
        self._property_changed('volume_in_limit')
        self.__volume_in_limit = value        

    @property
    def is_territory(self) -> dict:
        return self.__is_territory

    @is_territory.setter
    def is_territory(self, value: dict):
        self._property_changed('is_territory')
        self.__is_territory = value        

    @property
    def leg2_delivery_point(self) -> dict:
        return self.__leg2_delivery_point

    @leg2_delivery_point.setter
    def leg2_delivery_point(self, value: dict):
        self._property_changed('leg2_delivery_point')
        self.__leg2_delivery_point = value        

    @property
    def tcm_cost_horizon4_day(self) -> dict:
        return self.__tcm_cost_horizon4_day

    @tcm_cost_horizon4_day.setter
    def tcm_cost_horizon4_day(self, value: dict):
        self._property_changed('tcm_cost_horizon4_day')
        self.__tcm_cost_horizon4_day = value        

    @property
    def styles(self) -> dict:
        return self.__styles

    @styles.setter
    def styles(self, value: dict):
        self._property_changed('styles')
        self.__styles = value        

    @property
    def short_name(self) -> dict:
        return self.__short_name

    @short_name.setter
    def short_name(self, value: dict):
        self._property_changed('short_name')
        self.__short_name = value        

    @property
    def reset_frequency1(self) -> dict:
        return self.__reset_frequency1

    @reset_frequency1.setter
    def reset_frequency1(self, value: dict):
        self._property_changed('reset_frequency1')
        self.__reset_frequency1 = value        

    @property
    def buy4bps(self) -> dict:
        return self.__buy4bps

    @buy4bps.setter
    def buy4bps(self, value: dict):
        self._property_changed('buy4bps')
        self.__buy4bps = value        

    @property
    def reset_frequency2(self) -> dict:
        return self.__reset_frequency2

    @reset_frequency2.setter
    def reset_frequency2(self, value: dict):
        self._property_changed('reset_frequency2')
        self.__reset_frequency2 = value        

    @property
    def other_price_term(self) -> dict:
        return self.__other_price_term

    @other_price_term.setter
    def other_price_term(self, value: dict):
        self._property_changed('other_price_term')
        self.__other_price_term = value        

    @property
    def bid_gspread(self) -> dict:
        return self.__bid_gspread

    @bid_gspread.setter
    def bid_gspread(self, value: dict):
        self._property_changed('bid_gspread')
        self.__bid_gspread = value        

    @property
    def open_price(self) -> dict:
        return self.__open_price

    @open_price.setter
    def open_price(self, value: dict):
        self._property_changed('open_price')
        self.__open_price = value        

    @property
    def ps_id(self) -> dict:
        return self.__ps_id

    @ps_id.setter
    def ps_id(self, value: dict):
        self._property_changed('ps_id')
        self.__ps_id = value        

    @property
    def hit_rate_mtd(self) -> dict:
        return self.__hit_rate_mtd

    @hit_rate_mtd.setter
    def hit_rate_mtd(self, value: dict):
        self._property_changed('hit_rate_mtd')
        self.__hit_rate_mtd = value        

    @property
    def fair_volatility(self) -> dict:
        return self.__fair_volatility

    @fair_volatility.setter
    def fair_volatility(self, value: dict):
        self._property_changed('fair_volatility')
        self.__fair_volatility = value        

    @property
    def dollar_cross(self) -> dict:
        return self.__dollar_cross

    @dollar_cross.setter
    def dollar_cross(self, value: dict):
        self._property_changed('dollar_cross')
        self.__dollar_cross = value        

    @property
    def portfolio_type(self) -> dict:
        return self.__portfolio_type

    @portfolio_type.setter
    def portfolio_type(self, value: dict):
        self._property_changed('portfolio_type')
        self.__portfolio_type = value        

    @property
    def currency(self) -> dict:
        return self.__currency

    @currency.setter
    def currency(self, value: dict):
        self._property_changed('currency')
        self.__currency = value        

    @property
    def cluster_class(self) -> dict:
        return self.__cluster_class

    @cluster_class.setter
    def cluster_class(self, value: dict):
        self._property_changed('cluster_class')
        self.__cluster_class = value        

    @property
    def sell50bps(self) -> dict:
        return self.__sell50bps

    @sell50bps.setter
    def sell50bps(self, value: dict):
        self._property_changed('sell50bps')
        self.__sell50bps = value        

    @property
    def future_month_m21(self) -> dict:
        return self.__future_month_m21

    @future_month_m21.setter
    def future_month_m21(self, value: dict):
        self._property_changed('future_month_m21')
        self.__future_month_m21 = value        

    @property
    def bid_size(self) -> dict:
        return self.__bid_size

    @bid_size.setter
    def bid_size(self, value: dict):
        self._property_changed('bid_size')
        self.__bid_size = value        

    @property
    def arrival_mid(self) -> dict:
        return self.__arrival_mid

    @arrival_mid.setter
    def arrival_mid(self, value: dict):
        self._property_changed('arrival_mid')
        self.__arrival_mid = value        

    @property
    def asset_parameters_exchange_currency(self) -> dict:
        return self.__asset_parameters_exchange_currency

    @asset_parameters_exchange_currency.setter
    def asset_parameters_exchange_currency(self, value: dict):
        self._property_changed('asset_parameters_exchange_currency')
        self.__asset_parameters_exchange_currency = value        

    @property
    def candidate_name(self) -> dict:
        return self.__candidate_name

    @candidate_name.setter
    def candidate_name(self, value: dict):
        self._property_changed('candidate_name')
        self.__candidate_name = value        

    @property
    def implied_lognormal_volatility(self) -> dict:
        return self.__implied_lognormal_volatility

    @implied_lognormal_volatility.setter
    def implied_lognormal_volatility(self, value: dict):
        self._property_changed('implied_lognormal_volatility')
        self.__implied_lognormal_volatility = value        

    @property
    def vwap_in_limit_unrealized_cash(self) -> dict:
        return self.__vwap_in_limit_unrealized_cash

    @vwap_in_limit_unrealized_cash.setter
    def vwap_in_limit_unrealized_cash(self, value: dict):
        self._property_changed('vwap_in_limit_unrealized_cash')
        self.__vwap_in_limit_unrealized_cash = value        

    @property
    def rating_moodys(self) -> dict:
        return self.__rating_moodys

    @rating_moodys.setter
    def rating_moodys(self, value: dict):
        self._property_changed('rating_moodys')
        self.__rating_moodys = value        

    @property
    def future_month_m26(self) -> dict:
        return self.__future_month_m26

    @future_month_m26.setter
    def future_month_m26(self, value: dict):
        self._property_changed('future_month_m26')
        self.__future_month_m26 = value        

    @property
    def future_month_m25(self) -> dict:
        return self.__future_month_m25

    @future_month_m25.setter
    def future_month_m25(self, value: dict):
        self._property_changed('future_month_m25')
        self.__future_month_m25 = value        

    @property
    def future_month_m24(self) -> dict:
        return self.__future_month_m24

    @future_month_m24.setter
    def future_month_m24(self, value: dict):
        self._property_changed('future_month_m24')
        self.__future_month_m24 = value        

    @property
    def future_month_m23(self) -> dict:
        return self.__future_month_m23

    @future_month_m23.setter
    def future_month_m23(self, value: dict):
        self._property_changed('future_month_m23')
        self.__future_month_m23 = value        

    @property
    def future_month_m22(self) -> dict:
        return self.__future_month_m22

    @future_month_m22.setter
    def future_month_m22(self, value: dict):
        self._property_changed('future_month_m22')
        self.__future_month_m22 = value        

    @property
    def flow_pct(self) -> dict:
        return self.__flow_pct

    @flow_pct.setter
    def flow_pct(self, value: dict):
        self._property_changed('flow_pct')
        self.__flow_pct = value        

    @property
    def source(self) -> dict:
        return self.__source

    @source.setter
    def source(self, value: dict):
        self._property_changed('source')
        self.__source = value        

    @property
    def asset_classifications_country_code(self) -> dict:
        return self.__asset_classifications_country_code

    @asset_classifications_country_code.setter
    def asset_classifications_country_code(self, value: dict):
        self._property_changed('asset_classifications_country_code')
        self.__asset_classifications_country_code = value        

    @property
    def settle_drop(self) -> dict:
        return self.__settle_drop

    @settle_drop.setter
    def settle_drop(self, value: dict):
        self._property_changed('settle_drop')
        self.__settle_drop = value        

    @property
    def data_set_sub_category(self) -> dict:
        return self.__data_set_sub_category

    @data_set_sub_category.setter
    def data_set_sub_category(self, value: dict):
        self._property_changed('data_set_sub_category')
        self.__data_set_sub_category = value        

    @property
    def sell9point5bps(self) -> dict:
        return self.__sell9point5bps

    @sell9point5bps.setter
    def sell9point5bps(self, value: dict):
        self._property_changed('sell9point5bps')
        self.__sell9point5bps = value        

    @property
    def quantity_bucket(self) -> dict:
        return self.__quantity_bucket

    @quantity_bucket.setter
    def quantity_bucket(self, value: dict):
        self._property_changed('quantity_bucket')
        self.__quantity_bucket = value        

    @property
    def option_style_sdr(self) -> dict:
        return self.__option_style_sdr

    @option_style_sdr.setter
    def option_style_sdr(self, value: dict):
        self._property_changed('option_style_sdr')
        self.__option_style_sdr = value        

    @property
    def oe_name(self) -> dict:
        return self.__oe_name

    @oe_name.setter
    def oe_name(self, value: dict):
        self._property_changed('oe_name')
        self.__oe_name = value        

    @property
    def given(self) -> dict:
        return self.__given

    @given.setter
    def given(self, value: dict):
        self._property_changed('given')
        self.__given = value        

    @property
    def leg2_day_count_convention(self) -> dict:
        return self.__leg2_day_count_convention

    @leg2_day_count_convention.setter
    def leg2_day_count_convention(self, value: dict):
        self._property_changed('leg2_day_count_convention')
        self.__leg2_day_count_convention = value        

    @property
    def liquidity_score_sell(self) -> dict:
        return self.__liquidity_score_sell

    @liquidity_score_sell.setter
    def liquidity_score_sell(self, value: dict):
        self._property_changed('liquidity_score_sell')
        self.__liquidity_score_sell = value        

    @property
    def delisting_date(self) -> dict:
        return self.__delisting_date

    @delisting_date.setter
    def delisting_date(self, value: dict):
        self._property_changed('delisting_date')
        self.__delisting_date = value        

    @property
    def weight(self) -> dict:
        return self.__weight

    @weight.setter
    def weight(self, value: dict):
        self._property_changed('weight')
        self.__weight = value        

    @property
    def accrued_interest(self) -> dict:
        return self.__accrued_interest

    @accrued_interest.setter
    def accrued_interest(self, value: dict):
        self._property_changed('accrued_interest')
        self.__accrued_interest = value        

    @property
    def business_scope(self) -> dict:
        return self.__business_scope

    @business_scope.setter
    def business_scope(self, value: dict):
        self._property_changed('business_scope')
        self.__business_scope = value        

    @property
    def wtd_degree_days(self) -> dict:
        return self.__wtd_degree_days

    @wtd_degree_days.setter
    def wtd_degree_days(self, value: dict):
        self._property_changed('wtd_degree_days')
        self.__wtd_degree_days = value        

    @property
    def absolute_weight(self) -> dict:
        return self.__absolute_weight

    @absolute_weight.setter
    def absolute_weight(self, value: dict):
        self._property_changed('absolute_weight')
        self.__absolute_weight = value        

    @property
    def measure(self) -> dict:
        return self.__measure

    @measure.setter
    def measure(self, value: dict):
        self._property_changed('measure')
        self.__measure = value        

    @property
    def temperature_hourly_forecast(self) -> dict:
        return self.__temperature_hourly_forecast

    @temperature_hourly_forecast.setter
    def temperature_hourly_forecast(self, value: dict):
        self._property_changed('temperature_hourly_forecast')
        self.__temperature_hourly_forecast = value        

    @property
    def iceberg_tip_rate_type(self) -> dict:
        return self.__iceberg_tip_rate_type

    @iceberg_tip_rate_type.setter
    def iceberg_tip_rate_type(self, value: dict):
        self._property_changed('iceberg_tip_rate_type')
        self.__iceberg_tip_rate_type = value        

    @property
    def sharpe_ytd(self) -> dict:
        return self.__sharpe_ytd

    @sharpe_ytd.setter
    def sharpe_ytd(self, value: dict):
        self._property_changed('sharpe_ytd')
        self.__sharpe_ytd = value        

    @property
    def wind_speed_forecast(self) -> dict:
        return self.__wind_speed_forecast

    @wind_speed_forecast.setter
    def wind_speed_forecast(self, value: dict):
        self._property_changed('wind_speed_forecast')
        self.__wind_speed_forecast = value        

    @property
    def gross_investment_ytd(self) -> dict:
        return self.__gross_investment_ytd

    @gross_investment_ytd.setter
    def gross_investment_ytd(self, value: dict):
        self._property_changed('gross_investment_ytd')
        self.__gross_investment_ytd = value        

    @property
    def yield_price(self) -> dict:
        return self.__yield_price

    @yield_price.setter
    def yield_price(self, value: dict):
        self._property_changed('yield_price')
        self.__yield_price = value        

    @property
    def leg1_total_notional_unit(self) -> dict:
        return self.__leg1_total_notional_unit

    @leg1_total_notional_unit.setter
    def leg1_total_notional_unit(self, value: dict):
        self._property_changed('leg1_total_notional_unit')
        self.__leg1_total_notional_unit = value        

    @property
    def issue_price(self) -> dict:
        return self.__issue_price

    @issue_price.setter
    def issue_price(self, value: dict):
        self._property_changed('issue_price')
        self.__issue_price = value        

    @property
    def ask_high(self) -> dict:
        return self.__ask_high

    @ask_high.setter
    def ask_high(self, value: dict):
        self._property_changed('ask_high')
        self.__ask_high = value        

    @property
    def expected_data_quality(self) -> dict:
        return self.__expected_data_quality

    @expected_data_quality.setter
    def expected_data_quality(self, value: dict):
        self._property_changed('expected_data_quality')
        self.__expected_data_quality = value        

    @property
    def region_name(self) -> dict:
        return self.__region_name

    @region_name.setter
    def region_name(self, value: dict):
        self._property_changed('region_name')
        self.__region_name = value        

    @property
    def value_revised(self) -> dict:
        return self.__value_revised

    @value_revised.setter
    def value_revised(self, value: dict):
        self._property_changed('value_revised')
        self.__value_revised = value        

    @property
    def discretion_upper_bound(self) -> dict:
        return self.__discretion_upper_bound

    @discretion_upper_bound.setter
    def discretion_upper_bound(self, value: dict):
        self._property_changed('discretion_upper_bound')
        self.__discretion_upper_bound = value        

    @property
    def adjusted_trade_price(self) -> dict:
        return self.__adjusted_trade_price

    @adjusted_trade_price.setter
    def adjusted_trade_price(self, value: dict):
        self._property_changed('adjusted_trade_price')
        self.__adjusted_trade_price = value        

    @property
    def iso_subdivision_code_alpha2(self) -> dict:
        return self.__iso_subdivision_code_alpha2

    @iso_subdivision_code_alpha2.setter
    def iso_subdivision_code_alpha2(self, value: dict):
        self._property_changed('iso_subdivision_code_alpha2')
        self.__iso_subdivision_code_alpha2 = value        

    @property
    def ctd_conversion_factor(self) -> dict:
        return self.__ctd_conversion_factor

    @ctd_conversion_factor.setter
    def ctd_conversion_factor(self, value: dict):
        self._property_changed('ctd_conversion_factor')
        self.__ctd_conversion_factor = value        

    @property
    def proceeds_asset_swap_spread(self) -> dict:
        return self.__proceeds_asset_swap_spread

    @proceeds_asset_swap_spread.setter
    def proceeds_asset_swap_spread(self, value: dict):
        self._property_changed('proceeds_asset_swap_spread')
        self.__proceeds_asset_swap_spread = value        

    @property
    def is_adr(self) -> dict:
        return self.__is_adr

    @is_adr.setter
    def is_adr(self, value: dict):
        self._property_changed('is_adr')
        self.__is_adr = value        

    @property
    def issue_date(self) -> dict:
        return self.__issue_date

    @issue_date.setter
    def issue_date(self, value: dict):
        self._property_changed('issue_date')
        self.__issue_date = value        

    @property
    def service_id(self) -> dict:
        return self.__service_id

    @service_id.setter
    def service_id(self, value: dict):
        self._property_changed('service_id')
        self.__service_id = value        

    @property
    def yes(self) -> dict:
        return self.__yes

    @yes.setter
    def yes(self, value: dict):
        self._property_changed('yes')
        self.__yes = value        

    @property
    def g_score(self) -> dict:
        return self.__g_score

    @g_score.setter
    def g_score(self, value: dict):
        self._property_changed('g_score')
        self.__g_score = value        

    @property
    def market_value(self) -> dict:
        return self.__market_value

    @market_value.setter
    def market_value(self, value: dict):
        self._property_changed('market_value')
        self.__market_value = value        

    @property
    def entity_id(self) -> dict:
        return self.__entity_id

    @entity_id.setter
    def entity_id(self, value: dict):
        self._property_changed('entity_id')
        self.__entity_id = value        

    @property
    def notional_currency1(self) -> dict:
        return self.__notional_currency1

    @notional_currency1.setter
    def notional_currency1(self, value: dict):
        self._property_changed('notional_currency1')
        self.__notional_currency1 = value        

    @property
    def net_debt_to_ebitda(self) -> dict:
        return self.__net_debt_to_ebitda

    @net_debt_to_ebitda.setter
    def net_debt_to_ebitda(self, value: dict):
        self._property_changed('net_debt_to_ebitda')
        self.__net_debt_to_ebitda = value        

    @property
    def num_units_upper(self) -> dict:
        return self.__num_units_upper

    @num_units_upper.setter
    def num_units_upper(self, value: dict):
        self._property_changed('num_units_upper')
        self.__num_units_upper = value        

    @property
    def notional_currency2(self) -> dict:
        return self.__notional_currency2

    @notional_currency2.setter
    def notional_currency2(self, value: dict):
        self._property_changed('notional_currency2')
        self.__notional_currency2 = value        

    @property
    def in_limit_participation_rate(self) -> dict:
        return self.__in_limit_participation_rate

    @in_limit_participation_rate.setter
    def in_limit_participation_rate(self, value: dict):
        self._property_changed('in_limit_participation_rate')
        self.__in_limit_participation_rate = value        

    @property
    def pressure_forecast(self) -> dict:
        return self.__pressure_forecast

    @pressure_forecast.setter
    def pressure_forecast(self, value: dict):
        self._property_changed('pressure_forecast')
        self.__pressure_forecast = value        

    @property
    def paid(self) -> dict:
        return self.__paid

    @paid.setter
    def paid(self, value: dict):
        self._property_changed('paid')
        self.__paid = value        

    @property
    def fixed_rate(self) -> dict:
        return self.__fixed_rate

    @fixed_rate.setter
    def fixed_rate(self, value: dict):
        self._property_changed('fixed_rate')
        self.__fixed_rate = value        

    @property
    def short(self) -> dict:
        return self.__short

    @short.setter
    def short(self, value: dict):
        self._property_changed('short')
        self.__short = value        

    @property
    def buy4point5bps(self) -> dict:
        return self.__buy4point5bps

    @buy4point5bps.setter
    def buy4point5bps(self, value: dict):
        self._property_changed('buy4point5bps')
        self.__buy4point5bps = value        

    @property
    def sell30cents(self) -> dict:
        return self.__sell30cents

    @sell30cents.setter
    def sell30cents(self, value: dict):
        self._property_changed('sell30cents')
        self.__sell30cents = value        

    @property
    def leg1_payment_frequency(self) -> dict:
        return self.__leg1_payment_frequency

    @leg1_payment_frequency.setter
    def leg1_payment_frequency(self, value: dict):
        self._property_changed('leg1_payment_frequency')
        self.__leg1_payment_frequency = value        

    @property
    def cm_id(self) -> dict:
        return self.__cm_id

    @cm_id.setter
    def cm_id(self, value: dict):
        self._property_changed('cm_id')
        self.__cm_id = value        

    @property
    def taxonomy(self) -> dict:
        return self.__taxonomy

    @taxonomy.setter
    def taxonomy(self, value: dict):
        self._property_changed('taxonomy')
        self.__taxonomy = value        

    @property
    def buy45cents(self) -> dict:
        return self.__buy45cents

    @buy45cents.setter
    def buy45cents(self, value: dict):
        self._property_changed('buy45cents')
        self.__buy45cents = value        

    @property
    def measures(self) -> dict:
        return self.__measures

    @measures.setter
    def measures(self, value: dict):
        self._property_changed('measures')
        self.__measures = value        

    @property
    def seasonal_adjustment(self) -> dict:
        return self.__seasonal_adjustment

    @seasonal_adjustment.setter
    def seasonal_adjustment(self, value: dict):
        self._property_changed('seasonal_adjustment')
        self.__seasonal_adjustment = value        

    @property
    def rank_wtd(self) -> dict:
        return self.__rank_wtd

    @rank_wtd.setter
    def rank_wtd(self, value: dict):
        self._property_changed('rank_wtd')
        self.__rank_wtd = value        

    @property
    def underlyer(self) -> dict:
        return self.__underlyer

    @underlyer.setter
    def underlyer(self, value: dict):
        self._property_changed('underlyer')
        self.__underlyer = value        

    @property
    def identifier(self) -> dict:
        return self.__identifier

    @identifier.setter
    def identifier(self, value: dict):
        self._property_changed('identifier')
        self.__identifier = value        

    @property
    def price_unit(self) -> dict:
        return self.__price_unit

    @price_unit.setter
    def price_unit(self, value: dict):
        self._property_changed('price_unit')
        self.__price_unit = value        

    @property
    def trade_report_ref_id(self) -> dict:
        return self.__trade_report_ref_id

    @trade_report_ref_id.setter
    def trade_report_ref_id(self, value: dict):
        self._property_changed('trade_report_ref_id')
        self.__trade_report_ref_id = value        

    @property
    def subdivision_id(self) -> dict:
        return self.__subdivision_id

    @subdivision_id.setter
    def subdivision_id(self, value: dict):
        self._property_changed('subdivision_id')
        self.__subdivision_id = value        

    @property
    def unadjusted_low(self) -> dict:
        return self.__unadjusted_low

    @unadjusted_low.setter
    def unadjusted_low(self, value: dict):
        self._property_changed('unadjusted_low')
        self.__unadjusted_low = value        

    @property
    def buy160cents(self) -> dict:
        return self.__buy160cents

    @buy160cents.setter
    def buy160cents(self, value: dict):
        self._property_changed('buy160cents')
        self.__buy160cents = value        

    @property
    def portfolio_id(self) -> dict:
        return self.__portfolio_id

    @portfolio_id.setter
    def portfolio_id(self, value: dict):
        self._property_changed('portfolio_id')
        self.__portfolio_id = value        

    @property
    def z_spread(self) -> dict:
        return self.__z_spread

    @z_spread.setter
    def z_spread(self, value: dict):
        self._property_changed('z_spread')
        self.__z_spread = value        

    @property
    def cap_floor_atm_fwd_rate(self) -> dict:
        return self.__cap_floor_atm_fwd_rate

    @cap_floor_atm_fwd_rate.setter
    def cap_floor_atm_fwd_rate(self, value: dict):
        self._property_changed('cap_floor_atm_fwd_rate')
        self.__cap_floor_atm_fwd_rate = value        

    @property
    def es_percentile(self) -> dict:
        return self.__es_percentile

    @es_percentile.setter
    def es_percentile(self, value: dict):
        self._property_changed('es_percentile')
        self.__es_percentile = value        

    @property
    def tdapi(self) -> dict:
        return self.__tdapi

    @tdapi.setter
    def tdapi(self, value: dict):
        self._property_changed('tdapi')
        self.__tdapi = value        

    @property
    def location_code(self) -> dict:
        return self.__location_code

    @location_code.setter
    def location_code(self, value: dict):
        self._property_changed('location_code')
        self.__location_code = value        

    @property
    def rcic(self) -> dict:
        return self.__rcic

    @rcic.setter
    def rcic(self, value: dict):
        self._property_changed('rcic')
        self.__rcic = value        

    @property
    def name_raw(self) -> dict:
        return self.__name_raw

    @name_raw.setter
    def name_raw(self, value: dict):
        self._property_changed('name_raw')
        self.__name_raw = value        

    @property
    def simon_asset_tags(self) -> dict:
        return self.__simon_asset_tags

    @simon_asset_tags.setter
    def simon_asset_tags(self, value: dict):
        self._property_changed('simon_asset_tags')
        self.__simon_asset_tags = value        

    @property
    def hit_rate_qtd(self) -> dict:
        return self.__hit_rate_qtd

    @hit_rate_qtd.setter
    def hit_rate_qtd(self, value: dict):
        self._property_changed('hit_rate_qtd')
        self.__hit_rate_qtd = value        

    @property
    def primary_volume_in_limit(self) -> dict:
        return self.__primary_volume_in_limit

    @primary_volume_in_limit.setter
    def primary_volume_in_limit(self, value: dict):
        self._property_changed('primary_volume_in_limit')
        self.__primary_volume_in_limit = value        

    @property
    def precipitation_daily_forecast_percent(self) -> dict:
        return self.__precipitation_daily_forecast_percent

    @precipitation_daily_forecast_percent.setter
    def precipitation_daily_forecast_percent(self, value: dict):
        self._property_changed('precipitation_daily_forecast_percent')
        self.__precipitation_daily_forecast_percent = value        

    @property
    def aum_end(self) -> dict:
        return self.__aum_end

    @aum_end.setter
    def aum_end(self, value: dict):
        self._property_changed('aum_end')
        self.__aum_end = value        

    @property
    def premium(self) -> dict:
        return self.__premium

    @premium.setter
    def premium(self, value: dict):
        self._property_changed('premium')
        self.__premium = value        

    @property
    def low(self) -> dict:
        return self.__low

    @low.setter
    def low(self, value: dict):
        self._property_changed('low')
        self.__low = value        

    @property
    def cross_group(self) -> dict:
        return self.__cross_group

    @cross_group.setter
    def cross_group(self, value: dict):
        self._property_changed('cross_group')
        self.__cross_group = value        

    @property
    def five_day_price_change_bps(self) -> dict:
        return self.__five_day_price_change_bps

    @five_day_price_change_bps.setter
    def five_day_price_change_bps(self, value: dict):
        self._property_changed('five_day_price_change_bps')
        self.__five_day_price_change_bps = value        

    @property
    def holdings(self) -> dict:
        return self.__holdings

    @holdings.setter
    def holdings(self, value: dict):
        self._property_changed('holdings')
        self.__holdings = value        

    @property
    def precipitation_daily_forecast(self) -> dict:
        return self.__precipitation_daily_forecast

    @precipitation_daily_forecast.setter
    def precipitation_daily_forecast(self, value: dict):
        self._property_changed('precipitation_daily_forecast')
        self.__precipitation_daily_forecast = value        

    @property
    def price_method(self) -> dict:
        return self.__price_method

    @price_method.setter
    def price_method(self, value: dict):
        self._property_changed('price_method')
        self.__price_method = value        

    @property
    def asset_parameters_fixed_rate_frequency(self) -> dict:
        return self.__asset_parameters_fixed_rate_frequency

    @asset_parameters_fixed_rate_frequency.setter
    def asset_parameters_fixed_rate_frequency(self, value: dict):
        self._property_changed('asset_parameters_fixed_rate_frequency')
        self.__asset_parameters_fixed_rate_frequency = value        

    @property
    def ois_xccy(self) -> dict:
        return self.__ois_xccy

    @ois_xccy.setter
    def ois_xccy(self, value: dict):
        self._property_changed('ois_xccy')
        self.__ois_xccy = value        

    @property
    def days_open(self) -> dict:
        return self.__days_open

    @days_open.setter
    def days_open(self, value: dict):
        self._property_changed('days_open')
        self.__days_open = value        

    @property
    def buy110cents(self) -> dict:
        return self.__buy110cents

    @buy110cents.setter
    def buy110cents(self, value: dict):
        self._property_changed('buy110cents')
        self.__buy110cents = value        

    @property
    def average_spread_bps(self) -> dict:
        return self.__average_spread_bps

    @average_spread_bps.setter
    def average_spread_bps(self, value: dict):
        self._property_changed('average_spread_bps')
        self.__average_spread_bps = value        

    @property
    def buy55cents(self) -> dict:
        return self.__buy55cents

    @buy55cents.setter
    def buy55cents(self, value: dict):
        self._property_changed('buy55cents')
        self.__buy55cents = value        

    @property
    def future_month_q26(self) -> dict:
        return self.__future_month_q26

    @future_month_q26.setter
    def future_month_q26(self, value: dict):
        self._property_changed('future_month_q26')
        self.__future_month_q26 = value        

    @property
    def issue_size(self) -> dict:
        return self.__issue_size

    @issue_size.setter
    def issue_size(self, value: dict):
        self._property_changed('issue_size')
        self.__issue_size = value        

    @property
    def future_month_q25(self) -> dict:
        return self.__future_month_q25

    @future_month_q25.setter
    def future_month_q25(self, value: dict):
        self._property_changed('future_month_q25')
        self.__future_month_q25 = value        

    @property
    def future_month_q24(self) -> dict:
        return self.__future_month_q24

    @future_month_q24.setter
    def future_month_q24(self, value: dict):
        self._property_changed('future_month_q24')
        self.__future_month_q24 = value        

    @property
    def future_month_q23(self) -> dict:
        return self.__future_month_q23

    @future_month_q23.setter
    def future_month_q23(self, value: dict):
        self._property_changed('future_month_q23')
        self.__future_month_q23 = value        

    @property
    def future_month_q22(self) -> dict:
        return self.__future_month_q22

    @future_month_q22.setter
    def future_month_q22(self, value: dict):
        self._property_changed('future_month_q22')
        self.__future_month_q22 = value        

    @property
    def pending_loan_count(self) -> dict:
        return self.__pending_loan_count

    @pending_loan_count.setter
    def pending_loan_count(self, value: dict):
        self._property_changed('pending_loan_count')
        self.__pending_loan_count = value        

    @property
    def future_month_q21(self) -> dict:
        return self.__future_month_q21

    @future_month_q21.setter
    def future_month_q21(self, value: dict):
        self._property_changed('future_month_q21')
        self.__future_month_q21 = value        

    @property
    def price_spot_stop_loss_unit(self) -> dict:
        return self.__price_spot_stop_loss_unit

    @price_spot_stop_loss_unit.setter
    def price_spot_stop_loss_unit(self, value: dict):
        self._property_changed('price_spot_stop_loss_unit')
        self.__price_spot_stop_loss_unit = value        

    @property
    def price_range_in_ticks_description(self) -> dict:
        return self.__price_range_in_ticks_description

    @price_range_in_ticks_description.setter
    def price_range_in_ticks_description(self, value: dict):
        self._property_changed('price_range_in_ticks_description')
        self.__price_range_in_ticks_description = value        

    @property
    def trade_volume(self) -> dict:
        return self.__trade_volume

    @trade_volume.setter
    def trade_volume(self, value: dict):
        self._property_changed('trade_volume')
        self.__trade_volume = value        

    @property
    def primary_country_ric(self) -> dict:
        return self.__primary_country_ric

    @primary_country_ric.setter
    def primary_country_ric(self, value: dict):
        self._property_changed('primary_country_ric')
        self.__primary_country_ric = value        

    @property
    def option_expiration_frequency(self) -> dict:
        return self.__option_expiration_frequency

    @option_expiration_frequency.setter
    def option_expiration_frequency(self, value: dict):
        self._property_changed('option_expiration_frequency')
        self.__option_expiration_frequency = value        

    @property
    def is_active(self) -> dict:
        return self.__is_active

    @is_active.setter
    def is_active(self, value: dict):
        self._property_changed('is_active')
        self.__is_active = value        

    @property
    def use_machine_learning(self) -> dict:
        return self.__use_machine_learning

    @use_machine_learning.setter
    def use_machine_learning(self, value: dict):
        self._property_changed('use_machine_learning')
        self.__use_machine_learning = value        

    @property
    def growth_score(self) -> dict:
        return self.__growth_score

    @growth_score.setter
    def growth_score(self, value: dict):
        self._property_changed('growth_score')
        self.__growth_score = value        

    @property
    def buffer_threshold(self) -> dict:
        return self.__buffer_threshold

    @buffer_threshold.setter
    def buffer_threshold(self, value: dict):
        self._property_changed('buffer_threshold')
        self.__buffer_threshold = value        

    @property
    def buy120cents(self) -> dict:
        return self.__buy120cents

    @buy120cents.setter
    def buy120cents(self, value: dict):
        self._property_changed('buy120cents')
        self.__buy120cents = value        

    @property
    def matched_maturity_swap_rate(self) -> dict:
        return self.__matched_maturity_swap_rate

    @matched_maturity_swap_rate.setter
    def matched_maturity_swap_rate(self, value: dict):
        self._property_changed('matched_maturity_swap_rate')
        self.__matched_maturity_swap_rate = value        

    @property
    def primary_vwap(self) -> dict:
        return self.__primary_vwap

    @primary_vwap.setter
    def primary_vwap(self, value: dict):
        self._property_changed('primary_vwap')
        self.__primary_vwap = value        

    @property
    def exchange_type_id(self) -> dict:
        return self.__exchange_type_id

    @exchange_type_id.setter
    def exchange_type_id(self, value: dict):
        self._property_changed('exchange_type_id')
        self.__exchange_type_id = value        

    @property
    def basis_swap_rate(self) -> dict:
        return self.__basis_swap_rate

    @basis_swap_rate.setter
    def basis_swap_rate(self, value: dict):
        self._property_changed('basis_swap_rate')
        self.__basis_swap_rate = value        

    @property
    def exchange_code(self) -> dict:
        return self.__exchange_code

    @exchange_code.setter
    def exchange_code(self, value: dict):
        self._property_changed('exchange_code')
        self.__exchange_code = value        

    @property
    def group(self) -> dict:
        return self.__group

    @group.setter
    def group(self, value: dict):
        self._property_changed('group')
        self.__group = value        

    @property
    def asset_parameters_termination_date(self) -> dict:
        return self.__asset_parameters_termination_date

    @asset_parameters_termination_date.setter
    def asset_parameters_termination_date(self, value: dict):
        self._property_changed('asset_parameters_termination_date')
        self.__asset_parameters_termination_date = value        

    @property
    def estimated_spread(self) -> dict:
        return self.__estimated_spread

    @estimated_spread.setter
    def estimated_spread(self, value: dict):
        self._property_changed('estimated_spread')
        self.__estimated_spread = value        

    @property
    def yield_change_on_day(self) -> dict:
        return self.__yield_change_on_day

    @yield_change_on_day.setter
    def yield_change_on_day(self, value: dict):
        self._property_changed('yield_change_on_day')
        self.__yield_change_on_day = value        

    @property
    def auto_tags(self) -> dict:
        return self.__auto_tags

    @auto_tags.setter
    def auto_tags(self, value: dict):
        self._property_changed('auto_tags')
        self.__auto_tags = value        

    @property
    def tcm_cost(self) -> dict:
        return self.__tcm_cost

    @tcm_cost.setter
    def tcm_cost(self, value: dict):
        self._property_changed('tcm_cost')
        self.__tcm_cost = value        

    @property
    def sustain_japan(self) -> dict:
        return self.__sustain_japan

    @sustain_japan.setter
    def sustain_japan(self, value: dict):
        self._property_changed('sustain_japan')
        self.__sustain_japan = value        

    @property
    def history_start_date(self) -> dict:
        return self.__history_start_date

    @history_start_date.setter
    def history_start_date(self, value: dict):
        self._property_changed('history_start_date')
        self.__history_start_date = value        

    @property
    def bid_spread(self) -> dict:
        return self.__bid_spread

    @bid_spread.setter
    def bid_spread(self, value: dict):
        self._property_changed('bid_spread')
        self.__bid_spread = value        

    @property
    def percentage_complete(self) -> dict:
        return self.__percentage_complete

    @percentage_complete.setter
    def percentage_complete(self, value: dict):
        self._property_changed('percentage_complete')
        self.__percentage_complete = value        

    @property
    def hedge_tracking_error(self) -> dict:
        return self.__hedge_tracking_error

    @hedge_tracking_error.setter
    def hedge_tracking_error(self, value: dict):
        self._property_changed('hedge_tracking_error')
        self.__hedge_tracking_error = value        

    @property
    def wind_speed_type(self) -> dict:
        return self.__wind_speed_type

    @wind_speed_type.setter
    def wind_speed_type(self, value: dict):
        self._property_changed('wind_speed_type')
        self.__wind_speed_type = value        

    @property
    def strike_price(self) -> dict:
        return self.__strike_price

    @strike_price.setter
    def strike_price(self, value: dict):
        self._property_changed('strike_price')
        self.__strike_price = value        

    @property
    def par_asset_swap_spread12m(self) -> dict:
        return self.__par_asset_swap_spread12m

    @par_asset_swap_spread12m.setter
    def par_asset_swap_spread12m(self, value: dict):
        self._property_changed('par_asset_swap_spread12m')
        self.__par_asset_swap_spread12m = value        

    @property
    def trade_report_id(self) -> dict:
        return self.__trade_report_id

    @trade_report_id.setter
    def trade_report_id(self, value: dict):
        self._property_changed('trade_report_id')
        self.__trade_report_id = value        

    @property
    def adjusted_open_price(self) -> dict:
        return self.__adjusted_open_price

    @adjusted_open_price.setter
    def adjusted_open_price(self, value: dict):
        self._property_changed('adjusted_open_price')
        self.__adjusted_open_price = value        

    @property
    def country_id(self) -> dict:
        return self.__country_id

    @country_id.setter
    def country_id(self, value: dict):
        self._property_changed('country_id')
        self.__country_id = value        

    @property
    def point(self) -> dict:
        return self.__point

    @point.setter
    def point(self, value: dict):
        self._property_changed('point')
        self.__point = value        

    @property
    def pnl_mtd(self) -> dict:
        return self.__pnl_mtd

    @pnl_mtd.setter
    def pnl_mtd(self, value: dict):
        self._property_changed('pnl_mtd')
        self.__pnl_mtd = value        

    @property
    def total_returns(self) -> dict:
        return self.__total_returns

    @total_returns.setter
    def total_returns(self, value: dict):
        self._property_changed('total_returns')
        self.__total_returns = value        

    @property
    def lender(self) -> dict:
        return self.__lender

    @lender.setter
    def lender(self, value: dict):
        self._property_changed('lender')
        self.__lender = value        

    @property
    def ann_return1_year(self) -> dict:
        return self.__ann_return1_year

    @ann_return1_year.setter
    def ann_return1_year(self, value: dict):
        self._property_changed('ann_return1_year')
        self.__ann_return1_year = value        

    @property
    def ctd_fwd_dv01(self) -> dict:
        return self.__ctd_fwd_dv01

    @ctd_fwd_dv01.setter
    def ctd_fwd_dv01(self, value: dict):
        self._property_changed('ctd_fwd_dv01')
        self.__ctd_fwd_dv01 = value        

    @property
    def eff_yield7_day(self) -> dict:
        return self.__eff_yield7_day

    @eff_yield7_day.setter
    def eff_yield7_day(self, value: dict):
        self._property_changed('eff_yield7_day')
        self.__eff_yield7_day = value        

    @property
    def meeting_date(self) -> dict:
        return self.__meeting_date

    @meeting_date.setter
    def meeting_date(self, value: dict):
        self._property_changed('meeting_date')
        self.__meeting_date = value        

    @property
    def calendar_spread_mispricing(self) -> dict:
        return self.__calendar_spread_mispricing

    @calendar_spread_mispricing.setter
    def calendar_spread_mispricing(self, value: dict):
        self._property_changed('calendar_spread_mispricing')
        self.__calendar_spread_mispricing = value        

    @property
    def buy140cents(self) -> dict:
        return self.__buy140cents

    @buy140cents.setter
    def buy140cents(self, value: dict):
        self._property_changed('buy140cents')
        self.__buy140cents = value        

    @property
    def price_notation2_type(self) -> dict:
        return self.__price_notation2_type

    @price_notation2_type.setter
    def price_notation2_type(self, value: dict):
        self._property_changed('price_notation2_type')
        self.__price_notation2_type = value        

    @property
    def fund_focus(self) -> dict:
        return self.__fund_focus

    @fund_focus.setter
    def fund_focus(self, value: dict):
        self._property_changed('fund_focus')
        self.__fund_focus = value        

    @property
    def relative_strike(self) -> dict:
        return self.__relative_strike

    @relative_strike.setter
    def relative_strike(self, value: dict):
        self._property_changed('relative_strike')
        self.__relative_strike = value        

    @property
    def flagship(self) -> dict:
        return self.__flagship

    @flagship.setter
    def flagship(self, value: dict):
        self._property_changed('flagship')
        self.__flagship = value        

    @property
    def additional_price_notation(self) -> dict:
        return self.__additional_price_notation

    @additional_price_notation.setter
    def additional_price_notation(self, value: dict):
        self._property_changed('additional_price_notation')
        self.__additional_price_notation = value        

    @property
    def factor_category(self) -> dict:
        return self.__factor_category

    @factor_category.setter
    def factor_category(self, value: dict):
        self._property_changed('factor_category')
        self.__factor_category = value        

    @property
    def equity_delta(self) -> dict:
        return self.__equity_delta

    @equity_delta.setter
    def equity_delta(self, value: dict):
        self._property_changed('equity_delta')
        self.__equity_delta = value        

    @property
    def gross_weight(self) -> dict:
        return self.__gross_weight

    @gross_weight.setter
    def gross_weight(self, value: dict):
        self._property_changed('gross_weight')
        self.__gross_weight = value        

    @property
    def listed(self) -> dict:
        return self.__listed

    @listed.setter
    def listed(self, value: dict):
        self._property_changed('listed')
        self.__listed = value        

    @property
    def sell7bps(self) -> dict:
        return self.__sell7bps

    @sell7bps.setter
    def sell7bps(self, value: dict):
        self._property_changed('sell7bps')
        self.__sell7bps = value        

    @property
    def earnings_record_type(self) -> dict:
        return self.__earnings_record_type

    @earnings_record_type.setter
    def earnings_record_type(self, value: dict):
        self._property_changed('earnings_record_type')
        self.__earnings_record_type = value        

    @property
    def mean(self) -> dict:
        return self.__mean

    @mean.setter
    def mean(self, value: dict):
        self._property_changed('mean')
        self.__mean = value        

    @property
    def ask_yield(self) -> dict:
        return self.__ask_yield

    @ask_yield.setter
    def ask_yield(self, value: dict):
        self._property_changed('ask_yield')
        self.__ask_yield = value        

    @property
    def shock_style(self) -> dict:
        return self.__shock_style

    @shock_style.setter
    def shock_style(self, value: dict):
        self._property_changed('shock_style')
        self.__shock_style = value        

    @property
    def methodology(self) -> dict:
        return self.__methodology

    @methodology.setter
    def methodology(self, value: dict):
        self._property_changed('methodology')
        self.__methodology = value        

    @property
    def buy25cents(self) -> dict:
        return self.__buy25cents

    @buy25cents.setter
    def buy25cents(self, value: dict):
        self._property_changed('buy25cents')
        self.__buy25cents = value        

    @property
    def amount_outstanding(self) -> dict:
        return self.__amount_outstanding

    @amount_outstanding.setter
    def amount_outstanding(self, value: dict):
        self._property_changed('amount_outstanding')
        self.__amount_outstanding = value        

    @property
    def market_pnl(self) -> dict:
        return self.__market_pnl

    @market_pnl.setter
    def market_pnl(self, value: dict):
        self._property_changed('market_pnl')
        self.__market_pnl = value        

    @property
    def sustain_asia_ex_japan(self) -> dict:
        return self.__sustain_asia_ex_japan

    @sustain_asia_ex_japan.setter
    def sustain_asia_ex_japan(self, value: dict):
        self._property_changed('sustain_asia_ex_japan')
        self.__sustain_asia_ex_japan = value        

    @property
    def sell6point5bps(self) -> dict:
        return self.__sell6point5bps

    @sell6point5bps.setter
    def sell6point5bps(self, value: dict):
        self._property_changed('sell6point5bps')
        self.__sell6point5bps = value        

    @property
    def neighbour_asset_id(self) -> dict:
        return self.__neighbour_asset_id

    @neighbour_asset_id.setter
    def neighbour_asset_id(self, value: dict):
        self._property_changed('neighbour_asset_id')
        self.__neighbour_asset_id = value        

    @property
    def count_ideas_ytd(self) -> dict:
        return self.__count_ideas_ytd

    @count_ideas_ytd.setter
    def count_ideas_ytd(self, value: dict):
        self._property_changed('count_ideas_ytd')
        self.__count_ideas_ytd = value        

    @property
    def simon_intl_asset_tags(self) -> dict:
        return self.__simon_intl_asset_tags

    @simon_intl_asset_tags.setter
    def simon_intl_asset_tags(self, value: dict):
        self._property_changed('simon_intl_asset_tags')
        self.__simon_intl_asset_tags = value        

    @property
    def path(self) -> dict:
        return self.__path

    @path.setter
    def path(self, value: dict):
        self._property_changed('path')
        self.__path = value        

    @property
    def vwap_unrealized_cash(self) -> dict:
        return self.__vwap_unrealized_cash

    @vwap_unrealized_cash.setter
    def vwap_unrealized_cash(self, value: dict):
        self._property_changed('vwap_unrealized_cash')
        self.__vwap_unrealized_cash = value        

    @property
    def payoff_mtd(self) -> dict:
        return self.__payoff_mtd

    @payoff_mtd.setter
    def payoff_mtd(self, value: dict):
        self._property_changed('payoff_mtd')
        self.__payoff_mtd = value        

    @property
    def bos_in_bps_label(self) -> tuple:
        return self.__bos_in_bps_label

    @bos_in_bps_label.setter
    def bos_in_bps_label(self, value: tuple):
        self._property_changed('bos_in_bps_label')
        self.__bos_in_bps_label = value        

    @property
    def bos_in_bps(self) -> dict:
        return self.__bos_in_bps

    @bos_in_bps.setter
    def bos_in_bps(self, value: dict):
        self._property_changed('bos_in_bps')
        self.__bos_in_bps = value        

    @property
    def point_class(self) -> dict:
        return self.__point_class

    @point_class.setter
    def point_class(self, value: dict):
        self._property_changed('point_class')
        self.__point_class = value        

    @property
    def fx_spot(self) -> dict:
        return self.__fx_spot

    @fx_spot.setter
    def fx_spot(self, value: dict):
        self._property_changed('fx_spot')
        self.__fx_spot = value        

    @property
    def restrict_named_individuals(self) -> dict:
        return self.__restrict_named_individuals

    @restrict_named_individuals.setter
    def restrict_named_individuals(self, value: dict):
        self._property_changed('restrict_named_individuals')
        self.__restrict_named_individuals = value        

    @property
    def hedge_volatility(self) -> dict:
        return self.__hedge_volatility

    @hedge_volatility.setter
    def hedge_volatility(self, value: dict):
        self._property_changed('hedge_volatility')
        self.__hedge_volatility = value        

    @property
    def tags(self) -> dict:
        return self.__tags

    @tags.setter
    def tags(self, value: dict):
        self._property_changed('tags')
        self.__tags = value        

    @property
    def population(self) -> dict:
        return self.__population

    @population.setter
    def population(self, value: dict):
        self._property_changed('population')
        self.__population = value        

    @property
    def underlying_asset_id(self) -> dict:
        return self.__underlying_asset_id

    @underlying_asset_id.setter
    def underlying_asset_id(self, value: dict):
        self._property_changed('underlying_asset_id')
        self.__underlying_asset_id = value        

    @property
    def real_long_rates_contribution(self) -> dict:
        return self.__real_long_rates_contribution

    @real_long_rates_contribution.setter
    def real_long_rates_contribution(self, value: dict):
        self._property_changed('real_long_rates_contribution')
        self.__real_long_rates_contribution = value        

    @property
    def pctprices_return(self) -> dict:
        return self.__pctprices_return

    @pctprices_return.setter
    def pctprices_return(self, value: dict):
        self._property_changed('pctprices_return')
        self.__pctprices_return = value        

    @property
    def domain(self) -> dict:
        return self.__domain

    @domain.setter
    def domain(self, value: dict):
        self._property_changed('domain')
        self.__domain = value        

    @property
    def buy80cents(self) -> dict:
        return self.__buy80cents

    @buy80cents.setter
    def buy80cents(self, value: dict):
        self._property_changed('buy80cents')
        self.__buy80cents = value        

    @property
    def forward_tenor(self) -> dict:
        return self.__forward_tenor

    @forward_tenor.setter
    def forward_tenor(self, value: dict):
        self._property_changed('forward_tenor')
        self.__forward_tenor = value        

    @property
    def average_price(self) -> dict:
        return self.__average_price

    @average_price.setter
    def average_price(self, value: dict):
        self._property_changed('average_price')
        self.__average_price = value        

    @property
    def target_price_realized_bps(self) -> dict:
        return self.__target_price_realized_bps

    @target_price_realized_bps.setter
    def target_price_realized_bps(self, value: dict):
        self._property_changed('target_price_realized_bps')
        self.__target_price_realized_bps = value        

    @property
    def leg2_fixed_rate(self) -> dict:
        return self.__leg2_fixed_rate

    @leg2_fixed_rate.setter
    def leg2_fixed_rate(self, value: dict):
        self._property_changed('leg2_fixed_rate')
        self.__leg2_fixed_rate = value        

    @property
    def share_class_assets(self) -> dict:
        return self.__share_class_assets

    @share_class_assets.setter
    def share_class_assets(self, value: dict):
        self._property_changed('share_class_assets')
        self.__share_class_assets = value        

    @property
    def annuity(self) -> dict:
        return self.__annuity

    @annuity.setter
    def annuity(self, value: dict):
        self._property_changed('annuity')
        self.__annuity = value        

    @property
    def total_count(self) -> dict:
        return self.__total_count

    @total_count.setter
    def total_count(self, value: dict):
        self._property_changed('total_count')
        self.__total_count = value        

    @property
    def quote_type(self) -> dict:
        return self.__quote_type

    @quote_type.setter
    def quote_type(self, value: dict):
        self._property_changed('quote_type')
        self.__quote_type = value        

    @property
    def corporate_action_status(self) -> dict:
        return self.__corporate_action_status

    @corporate_action_status.setter
    def corporate_action_status(self, value: dict):
        self._property_changed('corporate_action_status')
        self.__corporate_action_status = value        

    @property
    def pegged_tip_size(self) -> dict:
        return self.__pegged_tip_size

    @pegged_tip_size.setter
    def pegged_tip_size(self, value: dict):
        self._property_changed('pegged_tip_size')
        self.__pegged_tip_size = value        

    @property
    def uid(self) -> dict:
        return self.__uid

    @uid.setter
    def uid(self, value: dict):
        self._property_changed('uid')
        self.__uid = value        

    @property
    def es_policy_percentile(self) -> dict:
        return self.__es_policy_percentile

    @es_policy_percentile.setter
    def es_policy_percentile(self, value: dict):
        self._property_changed('es_policy_percentile')
        self.__es_policy_percentile = value        

    @property
    def usd_ois(self) -> dict:
        return self.__usd_ois

    @usd_ois.setter
    def usd_ois(self, value: dict):
        self._property_changed('usd_ois')
        self.__usd_ois = value        

    @property
    def term(self) -> dict:
        return self.__term

    @term.setter
    def term(self, value: dict):
        self._property_changed('term')
        self.__term = value        

    @property
    def restrict_internal_gs_ntk(self) -> dict:
        return self.__restrict_internal_gs_ntk

    @restrict_internal_gs_ntk.setter
    def restrict_internal_gs_ntk(self, value: dict):
        self._property_changed('restrict_internal_gs_ntk')
        self.__restrict_internal_gs_ntk = value        

    @property
    def tcm_cost_participation_rate100_pct(self) -> dict:
        return self.__tcm_cost_participation_rate100_pct

    @tcm_cost_participation_rate100_pct.setter
    def tcm_cost_participation_rate100_pct(self, value: dict):
        self._property_changed('tcm_cost_participation_rate100_pct')
        self.__tcm_cost_participation_rate100_pct = value        

    @property
    def relative_universe(self) -> dict:
        return self.__relative_universe

    @relative_universe.setter
    def relative_universe(self, value: dict):
        self._property_changed('relative_universe')
        self.__relative_universe = value        

    @property
    def measure_idx(self) -> dict:
        return self.__measure_idx

    @measure_idx.setter
    def measure_idx(self, value: dict):
        self._property_changed('measure_idx')
        self.__measure_idx = value        

    @property
    def fred_id(self) -> dict:
        return self.__fred_id

    @fred_id.setter
    def fred_id(self, value: dict):
        self._property_changed('fred_id')
        self.__fred_id = value        

    @property
    def twi_contribution(self) -> dict:
        return self.__twi_contribution

    @twi_contribution.setter
    def twi_contribution(self, value: dict):
        self._property_changed('twi_contribution')
        self.__twi_contribution = value        

    @property
    def cloud_cover_type(self) -> dict:
        return self.__cloud_cover_type

    @cloud_cover_type.setter
    def cloud_cover_type(self, value: dict):
        self._property_changed('cloud_cover_type')
        self.__cloud_cover_type = value        

    @property
    def delisted(self) -> dict:
        return self.__delisted

    @delisted.setter
    def delisted(self, value: dict):
        self._property_changed('delisted')
        self.__delisted = value        

    @property
    def regional_focus(self) -> dict:
        return self.__regional_focus

    @regional_focus.setter
    def regional_focus(self, value: dict):
        self._property_changed('regional_focus')
        self.__regional_focus = value        

    @property
    def volume_primary(self) -> dict:
        return self.__volume_primary

    @volume_primary.setter
    def volume_primary(self, value: dict):
        self._property_changed('volume_primary')
        self.__volume_primary = value        

    @property
    def asset_parameters_payer_designated_maturity(self) -> dict:
        return self.__asset_parameters_payer_designated_maturity

    @asset_parameters_payer_designated_maturity.setter
    def asset_parameters_payer_designated_maturity(self, value: dict):
        self._property_changed('asset_parameters_payer_designated_maturity')
        self.__asset_parameters_payer_designated_maturity = value        

    @property
    def buy30cents(self) -> dict:
        return self.__buy30cents

    @buy30cents.setter
    def buy30cents(self, value: dict):
        self._property_changed('buy30cents')
        self.__buy30cents = value        

    @property
    def funding_bid_price(self) -> dict:
        return self.__funding_bid_price

    @funding_bid_price.setter
    def funding_bid_price(self, value: dict):
        self._property_changed('funding_bid_price')
        self.__funding_bid_price = value        

    @property
    def series(self) -> dict:
        return self.__series

    @series.setter
    def series(self, value: dict):
        self._property_changed('series')
        self.__series = value        

    @property
    def sell3bps(self) -> dict:
        return self.__sell3bps

    @sell3bps.setter
    def sell3bps(self, value: dict):
        self._property_changed('sell3bps')
        self.__sell3bps = value        

    @property
    def settlement_price(self) -> dict:
        return self.__settlement_price

    @settlement_price.setter
    def settlement_price(self, value: dict):
        self._property_changed('settlement_price')
        self.__settlement_price = value        

    @property
    def quarter(self) -> dict:
        return self.__quarter

    @quarter.setter
    def quarter(self, value: dict):
        self._property_changed('quarter')
        self.__quarter = value        

    @property
    def sell18bps(self) -> dict:
        return self.__sell18bps

    @sell18bps.setter
    def sell18bps(self, value: dict):
        self._property_changed('sell18bps')
        self.__sell18bps = value        

    @property
    def asset_parameters_floating_rate_option(self) -> dict:
        return self.__asset_parameters_floating_rate_option

    @asset_parameters_floating_rate_option.setter
    def asset_parameters_floating_rate_option(self, value: dict):
        self._property_changed('asset_parameters_floating_rate_option')
        self.__asset_parameters_floating_rate_option = value        

    @property
    def realized_vwap_performance_bps(self) -> dict:
        return self.__realized_vwap_performance_bps

    @realized_vwap_performance_bps.setter
    def realized_vwap_performance_bps(self, value: dict):
        self._property_changed('realized_vwap_performance_bps')
        self.__realized_vwap_performance_bps = value        

    @property
    def vote_share(self) -> dict:
        return self.__vote_share

    @vote_share.setter
    def vote_share(self, value: dict):
        self._property_changed('vote_share')
        self.__vote_share = value        

    @property
    def servicing_cost_short_pnl(self) -> dict:
        return self.__servicing_cost_short_pnl

    @servicing_cost_short_pnl.setter
    def servicing_cost_short_pnl(self, value: dict):
        self._property_changed('servicing_cost_short_pnl')
        self.__servicing_cost_short_pnl = value        

    @property
    def total_confirmed(self) -> dict:
        return self.__total_confirmed

    @total_confirmed.setter
    def total_confirmed(self, value: dict):
        self._property_changed('total_confirmed')
        self.__total_confirmed = value        

    @property
    def economic_forecast(self) -> dict:
        return self.__economic_forecast

    @economic_forecast.setter
    def economic_forecast(self, value: dict):
        self._property_changed('economic_forecast')
        self.__economic_forecast = value        

    @property
    def plot_id(self) -> dict:
        return self.__plot_id

    @plot_id.setter
    def plot_id(self, value: dict):
        self._property_changed('plot_id')
        self.__plot_id = value        

    @property
    def cluster_description(self) -> dict:
        return self.__cluster_description

    @cluster_description.setter
    def cluster_description(self, value: dict):
        self._property_changed('cluster_description')
        self.__cluster_description = value        

    @property
    def concentration_limit(self) -> dict:
        return self.__concentration_limit

    @concentration_limit.setter
    def concentration_limit(self, value: dict):
        self._property_changed('concentration_limit')
        self.__concentration_limit = value        

    @property
    def wind_speed(self) -> dict:
        return self.__wind_speed

    @wind_speed.setter
    def wind_speed(self, value: dict):
        self._property_changed('wind_speed')
        self.__wind_speed = value        

    @property
    def observation_hour(self) -> dict:
        return self.__observation_hour

    @observation_hour.setter
    def observation_hour(self, value: dict):
        self._property_changed('observation_hour')
        self.__observation_hour = value        

    @property
    def signal(self) -> dict:
        return self.__signal

    @signal.setter
    def signal(self, value: dict):
        self._property_changed('signal')
        self.__signal = value        

    @property
    def borrower_id(self) -> dict:
        return self.__borrower_id

    @borrower_id.setter
    def borrower_id(self, value: dict):
        self._property_changed('borrower_id')
        self.__borrower_id = value        

    @property
    def data_product(self) -> dict:
        return self.__data_product

    @data_product.setter
    def data_product(self, value: dict):
        self._property_changed('data_product')
        self.__data_product = value        

    @property
    def buy7point5bps(self) -> dict:
        return self.__buy7point5bps

    @buy7point5bps.setter
    def buy7point5bps(self, value: dict):
        self._property_changed('buy7point5bps')
        self.__buy7point5bps = value        

    @property
    def limit_price(self) -> dict:
        return self.__limit_price

    @limit_price.setter
    def limit_price(self, value: dict):
        self._property_changed('limit_price')
        self.__limit_price = value        

    @property
    def bm_prime_id(self) -> dict:
        return self.__bm_prime_id

    @bm_prime_id.setter
    def bm_prime_id(self, value: dict):
        self._property_changed('bm_prime_id')
        self.__bm_prime_id = value        

    @property
    def data_type(self) -> dict:
        return self.__data_type

    @data_type.setter
    def data_type(self, value: dict):
        self._property_changed('data_type')
        self.__data_type = value        

    @property
    def count(self) -> dict:
        return self.__count

    @count.setter
    def count(self, value: dict):
        self._property_changed('count')
        self.__count = value        

    @property
    def conviction(self) -> dict:
        return self.__conviction

    @conviction.setter
    def conviction(self, value: dict):
        self._property_changed('conviction')
        self.__conviction = value        

    @property
    def rfqstate(self) -> dict:
        return self.__rfqstate

    @rfqstate.setter
    def rfqstate(self, value: dict):
        self._property_changed('rfqstate')
        self.__rfqstate = value        

    @property
    def benchmark_maturity(self) -> dict:
        return self.__benchmark_maturity

    @benchmark_maturity.setter
    def benchmark_maturity(self, value: dict):
        self._property_changed('benchmark_maturity')
        self.__benchmark_maturity = value        

    @property
    def gross_flow_normalized(self) -> dict:
        return self.__gross_flow_normalized

    @gross_flow_normalized.setter
    def gross_flow_normalized(self, value: dict):
        self._property_changed('gross_flow_normalized')
        self.__gross_flow_normalized = value        

    @property
    def buy14bps(self) -> dict:
        return self.__buy14bps

    @buy14bps.setter
    def buy14bps(self, value: dict):
        self._property_changed('buy14bps')
        self.__buy14bps = value        

    @property
    def factor_id(self) -> dict:
        return self.__factor_id

    @factor_id.setter
    def factor_id(self, value: dict):
        self._property_changed('factor_id')
        self.__factor_id = value        

    @property
    def future_month_v26(self) -> dict:
        return self.__future_month_v26

    @future_month_v26.setter
    def future_month_v26(self, value: dict):
        self._property_changed('future_month_v26')
        self.__future_month_v26 = value        

    @property
    def sts_fx_currency(self) -> dict:
        return self.__sts_fx_currency

    @sts_fx_currency.setter
    def sts_fx_currency(self, value: dict):
        self._property_changed('sts_fx_currency')
        self.__sts_fx_currency = value        

    @property
    def future_month_v25(self) -> dict:
        return self.__future_month_v25

    @future_month_v25.setter
    def future_month_v25(self, value: dict):
        self._property_changed('future_month_v25')
        self.__future_month_v25 = value        

    @property
    def bid_change(self) -> dict:
        return self.__bid_change

    @bid_change.setter
    def bid_change(self, value: dict):
        self._property_changed('bid_change')
        self.__bid_change = value        

    @property
    def month(self) -> dict:
        return self.__month

    @month.setter
    def month(self, value: dict):
        self._property_changed('month')
        self.__month = value        

    @property
    def future_month_v24(self) -> dict:
        return self.__future_month_v24

    @future_month_v24.setter
    def future_month_v24(self, value: dict):
        self._property_changed('future_month_v24')
        self.__future_month_v24 = value        

    @property
    def investment_wtd(self) -> dict:
        return self.__investment_wtd

    @investment_wtd.setter
    def investment_wtd(self, value: dict):
        self._property_changed('investment_wtd')
        self.__investment_wtd = value        

    @property
    def future_month_v23(self) -> dict:
        return self.__future_month_v23

    @future_month_v23.setter
    def future_month_v23(self, value: dict):
        self._property_changed('future_month_v23')
        self.__future_month_v23 = value        

    @property
    def future_month_v22(self) -> dict:
        return self.__future_month_v22

    @future_month_v22.setter
    def future_month_v22(self, value: dict):
        self._property_changed('future_month_v22')
        self.__future_month_v22 = value        

    @property
    def future_month_v21(self) -> dict:
        return self.__future_month_v21

    @future_month_v21.setter
    def future_month_v21(self, value: dict):
        self._property_changed('future_month_v21')
        self.__future_month_v21 = value        

    @property
    def expiration(self) -> dict:
        return self.__expiration

    @expiration.setter
    def expiration(self, value: dict):
        self._property_changed('expiration')
        self.__expiration = value        

    @property
    def leg2_reset_frequency(self) -> dict:
        return self.__leg2_reset_frequency

    @leg2_reset_frequency.setter
    def leg2_reset_frequency(self, value: dict):
        self._property_changed('leg2_reset_frequency')
        self.__leg2_reset_frequency = value        

    @property
    def controversy_score(self) -> dict:
        return self.__controversy_score

    @controversy_score.setter
    def controversy_score(self, value: dict):
        self._property_changed('controversy_score')
        self.__controversy_score = value        

    @property
    def proceed_asset_swap_spread(self) -> dict:
        return self.__proceed_asset_swap_spread

    @proceed_asset_swap_spread.setter
    def proceed_asset_swap_spread(self, value: dict):
        self._property_changed('proceed_asset_swap_spread')
        self.__proceed_asset_swap_spread = value        

    @property
    def concentration_level(self) -> dict:
        return self.__concentration_level

    @concentration_level.setter
    def concentration_level(self, value: dict):
        self._property_changed('concentration_level')
        self.__concentration_level = value        

    @property
    def importance(self) -> dict:
        return self.__importance

    @importance.setter
    def importance(self, value: dict):
        self._property_changed('importance')
        self.__importance = value        

    @property
    def asset_classifications_gics_sector(self) -> dict:
        return self.__asset_classifications_gics_sector

    @asset_classifications_gics_sector.setter
    def asset_classifications_gics_sector(self, value: dict):
        self._property_changed('asset_classifications_gics_sector')
        self.__asset_classifications_gics_sector = value        

    @property
    def sts_asset_name(self) -> dict:
        return self.__sts_asset_name

    @sts_asset_name.setter
    def sts_asset_name(self, value: dict):
        self._property_changed('sts_asset_name')
        self.__sts_asset_name = value        

    @property
    def net_exposure_classification(self) -> dict:
        return self.__net_exposure_classification

    @net_exposure_classification.setter
    def net_exposure_classification(self, value: dict):
        self._property_changed('net_exposure_classification')
        self.__net_exposure_classification = value        

    @property
    def settlement_method(self) -> dict:
        return self.__settlement_method

    @settlement_method.setter
    def settlement_method(self, value: dict):
        self._property_changed('settlement_method')
        self.__settlement_method = value        

    @property
    def receiver_designated_maturity(self) -> dict:
        return self.__receiver_designated_maturity

    @receiver_designated_maturity.setter
    def receiver_designated_maturity(self, value: dict):
        self._property_changed('receiver_designated_maturity')
        self.__receiver_designated_maturity = value        

    @property
    def title(self) -> dict:
        return self.__title

    @title.setter
    def title(self, value: dict):
        self._property_changed('title')
        self.__title = value        

    @property
    def x_ref_type_id(self) -> dict:
        return self.__x_ref_type_id

    @x_ref_type_id.setter
    def x_ref_type_id(self, value: dict):
        self._property_changed('x_ref_type_id')
        self.__x_ref_type_id = value        

    @property
    def duration(self) -> dict:
        return self.__duration

    @duration.setter
    def duration(self, value: dict):
        self._property_changed('duration')
        self.__duration = value        

    @property
    def load(self) -> dict:
        return self.__load

    @load.setter
    def load(self, value: dict):
        self._property_changed('load')
        self.__load = value        

    @property
    def alpha(self) -> dict:
        return self.__alpha

    @alpha.setter
    def alpha(self, value: dict):
        self._property_changed('alpha')
        self.__alpha = value        

    @property
    def company(self) -> dict:
        return self.__company

    @company.setter
    def company(self, value: dict):
        self._property_changed('company')
        self.__company = value        

    @property
    def settlement_frequency(self) -> dict:
        return self.__settlement_frequency

    @settlement_frequency.setter
    def settlement_frequency(self, value: dict):
        self._property_changed('settlement_frequency')
        self.__settlement_frequency = value        

    @property
    def dist_avg7_day(self) -> dict:
        return self.__dist_avg7_day

    @dist_avg7_day.setter
    def dist_avg7_day(self, value: dict):
        self._property_changed('dist_avg7_day')
        self.__dist_avg7_day = value        

    @property
    def in_risk_model(self) -> dict:
        return self.__in_risk_model

    @in_risk_model.setter
    def in_risk_model(self, value: dict):
        self._property_changed('in_risk_model')
        self.__in_risk_model = value        

    @property
    def daily_net_shareholder_flows_percent(self) -> dict:
        return self.__daily_net_shareholder_flows_percent

    @daily_net_shareholder_flows_percent.setter
    def daily_net_shareholder_flows_percent(self, value: dict):
        self._property_changed('daily_net_shareholder_flows_percent')
        self.__daily_net_shareholder_flows_percent = value        

    @property
    def filled_notional_local(self) -> dict:
        return self.__filled_notional_local

    @filled_notional_local.setter
    def filled_notional_local(self, value: dict):
        self._property_changed('filled_notional_local')
        self.__filled_notional_local = value        

    @property
    def ever_hospitalized(self) -> dict:
        return self.__ever_hospitalized

    @ever_hospitalized.setter
    def ever_hospitalized(self, value: dict):
        self._property_changed('ever_hospitalized')
        self.__ever_hospitalized = value        

    @property
    def meeting_number(self) -> dict:
        return self.__meeting_number

    @meeting_number.setter
    def meeting_number(self, value: dict):
        self._property_changed('meeting_number')
        self.__meeting_number = value        

    @property
    def mid_gspread(self) -> dict:
        return self.__mid_gspread

    @mid_gspread.setter
    def mid_gspread(self, value: dict):
        self._property_changed('mid_gspread')
        self.__mid_gspread = value        

    @property
    def days_open_unrealized_bps(self) -> dict:
        return self.__days_open_unrealized_bps

    @days_open_unrealized_bps.setter
    def days_open_unrealized_bps(self, value: dict):
        self._property_changed('days_open_unrealized_bps')
        self.__days_open_unrealized_bps = value        

    @property
    def long_level(self) -> dict:
        return self.__long_level

    @long_level.setter
    def long_level(self, value: dict):
        self._property_changed('long_level')
        self.__long_level = value        

    @property
    def data_description(self) -> dict:
        return self.__data_description

    @data_description.setter
    def data_description(self, value: dict):
        self._property_changed('data_description')
        self.__data_description = value        

    @property
    def temperature_type(self) -> dict:
        return self.__temperature_type

    @temperature_type.setter
    def temperature_type(self, value: dict):
        self._property_changed('temperature_type')
        self.__temperature_type = value        

    @property
    def gsideid(self) -> dict:
        return self.__gsideid

    @gsideid.setter
    def gsideid(self, value: dict):
        self._property_changed('gsideid')
        self.__gsideid = value        

    @property
    def repo_rate(self) -> dict:
        return self.__repo_rate

    @repo_rate.setter
    def repo_rate(self, value: dict):
        self._property_changed('repo_rate')
        self.__repo_rate = value        

    @property
    def division(self) -> dict:
        return self.__division

    @division.setter
    def division(self, value: dict):
        self._property_changed('division')
        self.__division = value        

    @property
    def cloud_cover_daily_forecast(self) -> dict:
        return self.__cloud_cover_daily_forecast

    @cloud_cover_daily_forecast.setter
    def cloud_cover_daily_forecast(self, value: dict):
        self._property_changed('cloud_cover_daily_forecast')
        self.__cloud_cover_daily_forecast = value        

    @property
    def wind_speed_daily_forecast(self) -> dict:
        return self.__wind_speed_daily_forecast

    @wind_speed_daily_forecast.setter
    def wind_speed_daily_forecast(self, value: dict):
        self._property_changed('wind_speed_daily_forecast')
        self.__wind_speed_daily_forecast = value        

    @property
    def asset_parameters_floating_rate_day_count_fraction(self) -> dict:
        return self.__asset_parameters_floating_rate_day_count_fraction

    @asset_parameters_floating_rate_day_count_fraction.setter
    def asset_parameters_floating_rate_day_count_fraction(self, value: dict):
        self._property_changed('asset_parameters_floating_rate_day_count_fraction')
        self.__asset_parameters_floating_rate_day_count_fraction = value        

    @property
    def trade_action(self) -> dict:
        return self.__trade_action

    @trade_action.setter
    def trade_action(self, value: dict):
        self._property_changed('trade_action')
        self.__trade_action = value        

    @property
    def action(self) -> dict:
        return self.__action

    @action.setter
    def action(self, value: dict):
        self._property_changed('action')
        self.__action = value        

    @property
    def ctd_yield(self) -> dict:
        return self.__ctd_yield

    @ctd_yield.setter
    def ctd_yield(self, value: dict):
        self._property_changed('ctd_yield')
        self.__ctd_yield = value        

    @property
    def arrival_haircut_vwap_normalized(self) -> dict:
        return self.__arrival_haircut_vwap_normalized

    @arrival_haircut_vwap_normalized.setter
    def arrival_haircut_vwap_normalized(self, value: dict):
        self._property_changed('arrival_haircut_vwap_normalized')
        self.__arrival_haircut_vwap_normalized = value        

    @property
    def price_component(self) -> dict:
        return self.__price_component

    @price_component.setter
    def price_component(self, value: dict):
        self._property_changed('price_component')
        self.__price_component = value        

    @property
    def queue_clock_time_description(self) -> dict:
        return self.__queue_clock_time_description

    @queue_clock_time_description.setter
    def queue_clock_time_description(self, value: dict):
        self._property_changed('queue_clock_time_description')
        self.__queue_clock_time_description = value        

    @property
    def asset_parameters_receiver_day_count_fraction(self) -> dict:
        return self.__asset_parameters_receiver_day_count_fraction

    @asset_parameters_receiver_day_count_fraction.setter
    def asset_parameters_receiver_day_count_fraction(self, value: dict):
        self._property_changed('asset_parameters_receiver_day_count_fraction')
        self.__asset_parameters_receiver_day_count_fraction = value        

    @property
    def percent_mid_execution_quantity(self) -> dict:
        return self.__percent_mid_execution_quantity

    @percent_mid_execution_quantity.setter
    def percent_mid_execution_quantity(self, value: dict):
        self._property_changed('percent_mid_execution_quantity')
        self.__percent_mid_execution_quantity = value        

    @property
    def delta_strike(self) -> dict:
        return self.__delta_strike

    @delta_strike.setter
    def delta_strike(self, value: dict):
        self._property_changed('delta_strike')
        self.__delta_strike = value        

    @property
    def cloud_cover(self) -> dict:
        return self.__cloud_cover

    @cloud_cover.setter
    def cloud_cover(self, value: dict):
        self._property_changed('cloud_cover')
        self.__cloud_cover = value        

    @property
    def asset_parameters_notional_currency(self) -> dict:
        return self.__asset_parameters_notional_currency

    @asset_parameters_notional_currency.setter
    def asset_parameters_notional_currency(self, value: dict):
        self._property_changed('asset_parameters_notional_currency')
        self.__asset_parameters_notional_currency = value        

    @property
    def buy18bps(self) -> dict:
        return self.__buy18bps

    @buy18bps.setter
    def buy18bps(self, value: dict):
        self._property_changed('buy18bps')
        self.__buy18bps = value        

    @property
    def value_actual(self) -> dict:
        return self.__value_actual

    @value_actual.setter
    def value_actual(self, value: dict):
        self._property_changed('value_actual')
        self.__value_actual = value        

    @property
    def upi(self) -> dict:
        return self.__upi

    @upi.setter
    def upi(self, value: dict):
        self._property_changed('upi')
        self.__upi = value        

    @property
    def collateral_currency(self) -> dict:
        return self.__collateral_currency

    @collateral_currency.setter
    def collateral_currency(self, value: dict):
        self._property_changed('collateral_currency')
        self.__collateral_currency = value        

    @property
    def original_country(self) -> dict:
        return self.__original_country

    @original_country.setter
    def original_country(self, value: dict):
        self._property_changed('original_country')
        self.__original_country = value        

    @property
    def field(self) -> dict:
        return self.__field

    @field.setter
    def field(self, value: dict):
        self._property_changed('field')
        self.__field = value        

    @property
    def geographic_focus(self) -> dict:
        return self.__geographic_focus

    @geographic_focus.setter
    def geographic_focus(self, value: dict):
        self._property_changed('geographic_focus')
        self.__geographic_focus = value        

    @property
    def days_open_realized_bps(self) -> dict:
        return self.__days_open_realized_bps

    @days_open_realized_bps.setter
    def days_open_realized_bps(self, value: dict):
        self._property_changed('days_open_realized_bps')
        self.__days_open_realized_bps = value        

    @property
    def fx_risk_premium_index(self) -> dict:
        return self.__fx_risk_premium_index

    @fx_risk_premium_index.setter
    def fx_risk_premium_index(self, value: dict):
        self._property_changed('fx_risk_premium_index')
        self.__fx_risk_premium_index = value        

    @property
    def skew(self) -> dict:
        return self.__skew

    @skew.setter
    def skew(self, value: dict):
        self._property_changed('skew')
        self.__skew = value        

    @property
    def status(self) -> dict:
        return self.__status

    @status.setter
    def status(self, value: dict):
        self._property_changed('status')
        self.__status = value        

    @property
    def notional_currency(self) -> dict:
        return self.__notional_currency

    @notional_currency.setter
    def notional_currency(self, value: dict):
        self._property_changed('notional_currency')
        self.__notional_currency = value        

    @property
    def sustain_emerging_markets(self) -> dict:
        return self.__sustain_emerging_markets

    @sustain_emerging_markets.setter
    def sustain_emerging_markets(self, value: dict):
        self._property_changed('sustain_emerging_markets')
        self.__sustain_emerging_markets = value        

    @property
    def leg1_designated_maturity(self) -> dict:
        return self.__leg1_designated_maturity

    @leg1_designated_maturity.setter
    def leg1_designated_maturity(self, value: dict):
        self._property_changed('leg1_designated_maturity')
        self.__leg1_designated_maturity = value        

    @property
    def total_price(self) -> dict:
        return self.__total_price

    @total_price.setter
    def total_price(self, value: dict):
        self._property_changed('total_price')
        self.__total_price = value        

    @property
    def on_behalf_of(self) -> dict:
        return self.__on_behalf_of

    @on_behalf_of.setter
    def on_behalf_of(self, value: dict):
        self._property_changed('on_behalf_of')
        self.__on_behalf_of = value        

    @property
    def test_type(self) -> dict:
        return self.__test_type

    @test_type.setter
    def test_type(self, value: dict):
        self._property_changed('test_type')
        self.__test_type = value        

    @property
    def accrued_interest_standard(self) -> dict:
        return self.__accrued_interest_standard

    @accrued_interest_standard.setter
    def accrued_interest_standard(self, value: dict):
        self._property_changed('accrued_interest_standard')
        self.__accrued_interest_standard = value        

    @property
    def future_month_z26(self) -> dict:
        return self.__future_month_z26

    @future_month_z26.setter
    def future_month_z26(self, value: dict):
        self._property_changed('future_month_z26')
        self.__future_month_z26 = value        

    @property
    def future_month_z25(self) -> dict:
        return self.__future_month_z25

    @future_month_z25.setter
    def future_month_z25(self, value: dict):
        self._property_changed('future_month_z25')
        self.__future_month_z25 = value        

    @property
    def ccg_code(self) -> dict:
        return self.__ccg_code

    @ccg_code.setter
    def ccg_code(self, value: dict):
        self._property_changed('ccg_code')
        self.__ccg_code = value        

    @property
    def short_exposure(self) -> dict:
        return self.__short_exposure

    @short_exposure.setter
    def short_exposure(self, value: dict):
        self._property_changed('short_exposure')
        self.__short_exposure = value        

    @property
    def leg1_fixed_payment_currency(self) -> dict:
        return self.__leg1_fixed_payment_currency

    @leg1_fixed_payment_currency.setter
    def leg1_fixed_payment_currency(self, value: dict):
        self._property_changed('leg1_fixed_payment_currency')
        self.__leg1_fixed_payment_currency = value        

    @property
    def arrival_haircut_vwap(self) -> dict:
        return self.__arrival_haircut_vwap

    @arrival_haircut_vwap.setter
    def arrival_haircut_vwap(self, value: dict):
        self._property_changed('arrival_haircut_vwap')
        self.__arrival_haircut_vwap = value        

    @property
    def execution_days(self) -> dict:
        return self.__execution_days

    @execution_days.setter
    def execution_days(self, value: dict):
        self._property_changed('execution_days')
        self.__execution_days = value        

    @property
    def recall_due_date(self) -> dict:
        return self.__recall_due_date

    @recall_due_date.setter
    def recall_due_date(self, value: dict):
        self._property_changed('recall_due_date')
        self.__recall_due_date = value        

    @property
    def forward(self) -> dict:
        return self.__forward

    @forward.setter
    def forward(self, value: dict):
        self._property_changed('forward')
        self.__forward = value        

    @property
    def strike(self) -> dict:
        return self.__strike

    @strike.setter
    def strike(self, value: dict):
        self._property_changed('strike')
        self.__strike = value        

    @property
    def spread_limit(self) -> dict:
        return self.__spread_limit

    @spread_limit.setter
    def spread_limit(self, value: dict):
        self._property_changed('spread_limit')
        self.__spread_limit = value        

    @property
    def product_scope(self) -> dict:
        return self.__product_scope

    @product_scope.setter
    def product_scope(self, value: dict):
        self._property_changed('product_scope')
        self.__product_scope = value        

    @property
    def asset_parameters_issuer_type(self) -> dict:
        return self.__asset_parameters_issuer_type

    @asset_parameters_issuer_type.setter
    def asset_parameters_issuer_type(self, value: dict):
        self._property_changed('asset_parameters_issuer_type')
        self.__asset_parameters_issuer_type = value        

    @property
    def currency1(self) -> dict:
        return self.__currency1

    @currency1.setter
    def currency1(self, value: dict):
        self._property_changed('currency1')
        self.__currency1 = value        

    @property
    def currency2(self) -> dict:
        return self.__currency2

    @currency2.setter
    def currency2(self, value: dict):
        self._property_changed('currency2')
        self.__currency2 = value        

    @property
    def previous_close_realized_bps(self) -> dict:
        return self.__previous_close_realized_bps

    @previous_close_realized_bps.setter
    def previous_close_realized_bps(self, value: dict):
        self._property_changed('previous_close_realized_bps')
        self.__previous_close_realized_bps = value        

    @property
    def days_since_reported(self) -> dict:
        return self.__days_since_reported

    @days_since_reported.setter
    def days_since_reported(self, value: dict):
        self._property_changed('days_since_reported')
        self.__days_since_reported = value        

    @property
    def event_status(self) -> dict:
        return self.__event_status

    @event_status.setter
    def event_status(self, value: dict):
        self._property_changed('event_status')
        self.__event_status = value        

    @property
    def vwap_in_limit(self) -> dict:
        return self.__vwap_in_limit

    @vwap_in_limit.setter
    def vwap_in_limit(self, value: dict):
        self._property_changed('vwap_in_limit')
        self.__vwap_in_limit = value        

    @property
    def fwd_duration(self) -> dict:
        return self.__fwd_duration

    @fwd_duration.setter
    def fwd_duration(self, value: dict):
        self._property_changed('fwd_duration')
        self.__fwd_duration = value        

    @property
    def return_(self) -> dict:
        return self.__return

    @return_.setter
    def return_(self, value: dict):
        self._property_changed('return_')
        self.__return = value        

    @property
    def is_pair_basket(self) -> dict:
        return self.__is_pair_basket

    @is_pair_basket.setter
    def is_pair_basket(self, value: dict):
        self._property_changed('is_pair_basket')
        self.__is_pair_basket = value        

    @property
    def notional_amount(self) -> dict:
        return self.__notional_amount

    @notional_amount.setter
    def notional_amount(self, value: dict):
        self._property_changed('notional_amount')
        self.__notional_amount = value        

    @property
    def pay_or_receive(self) -> dict:
        return self.__pay_or_receive

    @pay_or_receive.setter
    def pay_or_receive(self, value: dict):
        self._property_changed('pay_or_receive')
        self.__pay_or_receive = value        

    @property
    def total_severe(self) -> dict:
        return self.__total_severe

    @total_severe.setter
    def total_severe(self, value: dict):
        self._property_changed('total_severe')
        self.__total_severe = value        

    @property
    def unexecuted_notional_usd(self) -> dict:
        return self.__unexecuted_notional_usd

    @unexecuted_notional_usd.setter
    def unexecuted_notional_usd(self, value: dict):
        self._property_changed('unexecuted_notional_usd')
        self.__unexecuted_notional_usd = value        

    @property
    def expected_residual_percentage(self) -> dict:
        return self.__expected_residual_percentage

    @expected_residual_percentage.setter
    def expected_residual_percentage(self, value: dict):
        self._property_changed('expected_residual_percentage')
        self.__expected_residual_percentage = value        

    @property
    def maturity_date(self) -> dict:
        return self.__maturity_date

    @maturity_date.setter
    def maturity_date(self, value: dict):
        self._property_changed('maturity_date')
        self.__maturity_date = value        

    @property
    def trace_adv_sell(self) -> dict:
        return self.__trace_adv_sell

    @trace_adv_sell.setter
    def trace_adv_sell(self, value: dict):
        self._property_changed('trace_adv_sell')
        self.__trace_adv_sell = value        

    @property
    def event_name(self) -> dict:
        return self.__event_name

    @event_name.setter
    def event_name(self, value: dict):
        self._property_changed('event_name')
        self.__event_name = value        

    @property
    def address_line2(self) -> dict:
        return self.__address_line2

    @address_line2.setter
    def address_line2(self, value: dict):
        self._property_changed('address_line2')
        self.__address_line2 = value        

    @property
    def indication_of_other_price_affecting_term(self) -> dict:
        return self.__indication_of_other_price_affecting_term

    @indication_of_other_price_affecting_term.setter
    def indication_of_other_price_affecting_term(self, value: dict):
        self._property_changed('indication_of_other_price_affecting_term')
        self.__indication_of_other_price_affecting_term = value        

    @property
    def unadjusted_bid(self) -> dict:
        return self.__unadjusted_bid

    @unadjusted_bid.setter
    def unadjusted_bid(self, value: dict):
        self._property_changed('unadjusted_bid')
        self.__unadjusted_bid = value        

    @property
    def backtest_type(self) -> dict:
        return self.__backtest_type

    @backtest_type.setter
    def backtest_type(self, value: dict):
        self._property_changed('backtest_type')
        self.__backtest_type = value        

    @property
    def gsdeer(self) -> dict:
        return self.__gsdeer

    @gsdeer.setter
    def gsdeer(self, value: dict):
        self._property_changed('gsdeer')
        self.__gsdeer = value        

    @property
    def asset_parameters_issuer(self) -> dict:
        return self.__asset_parameters_issuer

    @asset_parameters_issuer.setter
    def asset_parameters_issuer(self, value: dict):
        self._property_changed('asset_parameters_issuer')
        self.__asset_parameters_issuer = value        

    @property
    def g_regional_percentile(self) -> dict:
        return self.__g_regional_percentile

    @g_regional_percentile.setter
    def g_regional_percentile(self, value: dict):
        self._property_changed('g_regional_percentile')
        self.__g_regional_percentile = value        

    @property
    def coverage_checked(self) -> dict:
        return self.__coverage_checked

    @coverage_checked.setter
    def coverage_checked(self, value: dict):
        self._property_changed('coverage_checked')
        self.__coverage_checked = value        

    @property
    def ois_xccy_ex_spike(self) -> dict:
        return self.__ois_xccy_ex_spike

    @ois_xccy_ex_spike.setter
    def ois_xccy_ex_spike(self, value: dict):
        self._property_changed('ois_xccy_ex_spike')
        self.__ois_xccy_ex_spike = value        

    @property
    def total_risk(self) -> dict:
        return self.__total_risk

    @total_risk.setter
    def total_risk(self, value: dict):
        self._property_changed('total_risk')
        self.__total_risk = value        

    @property
    def mnav(self) -> dict:
        return self.__mnav

    @mnav.setter
    def mnav(self, value: dict):
        self._property_changed('mnav')
        self.__mnav = value        

    @property
    def market_volume(self) -> dict:
        return self.__market_volume

    @market_volume.setter
    def market_volume(self, value: dict):
        self._property_changed('market_volume')
        self.__market_volume = value        

    @property
    def swap_annuity(self) -> dict:
        return self.__swap_annuity

    @swap_annuity.setter
    def swap_annuity(self, value: dict):
        self._property_changed('swap_annuity')
        self.__swap_annuity = value        

    @property
    def par_asset_swap_spread(self) -> dict:
        return self.__par_asset_swap_spread

    @par_asset_swap_spread.setter
    def par_asset_swap_spread(self, value: dict):
        self._property_changed('par_asset_swap_spread')
        self.__par_asset_swap_spread = value        

    @property
    def curr_yield7_day(self) -> dict:
        return self.__curr_yield7_day

    @curr_yield7_day.setter
    def curr_yield7_day(self, value: dict):
        self._property_changed('curr_yield7_day')
        self.__curr_yield7_day = value        

    @property
    def pressure(self) -> dict:
        return self.__pressure

    @pressure.setter
    def pressure(self, value: dict):
        self._property_changed('pressure')
        self.__pressure = value        

    @property
    def short_description(self) -> dict:
        return self.__short_description

    @short_description.setter
    def short_description(self, value: dict):
        self._property_changed('short_description')
        self.__short_description = value        

    @property
    def future_month_z24(self) -> dict:
        return self.__future_month_z24

    @future_month_z24.setter
    def future_month_z24(self, value: dict):
        self._property_changed('future_month_z24')
        self.__future_month_z24 = value        

    @property
    def feed(self) -> dict:
        return self.__feed

    @feed.setter
    def feed(self, value: dict):
        self._property_changed('feed')
        self.__feed = value        

    @property
    def future_month_z23(self) -> dict:
        return self.__future_month_z23

    @future_month_z23.setter
    def future_month_z23(self, value: dict):
        self._property_changed('future_month_z23')
        self.__future_month_z23 = value        

    @property
    def mkt_point1(self) -> dict:
        return self.__mkt_point1

    @mkt_point1.setter
    def mkt_point1(self, value: dict):
        self._property_changed('mkt_point1')
        self.__mkt_point1 = value        

    @property
    def future_month_z22(self) -> dict:
        return self.__future_month_z22

    @future_month_z22.setter
    def future_month_z22(self, value: dict):
        self._property_changed('future_month_z22')
        self.__future_month_z22 = value        

    @property
    def future_month_z21(self) -> dict:
        return self.__future_month_z21

    @future_month_z21.setter
    def future_month_z21(self, value: dict):
        self._property_changed('future_month_z21')
        self.__future_month_z21 = value        

    @property
    def future_month_z20(self) -> dict:
        return self.__future_month_z20

    @future_month_z20.setter
    def future_month_z20(self, value: dict):
        self._property_changed('future_month_z20')
        self.__future_month_z20 = value        

    @property
    def asset_parameters_commodity_sector(self) -> dict:
        return self.__asset_parameters_commodity_sector

    @asset_parameters_commodity_sector.setter
    def asset_parameters_commodity_sector(self, value: dict):
        self._property_changed('asset_parameters_commodity_sector')
        self.__asset_parameters_commodity_sector = value        

    @property
    def price_notation2(self) -> dict:
        return self.__price_notation2

    @price_notation2.setter
    def price_notation2(self, value: dict):
        self._property_changed('price_notation2')
        self.__price_notation2 = value        

    @property
    def market_buffer_threshold(self) -> dict:
        return self.__market_buffer_threshold

    @market_buffer_threshold.setter
    def market_buffer_threshold(self, value: dict):
        self._property_changed('market_buffer_threshold')
        self.__market_buffer_threshold = value        

    @property
    def price_notation3(self) -> dict:
        return self.__price_notation3

    @price_notation3.setter
    def price_notation3(self, value: dict):
        self._property_changed('price_notation3')
        self.__price_notation3 = value        

    @property
    def mkt_point3(self) -> dict:
        return self.__mkt_point3

    @mkt_point3.setter
    def mkt_point3(self, value: dict):
        self._property_changed('mkt_point3')
        self.__mkt_point3 = value        

    @property
    def mkt_point2(self) -> dict:
        return self.__mkt_point2

    @mkt_point2.setter
    def mkt_point2(self, value: dict):
        self._property_changed('mkt_point2')
        self.__mkt_point2 = value        

    @property
    def leg2_type(self) -> dict:
        return self.__leg2_type

    @leg2_type.setter
    def leg2_type(self, value: dict):
        self._property_changed('leg2_type')
        self.__leg2_type = value        

    @property
    def mkt_point4(self) -> dict:
        return self.__mkt_point4

    @mkt_point4.setter
    def mkt_point4(self, value: dict):
        self._property_changed('mkt_point4')
        self.__mkt_point4 = value        

    @property
    def degree_days_type(self) -> dict:
        return self.__degree_days_type

    @degree_days_type.setter
    def degree_days_type(self, value: dict):
        self._property_changed('degree_days_type')
        self.__degree_days_type = value        

    @property
    def sentiment(self) -> dict:
        return self.__sentiment

    @sentiment.setter
    def sentiment(self, value: dict):
        self._property_changed('sentiment')
        self.__sentiment = value        

    @property
    def investment_income(self) -> dict:
        return self.__investment_income

    @investment_income.setter
    def investment_income(self, value: dict):
        self._property_changed('investment_income')
        self.__investment_income = value        

    @property
    def group_type(self) -> dict:
        return self.__group_type

    @group_type.setter
    def group_type(self, value: dict):
        self._property_changed('group_type')
        self.__group_type = value        

    @property
    def forward_point_imm(self) -> dict:
        return self.__forward_point_imm

    @forward_point_imm.setter
    def forward_point_imm(self, value: dict):
        self._property_changed('forward_point_imm')
        self.__forward_point_imm = value        

    @property
    def twap(self) -> dict:
        return self.__twap

    @twap.setter
    def twap(self, value: dict):
        self._property_changed('twap')
        self.__twap = value        

    @property
    def client_short_name(self) -> dict:
        return self.__client_short_name

    @client_short_name.setter
    def client_short_name(self, value: dict):
        self._property_changed('client_short_name')
        self.__client_short_name = value        

    @property
    def group_category(self) -> dict:
        return self.__group_category

    @group_category.setter
    def group_category(self, value: dict):
        self._property_changed('group_category')
        self.__group_category = value        

    @property
    def bid_plus_ask(self) -> dict:
        return self.__bid_plus_ask

    @bid_plus_ask.setter
    def bid_plus_ask(self, value: dict):
        self._property_changed('bid_plus_ask')
        self.__bid_plus_ask = value        

    @property
    def foreign_ccy_rate(self) -> dict:
        return self.__foreign_ccy_rate

    @foreign_ccy_rate.setter
    def foreign_ccy_rate(self, value: dict):
        self._property_changed('foreign_ccy_rate')
        self.__foreign_ccy_rate = value        

    @property
    def election_odds(self) -> dict:
        return self.__election_odds

    @election_odds.setter
    def election_odds(self, value: dict):
        self._property_changed('election_odds')
        self.__election_odds = value        

    @property
    def wind_direction_forecast(self) -> dict:
        return self.__wind_direction_forecast

    @wind_direction_forecast.setter
    def wind_direction_forecast(self, value: dict):
        self._property_changed('wind_direction_forecast')
        self.__wind_direction_forecast = value        

    @property
    def require_anon_client_name(self) -> dict:
        return self.__require_anon_client_name

    @require_anon_client_name.setter
    def require_anon_client_name(self, value: dict):
        self._property_changed('require_anon_client_name')
        self.__require_anon_client_name = value        

    @property
    def pricing_location(self) -> dict:
        return self.__pricing_location

    @pricing_location.setter
    def pricing_location(self, value: dict):
        self._property_changed('pricing_location')
        self.__pricing_location = value        

    @property
    def beta(self) -> dict:
        return self.__beta

    @beta.setter
    def beta(self, value: dict):
        self._property_changed('beta')
        self.__beta = value        

    @property
    def last_returns_end_date(self) -> dict:
        return self.__last_returns_end_date

    @last_returns_end_date.setter
    def last_returns_end_date(self, value: dict):
        self._property_changed('last_returns_end_date')
        self.__last_returns_end_date = value        

    @property
    def upfront_payment_date(self) -> dict:
        return self.__upfront_payment_date

    @upfront_payment_date.setter
    def upfront_payment_date(self, value: dict):
        self._property_changed('upfront_payment_date')
        self.__upfront_payment_date = value        

    @property
    def sell1point5bps(self) -> dict:
        return self.__sell1point5bps

    @sell1point5bps.setter
    def sell1point5bps(self, value: dict):
        self._property_changed('sell1point5bps')
        self.__sell1point5bps = value        

    @property
    def long_exposure(self) -> dict:
        return self.__long_exposure

    @long_exposure.setter
    def long_exposure(self, value: dict):
        self._property_changed('long_exposure')
        self.__long_exposure = value        

    @property
    def sell4point5bps(self) -> dict:
        return self.__sell4point5bps

    @sell4point5bps.setter
    def sell4point5bps(self, value: dict):
        self._property_changed('sell4point5bps')
        self.__sell4point5bps = value        

    @property
    def tcm_cost_participation_rate20_pct(self) -> dict:
        return self.__tcm_cost_participation_rate20_pct

    @tcm_cost_participation_rate20_pct.setter
    def tcm_cost_participation_rate20_pct(self, value: dict):
        self._property_changed('tcm_cost_participation_rate20_pct')
        self.__tcm_cost_participation_rate20_pct = value        

    @property
    def venue_type(self) -> dict:
        return self.__venue_type

    @venue_type.setter
    def venue_type(self, value: dict):
        self._property_changed('venue_type')
        self.__venue_type = value        

    @property
    def multi_asset_class_swap(self) -> dict:
        return self.__multi_asset_class_swap

    @multi_asset_class_swap.setter
    def multi_asset_class_swap(self, value: dict):
        self._property_changed('multi_asset_class_swap')
        self.__multi_asset_class_swap = value        

    @property
    def delta_change_id(self) -> dict:
        return self.__delta_change_id

    @delta_change_id.setter
    def delta_change_id(self, value: dict):
        self._property_changed('delta_change_id')
        self.__delta_change_id = value        

    @property
    def implementation_id(self) -> dict:
        return self.__implementation_id

    @implementation_id.setter
    def implementation_id(self, value: dict):
        self._property_changed('implementation_id')
        self.__implementation_id = value        

    @property
    def leg1_fixed_payment(self) -> dict:
        return self.__leg1_fixed_payment

    @leg1_fixed_payment.setter
    def leg1_fixed_payment(self, value: dict):
        self._property_changed('leg1_fixed_payment')
        self.__leg1_fixed_payment = value        

    @property
    def es_numeric_score(self) -> dict:
        return self.__es_numeric_score

    @es_numeric_score.setter
    def es_numeric_score(self, value: dict):
        self._property_changed('es_numeric_score')
        self.__es_numeric_score = value        

    @property
    def in_benchmark(self) -> dict:
        return self.__in_benchmark

    @in_benchmark.setter
    def in_benchmark(self, value: dict):
        self._property_changed('in_benchmark')
        self.__in_benchmark = value        

    @property
    def action_sdr(self) -> dict:
        return self.__action_sdr

    @action_sdr.setter
    def action_sdr(self, value: dict):
        self._property_changed('action_sdr')
        self.__action_sdr = value        

    @property
    def count_ideas_qtd(self) -> dict:
        return self.__count_ideas_qtd

    @count_ideas_qtd.setter
    def count_ideas_qtd(self, value: dict):
        self._property_changed('count_ideas_qtd')
        self.__count_ideas_qtd = value        

    @property
    def knock_out_price(self) -> dict:
        return self.__knock_out_price

    @knock_out_price.setter
    def knock_out_price(self, value: dict):
        self._property_changed('knock_out_price')
        self.__knock_out_price = value        

    @property
    def ctd_asset_id(self) -> dict:
        return self.__ctd_asset_id

    @ctd_asset_id.setter
    def ctd_asset_id(self, value: dict):
        self._property_changed('ctd_asset_id')
        self.__ctd_asset_id = value        

    @property
    def buy10bps(self) -> dict:
        return self.__buy10bps

    @buy10bps.setter
    def buy10bps(self, value: dict):
        self._property_changed('buy10bps')
        self.__buy10bps = value        

    @property
    def precipitation(self) -> dict:
        return self.__precipitation

    @precipitation.setter
    def precipitation(self, value: dict):
        self._property_changed('precipitation')
        self.__precipitation = value        

    @property
    def value_type(self) -> dict:
        return self.__value_type

    @value_type.setter
    def value_type(self, value: dict):
        self._property_changed('value_type')
        self.__value_type = value        

    @property
    def beta_adjusted_net_exposure(self) -> dict:
        return self.__beta_adjusted_net_exposure

    @beta_adjusted_net_exposure.setter
    def beta_adjusted_net_exposure(self, value: dict):
        self._property_changed('beta_adjusted_net_exposure')
        self.__beta_adjusted_net_exposure = value        

    @property
    def estimated_rod_volume(self) -> dict:
        return self.__estimated_rod_volume

    @estimated_rod_volume.setter
    def estimated_rod_volume(self, value: dict):
        self._property_changed('estimated_rod_volume')
        self.__estimated_rod_volume = value        

    @property
    def sell14bps(self) -> dict:
        return self.__sell14bps

    @sell14bps.setter
    def sell14bps(self, value: dict):
        self._property_changed('sell14bps')
        self.__sell14bps = value        

    @property
    def excess_return_price(self) -> dict:
        return self.__excess_return_price

    @excess_return_price.setter
    def excess_return_price(self, value: dict):
        self._property_changed('excess_return_price')
        self.__excess_return_price = value        

    @property
    def fx_pnl(self) -> dict:
        return self.__fx_pnl

    @fx_pnl.setter
    def fx_pnl(self, value: dict):
        self._property_changed('fx_pnl')
        self.__fx_pnl = value        

    @property
    def asset_classifications_gics_industry_group(self) -> dict:
        return self.__asset_classifications_gics_industry_group

    @asset_classifications_gics_industry_group.setter
    def asset_classifications_gics_industry_group(self, value: dict):
        self._property_changed('asset_classifications_gics_industry_group')
        self.__asset_classifications_gics_industry_group = value        

    @property
    def lending_sec_id(self) -> dict:
        return self.__lending_sec_id

    @lending_sec_id.setter
    def lending_sec_id(self, value: dict):
        self._property_changed('lending_sec_id')
        self.__lending_sec_id = value        

    @property
    def dollar_duration(self) -> dict:
        return self.__dollar_duration

    @dollar_duration.setter
    def dollar_duration(self, value: dict):
        self._property_changed('dollar_duration')
        self.__dollar_duration = value        

    @property
    def equity_theta(self) -> dict:
        return self.__equity_theta

    @equity_theta.setter
    def equity_theta(self, value: dict):
        self._property_changed('equity_theta')
        self.__equity_theta = value        

    @property
    def dv01(self) -> dict:
        return self.__dv01

    @dv01.setter
    def dv01(self, value: dict):
        self._property_changed('dv01')
        self.__dv01 = value        

    @property
    def start_date(self) -> dict:
        return self.__start_date

    @start_date.setter
    def start_date(self, value: dict):
        self._property_changed('start_date')
        self.__start_date = value        

    @property
    def mixed_swap(self) -> dict:
        return self.__mixed_swap

    @mixed_swap.setter
    def mixed_swap(self, value: dict):
        self._property_changed('mixed_swap')
        self.__mixed_swap = value        

    @property
    def swaption_premium(self) -> dict:
        return self.__swaption_premium

    @swaption_premium.setter
    def swaption_premium(self, value: dict):
        self._property_changed('swaption_premium')
        self.__swaption_premium = value        

    @property
    def snowfall(self) -> dict:
        return self.__snowfall

    @snowfall.setter
    def snowfall(self, value: dict):
        self._property_changed('snowfall')
        self.__snowfall = value        

    @property
    def liquidity_bucket_buy(self) -> dict:
        return self.__liquidity_bucket_buy

    @liquidity_bucket_buy.setter
    def liquidity_bucket_buy(self, value: dict):
        self._property_changed('liquidity_bucket_buy')
        self.__liquidity_bucket_buy = value        

    @property
    def mic(self) -> dict:
        return self.__mic

    @mic.setter
    def mic(self, value: dict):
        self._property_changed('mic')
        self.__mic = value        

    @property
    def latitude(self) -> dict:
        return self.__latitude

    @latitude.setter
    def latitude(self, value: dict):
        self._property_changed('latitude')
        self.__latitude = value        

    @property
    def mid(self) -> dict:
        return self.__mid

    @mid.setter
    def mid(self, value: dict):
        self._property_changed('mid')
        self.__mid = value        

    @property
    def implied_repo(self) -> dict:
        return self.__implied_repo

    @implied_repo.setter
    def implied_repo(self, value: dict):
        self._property_changed('implied_repo')
        self.__implied_repo = value        

    @property
    def long(self) -> dict:
        return self.__long

    @long.setter
    def long(self, value: dict):
        self._property_changed('long')
        self.__long = value        

    @property
    def covered_bond(self) -> dict:
        return self.__covered_bond

    @covered_bond.setter
    def covered_bond(self, value: dict):
        self._property_changed('covered_bond')
        self.__covered_bond = value        

    @property
    def region_code(self) -> dict:
        return self.__region_code

    @region_code.setter
    def region_code(self, value: dict):
        self._property_changed('region_code')
        self.__region_code = value        

    @property
    def buy20cents(self) -> dict:
        return self.__buy20cents

    @buy20cents.setter
    def buy20cents(self, value: dict):
        self._property_changed('buy20cents')
        self.__buy20cents = value        

    @property
    def long_weight(self) -> dict:
        return self.__long_weight

    @long_weight.setter
    def long_weight(self, value: dict):
        self._property_changed('long_weight')
        self.__long_weight = value        

    @property
    def calculation_time(self) -> dict:
        return self.__calculation_time

    @calculation_time.setter
    def calculation_time(self, value: dict):
        self._property_changed('calculation_time')
        self.__calculation_time = value        

    @property
    def liquidity_bucket_sell(self) -> dict:
        return self.__liquidity_bucket_sell

    @liquidity_bucket_sell.setter
    def liquidity_bucket_sell(self, value: dict):
        self._property_changed('liquidity_bucket_sell')
        self.__liquidity_bucket_sell = value        

    @property
    def days_open_unrealized_cash(self) -> dict:
        return self.__days_open_unrealized_cash

    @days_open_unrealized_cash.setter
    def days_open_unrealized_cash(self, value: dict):
        self._property_changed('days_open_unrealized_cash')
        self.__days_open_unrealized_cash = value        

    @property
    def temperature(self) -> dict:
        return self.__temperature

    @temperature.setter
    def temperature(self, value: dict):
        self._property_changed('temperature')
        self.__temperature = value        

    @property
    def average_realized_variance(self) -> dict:
        return self.__average_realized_variance

    @average_realized_variance.setter
    def average_realized_variance(self, value: dict):
        self._property_changed('average_realized_variance')
        self.__average_realized_variance = value        

    @property
    def rating_fitch(self) -> dict:
        return self.__rating_fitch

    @rating_fitch.setter
    def rating_fitch(self, value: dict):
        self._property_changed('rating_fitch')
        self.__rating_fitch = value        

    @property
    def financial_returns_score(self) -> dict:
        return self.__financial_returns_score

    @financial_returns_score.setter
    def financial_returns_score(self, value: dict):
        self._property_changed('financial_returns_score')
        self.__financial_returns_score = value        

    @property
    def year_or_quarter(self) -> dict:
        return self.__year_or_quarter

    @year_or_quarter.setter
    def year_or_quarter(self, value: dict):
        self._property_changed('year_or_quarter')
        self.__year_or_quarter = value        

    @property
    def non_symbol_dimensions(self) -> dict:
        return self.__non_symbol_dimensions

    @non_symbol_dimensions.setter
    def non_symbol_dimensions(self, value: dict):
        self._property_changed('non_symbol_dimensions')
        self.__non_symbol_dimensions = value        

    @property
    def commodities_forecast(self) -> dict:
        return self.__commodities_forecast

    @commodities_forecast.setter
    def commodities_forecast(self, value: dict):
        self._property_changed('commodities_forecast')
        self.__commodities_forecast = value        

    @property
    def covid19_by_state(self) -> dict:
        return self.__covid19_by_state

    @covid19_by_state.setter
    def covid19_by_state(self, value: dict):
        self._property_changed('covid19_by_state')
        self.__covid19_by_state = value        

    @property
    def percentage_expected_residual(self) -> dict:
        return self.__percentage_expected_residual

    @percentage_expected_residual.setter
    def percentage_expected_residual(self, value: dict):
        self._property_changed('percentage_expected_residual')
        self.__percentage_expected_residual = value        

    @property
    def hospital_name(self) -> dict:
        return self.__hospital_name

    @hospital_name.setter
    def hospital_name(self, value: dict):
        self._property_changed('hospital_name')
        self.__hospital_name = value        

    @property
    def buy90cents(self) -> dict:
        return self.__buy90cents

    @buy90cents.setter
    def buy90cents(self, value: dict):
        self._property_changed('buy90cents')
        self.__buy90cents = value        

    @property
    def period_type(self) -> dict:
        return self.__period_type

    @period_type.setter
    def period_type(self, value: dict):
        self._property_changed('period_type')
        self.__period_type = value        

    @property
    def asset_classifications_country_name(self) -> dict:
        return self.__asset_classifications_country_name

    @asset_classifications_country_name.setter
    def asset_classifications_country_name(self, value: dict):
        self._property_changed('asset_classifications_country_name')
        self.__asset_classifications_country_name = value        

    @property
    def total_hospitalized(self) -> dict:
        return self.__total_hospitalized

    @total_hospitalized.setter
    def total_hospitalized(self, value: dict):
        self._property_changed('total_hospitalized')
        self.__total_hospitalized = value        

    @property
    def pegged_refill_interval(self) -> dict:
        return self.__pegged_refill_interval

    @pegged_refill_interval.setter
    def pegged_refill_interval(self, value: dict):
        self._property_changed('pegged_refill_interval')
        self.__pegged_refill_interval = value        

    @property
    def fatalities_probable(self) -> dict:
        return self.__fatalities_probable

    @fatalities_probable.setter
    def fatalities_probable(self, value: dict):
        self._property_changed('fatalities_probable')
        self.__fatalities_probable = value        

    @property
    def administrative_region(self) -> dict:
        return self.__administrative_region

    @administrative_region.setter
    def administrative_region(self, value: dict):
        self._property_changed('administrative_region')
        self.__administrative_region = value        

    @property
    def open(self) -> dict:
        return self.__open

    @open.setter
    def open(self, value: dict):
        self._property_changed('open')
        self.__open = value        

    @property
    def cusip(self) -> dict:
        return self.__cusip

    @cusip.setter
    def cusip(self, value: dict):
        self._property_changed('cusip')
        self.__cusip = value        

    @property
    def total_confirmed_by_state(self) -> dict:
        return self.__total_confirmed_by_state

    @total_confirmed_by_state.setter
    def total_confirmed_by_state(self, value: dict):
        self._property_changed('total_confirmed_by_state')
        self.__total_confirmed_by_state = value        

    @property
    def wind_attribute(self) -> dict:
        return self.__wind_attribute

    @wind_attribute.setter
    def wind_attribute(self, value: dict):
        self._property_changed('wind_attribute')
        self.__wind_attribute = value        

    @property
    def spread_option_atm_fwd_rate(self) -> dict:
        return self.__spread_option_atm_fwd_rate

    @spread_option_atm_fwd_rate.setter
    def spread_option_atm_fwd_rate(self, value: dict):
        self._property_changed('spread_option_atm_fwd_rate')
        self.__spread_option_atm_fwd_rate = value        

    @property
    def net_exposure(self) -> dict:
        return self.__net_exposure

    @net_exposure.setter
    def net_exposure(self, value: dict):
        self._property_changed('net_exposure')
        self.__net_exposure = value        

    @property
    def is_legacy_pair_basket(self) -> dict:
        return self.__is_legacy_pair_basket

    @is_legacy_pair_basket.setter
    def is_legacy_pair_basket(self, value: dict):
        self._property_changed('is_legacy_pair_basket')
        self.__is_legacy_pair_basket = value        

    @property
    def issuer_type(self) -> dict:
        return self.__issuer_type

    @issuer_type.setter
    def issuer_type(self, value: dict):
        self._property_changed('issuer_type')
        self.__issuer_type = value        

    @property
    def buy70cents(self) -> dict:
        return self.__buy70cents

    @buy70cents.setter
    def buy70cents(self, value: dict):
        self._property_changed('buy70cents')
        self.__buy70cents = value        

    @property
    def strike_reference(self) -> dict:
        return self.__strike_reference

    @strike_reference.setter
    def strike_reference(self, value: dict):
        self._property_changed('strike_reference')
        self.__strike_reference = value        

    @property
    def asset_count(self) -> dict:
        return self.__asset_count

    @asset_count.setter
    def asset_count(self, value: dict):
        self._property_changed('asset_count')
        self.__asset_count = value        

    @property
    def is_order_in_limit(self) -> dict:
        return self.__is_order_in_limit

    @is_order_in_limit.setter
    def is_order_in_limit(self, value: dict):
        self._property_changed('is_order_in_limit')
        self.__is_order_in_limit = value        

    @property
    def fundamental_metric(self) -> dict:
        return self.__fundamental_metric

    @fundamental_metric.setter
    def fundamental_metric(self, value: dict):
        self._property_changed('fundamental_metric')
        self.__fundamental_metric = value        

    @property
    def quote_status_id(self) -> dict:
        return self.__quote_status_id

    @quote_status_id.setter
    def quote_status_id(self, value: dict):
        self._property_changed('quote_status_id')
        self.__quote_status_id = value        

    @property
    def absolute_value(self) -> dict:
        return self.__absolute_value

    @absolute_value.setter
    def absolute_value(self, value: dict):
        self._property_changed('absolute_value')
        self.__absolute_value = value        

    @property
    def closing_report(self) -> dict:
        return self.__closing_report

    @closing_report.setter
    def closing_report(self, value: dict):
        self._property_changed('closing_report')
        self.__closing_report = value        

    @property
    def previous_total_confirmed(self) -> dict:
        return self.__previous_total_confirmed

    @previous_total_confirmed.setter
    def previous_total_confirmed(self, value: dict):
        self._property_changed('previous_total_confirmed')
        self.__previous_total_confirmed = value        

    @property
    def long_tenor(self) -> dict:
        return self.__long_tenor

    @long_tenor.setter
    def long_tenor(self, value: dict):
        self._property_changed('long_tenor')
        self.__long_tenor = value        

    @property
    def multiplier(self) -> dict:
        return self.__multiplier

    @multiplier.setter
    def multiplier(self, value: dict):
        self._property_changed('multiplier')
        self.__multiplier = value        

    @property
    def buy40cents(self) -> dict:
        return self.__buy40cents

    @buy40cents.setter
    def buy40cents(self, value: dict):
        self._property_changed('buy40cents')
        self.__buy40cents = value        

    @property
    def asset_count_priced(self) -> dict:
        return self.__asset_count_priced

    @asset_count_priced.setter
    def asset_count_priced(self, value: dict):
        self._property_changed('asset_count_priced')
        self.__asset_count_priced = value        

    @property
    def vote_direction(self) -> dict:
        return self.__vote_direction

    @vote_direction.setter
    def vote_direction(self, value: dict):
        self._property_changed('vote_direction')
        self.__vote_direction = value        

    @property
    def implied_repo_rate(self) -> dict:
        return self.__implied_repo_rate

    @implied_repo_rate.setter
    def implied_repo_rate(self, value: dict):
        self._property_changed('implied_repo_rate')
        self.__implied_repo_rate = value        

    @property
    def settlement_currency(self) -> dict:
        return self.__settlement_currency

    @settlement_currency.setter
    def settlement_currency(self, value: dict):
        self._property_changed('settlement_currency')
        self.__settlement_currency = value        

    @property
    def wtd_degree_days_forecast(self) -> dict:
        return self.__wtd_degree_days_forecast

    @wtd_degree_days_forecast.setter
    def wtd_degree_days_forecast(self, value: dict):
        self._property_changed('wtd_degree_days_forecast')
        self.__wtd_degree_days_forecast = value        

    @property
    def indication_of_collateralization(self) -> dict:
        return self.__indication_of_collateralization

    @indication_of_collateralization.setter
    def indication_of_collateralization(self, value: dict):
        self._property_changed('indication_of_collateralization')
        self.__indication_of_collateralization = value        

    @property
    def future_month_n26(self) -> dict:
        return self.__future_month_n26

    @future_month_n26.setter
    def future_month_n26(self, value: dict):
        self._property_changed('future_month_n26')
        self.__future_month_n26 = value        

    @property
    def lending_partner_fee(self) -> dict:
        return self.__lending_partner_fee

    @lending_partner_fee.setter
    def lending_partner_fee(self, value: dict):
        self._property_changed('lending_partner_fee')
        self.__lending_partner_fee = value        

    @property
    def future_month_n25(self) -> dict:
        return self.__future_month_n25

    @future_month_n25.setter
    def future_month_n25(self, value: dict):
        self._property_changed('future_month_n25')
        self.__future_month_n25 = value        

    @property
    def future_month_n24(self) -> dict:
        return self.__future_month_n24

    @future_month_n24.setter
    def future_month_n24(self, value: dict):
        self._property_changed('future_month_n24')
        self.__future_month_n24 = value        

    @property
    def primary_vwap_realized_bps(self) -> dict:
        return self.__primary_vwap_realized_bps

    @primary_vwap_realized_bps.setter
    def primary_vwap_realized_bps(self, value: dict):
        self._property_changed('primary_vwap_realized_bps')
        self.__primary_vwap_realized_bps = value        

    @property
    def future_month_n23(self) -> dict:
        return self.__future_month_n23

    @future_month_n23.setter
    def future_month_n23(self, value: dict):
        self._property_changed('future_month_n23')
        self.__future_month_n23 = value        

    @property
    def future_month_n22(self) -> dict:
        return self.__future_month_n22

    @future_month_n22.setter
    def future_month_n22(self, value: dict):
        self._property_changed('future_month_n22')
        self.__future_month_n22 = value        

    @property
    def future_month_n21(self) -> dict:
        return self.__future_month_n21

    @future_month_n21.setter
    def future_month_n21(self, value: dict):
        self._property_changed('future_month_n21')
        self.__future_month_n21 = value        

    @property
    def break_even_inflation(self) -> dict:
        return self.__break_even_inflation

    @break_even_inflation.setter
    def break_even_inflation(self, value: dict):
        self._property_changed('break_even_inflation')
        self.__break_even_inflation = value        

    @property
    def pnl_ytd(self) -> dict:
        return self.__pnl_ytd

    @pnl_ytd.setter
    def pnl_ytd(self, value: dict):
        self._property_changed('pnl_ytd')
        self.__pnl_ytd = value        

    @property
    def leg1_return_type(self) -> dict:
        return self.__leg1_return_type

    @leg1_return_type.setter
    def leg1_return_type(self, value: dict):
        self._property_changed('leg1_return_type')
        self.__leg1_return_type = value        

    @property
    def tenor2(self) -> dict:
        return self.__tenor2

    @tenor2.setter
    def tenor2(self, value: dict):
        self._property_changed('tenor2')
        self.__tenor2 = value        

    @property
    def reset_frequency(self) -> dict:
        return self.__reset_frequency

    @reset_frequency.setter
    def reset_frequency(self, value: dict):
        self._property_changed('reset_frequency')
        self.__reset_frequency = value        

    @property
    def asset_parameters_payer_frequency(self) -> dict:
        return self.__asset_parameters_payer_frequency

    @asset_parameters_payer_frequency.setter
    def asset_parameters_payer_frequency(self, value: dict):
        self._property_changed('asset_parameters_payer_frequency')
        self.__asset_parameters_payer_frequency = value        

    @property
    def degree_days_forecast(self) -> dict:
        return self.__degree_days_forecast

    @degree_days_forecast.setter
    def degree_days_forecast(self, value: dict):
        self._property_changed('degree_days_forecast')
        self.__degree_days_forecast = value        

    @property
    def is_manually_silenced(self) -> dict:
        return self.__is_manually_silenced

    @is_manually_silenced.setter
    def is_manually_silenced(self, value: dict):
        self._property_changed('is_manually_silenced')
        self.__is_manually_silenced = value        

    @property
    def buy3bps(self) -> dict:
        return self.__buy3bps

    @buy3bps.setter
    def buy3bps(self, value: dict):
        self._property_changed('buy3bps')
        self.__buy3bps = value        

    @property
    def last_updated_by_id(self) -> dict:
        return self.__last_updated_by_id

    @last_updated_by_id.setter
    def last_updated_by_id(self, value: dict):
        self._property_changed('last_updated_by_id')
        self.__last_updated_by_id = value        

    @property
    def legal_entity_acct(self) -> dict:
        return self.__legal_entity_acct

    @legal_entity_acct.setter
    def legal_entity_acct(self, value: dict):
        self._property_changed('legal_entity_acct')
        self.__legal_entity_acct = value        

    @property
    def target_shareholder_meeting_date(self) -> dict:
        return self.__target_shareholder_meeting_date

    @target_shareholder_meeting_date.setter
    def target_shareholder_meeting_date(self, value: dict):
        self._property_changed('target_shareholder_meeting_date')
        self.__target_shareholder_meeting_date = value        

    @property
    def pace_of_rollp0(self) -> dict:
        return self.__pace_of_rollp0

    @pace_of_rollp0.setter
    def pace_of_rollp0(self, value: dict):
        self._property_changed('pace_of_rollp0')
        self.__pace_of_rollp0 = value        

    @property
    def controversy_percentile(self) -> dict:
        return self.__controversy_percentile

    @controversy_percentile.setter
    def controversy_percentile(self, value: dict):
        self._property_changed('controversy_percentile')
        self.__controversy_percentile = value        

    @property
    def leg1_notional_currency(self) -> dict:
        return self.__leg1_notional_currency

    @leg1_notional_currency.setter
    def leg1_notional_currency(self, value: dict):
        self._property_changed('leg1_notional_currency')
        self.__leg1_notional_currency = value        

    @property
    def expiration_date(self) -> dict:
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value: dict):
        self._property_changed('expiration_date')
        self.__expiration_date = value        

    @property
    def floating_rate_day_count_fraction(self) -> dict:
        return self.__floating_rate_day_count_fraction

    @floating_rate_day_count_fraction.setter
    def floating_rate_day_count_fraction(self, value: dict):
        self._property_changed('floating_rate_day_count_fraction')
        self.__floating_rate_day_count_fraction = value        

    @property
    def call_last_date(self) -> dict:
        return self.__call_last_date

    @call_last_date.setter
    def call_last_date(self, value: dict):
        self._property_changed('call_last_date')
        self.__call_last_date = value        

    @property
    def factor_return(self) -> dict:
        return self.__factor_return

    @factor_return.setter
    def factor_return(self, value: dict):
        self._property_changed('factor_return')
        self.__factor_return = value        

    @property
    def passive_flow_ratio(self) -> dict:
        return self.__passive_flow_ratio

    @passive_flow_ratio.setter
    def passive_flow_ratio(self, value: dict):
        self._property_changed('passive_flow_ratio')
        self.__passive_flow_ratio = value        

    @property
    def composite5_day_adv(self) -> dict:
        return self.__composite5_day_adv

    @composite5_day_adv.setter
    def composite5_day_adv(self, value: dict):
        self._property_changed('composite5_day_adv')
        self.__composite5_day_adv = value        

    @property
    def marginal_contribution_to_risk(self) -> dict:
        return self.__marginal_contribution_to_risk

    @marginal_contribution_to_risk.setter
    def marginal_contribution_to_risk(self, value: dict):
        self._property_changed('marginal_contribution_to_risk')
        self.__marginal_contribution_to_risk = value        

    @property
    def close_date(self) -> dict:
        return self.__close_date

    @close_date.setter
    def close_date(self, value: dict):
        self._property_changed('close_date')
        self.__close_date = value        

    @property
    def temperature_hour_forecast(self) -> dict:
        return self.__temperature_hour_forecast

    @temperature_hour_forecast.setter
    def temperature_hour_forecast(self, value: dict):
        self._property_changed('temperature_hour_forecast')
        self.__temperature_hour_forecast = value        

    @property
    def new_ideas_wtd(self) -> dict:
        return self.__new_ideas_wtd

    @new_ideas_wtd.setter
    def new_ideas_wtd(self, value: dict):
        self._property_changed('new_ideas_wtd')
        self.__new_ideas_wtd = value        

    @property
    def asset_class_sdr(self) -> dict:
        return self.__asset_class_sdr

    @asset_class_sdr.setter
    def asset_class_sdr(self, value: dict):
        self._property_changed('asset_class_sdr')
        self.__asset_class_sdr = value        

    @property
    def yield_to_worst(self) -> dict:
        return self.__yield_to_worst

    @yield_to_worst.setter
    def yield_to_worst(self, value: dict):
        self._property_changed('yield_to_worst')
        self.__yield_to_worst = value        

    @property
    def closing_price(self) -> dict:
        return self.__closing_price

    @closing_price.setter
    def closing_price(self, value: dict):
        self._property_changed('closing_price')
        self.__closing_price = value        

    @property
    def turnover_composite_adjusted(self) -> dict:
        return self.__turnover_composite_adjusted

    @turnover_composite_adjusted.setter
    def turnover_composite_adjusted(self, value: dict):
        self._property_changed('turnover_composite_adjusted')
        self.__turnover_composite_adjusted = value        

    @property
    def comment(self) -> dict:
        return self.__comment

    @comment.setter
    def comment(self, value: dict):
        self._property_changed('comment')
        self.__comment = value        

    @property
    def source_symbol(self) -> dict:
        return self.__source_symbol

    @source_symbol.setter
    def source_symbol(self, value: dict):
        self._property_changed('source_symbol')
        self.__source_symbol = value        

    @property
    def ask_unadjusted(self) -> dict:
        return self.__ask_unadjusted

    @ask_unadjusted.setter
    def ask_unadjusted(self, value: dict):
        self._property_changed('ask_unadjusted')
        self.__ask_unadjusted = value        

    @property
    def restrict_external_derived_data(self) -> dict:
        return self.__restrict_external_derived_data

    @restrict_external_derived_data.setter
    def restrict_external_derived_data(self, value: dict):
        self._property_changed('restrict_external_derived_data')
        self.__restrict_external_derived_data = value        

    @property
    def ask_change(self) -> dict:
        return self.__ask_change

    @ask_change.setter
    def ask_change(self, value: dict):
        self._property_changed('ask_change')
        self.__ask_change = value        

    @property
    def count_ideas_mtd(self) -> dict:
        return self.__count_ideas_mtd

    @count_ideas_mtd.setter
    def count_ideas_mtd(self, value: dict):
        self._property_changed('count_ideas_mtd')
        self.__count_ideas_mtd = value        

    @property
    def end_date(self) -> dict:
        return self.__end_date

    @end_date.setter
    def end_date(self, value: dict):
        self._property_changed('end_date')
        self.__end_date = value        

    @property
    def sunshine(self) -> dict:
        return self.__sunshine

    @sunshine.setter
    def sunshine(self, value: dict):
        self._property_changed('sunshine')
        self.__sunshine = value        

    @property
    def contract_type(self) -> dict:
        return self.__contract_type

    @contract_type.setter
    def contract_type(self, value: dict):
        self._property_changed('contract_type')
        self.__contract_type = value        

    @property
    def momentum_type(self) -> dict:
        return self.__momentum_type

    @momentum_type.setter
    def momentum_type(self, value: dict):
        self._property_changed('momentum_type')
        self.__momentum_type = value        

    @property
    def specific_risk(self) -> dict:
        return self.__specific_risk

    @specific_risk.setter
    def specific_risk(self, value: dict):
        self._property_changed('specific_risk')
        self.__specific_risk = value        

    @property
    def mdapi(self) -> dict:
        return self.__mdapi

    @mdapi.setter
    def mdapi(self, value: dict):
        self._property_changed('mdapi')
        self.__mdapi = value        

    @property
    def payoff_qtd(self) -> dict:
        return self.__payoff_qtd

    @payoff_qtd.setter
    def payoff_qtd(self, value: dict):
        self._property_changed('payoff_qtd')
        self.__payoff_qtd = value        

    @property
    def loss(self) -> dict:
        return self.__loss

    @loss.setter
    def loss(self, value: dict):
        self._property_changed('loss')
        self.__loss = value        

    @property
    def midcurve_vol(self) -> dict:
        return self.__midcurve_vol

    @midcurve_vol.setter
    def midcurve_vol(self, value: dict):
        self._property_changed('midcurve_vol')
        self.__midcurve_vol = value        

    @property
    def sell6bps(self) -> dict:
        return self.__sell6bps

    @sell6bps.setter
    def sell6bps(self, value: dict):
        self._property_changed('sell6bps')
        self.__sell6bps = value        

    @property
    def trading_cost_pnl(self) -> dict:
        return self.__trading_cost_pnl

    @trading_cost_pnl.setter
    def trading_cost_pnl(self, value: dict):
        self._property_changed('trading_cost_pnl')
        self.__trading_cost_pnl = value        

    @property
    def price_notation_type(self) -> dict:
        return self.__price_notation_type

    @price_notation_type.setter
    def price_notation_type(self, value: dict):
        self._property_changed('price_notation_type')
        self.__price_notation_type = value        

    @property
    def price(self) -> dict:
        return self.__price

    @price.setter
    def price(self, value: dict):
        self._property_changed('price')
        self.__price = value        

    @property
    def payment_quantity(self) -> dict:
        return self.__payment_quantity

    @payment_quantity.setter
    def payment_quantity(self, value: dict):
        self._property_changed('payment_quantity')
        self.__payment_quantity = value        

    @property
    def redemption_date(self) -> dict:
        return self.__redemption_date

    @redemption_date.setter
    def redemption_date(self, value: dict):
        self._property_changed('redemption_date')
        self.__redemption_date = value        

    @property
    def leg2_notional_currency(self) -> dict:
        return self.__leg2_notional_currency

    @leg2_notional_currency.setter
    def leg2_notional_currency(self, value: dict):
        self._property_changed('leg2_notional_currency')
        self.__leg2_notional_currency = value        

    @property
    def sub_region(self) -> dict:
        return self.__sub_region

    @sub_region.setter
    def sub_region(self, value: dict):
        self._property_changed('sub_region')
        self.__sub_region = value        

    @property
    def benchmark(self) -> dict:
        return self.__benchmark

    @benchmark.setter
    def benchmark(self, value: dict):
        self._property_changed('benchmark')
        self.__benchmark = value        

    @property
    def tcm_cost_participation_rate15_pct(self) -> dict:
        return self.__tcm_cost_participation_rate15_pct

    @tcm_cost_participation_rate15_pct.setter
    def tcm_cost_participation_rate15_pct(self, value: dict):
        self._property_changed('tcm_cost_participation_rate15_pct')
        self.__tcm_cost_participation_rate15_pct = value        

    @property
    def fiscal_year(self) -> dict:
        return self.__fiscal_year

    @fiscal_year.setter
    def fiscal_year(self, value: dict):
        self._property_changed('fiscal_year')
        self.__fiscal_year = value        

    @property
    def recall_date(self) -> dict:
        return self.__recall_date

    @recall_date.setter
    def recall_date(self, value: dict):
        self._property_changed('recall_date')
        self.__recall_date = value        

    @property
    def esg_metric_value(self) -> dict:
        return self.__esg_metric_value

    @esg_metric_value.setter
    def esg_metric_value(self, value: dict):
        self._property_changed('esg_metric_value')
        self.__esg_metric_value = value        

    @property
    def internal(self) -> dict:
        return self.__internal

    @internal.setter
    def internal(self, value: dict):
        self._property_changed('internal')
        self.__internal = value        

    @property
    def gender(self) -> dict:
        return self.__gender

    @gender.setter
    def gender(self, value: dict):
        self._property_changed('gender')
        self.__gender = value        

    @property
    def asset_classifications_gics_industry(self) -> dict:
        return self.__asset_classifications_gics_industry

    @asset_classifications_gics_industry.setter
    def asset_classifications_gics_industry(self, value: dict):
        self._property_changed('asset_classifications_gics_industry')
        self.__asset_classifications_gics_industry = value        

    @property
    def adjusted_bid_price(self) -> dict:
        return self.__adjusted_bid_price

    @adjusted_bid_price.setter
    def adjusted_bid_price(self, value: dict):
        self._property_changed('adjusted_bid_price')
        self.__adjusted_bid_price = value        

    @property
    def low_unadjusted(self) -> dict:
        return self.__low_unadjusted

    @low_unadjusted.setter
    def low_unadjusted(self, value: dict):
        self._property_changed('low_unadjusted')
        self.__low_unadjusted = value        

    @property
    def macs_secondary_asset_class(self) -> dict:
        return self.__macs_secondary_asset_class

    @macs_secondary_asset_class.setter
    def macs_secondary_asset_class(self, value: dict):
        self._property_changed('macs_secondary_asset_class')
        self.__macs_secondary_asset_class = value        

    @property
    def confirmed_per_million(self) -> dict:
        return self.__confirmed_per_million

    @confirmed_per_million.setter
    def confirmed_per_million(self, value: dict):
        self._property_changed('confirmed_per_million')
        self.__confirmed_per_million = value        

    @property
    def data_source_id(self) -> dict:
        return self.__data_source_id

    @data_source_id.setter
    def data_source_id(self, value: dict):
        self._property_changed('data_source_id')
        self.__data_source_id = value        

    @property
    def integrated_score(self) -> dict:
        return self.__integrated_score

    @integrated_score.setter
    def integrated_score(self, value: dict):
        self._property_changed('integrated_score')
        self.__integrated_score = value        

    @property
    def buy7bps(self) -> dict:
        return self.__buy7bps

    @buy7bps.setter
    def buy7bps(self, value: dict):
        self._property_changed('buy7bps')
        self.__buy7bps = value        

    @property
    def arrival_mid_unrealized_cash(self) -> dict:
        return self.__arrival_mid_unrealized_cash

    @arrival_mid_unrealized_cash.setter
    def arrival_mid_unrealized_cash(self, value: dict):
        self._property_changed('arrival_mid_unrealized_cash')
        self.__arrival_mid_unrealized_cash = value        

    @property
    def knock_in_price(self) -> dict:
        return self.__knock_in_price

    @knock_in_price.setter
    def knock_in_price(self, value: dict):
        self._property_changed('knock_in_price')
        self.__knock_in_price = value        

    @property
    def event(self) -> dict:
        return self.__event

    @event.setter
    def event(self, value: dict):
        self._property_changed('event')
        self.__event = value        

    @property
    def is_intraday_auction(self) -> dict:
        return self.__is_intraday_auction

    @is_intraday_auction.setter
    def is_intraday_auction(self, value: dict):
        self._property_changed('is_intraday_auction')
        self.__is_intraday_auction = value        

    @property
    def location_name(self) -> dict:
        return self.__location_name

    @location_name.setter
    def location_name(self, value: dict):
        self._property_changed('location_name')
        self.__location_name = value        

    @property
    def coupon(self) -> dict:
        return self.__coupon

    @coupon.setter
    def coupon(self, value: dict):
        self._property_changed('coupon')
        self.__coupon = value        

    @property
    def percentage_auction_executed_quantity(self) -> dict:
        return self.__percentage_auction_executed_quantity

    @percentage_auction_executed_quantity.setter
    def percentage_auction_executed_quantity(self, value: dict):
        self._property_changed('percentage_auction_executed_quantity')
        self.__percentage_auction_executed_quantity = value        

    @property
    def avg_yield7_day(self) -> dict:
        return self.__avg_yield7_day

    @avg_yield7_day.setter
    def avg_yield7_day(self, value: dict):
        self._property_changed('avg_yield7_day')
        self.__avg_yield7_day = value        

    @property
    def original_dissemination_id(self) -> dict:
        return self.__original_dissemination_id

    @original_dissemination_id.setter
    def original_dissemination_id(self, value: dict):
        self._property_changed('original_dissemination_id')
        self.__original_dissemination_id = value        

    @property
    def total_on_vent(self) -> dict:
        return self.__total_on_vent

    @total_on_vent.setter
    def total_on_vent(self, value: dict):
        self._property_changed('total_on_vent')
        self.__total_on_vent = value        

    @property
    def twap_unrealized_cash(self) -> dict:
        return self.__twap_unrealized_cash

    @twap_unrealized_cash.setter
    def twap_unrealized_cash(self, value: dict):
        self._property_changed('twap_unrealized_cash')
        self.__twap_unrealized_cash = value        

    @property
    def sts_credit_market(self) -> dict:
        return self.__sts_credit_market

    @sts_credit_market.setter
    def sts_credit_market(self, value: dict):
        self._property_changed('sts_credit_market')
        self.__sts_credit_market = value        

    @property
    def ons_code(self) -> dict:
        return self.__ons_code

    @ons_code.setter
    def ons_code(self, value: dict):
        self._property_changed('ons_code')
        self.__ons_code = value        

    @property
    def passive_touch_fills_percentage(self) -> dict:
        return self.__passive_touch_fills_percentage

    @passive_touch_fills_percentage.setter
    def passive_touch_fills_percentage(self, value: dict):
        self._property_changed('passive_touch_fills_percentage')
        self.__passive_touch_fills_percentage = value        

    @property
    def seniority(self) -> dict:
        return self.__seniority

    @seniority.setter
    def seniority(self, value: dict):
        self._property_changed('seniority')
        self.__seniority = value        

    @property
    def leg1_index(self) -> dict:
        return self.__leg1_index

    @leg1_index.setter
    def leg1_index(self, value: dict):
        self._property_changed('leg1_index')
        self.__leg1_index = value        

    @property
    def high_unadjusted(self) -> dict:
        return self.__high_unadjusted

    @high_unadjusted.setter
    def high_unadjusted(self, value: dict):
        self._property_changed('high_unadjusted')
        self.__high_unadjusted = value        

    @property
    def submission_event(self) -> dict:
        return self.__submission_event

    @submission_event.setter
    def submission_event(self, value: dict):
        self._property_changed('submission_event')
        self.__submission_event = value        

    @property
    def tv_product_mnemonic(self) -> dict:
        return self.__tv_product_mnemonic

    @tv_product_mnemonic.setter
    def tv_product_mnemonic(self, value: dict):
        self._property_changed('tv_product_mnemonic')
        self.__tv_product_mnemonic = value        

    @property
    def avg_trade_rate_label(self) -> tuple:
        return self.__avg_trade_rate_label

    @avg_trade_rate_label.setter
    def avg_trade_rate_label(self, value: tuple):
        self._property_changed('avg_trade_rate_label')
        self.__avg_trade_rate_label = value        

    @property
    def last_activity_date(self) -> dict:
        return self.__last_activity_date

    @last_activity_date.setter
    def last_activity_date(self, value: dict):
        self._property_changed('last_activity_date')
        self.__last_activity_date = value        

    @property
    def price_to_cash(self) -> dict:
        return self.__price_to_cash

    @price_to_cash.setter
    def price_to_cash(self, value: dict):
        self._property_changed('price_to_cash')
        self.__price_to_cash = value        

    @property
    def buy10cents(self) -> dict:
        return self.__buy10cents

    @buy10cents.setter
    def buy10cents(self, value: dict):
        self._property_changed('buy10cents')
        self.__buy10cents = value        

    @property
    def nav_spread(self) -> dict:
        return self.__nav_spread

    @nav_spread.setter
    def nav_spread(self, value: dict):
        self._property_changed('nav_spread')
        self.__nav_spread = value        

    @property
    def venue_mic(self) -> dict:
        return self.__venue_mic

    @venue_mic.setter
    def venue_mic(self, value: dict):
        self._property_changed('venue_mic')
        self.__venue_mic = value        

    @property
    def dollar_total_return(self) -> dict:
        return self.__dollar_total_return

    @dollar_total_return.setter
    def dollar_total_return(self, value: dict):
        self._property_changed('dollar_total_return')
        self.__dollar_total_return = value        

    @property
    def block_unit(self) -> dict:
        return self.__block_unit

    @block_unit.setter
    def block_unit(self, value: dict):
        self._property_changed('block_unit')
        self.__block_unit = value        

    @property
    def mid_spread(self) -> dict:
        return self.__mid_spread

    @mid_spread.setter
    def mid_spread(self, value: dict):
        self._property_changed('mid_spread')
        self.__mid_spread = value        

    @property
    def istat_province_code(self) -> dict:
        return self.__istat_province_code

    @istat_province_code.setter
    def istat_province_code(self, value: dict):
        self._property_changed('istat_province_code')
        self.__istat_province_code = value        

    @property
    def total_recovered_by_state(self) -> dict:
        return self.__total_recovered_by_state

    @total_recovered_by_state.setter
    def total_recovered_by_state(self, value: dict):
        self._property_changed('total_recovered_by_state')
        self.__total_recovered_by_state = value        

    @property
    def repurchase_rate(self) -> dict:
        return self.__repurchase_rate

    @repurchase_rate.setter
    def repurchase_rate(self, value: dict):
        self._property_changed('repurchase_rate')
        self.__repurchase_rate = value        

    @property
    def data_source(self) -> dict:
        return self.__data_source

    @data_source.setter
    def data_source(self, value: dict):
        self._property_changed('data_source')
        self.__data_source = value        

    @property
    def total_being_tested(self) -> dict:
        return self.__total_being_tested

    @total_being_tested.setter
    def total_being_tested(self, value: dict):
        self._property_changed('total_being_tested')
        self.__total_being_tested = value        

    @property
    def cleared_or_bilateral(self) -> dict:
        return self.__cleared_or_bilateral

    @cleared_or_bilateral.setter
    def cleared_or_bilateral(self, value: dict):
        self._property_changed('cleared_or_bilateral')
        self.__cleared_or_bilateral = value        

    @property
    def metric_name(self) -> dict:
        return self.__metric_name

    @metric_name.setter
    def metric_name(self, value: dict):
        self._property_changed('metric_name')
        self.__metric_name = value        

    @property
    def ask_gspread(self) -> dict:
        return self.__ask_gspread

    @ask_gspread.setter
    def ask_gspread(self, value: dict):
        self._property_changed('ask_gspread')
        self.__ask_gspread = value        

    @property
    def forecast_hour(self) -> dict:
        return self.__forecast_hour

    @forecast_hour.setter
    def forecast_hour(self, value: dict):
        self._property_changed('forecast_hour')
        self.__forecast_hour = value        

    @property
    def leg2_payment_type(self) -> dict:
        return self.__leg2_payment_type

    @leg2_payment_type.setter
    def leg2_payment_type(self, value: dict):
        self._property_changed('leg2_payment_type')
        self.__leg2_payment_type = value        

    @property
    def cal_spread_mis_pricing(self) -> dict:
        return self.__cal_spread_mis_pricing

    @cal_spread_mis_pricing.setter
    def cal_spread_mis_pricing(self, value: dict):
        self._property_changed('cal_spread_mis_pricing')
        self.__cal_spread_mis_pricing = value        

    @property
    def total_tested_negative(self) -> dict:
        return self.__total_tested_negative

    @total_tested_negative.setter
    def total_tested_negative(self, value: dict):
        self._property_changed('total_tested_negative')
        self.__total_tested_negative = value        

    @property
    def rate366(self) -> dict:
        return self.__rate366

    @rate366.setter
    def rate366(self, value: dict):
        self._property_changed('rate366')
        self.__rate366 = value        

    @property
    def platform(self) -> dict:
        return self.__platform

    @platform.setter
    def platform(self, value: dict):
        self._property_changed('platform')
        self.__platform = value        

    @property
    def rate365(self) -> dict:
        return self.__rate365

    @rate365.setter
    def rate365(self, value: dict):
        self._property_changed('rate365')
        self.__rate365 = value        

    @property
    def fixed_rate_frequency(self) -> dict:
        return self.__fixed_rate_frequency

    @fixed_rate_frequency.setter
    def fixed_rate_frequency(self, value: dict):
        self._property_changed('fixed_rate_frequency')
        self.__fixed_rate_frequency = value        

    @property
    def rate360(self) -> dict:
        return self.__rate360

    @rate360.setter
    def rate360(self, value: dict):
        self._property_changed('rate360')
        self.__rate360 = value        

    @property
    def is_continuous(self) -> dict:
        return self.__is_continuous

    @is_continuous.setter
    def is_continuous(self, value: dict):
        self._property_changed('is_continuous')
        self.__is_continuous = value        

    @property
    def value(self) -> dict:
        return self.__value

    @value.setter
    def value(self, value: dict):
        self._property_changed('value')
        self.__value = value        

    @property
    def payer_designated_maturity(self) -> dict:
        return self.__payer_designated_maturity

    @payer_designated_maturity.setter
    def payer_designated_maturity(self, value: dict):
        self._property_changed('payer_designated_maturity')
        self.__payer_designated_maturity = value        

    @property
    def product_type(self) -> dict:
        return self.__product_type

    @product_type.setter
    def product_type(self, value: dict):
        self._property_changed('product_type')
        self.__product_type = value        

    @property
    def mdv22_day(self) -> dict:
        return self.__mdv22_day

    @mdv22_day.setter
    def mdv22_day(self, value: dict):
        self._property_changed('mdv22_day')
        self.__mdv22_day = value        

    @property
    def twap_realized_bps(self) -> dict:
        return self.__twap_realized_bps

    @twap_realized_bps.setter
    def twap_realized_bps(self, value: dict):
        self._property_changed('twap_realized_bps')
        self.__twap_realized_bps = value        

    @property
    def test_measure_label(self) -> dict:
        return self.__test_measure_label

    @test_measure_label.setter
    def test_measure_label(self, value: dict):
        self._property_changed('test_measure_label')
        self.__test_measure_label = value        

    @property
    def quantity(self) -> dict:
        return self.__quantity

    @quantity.setter
    def quantity(self, value: dict):
        self._property_changed('quantity')
        self.__quantity = value        

    @property
    def report_id(self) -> dict:
        return self.__report_id

    @report_id.setter
    def report_id(self, value: dict):
        self._property_changed('report_id')
        self.__report_id = value        

    @property
    def index_weight(self) -> dict:
        return self.__index_weight

    @index_weight.setter
    def index_weight(self, value: dict):
        self._property_changed('index_weight')
        self.__index_weight = value        

    @property
    def macs_primary_asset_class(self) -> dict:
        return self.__macs_primary_asset_class

    @macs_primary_asset_class.setter
    def macs_primary_asset_class(self, value: dict):
        self._property_changed('macs_primary_asset_class')
        self.__macs_primary_asset_class = value        

    @property
    def trader(self) -> dict:
        return self.__trader

    @trader.setter
    def trader(self, value: dict):
        self._property_changed('trader')
        self.__trader = value        

    @property
    def leg2_price_type(self) -> dict:
        return self.__leg2_price_type

    @leg2_price_type.setter
    def leg2_price_type(self, value: dict):
        self._property_changed('leg2_price_type')
        self.__leg2_price_type = value        

    @property
    def total_active(self) -> dict:
        return self.__total_active

    @total_active.setter
    def total_active(self, value: dict):
        self._property_changed('total_active')
        self.__total_active = value        

    @property
    def gsid2(self) -> dict:
        return self.__gsid2

    @gsid2.setter
    def gsid2(self, value: dict):
        self._property_changed('gsid2')
        self.__gsid2 = value        

    @property
    def matched_maturity_ois_swap_spread(self) -> dict:
        return self.__matched_maturity_ois_swap_spread

    @matched_maturity_ois_swap_spread.setter
    def matched_maturity_ois_swap_spread(self, value: dict):
        self._property_changed('matched_maturity_ois_swap_spread')
        self.__matched_maturity_ois_swap_spread = value        

    @property
    def valuation_date(self) -> dict:
        return self.__valuation_date

    @valuation_date.setter
    def valuation_date(self, value: dict):
        self._property_changed('valuation_date')
        self.__valuation_date = value        

    @property
    def restrict_gs_federation(self) -> dict:
        return self.__restrict_gs_federation

    @restrict_gs_federation.setter
    def restrict_gs_federation(self, value: dict):
        self._property_changed('restrict_gs_federation')
        self.__restrict_gs_federation = value        

    @property
    def position_source(self) -> dict:
        return self.__position_source

    @position_source.setter
    def position_source(self, value: dict):
        self._property_changed('position_source')
        self.__position_source = value        

    @property
    def tcm_cost_horizon6_hour(self) -> dict:
        return self.__tcm_cost_horizon6_hour

    @tcm_cost_horizon6_hour.setter
    def tcm_cost_horizon6_hour(self, value: dict):
        self._property_changed('tcm_cost_horizon6_hour')
        self.__tcm_cost_horizon6_hour = value        

    @property
    def buy200cents(self) -> dict:
        return self.__buy200cents

    @buy200cents.setter
    def buy200cents(self, value: dict):
        self._property_changed('buy200cents')
        self.__buy200cents = value        

    @property
    def vwap_unrealized_bps(self) -> dict:
        return self.__vwap_unrealized_bps

    @vwap_unrealized_bps.setter
    def vwap_unrealized_bps(self, value: dict):
        self._property_changed('vwap_unrealized_bps')
        self.__vwap_unrealized_bps = value        

    @property
    def price_to_book(self) -> dict:
        return self.__price_to_book

    @price_to_book.setter
    def price_to_book(self, value: dict):
        self._property_changed('price_to_book')
        self.__price_to_book = value        

    @property
    def isin(self) -> dict:
        return self.__isin

    @isin.setter
    def isin(self, value: dict):
        self._property_changed('isin')
        self.__isin = value        

    @property
    def pl_id(self) -> dict:
        return self.__pl_id

    @pl_id.setter
    def pl_id(self, value: dict):
        self._property_changed('pl_id')
        self.__pl_id = value        

    @property
    def last_returns_start_date(self) -> dict:
        return self.__last_returns_start_date

    @last_returns_start_date.setter
    def last_returns_start_date(self, value: dict):
        self._property_changed('last_returns_start_date')
        self.__last_returns_start_date = value        

    @property
    def collateral_value_variance(self) -> dict:
        return self.__collateral_value_variance

    @collateral_value_variance.setter
    def collateral_value_variance(self, value: dict):
        self._property_changed('collateral_value_variance')
        self.__collateral_value_variance = value        

    @property
    def year(self) -> dict:
        return self.__year

    @year.setter
    def year(self, value: dict):
        self._property_changed('year')
        self.__year = value        

    @property
    def forecast_period(self) -> dict:
        return self.__forecast_period

    @forecast_period.setter
    def forecast_period(self, value: dict):
        self._property_changed('forecast_period')
        self.__forecast_period = value        

    @property
    def call_first_date(self) -> dict:
        return self.__call_first_date

    @call_first_date.setter
    def call_first_date(self, value: dict):
        self._property_changed('call_first_date')
        self.__call_first_date = value        

    @property
    def data_set_ids(self) -> dict:
        return self.__data_set_ids

    @data_set_ids.setter
    def data_set_ids(self, value: dict):
        self._property_changed('data_set_ids')
        self.__data_set_ids = value        

    @property
    def economic_terms_hash(self) -> dict:
        return self.__economic_terms_hash

    @economic_terms_hash.setter
    def economic_terms_hash(self, value: dict):
        self._property_changed('economic_terms_hash')
        self.__economic_terms_hash = value        

    @property
    def num_beds(self) -> dict:
        return self.__num_beds

    @num_beds.setter
    def num_beds(self, value: dict):
        self._property_changed('num_beds')
        self.__num_beds = value        

    @property
    def sell20bps(self) -> dict:
        return self.__sell20bps

    @sell20bps.setter
    def sell20bps(self, value: dict):
        self._property_changed('sell20bps')
        self.__sell20bps = value        

    @property
    def client_type(self) -> dict:
        return self.__client_type

    @client_type.setter
    def client_type(self, value: dict):
        self._property_changed('client_type')
        self.__client_type = value        

    @property
    def percentage_close_executed_quantity(self) -> dict:
        return self.__percentage_close_executed_quantity

    @percentage_close_executed_quantity.setter
    def percentage_close_executed_quantity(self, value: dict):
        self._property_changed('percentage_close_executed_quantity')
        self.__percentage_close_executed_quantity = value        

    @property
    def macaulay_duration(self) -> dict:
        return self.__macaulay_duration

    @macaulay_duration.setter
    def macaulay_duration(self, value: dict):
        self._property_changed('macaulay_duration')
        self.__macaulay_duration = value        

    @property
    def available_inventory(self) -> dict:
        return self.__available_inventory

    @available_inventory.setter
    def available_inventory(self, value: dict):
        self._property_changed('available_inventory')
        self.__available_inventory = value        

    @property
    def est1_day_complete_pct(self) -> dict:
        return self.__est1_day_complete_pct

    @est1_day_complete_pct.setter
    def est1_day_complete_pct(self, value: dict):
        self._property_changed('est1_day_complete_pct')
        self.__est1_day_complete_pct = value        

    @property
    def relative_hit_rate_ytd(self) -> dict:
        return self.__relative_hit_rate_ytd

    @relative_hit_rate_ytd.setter
    def relative_hit_rate_ytd(self, value: dict):
        self._property_changed('relative_hit_rate_ytd')
        self.__relative_hit_rate_ytd = value        

    @property
    def created_by_id(self) -> dict:
        return self.__created_by_id

    @created_by_id.setter
    def created_by_id(self, value: dict):
        self._property_changed('created_by_id')
        self.__created_by_id = value        

    @property
    def market_data_type(self) -> dict:
        return self.__market_data_type

    @market_data_type.setter
    def market_data_type(self, value: dict):
        self._property_changed('market_data_type')
        self.__market_data_type = value        

    @property
    def real_short_rates_contribution(self) -> dict:
        return self.__real_short_rates_contribution

    @real_short_rates_contribution.setter
    def real_short_rates_contribution(self, value: dict):
        self._property_changed('real_short_rates_contribution')
        self.__real_short_rates_contribution = value        

    @property
    def metric_category(self) -> dict:
        return self.__metric_category

    @metric_category.setter
    def metric_category(self, value: dict):
        self._property_changed('metric_category')
        self.__metric_category = value        

    @property
    def annualized_carry(self) -> dict:
        return self.__annualized_carry

    @annualized_carry.setter
    def annualized_carry(self, value: dict):
        self._property_changed('annualized_carry')
        self.__annualized_carry = value        

    @property
    def value_previous(self) -> dict:
        return self.__value_previous

    @value_previous.setter
    def value_previous(self, value: dict):
        self._property_changed('value_previous')
        self.__value_previous = value        

    @property
    def transmission_classification(self) -> dict:
        return self.__transmission_classification

    @transmission_classification.setter
    def transmission_classification(self, value: dict):
        self._property_changed('transmission_classification')
        self.__transmission_classification = value        

    @property
    def avg_trade_rate(self) -> dict:
        return self.__avg_trade_rate

    @avg_trade_rate.setter
    def avg_trade_rate(self, value: dict):
        self._property_changed('avg_trade_rate')
        self.__avg_trade_rate = value        

    @property
    def short_level(self) -> dict:
        return self.__short_level

    @short_level.setter
    def short_level(self, value: dict):
        self._property_changed('short_level')
        self.__short_level = value        

    @property
    def version(self) -> dict:
        return self.__version

    @version.setter
    def version(self, value: dict):
        self._property_changed('version')
        self.__version = value        

    @property
    def category_type(self) -> dict:
        return self.__category_type

    @category_type.setter
    def category_type(self, value: dict):
        self._property_changed('category_type')
        self.__category_type = value        

    @property
    def policy_rate_expectation(self) -> dict:
        return self.__policy_rate_expectation

    @policy_rate_expectation.setter
    def policy_rate_expectation(self, value: dict):
        self._property_changed('policy_rate_expectation')
        self.__policy_rate_expectation = value        

    @property
    def upload_date(self) -> dict:
        return self.__upload_date

    @upload_date.setter
    def upload_date(self, value: dict):
        self._property_changed('upload_date')
        self.__upload_date = value        

    @property
    def block_off_facility(self) -> dict:
        return self.__block_off_facility

    @block_off_facility.setter
    def block_off_facility(self, value: dict):
        self._property_changed('block_off_facility')
        self.__block_off_facility = value        

    @property
    def unrealized_vwap_performance_usd(self) -> dict:
        return self.__unrealized_vwap_performance_usd

    @unrealized_vwap_performance_usd.setter
    def unrealized_vwap_performance_usd(self, value: dict):
        self._property_changed('unrealized_vwap_performance_usd')
        self.__unrealized_vwap_performance_usd = value        

    @property
    def pace_of_rollp75(self) -> dict:
        return self.__pace_of_rollp75

    @pace_of_rollp75.setter
    def pace_of_rollp75(self, value: dict):
        self._property_changed('pace_of_rollp75')
        self.__pace_of_rollp75 = value        

    @property
    def earnings_per_share_positive(self) -> dict:
        return self.__earnings_per_share_positive

    @earnings_per_share_positive.setter
    def earnings_per_share_positive(self, value: dict):
        self._property_changed('earnings_per_share_positive')
        self.__earnings_per_share_positive = value        

    @property
    def num_icu_beds(self) -> dict:
        return self.__num_icu_beds

    @num_icu_beds.setter
    def num_icu_beds(self, value: dict):
        self._property_changed('num_icu_beds')
        self.__num_icu_beds = value        

    @property
    def bucket_volume_in_percentage(self) -> dict:
        return self.__bucket_volume_in_percentage

    @bucket_volume_in_percentage.setter
    def bucket_volume_in_percentage(self, value: dict):
        self._property_changed('bucket_volume_in_percentage')
        self.__bucket_volume_in_percentage = value        

    @property
    def estimated_trading_cost(self) -> dict:
        return self.__estimated_trading_cost

    @estimated_trading_cost.setter
    def estimated_trading_cost(self, value: dict):
        self._property_changed('estimated_trading_cost')
        self.__estimated_trading_cost = value        

    @property
    def eid(self) -> dict:
        return self.__eid

    @eid.setter
    def eid(self, value: dict):
        self._property_changed('eid')
        self.__eid = value        

    @property
    def relative_return_qtd(self) -> dict:
        return self.__relative_return_qtd

    @relative_return_qtd.setter
    def relative_return_qtd(self, value: dict):
        self._property_changed('relative_return_qtd')
        self.__relative_return_qtd = value        

    @property
    def assessed_test_measure(self) -> dict:
        return self.__assessed_test_measure

    @assessed_test_measure.setter
    def assessed_test_measure(self, value: dict):
        self._property_changed('assessed_test_measure')
        self.__assessed_test_measure = value        

    @property
    def mkt_quoting_style(self) -> dict:
        return self.__mkt_quoting_style

    @mkt_quoting_style.setter
    def mkt_quoting_style(self, value: dict):
        self._property_changed('mkt_quoting_style')
        self.__mkt_quoting_style = value        

    @property
    def expiration_tenor(self) -> dict:
        return self.__expiration_tenor

    @expiration_tenor.setter
    def expiration_tenor(self, value: dict):
        self._property_changed('expiration_tenor')
        self.__expiration_tenor = value        

    @property
    def price_limit(self) -> dict:
        return self.__price_limit

    @price_limit.setter
    def price_limit(self, value: dict):
        self._property_changed('price_limit')
        self.__price_limit = value        

    @property
    def market_model_id(self) -> dict:
        return self.__market_model_id

    @market_model_id.setter
    def market_model_id(self, value: dict):
        self._property_changed('market_model_id')
        self.__market_model_id = value        

    @property
    def receiver_frequency(self) -> dict:
        return self.__receiver_frequency

    @receiver_frequency.setter
    def receiver_frequency(self, value: dict):
        self._property_changed('receiver_frequency')
        self.__receiver_frequency = value        

    @property
    def realized_correlation(self) -> dict:
        return self.__realized_correlation

    @realized_correlation.setter
    def realized_correlation(self, value: dict):
        self._property_changed('realized_correlation')
        self.__realized_correlation = value        

    @property
    def issue_status(self) -> dict:
        return self.__issue_status

    @issue_status.setter
    def issue_status(self, value: dict):
        self._property_changed('issue_status')
        self.__issue_status = value        

    @property
    def collateral_value_actual(self) -> dict:
        return self.__collateral_value_actual

    @collateral_value_actual.setter
    def collateral_value_actual(self, value: dict):
        self._property_changed('collateral_value_actual')
        self.__collateral_value_actual = value        

    @property
    def atm_fwd_rate(self) -> dict:
        return self.__atm_fwd_rate

    @atm_fwd_rate.setter
    def atm_fwd_rate(self, value: dict):
        self._property_changed('atm_fwd_rate')
        self.__atm_fwd_rate = value        

    @property
    def tcm_cost_participation_rate75_pct(self) -> dict:
        return self.__tcm_cost_participation_rate75_pct

    @tcm_cost_participation_rate75_pct.setter
    def tcm_cost_participation_rate75_pct(self, value: dict):
        self._property_changed('tcm_cost_participation_rate75_pct')
        self.__tcm_cost_participation_rate75_pct = value        

    @property
    def close(self) -> dict:
        return self.__close

    @close.setter
    def close(self, value: dict):
        self._property_changed('close')
        self.__close = value        

    @property
    def es_product_impact_score(self) -> dict:
        return self.__es_product_impact_score

    @es_product_impact_score.setter
    def es_product_impact_score(self, value: dict):
        self._property_changed('es_product_impact_score')
        self.__es_product_impact_score = value        

    @property
    def equity_vega(self) -> dict:
        return self.__equity_vega

    @equity_vega.setter
    def equity_vega(self, value: dict):
        self._property_changed('equity_vega')
        self.__equity_vega = value        

    @property
    def executed_fill_quantity(self) -> dict:
        return self.__executed_fill_quantity

    @executed_fill_quantity.setter
    def executed_fill_quantity(self, value: dict):
        self._property_changed('executed_fill_quantity')
        self.__executed_fill_quantity = value        

    @property
    def lender_payment(self) -> dict:
        return self.__lender_payment

    @lender_payment.setter
    def lender_payment(self, value: dict):
        self._property_changed('lender_payment')
        self.__lender_payment = value        

    @property
    def five_day_move(self) -> dict:
        return self.__five_day_move

    @five_day_move.setter
    def five_day_move(self, value: dict):
        self._property_changed('five_day_move')
        self.__five_day_move = value        

    @property
    def value_format(self) -> dict:
        return self.__value_format

    @value_format.setter
    def value_format(self, value: dict):
        self._property_changed('value_format')
        self.__value_format = value        

    @property
    def wind_chill_forecast(self) -> dict:
        return self.__wind_chill_forecast

    @wind_chill_forecast.setter
    def wind_chill_forecast(self, value: dict):
        self._property_changed('wind_chill_forecast')
        self.__wind_chill_forecast = value        

    @property
    def target_notional(self) -> dict:
        return self.__target_notional

    @target_notional.setter
    def target_notional(self, value: dict):
        self._property_changed('target_notional')
        self.__target_notional = value        

    @property
    def fill_leg_id(self) -> dict:
        return self.__fill_leg_id

    @fill_leg_id.setter
    def fill_leg_id(self, value: dict):
        self._property_changed('fill_leg_id')
        self.__fill_leg_id = value        

    @property
    def rationale(self) -> dict:
        return self.__rationale

    @rationale.setter
    def rationale(self, value: dict):
        self._property_changed('rationale')
        self.__rationale = value        

    @property
    def realized_twap_performance_bps(self) -> dict:
        return self.__realized_twap_performance_bps

    @realized_twap_performance_bps.setter
    def realized_twap_performance_bps(self, value: dict):
        self._property_changed('realized_twap_performance_bps')
        self.__realized_twap_performance_bps = value        

    @property
    def last_updated_since(self) -> dict:
        return self.__last_updated_since

    @last_updated_since.setter
    def last_updated_since(self, value: dict):
        self._property_changed('last_updated_since')
        self.__last_updated_since = value        

    @property
    def total_tests(self) -> dict:
        return self.__total_tests

    @total_tests.setter
    def total_tests(self, value: dict):
        self._property_changed('total_tests')
        self.__total_tests = value        

    @property
    def equities_contribution(self) -> dict:
        return self.__equities_contribution

    @equities_contribution.setter
    def equities_contribution(self, value: dict):
        self._property_changed('equities_contribution')
        self.__equities_contribution = value        

    @property
    def simon_id(self) -> dict:
        return self.__simon_id

    @simon_id.setter
    def simon_id(self, value: dict):
        self._property_changed('simon_id')
        self.__simon_id = value        

    @property
    def congestion(self) -> dict:
        return self.__congestion

    @congestion.setter
    def congestion(self, value: dict):
        self._property_changed('congestion')
        self.__congestion = value        

    @property
    def notes(self) -> dict:
        return self.__notes

    @notes.setter
    def notes(self, value: dict):
        self._property_changed('notes')
        self.__notes = value        

    @property
    def total_probable_senior_home(self) -> dict:
        return self.__total_probable_senior_home

    @total_probable_senior_home.setter
    def total_probable_senior_home(self, value: dict):
        self._property_changed('total_probable_senior_home')
        self.__total_probable_senior_home = value        

    @property
    def event_category(self) -> dict:
        return self.__event_category

    @event_category.setter
    def event_category(self, value: dict):
        self._property_changed('event_category')
        self.__event_category = value        

    @property
    def average_fill_rate(self) -> dict:
        return self.__average_fill_rate

    @average_fill_rate.setter
    def average_fill_rate(self, value: dict):
        self._property_changed('average_fill_rate')
        self.__average_fill_rate = value        

    @property
    def unadjusted_open(self) -> dict:
        return self.__unadjusted_open

    @unadjusted_open.setter
    def unadjusted_open(self, value: dict):
        self._property_changed('unadjusted_open')
        self.__unadjusted_open = value        

    @property
    def criticality(self) -> dict:
        return self.__criticality

    @criticality.setter
    def criticality(self, value: dict):
        self._property_changed('criticality')
        self.__criticality = value        

    @property
    def bid_ask_spread(self) -> dict:
        return self.__bid_ask_spread

    @bid_ask_spread.setter
    def bid_ask_spread(self, value: dict):
        self._property_changed('bid_ask_spread')
        self.__bid_ask_spread = value        

    @property
    def arrival_mid_unrealized_bps(self) -> dict:
        return self.__arrival_mid_unrealized_bps

    @arrival_mid_unrealized_bps.setter
    def arrival_mid_unrealized_bps(self, value: dict):
        self._property_changed('arrival_mid_unrealized_bps')
        self.__arrival_mid_unrealized_bps = value        

    @property
    def option_type(self) -> dict:
        return self.__option_type

    @option_type.setter
    def option_type(self, value: dict):
        self._property_changed('option_type')
        self.__option_type = value        

    @property
    def termination_date(self) -> dict:
        return self.__termination_date

    @termination_date.setter
    def termination_date(self, value: dict):
        self._property_changed('termination_date')
        self.__termination_date = value        

    @property
    def queries_per_second(self) -> dict:
        return self.__queries_per_second

    @queries_per_second.setter
    def queries_per_second(self, value: dict):
        self._property_changed('queries_per_second')
        self.__queries_per_second = value        

    @property
    def liquidity_type(self) -> dict:
        return self.__liquidity_type

    @liquidity_type.setter
    def liquidity_type(self, value: dict):
        self._property_changed('liquidity_type')
        self.__liquidity_type = value        

    @property
    def credit_limit(self) -> dict:
        return self.__credit_limit

    @credit_limit.setter
    def credit_limit(self, value: dict):
        self._property_changed('credit_limit')
        self.__credit_limit = value        

    @property
    def rank_qtd(self) -> dict:
        return self.__rank_qtd

    @rank_qtd.setter
    def rank_qtd(self, value: dict):
        self._property_changed('rank_qtd')
        self.__rank_qtd = value        

    @property
    def combined_key(self) -> dict:
        return self.__combined_key

    @combined_key.setter
    def combined_key(self, value: dict):
        self._property_changed('combined_key')
        self.__combined_key = value        

    @property
    def gir_fx_forecast(self) -> dict:
        return self.__gir_fx_forecast

    @gir_fx_forecast.setter
    def gir_fx_forecast(self, value: dict):
        self._property_changed('gir_fx_forecast')
        self.__gir_fx_forecast = value        

    @property
    def effective_tenor(self) -> dict:
        return self.__effective_tenor

    @effective_tenor.setter
    def effective_tenor(self, value: dict):
        self._property_changed('effective_tenor')
        self.__effective_tenor = value        

    @property
    def gir_commodities_forecast(self) -> dict:
        return self.__gir_commodities_forecast

    @gir_commodities_forecast.setter
    def gir_commodities_forecast(self, value: dict):
        self._property_changed('gir_commodities_forecast')
        self.__gir_commodities_forecast = value        

    @property
    def relative_humidity_daily_forecast(self) -> dict:
        return self.__relative_humidity_daily_forecast

    @relative_humidity_daily_forecast.setter
    def relative_humidity_daily_forecast(self, value: dict):
        self._property_changed('relative_humidity_daily_forecast')
        self.__relative_humidity_daily_forecast = value        

    @property
    def std30_days_subsidized_yield(self) -> dict:
        return self.__std30_days_subsidized_yield

    @std30_days_subsidized_yield.setter
    def std30_days_subsidized_yield(self, value: dict):
        self._property_changed('std30_days_subsidized_yield')
        self.__std30_days_subsidized_yield = value        

    @property
    def annualized_tracking_error(self) -> dict:
        return self.__annualized_tracking_error

    @annualized_tracking_error.setter
    def annualized_tracking_error(self, value: dict):
        self._property_changed('annualized_tracking_error')
        self.__annualized_tracking_error = value        

    @property
    def future_month_f26(self) -> dict:
        return self.__future_month_f26

    @future_month_f26.setter
    def future_month_f26(self, value: dict):
        self._property_changed('future_month_f26')
        self.__future_month_f26 = value        

    @property
    def future_month_f25(self) -> dict:
        return self.__future_month_f25

    @future_month_f25.setter
    def future_month_f25(self, value: dict):
        self._property_changed('future_month_f25')
        self.__future_month_f25 = value        

    @property
    def vol_swap(self) -> dict:
        return self.__vol_swap

    @vol_swap.setter
    def vol_swap(self, value: dict):
        self._property_changed('vol_swap')
        self.__vol_swap = value        

    @property
    def future_month_f24(self) -> dict:
        return self.__future_month_f24

    @future_month_f24.setter
    def future_month_f24(self, value: dict):
        self._property_changed('future_month_f24')
        self.__future_month_f24 = value        

    @property
    def heat_index_daily_forecast(self) -> dict:
        return self.__heat_index_daily_forecast

    @heat_index_daily_forecast.setter
    def heat_index_daily_forecast(self, value: dict):
        self._property_changed('heat_index_daily_forecast')
        self.__heat_index_daily_forecast = value        

    @property
    def future_month_f23(self) -> dict:
        return self.__future_month_f23

    @future_month_f23.setter
    def future_month_f23(self, value: dict):
        self._property_changed('future_month_f23')
        self.__future_month_f23 = value        

    @property
    def real_fci(self) -> dict:
        return self.__real_fci

    @real_fci.setter
    def real_fci(self, value: dict):
        self._property_changed('real_fci')
        self.__real_fci = value        

    @property
    def block_trades_and_large_notional_off_facility_swaps(self) -> dict:
        return self.__block_trades_and_large_notional_off_facility_swaps

    @block_trades_and_large_notional_off_facility_swaps.setter
    def block_trades_and_large_notional_off_facility_swaps(self, value: dict):
        self._property_changed('block_trades_and_large_notional_off_facility_swaps')
        self.__block_trades_and_large_notional_off_facility_swaps = value        

    @property
    def future_month_f22(self) -> dict:
        return self.__future_month_f22

    @future_month_f22.setter
    def future_month_f22(self, value: dict):
        self._property_changed('future_month_f22')
        self.__future_month_f22 = value        

    @property
    def buy1point5bps(self) -> dict:
        return self.__buy1point5bps

    @buy1point5bps.setter
    def buy1point5bps(self, value: dict):
        self._property_changed('buy1point5bps')
        self.__buy1point5bps = value        

    @property
    def future_month_f21(self) -> dict:
        return self.__future_month_f21

    @future_month_f21.setter
    def future_month_f21(self, value: dict):
        self._property_changed('future_month_f21')
        self.__future_month_f21 = value        

    @property
    def expiration_settlement_date(self) -> dict:
        return self.__expiration_settlement_date

    @expiration_settlement_date.setter
    def expiration_settlement_date(self, value: dict):
        self._property_changed('expiration_settlement_date')
        self.__expiration_settlement_date = value        

    @property
    def absolute_return_qtd(self) -> dict:
        return self.__absolute_return_qtd

    @absolute_return_qtd.setter
    def absolute_return_qtd(self, value: dict):
        self._property_changed('absolute_return_qtd')
        self.__absolute_return_qtd = value        

    @property
    def gross_exposure(self) -> dict:
        return self.__gross_exposure

    @gross_exposure.setter
    def gross_exposure(self, value: dict):
        self._property_changed('gross_exposure')
        self.__gross_exposure = value        

    @property
    def volume(self) -> dict:
        return self.__volume

    @volume.setter
    def volume(self, value: dict):
        self._property_changed('volume')
        self.__volume = value        

    @property
    def adv(self) -> dict:
        return self.__adv

    @adv.setter
    def adv(self, value: dict):
        self._property_changed('adv')
        self.__adv = value        

    @property
    def short_conviction_medium(self) -> dict:
        return self.__short_conviction_medium

    @short_conviction_medium.setter
    def short_conviction_medium(self, value: dict):
        self._property_changed('short_conviction_medium')
        self.__short_conviction_medium = value        

    @property
    def complete_test_measure(self) -> dict:
        return self.__complete_test_measure

    @complete_test_measure.setter
    def complete_test_measure(self, value: dict):
        self._property_changed('complete_test_measure')
        self.__complete_test_measure = value        

    @property
    def exchange(self) -> dict:
        return self.__exchange

    @exchange.setter
    def exchange(self, value: dict):
        self._property_changed('exchange')
        self.__exchange = value        

    @property
    def es_policy_score(self) -> dict:
        return self.__es_policy_score

    @es_policy_score.setter
    def es_policy_score(self, value: dict):
        self._property_changed('es_policy_score')
        self.__es_policy_score = value        

    @property
    def roll_volume_std(self) -> dict:
        return self.__roll_volume_std

    @roll_volume_std.setter
    def roll_volume_std(self, value: dict):
        self._property_changed('roll_volume_std')
        self.__roll_volume_std = value        

    @property
    def temperature_daily_forecast(self) -> dict:
        return self.__temperature_daily_forecast

    @temperature_daily_forecast.setter
    def temperature_daily_forecast(self, value: dict):
        self._property_changed('temperature_daily_forecast')
        self.__temperature_daily_forecast = value        

    @property
    def relative_payoff_qtd(self) -> dict:
        return self.__relative_payoff_qtd

    @relative_payoff_qtd.setter
    def relative_payoff_qtd(self, value: dict):
        self._property_changed('relative_payoff_qtd')
        self.__relative_payoff_qtd = value        

    @property
    def on_loan_percentage(self) -> dict:
        return self.__on_loan_percentage

    @on_loan_percentage.setter
    def on_loan_percentage(self, value: dict):
        self._property_changed('on_loan_percentage')
        self.__on_loan_percentage = value        

    @property
    def twap_remaining_slices(self) -> dict:
        return self.__twap_remaining_slices

    @twap_remaining_slices.setter
    def twap_remaining_slices(self, value: dict):
        self._property_changed('twap_remaining_slices')
        self.__twap_remaining_slices = value        

    @property
    def fair_variance(self) -> dict:
        return self.__fair_variance

    @fair_variance.setter
    def fair_variance(self, value: dict):
        self._property_changed('fair_variance')
        self.__fair_variance = value        

    @property
    def hit_rate_wtd(self) -> dict:
        return self.__hit_rate_wtd

    @hit_rate_wtd.setter
    def hit_rate_wtd(self, value: dict):
        self._property_changed('hit_rate_wtd')
        self.__hit_rate_wtd = value        

    @property
    def previous_close_realized_cash(self) -> dict:
        return self.__previous_close_realized_cash

    @previous_close_realized_cash.setter
    def previous_close_realized_cash(self, value: dict):
        self._property_changed('previous_close_realized_cash')
        self.__previous_close_realized_cash = value        

    @property
    def realized_volatility(self) -> dict:
        return self.__realized_volatility

    @realized_volatility.setter
    def realized_volatility(self, value: dict):
        self._property_changed('realized_volatility')
        self.__realized_volatility = value        

    @property
    def unexecuted_quantity(self) -> dict:
        return self.__unexecuted_quantity

    @unexecuted_quantity.setter
    def unexecuted_quantity(self, value: dict):
        self._property_changed('unexecuted_quantity')
        self.__unexecuted_quantity = value        

    @property
    def proceeds_asset_swap_spread1m(self) -> dict:
        return self.__proceeds_asset_swap_spread1m

    @proceeds_asset_swap_spread1m.setter
    def proceeds_asset_swap_spread1m(self, value: dict):
        self._property_changed('proceeds_asset_swap_spread1m')
        self.__proceeds_asset_swap_spread1m = value        

    @property
    def clone_parent_id(self) -> dict:
        return self.__clone_parent_id

    @clone_parent_id.setter
    def clone_parent_id(self, value: dict):
        self._property_changed('clone_parent_id')
        self.__clone_parent_id = value        

    @property
    def wind_speed_hourly_forecast(self) -> dict:
        return self.__wind_speed_hourly_forecast

    @wind_speed_hourly_forecast.setter
    def wind_speed_hourly_forecast(self, value: dict):
        self._property_changed('wind_speed_hourly_forecast')
        self.__wind_speed_hourly_forecast = value        

    @property
    def etf_flow_ratio(self) -> dict:
        return self.__etf_flow_ratio

    @etf_flow_ratio.setter
    def etf_flow_ratio(self, value: dict):
        self._property_changed('etf_flow_ratio')
        self.__etf_flow_ratio = value        

    @property
    def asset_parameters_receiver_rate_option(self) -> dict:
        return self.__asset_parameters_receiver_rate_option

    @asset_parameters_receiver_rate_option.setter
    def asset_parameters_receiver_rate_option(self, value: dict):
        self._property_changed('asset_parameters_receiver_rate_option')
        self.__asset_parameters_receiver_rate_option = value        

    @property
    def buy60cents(self) -> dict:
        return self.__buy60cents

    @buy60cents.setter
    def buy60cents(self, value: dict):
        self._property_changed('buy60cents')
        self.__buy60cents = value        

    @property
    def security_sub_type_id(self) -> dict:
        return self.__security_sub_type_id

    @security_sub_type_id.setter
    def security_sub_type_id(self, value: dict):
        self._property_changed('security_sub_type_id')
        self.__security_sub_type_id = value        

    @property
    def message(self) -> dict:
        return self.__message

    @message.setter
    def message(self, value: dict):
        self._property_changed('message')
        self.__message = value        

    @property
    def sts_rates_country(self) -> dict:
        return self.__sts_rates_country

    @sts_rates_country.setter
    def sts_rates_country(self, value: dict):
        self._property_changed('sts_rates_country')
        self.__sts_rates_country = value        

    @property
    def sell65cents(self) -> dict:
        return self.__sell65cents

    @sell65cents.setter
    def sell65cents(self, value: dict):
        self._property_changed('sell65cents')
        self.__sell65cents = value        

    @property
    def horizon(self) -> dict:
        return self.__horizon

    @horizon.setter
    def horizon(self, value: dict):
        self._property_changed('horizon')
        self.__horizon = value        

    @property
    def would_if_good_level(self) -> dict:
        return self.__would_if_good_level

    @would_if_good_level.setter
    def would_if_good_level(self, value: dict):
        self._property_changed('would_if_good_level')
        self.__would_if_good_level = value        

    @property
    def buffer_threshold_required(self) -> dict:
        return self.__buffer_threshold_required

    @buffer_threshold_required.setter
    def buffer_threshold_required(self, value: dict):
        self._property_changed('buffer_threshold_required')
        self.__buffer_threshold_required = value        

    @property
    def face_value(self) -> dict:
        return self.__face_value

    @face_value.setter
    def face_value(self, value: dict):
        self._property_changed('face_value')
        self.__face_value = value        

    @property
    def roll_volume_hist(self) -> dict:
        return self.__roll_volume_hist

    @roll_volume_hist.setter
    def roll_volume_hist(self, value: dict):
        self._property_changed('roll_volume_hist')
        self.__roll_volume_hist = value        

    @property
    def counter_party_status(self) -> dict:
        return self.__counter_party_status

    @counter_party_status.setter
    def counter_party_status(self, value: dict):
        self._property_changed('counter_party_status')
        self.__counter_party_status = value        

    @property
    def composite22_day_adv(self) -> dict:
        return self.__composite22_day_adv

    @composite22_day_adv.setter
    def composite22_day_adv(self, value: dict):
        self._property_changed('composite22_day_adv')
        self.__composite22_day_adv = value        

    @property
    def percentage_far_executed_quantity(self) -> dict:
        return self.__percentage_far_executed_quantity

    @percentage_far_executed_quantity.setter
    def percentage_far_executed_quantity(self, value: dict):
        self._property_changed('percentage_far_executed_quantity')
        self.__percentage_far_executed_quantity = value        

    @property
    def loan_spread_required(self) -> dict:
        return self.__loan_spread_required

    @loan_spread_required.setter
    def loan_spread_required(self, value: dict):
        self._property_changed('loan_spread_required')
        self.__loan_spread_required = value        

    @property
    def asset_class(self) -> dict:
        return self.__asset_class

    @asset_class.setter
    def asset_class(self, value: dict):
        self._property_changed('asset_class')
        self.__asset_class = value        

    @property
    def sovereign_spread_contribution(self) -> dict:
        return self.__sovereign_spread_contribution

    @sovereign_spread_contribution.setter
    def sovereign_spread_contribution(self, value: dict):
        self._property_changed('sovereign_spread_contribution')
        self.__sovereign_spread_contribution = value        

    @property
    def ric(self) -> dict:
        return self.__ric

    @ric.setter
    def ric(self, value: dict):
        self._property_changed('ric')
        self.__ric = value        

    @property
    def rate_type(self) -> dict:
        return self.__rate_type

    @rate_type.setter
    def rate_type(self, value: dict):
        self._property_changed('rate_type')
        self.__rate_type = value        

    @property
    def total_fatalities_senior_home(self) -> dict:
        return self.__total_fatalities_senior_home

    @total_fatalities_senior_home.setter
    def total_fatalities_senior_home(self, value: dict):
        self._property_changed('total_fatalities_senior_home')
        self.__total_fatalities_senior_home = value        

    @property
    def loan_status(self) -> dict:
        return self.__loan_status

    @loan_status.setter
    def loan_status(self, value: dict):
        self._property_changed('loan_status')
        self.__loan_status = value        

    @property
    def short_weight(self) -> dict:
        return self.__short_weight

    @short_weight.setter
    def short_weight(self, value: dict):
        self._property_changed('short_weight')
        self.__short_weight = value        

    @property
    def geography_id(self) -> dict:
        return self.__geography_id

    @geography_id.setter
    def geography_id(self, value: dict):
        self._property_changed('geography_id')
        self.__geography_id = value        

    @property
    def sell7point5bps(self) -> dict:
        return self.__sell7point5bps

    @sell7point5bps.setter
    def sell7point5bps(self, value: dict):
        self._property_changed('sell7point5bps')
        self.__sell7point5bps = value        

    @property
    def nav(self) -> dict:
        return self.__nav

    @nav.setter
    def nav(self, value: dict):
        self._property_changed('nav')
        self.__nav = value        

    @property
    def fiscal_quarter(self) -> dict:
        return self.__fiscal_quarter

    @fiscal_quarter.setter
    def fiscal_quarter(self, value: dict):
        self._property_changed('fiscal_quarter')
        self.__fiscal_quarter = value        

    @property
    def version_string(self) -> dict:
        return self.__version_string

    @version_string.setter
    def version_string(self, value: dict):
        self._property_changed('version_string')
        self.__version_string = value        

    @property
    def payoff_ytd(self) -> dict:
        return self.__payoff_ytd

    @payoff_ytd.setter
    def payoff_ytd(self, value: dict):
        self._property_changed('payoff_ytd')
        self.__payoff_ytd = value        

    @property
    def market_impact(self) -> dict:
        return self.__market_impact

    @market_impact.setter
    def market_impact(self, value: dict):
        self._property_changed('market_impact')
        self.__market_impact = value        

    @property
    def event_type(self) -> dict:
        return self.__event_type

    @event_type.setter
    def event_type(self, value: dict):
        self._property_changed('event_type')
        self.__event_type = value        

    @property
    def fill_price(self) -> dict:
        return self.__fill_price

    @fill_price.setter
    def fill_price(self, value: dict):
        self._property_changed('fill_price')
        self.__fill_price = value        

    @property
    def asset_count_long(self) -> dict:
        return self.__asset_count_long

    @asset_count_long.setter
    def asset_count_long(self, value: dict):
        self._property_changed('asset_count_long')
        self.__asset_count_long = value        

    @property
    def sell180cents(self) -> dict:
        return self.__sell180cents

    @sell180cents.setter
    def sell180cents(self, value: dict):
        self._property_changed('sell180cents')
        self.__sell180cents = value        

    @property
    def spot(self) -> dict:
        return self.__spot

    @spot.setter
    def spot(self, value: dict):
        self._property_changed('spot')
        self.__spot = value        

    @property
    def application_id(self) -> dict:
        return self.__application_id

    @application_id.setter
    def application_id(self, value: dict):
        self._property_changed('application_id')
        self.__application_id = value        

    @property
    def indicative_close_price(self) -> dict:
        return self.__indicative_close_price

    @indicative_close_price.setter
    def indicative_close_price(self, value: dict):
        self._property_changed('indicative_close_price')
        self.__indicative_close_price = value        

    @property
    def swap_spread(self) -> dict:
        return self.__swap_spread

    @swap_spread.setter
    def swap_spread(self, value: dict):
        self._property_changed('swap_spread')
        self.__swap_spread = value        

    @property
    def trading_restriction(self) -> dict:
        return self.__trading_restriction

    @trading_restriction.setter
    def trading_restriction(self, value: dict):
        self._property_changed('trading_restriction')
        self.__trading_restriction = value        

    @property
    def asset_parameters_pay_or_receive(self) -> dict:
        return self.__asset_parameters_pay_or_receive

    @asset_parameters_pay_or_receive.setter
    def asset_parameters_pay_or_receive(self, value: dict):
        self._property_changed('asset_parameters_pay_or_receive')
        self.__asset_parameters_pay_or_receive = value        

    @property
    def price_spot_entry_unit(self) -> dict:
        return self.__price_spot_entry_unit

    @price_spot_entry_unit.setter
    def price_spot_entry_unit(self, value: dict):
        self._property_changed('price_spot_entry_unit')
        self.__price_spot_entry_unit = value        

    @property
    def unrealized_arrival_performance_bps(self) -> dict:
        return self.__unrealized_arrival_performance_bps

    @unrealized_arrival_performance_bps.setter
    def unrealized_arrival_performance_bps(self, value: dict):
        self._property_changed('unrealized_arrival_performance_bps')
        self.__unrealized_arrival_performance_bps = value        

    @property
    def city(self) -> dict:
        return self.__city

    @city.setter
    def city(self, value: dict):
        self._property_changed('city')
        self.__city = value        

    @property
    def pnl_wtd(self) -> dict:
        return self.__pnl_wtd

    @pnl_wtd.setter
    def pnl_wtd(self, value: dict):
        self._property_changed('pnl_wtd')
        self.__pnl_wtd = value        

    @property
    def covariance(self) -> dict:
        return self.__covariance

    @covariance.setter
    def covariance(self, value: dict):
        self._property_changed('covariance')
        self.__covariance = value        

    @property
    def bucket_volume_in_shares(self) -> dict:
        return self.__bucket_volume_in_shares

    @bucket_volume_in_shares.setter
    def bucket_volume_in_shares(self, value: dict):
        self._property_changed('bucket_volume_in_shares')
        self.__bucket_volume_in_shares = value        

    @property
    def commodity_forecast(self) -> dict:
        return self.__commodity_forecast

    @commodity_forecast.setter
    def commodity_forecast(self, value: dict):
        self._property_changed('commodity_forecast')
        self.__commodity_forecast = value        

    @property
    def valid(self) -> dict:
        return self.__valid

    @valid.setter
    def valid(self, value: dict):
        self._property_changed('valid')
        self.__valid = value        

    @property
    def sts_commodity(self) -> dict:
        return self.__sts_commodity

    @sts_commodity.setter
    def sts_commodity(self, value: dict):
        self._property_changed('sts_commodity')
        self.__sts_commodity = value        

    @property
    def initial_pricing_date(self) -> dict:
        return self.__initial_pricing_date

    @initial_pricing_date.setter
    def initial_pricing_date(self, value: dict):
        self._property_changed('initial_pricing_date')
        self.__initial_pricing_date = value        

    @property
    def indication_of_end_user_exception(self) -> dict:
        return self.__indication_of_end_user_exception

    @indication_of_end_user_exception.setter
    def indication_of_end_user_exception(self, value: dict):
        self._property_changed('indication_of_end_user_exception')
        self.__indication_of_end_user_exception = value        

    @property
    def wind_direction_hourly_forecast(self) -> dict:
        return self.__wind_direction_hourly_forecast

    @wind_direction_hourly_forecast.setter
    def wind_direction_hourly_forecast(self, value: dict):
        self._property_changed('wind_direction_hourly_forecast')
        self.__wind_direction_hourly_forecast = value        

    @property
    def es_score(self) -> dict:
        return self.__es_score

    @es_score.setter
    def es_score(self, value: dict):
        self._property_changed('es_score')
        self.__es_score = value        

    @property
    def yield_(self) -> dict:
        return self.__yield

    @yield_.setter
    def yield_(self, value: dict):
        self._property_changed('yield_')
        self.__yield = value        

    @property
    def fatalities_underlying_conditions_present(self) -> dict:
        return self.__fatalities_underlying_conditions_present

    @fatalities_underlying_conditions_present.setter
    def fatalities_underlying_conditions_present(self, value: dict):
        self._property_changed('fatalities_underlying_conditions_present')
        self.__fatalities_underlying_conditions_present = value        

    @property
    def price_range_in_ticks(self) -> dict:
        return self.__price_range_in_ticks

    @price_range_in_ticks.setter
    def price_range_in_ticks(self, value: dict):
        self._property_changed('price_range_in_ticks')
        self.__price_range_in_ticks = value        

    @property
    def pace_of_rollp25(self) -> dict:
        return self.__pace_of_rollp25

    @pace_of_rollp25.setter
    def pace_of_rollp25(self, value: dict):
        self._property_changed('pace_of_rollp25')
        self.__pace_of_rollp25 = value        

    @property
    def day_close_realized_usd(self) -> dict:
        return self.__day_close_realized_usd

    @day_close_realized_usd.setter
    def day_close_realized_usd(self, value: dict):
        self._property_changed('day_close_realized_usd')
        self.__day_close_realized_usd = value        

    @property
    def pct_change(self) -> dict:
        return self.__pct_change

    @pct_change.setter
    def pct_change(self, value: dict):
        self._property_changed('pct_change')
        self.__pct_change = value        

    @property
    def brightness_type(self) -> dict:
        return self.__brightness_type

    @brightness_type.setter
    def brightness_type(self, value: dict):
        self._property_changed('brightness_type')
        self.__brightness_type = value        

    @property
    def future_month3_m(self) -> dict:
        return self.__future_month3_m

    @future_month3_m.setter
    def future_month3_m(self, value: dict):
        self._property_changed('future_month3_m')
        self.__future_month3_m = value        

    @property
    def number_of_rolls(self) -> dict:
        return self.__number_of_rolls

    @number_of_rolls.setter
    def number_of_rolls(self, value: dict):
        self._property_changed('number_of_rolls')
        self.__number_of_rolls = value        

    @property
    def iso_country_code_numeric(self) -> dict:
        return self.__iso_country_code_numeric

    @iso_country_code_numeric.setter
    def iso_country_code_numeric(self, value: dict):
        self._property_changed('iso_country_code_numeric')
        self.__iso_country_code_numeric = value        

    @property
    def price_type(self) -> dict:
        return self.__price_type

    @price_type.setter
    def price_type(self, value: dict):
        self._property_changed('price_type')
        self.__price_type = value        

    @property
    def realized_vwap_performance_usd(self) -> dict:
        return self.__realized_vwap_performance_usd

    @realized_vwap_performance_usd.setter
    def realized_vwap_performance_usd(self, value: dict):
        self._property_changed('realized_vwap_performance_usd')
        self.__realized_vwap_performance_usd = value        

    @property
    def fuel_type(self) -> dict:
        return self.__fuel_type

    @fuel_type.setter
    def fuel_type(self, value: dict):
        self._property_changed('fuel_type')
        self.__fuel_type = value        

    @property
    def bbid(self) -> dict:
        return self.__bbid

    @bbid.setter
    def bbid(self, value: dict):
        self._property_changed('bbid')
        self.__bbid = value        

    @property
    def vega_notional_amount(self) -> dict:
        return self.__vega_notional_amount

    @vega_notional_amount.setter
    def vega_notional_amount(self, value: dict):
        self._property_changed('vega_notional_amount')
        self.__vega_notional_amount = value        

    @property
    def fatalities_underlying_conditions_absent(self) -> dict:
        return self.__fatalities_underlying_conditions_absent

    @fatalities_underlying_conditions_absent.setter
    def fatalities_underlying_conditions_absent(self, value: dict):
        self._property_changed('fatalities_underlying_conditions_absent')
        self.__fatalities_underlying_conditions_absent = value        

    @property
    def effective_date(self) -> dict:
        return self.__effective_date

    @effective_date.setter
    def effective_date(self, value: dict):
        self._property_changed('effective_date')
        self.__effective_date = value        

    @property
    def capped(self) -> dict:
        return self.__capped

    @capped.setter
    def capped(self, value: dict):
        self._property_changed('capped')
        self.__capped = value        

    @property
    def rating(self) -> dict:
        return self.__rating

    @rating.setter
    def rating(self, value: dict):
        self._property_changed('rating')
        self.__rating = value        

    @property
    def option_currency(self) -> dict:
        return self.__option_currency

    @option_currency.setter
    def option_currency(self, value: dict):
        self._property_changed('option_currency')
        self.__option_currency = value        

    @property
    def is_close_auction(self) -> dict:
        return self.__is_close_auction

    @is_close_auction.setter
    def is_close_auction(self, value: dict):
        self._property_changed('is_close_auction')
        self.__is_close_auction = value        

    @property
    def volatility(self) -> dict:
        return self.__volatility

    @volatility.setter
    def volatility(self, value: dict):
        self._property_changed('volatility')
        self.__volatility = value        

    @property
    def avg_vent_util(self) -> dict:
        return self.__avg_vent_util

    @avg_vent_util.setter
    def avg_vent_util(self, value: dict):
        self._property_changed('avg_vent_util')
        self.__avg_vent_util = value        

    @property
    def underlying_asset_ids(self) -> dict:
        return self.__underlying_asset_ids

    @underlying_asset_ids.setter
    def underlying_asset_ids(self, value: dict):
        self._property_changed('underlying_asset_ids')
        self.__underlying_asset_ids = value        

    @property
    def buy6point5bps(self) -> dict:
        return self.__buy6point5bps

    @buy6point5bps.setter
    def buy6point5bps(self, value: dict):
        self._property_changed('buy6point5bps')
        self.__buy6point5bps = value        

    @property
    def vwap_in_limit_realized_cash(self) -> dict:
        return self.__vwap_in_limit_realized_cash

    @vwap_in_limit_realized_cash.setter
    def vwap_in_limit_realized_cash(self, value: dict):
        self._property_changed('vwap_in_limit_realized_cash')
        self.__vwap_in_limit_realized_cash = value        

    @property
    def estimated_closing_auction_volume(self) -> dict:
        return self.__estimated_closing_auction_volume

    @estimated_closing_auction_volume.setter
    def estimated_closing_auction_volume(self, value: dict):
        self._property_changed('estimated_closing_auction_volume')
        self.__estimated_closing_auction_volume = value        

    @property
    def sell2bps(self) -> dict:
        return self.__sell2bps

    @sell2bps.setter
    def sell2bps(self, value: dict):
        self._property_changed('sell2bps')
        self.__sell2bps = value        

    @property
    def annual_risk(self) -> dict:
        return self.__annual_risk

    @annual_risk.setter
    def annual_risk(self, value: dict):
        self._property_changed('annual_risk')
        self.__annual_risk = value        

    @property
    def eti(self) -> dict:
        return self.__eti

    @eti.setter
    def eti(self, value: dict):
        self._property_changed('eti')
        self.__eti = value        

    @property
    def vwap_in_limit_realized_bps(self) -> dict:
        return self.__vwap_in_limit_realized_bps

    @vwap_in_limit_realized_bps.setter
    def vwap_in_limit_realized_bps(self, value: dict):
        self._property_changed('vwap_in_limit_realized_bps')
        self.__vwap_in_limit_realized_bps = value        

    @property
    def rank_mtd(self) -> dict:
        return self.__rank_mtd

    @rank_mtd.setter
    def rank_mtd(self, value: dict):
        self._property_changed('rank_mtd')
        self.__rank_mtd = value        

    @property
    def market_buffer(self) -> dict:
        return self.__market_buffer

    @market_buffer.setter
    def market_buffer(self, value: dict):
        self._property_changed('market_buffer')
        self.__market_buffer = value        

    @property
    def future_month_j24(self) -> dict:
        return self.__future_month_j24

    @future_month_j24.setter
    def future_month_j24(self, value: dict):
        self._property_changed('future_month_j24')
        self.__future_month_j24 = value        

    @property
    def future_month_j23(self) -> dict:
        return self.__future_month_j23

    @future_month_j23.setter
    def future_month_j23(self, value: dict):
        self._property_changed('future_month_j23')
        self.__future_month_j23 = value        

    @property
    def oe_id(self) -> dict:
        return self.__oe_id

    @oe_id.setter
    def oe_id(self, value: dict):
        self._property_changed('oe_id')
        self.__oe_id = value        

    @property
    def future_month_j22(self) -> dict:
        return self.__future_month_j22

    @future_month_j22.setter
    def future_month_j22(self, value: dict):
        self._property_changed('future_month_j22')
        self.__future_month_j22 = value        

    @property
    def future_month_j21(self) -> dict:
        return self.__future_month_j21

    @future_month_j21.setter
    def future_month_j21(self, value: dict):
        self._property_changed('future_month_j21')
        self.__future_month_j21 = value        

    @property
    def bbid_equivalent(self) -> dict:
        return self.__bbid_equivalent

    @bbid_equivalent.setter
    def bbid_equivalent(self, value: dict):
        self._property_changed('bbid_equivalent')
        self.__bbid_equivalent = value        

    @property
    def init_buffer_threshold_required(self) -> dict:
        return self.__init_buffer_threshold_required

    @init_buffer_threshold_required.setter
    def init_buffer_threshold_required(self, value: dict):
        self._property_changed('init_buffer_threshold_required')
        self.__init_buffer_threshold_required = value        

    @property
    def leg2_designated_maturity(self) -> dict:
        return self.__leg2_designated_maturity

    @leg2_designated_maturity.setter
    def leg2_designated_maturity(self, value: dict):
        self._property_changed('leg2_designated_maturity')
        self.__leg2_designated_maturity = value        

    @property
    def matched_maturity_ois_swap_rate(self) -> dict:
        return self.__matched_maturity_ois_swap_rate

    @matched_maturity_ois_swap_rate.setter
    def matched_maturity_ois_swap_rate(self, value: dict):
        self._property_changed('matched_maturity_ois_swap_rate')
        self.__matched_maturity_ois_swap_rate = value        

    @property
    def fair_price(self) -> dict:
        return self.__fair_price

    @fair_price.setter
    def fair_price(self, value: dict):
        self._property_changed('fair_price')
        self.__fair_price = value        

    @property
    def participation_rate_in_limit(self) -> dict:
        return self.__participation_rate_in_limit

    @participation_rate_in_limit.setter
    def participation_rate_in_limit(self, value: dict):
        self._property_changed('participation_rate_in_limit')
        self.__participation_rate_in_limit = value        

    @property
    def ext_mkt_class(self) -> dict:
        return self.__ext_mkt_class

    @ext_mkt_class.setter
    def ext_mkt_class(self, value: dict):
        self._property_changed('ext_mkt_class')
        self.__ext_mkt_class = value        

    @property
    def price_currency(self) -> dict:
        return self.__price_currency

    @price_currency.setter
    def price_currency(self, value: dict):
        self._property_changed('price_currency')
        self.__price_currency = value        

    @property
    def failed_count(self) -> dict:
        return self.__failed_count

    @failed_count.setter
    def failed_count(self, value: dict):
        self._property_changed('failed_count')
        self.__failed_count = value        

    @property
    def leg1_index_location(self) -> dict:
        return self.__leg1_index_location

    @leg1_index_location.setter
    def leg1_index_location(self, value: dict):
        self._property_changed('leg1_index_location')
        self.__leg1_index_location = value        

    @property
    def supra_strategy(self) -> dict:
        return self.__supra_strategy

    @supra_strategy.setter
    def supra_strategy(self, value: dict):
        self._property_changed('supra_strategy')
        self.__supra_strategy = value        

    @property
    def day_count_convention(self) -> dict:
        return self.__day_count_convention

    @day_count_convention.setter
    def day_count_convention(self, value: dict):
        self._property_changed('day_count_convention')
        self.__day_count_convention = value        

    @property
    def rounded_notional_amount1(self) -> dict:
        return self.__rounded_notional_amount1

    @rounded_notional_amount1.setter
    def rounded_notional_amount1(self, value: dict):
        self._property_changed('rounded_notional_amount1')
        self.__rounded_notional_amount1 = value        

    @property
    def rounded_notional_amount2(self) -> dict:
        return self.__rounded_notional_amount2

    @rounded_notional_amount2.setter
    def rounded_notional_amount2(self, value: dict):
        self._property_changed('rounded_notional_amount2')
        self.__rounded_notional_amount2 = value        

    @property
    def factor_source(self) -> dict:
        return self.__factor_source

    @factor_source.setter
    def factor_source(self, value: dict):
        self._property_changed('factor_source')
        self.__factor_source = value        

    @property
    def future_month_j26(self) -> dict:
        return self.__future_month_j26

    @future_month_j26.setter
    def future_month_j26(self, value: dict):
        self._property_changed('future_month_j26')
        self.__future_month_j26 = value        

    @property
    def lending_sec_type(self) -> dict:
        return self.__lending_sec_type

    @lending_sec_type.setter
    def lending_sec_type(self, value: dict):
        self._property_changed('lending_sec_type')
        self.__lending_sec_type = value        

    @property
    def future_month_j25(self) -> dict:
        return self.__future_month_j25

    @future_month_j25.setter
    def future_month_j25(self, value: dict):
        self._property_changed('future_month_j25')
        self.__future_month_j25 = value        

    @property
    def leverage(self) -> dict:
        return self.__leverage

    @leverage.setter
    def leverage(self, value: dict):
        self._property_changed('leverage')
        self.__leverage = value        

    @property
    def forecast_day(self) -> dict:
        return self.__forecast_day

    @forecast_day.setter
    def forecast_day(self, value: dict):
        self._property_changed('forecast_day')
        self.__forecast_day = value        

    @property
    def option_family(self) -> dict:
        return self.__option_family

    @option_family.setter
    def option_family(self, value: dict):
        self._property_changed('option_family')
        self.__option_family = value        

    @property
    def generator_output(self) -> dict:
        return self.__generator_output

    @generator_output.setter
    def generator_output(self, value: dict):
        self._property_changed('generator_output')
        self.__generator_output = value        

    @property
    def price_spot_stop_loss_value(self) -> dict:
        return self.__price_spot_stop_loss_value

    @price_spot_stop_loss_value.setter
    def price_spot_stop_loss_value(self, value: dict):
        self._property_changed('price_spot_stop_loss_value')
        self.__price_spot_stop_loss_value = value        

    @property
    def kpi_id(self) -> dict:
        return self.__kpi_id

    @kpi_id.setter
    def kpi_id(self, value: dict):
        self._property_changed('kpi_id')
        self.__kpi_id = value        

    @property
    def wind_generation(self) -> dict:
        return self.__wind_generation

    @wind_generation.setter
    def wind_generation(self, value: dict):
        self._property_changed('wind_generation')
        self.__wind_generation = value        

    @property
    def percentage_mid_executed_quantity(self) -> dict:
        return self.__percentage_mid_executed_quantity

    @percentage_mid_executed_quantity.setter
    def percentage_mid_executed_quantity(self, value: dict):
        self._property_changed('percentage_mid_executed_quantity')
        self.__percentage_mid_executed_quantity = value        

    @property
    def borrow_cost(self) -> dict:
        return self.__borrow_cost

    @borrow_cost.setter
    def borrow_cost(self, value: dict):
        self._property_changed('borrow_cost')
        self.__borrow_cost = value        

    @property
    def knock_out_direction(self) -> dict:
        return self.__knock_out_direction

    @knock_out_direction.setter
    def knock_out_direction(self, value: dict):
        self._property_changed('knock_out_direction')
        self.__knock_out_direction = value        

    @property
    def risk_model(self) -> dict:
        return self.__risk_model

    @risk_model.setter
    def risk_model(self, value: dict):
        self._property_changed('risk_model')
        self.__risk_model = value        

    @property
    def asset_parameters_vendor(self) -> dict:
        return self.__asset_parameters_vendor

    @asset_parameters_vendor.setter
    def asset_parameters_vendor(self, value: dict):
        self._property_changed('asset_parameters_vendor')
        self.__asset_parameters_vendor = value        

    @property
    def fair_value(self) -> dict:
        return self.__fair_value

    @fair_value.setter
    def fair_value(self, value: dict):
        self._property_changed('fair_value')
        self.__fair_value = value        

    @property
    def pressure_hourly_forecast(self) -> dict:
        return self.__pressure_hourly_forecast

    @pressure_hourly_forecast.setter
    def pressure_hourly_forecast(self, value: dict):
        self._property_changed('pressure_hourly_forecast')
        self.__pressure_hourly_forecast = value        

    @property
    def local_ccy_rate(self) -> dict:
        return self.__local_ccy_rate

    @local_ccy_rate.setter
    def local_ccy_rate(self, value: dict):
        self._property_changed('local_ccy_rate')
        self.__local_ccy_rate = value        

    @property
    def end_user_exception(self) -> dict:
        return self.__end_user_exception

    @end_user_exception.setter
    def end_user_exception(self, value: dict):
        self._property_changed('end_user_exception')
        self.__end_user_exception = value        

    @property
    def sell90cents(self) -> dict:
        return self.__sell90cents

    @sell90cents.setter
    def sell90cents(self, value: dict):
        self._property_changed('sell90cents')
        self.__sell90cents = value        

    @property
    def execution_venue(self) -> dict:
        return self.__execution_venue

    @execution_venue.setter
    def execution_venue(self, value: dict):
        self._property_changed('execution_venue')
        self.__execution_venue = value        

    @property
    def primary_vwap_in_limit_realized_bps(self) -> dict:
        return self.__primary_vwap_in_limit_realized_bps

    @primary_vwap_in_limit_realized_bps.setter
    def primary_vwap_in_limit_realized_bps(self, value: dict):
        self._property_changed('primary_vwap_in_limit_realized_bps')
        self.__primary_vwap_in_limit_realized_bps = value        

    @property
    def approve_rebalance(self) -> dict:
        return self.__approve_rebalance

    @approve_rebalance.setter
    def approve_rebalance(self, value: dict):
        self._property_changed('approve_rebalance')
        self.__approve_rebalance = value        

    @property
    def adjusted_close_price(self) -> dict:
        return self.__adjusted_close_price

    @adjusted_close_price.setter
    def adjusted_close_price(self, value: dict):
        self._property_changed('adjusted_close_price')
        self.__adjusted_close_price = value        

    @property
    def lms_id(self) -> dict:
        return self.__lms_id

    @lms_id.setter
    def lms_id(self, value: dict):
        self._property_changed('lms_id')
        self.__lms_id = value        

    @property
    def rebate_rate(self) -> dict:
        return self.__rebate_rate

    @rebate_rate.setter
    def rebate_rate(self, value: dict):
        self._property_changed('rebate_rate')
        self.__rebate_rate = value        

    @property
    def sell130cents(self) -> dict:
        return self.__sell130cents

    @sell130cents.setter
    def sell130cents(self, value: dict):
        self._property_changed('sell130cents')
        self.__sell130cents = value        

    @property
    def sell32bps(self) -> dict:
        return self.__sell32bps

    @sell32bps.setter
    def sell32bps(self, value: dict):
        self._property_changed('sell32bps')
        self.__sell32bps = value        

    @property
    def pace_of_rollp50(self) -> dict:
        return self.__pace_of_rollp50

    @pace_of_rollp50.setter
    def pace_of_rollp50(self, value: dict):
        self._property_changed('pace_of_rollp50')
        self.__pace_of_rollp50 = value        

    @property
    def price_move_vs_arrival(self) -> dict:
        return self.__price_move_vs_arrival

    @price_move_vs_arrival.setter
    def price_move_vs_arrival(self, value: dict):
        self._property_changed('price_move_vs_arrival')
        self.__price_move_vs_arrival = value        

    @property
    def strike_relative(self) -> dict:
        return self.__strike_relative

    @strike_relative.setter
    def strike_relative(self, value: dict):
        self._property_changed('strike_relative')
        self.__strike_relative = value        

    @property
    def pressure_type(self) -> dict:
        return self.__pressure_type

    @pressure_type.setter
    def pressure_type(self, value: dict):
        self._property_changed('pressure_type')
        self.__pressure_type = value        

    @property
    def buy40bps(self) -> dict:
        return self.__buy40bps

    @buy40bps.setter
    def buy40bps(self, value: dict):
        self._property_changed('buy40bps')
        self.__buy40bps = value        

    @property
    def price_notation(self) -> dict:
        return self.__price_notation

    @price_notation.setter
    def price_notation(self, value: dict):
        self._property_changed('price_notation')
        self.__price_notation = value        

    @property
    def strategy(self) -> dict:
        return self.__strategy

    @strategy.setter
    def strategy(self, value: dict):
        self._property_changed('strategy')
        self.__strategy = value        

    @property
    def issue_status_date(self) -> dict:
        return self.__issue_status_date

    @issue_status_date.setter
    def issue_status_date(self, value: dict):
        self._property_changed('issue_status_date')
        self.__issue_status_date = value        

    @property
    def lender_income(self) -> dict:
        return self.__lender_income

    @lender_income.setter
    def lender_income(self, value: dict):
        self._property_changed('lender_income')
        self.__lender_income = value        

    @property
    def pb_client_id(self) -> dict:
        return self.__pb_client_id

    @pb_client_id.setter
    def pb_client_id(self, value: dict):
        self._property_changed('pb_client_id')
        self.__pb_client_id = value        

    @property
    def istat_region_code(self) -> dict:
        return self.__istat_region_code

    @istat_region_code.setter
    def istat_region_code(self, value: dict):
        self._property_changed('istat_region_code')
        self.__istat_region_code = value        

    @property
    def sell9bps(self) -> dict:
        return self.__sell9bps

    @sell9bps.setter
    def sell9bps(self, value: dict):
        self._property_changed('sell9bps')
        self.__sell9bps = value        

    @property
    def owner_id(self) -> dict:
        return self.__owner_id

    @owner_id.setter
    def owner_id(self, value: dict):
        self._property_changed('owner_id')
        self.__owner_id = value        

    @property
    def composite10_day_adv(self) -> dict:
        return self.__composite10_day_adv

    @composite10_day_adv.setter
    def composite10_day_adv(self, value: dict):
        self._property_changed('composite10_day_adv')
        self.__composite10_day_adv = value        

    @property
    def max_loan_balance(self) -> dict:
        return self.__max_loan_balance

    @max_loan_balance.setter
    def max_loan_balance(self, value: dict):
        self._property_changed('max_loan_balance')
        self.__max_loan_balance = value        

    @property
    def idea_activity_type(self) -> dict:
        return self.__idea_activity_type

    @idea_activity_type.setter
    def idea_activity_type(self, value: dict):
        self._property_changed('idea_activity_type')
        self.__idea_activity_type = value        

    @property
    def sell60cents(self) -> dict:
        return self.__sell60cents

    @sell60cents.setter
    def sell60cents(self, value: dict):
        self._property_changed('sell60cents')
        self.__sell60cents = value        

    @property
    def idea_source(self) -> dict:
        return self.__idea_source

    @idea_source.setter
    def idea_source(self, value: dict):
        self._property_changed('idea_source')
        self.__idea_source = value        

    @property
    def ever_on_vent(self) -> dict:
        return self.__ever_on_vent

    @ever_on_vent.setter
    def ever_on_vent(self, value: dict):
        self._property_changed('ever_on_vent')
        self.__ever_on_vent = value        

    @property
    def buy15cents(self) -> dict:
        return self.__buy15cents

    @buy15cents.setter
    def buy15cents(self, value: dict):
        self._property_changed('buy15cents')
        self.__buy15cents = value        

    @property
    def unadjusted_ask(self) -> dict:
        return self.__unadjusted_ask

    @unadjusted_ask.setter
    def unadjusted_ask(self, value: dict):
        self._property_changed('unadjusted_ask')
        self.__unadjusted_ask = value        

    @property
    def contribution_name(self) -> dict:
        return self.__contribution_name

    @contribution_name.setter
    def contribution_name(self, value: dict):
        self._property_changed('contribution_name')
        self.__contribution_name = value        

    @property
    def given_plus_paid(self) -> dict:
        return self.__given_plus_paid

    @given_plus_paid.setter
    def given_plus_paid(self, value: dict):
        self._property_changed('given_plus_paid')
        self.__given_plus_paid = value        

    @property
    def last_fill_price(self) -> dict:
        return self.__last_fill_price

    @last_fill_price.setter
    def last_fill_price(self, value: dict):
        self._property_changed('last_fill_price')
        self.__last_fill_price = value        

    @property
    def short_conviction_small(self) -> dict:
        return self.__short_conviction_small

    @short_conviction_small.setter
    def short_conviction_small(self, value: dict):
        self._property_changed('short_conviction_small')
        self.__short_conviction_small = value        

    @property
    def upfront_payment_currency(self) -> dict:
        return self.__upfront_payment_currency

    @upfront_payment_currency.setter
    def upfront_payment_currency(self, value: dict):
        self._property_changed('upfront_payment_currency')
        self.__upfront_payment_currency = value        

    @property
    def spot_settlement_date(self) -> dict:
        return self.__spot_settlement_date

    @spot_settlement_date.setter
    def spot_settlement_date(self, value: dict):
        self._property_changed('spot_settlement_date')
        self.__spot_settlement_date = value        

    @property
    def matrix_order(self) -> dict:
        return self.__matrix_order

    @matrix_order.setter
    def matrix_order(self, value: dict):
        self._property_changed('matrix_order')
        self.__matrix_order = value        

    @property
    def date_index(self) -> dict:
        return self.__date_index

    @date_index.setter
    def date_index(self, value: dict):
        self._property_changed('date_index')
        self.__date_index = value        

    @property
    def payer_day_count_fraction(self) -> dict:
        return self.__payer_day_count_fraction

    @payer_day_count_fraction.setter
    def payer_day_count_fraction(self, value: dict):
        self._property_changed('payer_day_count_fraction')
        self.__payer_day_count_fraction = value        

    @property
    def asset_classifications_is_primary(self) -> dict:
        return self.__asset_classifications_is_primary

    @asset_classifications_is_primary.setter
    def asset_classifications_is_primary(self, value: dict):
        self._property_changed('asset_classifications_is_primary')
        self.__asset_classifications_is_primary = value        

    @property
    def break_even_inflation_change(self) -> dict:
        return self.__break_even_inflation_change

    @break_even_inflation_change.setter
    def break_even_inflation_change(self, value: dict):
        self._property_changed('break_even_inflation_change')
        self.__break_even_inflation_change = value        

    @property
    def buy130cents(self) -> dict:
        return self.__buy130cents

    @buy130cents.setter
    def buy130cents(self, value: dict):
        self._property_changed('buy130cents')
        self.__buy130cents = value        

    @property
    def dwi_contribution(self) -> dict:
        return self.__dwi_contribution

    @dwi_contribution.setter
    def dwi_contribution(self, value: dict):
        self._property_changed('dwi_contribution')
        self.__dwi_contribution = value        

    @property
    def asset2_id(self) -> dict:
        return self.__asset2_id

    @asset2_id.setter
    def asset2_id(self, value: dict):
        self._property_changed('asset2_id')
        self.__asset2_id = value        

    @property
    def average_fill_price(self) -> dict:
        return self.__average_fill_price

    @average_fill_price.setter
    def average_fill_price(self, value: dict):
        self._property_changed('average_fill_price')
        self.__average_fill_price = value        

    @property
    def depth_spread_score(self) -> dict:
        return self.__depth_spread_score

    @depth_spread_score.setter
    def depth_spread_score(self, value: dict):
        self._property_changed('depth_spread_score')
        self.__depth_spread_score = value        

    @property
    def sell10cents(self) -> dict:
        return self.__sell10cents

    @sell10cents.setter
    def sell10cents(self, value: dict):
        self._property_changed('sell10cents')
        self.__sell10cents = value        

    @property
    def sub_account(self) -> dict:
        return self.__sub_account

    @sub_account.setter
    def sub_account(self, value: dict):
        self._property_changed('sub_account')
        self.__sub_account = value        

    @property
    def buy65cents(self) -> dict:
        return self.__buy65cents

    @buy65cents.setter
    def buy65cents(self, value: dict):
        self._property_changed('buy65cents')
        self.__buy65cents = value        

    @property
    def bond_cds_basis(self) -> dict:
        return self.__bond_cds_basis

    @bond_cds_basis.setter
    def bond_cds_basis(self, value: dict):
        self._property_changed('bond_cds_basis')
        self.__bond_cds_basis = value        

    @property
    def vendor(self) -> dict:
        return self.__vendor

    @vendor.setter
    def vendor(self, value: dict):
        self._property_changed('vendor')
        self.__vendor = value        

    @property
    def data_set(self) -> dict:
        return self.__data_set

    @data_set.setter
    def data_set(self, value: dict):
        self._property_changed('data_set')
        self.__data_set = value        

    @property
    def notional_amount2(self) -> dict:
        return self.__notional_amount2

    @notional_amount2.setter
    def notional_amount2(self, value: dict):
        self._property_changed('notional_amount2')
        self.__notional_amount2 = value        

    @property
    def notional_amount1(self) -> dict:
        return self.__notional_amount1

    @notional_amount1.setter
    def notional_amount1(self, value: dict):
        self._property_changed('notional_amount1')
        self.__notional_amount1 = value        

    @property
    def queueing_time(self) -> dict:
        return self.__queueing_time

    @queueing_time.setter
    def queueing_time(self, value: dict):
        self._property_changed('queueing_time')
        self.__queueing_time = value        

    @property
    def ann_return5_year(self) -> dict:
        return self.__ann_return5_year

    @ann_return5_year.setter
    def ann_return5_year(self, value: dict):
        self._property_changed('ann_return5_year')
        self.__ann_return5_year = value        

    @property
    def volume_start_of_day(self) -> dict:
        return self.__volume_start_of_day

    @volume_start_of_day.setter
    def volume_start_of_day(self, value: dict):
        self._property_changed('volume_start_of_day')
        self.__volume_start_of_day = value        

    @property
    def price_notation3_type(self) -> dict:
        return self.__price_notation3_type

    @price_notation3_type.setter
    def price_notation3_type(self, value: dict):
        self._property_changed('price_notation3_type')
        self.__price_notation3_type = value        

    @property
    def asset_parameters_floating_rate_designated_maturity(self) -> dict:
        return self.__asset_parameters_floating_rate_designated_maturity

    @asset_parameters_floating_rate_designated_maturity.setter
    def asset_parameters_floating_rate_designated_maturity(self, value: dict):
        self._property_changed('asset_parameters_floating_rate_designated_maturity')
        self.__asset_parameters_floating_rate_designated_maturity = value        

    @property
    def executed_notional_local(self) -> dict:
        return self.__executed_notional_local

    @executed_notional_local.setter
    def executed_notional_local(self, value: dict):
        self._property_changed('executed_notional_local')
        self.__executed_notional_local = value        

    @property
    def business_sponsor(self) -> dict:
        return self.__business_sponsor

    @business_sponsor.setter
    def business_sponsor(self, value: dict):
        self._property_changed('business_sponsor')
        self.__business_sponsor = value        

    @property
    def unexplained(self) -> dict:
        return self.__unexplained

    @unexplained.setter
    def unexplained(self, value: dict):
        self._property_changed('unexplained')
        self.__unexplained = value        

    @property
    def seasonal_adjustment_short(self) -> dict:
        return self.__seasonal_adjustment_short

    @seasonal_adjustment_short.setter
    def seasonal_adjustment_short(self, value: dict):
        self._property_changed('seasonal_adjustment_short')
        self.__seasonal_adjustment_short = value        

    @property
    def metric(self) -> dict:
        return self.__metric

    @metric.setter
    def metric(self, value: dict):
        self._property_changed('metric')
        self.__metric = value        

    @property
    def ask(self) -> dict:
        return self.__ask

    @ask.setter
    def ask(self, value: dict):
        self._property_changed('ask')
        self.__ask = value        

    @property
    def close_price(self) -> dict:
        return self.__close_price

    @close_price.setter
    def close_price(self, value: dict):
        self._property_changed('close_price')
        self.__close_price = value        

    @property
    def sell100cents(self) -> dict:
        return self.__sell100cents

    @sell100cents.setter
    def sell100cents(self, value: dict):
        self._property_changed('sell100cents')
        self.__sell100cents = value        

    @property
    def buy180cents(self) -> dict:
        return self.__buy180cents

    @buy180cents.setter
    def buy180cents(self, value: dict):
        self._property_changed('buy180cents')
        self.__buy180cents = value        

    @property
    def absolute_strike(self) -> dict:
        return self.__absolute_strike

    @absolute_strike.setter
    def absolute_strike(self, value: dict):
        self._property_changed('absolute_strike')
        self.__absolute_strike = value        

    @property
    def sell3point5bps(self) -> dict:
        return self.__sell3point5bps

    @sell3point5bps.setter
    def sell3point5bps(self, value: dict):
        self._property_changed('sell3point5bps')
        self.__sell3point5bps = value        

    @property
    def liquidity_score_buy(self) -> dict:
        return self.__liquidity_score_buy

    @liquidity_score_buy.setter
    def liquidity_score_buy(self, value: dict):
        self._property_changed('liquidity_score_buy')
        self.__liquidity_score_buy = value        

    @property
    def payment_frequency(self) -> dict:
        return self.__payment_frequency

    @payment_frequency.setter
    def payment_frequency(self, value: dict):
        self._property_changed('payment_frequency')
        self.__payment_frequency = value        

    @property
    def expense_ratio_net_bps(self) -> dict:
        return self.__expense_ratio_net_bps

    @expense_ratio_net_bps.setter
    def expense_ratio_net_bps(self, value: dict):
        self._property_changed('expense_ratio_net_bps')
        self.__expense_ratio_net_bps = value        

    @property
    def metric_type(self) -> dict:
        return self.__metric_type

    @metric_type.setter
    def metric_type(self, value: dict):
        self._property_changed('metric_type')
        self.__metric_type = value        

    @property
    def rank_ytd(self) -> dict:
        return self.__rank_ytd

    @rank_ytd.setter
    def rank_ytd(self, value: dict):
        self._property_changed('rank_ytd')
        self.__rank_ytd = value        

    @property
    def leg1_spread(self) -> dict:
        return self.__leg1_spread

    @leg1_spread.setter
    def leg1_spread(self, value: dict):
        self._property_changed('leg1_spread')
        self.__leg1_spread = value        

    @property
    def coverage_region(self) -> dict:
        return self.__coverage_region

    @coverage_region.setter
    def coverage_region(self, value: dict):
        self._property_changed('coverage_region')
        self.__coverage_region = value        

    @property
    def absolute_return_ytd(self) -> dict:
        return self.__absolute_return_ytd

    @absolute_return_ytd.setter
    def absolute_return_ytd(self, value: dict):
        self._property_changed('absolute_return_ytd')
        self.__absolute_return_ytd = value        

    @property
    def day_count_convention2(self) -> dict:
        return self.__day_count_convention2

    @day_count_convention2.setter
    def day_count_convention2(self, value: dict):
        self._property_changed('day_count_convention2')
        self.__day_count_convention2 = value        

    @property
    def fwdtier(self) -> dict:
        return self.__fwdtier

    @fwdtier.setter
    def fwdtier(self, value: dict):
        self._property_changed('fwdtier')
        self.__fwdtier = value        

    @property
    def degree_days(self) -> dict:
        return self.__degree_days

    @degree_days.setter
    def degree_days(self, value: dict):
        self._property_changed('degree_days')
        self.__degree_days = value        

    @property
    def turnover_adjusted(self) -> dict:
        return self.__turnover_adjusted

    @turnover_adjusted.setter
    def turnover_adjusted(self, value: dict):
        self._property_changed('turnover_adjusted')
        self.__turnover_adjusted = value        

    @property
    def price_spot_target_value(self) -> dict:
        return self.__price_spot_target_value

    @price_spot_target_value.setter
    def price_spot_target_value(self, value: dict):
        self._property_changed('price_spot_target_value')
        self.__price_spot_target_value = value        

    @property
    def market_data_point(self) -> dict:
        return self.__market_data_point

    @market_data_point.setter
    def market_data_point(self, value: dict):
        self._property_changed('market_data_point')
        self.__market_data_point = value        

    @property
    def num_of_funds(self) -> dict:
        return self.__num_of_funds

    @num_of_funds.setter
    def num_of_funds(self, value: dict):
        self._property_changed('num_of_funds')
        self.__num_of_funds = value        

    @property
    def execution_id(self) -> dict:
        return self.__execution_id

    @execution_id.setter
    def execution_id(self, value: dict):
        self._property_changed('execution_id')
        self.__execution_id = value        

    @property
    def turnover_unadjusted(self) -> dict:
        return self.__turnover_unadjusted

    @turnover_unadjusted.setter
    def turnover_unadjusted(self, value: dict):
        self._property_changed('turnover_unadjusted')
        self.__turnover_unadjusted = value        

    @property
    def leg1_floating_index(self) -> dict:
        return self.__leg1_floating_index

    @leg1_floating_index.setter
    def leg1_floating_index(self, value: dict):
        self._property_changed('leg1_floating_index')
        self.__leg1_floating_index = value        

    @property
    def hedge_annualized_volatility(self) -> dict:
        return self.__hedge_annualized_volatility

    @hedge_annualized_volatility.setter
    def hedge_annualized_volatility(self, value: dict):
        self._property_changed('hedge_annualized_volatility')
        self.__hedge_annualized_volatility = value        

    @property
    def benchmark_currency(self) -> dict:
        return self.__benchmark_currency

    @benchmark_currency.setter
    def benchmark_currency(self, value: dict):
        self._property_changed('benchmark_currency')
        self.__benchmark_currency = value        

    @property
    def futures_contract(self) -> dict:
        return self.__futures_contract

    @futures_contract.setter
    def futures_contract(self, value: dict):
        self._property_changed('futures_contract')
        self.__futures_contract = value        

    @property
    def name(self) -> dict:
        return self.__name

    @name.setter
    def name(self, value: dict):
        self._property_changed('name')
        self.__name = value        

    @property
    def aum(self) -> dict:
        return self.__aum

    @aum.setter
    def aum(self, value: dict):
        self._property_changed('aum')
        self.__aum = value        

    @property
    def leg1_day_count_convention(self) -> dict:
        return self.__leg1_day_count_convention

    @leg1_day_count_convention.setter
    def leg1_day_count_convention(self, value: dict):
        self._property_changed('leg1_day_count_convention')
        self.__leg1_day_count_convention = value        

    @property
    def cbs_code(self) -> dict:
        return self.__cbs_code

    @cbs_code.setter
    def cbs_code(self, value: dict):
        self._property_changed('cbs_code')
        self.__cbs_code = value        

    @property
    def folder_name(self) -> dict:
        return self.__folder_name

    @folder_name.setter
    def folder_name(self, value: dict):
        self._property_changed('folder_name')
        self.__folder_name = value        

    @property
    def api_usage(self) -> dict:
        return self.__api_usage

    @api_usage.setter
    def api_usage(self, value: dict):
        self._property_changed('api_usage')
        self.__api_usage = value        

    @property
    def twap_interval(self) -> dict:
        return self.__twap_interval

    @twap_interval.setter
    def twap_interval(self, value: dict):
        self._property_changed('twap_interval')
        self.__twap_interval = value        

    @property
    def unique_id(self) -> dict:
        return self.__unique_id

    @unique_id.setter
    def unique_id(self, value: dict):
        self._property_changed('unique_id')
        self.__unique_id = value        

    @property
    def option_expiration_date(self) -> dict:
        return self.__option_expiration_date

    @option_expiration_date.setter
    def option_expiration_date(self, value: dict):
        self._property_changed('option_expiration_date')
        self.__option_expiration_date = value        

    @property
    def swaption_atm_fwd_rate(self) -> dict:
        return self.__swaption_atm_fwd_rate

    @swaption_atm_fwd_rate.setter
    def swaption_atm_fwd_rate(self, value: dict):
        self._property_changed('swaption_atm_fwd_rate')
        self.__swaption_atm_fwd_rate = value        

    @property
    def live_date(self) -> dict:
        return self.__live_date

    @live_date.setter
    def live_date(self, value: dict):
        self._property_changed('live_date')
        self.__live_date = value        

    @property
    def corporate_action_type(self) -> dict:
        return self.__corporate_action_type

    @corporate_action_type.setter
    def corporate_action_type(self, value: dict):
        self._property_changed('corporate_action_type')
        self.__corporate_action_type = value        

    @property
    def prime_id(self) -> dict:
        return self.__prime_id

    @prime_id.setter
    def prime_id(self, value: dict):
        self._property_changed('prime_id')
        self.__prime_id = value        

    @property
    def description(self) -> dict:
        return self.__description

    @description.setter
    def description(self, value: dict):
        self._property_changed('description')
        self.__description = value        

    @property
    def asset_classifications_is_country_primary(self) -> dict:
        return self.__asset_classifications_is_country_primary

    @asset_classifications_is_country_primary.setter
    def asset_classifications_is_country_primary(self, value: dict):
        self._property_changed('asset_classifications_is_country_primary')
        self.__asset_classifications_is_country_primary = value        

    @property
    def rebate_rate_limit(self) -> dict:
        return self.__rebate_rate_limit

    @rebate_rate_limit.setter
    def rebate_rate_limit(self, value: dict):
        self._property_changed('rebate_rate_limit')
        self.__rebate_rate_limit = value        

    @property
    def factor(self) -> dict:
        return self.__factor

    @factor.setter
    def factor(self, value: dict):
        self._property_changed('factor')
        self.__factor = value        

    @property
    def days_on_loan(self) -> dict:
        return self.__days_on_loan

    @days_on_loan.setter
    def days_on_loan(self, value: dict):
        self._property_changed('days_on_loan')
        self.__days_on_loan = value        

    @property
    def long_conviction_small(self) -> dict:
        return self.__long_conviction_small

    @long_conviction_small.setter
    def long_conviction_small(self, value: dict):
        self._property_changed('long_conviction_small')
        self.__long_conviction_small = value        

    @property
    def sell40cents(self) -> dict:
        return self.__sell40cents

    @sell40cents.setter
    def sell40cents(self, value: dict):
        self._property_changed('sell40cents')
        self.__sell40cents = value        

    @property
    def relative_payoff_ytd(self) -> dict:
        return self.__relative_payoff_ytd

    @relative_payoff_ytd.setter
    def relative_payoff_ytd(self, value: dict):
        self._property_changed('relative_payoff_ytd')
        self.__relative_payoff_ytd = value        

    @property
    def gsfeer(self) -> dict:
        return self.__gsfeer

    @gsfeer.setter
    def gsfeer(self, value: dict):
        self._property_changed('gsfeer')
        self.__gsfeer = value        

    @property
    def relative_hit_rate_qtd(self) -> dict:
        return self.__relative_hit_rate_qtd

    @relative_hit_rate_qtd.setter
    def relative_hit_rate_qtd(self, value: dict):
        self._property_changed('relative_hit_rate_qtd')
        self.__relative_hit_rate_qtd = value        

    @property
    def wam(self) -> dict:
        return self.__wam

    @wam.setter
    def wam(self, value: dict):
        self._property_changed('wam')
        self.__wam = value        

    @property
    def wal(self) -> dict:
        return self.__wal

    @wal.setter
    def wal(self, value: dict):
        self._property_changed('wal')
        self.__wal = value        

    @property
    def quantityccy(self) -> dict:
        return self.__quantityccy

    @quantityccy.setter
    def quantityccy(self, value: dict):
        self._property_changed('quantityccy')
        self.__quantityccy = value        

    @property
    def backtest_id(self) -> dict:
        return self.__backtest_id

    @backtest_id.setter
    def backtest_id(self, value: dict):
        self._property_changed('backtest_id')
        self.__backtest_id = value        

    @property
    def dirty_price(self) -> dict:
        return self.__dirty_price

    @dirty_price.setter
    def dirty_price(self, value: dict):
        self._property_changed('dirty_price')
        self.__dirty_price = value        

    @property
    def corporate_spread_contribution(self) -> dict:
        return self.__corporate_spread_contribution

    @corporate_spread_contribution.setter
    def corporate_spread_contribution(self, value: dict):
        self._property_changed('corporate_spread_contribution')
        self.__corporate_spread_contribution = value        

    @property
    def relative_humidity_hourly_forecast(self) -> dict:
        return self.__relative_humidity_hourly_forecast

    @relative_humidity_hourly_forecast.setter
    def relative_humidity_hourly_forecast(self, value: dict):
        self._property_changed('relative_humidity_hourly_forecast')
        self.__relative_humidity_hourly_forecast = value        

    @property
    def multiple_score(self) -> dict:
        return self.__multiple_score

    @multiple_score.setter
    def multiple_score(self, value: dict):
        self._property_changed('multiple_score')
        self.__multiple_score = value        

    @property
    def beta_adjusted_exposure(self) -> dict:
        return self.__beta_adjusted_exposure

    @beta_adjusted_exposure.setter
    def beta_adjusted_exposure(self, value: dict):
        self._property_changed('beta_adjusted_exposure')
        self.__beta_adjusted_exposure = value        

    @property
    def dividend_points(self) -> dict:
        return self.__dividend_points

    @dividend_points.setter
    def dividend_points(self, value: dict):
        self._property_changed('dividend_points')
        self.__dividend_points = value        

    @property
    def brightness(self) -> dict:
        return self.__brightness

    @brightness.setter
    def brightness(self, value: dict):
        self._property_changed('brightness')
        self.__brightness = value        

    @property
    def asset_parameters_receiver_designated_maturity(self) -> dict:
        return self.__asset_parameters_receiver_designated_maturity

    @asset_parameters_receiver_designated_maturity.setter
    def asset_parameters_receiver_designated_maturity(self, value: dict):
        self._property_changed('asset_parameters_receiver_designated_maturity')
        self.__asset_parameters_receiver_designated_maturity = value        

    @property
    def bos_in_ticks_description(self) -> dict:
        return self.__bos_in_ticks_description

    @bos_in_ticks_description.setter
    def bos_in_ticks_description(self, value: dict):
        self._property_changed('bos_in_ticks_description')
        self.__bos_in_ticks_description = value        

    @property
    def test_id(self) -> dict:
        return self.__test_id

    @test_id.setter
    def test_id(self, value: dict):
        self._property_changed('test_id')
        self.__test_id = value        

    @property
    def implied_correlation(self) -> dict:
        return self.__implied_correlation

    @implied_correlation.setter
    def implied_correlation(self, value: dict):
        self._property_changed('implied_correlation')
        self.__implied_correlation = value        

    @property
    def normalized_performance(self) -> dict:
        return self.__normalized_performance

    @normalized_performance.setter
    def normalized_performance(self, value: dict):
        self._property_changed('normalized_performance')
        self.__normalized_performance = value        

    @property
    def bytes_consumed(self) -> dict:
        return self.__bytes_consumed

    @bytes_consumed.setter
    def bytes_consumed(self, value: dict):
        self._property_changed('bytes_consumed')
        self.__bytes_consumed = value        

    @property
    def swaption_vol(self) -> dict:
        return self.__swaption_vol

    @swaption_vol.setter
    def swaption_vol(self, value: dict):
        self._property_changed('swaption_vol')
        self.__swaption_vol = value        

    @property
    def estimated_closing_volume(self) -> dict:
        return self.__estimated_closing_volume

    @estimated_closing_volume.setter
    def estimated_closing_volume(self, value: dict):
        self._property_changed('estimated_closing_volume')
        self.__estimated_closing_volume = value        

    @property
    def issuer(self) -> dict:
        return self.__issuer

    @issuer.setter
    def issuer(self, value: dict):
        self._property_changed('issuer')
        self.__issuer = value        

    @property
    def dividend_yield(self) -> dict:
        return self.__dividend_yield

    @dividend_yield.setter
    def dividend_yield(self, value: dict):
        self._property_changed('dividend_yield')
        self.__dividend_yield = value        

    @property
    def market_type(self) -> dict:
        return self.__market_type

    @market_type.setter
    def market_type(self, value: dict):
        self._property_changed('market_type')
        self.__market_type = value        

    @property
    def num_units_lower(self) -> dict:
        return self.__num_units_lower

    @num_units_lower.setter
    def num_units_lower(self, value: dict):
        self._property_changed('num_units_lower')
        self.__num_units_lower = value        

    @property
    def source_origin(self) -> dict:
        return self.__source_origin

    @source_origin.setter
    def source_origin(self, value: dict):
        self._property_changed('source_origin')
        self.__source_origin = value        

    @property
    def proceeds_asset_swap_spread3m(self) -> dict:
        return self.__proceeds_asset_swap_spread3m

    @proceeds_asset_swap_spread3m.setter
    def proceeds_asset_swap_spread3m(self, value: dict):
        self._property_changed('proceeds_asset_swap_spread3m')
        self.__proceeds_asset_swap_spread3m = value        

    @property
    def total_quantity(self) -> dict:
        return self.__total_quantity

    @total_quantity.setter
    def total_quantity(self, value: dict):
        self._property_changed('total_quantity')
        self.__total_quantity = value        

    @property
    def internal_user(self) -> dict:
        return self.__internal_user

    @internal_user.setter
    def internal_user(self, value: dict):
        self._property_changed('internal_user')
        self.__internal_user = value        

    @property
    def sell40bps(self) -> dict:
        return self.__sell40bps

    @sell40bps.setter
    def sell40bps(self, value: dict):
        self._property_changed('sell40bps')
        self.__sell40bps = value        

    @property
    def redemption_option(self) -> dict:
        return self.__redemption_option

    @redemption_option.setter
    def redemption_option(self, value: dict):
        self._property_changed('redemption_option')
        self.__redemption_option = value        

    @property
    def notional_unit2(self) -> dict:
        return self.__notional_unit2

    @notional_unit2.setter
    def notional_unit2(self, value: dict):
        self._property_changed('notional_unit2')
        self.__notional_unit2 = value        

    @property
    def notional_unit1(self) -> dict:
        return self.__notional_unit1

    @notional_unit1.setter
    def notional_unit1(self, value: dict):
        self._property_changed('notional_unit1')
        self.__notional_unit1 = value        

    @property
    def sedol(self) -> dict:
        return self.__sedol

    @sedol.setter
    def sedol(self, value: dict):
        self._property_changed('sedol')
        self.__sedol = value        

    @property
    def rounding_cost_pnl(self) -> dict:
        return self.__rounding_cost_pnl

    @rounding_cost_pnl.setter
    def rounding_cost_pnl(self, value: dict):
        self._property_changed('rounding_cost_pnl')
        self.__rounding_cost_pnl = value        

    @property
    def mid_yield(self) -> dict:
        return self.__mid_yield

    @mid_yield.setter
    def mid_yield(self, value: dict):
        self._property_changed('mid_yield')
        self.__mid_yield = value        

    @property
    def unexecuted_notional_local(self) -> dict:
        return self.__unexecuted_notional_local

    @unexecuted_notional_local.setter
    def unexecuted_notional_local(self, value: dict):
        self._property_changed('unexecuted_notional_local')
        self.__unexecuted_notional_local = value        

    @property
    def sustain_global(self) -> dict:
        return self.__sustain_global

    @sustain_global.setter
    def sustain_global(self, value: dict):
        self._property_changed('sustain_global')
        self.__sustain_global = value        

    @property
    def ending_date(self) -> dict:
        return self.__ending_date

    @ending_date.setter
    def ending_date(self, value: dict):
        self._property_changed('ending_date')
        self.__ending_date = value        

    @property
    def proceeds_asset_swap_spread12m(self) -> dict:
        return self.__proceeds_asset_swap_spread12m

    @proceeds_asset_swap_spread12m.setter
    def proceeds_asset_swap_spread12m(self, value: dict):
        self._property_changed('proceeds_asset_swap_spread12m')
        self.__proceeds_asset_swap_spread12m = value        

    @property
    def gross_investment_wtd(self) -> dict:
        return self.__gross_investment_wtd

    @gross_investment_wtd.setter
    def gross_investment_wtd(self, value: dict):
        self._property_changed('gross_investment_wtd')
        self.__gross_investment_wtd = value        

    @property
    def ann_return3_year(self) -> dict:
        return self.__ann_return3_year

    @ann_return3_year.setter
    def ann_return3_year(self, value: dict):
        self._property_changed('ann_return3_year')
        self.__ann_return3_year = value        

    @property
    def sharpe_wtd(self) -> dict:
        return self.__sharpe_wtd

    @sharpe_wtd.setter
    def sharpe_wtd(self, value: dict):
        self._property_changed('sharpe_wtd')
        self.__sharpe_wtd = value        

    @property
    def discount_factor(self) -> dict:
        return self.__discount_factor

    @discount_factor.setter
    def discount_factor(self, value: dict):
        self._property_changed('discount_factor')
        self.__discount_factor = value        

    @property
    def relative_return_mtd(self) -> dict:
        return self.__relative_return_mtd

    @relative_return_mtd.setter
    def relative_return_mtd(self, value: dict):
        self._property_changed('relative_return_mtd')
        self.__relative_return_mtd = value        

    @property
    def price_change_on_day(self) -> dict:
        return self.__price_change_on_day

    @price_change_on_day.setter
    def price_change_on_day(self, value: dict):
        self._property_changed('price_change_on_day')
        self.__price_change_on_day = value        

    @property
    def buy100cents(self) -> dict:
        return self.__buy100cents

    @buy100cents.setter
    def buy100cents(self, value: dict):
        self._property_changed('buy100cents')
        self.__buy100cents = value        

    @property
    def forward_point(self) -> dict:
        return self.__forward_point

    @forward_point.setter
    def forward_point(self, value: dict):
        self._property_changed('forward_point')
        self.__forward_point = value        

    @property
    def fci(self) -> dict:
        return self.__fci

    @fci.setter
    def fci(self, value: dict):
        self._property_changed('fci')
        self.__fci = value        

    @property
    def recall_quantity(self) -> dict:
        return self.__recall_quantity

    @recall_quantity.setter
    def recall_quantity(self, value: dict):
        self._property_changed('recall_quantity')
        self.__recall_quantity = value        

    @property
    def fx_positioning(self) -> dict:
        return self.__fx_positioning

    @fx_positioning.setter
    def fx_positioning(self, value: dict):
        self._property_changed('fx_positioning')
        self.__fx_positioning = value        

    @property
    def gsid_equivalent(self) -> dict:
        return self.__gsid_equivalent

    @gsid_equivalent.setter
    def gsid_equivalent(self, value: dict):
        self._property_changed('gsid_equivalent')
        self.__gsid_equivalent = value        

    @property
    def categories(self) -> dict:
        return self.__categories

    @categories.setter
    def categories(self, value: dict):
        self._property_changed('categories')
        self.__categories = value        

    @property
    def ext_mkt_asset(self) -> dict:
        return self.__ext_mkt_asset

    @ext_mkt_asset.setter
    def ext_mkt_asset(self, value: dict):
        self._property_changed('ext_mkt_asset')
        self.__ext_mkt_asset = value        

    @property
    def quoting_style(self) -> dict:
        return self.__quoting_style

    @quoting_style.setter
    def quoting_style(self, value: dict):
        self._property_changed('quoting_style')
        self.__quoting_style = value        

    @property
    def error_message(self) -> dict:
        return self.__error_message

    @error_message.setter
    def error_message(self, value: dict):
        self._property_changed('error_message')
        self.__error_message = value        

    @property
    def mid_price(self) -> dict:
        return self.__mid_price

    @mid_price.setter
    def mid_price(self, value: dict):
        self._property_changed('mid_price')
        self.__mid_price = value        

    @property
    def proceeds_asset_swap_spread6m(self) -> dict:
        return self.__proceeds_asset_swap_spread6m

    @proceeds_asset_swap_spread6m.setter
    def proceeds_asset_swap_spread6m(self, value: dict):
        self._property_changed('proceeds_asset_swap_spread6m')
        self.__proceeds_asset_swap_spread6m = value        

    @property
    def sts_em_dm(self) -> dict:
        return self.__sts_em_dm

    @sts_em_dm.setter
    def sts_em_dm(self, value: dict):
        self._property_changed('sts_em_dm')
        self.__sts_em_dm = value        

    @property
    def embedded_option(self) -> dict:
        return self.__embedded_option

    @embedded_option.setter
    def embedded_option(self, value: dict):
        self._property_changed('embedded_option')
        self.__embedded_option = value        

    @property
    def tcm_cost_horizon2_day(self) -> dict:
        return self.__tcm_cost_horizon2_day

    @tcm_cost_horizon2_day.setter
    def tcm_cost_horizon2_day(self, value: dict):
        self._property_changed('tcm_cost_horizon2_day')
        self.__tcm_cost_horizon2_day = value        

    @property
    def age_band(self) -> dict:
        return self.__age_band

    @age_band.setter
    def age_band(self, value: dict):
        self._property_changed('age_band')
        self.__age_band = value        

    @property
    def returns_enabled(self) -> dict:
        return self.__returns_enabled

    @returns_enabled.setter
    def returns_enabled(self, value: dict):
        self._property_changed('returns_enabled')
        self.__returns_enabled = value        

    @property
    def run_id(self) -> dict:
        return self.__run_id

    @run_id.setter
    def run_id(self, value: dict):
        self._property_changed('run_id')
        self.__run_id = value        

    @property
    def queue_in_lots(self) -> dict:
        return self.__queue_in_lots

    @queue_in_lots.setter
    def queue_in_lots(self, value: dict):
        self._property_changed('queue_in_lots')
        self.__queue_in_lots = value        

    @property
    def tender_offer_expiration_date(self) -> dict:
        return self.__tender_offer_expiration_date

    @tender_offer_expiration_date.setter
    def tender_offer_expiration_date(self, value: dict):
        self._property_changed('tender_offer_expiration_date')
        self.__tender_offer_expiration_date = value        

    @property
    def midcurve_annuity(self) -> dict:
        return self.__midcurve_annuity

    @midcurve_annuity.setter
    def midcurve_annuity(self, value: dict):
        self._property_changed('midcurve_annuity')
        self.__midcurve_annuity = value        

    @property
    def lending_fund_nav_trend(self) -> dict:
        return self.__lending_fund_nav_trend

    @lending_fund_nav_trend.setter
    def lending_fund_nav_trend(self, value: dict):
        self._property_changed('lending_fund_nav_trend')
        self.__lending_fund_nav_trend = value        

    @property
    def cloud_cover_forecast(self) -> dict:
        return self.__cloud_cover_forecast

    @cloud_cover_forecast.setter
    def cloud_cover_forecast(self, value: dict):
        self._property_changed('cloud_cover_forecast')
        self.__cloud_cover_forecast = value        

    @property
    def tcm_cost_participation_rate5_pct(self) -> dict:
        return self.__tcm_cost_participation_rate5_pct

    @tcm_cost_participation_rate5_pct.setter
    def tcm_cost_participation_rate5_pct(self, value: dict):
        self._property_changed('tcm_cost_participation_rate5_pct')
        self.__tcm_cost_participation_rate5_pct = value        

    @property
    def default_backcast(self) -> dict:
        return self.__default_backcast

    @default_backcast.setter
    def default_backcast(self, value: dict):
        self._property_changed('default_backcast')
        self.__default_backcast = value        

    @property
    def news_on_intensity(self) -> dict:
        return self.__news_on_intensity

    @news_on_intensity.setter
    def news_on_intensity(self, value: dict):
        self._property_changed('news_on_intensity')
        self.__news_on_intensity = value        

    @property
    def price_forming_continuation_data(self) -> dict:
        return self.__price_forming_continuation_data

    @price_forming_continuation_data.setter
    def price_forming_continuation_data(self, value: dict):
        self._property_changed('price_forming_continuation_data')
        self.__price_forming_continuation_data = value        

    @property
    def adjusted_short_interest(self) -> dict:
        return self.__adjusted_short_interest

    @adjusted_short_interest.setter
    def adjusted_short_interest(self, value: dict):
        self._property_changed('adjusted_short_interest')
        self.__adjusted_short_interest = value        

    @property
    def new_hospitalized(self) -> dict:
        return self.__new_hospitalized

    @new_hospitalized.setter
    def new_hospitalized(self, value: dict):
        self._property_changed('new_hospitalized')
        self.__new_hospitalized = value        

    @property
    def asset_parameters_strike(self) -> dict:
        return self.__asset_parameters_strike

    @asset_parameters_strike.setter
    def asset_parameters_strike(self, value: dict):
        self._property_changed('asset_parameters_strike')
        self.__asset_parameters_strike = value        

    @property
    def buy35cents(self) -> dict:
        return self.__buy35cents

    @buy35cents.setter
    def buy35cents(self, value: dict):
        self._property_changed('buy35cents')
        self.__buy35cents = value        

    @property
    def leg2_total_notional(self) -> dict:
        return self.__leg2_total_notional

    @leg2_total_notional.setter
    def leg2_total_notional(self, value: dict):
        self._property_changed('leg2_total_notional')
        self.__leg2_total_notional = value        

    @property
    def asset_parameters_effective_date(self) -> dict:
        return self.__asset_parameters_effective_date

    @asset_parameters_effective_date.setter
    def asset_parameters_effective_date(self, value: dict):
        self._property_changed('asset_parameters_effective_date')
        self.__asset_parameters_effective_date = value        

    @property
    def ann_return10_year(self) -> dict:
        return self.__ann_return10_year

    @ann_return10_year.setter
    def ann_return10_year(self, value: dict):
        self._property_changed('ann_return10_year')
        self.__ann_return10_year = value        

    @property
    def num_adult_icu_beds(self) -> dict:
        return self.__num_adult_icu_beds

    @num_adult_icu_beds.setter
    def num_adult_icu_beds(self, value: dict):
        self._property_changed('num_adult_icu_beds')
        self.__num_adult_icu_beds = value        

    @property
    def days_to_expiration(self) -> dict:
        return self.__days_to_expiration

    @days_to_expiration.setter
    def days_to_expiration(self, value: dict):
        self._property_changed('days_to_expiration')
        self.__days_to_expiration = value        

    @property
    def continuation_event(self) -> dict:
        return self.__continuation_event

    @continuation_event.setter
    def continuation_event(self, value: dict):
        self._property_changed('continuation_event')
        self.__continuation_event = value        

    @property
    def wi_id(self) -> dict:
        return self.__wi_id

    @wi_id.setter
    def wi_id(self, value: dict):
        self._property_changed('wi_id')
        self.__wi_id = value        

    @property
    def market_cap_category(self) -> dict:
        return self.__market_cap_category

    @market_cap_category.setter
    def market_cap_category(self, value: dict):
        self._property_changed('market_cap_category')
        self.__market_cap_category = value        

    @property
    def historical_volume(self) -> dict:
        return self.__historical_volume

    @historical_volume.setter
    def historical_volume(self, value: dict):
        self._property_changed('historical_volume')
        self.__historical_volume = value        

    @property
    def buy5cents(self) -> dict:
        return self.__buy5cents

    @buy5cents.setter
    def buy5cents(self, value: dict):
        self._property_changed('buy5cents')
        self.__buy5cents = value        

    @property
    def event_start_date(self) -> dict:
        return self.__event_start_date

    @event_start_date.setter
    def event_start_date(self, value: dict):
        self._property_changed('event_start_date')
        self.__event_start_date = value        

    @property
    def leg1_fixed_rate(self) -> dict:
        return self.__leg1_fixed_rate

    @leg1_fixed_rate.setter
    def leg1_fixed_rate(self, value: dict):
        self._property_changed('leg1_fixed_rate')
        self.__leg1_fixed_rate = value        

    @property
    def equity_gamma(self) -> dict:
        return self.__equity_gamma

    @equity_gamma.setter
    def equity_gamma(self, value: dict):
        self._property_changed('equity_gamma')
        self.__equity_gamma = value        

    @property
    def rpt_id(self) -> dict:
        return self.__rpt_id

    @rpt_id.setter
    def rpt_id(self, value: dict):
        self._property_changed('rpt_id')
        self.__rpt_id = value        

    @property
    def gross_income(self) -> dict:
        return self.__gross_income

    @gross_income.setter
    def gross_income(self, value: dict):
        self._property_changed('gross_income')
        self.__gross_income = value        

    @property
    def em_id(self) -> dict:
        return self.__em_id

    @em_id.setter
    def em_id(self, value: dict):
        self._property_changed('em_id')
        self.__em_id = value        

    @property
    def asset_count_in_model(self) -> dict:
        return self.__asset_count_in_model

    @asset_count_in_model.setter
    def asset_count_in_model(self, value: dict):
        self._property_changed('asset_count_in_model')
        self.__asset_count_in_model = value        

    @property
    def sts_credit_region(self) -> dict:
        return self.__sts_credit_region

    @sts_credit_region.setter
    def sts_credit_region(self, value: dict):
        self._property_changed('sts_credit_region')
        self.__sts_credit_region = value        

    @property
    def min_temperature(self) -> dict:
        return self.__min_temperature

    @min_temperature.setter
    def min_temperature(self, value: dict):
        self._property_changed('min_temperature')
        self.__min_temperature = value        

    @property
    def fill_type(self) -> dict:
        return self.__fill_type

    @fill_type.setter
    def fill_type(self, value: dict):
        self._property_changed('fill_type')
        self.__fill_type = value        

    @property
    def fail_pct(self) -> dict:
        return self.__fail_pct

    @fail_pct.setter
    def fail_pct(self, value: dict):
        self._property_changed('fail_pct')
        self.__fail_pct = value        

    @property
    def iso_country_code_alpha2(self) -> dict:
        return self.__iso_country_code_alpha2

    @iso_country_code_alpha2.setter
    def iso_country_code_alpha2(self, value: dict):
        self._property_changed('iso_country_code_alpha2')
        self.__iso_country_code_alpha2 = value        

    @property
    def iso_country_code_alpha3(self) -> dict:
        return self.__iso_country_code_alpha3

    @iso_country_code_alpha3.setter
    def iso_country_code_alpha3(self, value: dict):
        self._property_changed('iso_country_code_alpha3')
        self.__iso_country_code_alpha3 = value        

    @property
    def amount(self) -> dict:
        return self.__amount

    @amount.setter
    def amount(self, value: dict):
        self._property_changed('amount')
        self.__amount = value        

    @property
    def lending_fund_acct(self) -> dict:
        return self.__lending_fund_acct

    @lending_fund_acct.setter
    def lending_fund_acct(self, value: dict):
        self._property_changed('lending_fund_acct')
        self.__lending_fund_acct = value        

    @property
    def rebate(self) -> dict:
        return self.__rebate

    @rebate.setter
    def rebate(self, value: dict):
        self._property_changed('rebate')
        self.__rebate = value        

    @property
    def election_type(self) -> dict:
        return self.__election_type

    @election_type.setter
    def election_type(self, value: dict):
        self._property_changed('election_type')
        self.__election_type = value        

    @property
    def relative_hit_rate_mtd(self) -> dict:
        return self.__relative_hit_rate_mtd

    @relative_hit_rate_mtd.setter
    def relative_hit_rate_mtd(self, value: dict):
        self._property_changed('relative_hit_rate_mtd')
        self.__relative_hit_rate_mtd = value        

    @property
    def implied_volatility(self) -> dict:
        return self.__implied_volatility

    @implied_volatility.setter
    def implied_volatility(self, value: dict):
        self._property_changed('implied_volatility')
        self.__implied_volatility = value        

    @property
    def spread(self) -> dict:
        return self.__spread

    @spread.setter
    def spread(self, value: dict):
        self._property_changed('spread')
        self.__spread = value        

    @property
    def variance(self) -> dict:
        return self.__variance

    @variance.setter
    def variance(self, value: dict):
        self._property_changed('variance')
        self.__variance = value        

    @property
    def wtd_degree_days_daily_forecast(self) -> dict:
        return self.__wtd_degree_days_daily_forecast

    @wtd_degree_days_daily_forecast.setter
    def wtd_degree_days_daily_forecast(self, value: dict):
        self._property_changed('wtd_degree_days_daily_forecast')
        self.__wtd_degree_days_daily_forecast = value        

    @property
    def swaption_annuity(self) -> dict:
        return self.__swaption_annuity

    @swaption_annuity.setter
    def swaption_annuity(self, value: dict):
        self._property_changed('swaption_annuity')
        self.__swaption_annuity = value        

    @property
    def buy6bps(self) -> dict:
        return self.__buy6bps

    @buy6bps.setter
    def buy6bps(self, value: dict):
        self._property_changed('buy6bps')
        self.__buy6bps = value        

    @property
    def g10_currency(self) -> dict:
        return self.__g10_currency

    @g10_currency.setter
    def g10_currency(self, value: dict):
        self._property_changed('g10_currency')
        self.__g10_currency = value        

    @property
    def humidity_forecast(self) -> dict:
        return self.__humidity_forecast

    @humidity_forecast.setter
    def humidity_forecast(self, value: dict):
        self._property_changed('humidity_forecast')
        self.__humidity_forecast = value        

    @property
    def relative_period(self) -> dict:
        return self.__relative_period

    @relative_period.setter
    def relative_period(self, value: dict):
        self._property_changed('relative_period')
        self.__relative_period = value        

    @property
    def user(self) -> dict:
        return self.__user

    @user.setter
    def user(self, value: dict):
        self._property_changed('user')
        self.__user = value        

    @property
    def customer(self) -> dict:
        return self.__customer

    @customer.setter
    def customer(self, value: dict):
        self._property_changed('customer')
        self.__customer = value        

    @property
    def leg1_reset_frequency(self) -> dict:
        return self.__leg1_reset_frequency

    @leg1_reset_frequency.setter
    def leg1_reset_frequency(self, value: dict):
        self._property_changed('leg1_reset_frequency')
        self.__leg1_reset_frequency = value        

    @property
    def queue_clock_time_label(self) -> tuple:
        return self.__queue_clock_time_label

    @queue_clock_time_label.setter
    def queue_clock_time_label(self, value: tuple):
        self._property_changed('queue_clock_time_label')
        self.__queue_clock_time_label = value        

    @property
    def pace_of_rollp100(self) -> dict:
        return self.__pace_of_rollp100

    @pace_of_rollp100.setter
    def pace_of_rollp100(self, value: dict):
        self._property_changed('pace_of_rollp100')
        self.__pace_of_rollp100 = value        

    @property
    def asset_classifications_gics_sub_industry(self) -> dict:
        return self.__asset_classifications_gics_sub_industry

    @asset_classifications_gics_sub_industry.setter
    def asset_classifications_gics_sub_industry(self, value: dict):
        self._property_changed('asset_classifications_gics_sub_industry')
        self.__asset_classifications_gics_sub_industry = value        

    @property
    def dew_point_hourly_forecast(self) -> dict:
        return self.__dew_point_hourly_forecast

    @dew_point_hourly_forecast.setter
    def dew_point_hourly_forecast(self, value: dict):
        self._property_changed('dew_point_hourly_forecast')
        self.__dew_point_hourly_forecast = value        

    @property
    def location_type(self) -> dict:
        return self.__location_type

    @location_type.setter
    def location_type(self, value: dict):
        self._property_changed('location_type')
        self.__location_type = value        

    @property
    def facet_divisional_reporting_group_id(self) -> dict:
        return self.__facet_divisional_reporting_group_id

    @facet_divisional_reporting_group_id.setter
    def facet_divisional_reporting_group_id(self, value: dict):
        self._property_changed('facet_divisional_reporting_group_id')
        self.__facet_divisional_reporting_group_id = value        

    @property
    def realized_twap_performance_usd(self) -> dict:
        return self.__realized_twap_performance_usd

    @realized_twap_performance_usd.setter
    def realized_twap_performance_usd(self, value: dict):
        self._property_changed('realized_twap_performance_usd')
        self.__realized_twap_performance_usd = value        

    @property
    def swap_rate(self) -> dict:
        return self.__swap_rate

    @swap_rate.setter
    def swap_rate(self, value: dict):
        self._property_changed('swap_rate')
        self.__swap_rate = value        

    @property
    def algo_execution_style(self) -> dict:
        return self.__algo_execution_style

    @algo_execution_style.setter
    def algo_execution_style(self, value: dict):
        self._property_changed('algo_execution_style')
        self.__algo_execution_style = value        

    @property
    def client_contact(self) -> dict:
        return self.__client_contact

    @client_contact.setter
    def client_contact(self, value: dict):
        self._property_changed('client_contact')
        self.__client_contact = value        

    @property
    def min_temperature_hour(self) -> dict:
        return self.__min_temperature_hour

    @min_temperature_hour.setter
    def min_temperature_hour(self, value: dict):
        self._property_changed('min_temperature_hour')
        self.__min_temperature_hour = value        

    @property
    def trading_currency(self) -> dict:
        return self.__trading_currency

    @trading_currency.setter
    def trading_currency(self, value: dict):
        self._property_changed('trading_currency')
        self.__trading_currency = value        

    @property
    def total_by_onset(self) -> dict:
        return self.__total_by_onset

    @total_by_onset.setter
    def total_by_onset(self, value: dict):
        self._property_changed('total_by_onset')
        self.__total_by_onset = value        

    @property
    def agency_swap_spread(self) -> dict:
        return self.__agency_swap_spread

    @agency_swap_spread.setter
    def agency_swap_spread(self, value: dict):
        self._property_changed('agency_swap_spread')
        self.__agency_swap_spread = value        

    @property
    def rank(self) -> dict:
        return self.__rank

    @rank.setter
    def rank(self, value: dict):
        self._property_changed('rank')
        self.__rank = value        

    @property
    def mixed_swap_other_reported_sdr(self) -> dict:
        return self.__mixed_swap_other_reported_sdr

    @mixed_swap_other_reported_sdr.setter
    def mixed_swap_other_reported_sdr(self, value: dict):
        self._property_changed('mixed_swap_other_reported_sdr')
        self.__mixed_swap_other_reported_sdr = value        

    @property
    def humidity(self) -> dict:
        return self.__humidity

    @humidity.setter
    def humidity(self, value: dict):
        self._property_changed('humidity')
        self.__humidity = value        

    @property
    def data_set_category(self) -> dict:
        return self.__data_set_category

    @data_set_category.setter
    def data_set_category(self, value: dict):
        self._property_changed('data_set_category')
        self.__data_set_category = value        

    @property
    def vwap_realized_bps(self) -> dict:
        return self.__vwap_realized_bps

    @vwap_realized_bps.setter
    def vwap_realized_bps(self, value: dict):
        self._property_changed('vwap_realized_bps')
        self.__vwap_realized_bps = value        

    @property
    def buy9bps(self) -> dict:
        return self.__buy9bps

    @buy9bps.setter
    def buy9bps(self, value: dict):
        self._property_changed('buy9bps')
        self.__buy9bps = value        

    @property
    def total_tested(self) -> dict:
        return self.__total_tested

    @total_tested.setter
    def total_tested(self, value: dict):
        self._property_changed('total_tested')
        self.__total_tested = value        

    @property
    def fatalities_confirmed(self) -> dict:
        return self.__fatalities_confirmed

    @fatalities_confirmed.setter
    def fatalities_confirmed(self, value: dict):
        self._property_changed('fatalities_confirmed')
        self.__fatalities_confirmed = value        

    @property
    def universe_id1(self) -> dict:
        return self.__universe_id1

    @universe_id1.setter
    def universe_id1(self, value: dict):
        self._property_changed('universe_id1')
        self.__universe_id1 = value        

    @property
    def asset_parameters_payer_day_count_fraction(self) -> dict:
        return self.__asset_parameters_payer_day_count_fraction

    @asset_parameters_payer_day_count_fraction.setter
    def asset_parameters_payer_day_count_fraction(self, value: dict):
        self._property_changed('asset_parameters_payer_day_count_fraction')
        self.__asset_parameters_payer_day_count_fraction = value        

    @property
    def universe_id2(self) -> dict:
        return self.__universe_id2

    @universe_id2.setter
    def universe_id2(self, value: dict):
        self._property_changed('universe_id2')
        self.__universe_id2 = value        

    @property
    def bid_low(self) -> dict:
        return self.__bid_low

    @bid_low.setter
    def bid_low(self, value: dict):
        self._property_changed('bid_low')
        self.__bid_low = value        

    @property
    def bucketize_price(self) -> dict:
        return self.__bucketize_price

    @bucketize_price.setter
    def bucketize_price(self, value: dict):
        self._property_changed('bucketize_price')
        self.__bucketize_price = value        

    @property
    def fair_variance_volatility(self) -> dict:
        return self.__fair_variance_volatility

    @fair_variance_volatility.setter
    def fair_variance_volatility(self, value: dict):
        self._property_changed('fair_variance_volatility')
        self.__fair_variance_volatility = value        

    @property
    def covid19(self) -> dict:
        return self.__covid19

    @covid19.setter
    def covid19(self, value: dict):
        self._property_changed('covid19')
        self.__covid19 = value        

    @property
    def client_exposure(self) -> dict:
        return self.__client_exposure

    @client_exposure.setter
    def client_exposure(self, value: dict):
        self._property_changed('client_exposure')
        self.__client_exposure = value        

    @property
    def leg2_total_notional_unit(self) -> dict:
        return self.__leg2_total_notional_unit

    @leg2_total_notional_unit.setter
    def leg2_total_notional_unit(self, value: dict):
        self._property_changed('leg2_total_notional_unit')
        self.__leg2_total_notional_unit = value        

    @property
    def sell45cents(self) -> dict:
        return self.__sell45cents

    @sell45cents.setter
    def sell45cents(self, value: dict):
        self._property_changed('sell45cents')
        self.__sell45cents = value        

    @property
    def gs_sustain_sub_sector(self) -> dict:
        return self.__gs_sustain_sub_sector

    @gs_sustain_sub_sector.setter
    def gs_sustain_sub_sector(self, value: dict):
        self._property_changed('gs_sustain_sub_sector')
        self.__gs_sustain_sub_sector = value        

    @property
    def sinkable(self) -> dict:
        return self.__sinkable

    @sinkable.setter
    def sinkable(self, value: dict):
        self._property_changed('sinkable')
        self.__sinkable = value        

    @property
    def is_real(self) -> dict:
        return self.__is_real

    @is_real.setter
    def is_real(self, value: dict):
        self._property_changed('is_real')
        self.__is_real = value        

    @property
    def max_temperature_hour(self) -> dict:
        return self.__max_temperature_hour

    @max_temperature_hour.setter
    def max_temperature_hour(self, value: dict):
        self._property_changed('max_temperature_hour')
        self.__max_temperature_hour = value        

    @property
    def leg2_averaging_method(self) -> dict:
        return self.__leg2_averaging_method

    @leg2_averaging_method.setter
    def leg2_averaging_method(self, value: dict):
        self._property_changed('leg2_averaging_method')
        self.__leg2_averaging_method = value        

    @property
    def jsn(self) -> dict:
        return self.__jsn

    @jsn.setter
    def jsn(self, value: dict):
        self._property_changed('jsn')
        self.__jsn = value        

    @property
    def sell160cents(self) -> dict:
        return self.__sell160cents

    @sell160cents.setter
    def sell160cents(self, value: dict):
        self._property_changed('sell160cents')
        self.__sell160cents = value        

    @property
    def knock_in_direction(self) -> dict:
        return self.__knock_in_direction

    @knock_in_direction.setter
    def knock_in_direction(self, value: dict):
        self._property_changed('knock_in_direction')
        self.__knock_in_direction = value        

    @property
    def day_close_unrealized_usd(self) -> dict:
        return self.__day_close_unrealized_usd

    @day_close_unrealized_usd.setter
    def day_close_unrealized_usd(self, value: dict):
        self._property_changed('day_close_unrealized_usd')
        self.__day_close_unrealized_usd = value        

    @property
    def tenor(self) -> dict:
        return self.__tenor

    @tenor.setter
    def tenor(self, value: dict):
        self._property_changed('tenor')
        self.__tenor = value        

    @property
    def pricing_convention(self) -> dict:
        return self.__pricing_convention

    @pricing_convention.setter
    def pricing_convention(self, value: dict):
        self._property_changed('pricing_convention')
        self.__pricing_convention = value        

    @property
    def popularity(self) -> dict:
        return self.__popularity

    @popularity.setter
    def popularity(self, value: dict):
        self._property_changed('popularity')
        self.__popularity = value        

    @property
    def floating_rate_option(self) -> dict:
        return self.__floating_rate_option

    @floating_rate_option.setter
    def floating_rate_option(self, value: dict):
        self._property_changed('floating_rate_option')
        self.__floating_rate_option = value        

    @property
    def hedge_value_type(self) -> dict:
        return self.__hedge_value_type

    @hedge_value_type.setter
    def hedge_value_type(self, value: dict):
        self._property_changed('hedge_value_type')
        self.__hedge_value_type = value        

    @property
    def asset_parameters_clearing_house(self) -> dict:
        return self.__asset_parameters_clearing_house

    @asset_parameters_clearing_house.setter
    def asset_parameters_clearing_house(self, value: dict):
        self._property_changed('asset_parameters_clearing_house')
        self.__asset_parameters_clearing_house = value        

    @property
    def disclaimer(self) -> dict:
        return self.__disclaimer

    @disclaimer.setter
    def disclaimer(self, value: dict):
        self._property_changed('disclaimer')
        self.__disclaimer = value        

    @property
    def payer_frequency(self) -> dict:
        return self.__payer_frequency

    @payer_frequency.setter
    def payer_frequency(self, value: dict):
        self._property_changed('payer_frequency')
        self.__payer_frequency = value        

    @property
    def loan_fee(self) -> dict:
        return self.__loan_fee

    @loan_fee.setter
    def loan_fee(self, value: dict):
        self._property_changed('loan_fee')
        self.__loan_fee = value        

    @property
    def deployment_version(self) -> dict:
        return self.__deployment_version

    @deployment_version.setter
    def deployment_version(self, value: dict):
        self._property_changed('deployment_version')
        self.__deployment_version = value        

    @property
    def buy16bps(self) -> dict:
        return self.__buy16bps

    @buy16bps.setter
    def buy16bps(self, value: dict):
        self._property_changed('buy16bps')
        self.__buy16bps = value        

    @property
    def trade_day_count(self) -> dict:
        return self.__trade_day_count

    @trade_day_count.setter
    def trade_day_count(self, value: dict):
        self._property_changed('trade_day_count')
        self.__trade_day_count = value        

    @property
    def price_to_sales(self) -> dict:
        return self.__price_to_sales

    @price_to_sales.setter
    def price_to_sales(self, value: dict):
        self._property_changed('price_to_sales')
        self.__price_to_sales = value        

    @property
    def new_ideas_qtd(self) -> dict:
        return self.__new_ideas_qtd

    @new_ideas_qtd.setter
    def new_ideas_qtd(self, value: dict):
        self._property_changed('new_ideas_qtd')
        self.__new_ideas_qtd = value        

    @property
    def subdivision_name(self) -> dict:
        return self.__subdivision_name

    @subdivision_name.setter
    def subdivision_name(self, value: dict):
        self._property_changed('subdivision_name')
        self.__subdivision_name = value        

    @property
    def adjusted_ask_price(self) -> dict:
        return self.__adjusted_ask_price

    @adjusted_ask_price.setter
    def adjusted_ask_price(self, value: dict):
        self._property_changed('adjusted_ask_price')
        self.__adjusted_ask_price = value        

    @property
    def factor_universe(self) -> dict:
        return self.__factor_universe

    @factor_universe.setter
    def factor_universe(self, value: dict):
        self._property_changed('factor_universe')
        self.__factor_universe = value        

    @property
    def arrival_rt(self) -> dict:
        return self.__arrival_rt

    @arrival_rt.setter
    def arrival_rt(self, value: dict):
        self._property_changed('arrival_rt')
        self.__arrival_rt = value        

    @property
    def internal_index_calc_agent(self) -> dict:
        return self.__internal_index_calc_agent

    @internal_index_calc_agent.setter
    def internal_index_calc_agent(self, value: dict):
        self._property_changed('internal_index_calc_agent')
        self.__internal_index_calc_agent = value        

    @property
    def excess_margin_value(self) -> dict:
        return self.__excess_margin_value

    @excess_margin_value.setter
    def excess_margin_value(self, value: dict):
        self._property_changed('excess_margin_value')
        self.__excess_margin_value = value        

    @property
    def transaction_cost(self) -> dict:
        return self.__transaction_cost

    @transaction_cost.setter
    def transaction_cost(self, value: dict):
        self._property_changed('transaction_cost')
        self.__transaction_cost = value        

    @property
    def central_bank_swap_rate(self) -> dict:
        return self.__central_bank_swap_rate

    @central_bank_swap_rate.setter
    def central_bank_swap_rate(self, value: dict):
        self._property_changed('central_bank_swap_rate')
        self.__central_bank_swap_rate = value        

    @property
    def previous_new_confirmed(self) -> dict:
        return self.__previous_new_confirmed

    @previous_new_confirmed.setter
    def previous_new_confirmed(self, value: dict):
        self._property_changed('previous_new_confirmed')
        self.__previous_new_confirmed = value        

    @property
    def unrealized_vwap_performance_bps(self) -> dict:
        return self.__unrealized_vwap_performance_bps

    @unrealized_vwap_performance_bps.setter
    def unrealized_vwap_performance_bps(self, value: dict):
        self._property_changed('unrealized_vwap_performance_bps')
        self.__unrealized_vwap_performance_bps = value        

    @property
    def degree_days_daily_forecast(self) -> dict:
        return self.__degree_days_daily_forecast

    @degree_days_daily_forecast.setter
    def degree_days_daily_forecast(self, value: dict):
        self._property_changed('degree_days_daily_forecast')
        self.__degree_days_daily_forecast = value        

    @property
    def position_amount(self) -> dict:
        return self.__position_amount

    @position_amount.setter
    def position_amount(self, value: dict):
        self._property_changed('position_amount')
        self.__position_amount = value        

    @property
    def heat_index_hourly_forecast(self) -> dict:
        return self.__heat_index_hourly_forecast

    @heat_index_hourly_forecast.setter
    def heat_index_hourly_forecast(self, value: dict):
        self._property_changed('heat_index_hourly_forecast')
        self.__heat_index_hourly_forecast = value        

    @property
    def ma_rank(self) -> dict:
        return self.__ma_rank

    @ma_rank.setter
    def ma_rank(self, value: dict):
        self._property_changed('ma_rank')
        self.__ma_rank = value        

    @property
    def fx_positioning_source(self) -> dict:
        return self.__fx_positioning_source

    @fx_positioning_source.setter
    def fx_positioning_source(self, value: dict):
        self._property_changed('fx_positioning_source')
        self.__fx_positioning_source = value        

    @property
    def implied_volatility_by_delta_strike(self) -> dict:
        return self.__implied_volatility_by_delta_strike

    @implied_volatility_by_delta_strike.setter
    def implied_volatility_by_delta_strike(self, value: dict):
        self._property_changed('implied_volatility_by_delta_strike')
        self.__implied_volatility_by_delta_strike = value        

    @property
    def mq_symbol(self) -> dict:
        return self.__mq_symbol

    @mq_symbol.setter
    def mq_symbol(self, value: dict):
        self._property_changed('mq_symbol')
        self.__mq_symbol = value        

    @property
    def num_total_units(self) -> dict:
        return self.__num_total_units

    @num_total_units.setter
    def num_total_units(self, value: dict):
        self._property_changed('num_total_units')
        self.__num_total_units = value        

    @property
    def corporate_action(self) -> dict:
        return self.__corporate_action

    @corporate_action.setter
    def corporate_action(self, value: dict):
        self._property_changed('corporate_action')
        self.__corporate_action = value        

    @property
    def leg1_price_type(self) -> dict:
        return self.__leg1_price_type

    @leg1_price_type.setter
    def leg1_price_type(self, value: dict):
        self._property_changed('leg1_price_type')
        self.__leg1_price_type = value        

    @property
    def asset_parameters_payer_rate_option(self) -> dict:
        return self.__asset_parameters_payer_rate_option

    @asset_parameters_payer_rate_option.setter
    def asset_parameters_payer_rate_option(self, value: dict):
        self._property_changed('asset_parameters_payer_rate_option')
        self.__asset_parameters_payer_rate_option = value        

    @property
    def sell20cents(self) -> dict:
        return self.__sell20cents

    @sell20cents.setter
    def sell20cents(self, value: dict):
        self._property_changed('sell20cents')
        self.__sell20cents = value        

    @property
    def leg2_fixed_payment_currency(self) -> dict:
        return self.__leg2_fixed_payment_currency

    @leg2_fixed_payment_currency.setter
    def leg2_fixed_payment_currency(self, value: dict):
        self._property_changed('leg2_fixed_payment_currency')
        self.__leg2_fixed_payment_currency = value        

    @property
    def g_regional_score(self) -> dict:
        return self.__g_regional_score

    @g_regional_score.setter
    def g_regional_score(self, value: dict):
        self._property_changed('g_regional_score')
        self.__g_regional_score = value        

    @property
    def hard_to_borrow(self) -> dict:
        return self.__hard_to_borrow

    @hard_to_borrow.setter
    def hard_to_borrow(self, value: dict):
        self._property_changed('hard_to_borrow')
        self.__hard_to_borrow = value        

    @property
    def sell5bps(self) -> dict:
        return self.__sell5bps

    @sell5bps.setter
    def sell5bps(self, value: dict):
        self._property_changed('sell5bps')
        self.__sell5bps = value        

    @property
    def roll_vwap(self) -> dict:
        return self.__roll_vwap

    @roll_vwap.setter
    def roll_vwap(self, value: dict):
        self._property_changed('roll_vwap')
        self.__roll_vwap = value        

    @property
    def wpk(self) -> dict:
        return self.__wpk

    @wpk.setter
    def wpk(self, value: dict):
        self._property_changed('wpk')
        self.__wpk = value        

    @property
    def bespoke_swap(self) -> dict:
        return self.__bespoke_swap

    @bespoke_swap.setter
    def bespoke_swap(self, value: dict):
        self._property_changed('bespoke_swap')
        self.__bespoke_swap = value        

    @property
    def asset_parameters_expiration_date(self) -> dict:
        return self.__asset_parameters_expiration_date

    @asset_parameters_expiration_date.setter
    def asset_parameters_expiration_date(self, value: dict):
        self._property_changed('asset_parameters_expiration_date')
        self.__asset_parameters_expiration_date = value        

    @property
    def country_name(self) -> dict:
        return self.__country_name

    @country_name.setter
    def country_name(self, value: dict):
        self._property_changed('country_name')
        self.__country_name = value        

    @property
    def carry(self) -> dict:
        return self.__carry

    @carry.setter
    def carry(self, value: dict):
        self._property_changed('carry')
        self.__carry = value        

    @property
    def starting_date(self) -> dict:
        return self.__starting_date

    @starting_date.setter
    def starting_date(self, value: dict):
        self._property_changed('starting_date')
        self.__starting_date = value        

    @property
    def loan_id(self) -> dict:
        return self.__loan_id

    @loan_id.setter
    def loan_id(self, value: dict):
        self._property_changed('loan_id')
        self.__loan_id = value        

    @property
    def onboarded(self) -> dict:
        return self.__onboarded

    @onboarded.setter
    def onboarded(self, value: dict):
        self._property_changed('onboarded')
        self.__onboarded = value        

    @property
    def liquidity_score(self) -> dict:
        return self.__liquidity_score

    @liquidity_score.setter
    def liquidity_score(self, value: dict):
        self._property_changed('liquidity_score')
        self.__liquidity_score = value        

    @property
    def long_rates_contribution(self) -> dict:
        return self.__long_rates_contribution

    @long_rates_contribution.setter
    def long_rates_contribution(self, value: dict):
        self._property_changed('long_rates_contribution')
        self.__long_rates_contribution = value        

    @property
    def source_date_span(self) -> dict:
        return self.__source_date_span

    @source_date_span.setter
    def source_date_span(self, value: dict):
        self._property_changed('source_date_span')
        self.__source_date_span = value        

    @property
    def ann_yield6_month(self) -> dict:
        return self.__ann_yield6_month

    @ann_yield6_month.setter
    def ann_yield6_month(self, value: dict):
        self._property_changed('ann_yield6_month')
        self.__ann_yield6_month = value        

    @property
    def underlying_data_set_id(self) -> dict:
        return self.__underlying_data_set_id

    @underlying_data_set_id.setter
    def underlying_data_set_id(self, value: dict):
        self._property_changed('underlying_data_set_id')
        self.__underlying_data_set_id = value        

    @property
    def close_unadjusted(self) -> dict:
        return self.__close_unadjusted

    @close_unadjusted.setter
    def close_unadjusted(self, value: dict):
        self._property_changed('close_unadjusted')
        self.__close_unadjusted = value        

    @property
    def value_unit(self) -> dict:
        return self.__value_unit

    @value_unit.setter
    def value_unit(self, value: dict):
        self._property_changed('value_unit')
        self.__value_unit = value        

    @property
    def quantity_unit(self) -> dict:
        return self.__quantity_unit

    @quantity_unit.setter
    def quantity_unit(self, value: dict):
        self._property_changed('quantity_unit')
        self.__quantity_unit = value        

    @property
    def adjusted_low_price(self) -> dict:
        return self.__adjusted_low_price

    @adjusted_low_price.setter
    def adjusted_low_price(self, value: dict):
        self._property_changed('adjusted_low_price')
        self.__adjusted_low_price = value        

    @property
    def is_momentum(self) -> dict:
        return self.__is_momentum

    @is_momentum.setter
    def is_momentum(self, value: dict):
        self._property_changed('is_momentum')
        self.__is_momentum = value        

    @property
    def long_conviction_large(self) -> dict:
        return self.__long_conviction_large

    @long_conviction_large.setter
    def long_conviction_large(self, value: dict):
        self._property_changed('long_conviction_large')
        self.__long_conviction_large = value        

    @property
    def oad(self) -> dict:
        return self.__oad

    @oad.setter
    def oad(self, value: dict):
        self._property_changed('oad')
        self.__oad = value        

    @property
    def rate(self) -> dict:
        return self.__rate

    @rate.setter
    def rate(self, value: dict):
        self._property_changed('rate')
        self.__rate = value        

    @property
    def coupon_type(self) -> dict:
        return self.__coupon_type

    @coupon_type.setter
    def coupon_type(self, value: dict):
        self._property_changed('coupon_type')
        self.__coupon_type = value        

    @property
    def client(self) -> dict:
        return self.__client

    @client.setter
    def client(self, value: dict):
        self._property_changed('client')
        self.__client = value        

    @property
    def conviction_list(self) -> dict:
        return self.__conviction_list

    @conviction_list.setter
    def conviction_list(self, value: dict):
        self._property_changed('conviction_list')
        self.__conviction_list = value        

    @property
    def passive_etf_ratio(self) -> dict:
        return self.__passive_etf_ratio

    @passive_etf_ratio.setter
    def passive_etf_ratio(self, value: dict):
        self._property_changed('passive_etf_ratio')
        self.__passive_etf_ratio = value        

    @property
    def future_month_g26(self) -> dict:
        return self.__future_month_g26

    @future_month_g26.setter
    def future_month_g26(self, value: dict):
        self._property_changed('future_month_g26')
        self.__future_month_g26 = value        

    @property
    def future_month_g25(self) -> dict:
        return self.__future_month_g25

    @future_month_g25.setter
    def future_month_g25(self, value: dict):
        self._property_changed('future_month_g25')
        self.__future_month_g25 = value        

    @property
    def future_month_g24(self) -> dict:
        return self.__future_month_g24

    @future_month_g24.setter
    def future_month_g24(self, value: dict):
        self._property_changed('future_month_g24')
        self.__future_month_g24 = value        

    @property
    def future_month_g23(self) -> dict:
        return self.__future_month_g23

    @future_month_g23.setter
    def future_month_g23(self, value: dict):
        self._property_changed('future_month_g23')
        self.__future_month_g23 = value        

    @property
    def type_of_return(self) -> dict:
        return self.__type_of_return

    @type_of_return.setter
    def type_of_return(self, value: dict):
        self._property_changed('type_of_return')
        self.__type_of_return = value        

    @property
    def future_month_g22(self) -> dict:
        return self.__future_month_g22

    @future_month_g22.setter
    def future_month_g22(self, value: dict):
        self._property_changed('future_month_g22')
        self.__future_month_g22 = value        

    @property
    def servicing_cost_long_pnl(self) -> dict:
        return self.__servicing_cost_long_pnl

    @servicing_cost_long_pnl.setter
    def servicing_cost_long_pnl(self, value: dict):
        self._property_changed('servicing_cost_long_pnl')
        self.__servicing_cost_long_pnl = value        

    @property
    def excess_margin_percentage(self) -> dict:
        return self.__excess_margin_percentage

    @excess_margin_percentage.setter
    def excess_margin_percentage(self, value: dict):
        self._property_changed('excess_margin_percentage')
        self.__excess_margin_percentage = value        

    @property
    def future_month_g21(self) -> dict:
        return self.__future_month_g21

    @future_month_g21.setter
    def future_month_g21(self, value: dict):
        self._property_changed('future_month_g21')
        self.__future_month_g21 = value        

    @property
    def total_mild(self) -> dict:
        return self.__total_mild

    @total_mild.setter
    def total_mild(self, value: dict):
        self._property_changed('total_mild')
        self.__total_mild = value        

    @property
    def realized_arrival_performance_bps(self) -> dict:
        return self.__realized_arrival_performance_bps

    @realized_arrival_performance_bps.setter
    def realized_arrival_performance_bps(self, value: dict):
        self._property_changed('realized_arrival_performance_bps')
        self.__realized_arrival_performance_bps = value        

    @property
    def precipitation_daily_forecast_inches(self) -> dict:
        return self.__precipitation_daily_forecast_inches

    @precipitation_daily_forecast_inches.setter
    def precipitation_daily_forecast_inches(self, value: dict):
        self._property_changed('precipitation_daily_forecast_inches')
        self.__precipitation_daily_forecast_inches = value        

    @property
    def exchange_id(self) -> dict:
        return self.__exchange_id

    @exchange_id.setter
    def exchange_id(self, value: dict):
        self._property_changed('exchange_id')
        self.__exchange_id = value        

    @property
    def leg2_fixed_payment(self) -> dict:
        return self.__leg2_fixed_payment

    @leg2_fixed_payment.setter
    def leg2_fixed_payment(self, value: dict):
        self._property_changed('leg2_fixed_payment')
        self.__leg2_fixed_payment = value        

    @property
    def tcm_cost_horizon20_day(self) -> dict:
        return self.__tcm_cost_horizon20_day

    @tcm_cost_horizon20_day.setter
    def tcm_cost_horizon20_day(self, value: dict):
        self._property_changed('tcm_cost_horizon20_day')
        self.__tcm_cost_horizon20_day = value        

    @property
    def realm(self) -> dict:
        return self.__realm

    @realm.setter
    def realm(self, value: dict):
        self._property_changed('realm')
        self.__realm = value        

    @property
    def bid(self) -> dict:
        return self.__bid

    @bid.setter
    def bid(self, value: dict):
        self._property_changed('bid')
        self.__bid = value        

    @property
    def hedge_value(self) -> dict:
        return self.__hedge_value

    @hedge_value.setter
    def hedge_value(self, value: dict):
        self._property_changed('hedge_value')
        self.__hedge_value = value        

    @property
    def is_aggressive(self) -> dict:
        return self.__is_aggressive

    @is_aggressive.setter
    def is_aggressive(self, value: dict):
        self._property_changed('is_aggressive')
        self.__is_aggressive = value        

    @property
    def floating_rate_designated_maturity(self) -> dict:
        return self.__floating_rate_designated_maturity

    @floating_rate_designated_maturity.setter
    def floating_rate_designated_maturity(self, value: dict):
        self._property_changed('floating_rate_designated_maturity')
        self.__floating_rate_designated_maturity = value        

    @property
    def percentage_near_executed_quantity(self) -> dict:
        return self.__percentage_near_executed_quantity

    @percentage_near_executed_quantity.setter
    def percentage_near_executed_quantity(self, value: dict):
        self._property_changed('percentage_near_executed_quantity')
        self.__percentage_near_executed_quantity = value        

    @property
    def order_id(self) -> dict:
        return self.__order_id

    @order_id.setter
    def order_id(self, value: dict):
        self._property_changed('order_id')
        self.__order_id = value        

    @property
    def hospital_type(self) -> dict:
        return self.__hospital_type

    @hospital_type.setter
    def hospital_type(self, value: dict):
        self._property_changed('hospital_type')
        self.__hospital_type = value        

    @property
    def day_close_realized_bps(self) -> dict:
        return self.__day_close_realized_bps

    @day_close_realized_bps.setter
    def day_close_realized_bps(self, value: dict):
        self._property_changed('day_close_realized_bps')
        self.__day_close_realized_bps = value        

    @property
    def precipitation_hourly_forecast(self) -> dict:
        return self.__precipitation_hourly_forecast

    @precipitation_hourly_forecast.setter
    def precipitation_hourly_forecast(self, value: dict):
        self._property_changed('precipitation_hourly_forecast')
        self.__precipitation_hourly_forecast = value        

    @property
    def market_cap_usd(self) -> dict:
        return self.__market_cap_usd

    @market_cap_usd.setter
    def market_cap_usd(self, value: dict):
        self._property_changed('market_cap_usd')
        self.__market_cap_usd = value        

    @property
    def auction_fills_percentage(self) -> dict:
        return self.__auction_fills_percentage

    @auction_fills_percentage.setter
    def auction_fills_percentage(self, value: dict):
        self._property_changed('auction_fills_percentage')
        self.__auction_fills_percentage = value        

    @property
    def high_price(self) -> dict:
        return self.__high_price

    @high_price.setter
    def high_price(self, value: dict):
        self._property_changed('high_price')
        self.__high_price = value        

    @property
    def absolute_shares(self) -> dict:
        return self.__absolute_shares

    @absolute_shares.setter
    def absolute_shares(self, value: dict):
        self._property_changed('absolute_shares')
        self.__absolute_shares = value        

    @property
    def fixed_rate_day_count_fraction(self) -> dict:
        return self.__fixed_rate_day_count_fraction

    @fixed_rate_day_count_fraction.setter
    def fixed_rate_day_count_fraction(self, value: dict):
        self._property_changed('fixed_rate_day_count_fraction')
        self.__fixed_rate_day_count_fraction = value        

    @property
    def model(self) -> dict:
        return self.__model

    @model.setter
    def model(self, value: dict):
        self._property_changed('model')
        self.__model = value        

    @property
    def unrealized_twap_performance_usd(self) -> dict:
        return self.__unrealized_twap_performance_usd

    @unrealized_twap_performance_usd.setter
    def unrealized_twap_performance_usd(self, value: dict):
        self._property_changed('unrealized_twap_performance_usd')
        self.__unrealized_twap_performance_usd = value        

    @property
    def id(self) -> dict:
        return self.__id

    @id.setter
    def id(self, value: dict):
        self._property_changed('id')
        self.__id = value        

    @property
    def maturity(self) -> dict:
        return self.__maturity

    @maturity.setter
    def maturity(self, value: dict):
        self._property_changed('maturity')
        self.__maturity = value        

    @property
    def delta_change(self) -> dict:
        return self.__delta_change

    @delta_change.setter
    def delta_change(self, value: dict):
        self._property_changed('delta_change')
        self.__delta_change = value        

    @property
    def index(self) -> dict:
        return self.__index

    @index.setter
    def index(self, value: dict):
        self._property_changed('index')
        self.__index = value        

    @property
    def unrealized_arrival_performance_usd(self) -> dict:
        return self.__unrealized_arrival_performance_usd

    @unrealized_arrival_performance_usd.setter
    def unrealized_arrival_performance_usd(self, value: dict):
        self._property_changed('unrealized_arrival_performance_usd')
        self.__unrealized_arrival_performance_usd = value        

    @property
    def iceberg_slippage(self) -> dict:
        return self.__iceberg_slippage

    @iceberg_slippage.setter
    def iceberg_slippage(self, value: dict):
        self._property_changed('iceberg_slippage')
        self.__iceberg_slippage = value        

    @property
    def sell120cents(self) -> dict:
        return self.__sell120cents

    @sell120cents.setter
    def sell120cents(self, value: dict):
        self._property_changed('sell120cents')
        self.__sell120cents = value        

    @property
    def future_month_x26(self) -> dict:
        return self.__future_month_x26

    @future_month_x26.setter
    def future_month_x26(self, value: dict):
        self._property_changed('future_month_x26')
        self.__future_month_x26 = value        

    @property
    def asset_types(self) -> dict:
        return self.__asset_types

    @asset_types.setter
    def asset_types(self, value: dict):
        self._property_changed('asset_types')
        self.__asset_types = value        

    @property
    def future_month_x25(self) -> dict:
        return self.__future_month_x25

    @future_month_x25.setter
    def future_month_x25(self, value: dict):
        self._property_changed('future_month_x25')
        self.__future_month_x25 = value        

    @property
    def bcid(self) -> dict:
        return self.__bcid

    @bcid.setter
    def bcid(self, value: dict):
        self._property_changed('bcid')
        self.__bcid = value        

    @property
    def mkt_point(self) -> dict:
        return self.__mkt_point

    @mkt_point.setter
    def mkt_point(self, value: dict):
        self._property_changed('mkt_point')
        self.__mkt_point = value        

    @property
    def future_month_x24(self) -> dict:
        return self.__future_month_x24

    @future_month_x24.setter
    def future_month_x24(self, value: dict):
        self._property_changed('future_month_x24')
        self.__future_month_x24 = value        

    @property
    def restriction_start_date(self) -> dict:
        return self.__restriction_start_date

    @restriction_start_date.setter
    def restriction_start_date(self, value: dict):
        self._property_changed('restriction_start_date')
        self.__restriction_start_date = value        

    @property
    def touch_liquidity_score(self) -> dict:
        return self.__touch_liquidity_score

    @touch_liquidity_score.setter
    def touch_liquidity_score(self, value: dict):
        self._property_changed('touch_liquidity_score')
        self.__touch_liquidity_score = value        

    @property
    def future_month_x23(self) -> dict:
        return self.__future_month_x23

    @future_month_x23.setter
    def future_month_x23(self, value: dict):
        self._property_changed('future_month_x23')
        self.__future_month_x23 = value        

    @property
    def future_month_x22(self) -> dict:
        return self.__future_month_x22

    @future_month_x22.setter
    def future_month_x22(self, value: dict):
        self._property_changed('future_month_x22')
        self.__future_month_x22 = value        

    @property
    def factor_category_id(self) -> dict:
        return self.__factor_category_id

    @factor_category_id.setter
    def factor_category_id(self, value: dict):
        self._property_changed('factor_category_id')
        self.__factor_category_id = value        

    @property
    def security_type_id(self) -> dict:
        return self.__security_type_id

    @security_type_id.setter
    def security_type_id(self, value: dict):
        self._property_changed('security_type_id')
        self.__security_type_id = value        

    @property
    def future_month_x21(self) -> dict:
        return self.__future_month_x21

    @future_month_x21.setter
    def future_month_x21(self, value: dict):
        self._property_changed('future_month_x21')
        self.__future_month_x21 = value        

    @property
    def investment_ytd(self) -> dict:
        return self.__investment_ytd

    @investment_ytd.setter
    def investment_ytd(self, value: dict):
        self._property_changed('investment_ytd')
        self.__investment_ytd = value        

    @property
    def leg2_notional(self) -> dict:
        return self.__leg2_notional

    @leg2_notional.setter
    def leg2_notional(self, value: dict):
        self._property_changed('leg2_notional')
        self.__leg2_notional = value        

    @property
    def sell1bps(self) -> dict:
        return self.__sell1bps

    @sell1bps.setter
    def sell1bps(self, value: dict):
        self._property_changed('sell1bps')
        self.__sell1bps = value        

    @property
    def sell200cents(self) -> dict:
        return self.__sell200cents

    @sell200cents.setter
    def sell200cents(self, value: dict):
        self._property_changed('sell200cents')
        self.__sell200cents = value        

    @property
    def expected_completion_date(self) -> dict:
        return self.__expected_completion_date

    @expected_completion_date.setter
    def expected_completion_date(self, value: dict):
        self._property_changed('expected_completion_date')
        self.__expected_completion_date = value        

    @property
    def spread_option_vol(self) -> dict:
        return self.__spread_option_vol

    @spread_option_vol.setter
    def spread_option_vol(self, value: dict):
        self._property_changed('spread_option_vol')
        self.__spread_option_vol = value        

    @property
    def sell80cents(self) -> dict:
        return self.__sell80cents

    @sell80cents.setter
    def sell80cents(self, value: dict):
        self._property_changed('sell80cents')
        self.__sell80cents = value        

    @property
    def inflation_swap_rate(self) -> dict:
        return self.__inflation_swap_rate

    @inflation_swap_rate.setter
    def inflation_swap_rate(self, value: dict):
        self._property_changed('inflation_swap_rate')
        self.__inflation_swap_rate = value        

    @property
    def active_queries(self) -> dict:
        return self.__active_queries

    @active_queries.setter
    def active_queries(self, value: dict):
        self._property_changed('active_queries')
        self.__active_queries = value        

    @property
    def sell45bps(self) -> dict:
        return self.__sell45bps

    @sell45bps.setter
    def sell45bps(self, value: dict):
        self._property_changed('sell45bps')
        self.__sell45bps = value        

    @property
    def embeded_option(self) -> dict:
        return self.__embeded_option

    @embeded_option.setter
    def embeded_option(self, value: dict):
        self._property_changed('embeded_option')
        self.__embeded_option = value        

    @property
    def event_source(self) -> dict:
        return self.__event_source

    @event_source.setter
    def event_source(self, value: dict):
        self._property_changed('event_source')
        self.__event_source = value        

    @property
    def qis_perm_no(self) -> dict:
        return self.__qis_perm_no

    @qis_perm_no.setter
    def qis_perm_no(self, value: dict):
        self._property_changed('qis_perm_no')
        self.__qis_perm_no = value        

    @property
    def settlement(self) -> dict:
        return self.__settlement

    @settlement.setter
    def settlement(self, value: dict):
        self._property_changed('settlement')
        self.__settlement = value        

    @property
    def shareclass_id(self) -> dict:
        return self.__shareclass_id

    @shareclass_id.setter
    def shareclass_id(self, value: dict):
        self._property_changed('shareclass_id')
        self.__shareclass_id = value        

    @property
    def feature2(self) -> dict:
        return self.__feature2

    @feature2.setter
    def feature2(self, value: dict):
        self._property_changed('feature2')
        self.__feature2 = value        

    @property
    def feature3(self) -> dict:
        return self.__feature3

    @feature3.setter
    def feature3(self, value: dict):
        self._property_changed('feature3')
        self.__feature3 = value        

    @property
    def sts_commodity_sector(self) -> dict:
        return self.__sts_commodity_sector

    @sts_commodity_sector.setter
    def sts_commodity_sector(self, value: dict):
        self._property_changed('sts_commodity_sector')
        self.__sts_commodity_sector = value        

    @property
    def exception_status(self) -> dict:
        return self.__exception_status

    @exception_status.setter
    def exception_status(self, value: dict):
        self._property_changed('exception_status')
        self.__exception_status = value        

    @property
    def overnight_news_intensity(self) -> dict:
        return self.__overnight_news_intensity

    @overnight_news_intensity.setter
    def overnight_news_intensity(self, value: dict):
        self._property_changed('overnight_news_intensity')
        self.__overnight_news_intensity = value        

    @property
    def sales_coverage(self) -> dict:
        return self.__sales_coverage

    @sales_coverage.setter
    def sales_coverage(self, value: dict):
        self._property_changed('sales_coverage')
        self.__sales_coverage = value        

    @property
    def feature1(self) -> dict:
        return self.__feature1

    @feature1.setter
    def feature1(self, value: dict):
        self._property_changed('feature1')
        self.__feature1 = value        

    @property
    def tcm_cost_participation_rate10_pct(self) -> dict:
        return self.__tcm_cost_participation_rate10_pct

    @tcm_cost_participation_rate10_pct.setter
    def tcm_cost_participation_rate10_pct(self, value: dict):
        self._property_changed('tcm_cost_participation_rate10_pct')
        self.__tcm_cost_participation_rate10_pct = value        

    @property
    def event_time(self) -> dict:
        return self.__event_time

    @event_time.setter
    def event_time(self, value: dict):
        self._property_changed('event_time')
        self.__event_time = value        

    @property
    def position_source_name(self) -> dict:
        return self.__position_source_name

    @position_source_name.setter
    def position_source_name(self, value: dict):
        self._property_changed('position_source_name')
        self.__position_source_name = value        

    @property
    def delivery_date(self) -> dict:
        return self.__delivery_date

    @delivery_date.setter
    def delivery_date(self, value: dict):
        self._property_changed('delivery_date')
        self.__delivery_date = value        

    @property
    def interest_rate(self) -> dict:
        return self.__interest_rate

    @interest_rate.setter
    def interest_rate(self, value: dict):
        self._property_changed('interest_rate')
        self.__interest_rate = value        

    @property
    def side(self) -> dict:
        return self.__side

    @side.setter
    def side(self, value: dict):
        self._property_changed('side')
        self.__side = value        

    @property
    def dynamic_hybrid_aggressive_style(self) -> dict:
        return self.__dynamic_hybrid_aggressive_style

    @dynamic_hybrid_aggressive_style.setter
    def dynamic_hybrid_aggressive_style(self, value: dict):
        self._property_changed('dynamic_hybrid_aggressive_style')
        self.__dynamic_hybrid_aggressive_style = value        

    @property
    def compliance_restricted_status(self) -> dict:
        return self.__compliance_restricted_status

    @compliance_restricted_status.setter
    def compliance_restricted_status(self, value: dict):
        self._property_changed('compliance_restricted_status')
        self.__compliance_restricted_status = value        

    @property
    def borrow_fee(self) -> dict:
        return self.__borrow_fee

    @borrow_fee.setter
    def borrow_fee(self, value: dict):
        self._property_changed('borrow_fee')
        self.__borrow_fee = value        

    @property
    def ever_icu(self) -> dict:
        return self.__ever_icu

    @ever_icu.setter
    def ever_icu(self, value: dict):
        self._property_changed('ever_icu')
        self.__ever_icu = value        

    @property
    def no_worse_than_level(self) -> dict:
        return self.__no_worse_than_level

    @no_worse_than_level.setter
    def no_worse_than_level(self, value: dict):
        self._property_changed('no_worse_than_level')
        self.__no_worse_than_level = value        

    @property
    def loan_spread(self) -> dict:
        return self.__loan_spread

    @loan_spread.setter
    def loan_spread(self, value: dict):
        self._property_changed('loan_spread')
        self.__loan_spread = value        

    @property
    def tcm_cost_horizon12_hour(self) -> dict:
        return self.__tcm_cost_horizon12_hour

    @tcm_cost_horizon12_hour.setter
    def tcm_cost_horizon12_hour(self, value: dict):
        self._property_changed('tcm_cost_horizon12_hour')
        self.__tcm_cost_horizon12_hour = value        

    @property
    def dew_point(self) -> dict:
        return self.__dew_point

    @dew_point.setter
    def dew_point(self, value: dict):
        self._property_changed('dew_point')
        self.__dew_point = value        

    @property
    def research_commission(self) -> dict:
        return self.__research_commission

    @research_commission.setter
    def research_commission(self, value: dict):
        self._property_changed('research_commission')
        self.__research_commission = value        

    @property
    def buy2bps(self) -> dict:
        return self.__buy2bps

    @buy2bps.setter
    def buy2bps(self, value: dict):
        self._property_changed('buy2bps')
        self.__buy2bps = value        

    @property
    def asset_classifications_risk_country_code(self) -> dict:
        return self.__asset_classifications_risk_country_code

    @asset_classifications_risk_country_code.setter
    def asset_classifications_risk_country_code(self, value: dict):
        self._property_changed('asset_classifications_risk_country_code')
        self.__asset_classifications_risk_country_code = value        

    @property
    def new_ideas_mtd(self) -> dict:
        return self.__new_ideas_mtd

    @new_ideas_mtd.setter
    def new_ideas_mtd(self, value: dict):
        self._property_changed('new_ideas_mtd')
        self.__new_ideas_mtd = value        

    @property
    def var_swap_by_expiry(self) -> dict:
        return self.__var_swap_by_expiry

    @var_swap_by_expiry.setter
    def var_swap_by_expiry(self, value: dict):
        self._property_changed('var_swap_by_expiry')
        self.__var_swap_by_expiry = value        

    @property
    def sell_date(self) -> dict:
        return self.__sell_date

    @sell_date.setter
    def sell_date(self, value: dict):
        self._property_changed('sell_date')
        self.__sell_date = value        

    @property
    def aum_start(self) -> dict:
        return self.__aum_start

    @aum_start.setter
    def aum_start(self, value: dict):
        self._property_changed('aum_start')
        self.__aum_start = value        

    @property
    def asset_parameters_settlement(self) -> dict:
        return self.__asset_parameters_settlement

    @asset_parameters_settlement.setter
    def asset_parameters_settlement(self, value: dict):
        self._property_changed('asset_parameters_settlement')
        self.__asset_parameters_settlement = value        

    @property
    def max_temperature(self) -> dict:
        return self.__max_temperature

    @max_temperature.setter
    def max_temperature(self, value: dict):
        self._property_changed('max_temperature')
        self.__max_temperature = value        

    @property
    def acquirer_shareholder_meeting_date(self) -> dict:
        return self.__acquirer_shareholder_meeting_date

    @acquirer_shareholder_meeting_date.setter
    def acquirer_shareholder_meeting_date(self, value: dict):
        self._property_changed('acquirer_shareholder_meeting_date')
        self.__acquirer_shareholder_meeting_date = value        

    @property
    def count_ideas_wtd(self) -> dict:
        return self.__count_ideas_wtd

    @count_ideas_wtd.setter
    def count_ideas_wtd(self, value: dict):
        self._property_changed('count_ideas_wtd')
        self.__count_ideas_wtd = value        

    @property
    def arrival_rt_normalized(self) -> dict:
        return self.__arrival_rt_normalized

    @arrival_rt_normalized.setter
    def arrival_rt_normalized(self, value: dict):
        self._property_changed('arrival_rt_normalized')
        self.__arrival_rt_normalized = value        

    @property
    def report_type(self) -> dict:
        return self.__report_type

    @report_type.setter
    def report_type(self, value: dict):
        self._property_changed('report_type')
        self.__report_type = value        

    @property
    def source_url(self) -> dict:
        return self.__source_url

    @source_url.setter
    def source_url(self, value: dict):
        self._property_changed('source_url')
        self.__source_url = value        

    @property
    def estimated_return(self) -> dict:
        return self.__estimated_return

    @estimated_return.setter
    def estimated_return(self, value: dict):
        self._property_changed('estimated_return')
        self.__estimated_return = value        

    @property
    def high(self) -> dict:
        return self.__high

    @high.setter
    def high(self, value: dict):
        self._property_changed('high')
        self.__high = value        

    @property
    def source_last_update(self) -> dict:
        return self.__source_last_update

    @source_last_update.setter
    def source_last_update(self, value: dict):
        self._property_changed('source_last_update')
        self.__source_last_update = value        

    @property
    def sunshine_forecast(self) -> dict:
        return self.__sunshine_forecast

    @sunshine_forecast.setter
    def sunshine_forecast(self, value: dict):
        self._property_changed('sunshine_forecast')
        self.__sunshine_forecast = value        

    @property
    def quantity_mw(self) -> dict:
        return self.__quantity_mw

    @quantity_mw.setter
    def quantity_mw(self, value: dict):
        self._property_changed('quantity_mw')
        self.__quantity_mw = value        

    @property
    def sell70cents(self) -> dict:
        return self.__sell70cents

    @sell70cents.setter
    def sell70cents(self, value: dict):
        self._property_changed('sell70cents')
        self.__sell70cents = value        

    @property
    def sell110cents(self) -> dict:
        return self.__sell110cents

    @sell110cents.setter
    def sell110cents(self, value: dict):
        self._property_changed('sell110cents')
        self.__sell110cents = value        

    @property
    def pnode_id(self) -> dict:
        return self.__pnode_id

    @pnode_id.setter
    def pnode_id(self, value: dict):
        self._property_changed('pnode_id')
        self.__pnode_id = value        

    @property
    def humidity_type(self) -> dict:
        return self.__humidity_type

    @humidity_type.setter
    def humidity_type(self, value: dict):
        self._property_changed('humidity_type')
        self.__humidity_type = value        

    @property
    def prev_close_ask(self) -> dict:
        return self.__prev_close_ask

    @prev_close_ask.setter
    def prev_close_ask(self, value: dict):
        self._property_changed('prev_close_ask')
        self.__prev_close_ask = value        

    @property
    def level(self) -> dict:
        return self.__level

    @level.setter
    def level(self, value: dict):
        self._property_changed('level')
        self.__level = value        

    @property
    def implied_volatility_by_expiration(self) -> dict:
        return self.__implied_volatility_by_expiration

    @implied_volatility_by_expiration.setter
    def implied_volatility_by_expiration(self, value: dict):
        self._property_changed('implied_volatility_by_expiration')
        self.__implied_volatility_by_expiration = value        

    @property
    def asset_parameters_fixed_rate_day_count_fraction(self) -> dict:
        return self.__asset_parameters_fixed_rate_day_count_fraction

    @asset_parameters_fixed_rate_day_count_fraction.setter
    def asset_parameters_fixed_rate_day_count_fraction(self, value: dict):
        self._property_changed('asset_parameters_fixed_rate_day_count_fraction')
        self.__asset_parameters_fixed_rate_day_count_fraction = value        

    @property
    def es_momentum_score(self) -> dict:
        return self.__es_momentum_score

    @es_momentum_score.setter
    def es_momentum_score(self, value: dict):
        self._property_changed('es_momentum_score')
        self.__es_momentum_score = value        

    @property
    def leg2_index(self) -> dict:
        return self.__leg2_index

    @leg2_index.setter
    def leg2_index(self, value: dict):
        self._property_changed('leg2_index')
        self.__leg2_index = value        

    @property
    def net_weight(self) -> dict:
        return self.__net_weight

    @net_weight.setter
    def net_weight(self, value: dict):
        self._property_changed('net_weight')
        self.__net_weight = value        

    @property
    def portfolio_managers(self) -> dict:
        return self.__portfolio_managers

    @portfolio_managers.setter
    def portfolio_managers(self, value: dict):
        self._property_changed('portfolio_managers')
        self.__portfolio_managers = value        

    @property
    def bos_in_ticks(self) -> dict:
        return self.__bos_in_ticks

    @bos_in_ticks.setter
    def bos_in_ticks(self, value: dict):
        self._property_changed('bos_in_ticks')
        self.__bos_in_ticks = value        

    @property
    def asset_parameters_coupon_type(self) -> dict:
        return self.__asset_parameters_coupon_type

    @asset_parameters_coupon_type.setter
    def asset_parameters_coupon_type(self, value: dict):
        self._property_changed('asset_parameters_coupon_type')
        self.__asset_parameters_coupon_type = value        

    @property
    def expected_residual_quantity(self) -> dict:
        return self.__expected_residual_quantity

    @expected_residual_quantity.setter
    def expected_residual_quantity(self, value: dict):
        self._property_changed('expected_residual_quantity')
        self.__expected_residual_quantity = value        

    @property
    def roll_date(self) -> dict:
        return self.__roll_date

    @roll_date.setter
    def roll_date(self, value: dict):
        self._property_changed('roll_date')
        self.__roll_date = value        

    @property
    def dynamic_hybrid_speed(self) -> dict:
        return self.__dynamic_hybrid_speed

    @dynamic_hybrid_speed.setter
    def dynamic_hybrid_speed(self, value: dict):
        self._property_changed('dynamic_hybrid_speed')
        self.__dynamic_hybrid_speed = value        

    @property
    def cap_floor_vol(self) -> dict:
        return self.__cap_floor_vol

    @cap_floor_vol.setter
    def cap_floor_vol(self, value: dict):
        self._property_changed('cap_floor_vol')
        self.__cap_floor_vol = value        

    @property
    def target_quantity(self) -> dict:
        return self.__target_quantity

    @target_quantity.setter
    def target_quantity(self, value: dict):
        self._property_changed('target_quantity')
        self.__target_quantity = value        

    @property
    def submitter(self) -> dict:
        return self.__submitter

    @submitter.setter
    def submitter(self, value: dict):
        self._property_changed('submitter')
        self.__submitter = value        

    @property
    def no(self) -> dict:
        return self.__no

    @no.setter
    def no(self, value: dict):
        self._property_changed('no')
        self.__no = value        

    @property
    def notional(self) -> dict:
        return self.__notional

    @notional.setter
    def notional(self, value: dict):
        self._property_changed('notional')
        self.__notional = value        

    @property
    def es_disclosure_percentage(self) -> dict:
        return self.__es_disclosure_percentage

    @es_disclosure_percentage.setter
    def es_disclosure_percentage(self, value: dict):
        self._property_changed('es_disclosure_percentage')
        self.__es_disclosure_percentage = value        

    @property
    def close_executed_quantity_percentage(self) -> dict:
        return self.__close_executed_quantity_percentage

    @close_executed_quantity_percentage.setter
    def close_executed_quantity_percentage(self, value: dict):
        self._property_changed('close_executed_quantity_percentage')
        self.__close_executed_quantity_percentage = value        

    @property
    def twap_realized_cash(self) -> dict:
        return self.__twap_realized_cash

    @twap_realized_cash.setter
    def twap_realized_cash(self, value: dict):
        self._property_changed('twap_realized_cash')
        self.__twap_realized_cash = value        

    @property
    def is_open_auction(self) -> dict:
        return self.__is_open_auction

    @is_open_auction.setter
    def is_open_auction(self, value: dict):
        self._property_changed('is_open_auction')
        self.__is_open_auction = value        

    @property
    def leg1_type(self) -> dict:
        return self.__leg1_type

    @leg1_type.setter
    def leg1_type(self, value: dict):
        self._property_changed('leg1_type')
        self.__leg1_type = value        

    @property
    def wet_bulb_temp_hourly_forecast(self) -> dict:
        return self.__wet_bulb_temp_hourly_forecast

    @wet_bulb_temp_hourly_forecast.setter
    def wet_bulb_temp_hourly_forecast(self, value: dict):
        self._property_changed('wet_bulb_temp_hourly_forecast')
        self.__wet_bulb_temp_hourly_forecast = value        

    @property
    def cleanup_price(self) -> dict:
        return self.__cleanup_price

    @cleanup_price.setter
    def cleanup_price(self, value: dict):
        self._property_changed('cleanup_price')
        self.__cleanup_price = value        

    @property
    def total(self) -> dict:
        return self.__total

    @total.setter
    def total(self, value: dict):
        self._property_changed('total')
        self.__total = value        

    @property
    def filled_notional_usd(self) -> dict:
        return self.__filled_notional_usd

    @filled_notional_usd.setter
    def filled_notional_usd(self, value: dict):
        self._property_changed('filled_notional_usd')
        self.__filled_notional_usd = value        

    @property
    def asset_id(self) -> dict:
        return self.__asset_id

    @asset_id.setter
    def asset_id(self, value: dict):
        self._property_changed('asset_id')
        self.__asset_id = value        

    @property
    def test_status(self) -> dict:
        return self.__test_status

    @test_status.setter
    def test_status(self, value: dict):
        self._property_changed('test_status')
        self.__test_status = value        

    @property
    def mkt_type(self) -> dict:
        return self.__mkt_type

    @mkt_type.setter
    def mkt_type(self, value: dict):
        self._property_changed('mkt_type')
        self.__mkt_type = value        

    @property
    def yield30_day(self) -> dict:
        return self.__yield30_day

    @yield30_day.setter
    def yield30_day(self, value: dict):
        self._property_changed('yield30_day')
        self.__yield30_day = value        

    @property
    def buy28bps(self) -> dict:
        return self.__buy28bps

    @buy28bps.setter
    def buy28bps(self, value: dict):
        self._property_changed('buy28bps')
        self.__buy28bps = value        

    @property
    def proportion_of_risk(self) -> dict:
        return self.__proportion_of_risk

    @proportion_of_risk.setter
    def proportion_of_risk(self, value: dict):
        self._property_changed('proportion_of_risk')
        self.__proportion_of_risk = value        

    @property
    def future_month_k23(self) -> dict:
        return self.__future_month_k23

    @future_month_k23.setter
    def future_month_k23(self, value: dict):
        self._property_changed('future_month_k23')
        self.__future_month_k23 = value        

    @property
    def future_month_k22(self) -> dict:
        return self.__future_month_k22

    @future_month_k22.setter
    def future_month_k22(self, value: dict):
        self._property_changed('future_month_k22')
        self.__future_month_k22 = value        

    @property
    def future_month_k21(self) -> dict:
        return self.__future_month_k21

    @future_month_k21.setter
    def future_month_k21(self, value: dict):
        self._property_changed('future_month_k21')
        self.__future_month_k21 = value        

    @property
    def primary_entity_id(self) -> dict:
        return self.__primary_entity_id

    @primary_entity_id.setter
    def primary_entity_id(self, value: dict):
        self._property_changed('primary_entity_id')
        self.__primary_entity_id = value        

    @property
    def cross(self) -> dict:
        return self.__cross

    @cross.setter
    def cross(self, value: dict):
        self._property_changed('cross')
        self.__cross = value        

    @property
    def idea_status(self) -> dict:
        return self.__idea_status

    @idea_status.setter
    def idea_status(self, value: dict):
        self._property_changed('idea_status')
        self.__idea_status = value        

    @property
    def contract_subtype(self) -> dict:
        return self.__contract_subtype

    @contract_subtype.setter
    def contract_subtype(self, value: dict):
        self._property_changed('contract_subtype')
        self.__contract_subtype = value        

    @property
    def sri(self) -> dict:
        return self.__sri

    @sri.setter
    def sri(self, value: dict):
        self._property_changed('sri')
        self.__sri = value        

    @property
    def fx_forecast(self) -> dict:
        return self.__fx_forecast

    @fx_forecast.setter
    def fx_forecast(self, value: dict):
        self._property_changed('fx_forecast')
        self.__fx_forecast = value        

    @property
    def fixing_time_label(self) -> dict:
        return self.__fixing_time_label

    @fixing_time_label.setter
    def fixing_time_label(self, value: dict):
        self._property_changed('fixing_time_label')
        self.__fixing_time_label = value        

    @property
    def is_etf(self) -> dict:
        return self.__is_etf

    @is_etf.setter
    def is_etf(self, value: dict):
        self._property_changed('is_etf')
        self.__is_etf = value        

    @property
    def fill_id(self) -> dict:
        return self.__fill_id

    @fill_id.setter
    def fill_id(self, value: dict):
        self._property_changed('fill_id')
        self.__fill_id = value        

    @property
    def excess_returns(self) -> dict:
        return self.__excess_returns

    @excess_returns.setter
    def excess_returns(self, value: dict):
        self._property_changed('excess_returns')
        self.__excess_returns = value        

    @property
    def dollar_return(self) -> dict:
        return self.__dollar_return

    @dollar_return.setter
    def dollar_return(self, value: dict):
        self._property_changed('dollar_return')
        self.__dollar_return = value        

    @property
    def order_in_limit(self) -> dict:
        return self.__order_in_limit

    @order_in_limit.setter
    def order_in_limit(self, value: dict):
        self._property_changed('order_in_limit')
        self.__order_in_limit = value        

    @property
    def expiry_time(self) -> dict:
        return self.__expiry_time

    @expiry_time.setter
    def expiry_time(self, value: dict):
        self._property_changed('expiry_time')
        self.__expiry_time = value        

    @property
    def return_on_equity(self) -> dict:
        return self.__return_on_equity

    @return_on_equity.setter
    def return_on_equity(self, value: dict):
        self._property_changed('return_on_equity')
        self.__return_on_equity = value        

    @property
    def future_month_k26(self) -> dict:
        return self.__future_month_k26

    @future_month_k26.setter
    def future_month_k26(self, value: dict):
        self._property_changed('future_month_k26')
        self.__future_month_k26 = value        

    @property
    def future_month_k25(self) -> dict:
        return self.__future_month_k25

    @future_month_k25.setter
    def future_month_k25(self, value: dict):
        self._property_changed('future_month_k25')
        self.__future_month_k25 = value        

    @property
    def future_month_k24(self) -> dict:
        return self.__future_month_k24

    @future_month_k24.setter
    def future_month_k24(self, value: dict):
        self._property_changed('future_month_k24')
        self.__future_month_k24 = value        

    @property
    def restriction_end_date(self) -> dict:
        return self.__restriction_end_date

    @restriction_end_date.setter
    def restriction_end_date(self, value: dict):
        self._property_changed('restriction_end_date')
        self.__restriction_end_date = value        

    @property
    def queue_in_lots_description(self) -> dict:
        return self.__queue_in_lots_description

    @queue_in_lots_description.setter
    def queue_in_lots_description(self, value: dict):
        self._property_changed('queue_in_lots_description')
        self.__queue_in_lots_description = value        

    @property
    def volume_limit(self) -> dict:
        return self.__volume_limit

    @volume_limit.setter
    def volume_limit(self, value: dict):
        self._property_changed('volume_limit')
        self.__volume_limit = value        

    @property
    def objective(self) -> dict:
        return self.__objective

    @objective.setter
    def objective(self, value: dict):
        self._property_changed('objective')
        self.__objective = value        

    @property
    def nav_price(self) -> dict:
        return self.__nav_price

    @nav_price.setter
    def nav_price(self, value: dict):
        self._property_changed('nav_price')
        self.__nav_price = value        

    @property
    def leg1_underlying_asset(self) -> dict:
        return self.__leg1_underlying_asset

    @leg1_underlying_asset.setter
    def leg1_underlying_asset(self, value: dict):
        self._property_changed('leg1_underlying_asset')
        self.__leg1_underlying_asset = value        

    @property
    def private_placement_type(self) -> dict:
        return self.__private_placement_type

    @private_placement_type.setter
    def private_placement_type(self, value: dict):
        self._property_changed('private_placement_type')
        self.__private_placement_type = value        

    @property
    def hedge_notional(self) -> dict:
        return self.__hedge_notional

    @hedge_notional.setter
    def hedge_notional(self, value: dict):
        self._property_changed('hedge_notional')
        self.__hedge_notional = value        

    @property
    def ask_low(self) -> dict:
        return self.__ask_low

    @ask_low.setter
    def ask_low(self, value: dict):
        self._property_changed('ask_low')
        self.__ask_low = value        

    @property
    def intended_p_rate(self) -> dict:
        return self.__intended_p_rate

    @intended_p_rate.setter
    def intended_p_rate(self, value: dict):
        self._property_changed('intended_p_rate')
        self.__intended_p_rate = value        

    @property
    def expiry(self) -> dict:
        return self.__expiry

    @expiry.setter
    def expiry(self, value: dict):
        self._property_changed('expiry')
        self.__expiry = value        

    @property
    def avg_monthly_yield(self) -> dict:
        return self.__avg_monthly_yield

    @avg_monthly_yield.setter
    def avg_monthly_yield(self, value: dict):
        self._property_changed('avg_monthly_yield')
        self.__avg_monthly_yield = value        

    @property
    def period_direction(self) -> dict:
        return self.__period_direction

    @period_direction.setter
    def period_direction(self, value: dict):
        self._property_changed('period_direction')
        self.__period_direction = value        

    @property
    def prev_rpt_id(self) -> dict:
        return self.__prev_rpt_id

    @prev_rpt_id.setter
    def prev_rpt_id(self, value: dict):
        self._property_changed('prev_rpt_id')
        self.__prev_rpt_id = value        

    @property
    def earnings_per_share(self) -> dict:
        return self.__earnings_per_share

    @earnings_per_share.setter
    def earnings_per_share(self, value: dict):
        self._property_changed('earnings_per_share')
        self.__earnings_per_share = value        

    @property
    def strike_percentage(self) -> dict:
        return self.__strike_percentage

    @strike_percentage.setter
    def strike_percentage(self, value: dict):
        self._property_changed('strike_percentage')
        self.__strike_percentage = value        

    @property
    def es_product_impact_percentile(self) -> dict:
        return self.__es_product_impact_percentile

    @es_product_impact_percentile.setter
    def es_product_impact_percentile(self, value: dict):
        self._property_changed('es_product_impact_percentile')
        self.__es_product_impact_percentile = value        

    @property
    def vwap_realized_cash(self) -> dict:
        return self.__vwap_realized_cash

    @vwap_realized_cash.setter
    def vwap_realized_cash(self, value: dict):
        self._property_changed('vwap_realized_cash')
        self.__vwap_realized_cash = value        

    @property
    def par_asset_swap_spread1m(self) -> dict:
        return self.__par_asset_swap_spread1m

    @par_asset_swap_spread1m.setter
    def par_asset_swap_spread1m(self, value: dict):
        self._property_changed('par_asset_swap_spread1m')
        self.__par_asset_swap_spread1m = value        

    @property
    def prev_close_bid(self) -> dict:
        return self.__prev_close_bid

    @prev_close_bid.setter
    def prev_close_bid(self, value: dict):
        self._property_changed('prev_close_bid')
        self.__prev_close_bid = value        

    @property
    def minimum_increment(self) -> dict:
        return self.__minimum_increment

    @minimum_increment.setter
    def minimum_increment(self, value: dict):
        self._property_changed('minimum_increment')
        self.__minimum_increment = value        

    @property
    def tcm_cost_horizon16_day(self) -> dict:
        return self.__tcm_cost_horizon16_day

    @tcm_cost_horizon16_day.setter
    def tcm_cost_horizon16_day(self, value: dict):
        self._property_changed('tcm_cost_horizon16_day')
        self.__tcm_cost_horizon16_day = value        

    @property
    def investment_mtd(self) -> dict:
        return self.__investment_mtd

    @investment_mtd.setter
    def investment_mtd(self, value: dict):
        self._property_changed('investment_mtd')
        self.__investment_mtd = value        

    @property
    def settlement_date(self) -> dict:
        return self.__settlement_date

    @settlement_date.setter
    def settlement_date(self, value: dict):
        self._property_changed('settlement_date')
        self.__settlement_date = value        

    @property
    def weighted_average_mid_normalized(self) -> dict:
        return self.__weighted_average_mid_normalized

    @weighted_average_mid_normalized.setter
    def weighted_average_mid_normalized(self, value: dict):
        self._property_changed('weighted_average_mid_normalized')
        self.__weighted_average_mid_normalized = value        

    @property
    def sales_per_share(self) -> dict:
        return self.__sales_per_share

    @sales_per_share.setter
    def sales_per_share(self, value: dict):
        self._property_changed('sales_per_share')
        self.__sales_per_share = value        

    @property
    def unadjusted_close(self) -> dict:
        return self.__unadjusted_close

    @unadjusted_close.setter
    def unadjusted_close(self, value: dict):
        self._property_changed('unadjusted_close')
        self.__unadjusted_close = value        

    @property
    def loan_date(self) -> dict:
        return self.__loan_date

    @loan_date.setter
    def loan_date(self, value: dict):
        self._property_changed('loan_date')
        self.__loan_date = value        

    @property
    def matched_maturity_swap_spread1m(self) -> dict:
        return self.__matched_maturity_swap_spread1m

    @matched_maturity_swap_spread1m.setter
    def matched_maturity_swap_spread1m(self, value: dict):
        self._property_changed('matched_maturity_swap_spread1m')
        self.__matched_maturity_swap_spread1m = value        

    @property
    def collateral_percentage_actual(self) -> dict:
        return self.__collateral_percentage_actual

    @collateral_percentage_actual.setter
    def collateral_percentage_actual(self, value: dict):
        self._property_changed('collateral_percentage_actual')
        self.__collateral_percentage_actual = value        

    @property
    def vwap_in_limit_unrealized_bps(self) -> dict:
        return self.__vwap_in_limit_unrealized_bps

    @vwap_in_limit_unrealized_bps.setter
    def vwap_in_limit_unrealized_bps(self, value: dict):
        self._property_changed('vwap_in_limit_unrealized_bps')
        self.__vwap_in_limit_unrealized_bps = value        

    @property
    def metric_value(self) -> dict:
        return self.__metric_value

    @metric_value.setter
    def metric_value(self, value: dict):
        self._property_changed('metric_value')
        self.__metric_value = value        

    @property
    def auto_exec_state(self) -> dict:
        return self.__auto_exec_state

    @auto_exec_state.setter
    def auto_exec_state(self, value: dict):
        self._property_changed('auto_exec_state')
        self.__auto_exec_state = value        

    @property
    def total_recovered(self) -> dict:
        return self.__total_recovered

    @total_recovered.setter
    def total_recovered(self, value: dict):
        self._property_changed('total_recovered')
        self.__total_recovered = value        

    @property
    def relative_return_ytd(self) -> dict:
        return self.__relative_return_ytd

    @relative_return_ytd.setter
    def relative_return_ytd(self, value: dict):
        self._property_changed('relative_return_ytd')
        self.__relative_return_ytd = value        

    @property
    def tick_server(self) -> dict:
        return self.__tick_server

    @tick_server.setter
    def tick_server(self, value: dict):
        self._property_changed('tick_server')
        self.__tick_server = value        

    @property
    def cumulative_volume_in_percentage(self) -> dict:
        return self.__cumulative_volume_in_percentage

    @cumulative_volume_in_percentage.setter
    def cumulative_volume_in_percentage(self, value: dict):
        self._property_changed('cumulative_volume_in_percentage')
        self.__cumulative_volume_in_percentage = value        

    @property
    def real_time_restriction_status(self) -> dict:
        return self.__real_time_restriction_status

    @real_time_restriction_status.setter
    def real_time_restriction_status(self, value: dict):
        self._property_changed('real_time_restriction_status')
        self.__real_time_restriction_status = value        

    @property
    def trade_type(self) -> dict:
        return self.__trade_type

    @trade_type.setter
    def trade_type(self, value: dict):
        self._property_changed('trade_type')
        self.__trade_type = value        

    @property
    def settlement_type(self) -> dict:
        return self.__settlement_type

    @settlement_type.setter
    def settlement_type(self, value: dict):
        self._property_changed('settlement_type')
        self.__settlement_type = value        

    @property
    def net_change(self) -> dict:
        return self.__net_change

    @net_change.setter
    def net_change(self, value: dict):
        self._property_changed('net_change')
        self.__net_change = value        

    @property
    def number_of_underliers(self) -> dict:
        return self.__number_of_underliers

    @number_of_underliers.setter
    def number_of_underliers(self, value: dict):
        self._property_changed('number_of_underliers')
        self.__number_of_underliers = value        

    @property
    def swap_type(self) -> dict:
        return self.__swap_type

    @swap_type.setter
    def swap_type(self, value: dict):
        self._property_changed('swap_type')
        self.__swap_type = value        

    @property
    def forecast_type(self) -> dict:
        return self.__forecast_type

    @forecast_type.setter
    def forecast_type(self, value: dict):
        self._property_changed('forecast_type')
        self.__forecast_type = value        

    @property
    def leg1_notional(self) -> dict:
        return self.__leg1_notional

    @leg1_notional.setter
    def leg1_notional(self, value: dict):
        self._property_changed('leg1_notional')
        self.__leg1_notional = value        

    @property
    def sell_settle_date(self) -> dict:
        return self.__sell_settle_date

    @sell_settle_date.setter
    def sell_settle_date(self, value: dict):
        self._property_changed('sell_settle_date')
        self.__sell_settle_date = value        

    @property
    def new_ideas_ytd(self) -> dict:
        return self.__new_ideas_ytd

    @new_ideas_ytd.setter
    def new_ideas_ytd(self, value: dict):
        self._property_changed('new_ideas_ytd')
        self.__new_ideas_ytd = value        

    @property
    def management_fee(self) -> dict:
        return self.__management_fee

    @management_fee.setter
    def management_fee(self, value: dict):
        self._property_changed('management_fee')
        self.__management_fee = value        

    @property
    def par_asset_swap_spread3m(self) -> dict:
        return self.__par_asset_swap_spread3m

    @par_asset_swap_spread3m.setter
    def par_asset_swap_spread3m(self, value: dict):
        self._property_changed('par_asset_swap_spread3m')
        self.__par_asset_swap_spread3m = value        

    @property
    def sell36bps(self) -> dict:
        return self.__sell36bps

    @sell36bps.setter
    def sell36bps(self, value: dict):
        self._property_changed('sell36bps')
        self.__sell36bps = value        

    @property
    def matched_maturity_swap_spread3m(self) -> dict:
        return self.__matched_maturity_swap_spread3m

    @matched_maturity_swap_spread3m.setter
    def matched_maturity_swap_spread3m(self, value: dict):
        self._property_changed('matched_maturity_swap_spread3m')
        self.__matched_maturity_swap_spread3m = value        

    @property
    def source_id(self) -> dict:
        return self.__source_id

    @source_id.setter
    def source_id(self, value: dict):
        self._property_changed('source_id')
        self.__source_id = value        

    @property
    def country(self) -> dict:
        return self.__country

    @country.setter
    def country(self, value: dict):
        self._property_changed('country')
        self.__country = value        

    @property
    def vwap(self) -> dict:
        return self.__vwap

    @vwap.setter
    def vwap(self, value: dict):
        self._property_changed('vwap')
        self.__vwap = value        

    @property
    def touch_spread_score(self) -> dict:
        return self.__touch_spread_score

    @touch_spread_score.setter
    def touch_spread_score(self, value: dict):
        self._property_changed('touch_spread_score')
        self.__touch_spread_score = value        

    @property
    def rating_second_highest(self) -> dict:
        return self.__rating_second_highest

    @rating_second_highest.setter
    def rating_second_highest(self, value: dict):
        self._property_changed('rating_second_highest')
        self.__rating_second_highest = value        

    @property
    def sell24bps(self) -> dict:
        return self.__sell24bps

    @sell24bps.setter
    def sell24bps(self, value: dict):
        self._property_changed('sell24bps')
        self.__sell24bps = value        

    @property
    def frequency(self) -> dict:
        return self.__frequency

    @frequency.setter
    def frequency(self, value: dict):
        self._property_changed('frequency')
        self.__frequency = value        

    @property
    def activity_id(self) -> dict:
        return self.__activity_id

    @activity_id.setter
    def activity_id(self, value: dict):
        self._property_changed('activity_id')
        self.__activity_id = value        

    @property
    def estimated_impact(self) -> dict:
        return self.__estimated_impact

    @estimated_impact.setter
    def estimated_impact(self, value: dict):
        self._property_changed('estimated_impact')
        self.__estimated_impact = value        

    @property
    def sell35cents(self) -> dict:
        return self.__sell35cents

    @sell35cents.setter
    def sell35cents(self, value: dict):
        self._property_changed('sell35cents')
        self.__sell35cents = value        

    @property
    def loan_spread_bucket(self) -> dict:
        return self.__loan_spread_bucket

    @loan_spread_bucket.setter
    def loan_spread_bucket(self, value: dict):
        self._property_changed('loan_spread_bucket')
        self.__loan_spread_bucket = value        

    @property
    def coronavirus_global_activity_tracker(self) -> dict:
        return self.__coronavirus_global_activity_tracker

    @coronavirus_global_activity_tracker.setter
    def coronavirus_global_activity_tracker(self, value: dict):
        self._property_changed('coronavirus_global_activity_tracker')
        self.__coronavirus_global_activity_tracker = value        

    @property
    def underlyers(self) -> dict:
        return self.__underlyers

    @underlyers.setter
    def underlyers(self, value: dict):
        self._property_changed('underlyers')
        self.__underlyers = value        

    @property
    def asset_parameters_pricing_location(self) -> dict:
        return self.__asset_parameters_pricing_location

    @asset_parameters_pricing_location.setter
    def asset_parameters_pricing_location(self, value: dict):
        self._property_changed('asset_parameters_pricing_location')
        self.__asset_parameters_pricing_location = value        

    @property
    def event_description(self) -> dict:
        return self.__event_description

    @event_description.setter
    def event_description(self, value: dict):
        self._property_changed('event_description')
        self.__event_description = value        

    @property
    def iceberg_max_size(self) -> dict:
        return self.__iceberg_max_size

    @iceberg_max_size.setter
    def iceberg_max_size(self, value: dict):
        self._property_changed('iceberg_max_size')
        self.__iceberg_max_size = value        

    @property
    def asset_parameters_coupon(self) -> dict:
        return self.__asset_parameters_coupon

    @asset_parameters_coupon.setter
    def asset_parameters_coupon(self, value: dict):
        self._property_changed('asset_parameters_coupon')
        self.__asset_parameters_coupon = value        

    @property
    def details(self) -> dict:
        return self.__details

    @details.setter
    def details(self, value: dict):
        self._property_changed('details')
        self.__details = value        

    @property
    def sector(self) -> dict:
        return self.__sector

    @sector.setter
    def sector(self, value: dict):
        self._property_changed('sector')
        self.__sector = value        

    @property
    def avg_bed_util_rate(self) -> dict:
        return self.__avg_bed_util_rate

    @avg_bed_util_rate.setter
    def avg_bed_util_rate(self, value: dict):
        self._property_changed('avg_bed_util_rate')
        self.__avg_bed_util_rate = value        

    @property
    def buy20bps(self) -> dict:
        return self.__buy20bps

    @buy20bps.setter
    def buy20bps(self, value: dict):
        self._property_changed('buy20bps')
        self.__buy20bps = value        

    @property
    def epidemic(self) -> dict:
        return self.__epidemic

    @epidemic.setter
    def epidemic(self, value: dict):
        self._property_changed('epidemic')
        self.__epidemic = value        

    @property
    def mctr(self) -> dict:
        return self.__mctr

    @mctr.setter
    def mctr(self, value: dict):
        self._property_changed('mctr')
        self.__mctr = value        

    @property
    def exchange_time(self) -> dict:
        return self.__exchange_time

    @exchange_time.setter
    def exchange_time(self, value: dict):
        self._property_changed('exchange_time')
        self.__exchange_time = value        

    @property
    def historical_close(self) -> dict:
        return self.__historical_close

    @historical_close.setter
    def historical_close(self, value: dict):
        self._property_changed('historical_close')
        self.__historical_close = value        

    @property
    def fips_code(self) -> dict:
        return self.__fips_code

    @fips_code.setter
    def fips_code(self, value: dict):
        self._property_changed('fips_code')
        self.__fips_code = value        

    @property
    def buy32bps(self) -> dict:
        return self.__buy32bps

    @buy32bps.setter
    def buy32bps(self, value: dict):
        self._property_changed('buy32bps')
        self.__buy32bps = value        

    @property
    def idea_id(self) -> dict:
        return self.__idea_id

    @idea_id.setter
    def idea_id(self, value: dict):
        self._property_changed('idea_id')
        self.__idea_id = value        

    @property
    def comment_status(self) -> dict:
        return self.__comment_status

    @comment_status.setter
    def comment_status(self, value: dict):
        self._property_changed('comment_status')
        self.__comment_status = value        

    @property
    def marginal_cost(self) -> dict:
        return self.__marginal_cost

    @marginal_cost.setter
    def marginal_cost(self, value: dict):
        self._property_changed('marginal_cost')
        self.__marginal_cost = value        

    @property
    def client_weight(self) -> dict:
        return self.__client_weight

    @client_weight.setter
    def client_weight(self, value: dict):
        self._property_changed('client_weight')
        self.__client_weight = value        

    @property
    def leg1_delivery_point(self) -> dict:
        return self.__leg1_delivery_point

    @leg1_delivery_point.setter
    def leg1_delivery_point(self, value: dict):
        self._property_changed('leg1_delivery_point')
        self.__leg1_delivery_point = value        

    @property
    def sell5cents(self) -> dict:
        return self.__sell5cents

    @sell5cents.setter
    def sell5cents(self, value: dict):
        self._property_changed('sell5cents')
        self.__sell5cents = value        

    @property
    def liq_wkly(self) -> dict:
        return self.__liq_wkly

    @liq_wkly.setter
    def liq_wkly(self, value: dict):
        self._property_changed('liq_wkly')
        self.__liq_wkly = value        

    @property
    def unrealized_twap_performance_bps(self) -> dict:
        return self.__unrealized_twap_performance_bps

    @unrealized_twap_performance_bps.setter
    def unrealized_twap_performance_bps(self, value: dict):
        self._property_changed('unrealized_twap_performance_bps')
        self.__unrealized_twap_performance_bps = value        

    @property
    def region(self) -> dict:
        return self.__region

    @region.setter
    def region(self, value: dict):
        self._property_changed('region')
        self.__region = value        

    @property
    def temperature_hour(self) -> dict:
        return self.__temperature_hour

    @temperature_hour.setter
    def temperature_hour(self, value: dict):
        self._property_changed('temperature_hour')
        self.__temperature_hour = value        

    @property
    def upper_bound(self) -> dict:
        return self.__upper_bound

    @upper_bound.setter
    def upper_bound(self, value: dict):
        self._property_changed('upper_bound')
        self.__upper_bound = value        

    @property
    def sell55cents(self) -> dict:
        return self.__sell55cents

    @sell55cents.setter
    def sell55cents(self, value: dict):
        self._property_changed('sell55cents')
        self.__sell55cents = value        

    @property
    def num_pedi_icu_beds(self) -> dict:
        return self.__num_pedi_icu_beds

    @num_pedi_icu_beds.setter
    def num_pedi_icu_beds(self, value: dict):
        self._property_changed('num_pedi_icu_beds')
        self.__num_pedi_icu_beds = value        

    @property
    def bid_yield(self) -> dict:
        return self.__bid_yield

    @bid_yield.setter
    def bid_yield(self, value: dict):
        self._property_changed('bid_yield')
        self.__bid_yield = value        

    @property
    def expected_residual(self) -> dict:
        return self.__expected_residual

    @expected_residual.setter
    def expected_residual(self, value: dict):
        self._property_changed('expected_residual')
        self.__expected_residual = value        

    @property
    def option_premium(self) -> dict:
        return self.__option_premium

    @option_premium.setter
    def option_premium(self, value: dict):
        self._property_changed('option_premium')
        self.__option_premium = value        

    @property
    def owner_name(self) -> dict:
        return self.__owner_name

    @owner_name.setter
    def owner_name(self, value: dict):
        self._property_changed('owner_name')
        self.__owner_name = value        

    @property
    def par_asset_swap_spread6m(self) -> dict:
        return self.__par_asset_swap_spread6m

    @par_asset_swap_spread6m.setter
    def par_asset_swap_spread6m(self, value: dict):
        self._property_changed('par_asset_swap_spread6m')
        self.__par_asset_swap_spread6m = value        

    @property
    def z_score(self) -> dict:
        return self.__z_score

    @z_score.setter
    def z_score(self, value: dict):
        self._property_changed('z_score')
        self.__z_score = value        

    @property
    def sell12bps(self) -> dict:
        return self.__sell12bps

    @sell12bps.setter
    def sell12bps(self, value: dict):
        self._property_changed('sell12bps')
        self.__sell12bps = value        

    @property
    def event_start_time(self) -> dict:
        return self.__event_start_time

    @event_start_time.setter
    def event_start_time(self, value: dict):
        self._property_changed('event_start_time')
        self.__event_start_time = value        

    @property
    def matched_maturity_swap_spread6m(self) -> dict:
        return self.__matched_maturity_swap_spread6m

    @matched_maturity_swap_spread6m.setter
    def matched_maturity_swap_spread6m(self, value: dict):
        self._property_changed('matched_maturity_swap_spread6m')
        self.__matched_maturity_swap_spread6m = value        

    @property
    def turnover(self) -> dict:
        return self.__turnover

    @turnover.setter
    def turnover(self, value: dict):
        self._property_changed('turnover')
        self.__turnover = value        

    @property
    def price_spot_target_unit(self) -> dict:
        return self.__price_spot_target_unit

    @price_spot_target_unit.setter
    def price_spot_target_unit(self, value: dict):
        self._property_changed('price_spot_target_unit')
        self.__price_spot_target_unit = value        

    @property
    def coverage(self) -> dict:
        return self.__coverage

    @coverage.setter
    def coverage(self, value: dict):
        self._property_changed('coverage')
        self.__coverage = value        

    @property
    def g_percentile(self) -> dict:
        return self.__g_percentile

    @g_percentile.setter
    def g_percentile(self, value: dict):
        self._property_changed('g_percentile')
        self.__g_percentile = value        

    @property
    def cloud_cover_hourly_forecast(self) -> dict:
        return self.__cloud_cover_hourly_forecast

    @cloud_cover_hourly_forecast.setter
    def cloud_cover_hourly_forecast(self, value: dict):
        self._property_changed('cloud_cover_hourly_forecast')
        self.__cloud_cover_hourly_forecast = value        

    @property
    def lending_fund_nav(self) -> dict:
        return self.__lending_fund_nav

    @lending_fund_nav.setter
    def lending_fund_nav(self, value: dict):
        self._property_changed('lending_fund_nav')
        self.__lending_fund_nav = value        

    @property
    def source_original_category(self) -> dict:
        return self.__source_original_category

    @source_original_category.setter
    def source_original_category(self, value: dict):
        self._property_changed('source_original_category')
        self.__source_original_category = value        

    @property
    def percent_close_execution_quantity(self) -> dict:
        return self.__percent_close_execution_quantity

    @percent_close_execution_quantity.setter
    def percent_close_execution_quantity(self, value: dict):
        self._property_changed('percent_close_execution_quantity')
        self.__percent_close_execution_quantity = value        

    @property
    def latest_execution_time(self) -> dict:
        return self.__latest_execution_time

    @latest_execution_time.setter
    def latest_execution_time(self, value: dict):
        self._property_changed('latest_execution_time')
        self.__latest_execution_time = value        

    @property
    def arrival_mid_realized_bps(self) -> dict:
        return self.__arrival_mid_realized_bps

    @arrival_mid_realized_bps.setter
    def arrival_mid_realized_bps(self, value: dict):
        self._property_changed('arrival_mid_realized_bps')
        self.__arrival_mid_realized_bps = value        

    @property
    def location(self) -> dict:
        return self.__location

    @location.setter
    def location(self, value: dict):
        self._property_changed('location')
        self.__location = value        

    @property
    def scenario_id(self) -> dict:
        return self.__scenario_id

    @scenario_id.setter
    def scenario_id(self, value: dict):
        self._property_changed('scenario_id')
        self.__scenario_id = value        

    @property
    def termination_tenor(self) -> dict:
        return self.__termination_tenor

    @termination_tenor.setter
    def termination_tenor(self, value: dict):
        self._property_changed('termination_tenor')
        self.__termination_tenor = value        

    @property
    def queue_clock_time(self) -> dict:
        return self.__queue_clock_time

    @queue_clock_time.setter
    def queue_clock_time(self, value: dict):
        self._property_changed('queue_clock_time')
        self.__queue_clock_time = value        

    @property
    def discretion_lower_bound(self) -> dict:
        return self.__discretion_lower_bound

    @discretion_lower_bound.setter
    def discretion_lower_bound(self, value: dict):
        self._property_changed('discretion_lower_bound')
        self.__discretion_lower_bound = value        

    @property
    def tcm_cost_participation_rate50_pct(self) -> dict:
        return self.__tcm_cost_participation_rate50_pct

    @tcm_cost_participation_rate50_pct.setter
    def tcm_cost_participation_rate50_pct(self, value: dict):
        self._property_changed('tcm_cost_participation_rate50_pct')
        self.__tcm_cost_participation_rate50_pct = value        

    @property
    def rating_linear(self) -> dict:
        return self.__rating_linear

    @rating_linear.setter
    def rating_linear(self, value: dict):
        self._property_changed('rating_linear')
        self.__rating_linear = value        

    @property
    def previous_close_unrealized_bps(self) -> dict:
        return self.__previous_close_unrealized_bps

    @previous_close_unrealized_bps.setter
    def previous_close_unrealized_bps(self, value: dict):
        self._property_changed('previous_close_unrealized_bps')
        self.__previous_close_unrealized_bps = value        

    @property
    def sub_asset_class_for_other_commodity(self) -> dict:
        return self.__sub_asset_class_for_other_commodity

    @sub_asset_class_for_other_commodity.setter
    def sub_asset_class_for_other_commodity(self, value: dict):
        self._property_changed('sub_asset_class_for_other_commodity')
        self.__sub_asset_class_for_other_commodity = value        

    @property
    def forward_price(self) -> dict:
        return self.__forward_price

    @forward_price.setter
    def forward_price(self, value: dict):
        self._property_changed('forward_price')
        self.__forward_price = value        

    @property
    def type(self) -> dict:
        return self.__type

    @type.setter
    def type(self, value: dict):
        self._property_changed('type')
        self.__type = value        

    @property
    def strike_ref(self) -> dict:
        return self.__strike_ref

    @strike_ref.setter
    def strike_ref(self, value: dict):
        self._property_changed('strike_ref')
        self.__strike_ref = value        

    @property
    def cumulative_pnl(self) -> dict:
        return self.__cumulative_pnl

    @cumulative_pnl.setter
    def cumulative_pnl(self, value: dict):
        self._property_changed('cumulative_pnl')
        self.__cumulative_pnl = value        

    @property
    def short_tenor(self) -> dict:
        return self.__short_tenor

    @short_tenor.setter
    def short_tenor(self, value: dict):
        self._property_changed('short_tenor')
        self.__short_tenor = value        

    @property
    def sell28bps(self) -> dict:
        return self.__sell28bps

    @sell28bps.setter
    def sell28bps(self, value: dict):
        self._property_changed('sell28bps')
        self.__sell28bps = value        

    @property
    def fund_class(self) -> dict:
        return self.__fund_class

    @fund_class.setter
    def fund_class(self, value: dict):
        self._property_changed('fund_class')
        self.__fund_class = value        

    @property
    def unadjusted_volume(self) -> dict:
        return self.__unadjusted_volume

    @unadjusted_volume.setter
    def unadjusted_volume(self, value: dict):
        self._property_changed('unadjusted_volume')
        self.__unadjusted_volume = value        

    @property
    def buy36bps(self) -> dict:
        return self.__buy36bps

    @buy36bps.setter
    def buy36bps(self, value: dict):
        self._property_changed('buy36bps')
        self.__buy36bps = value        

    @property
    def position_idx(self) -> dict:
        return self.__position_idx

    @position_idx.setter
    def position_idx(self, value: dict):
        self._property_changed('position_idx')
        self.__position_idx = value        

    @property
    def wind_chill_hourly_forecast(self) -> dict:
        return self.__wind_chill_hourly_forecast

    @wind_chill_hourly_forecast.setter
    def wind_chill_hourly_forecast(self, value: dict):
        self._property_changed('wind_chill_hourly_forecast')
        self.__wind_chill_hourly_forecast = value        

    @property
    def sec_name(self) -> dict:
        return self.__sec_name

    @sec_name.setter
    def sec_name(self, value: dict):
        self._property_changed('sec_name')
        self.__sec_name = value        

    @property
    def implied_volatility_by_relative_strike(self) -> dict:
        return self.__implied_volatility_by_relative_strike

    @implied_volatility_by_relative_strike.setter
    def implied_volatility_by_relative_strike(self, value: dict):
        self._property_changed('implied_volatility_by_relative_strike')
        self.__implied_volatility_by_relative_strike = value        

    @property
    def percent_adv(self) -> dict:
        return self.__percent_adv

    @percent_adv.setter
    def percent_adv(self, value: dict):
        self._property_changed('percent_adv')
        self.__percent_adv = value        

    @property
    def leg1_total_notional(self) -> dict:
        return self.__leg1_total_notional

    @leg1_total_notional.setter
    def leg1_total_notional(self, value: dict):
        self._property_changed('leg1_total_notional')
        self.__leg1_total_notional = value        

    @property
    def contract(self) -> dict:
        return self.__contract

    @contract.setter
    def contract(self, value: dict):
        self._property_changed('contract')
        self.__contract = value        

    @property
    def payment_frequency1(self) -> dict:
        return self.__payment_frequency1

    @payment_frequency1.setter
    def payment_frequency1(self, value: dict):
        self._property_changed('payment_frequency1')
        self.__payment_frequency1 = value        

    @property
    def payment_frequency2(self) -> dict:
        return self.__payment_frequency2

    @payment_frequency2.setter
    def payment_frequency2(self, value: dict):
        self._property_changed('payment_frequency2')
        self.__payment_frequency2 = value        

    @property
    def bespoke(self) -> dict:
        return self.__bespoke

    @bespoke.setter
    def bespoke(self, value: dict):
        self._property_changed('bespoke')
        self.__bespoke = value        

    @property
    def repo_tenor(self) -> dict:
        return self.__repo_tenor

    @repo_tenor.setter
    def repo_tenor(self, value: dict):
        self._property_changed('repo_tenor')
        self.__repo_tenor = value        

    @property
    def sell15cents(self) -> dict:
        return self.__sell15cents

    @sell15cents.setter
    def sell15cents(self, value: dict):
        self._property_changed('sell15cents')
        self.__sell15cents = value        

    @property
    def investment_qtd(self) -> dict:
        return self.__investment_qtd

    @investment_qtd.setter
    def investment_qtd(self, value: dict):
        self._property_changed('investment_qtd')
        self.__investment_qtd = value        

    @property
    def heat_index_forecast(self) -> dict:
        return self.__heat_index_forecast

    @heat_index_forecast.setter
    def heat_index_forecast(self, value: dict):
        self._property_changed('heat_index_forecast')
        self.__heat_index_forecast = value        

    @property
    def rating_standard_and_poors(self) -> dict:
        return self.__rating_standard_and_poors

    @rating_standard_and_poors.setter
    def rating_standard_and_poors(self, value: dict):
        self._property_changed('rating_standard_and_poors')
        self.__rating_standard_and_poors = value        

    @property
    def quality_stars(self) -> dict:
        return self.__quality_stars

    @quality_stars.setter
    def quality_stars(self, value: dict):
        self._property_changed('quality_stars')
        self.__quality_stars = value        

    @property
    def leg2_floating_index(self) -> dict:
        return self.__leg2_floating_index

    @leg2_floating_index.setter
    def leg2_floating_index(self, value: dict):
        self._property_changed('leg2_floating_index')
        self.__leg2_floating_index = value        

    @property
    def source_ticker(self) -> dict:
        return self.__source_ticker

    @source_ticker.setter
    def source_ticker(self, value: dict):
        self._property_changed('source_ticker')
        self.__source_ticker = value        

    @property
    def primary_vwap_unrealized_bps(self) -> dict:
        return self.__primary_vwap_unrealized_bps

    @primary_vwap_unrealized_bps.setter
    def primary_vwap_unrealized_bps(self, value: dict):
        self._property_changed('primary_vwap_unrealized_bps')
        self.__primary_vwap_unrealized_bps = value        

    @property
    def gsid(self) -> dict:
        return self.__gsid

    @gsid.setter
    def gsid(self, value: dict):
        self._property_changed('gsid')
        self.__gsid = value        

    @property
    def lending_fund(self) -> dict:
        return self.__lending_fund

    @lending_fund.setter
    def lending_fund(self, value: dict):
        self._property_changed('lending_fund')
        self.__lending_fund = value        

    @property
    def sensitivity(self) -> dict:
        return self.__sensitivity

    @sensitivity.setter
    def sensitivity(self, value: dict):
        self._property_changed('sensitivity')
        self.__sensitivity = value        

    @property
    def day_count(self) -> dict:
        return self.__day_count

    @day_count.setter
    def day_count(self, value: dict):
        self._property_changed('day_count')
        self.__day_count = value        

    @property
    def sell16bps(self) -> dict:
        return self.__sell16bps

    @sell16bps.setter
    def sell16bps(self, value: dict):
        self._property_changed('sell16bps')
        self.__sell16bps = value        

    @property
    def relative_break_even_inflation_change(self) -> dict:
        return self.__relative_break_even_inflation_change

    @relative_break_even_inflation_change.setter
    def relative_break_even_inflation_change(self, value: dict):
        self._property_changed('relative_break_even_inflation_change')
        self.__relative_break_even_inflation_change = value        

    @property
    def sell25cents(self) -> dict:
        return self.__sell25cents

    @sell25cents.setter
    def sell25cents(self, value: dict):
        self._property_changed('sell25cents')
        self.__sell25cents = value        

    @property
    def var_swap(self) -> dict:
        return self.__var_swap

    @var_swap.setter
    def var_swap(self, value: dict):
        self._property_changed('var_swap')
        self.__var_swap = value        

    @property
    def buy5point5bps(self) -> dict:
        return self.__buy5point5bps

    @buy5point5bps.setter
    def buy5point5bps(self, value: dict):
        self._property_changed('buy5point5bps')
        self.__buy5point5bps = value        

    @property
    def block_large_notional(self) -> dict:
        return self.__block_large_notional

    @block_large_notional.setter
    def block_large_notional(self, value: dict):
        self._property_changed('block_large_notional')
        self.__block_large_notional = value        

    @property
    def sell2point5bps(self) -> dict:
        return self.__sell2point5bps

    @sell2point5bps.setter
    def sell2point5bps(self, value: dict):
        self._property_changed('sell2point5bps')
        self.__sell2point5bps = value        

    @property
    def capacity(self) -> dict:
        return self.__capacity

    @capacity.setter
    def capacity(self, value: dict):
        self._property_changed('capacity')
        self.__capacity = value        

    @property
    def sectors_raw(self) -> dict:
        return self.__sectors_raw

    @sectors_raw.setter
    def sectors_raw(self, value: dict):
        self._property_changed('sectors_raw')
        self.__sectors_raw = value        

    @property
    def primary_vwap_in_limit(self) -> dict:
        return self.__primary_vwap_in_limit

    @primary_vwap_in_limit.setter
    def primary_vwap_in_limit(self, value: dict):
        self._property_changed('primary_vwap_in_limit')
        self.__primary_vwap_in_limit = value        

    @property
    def shareclass_price(self) -> dict:
        return self.__shareclass_price

    @shareclass_price.setter
    def shareclass_price(self, value: dict):
        self._property_changed('shareclass_price')
        self.__shareclass_price = value        

    @property
    def trade_size(self) -> dict:
        return self.__trade_size

    @trade_size.setter
    def trade_size(self, value: dict):
        self._property_changed('trade_size')
        self.__trade_size = value        

    @property
    def price_spot_entry_value(self) -> dict:
        return self.__price_spot_entry_value

    @price_spot_entry_value.setter
    def price_spot_entry_value(self, value: dict):
        self._property_changed('price_spot_entry_value')
        self.__price_spot_entry_value = value        

    @property
    def buy8point5bps(self) -> dict:
        return self.__buy8point5bps

    @buy8point5bps.setter
    def buy8point5bps(self, value: dict):
        self._property_changed('buy8point5bps')
        self.__buy8point5bps = value        

    @property
    def symbol_dimensions(self) -> dict:
        return self.__symbol_dimensions

    @symbol_dimensions.setter
    def symbol_dimensions(self, value: dict):
        self._property_changed('symbol_dimensions')
        self.__symbol_dimensions = value        

    @property
    def buy24bps(self) -> dict:
        return self.__buy24bps

    @buy24bps.setter
    def buy24bps(self, value: dict):
        self._property_changed('buy24bps')
        self.__buy24bps = value        

    @property
    def observation(self) -> dict:
        return self.__observation

    @observation.setter
    def observation(self, value: dict):
        self._property_changed('observation')
        self.__observation = value        

    @property
    def option_type_sdr(self) -> dict:
        return self.__option_type_sdr

    @option_type_sdr.setter
    def option_type_sdr(self, value: dict):
        self._property_changed('option_type_sdr')
        self.__option_type_sdr = value        

    @property
    def scenario_group_id(self) -> dict:
        return self.__scenario_group_id

    @scenario_group_id.setter
    def scenario_group_id(self, value: dict):
        self._property_changed('scenario_group_id')
        self.__scenario_group_id = value        

    @property
    def average_implied_variance(self) -> dict:
        return self.__average_implied_variance

    @average_implied_variance.setter
    def average_implied_variance(self, value: dict):
        self._property_changed('average_implied_variance')
        self.__average_implied_variance = value        

    @property
    def avg_trade_rate_description(self) -> dict:
        return self.__avg_trade_rate_description

    @avg_trade_rate_description.setter
    def avg_trade_rate_description(self, value: dict):
        self._property_changed('avg_trade_rate_description')
        self.__avg_trade_rate_description = value        

    @property
    def fraction(self) -> dict:
        return self.__fraction

    @fraction.setter
    def fraction(self, value: dict):
        self._property_changed('fraction')
        self.__fraction = value        

    @property
    def asset_count_short(self) -> dict:
        return self.__asset_count_short

    @asset_count_short.setter
    def asset_count_short(self, value: dict):
        self._property_changed('asset_count_short')
        self.__asset_count_short = value        

    @property
    def collateral_percentage_required(self) -> dict:
        return self.__collateral_percentage_required

    @collateral_percentage_required.setter
    def collateral_percentage_required(self, value: dict):
        self._property_changed('collateral_percentage_required')
        self.__collateral_percentage_required = value        

    @property
    def sell5point5bps(self) -> dict:
        return self.__sell5point5bps

    @sell5point5bps.setter
    def sell5point5bps(self, value: dict):
        self._property_changed('sell5point5bps')
        self.__sell5point5bps = value        

    @property
    def date(self) -> dict:
        return self.__date

    @date.setter
    def date(self, value: dict):
        self._property_changed('date')
        self.__date = value        

    @property
    def zip_code(self) -> dict:
        return self.__zip_code

    @zip_code.setter
    def zip_code(self, value: dict):
        self._property_changed('zip_code')
        self.__zip_code = value        

    @property
    def total_std_return_since_inception(self) -> dict:
        return self.__total_std_return_since_inception

    @total_std_return_since_inception.setter
    def total_std_return_since_inception(self, value: dict):
        self._property_changed('total_std_return_since_inception')
        self.__total_std_return_since_inception = value        

    @property
    def source_category(self) -> dict:
        return self.__source_category

    @source_category.setter
    def source_category(self, value: dict):
        self._property_changed('source_category')
        self.__source_category = value        

    @property
    def volume_unadjusted(self) -> dict:
        return self.__volume_unadjusted

    @volume_unadjusted.setter
    def volume_unadjusted(self, value: dict):
        self._property_changed('volume_unadjusted')
        self.__volume_unadjusted = value        

    @property
    def passive_ratio(self) -> dict:
        return self.__passive_ratio

    @passive_ratio.setter
    def passive_ratio(self, value: dict):
        self._property_changed('passive_ratio')
        self.__passive_ratio = value        

    @property
    def price_to_earnings(self) -> dict:
        return self.__price_to_earnings

    @price_to_earnings.setter
    def price_to_earnings(self, value: dict):
        self._property_changed('price_to_earnings')
        self.__price_to_earnings = value        

    @property
    def order_depth(self) -> dict:
        return self.__order_depth

    @order_depth.setter
    def order_depth(self, value: dict):
        self._property_changed('order_depth')
        self.__order_depth = value        

    @property
    def ann_yield3_month(self) -> dict:
        return self.__ann_yield3_month

    @ann_yield3_month.setter
    def ann_yield3_month(self, value: dict):
        self._property_changed('ann_yield3_month')
        self.__ann_yield3_month = value        

    @property
    def net_flow_std(self) -> dict:
        return self.__net_flow_std

    @net_flow_std.setter
    def net_flow_std(self, value: dict):
        self._property_changed('net_flow_std')
        self.__net_flow_std = value        

    @property
    def encoded_stats(self) -> dict:
        return self.__encoded_stats

    @encoded_stats.setter
    def encoded_stats(self, value: dict):
        self._property_changed('encoded_stats')
        self.__encoded_stats = value        

    @property
    def buy5bps(self) -> dict:
        return self.__buy5bps

    @buy5bps.setter
    def buy5bps(self, value: dict):
        self._property_changed('buy5bps')
        self.__buy5bps = value        

    @property
    def run_time(self) -> dict:
        return self.__run_time

    @run_time.setter
    def run_time(self, value: dict):
        self._property_changed('run_time')
        self.__run_time = value        

    @property
    def ask_size(self) -> dict:
        return self.__ask_size

    @ask_size.setter
    def ask_size(self, value: dict):
        self._property_changed('ask_size')
        self.__ask_size = value        

    @property
    def absolute_return_mtd(self) -> dict:
        return self.__absolute_return_mtd

    @absolute_return_mtd.setter
    def absolute_return_mtd(self, value: dict):
        self._property_changed('absolute_return_mtd')
        self.__absolute_return_mtd = value        

    @property
    def std30_days_unsubsidized_yield(self) -> dict:
        return self.__std30_days_unsubsidized_yield

    @std30_days_unsubsidized_yield.setter
    def std30_days_unsubsidized_yield(self, value: dict):
        self._property_changed('std30_days_unsubsidized_yield')
        self.__std30_days_unsubsidized_yield = value        

    @property
    def resource(self) -> dict:
        return self.__resource

    @resource.setter
    def resource(self, value: dict):
        self._property_changed('resource')
        self.__resource = value        

    @property
    def average_realized_volatility(self) -> dict:
        return self.__average_realized_volatility

    @average_realized_volatility.setter
    def average_realized_volatility(self, value: dict):
        self._property_changed('average_realized_volatility')
        self.__average_realized_volatility = value        

    @property
    def trace_adv_buy(self) -> dict:
        return self.__trace_adv_buy

    @trace_adv_buy.setter
    def trace_adv_buy(self, value: dict):
        self._property_changed('trace_adv_buy')
        self.__trace_adv_buy = value        

    @property
    def new_confirmed(self) -> dict:
        return self.__new_confirmed

    @new_confirmed.setter
    def new_confirmed(self, value: dict):
        self._property_changed('new_confirmed')
        self.__new_confirmed = value        

    @property
    def sell8bps(self) -> dict:
        return self.__sell8bps

    @sell8bps.setter
    def sell8bps(self, value: dict):
        self._property_changed('sell8bps')
        self.__sell8bps = value        

    @property
    def bid_price(self) -> dict:
        return self.__bid_price

    @bid_price.setter
    def bid_price(self, value: dict):
        self._property_changed('bid_price')
        self.__bid_price = value        

    @property
    def sell8point5bps(self) -> dict:
        return self.__sell8point5bps

    @sell8point5bps.setter
    def sell8point5bps(self, value: dict):
        self._property_changed('sell8point5bps')
        self.__sell8point5bps = value        

    @property
    def target_price_unrealized_bps(self) -> dict:
        return self.__target_price_unrealized_bps

    @target_price_unrealized_bps.setter
    def target_price_unrealized_bps(self, value: dict):
        self._property_changed('target_price_unrealized_bps')
        self.__target_price_unrealized_bps = value        

    @property
    def es_numeric_percentile(self) -> dict:
        return self.__es_numeric_percentile

    @es_numeric_percentile.setter
    def es_numeric_percentile(self, value: dict):
        self._property_changed('es_numeric_percentile')
        self.__es_numeric_percentile = value        

    @property
    def leg2_underlying_asset(self) -> dict:
        return self.__leg2_underlying_asset

    @leg2_underlying_asset.setter
    def leg2_underlying_asset(self, value: dict):
        self._property_changed('leg2_underlying_asset')
        self.__leg2_underlying_asset = value        

    @property
    def csa_terms(self) -> dict:
        return self.__csa_terms

    @csa_terms.setter
    def csa_terms(self, value: dict):
        self._property_changed('csa_terms')
        self.__csa_terms = value        

    @property
    def relative_payoff_mtd(self) -> dict:
        return self.__relative_payoff_mtd

    @relative_payoff_mtd.setter
    def relative_payoff_mtd(self, value: dict):
        self._property_changed('relative_payoff_mtd')
        self.__relative_payoff_mtd = value        

    @property
    def daily_net_shareholder_flows(self) -> dict:
        return self.__daily_net_shareholder_flows

    @daily_net_shareholder_flows.setter
    def daily_net_shareholder_flows(self, value: dict):
        self._property_changed('daily_net_shareholder_flows')
        self.__daily_net_shareholder_flows = value        

    @property
    def buy2point5bps(self) -> dict:
        return self.__buy2point5bps

    @buy2point5bps.setter
    def buy2point5bps(self, value: dict):
        self._property_changed('buy2point5bps')
        self.__buy2point5bps = value        

    @property
    def cai(self) -> dict:
        return self.__cai

    @cai.setter
    def cai(self, value: dict):
        self._property_changed('cai')
        self.__cai = value        

    @property
    def executed_notional_usd(self) -> dict:
        return self.__executed_notional_usd

    @executed_notional_usd.setter
    def executed_notional_usd(self, value: dict):
        self._property_changed('executed_notional_usd')
        self.__executed_notional_usd = value        

    @property
    def total_home_isolation(self) -> dict:
        return self.__total_home_isolation

    @total_home_isolation.setter
    def total_home_isolation(self, value: dict):
        self._property_changed('total_home_isolation')
        self.__total_home_isolation = value        

    @property
    def station_name(self) -> dict:
        return self.__station_name

    @station_name.setter
    def station_name(self, value: dict):
        self._property_changed('station_name')
        self.__station_name = value        

    @property
    def pass_pct(self) -> dict:
        return self.__pass_pct

    @pass_pct.setter
    def pass_pct(self, value: dict):
        self._property_changed('pass_pct')
        self.__pass_pct = value        

    @property
    def opening_report(self) -> dict:
        return self.__opening_report

    @opening_report.setter
    def opening_report(self, value: dict):
        self._property_changed('opening_report')
        self.__opening_report = value        

    @property
    def midcurve_atm_fwd_rate(self) -> dict:
        return self.__midcurve_atm_fwd_rate

    @midcurve_atm_fwd_rate.setter
    def midcurve_atm_fwd_rate(self, value: dict):
        self._property_changed('midcurve_atm_fwd_rate')
        self.__midcurve_atm_fwd_rate = value        

    @property
    def precipitation_forecast(self) -> dict:
        return self.__precipitation_forecast

    @precipitation_forecast.setter
    def precipitation_forecast(self, value: dict):
        self._property_changed('precipitation_forecast')
        self.__precipitation_forecast = value        

    @property
    def equity_risk_premium_index(self) -> dict:
        return self.__equity_risk_premium_index

    @equity_risk_premium_index.setter
    def equity_risk_premium_index(self, value: dict):
        self._property_changed('equity_risk_premium_index')
        self.__equity_risk_premium_index = value        

    @property
    def fatalities_underlying_conditions_unknown(self) -> dict:
        return self.__fatalities_underlying_conditions_unknown

    @fatalities_underlying_conditions_unknown.setter
    def fatalities_underlying_conditions_unknown(self, value: dict):
        self._property_changed('fatalities_underlying_conditions_unknown')
        self.__fatalities_underlying_conditions_unknown = value        

    @property
    def buy12bps(self) -> dict:
        return self.__buy12bps

    @buy12bps.setter
    def buy12bps(self, value: dict):
        self._property_changed('buy12bps')
        self.__buy12bps = value        

    @property
    def clearing_house(self) -> dict:
        return self.__clearing_house

    @clearing_house.setter
    def clearing_house(self, value: dict):
        self._property_changed('clearing_house')
        self.__clearing_house = value        

    @property
    def day_close_unrealized_bps(self) -> dict:
        return self.__day_close_unrealized_bps

    @day_close_unrealized_bps.setter
    def day_close_unrealized_bps(self, value: dict):
        self._property_changed('day_close_unrealized_bps')
        self.__day_close_unrealized_bps = value        

    @property
    def sts_rates_maturity(self) -> dict:
        return self.__sts_rates_maturity

    @sts_rates_maturity.setter
    def sts_rates_maturity(self, value: dict):
        self._property_changed('sts_rates_maturity')
        self.__sts_rates_maturity = value        

    @property
    def liq_dly(self) -> dict:
        return self.__liq_dly

    @liq_dly.setter
    def liq_dly(self, value: dict):
        self._property_changed('liq_dly')
        self.__liq_dly = value        

    @property
    def contributor_role(self) -> dict:
        return self.__contributor_role

    @contributor_role.setter
    def contributor_role(self, value: dict):
        self._property_changed('contributor_role')
        self.__contributor_role = value        

    @property
    def total_fatalities(self) -> dict:
        return self.__total_fatalities

    @total_fatalities.setter
    def total_fatalities(self, value: dict):
        self._property_changed('total_fatalities')
        self.__total_fatalities = value        


class FieldLinkSelector(Base):
        
    """Stores selector and name how field is presented in dataset."""

    @camel_case_translate
    def __init__(
        self,
        field_selector: str = None,
        description: str = None,
        display_name: str = None,
        name: str = None
    ):        
        super().__init__()
        self.field_selector = field_selector
        self.description = description
        self.display_name = display_name
        self.name = name

    @property
    def field_selector(self) -> str:
        """Selector which captures the field from the Entity."""
        return self.__field_selector

    @field_selector.setter
    def field_selector(self, value: str):
        self._property_changed('field_selector')
        self.__field_selector = value        

    @property
    def description(self) -> str:
        """Custom description (overrides field default)."""
        return self.__description

    @description.setter
    def description(self, value: str):
        self._property_changed('description')
        self.__description = value        

    @property
    def display_name(self) -> str:
        """Name under which the captured field will be displayed. The name must be
           registered in fields."""
        return self.__display_name

    @display_name.setter
    def display_name(self, value: str):
        self._property_changed('display_name')
        self.__display_name = value        


class MDAPI(Base):
        
    """Defines MDAPI fields."""

    @camel_case_translate
    def __init__(
        self,
        type_: str,
        quoting_styles: Tuple[dict, ...],
        class_: str = None,
        name: str = None
    ):        
        super().__init__()
        self.__class = class_
        self.__type = type_
        self.quoting_styles = quoting_styles
        self.name = name

    @property
    def class_(self) -> str:
        """MDAPI Class."""
        return self.__class

    @class_.setter
    def class_(self, value: str):
        self._property_changed('class_')
        self.__class = value        

    @property
    def type(self) -> str:
        """The MDAPI Type field (private)"""
        return self.__type

    @type.setter
    def type(self, value: str):
        self._property_changed('type')
        self.__type = value        

    @property
    def quoting_styles(self) -> Tuple[dict, ...]:
        """Map from MDAPI QuotingStyles to database columns"""
        return self.__quoting_styles

    @quoting_styles.setter
    def quoting_styles(self, value: Tuple[dict, ...]):
        self._property_changed('quoting_styles')
        self.__quoting_styles = value        


class MarketDataField(Base):
        
    @camel_case_translate
    def __init__(
        self,
        name: str = None,
        mapping: str = None
    ):        
        super().__init__()
        self.name = name
        self.mapping = mapping

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def mapping(self) -> str:
        return self.__mapping

    @mapping.setter
    def mapping(self, value: str):
        self._property_changed('mapping')
        self.__mapping = value        


class MarketDataFilteredField(Base):
        
    @camel_case_translate
    def __init__(
        self,
        field: str = None,
        default_value: str = None,
        default_numerical_value: float = None,
        default_boolean_value: bool = None,
        numerical_values: Tuple[float, ...] = None,
        values: Tuple[str, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.field = field
        self.default_value = default_value
        self.default_numerical_value = default_numerical_value
        self.default_boolean_value = default_boolean_value
        self.numerical_values = numerical_values
        self.values = values
        self.name = name

    @property
    def field(self) -> str:
        """Filtered field name"""
        return self.__field

    @field.setter
    def field(self, value: str):
        self._property_changed('field')
        self.__field = value        

    @property
    def default_value(self) -> str:
        """Default filtered field"""
        return self.__default_value

    @default_value.setter
    def default_value(self, value: str):
        self._property_changed('default_value')
        self.__default_value = value        

    @property
    def default_numerical_value(self) -> float:
        """Default numerical filtered field"""
        return self.__default_numerical_value

    @default_numerical_value.setter
    def default_numerical_value(self, value: float):
        self._property_changed('default_numerical_value')
        self.__default_numerical_value = value        

    @property
    def default_boolean_value(self) -> bool:
        """Default for boolean field"""
        return self.__default_boolean_value

    @default_boolean_value.setter
    def default_boolean_value(self, value: bool):
        self._property_changed('default_boolean_value')
        self.__default_boolean_value = value        

    @property
    def numerical_values(self) -> Tuple[float, ...]:
        """Array of numerical filtered fields"""
        return self.__numerical_values

    @numerical_values.setter
    def numerical_values(self, value: Tuple[float, ...]):
        self._property_changed('numerical_values')
        self.__numerical_values = value        

    @property
    def values(self) -> Tuple[str, ...]:
        """Array of filtered fields"""
        return self.__values

    @values.setter
    def values(self, value: Tuple[str, ...]):
        self._property_changed('values')
        self.__values = value        


class MeasureBacktest(Base):
        
    """Describes backtests that should be associated with a measure."""

    @camel_case_translate
    def __init__(
        self,
        name: str = None
    ):        
        super().__init__()
        self.name = name


class MeasureKpi(Base):
        
    """Describes KPIs that should be associated with a measure."""

    @camel_case_translate
    def __init__(
        self,
        name: str = None
    ):        
        super().__init__()
        self.name = name


class MidPrice(Base):
        
    """Specification for a mid price column derived from bid and ask columns."""

    @camel_case_translate
    def __init__(
        self,
        bid_column: str = None,
        ask_column: str = None,
        mid_column: str = None,
        name: str = None
    ):        
        super().__init__()
        self.bid_column = bid_column
        self.ask_column = ask_column
        self.mid_column = mid_column
        self.name = name

    @property
    def bid_column(self) -> str:
        """Database column name."""
        return self.__bid_column

    @bid_column.setter
    def bid_column(self, value: str):
        self._property_changed('bid_column')
        self.__bid_column = value        

    @property
    def ask_column(self) -> str:
        """Database column name."""
        return self.__ask_column

    @ask_column.setter
    def ask_column(self, value: str):
        self._property_changed('ask_column')
        self.__ask_column = value        

    @property
    def mid_column(self) -> str:
        """Database column name."""
        return self.__mid_column

    @mid_column.setter
    def mid_column(self, value: str):
        self._property_changed('mid_column')
        self.__mid_column = value        


class ParserEntity(Base):
        
    """Settings for a parser processor"""

    @camel_case_translate
    def __init__(
        self,
        only_normalized_fields: bool = None,
        quotes: bool = None,
        trades: bool = None,
        name: str = None
    ):        
        super().__init__()
        self.only_normalized_fields = only_normalized_fields
        self.quotes = quotes
        self.trades = trades
        self.name = name

    @property
    def only_normalized_fields(self) -> bool:
        """Setting for onlyNormalizedFields."""
        return self.__only_normalized_fields

    @only_normalized_fields.setter
    def only_normalized_fields(self, value: bool):
        self._property_changed('only_normalized_fields')
        self.__only_normalized_fields = value        

    @property
    def quotes(self) -> bool:
        """Setting for quotes."""
        return self.__quotes

    @quotes.setter
    def quotes(self, value: bool):
        self._property_changed('quotes')
        self.__quotes = value        

    @property
    def trades(self) -> bool:
        """Setting for trades."""
        return self.__trades

    @trades.setter
    def trades(self, value: bool):
        self._property_changed('trades')
        self.__trades = value        


class RemapFieldPair(Base):
        
    """Field and remapTo field pair."""

    @camel_case_translate
    def __init__(
        self,
        field: str = None,
        remap_to: str = None,
        name: str = None
    ):        
        super().__init__()
        self.field = field
        self.remap_to = remap_to
        self.name = name

    @property
    def field(self) -> str:
        """Field to remap."""
        return self.__field

    @field.setter
    def field(self, value: str):
        self._property_changed('field')
        self.__field = value        

    @property
    def remap_to(self) -> str:
        """Field to remap to."""
        return self.__remap_to

    @remap_to.setter
    def remap_to(self, value: str):
        self._property_changed('remap_to')
        self.__remap_to = value        


class SymbolFilterLink(Base):
        
    """The entity type and field used to filter symbols."""

    @camel_case_translate
    def __init__(
        self,
        entity_field: str = None,
        name: str = None
    ):        
        super().__init__()
        self.entity_field = entity_field
        self.name = name

    @property
    def entity_type(self) -> str:
        """The type of the entity to lookup to."""
        return 'MktCoordinate'        

    @property
    def entity_field(self) -> str:
        """The field of the entity to lookup to."""
        return self.__entity_field

    @entity_field.setter
    def entity_field(self, value: str):
        self._property_changed('entity_field')
        self.__entity_field = value        


class DataFilter(Base):
        
    """Filter on specified field."""

    @camel_case_translate
    def __init__(
        self,
        field: str,
        values: Tuple[str, ...],
        column: str = None,
        where: DataSetCondition = None,
        name: str = None
    ):        
        super().__init__()
        self.field = field
        self.column = column
        self.values = values
        self.where = where
        self.name = name

    @property
    def field(self) -> str:
        """Field to filter on."""
        return self.__field

    @field.setter
    def field(self, value: str):
        self._property_changed('field')
        self.__field = value        

    @property
    def column(self) -> str:
        """Database column name."""
        return self.__column

    @column.setter
    def column(self, value: str):
        self._property_changed('column')
        self.__column = value        

    @property
    def values(self) -> Tuple[str, ...]:
        """Value(s) to match."""
        return self.__values

    @values.setter
    def values(self, value: Tuple[str, ...]):
        self._property_changed('values')
        self.__values = value        

    @property
    def where(self) -> DataSetCondition:
        """Only apply the filter where this condition matches."""
        return self.__where

    @where.setter
    def where(self, value: DataSetCondition):
        self._property_changed('where')
        self.__where = value        


class DataQuery(Base):
        
    @camel_case_translate
    def __init__(
        self,
        id_: str = None,
        data_set_id: str = None,
        format_: Union[Format, str] = None,
        where: FieldFilterMapDataQuery = None,
        vendor: Union[MarketDataVendor, str] = None,
        start_date: datetime.date = None,
        end_date: datetime.date = None,
        start_time: datetime.datetime = None,
        page: int = None,
        page_size: int = None,
        end_time: datetime.datetime = None,
        as_of_time: datetime.datetime = None,
        id_as_of_date: datetime.date = None,
        use_temporal_x_ref: bool = False,
        since: datetime.datetime = None,
        dates: Tuple[datetime.date, ...] = None,
        times: Tuple[datetime.datetime, ...] = None,
        delay: int = None,
        intervals: int = None,
        samples: int = None,
        limit: int = None,
        polling_interval: int = None,
        grouped: bool = None,
        fields: Tuple[Union[dict, str], ...] = None,
        restrict_fields: bool = False,
        entity_filter: FieldFilterMapDataQuery = None,
        interval: str = None,
        distinct_consecutive: bool = False,
        time_filter: TimeFilter = None,
        use_field_alias: bool = False,
        remap_schema_to_alias: bool = False,
        name: str = None
    ):        
        super().__init__()
        self.__id = id_
        self.data_set_id = data_set_id
        self.__format = get_enum_value(Format, format_)
        self.where = where
        self.vendor = vendor
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.page = page
        self.page_size = page_size
        self.end_time = end_time
        self.as_of_time = as_of_time
        self.id_as_of_date = id_as_of_date
        self.use_temporal_x_ref = use_temporal_x_ref
        self.since = since
        self.dates = dates
        self.times = times
        self.delay = delay
        self.intervals = intervals
        self.samples = samples
        self.limit = limit
        self.polling_interval = polling_interval
        self.grouped = grouped
        self.fields = fields
        self.restrict_fields = restrict_fields
        self.entity_filter = entity_filter
        self.interval = interval
        self.distinct_consecutive = distinct_consecutive
        self.time_filter = time_filter
        self.use_field_alias = use_field_alias
        self.remap_schema_to_alias = remap_schema_to_alias
        self.name = name

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def data_set_id(self) -> str:
        """Marquee unique identifier"""
        return self.__data_set_id

    @data_set_id.setter
    def data_set_id(self, value: str):
        self._property_changed('data_set_id')
        self.__data_set_id = value        

    @property
    def format(self) -> Union[Format, str]:
        """Alternative format for data to be returned in"""
        return self.__format

    @format.setter
    def format(self, value: Union[Format, str]):
        self._property_changed('format')
        self.__format = get_enum_value(Format, value)        

    @property
    def where(self) -> FieldFilterMapDataQuery:
        """Filters on data fields."""
        return self.__where

    @where.setter
    def where(self, value: FieldFilterMapDataQuery):
        self._property_changed('where')
        self.__where = value        

    @property
    def vendor(self) -> Union[MarketDataVendor, str]:
        return self.__vendor

    @vendor.setter
    def vendor(self, value: Union[MarketDataVendor, str]):
        self._property_changed('vendor')
        self.__vendor = get_enum_value(MarketDataVendor, value)        

    @property
    def start_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__start_date

    @start_date.setter
    def start_date(self, value: datetime.date):
        self._property_changed('start_date')
        self.__start_date = value        

    @property
    def end_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__end_date

    @end_date.setter
    def end_date(self, value: datetime.date):
        self._property_changed('end_date')
        self.__end_date = value        

    @property
    def start_time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__start_time

    @start_time.setter
    def start_time(self, value: datetime.datetime):
        self._property_changed('start_time')
        self.__start_time = value        

    @property
    def page(self) -> int:
        """Number of symbols page to fetch."""
        return self.__page

    @page.setter
    def page(self, value: int):
        self._property_changed('page')
        self.__page = value        

    @property
    def page_size(self) -> int:
        """Number of how many symbols can be single page contain"""
        return self.__page_size

    @page_size.setter
    def page_size(self, value: int):
        self._property_changed('page_size')
        self.__page_size = value        

    @property
    def end_time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__end_time

    @end_time.setter
    def end_time(self, value: datetime.datetime):
        self._property_changed('end_time')
        self.__end_time = value        

    @property
    def as_of_time(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__as_of_time

    @as_of_time.setter
    def as_of_time(self, value: datetime.datetime):
        self._property_changed('as_of_time')
        self.__as_of_time = value        

    @property
    def id_as_of_date(self) -> datetime.date:
        """ISO 8601-formatted date"""
        return self.__id_as_of_date

    @id_as_of_date.setter
    def id_as_of_date(self, value: datetime.date):
        self._property_changed('id_as_of_date')
        self.__id_as_of_date = value        

    @property
    def use_temporal_x_ref(self) -> bool:
        """Set to true when xrefs provided in the query should be treated in a temporal way
           (e.g. get data points which had a certain BCID at some point in time,
           not which currently have it)."""
        return self.__use_temporal_x_ref

    @use_temporal_x_ref.setter
    def use_temporal_x_ref(self, value: bool):
        self._property_changed('use_temporal_x_ref')
        self.__use_temporal_x_ref = value        

    @property
    def since(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__since

    @since.setter
    def since(self, value: datetime.datetime):
        self._property_changed('since')
        self.__since = value        

    @property
    def dates(self) -> Tuple[datetime.date, ...]:
        """Select and return specific dates from dataset query results."""
        return self.__dates

    @dates.setter
    def dates(self, value: Tuple[datetime.date, ...]):
        self._property_changed('dates')
        self.__dates = value        

    @property
    def times(self) -> Tuple[datetime.datetime, ...]:
        """Select and return specific times from dataset query results."""
        return self.__times

    @times.setter
    def times(self, value: Tuple[datetime.datetime, ...]):
        self._property_changed('times')
        self.__times = value        

    @property
    def delay(self) -> int:
        """Number of minutes to delay returning data."""
        return self.__delay

    @delay.setter
    def delay(self, value: int):
        self._property_changed('delay')
        self.__delay = value        

    @property
    def intervals(self) -> int:
        """Number of intervals for which to return output times, for example if 10, it will
           return 10 data points evenly spaced over the time/date range."""
        return self.__intervals

    @intervals.setter
    def intervals(self, value: int):
        self._property_changed('intervals')
        self.__intervals = value        

    @property
    def samples(self) -> int:
        """Number of points to down sample the data, for example if 10, it will return at
           most 10 sample data points evenly spaced over the time/date range"""
        return self.__samples

    @samples.setter
    def samples(self, value: int):
        self._property_changed('samples')
        self.__samples = value        

    @property
    def limit(self) -> int:
        """Maximum number of rows for each asset to return."""
        return self.__limit

    @limit.setter
    def limit(self, value: int):
        self._property_changed('limit')
        self.__limit = value        

    @property
    def polling_interval(self) -> int:
        """When streaming, wait for this number of seconds between poll attempts."""
        return self.__polling_interval

    @polling_interval.setter
    def polling_interval(self, value: int):
        self._property_changed('polling_interval')
        self.__polling_interval = value        

    @property
    def grouped(self) -> bool:
        """Set to true to return results grouped by a given context (set of dimensions)."""
        return self.__grouped

    @grouped.setter
    def grouped(self, value: bool):
        self._property_changed('grouped')
        self.__grouped = value        

    @property
    def fields(self) -> Tuple[Union[dict, str], ...]:
        """Fields to be returned."""
        return self.__fields

    @fields.setter
    def fields(self, value: Tuple[Union[dict, str], ...]):
        self._property_changed('fields')
        self.__fields = value        

    @property
    def restrict_fields(self) -> bool:
        """Whether to return only the fields which are requested and suppress every other
           field"""
        return self.__restrict_fields

    @restrict_fields.setter
    def restrict_fields(self, value: bool):
        self._property_changed('restrict_fields')
        self.__restrict_fields = value        

    @property
    def entity_filter(self) -> FieldFilterMapDataQuery:
        """Filters that are applied only to entities i.e Asset. It is used for querying by
           asset parameters to return data for assets matching a certain
           criteria i.e floatingRateOption = LIBOR."""
        return self.__entity_filter

    @entity_filter.setter
    def entity_filter(self, value: FieldFilterMapDataQuery):
        self._property_changed('entity_filter')
        self.__entity_filter = value        

    @property
    def interval(self) -> str:
        """Interval to use when returning data. E.g. 1s, 1m, 1h, 1d. Only seconds(s),
           minutes(m), hours(h) and days(d) are supported."""
        return self.__interval

    @interval.setter
    def interval(self, value: str):
        self._property_changed('interval')
        self.__interval = value        

    @property
    def distinct_consecutive(self) -> bool:
        """enable removing consecutive duplicates"""
        return self.__distinct_consecutive

    @distinct_consecutive.setter
    def distinct_consecutive(self, value: bool):
        self._property_changed('distinct_consecutive')
        self.__distinct_consecutive = value        

    @property
    def time_filter(self) -> TimeFilter:
        """Filter to restrict data to a range of hours per day."""
        return self.__time_filter

    @time_filter.setter
    def time_filter(self, value: TimeFilter):
        self._property_changed('time_filter')
        self.__time_filter = value        

    @property
    def use_field_alias(self) -> bool:
        """Whether to use field alias in the query."""
        return self.__use_field_alias

    @use_field_alias.setter
    def use_field_alias(self, value: bool):
        self._property_changed('use_field_alias')
        self.__use_field_alias = value        

    @property
    def remap_schema_to_alias(self) -> bool:
        """Whether to remap the schema of the output data to field aliases, if aliases have
           been used to query the data"""
        return self.__remap_schema_to_alias

    @remap_schema_to_alias.setter
    def remap_schema_to_alias(self, value: bool):
        self._property_changed('remap_schema_to_alias')
        self.__remap_schema_to_alias = value        


class DataQueryResponse(Base):
        
    @camel_case_translate
    def __init__(
        self,
        type_: str,
        request_id: str = None,
        error_message: str = None,
        id_: str = None,
        total_pages: int = None,
        data_set_id: str = None,
        entity_type: Union[MeasureEntityType, str] = None,
        delay: int = None,
        data: Tuple[FieldValueMap, ...] = None,
        groups: Tuple[DataGroup, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.request_id = request_id
        self.__type = type_
        self.error_message = error_message
        self.__id = id_
        self.total_pages = total_pages
        self.data_set_id = data_set_id
        self.entity_type = entity_type
        self.delay = delay
        self.data = data
        self.groups = groups
        self.name = name

    @property
    def request_id(self) -> str:
        """Marquee unique identifier"""
        return self.__request_id

    @request_id.setter
    def request_id(self, value: str):
        self._property_changed('request_id')
        self.__request_id = value        

    @property
    def type(self) -> str:
        return self.__type

    @type.setter
    def type(self, value: str):
        self._property_changed('type')
        self.__type = value        

    @property
    def error_message(self) -> str:
        return self.__error_message

    @error_message.setter
    def error_message(self, value: str):
        self._property_changed('error_message')
        self.__error_message = value        

    @property
    def id(self) -> str:
        """Marquee unique identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def total_pages(self) -> int:
        """Number of total symbol pages"""
        return self.__total_pages

    @total_pages.setter
    def total_pages(self, value: int):
        self._property_changed('total_pages')
        self.__total_pages = value        

    @property
    def data_set_id(self) -> str:
        """Unique id of dataset."""
        return self.__data_set_id

    @data_set_id.setter
    def data_set_id(self, value: str):
        self._property_changed('data_set_id')
        self.__data_set_id = value        

    @property
    def entity_type(self) -> Union[MeasureEntityType, str]:
        """Entity type associated with a measure."""
        return self.__entity_type

    @entity_type.setter
    def entity_type(self, value: Union[MeasureEntityType, str]):
        self._property_changed('entity_type')
        self.__entity_type = get_enum_value(MeasureEntityType, value)        

    @property
    def delay(self) -> int:
        return self.__delay

    @delay.setter
    def delay(self, value: int):
        self._property_changed('delay')
        self.__delay = value        

    @property
    def data(self) -> Tuple[FieldValueMap, ...]:
        """Array of data elements from dataset"""
        return self.__data

    @data.setter
    def data(self, value: Tuple[FieldValueMap, ...]):
        self._property_changed('data')
        self.__data = value        

    @property
    def groups(self) -> Tuple[DataGroup, ...]:
        """If the data is requested in grouped mode, will return data group object"""
        return self.__groups

    @groups.setter
    def groups(self, value: Tuple[DataGroup, ...]):
        self._property_changed('groups')
        self.__groups = value        


class DataSetDelay(Base):
        
    """Specifies the delayed data properties."""

    @camel_case_translate
    def __init__(
        self,
        until_seconds: float,
        at_time_zone: str,
        when: Tuple[Union[DelayExclusionType, str], ...] = None,
        history_up_to_seconds: float = None,
        history_up_to_time: datetime.datetime = None,
        history_up_to_months: float = None,
        name: str = None
    ):        
        super().__init__()
        self.until_seconds = until_seconds
        self.at_time_zone = at_time_zone
        self.when = when
        self.history_up_to_seconds = history_up_to_seconds
        self.history_up_to_time = history_up_to_time
        self.history_up_to_months = history_up_to_months
        self.name = name

    @property
    def until_seconds(self) -> float:
        """Seconds from midnight until which the delay will be applicable."""
        return self.__until_seconds

    @until_seconds.setter
    def until_seconds(self, value: float):
        self._property_changed('until_seconds')
        self.__until_seconds = value        

    @property
    def at_time_zone(self) -> str:
        """The time zone with respect to which the delay will be applied (must be a valid
           IANA TimeZone identifier)."""
        return self.__at_time_zone

    @at_time_zone.setter
    def at_time_zone(self, value: str):
        self._property_changed('at_time_zone')
        self.__at_time_zone = value        

    @property
    def when(self) -> Tuple[Union[DelayExclusionType, str], ...]:
        """Apply this delay filter only when the day belongs to this exclusion list."""
        return self.__when

    @when.setter
    def when(self, value: Tuple[Union[DelayExclusionType, str], ...]):
        self._property_changed('when')
        self.__when = value        

    @property
    def history_up_to_seconds(self) -> float:
        """Relative seconds up to which the data history will be shown for the business
           day."""
        return self.__history_up_to_seconds

    @history_up_to_seconds.setter
    def history_up_to_seconds(self, value: float):
        self._property_changed('history_up_to_seconds')
        self.__history_up_to_seconds = value        

    @property
    def history_up_to_time(self) -> datetime.datetime:
        """Absolute time up to which the data history will be shown for the business day."""
        return self.__history_up_to_time

    @history_up_to_time.setter
    def history_up_to_time(self, value: datetime.datetime):
        self._property_changed('history_up_to_time')
        self.__history_up_to_time = value        

    @property
    def history_up_to_months(self) -> float:
        """Months time up to which the data history will be shown for the business day."""
        return self.__history_up_to_months

    @history_up_to_months.setter
    def history_up_to_months(self, value: float):
        self._property_changed('history_up_to_months')
        self.__history_up_to_months = value        


class DataSetTransforms(Base):
        
    """Dataset transformation specifiers."""

    @camel_case_translate
    def __init__(
        self,
        redact_columns: Tuple[str, ...] = None,
        round_columns: Tuple[str, ...] = None,
        remap_fields: Tuple[RemapFieldPair, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.redact_columns = redact_columns
        self.round_columns = round_columns
        self.remap_fields = remap_fields
        self.name = name

    @property
    def redact_columns(self) -> Tuple[str, ...]:
        """Redact (exclude) a list of database columns."""
        return self.__redact_columns

    @redact_columns.setter
    def redact_columns(self, value: Tuple[str, ...]):
        self._property_changed('redact_columns')
        self.__redact_columns = value        

    @property
    def round_columns(self) -> Tuple[str, ...]:
        """Rounds list of database columns."""
        return self.__round_columns

    @round_columns.setter
    def round_columns(self, value: Tuple[str, ...]):
        self._property_changed('round_columns')
        self.__round_columns = value        

    @property
    def remap_fields(self) -> Tuple[RemapFieldPair, ...]:
        """Remaps a list of output fields to a different list of fields."""
        return self.__remap_fields

    @remap_fields.setter
    def remap_fields(self, value: Tuple[RemapFieldPair, ...]):
        self._property_changed('remap_fields')
        self.__remap_fields = value        


class DeleteCoverageQuery(Base):
        
    @camel_case_translate
    def __init__(
        self,
        where: FieldFilterMapDataQuery = None,
        delete_all: bool = False,
        name: str = None
    ):        
        super().__init__()
        self.where = where
        self.delete_all = delete_all
        self.name = name

    @property
    def where(self) -> FieldFilterMapDataQuery:
        """Filters on data fields."""
        return self.__where

    @where.setter
    def where(self, value: FieldFilterMapDataQuery):
        self._property_changed('where')
        self.__where = value        

    @property
    def delete_all(self) -> bool:
        return self.__delete_all

    @delete_all.setter
    def delete_all(self, value: bool):
        self._property_changed('delete_all')
        self.__delete_all = value        


class FieldLink(Base):
        
    """Link the dataset field to an entity to also fetch its fields. It has two
       mutually exclusive modes of operation: prefixing or explicit inclusion
       entity fields."""

    @camel_case_translate
    def __init__(
        self,
        entity_identifier: str = None,
        prefix: str = None,
        additional_entity_fields: Tuple[FieldLinkSelector, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.entity_identifier = entity_identifier
        self.prefix = prefix
        self.additional_entity_fields = additional_entity_fields
        self.name = name

    @property
    def entity_type(self) -> str:
        """The type of the entity to lookup to."""
        return 'Asset'        

    @property
    def entity_identifier(self) -> str:
        """The identifier of the entity to link the dataset field to."""
        return self.__entity_identifier

    @entity_identifier.setter
    def entity_identifier(self, value: str):
        self._property_changed('entity_identifier')
        self.__entity_identifier = value        

    @property
    def prefix(self) -> str:
        """Prefix to put before the fields fetched from the linked entity (must be unique
           for each dataset field). Prefix cannot be applied with
           additionalEntityFields."""
        return self.__prefix

    @prefix.setter
    def prefix(self, value: str):
        self._property_changed('prefix')
        self.__prefix = value        

    @property
    def additional_entity_fields(self) -> Tuple[FieldLinkSelector, ...]:
        """List of fields from the linked entity to include. It cannot be applied with
           prefix"""
        return self.__additional_entity_fields

    @additional_entity_fields.setter
    def additional_entity_fields(self, value: Tuple[FieldLinkSelector, ...]):
        self._property_changed('additional_entity_fields')
        self.__additional_entity_fields = value        


class MarketDataMapping(Base):
        
    @camel_case_translate
    def __init__(
        self,
        asset_class: Union[AssetClass, str] = None,
        query_type: str = None,
        description: str = None,
        scale: float = None,
        frequency: Union[MarketDataFrequency, str] = None,
        measures: Tuple[Union[MarketDataMeasure, str], ...] = None,
        data_set: str = None,
        vendor: Union[MarketDataVendor, str] = None,
        fields: Tuple[MarketDataField, ...] = None,
        rank: float = None,
        filtered_fields: Tuple[MarketDataFilteredField, ...] = None,
        asset_types: Tuple[Union[AssetType, str], ...] = None,
        entity_type: Union[MeasureEntityType, str] = None,
        backtest_entity: MeasureBacktest = None,
        kpi_entity: MeasureKpi = None,
        name: str = None
    ):        
        super().__init__()
        self.asset_class = asset_class
        self.query_type = query_type
        self.description = description
        self.scale = scale
        self.frequency = frequency
        self.measures = measures
        self.data_set = data_set
        self.vendor = vendor
        self.fields = fields
        self.rank = rank
        self.filtered_fields = filtered_fields
        self.asset_types = asset_types
        self.entity_type = entity_type
        self.backtest_entity = backtest_entity
        self.kpi_entity = kpi_entity
        self.name = name

    @property
    def asset_class(self) -> Union[AssetClass, str]:
        """Asset class that is applicable for mapping."""
        return self.__asset_class

    @asset_class.setter
    def asset_class(self, value: Union[AssetClass, str]):
        self._property_changed('asset_class')
        self.__asset_class = get_enum_value(AssetClass, value)        

    @property
    def query_type(self) -> str:
        """Market data query type."""
        return self.__query_type

    @query_type.setter
    def query_type(self, value: str):
        self._property_changed('query_type')
        self.__query_type = value        

    @property
    def description(self) -> str:
        """Query type description"""
        return self.__description

    @description.setter
    def description(self, value: str):
        self._property_changed('description')
        self.__description = value        

    @property
    def scale(self) -> float:
        """Scale multiplier for time series"""
        return self.__scale

    @scale.setter
    def scale(self, value: float):
        self._property_changed('scale')
        self.__scale = value        

    @property
    def frequency(self) -> Union[MarketDataFrequency, str]:
        return self.__frequency

    @frequency.setter
    def frequency(self, value: Union[MarketDataFrequency, str]):
        self._property_changed('frequency')
        self.__frequency = get_enum_value(MarketDataFrequency, value)        

    @property
    def measures(self) -> Tuple[Union[MarketDataMeasure, str], ...]:
        return self.__measures

    @measures.setter
    def measures(self, value: Tuple[Union[MarketDataMeasure, str], ...]):
        self._property_changed('measures')
        self.__measures = value        

    @property
    def data_set(self) -> str:
        """Marquee unique identifier"""
        return self.__data_set

    @data_set.setter
    def data_set(self, value: str):
        self._property_changed('data_set')
        self.__data_set = value        

    @property
    def vendor(self) -> Union[MarketDataVendor, str]:
        return self.__vendor

    @vendor.setter
    def vendor(self, value: Union[MarketDataVendor, str]):
        self._property_changed('vendor')
        self.__vendor = get_enum_value(MarketDataVendor, value)        

    @property
    def fields(self) -> Tuple[MarketDataField, ...]:
        return self.__fields

    @fields.setter
    def fields(self, value: Tuple[MarketDataField, ...]):
        self._property_changed('fields')
        self.__fields = value        

    @property
    def rank(self) -> float:
        return self.__rank

    @rank.setter
    def rank(self, value: float):
        self._property_changed('rank')
        self.__rank = value        

    @property
    def filtered_fields(self) -> Tuple[MarketDataFilteredField, ...]:
        return self.__filtered_fields

    @filtered_fields.setter
    def filtered_fields(self, value: Tuple[MarketDataFilteredField, ...]):
        self._property_changed('filtered_fields')
        self.__filtered_fields = value        

    @property
    def asset_types(self) -> Tuple[Union[AssetType, str], ...]:
        """Asset type differentiates the product categorization or contract type"""
        return self.__asset_types

    @asset_types.setter
    def asset_types(self, value: Tuple[Union[AssetType, str], ...]):
        self._property_changed('asset_types')
        self.__asset_types = value        

    @property
    def entity_type(self) -> Union[MeasureEntityType, str]:
        """Entity type associated with a measure."""
        return self.__entity_type

    @entity_type.setter
    def entity_type(self, value: Union[MeasureEntityType, str]):
        self._property_changed('entity_type')
        self.__entity_type = get_enum_value(MeasureEntityType, value)        

    @property
    def backtest_entity(self) -> MeasureBacktest:
        """Describes backtests that should be associated with a measure."""
        return self.__backtest_entity

    @backtest_entity.setter
    def backtest_entity(self, value: MeasureBacktest):
        self._property_changed('backtest_entity')
        self.__backtest_entity = value        

    @property
    def kpi_entity(self) -> MeasureKpi:
        """Describes KPIs that should be associated with a measure."""
        return self.__kpi_entity

    @kpi_entity.setter
    def kpi_entity(self, value: MeasureKpi):
        self._property_changed('kpi_entity')
        self.__kpi_entity = value        


class ProcessorEntity(Base):
        
    """Query processors for dataset."""

    @camel_case_translate
    def __init__(
        self,
        filters: Tuple[str, ...] = None,
        parsers: Tuple[ParserEntity, ...] = None,
        deduplicate: Tuple[str, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.filters = filters
        self.parsers = parsers
        self.deduplicate = deduplicate
        self.name = name

    @property
    def filters(self) -> Tuple[str, ...]:
        """List of filter processors."""
        return self.__filters

    @filters.setter
    def filters(self, value: Tuple[str, ...]):
        self._property_changed('filters')
        self.__filters = value        

    @property
    def parsers(self) -> Tuple[ParserEntity, ...]:
        """List of parser processors."""
        return self.__parsers

    @parsers.setter
    def parsers(self, value: Tuple[ParserEntity, ...]):
        self._property_changed('parsers')
        self.__parsers = value        

    @property
    def deduplicate(self) -> Tuple[str, ...]:
        """Columns on which a deduplication processor should be run."""
        return self.__deduplicate

    @deduplicate.setter
    def deduplicate(self, value: Tuple[str, ...]):
        self._property_changed('deduplicate')
        self.__deduplicate = value        


class SymbolFilterDimension(Base):
        
    """Map the dataset field with an entity for filtering arctic symbols."""

    @camel_case_translate
    def __init__(
        self,
        field: str = None,
        field_description: str = None,
        symbol_filter_link: SymbolFilterLink = None,
        name: str = None
    ):        
        super().__init__()
        self.field = field
        self.field_description = field_description
        self.symbol_filter_link = symbol_filter_link
        self.name = name

    @property
    def field(self) -> str:
        """Field name."""
        return self.__field

    @field.setter
    def field(self, value: str):
        self._property_changed('field')
        self.__field = value        

    @property
    def field_description(self) -> str:
        """Custom description (overrides field default)."""
        return self.__field_description

    @field_description.setter
    def field_description(self, value: str):
        self._property_changed('field_description')
        self.__field_description = value        

    @property
    def symbol_filter_link(self) -> SymbolFilterLink:
        """The entity type and field used to filter symbols."""
        return self.__symbol_filter_link

    @symbol_filter_link.setter
    def symbol_filter_link(self, value: SymbolFilterLink):
        self._property_changed('symbol_filter_link')
        self.__symbol_filter_link = value        


class ComplexFilter(Base):
        
    """A compound filter for data requests."""

    @camel_case_translate
    def __init__(
        self,
        operator: str,
        simple_filters: Tuple[DataFilter, ...],
        name: str = None
    ):        
        super().__init__()
        self.operator = operator
        self.simple_filters = simple_filters
        self.name = name

    @property
    def operator(self) -> str:
        return self.__operator

    @operator.setter
    def operator(self, value: str):
        self._property_changed('operator')
        self.__operator = value        

    @property
    def simple_filters(self) -> Tuple[DataFilter, ...]:
        """Filter on specified field."""
        return self.__simple_filters

    @simple_filters.setter
    def simple_filters(self, value: Tuple[DataFilter, ...]):
        self._property_changed('simple_filters')
        self.__simple_filters = value        


class DataSetTransformation(Base):
        
    """Transform the Dataset output. Can be used with or without certain conditions."""

    @camel_case_translate
    def __init__(
        self,
        transforms: DataSetTransforms,
        condition: DataSetCondition = None,
        name: str = None
    ):        
        super().__init__()
        self.condition = condition
        self.transforms = transforms
        self.name = name

    @property
    def condition(self) -> DataSetCondition:
        """Condition to match before applying the transformations."""
        return self.__condition

    @condition.setter
    def condition(self, value: DataSetCondition):
        self._property_changed('condition')
        self.__condition = value        

    @property
    def transforms(self) -> DataSetTransforms:
        """Series of transformation actions to perform."""
        return self.__transforms

    @transforms.setter
    def transforms(self, value: DataSetTransforms):
        self._property_changed('transforms')
        self.__transforms = value        


class FieldColumnPair(Base):
        
    """Map from fields to database columns."""

    @camel_case_translate
    def __init__(
        self,
        field: str = None,
        column: str = None,
        field_description: str = None,
        link: FieldLink = None,
        aliases: Tuple[str, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.field = field
        self.column = column
        self.field_description = field_description
        self.link = link
        self.aliases = aliases
        self.name = name

    @property
    def field(self) -> str:
        """Field name."""
        return self.__field

    @field.setter
    def field(self, value: str):
        self._property_changed('field')
        self.__field = value        

    @property
    def column(self) -> str:
        """Database column name."""
        return self.__column

    @column.setter
    def column(self, value: str):
        self._property_changed('column')
        self.__column = value        

    @property
    def field_description(self) -> str:
        """Custom description (overrides field default)."""
        return self.__field_description

    @field_description.setter
    def field_description(self, value: str):
        self._property_changed('field_description')
        self.__field_description = value        

    @property
    def link(self) -> FieldLink:
        """Link the field with other entity to also fetch its fields."""
        return self.__link

    @link.setter
    def link(self, value: FieldLink):
        self._property_changed('link')
        self.__link = value        

    @property
    def aliases(self) -> Tuple[str, ...]:
        """Set of alias fields that can be used to refer to the current field when
           querying."""
        return self.__aliases

    @aliases.setter
    def aliases(self, value: Tuple[str, ...]):
        self._property_changed('aliases')
        self.__aliases = value        


class HistoryFilter(Base):
        
    """Restricts queries against dataset to a time range."""

    @camel_case_translate
    def __init__(
        self,
        absolute_start: datetime.datetime = None,
        absolute_end: datetime.datetime = None,
        relative_start_seconds: float = None,
        relative_end_seconds: float = None,
        delay: dict = None,
        name: str = None
    ):        
        super().__init__()
        self.absolute_start = absolute_start
        self.absolute_end = absolute_end
        self.relative_start_seconds = relative_start_seconds
        self.relative_end_seconds = relative_end_seconds
        self.delay = delay
        self.name = name

    @property
    def absolute_start(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__absolute_start

    @absolute_start.setter
    def absolute_start(self, value: datetime.datetime):
        self._property_changed('absolute_start')
        self.__absolute_start = value        

    @property
    def absolute_end(self) -> datetime.datetime:
        """ISO 8601-formatted timestamp"""
        return self.__absolute_end

    @absolute_end.setter
    def absolute_end(self, value: datetime.datetime):
        self._property_changed('absolute_end')
        self.__absolute_end = value        

    @property
    def relative_start_seconds(self) -> float:
        """Earliest start time in seconds before current time."""
        return self.__relative_start_seconds

    @relative_start_seconds.setter
    def relative_start_seconds(self, value: float):
        self._property_changed('relative_start_seconds')
        self.__relative_start_seconds = value        

    @property
    def relative_end_seconds(self) -> float:
        """Latest end time in seconds before current time."""
        return self.__relative_end_seconds

    @relative_end_seconds.setter
    def relative_end_seconds(self, value: float):
        self._property_changed('relative_end_seconds')
        self.__relative_end_seconds = value        

    @property
    def delay(self) -> dict:
        return self.__delay

    @delay.setter
    def delay(self, value: dict):
        self._property_changed('delay')
        self.__delay = value        


class DataSetDimensions(Base):
        
    """Dataset dimensions."""

    @camel_case_translate
    def __init__(
        self,
        symbol_dimensions: Tuple[str, ...],
        time_field: str = None,
        transaction_time_field: str = None,
        symbol_dimension_properties: Tuple[FieldColumnPair, ...] = None,
        non_symbol_dimensions: Tuple[FieldColumnPair, ...] = None,
        symbol_dimension_link: FieldLink = None,
        linked_dimensions: Tuple[FieldLinkSelector, ...] = None,
        symbol_filter_dimensions: Tuple[SymbolFilterDimension, ...] = None,
        key_dimensions: Tuple[str, ...] = None,
        measures: Tuple[FieldColumnPair, ...] = None,
        entity_dimension: str = None,
        name: str = None
    ):        
        super().__init__()
        self.time_field = time_field
        self.transaction_time_field = transaction_time_field
        self.symbol_dimensions = symbol_dimensions
        self.symbol_dimension_properties = symbol_dimension_properties
        self.non_symbol_dimensions = non_symbol_dimensions
        self.symbol_dimension_link = symbol_dimension_link
        self.linked_dimensions = linked_dimensions
        self.symbol_filter_dimensions = symbol_filter_dimensions
        self.key_dimensions = key_dimensions
        self.measures = measures
        self.entity_dimension = entity_dimension
        self.name = name

    @property
    def time_field(self) -> str:
        return self.__time_field

    @time_field.setter
    def time_field(self, value: str):
        self._property_changed('time_field')
        self.__time_field = value        

    @property
    def transaction_time_field(self) -> str:
        """For bi-temporal datasets, field for capturing the time at which a data point was
           updated."""
        return self.__transaction_time_field

    @transaction_time_field.setter
    def transaction_time_field(self, value: str):
        self._property_changed('transaction_time_field')
        self.__transaction_time_field = value        

    @property
    def symbol_dimensions(self) -> Tuple[str, ...]:
        """Set of fields that determine database table name."""
        return self.__symbol_dimensions

    @symbol_dimensions.setter
    def symbol_dimensions(self, value: Tuple[str, ...]):
        self._property_changed('symbol_dimensions')
        self.__symbol_dimensions = value        

    @property
    def symbol_dimension_properties(self) -> Tuple[FieldColumnPair, ...]:
        """Additional properties for symbol dimensions."""
        return self.__symbol_dimension_properties

    @symbol_dimension_properties.setter
    def symbol_dimension_properties(self, value: Tuple[FieldColumnPair, ...]):
        self._property_changed('symbol_dimension_properties')
        self.__symbol_dimension_properties = value        

    @property
    def non_symbol_dimensions(self) -> Tuple[FieldColumnPair, ...]:
        """Fields that are not nullable."""
        return self.__non_symbol_dimensions

    @non_symbol_dimensions.setter
    def non_symbol_dimensions(self, value: Tuple[FieldColumnPair, ...]):
        self._property_changed('non_symbol_dimensions')
        self.__non_symbol_dimensions = value        

    @property
    def symbol_dimension_link(self) -> FieldLink:
        """Deprecated - use linkedDimensions."""
        return self.__symbol_dimension_link

    @symbol_dimension_link.setter
    def symbol_dimension_link(self, value: FieldLink):
        self._property_changed('symbol_dimension_link')
        self.__symbol_dimension_link = value        

    @property
    def linked_dimensions(self) -> Tuple[FieldLinkSelector, ...]:
        """Fields that are injected from entity into dataset."""
        return self.__linked_dimensions

    @linked_dimensions.setter
    def linked_dimensions(self, value: Tuple[FieldLinkSelector, ...]):
        self._property_changed('linked_dimensions')
        self.__linked_dimensions = value        

    @property
    def symbol_filter_dimensions(self) -> Tuple[SymbolFilterDimension, ...]:
        """Map the dataset field with an entity for filtering arctic symbols."""
        return self.__symbol_filter_dimensions

    @symbol_filter_dimensions.setter
    def symbol_filter_dimensions(self, value: Tuple[SymbolFilterDimension, ...]):
        self._property_changed('symbol_filter_dimensions')
        self.__symbol_filter_dimensions = value        

    @property
    def key_dimensions(self) -> Tuple[str, ...]:
        """Fields to slice dataset by. Used for query results where same symbolDimension
           has multiple updateTimes."""
        return self.__key_dimensions

    @key_dimensions.setter
    def key_dimensions(self, value: Tuple[str, ...]):
        self._property_changed('key_dimensions')
        self.__key_dimensions = value        

    @property
    def measures(self) -> Tuple[FieldColumnPair, ...]:
        """Fields that are nullable."""
        return self.__measures

    @measures.setter
    def measures(self, value: Tuple[FieldColumnPair, ...]):
        self._property_changed('measures')
        self.__measures = value        

    @property
    def entity_dimension(self) -> str:
        """Symbol dimension corresponding to an entity e.g. asset or report."""
        return self.__entity_dimension

    @entity_dimension.setter
    def entity_dimension(self, value: str):
        self._property_changed('entity_dimension')
        self.__entity_dimension = value        


class EntityFilter(Base):
        
    """Filter on entities."""

    @camel_case_translate
    def __init__(
        self,
        operator: str = None,
        simple_filters: Tuple[DataFilter, ...] = None,
        complex_filters: Tuple[ComplexFilter, ...] = None,
        name: str = None
    ):        
        super().__init__()
        self.operator = operator
        self.simple_filters = simple_filters
        self.complex_filters = complex_filters
        self.name = name

    @property
    def operator(self) -> str:
        return self.__operator

    @operator.setter
    def operator(self, value: str):
        self._property_changed('operator')
        self.__operator = value        

    @property
    def simple_filters(self) -> Tuple[DataFilter, ...]:
        """Filter on specified field."""
        return self.__simple_filters

    @simple_filters.setter
    def simple_filters(self, value: Tuple[DataFilter, ...]):
        self._property_changed('simple_filters')
        self.__simple_filters = value        

    @property
    def complex_filters(self) -> Tuple[ComplexFilter, ...]:
        """A compound filter for data requests."""
        return self.__complex_filters

    @complex_filters.setter
    def complex_filters(self, value: Tuple[ComplexFilter, ...]):
        self._property_changed('complex_filters')
        self.__complex_filters = value        


class DataSetFilters(Base):
        
    """Filters to restrict the set of data returned."""

    @camel_case_translate
    def __init__(
        self,
        entity_filter: EntityFilter = None,
        row_filters: Tuple[DataFilter, ...] = None,
        advanced_filters: Tuple[AdvancedFilter, ...] = None,
        history_filter: HistoryFilter = None,
        time_filter: TimeFilter = None,
        name: str = None
    ):        
        super().__init__()
        self.entity_filter = entity_filter
        self.row_filters = row_filters
        self.advanced_filters = advanced_filters
        self.history_filter = history_filter
        self.time_filter = time_filter
        self.name = name

    @property
    def entity_filter(self) -> EntityFilter:
        """Filter on entities."""
        return self.__entity_filter

    @entity_filter.setter
    def entity_filter(self, value: EntityFilter):
        self._property_changed('entity_filter')
        self.__entity_filter = value        

    @property
    def row_filters(self) -> Tuple[DataFilter, ...]:
        """Filters on database rows."""
        return self.__row_filters

    @row_filters.setter
    def row_filters(self, value: Tuple[DataFilter, ...]):
        self._property_changed('row_filters')
        self.__row_filters = value        

    @property
    def advanced_filters(self) -> Tuple[AdvancedFilter, ...]:
        """Advanced filters for the Dataset."""
        return self.__advanced_filters

    @advanced_filters.setter
    def advanced_filters(self, value: Tuple[AdvancedFilter, ...]):
        self._property_changed('advanced_filters')
        self.__advanced_filters = value        

    @property
    def history_filter(self) -> HistoryFilter:
        """Restricts queries against dataset to a time range."""
        return self.__history_filter

    @history_filter.setter
    def history_filter(self, value: HistoryFilter):
        self._property_changed('history_filter')
        self.__history_filter = value        

    @property
    def time_filter(self) -> TimeFilter:
        """Filter to restrict data to a range of hours per day."""
        return self.__time_filter

    @time_filter.setter
    def time_filter(self, value: TimeFilter):
        self._property_changed('time_filter')
        self.__time_filter = value        


class DataSetEntity(Base):
        
    @camel_case_translate
    def __init__(
        self,
        id_: str,
        name: str,
        owner_id: str = None,
        description: str = None,
        short_description: str = None,
        mappings: Tuple[MarketDataMapping, ...] = None,
        vendor: Union[MarketDataVendor, str] = None,
        start_date: datetime.date = None,
        mdapi: MDAPI = None,
        data_product: str = None,
        entitlements: Entitlements = None,
        entitlement_exclusions: EntitlementExclusions = None,
        query_processors: ProcessorEntity = None,
        parameters: DataSetParameters = None,
        dimensions: DataSetDimensions = None,
        defaults: DataSetDefaults = None,
        filters: DataSetFilters = None,
        transformations: Tuple[DataSetTransformation, ...] = None,
        created_by_id: str = None,
        created_time: datetime.datetime = None,
        last_updated_by_id: str = None,
        last_updated_time: datetime.datetime = None,
        tags: Tuple[str, ...] = None
    ):        
        super().__init__()
        self.owner_id = owner_id
        self.__id = id_
        self.name = name
        self.description = description
        self.short_description = short_description
        self.mappings = mappings
        self.vendor = vendor
        self.start_date = start_date
        self.mdapi = mdapi
        self.data_product = data_product
        self.entitlements = entitlements
        self.entitlement_exclusions = entitlement_exclusions
        self.query_processors = query_processors
        self.parameters = parameters
        self.dimensions = dimensions
        self.defaults = defaults
        self.filters = filters
        self.transformations = transformations
        self.created_by_id = created_by_id
        self.created_time = created_time
        self.last_updated_by_id = last_updated_by_id
        self.last_updated_time = last_updated_time
        self.tags = tags

    @property
    def owner_id(self) -> str:
        """Marquee unique identifier for user who owns the object."""
        return self.__owner_id

    @owner_id.setter
    def owner_id(self, value: str):
        self._property_changed('owner_id')
        self.__owner_id = value        

    @property
    def id(self) -> str:
        """Unique id of dataset."""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

    @property
    def name(self) -> str:
        """Name of dataset."""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def description(self) -> str:
        """Description of dataset."""
        return self.__description

    @description.setter
    def description(self, value: str):
        self._property_changed('description')
        self.__description = value        

    @property
    def short_description(self) -> str:
        """Short description of dataset."""
        return self.__short_description

    @short_description.setter
    def short_description(self, value: str):
        self._property_changed('short_description')
        self.__short_description = value        

    @property
    def mappings(self) -> Tuple[MarketDataMapping, ...]:
        """Market data mappings."""
        return self.__mappings

    @mappings.setter
    def mappings(self, value: Tuple[MarketDataMapping, ...]):
        self._property_changed('mappings')
        self.__mappings = value        

    @property
    def vendor(self) -> Union[MarketDataVendor, str]:
        return self.__vendor

    @vendor.setter
    def vendor(self, value: Union[MarketDataVendor, str]):
        self._property_changed('vendor')
        self.__vendor = get_enum_value(MarketDataVendor, value)        

    @property
    def start_date(self) -> datetime.date:
        """The start of this data set"""
        return self.__start_date

    @start_date.setter
    def start_date(self, value: datetime.date):
        self._property_changed('start_date')
        self.__start_date = value        

    @property
    def mdapi(self) -> MDAPI:
        """Defines MDAPI fields."""
        return self.__mdapi

    @mdapi.setter
    def mdapi(self, value: MDAPI):
        self._property_changed('mdapi')
        self.__mdapi = value        

    @property
    def data_product(self) -> str:
        """Product that dataset belongs to."""
        return self.__data_product

    @data_product.setter
    def data_product(self, value: str):
        self._property_changed('data_product')
        self.__data_product = value        

    @property
    def entitlements(self) -> Entitlements:
        """Defines the entitlements of a given resource."""
        return self.__entitlements

    @entitlements.setter
    def entitlements(self, value: Entitlements):
        self._property_changed('entitlements')
        self.__entitlements = value        

    @property
    def entitlement_exclusions(self) -> EntitlementExclusions:
        """Defines the exclusion entitlements of a given resource."""
        return self.__entitlement_exclusions

    @entitlement_exclusions.setter
    def entitlement_exclusions(self, value: EntitlementExclusions):
        self._property_changed('entitlement_exclusions')
        self.__entitlement_exclusions = value        

    @property
    def query_processors(self) -> ProcessorEntity:
        """Query processors for dataset."""
        return self.__query_processors

    @query_processors.setter
    def query_processors(self, value: ProcessorEntity):
        self._property_changed('query_processors')
        self.__query_processors = value        

    @property
    def parameters(self) -> DataSetParameters:
        """Dataset parameters."""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: DataSetParameters):
        self._property_changed('parameters')
        self.__parameters = value        

    @property
    def dimensions(self) -> DataSetDimensions:
        """Dataset dimensions."""
        return self.__dimensions

    @dimensions.setter
    def dimensions(self, value: DataSetDimensions):
        self._property_changed('dimensions')
        self.__dimensions = value        

    @property
    def defaults(self) -> DataSetDefaults:
        """Default settings."""
        return self.__defaults

    @defaults.setter
    def defaults(self, value: DataSetDefaults):
        self._property_changed('defaults')
        self.__defaults = value        

    @property
    def filters(self) -> DataSetFilters:
        """Filters to restrict the set of data returned."""
        return self.__filters

    @filters.setter
    def filters(self, value: DataSetFilters):
        self._property_changed('filters')
        self.__filters = value        

    @property
    def transformations(self) -> Tuple[DataSetTransformation, ...]:
        return self.__transformations

    @transformations.setter
    def transformations(self, value: Tuple[DataSetTransformation, ...]):
        self._property_changed('transformations')
        self.__transformations = value        

    @property
    def created_by_id(self) -> str:
        """Unique identifier of user who created the object."""
        return self.__created_by_id

    @created_by_id.setter
    def created_by_id(self, value: str):
        self._property_changed('created_by_id')
        self.__created_by_id = value        

    @property
    def created_time(self) -> datetime.datetime:
        """Time created. ISO 8601 formatted string."""
        return self.__created_time

    @created_time.setter
    def created_time(self, value: datetime.datetime):
        self._property_changed('created_time')
        self.__created_time = value        

    @property
    def last_updated_by_id(self) -> str:
        """Unique identifier of user who last updated the object."""
        return self.__last_updated_by_id

    @last_updated_by_id.setter
    def last_updated_by_id(self, value: str):
        self._property_changed('last_updated_by_id')
        self.__last_updated_by_id = value        

    @property
    def last_updated_time(self) -> datetime.datetime:
        """Timestamp of when the object was last updated."""
        return self.__last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, value: datetime.datetime):
        self._property_changed('last_updated_time')
        self.__last_updated_time = value        

    @property
    def tags(self) -> Tuple[str, ...]:
        """Tags associated with dataset."""
        return self.__tags

    @tags.setter
    def tags(self, value: Tuple[str, ...]):
        self._property_changed('tags')
        self.__tags = value        
