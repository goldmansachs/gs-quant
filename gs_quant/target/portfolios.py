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

from gs_quant.common import *
import datetime
from typing import Mapping, Tuple, Union, Optional
from enum import Enum
from gs_quant.base import Base, EnumBase, InstrumentBase, camel_case_translate, get_enum_value


class ClientPositionFilter(EnumBase, Enum):    
    
    """Filter used to select client positions from GRDB. 'oeId' selects all positions
       associated with the provided oeId. 'oeIdOrClientAccounts' selects
       positions associated with their the provided oeId or ClientAccounts.
       'clientAccounts' selects positions only associated with those provided
       accounts."""

    oeId = 'oeId'
    clientAccounts = 'clientAccounts'
    oeIdOrClientAccounts = 'oeIdOrClientAccounts'    


class PortfolioType(EnumBase, Enum):    
    
    """Portfolio type differentiates the portfolio categorization"""

    Securities_Lending = 'Securities Lending'
    Draft_Portfolio = 'Draft Portfolio'
    Draft_Bond = 'Draft Bond'
    PCO_Portfolio = 'PCO Portfolio'
    PCO_Share_Class = 'PCO Share Class'    


class RiskAumSource(EnumBase, Enum):    
    
    """Source of AUM for portfolio risk calculations."""

    Gross = 'Gross'
    Long = 'Long'
    Short = 'Short'
    Custom_AUM = 'Custom AUM'
    Net = 'Net'    


class SecDbBookDetail(Base):
        
    """Details about SecDb Book"""

    @camel_case_translate
    def __init__(
        self,
        book_id: str = None,
        book_type: str = None,
        name: str = None
    ):        
        super().__init__()
        self.book_id = book_id
        self.book_type = book_type
        self.name = name

    @property
    def book_id(self) -> str:
        """Book Id"""
        return self.__book_id

    @book_id.setter
    def book_id(self, value: str):
        self._property_changed('book_id')
        self.__book_id = value        

    @property
    def book_type(self) -> str:
        return self.__book_type

    @book_type.setter
    def book_type(self, value: str):
        self._property_changed('book_type')
        self.__book_type = value        


class GRDBPortfolioParameters(Base):
        
    """Parameters required for a GRDB portfolio."""

    _name_mappings = {'oasis_account_names': 'OasisAccountNames'}

    @camel_case_translate
    def __init__(
        self,
        oe_id: str,
        client_name: str,
        increment: str,
        risk_packages: Tuple[str, ...],
        enabled: str,
        is_live: str,
        client_account_names: Tuple[str, ...] = None,
        oasis_account_names: Tuple[str, ...] = None,
        client_position_filter: Union[ClientPositionFilter, str] = None,
        name: str = None
    ):        
        super().__init__()
        self.oe_id = oe_id
        self.client_name = client_name
        self.client_account_names = client_account_names
        self.oasis_account_names = oasis_account_names
        self.client_position_filter = client_position_filter
        self.increment = increment
        self.risk_packages = risk_packages
        self.enabled = enabled
        self.is_live = is_live
        self.name = name

    @property
    def oe_id(self) -> str:
        """Marquee unique identifier"""
        return self.__oe_id

    @oe_id.setter
    def oe_id(self, value: str):
        self._property_changed('oe_id')
        self.__oe_id = value        

    @property
    def client_name(self) -> str:
        """Client's name or user-friendly identifier"""
        return self.__client_name

    @client_name.setter
    def client_name(self, value: str):
        self._property_changed('client_name')
        self.__client_name = value        

    @property
    def client_account_names(self) -> Tuple[str, ...]:
        """List of SecDB Customer Book Names"""
        return self.__client_account_names

    @client_account_names.setter
    def client_account_names(self, value: Tuple[str, ...]):
        self._property_changed('client_account_names')
        self.__client_account_names = value        

    @property
    def oasis_account_names(self) -> Tuple[str, ...]:
        """List of OASIS Accounts"""
        return self.__oasis_account_names

    @oasis_account_names.setter
    def oasis_account_names(self, value: Tuple[str, ...]):
        self._property_changed('oasis_account_names')
        self.__oasis_account_names = value        

    @property
    def client_position_filter(self) -> Union[ClientPositionFilter, str]:
        """Filter used to select client positions from GRDB. 'oeId' selects all positions
           associated with the provided oeId. 'oeIdOrClientAccounts' selects
           positions associated with their the provided oeId or ClientAccounts.
           'clientAccounts' selects positions only associated with those
           provided accounts."""
        return self.__client_position_filter

    @client_position_filter.setter
    def client_position_filter(self, value: Union[ClientPositionFilter, str]):
        self._property_changed('client_position_filter')
        self.__client_position_filter = get_enum_value(ClientPositionFilter, value)        

    @property
    def increment(self) -> str:
        """Generated Unique three character string"""
        return self.__increment

    @increment.setter
    def increment(self, value: str):
        self._property_changed('increment')
        self.__increment = value        

    @property
    def risk_packages(self) -> Tuple[str, ...]:
        """Metadata associated with the object. Provide an array of strings which will be
           indexed for search and locating related objects"""
        return self.__risk_packages

    @risk_packages.setter
    def risk_packages(self, value: Tuple[str, ...]):
        self._property_changed('risk_packages')
        self.__risk_packages = value        

    @property
    def enabled(self) -> str:
        """Gives information on whether risks are run for the portfolio"""
        return self.__enabled

    @enabled.setter
    def enabled(self, value: str):
        self._property_changed('enabled')
        self.__enabled = value        

    @property
    def is_live(self) -> str:
        """Gives information on whether alerts are enabled for the portfolio"""
        return self.__is_live

    @is_live.setter
    def is_live(self, value: str):
        self._property_changed('is_live')
        self.__is_live = value        


class PCOTrade(Base):
        
    """Parameters required for a PCO Trade"""

    @camel_case_translate
    def __init__(
        self,
        fill_rate: str = None,
        include_in_hedge: bool = None,
        settlement_date: datetime.date = None,
        spot_ref: str = None,
        notes: str = None,
        creation_date: datetime.date = None,
        base_currency: Union[Currency, str] = None,
        quote_currency: Union[Currency, str] = None,
        base_currency_notional: str = None,
        quote_currency_notional: str = None,
        trade_date: datetime.date = None,
        fixing_ref: str = None,
        side: str = None,
        name: str = None
    ):        
        super().__init__()
        self.fill_rate = fill_rate
        self.include_in_hedge = include_in_hedge
        self.settlement_date = settlement_date
        self.spot_ref = spot_ref
        self.notes = notes
        self.creation_date = creation_date
        self.base_currency = base_currency
        self.quote_currency = quote_currency
        self.base_currency_notional = base_currency_notional
        self.quote_currency_notional = quote_currency_notional
        self.trade_date = trade_date
        self.fixing_ref = fixing_ref
        self.side = side
        self.name = name

    @property
    def fill_rate(self) -> str:
        """Fill rate"""
        return self.__fill_rate

    @fill_rate.setter
    def fill_rate(self, value: str):
        self._property_changed('fill_rate')
        self.__fill_rate = value        

    @property
    def include_in_hedge(self) -> bool:
        """Include trade in hedge"""
        return self.__include_in_hedge

    @include_in_hedge.setter
    def include_in_hedge(self, value: bool):
        self._property_changed('include_in_hedge')
        self.__include_in_hedge = value        

    @property
    def settlement_date(self) -> datetime.date:
        """Settlement date"""
        return self.__settlement_date

    @settlement_date.setter
    def settlement_date(self, value: datetime.date):
        self._property_changed('settlement_date')
        self.__settlement_date = value        

    @property
    def spot_ref(self) -> str:
        """Spot ref"""
        return self.__spot_ref

    @spot_ref.setter
    def spot_ref(self, value: str):
        self._property_changed('spot_ref')
        self.__spot_ref = value        

    @property
    def notes(self) -> str:
        """Notes"""
        return self.__notes

    @notes.setter
    def notes(self, value: str):
        self._property_changed('notes')
        self.__notes = value        

    @property
    def creation_date(self) -> datetime.date:
        """Creation date."""
        return self.__creation_date

    @creation_date.setter
    def creation_date(self, value: datetime.date):
        self._property_changed('creation_date')
        self.__creation_date = value        

    @property
    def base_currency(self) -> Union[Currency, str]:
        """Base currency"""
        return self.__base_currency

    @base_currency.setter
    def base_currency(self, value: Union[Currency, str]):
        self._property_changed('base_currency')
        self.__base_currency = get_enum_value(Currency, value)        

    @property
    def quote_currency(self) -> Union[Currency, str]:
        """Quote currency"""
        return self.__quote_currency

    @quote_currency.setter
    def quote_currency(self, value: Union[Currency, str]):
        self._property_changed('quote_currency')
        self.__quote_currency = get_enum_value(Currency, value)        

    @property
    def base_currency_notional(self) -> str:
        """Base currency notional"""
        return self.__base_currency_notional

    @base_currency_notional.setter
    def base_currency_notional(self, value: str):
        self._property_changed('base_currency_notional')
        self.__base_currency_notional = value        

    @property
    def quote_currency_notional(self) -> str:
        """Quote currency notional"""
        return self.__quote_currency_notional

    @quote_currency_notional.setter
    def quote_currency_notional(self, value: str):
        self._property_changed('quote_currency_notional')
        self.__quote_currency_notional = value        

    @property
    def trade_date(self) -> datetime.date:
        """Trade date."""
        return self.__trade_date

    @trade_date.setter
    def trade_date(self, value: datetime.date):
        self._property_changed('trade_date')
        self.__trade_date = value        

    @property
    def fixing_ref(self) -> str:
        """Fixing ref"""
        return self.__fixing_ref

    @fixing_ref.setter
    def fixing_ref(self, value: str):
        self._property_changed('fixing_ref')
        self.__fixing_ref = value        

    @property
    def side(self) -> str:
        """side"""
        return self.__side

    @side.setter
    def side(self, value: str):
        self._property_changed('side')
        self.__side = value        


class PCOPortfolioParameters(Base):
        
    """Parameters required for a PCO Portfolio"""

    _name_mappings = {'enable_rfq': 'enableRFQ'}

    @camel_case_translate
    def __init__(
        self,
        base_currency: Union[Currency, str] = None,
        local_currency: Union[Currency, str] = None,
        fund_calendar: str = None,
        calculation_currency: Union[PCOCurrencyType, str] = None,
        hedge_settlement_interval: Tuple[PCOParameterValues, ...] = None,
        hedge_settlement_day: Tuple[PCOParameterValues, ...] = None,
        roll_horizon: Tuple[PCOParameterValues, ...] = None,
        pnl_currency: Tuple[PCOParameterValues, ...] = None,
        nav_publication_period: Tuple[PCOParameterValues, ...] = None,
        roll_date_zero_threshold: bool = None,
        unrealised_mark_to_market: PCOUnrealisedMarkToMarket = None,
        target_deviation: Tuple[PCOTargetDeviation, ...] = None,
        cash_balances: Tuple[PCOCashBalance, ...] = None,
        exposure: PCOExposure = None,
        pco_share_class: PCOShareClass = None,
        settlements: Tuple[PCOSettlements, ...] = None,
        show_cash: bool = None,
        show_exposure: bool = None,
        enable_rfq: bool = None,
        fixing_descriptions: Tuple[str, ...] = None,
        pco_origin: str = None,
        version: str = None,
        trades: Tuple[PCOTrade, ...] = None,
        investment_ratio: str = None,
        name: str = None
    ):        
        super().__init__()
        self.base_currency = base_currency
        self.local_currency = local_currency
        self.fund_calendar = fund_calendar
        self.calculation_currency = calculation_currency
        self.hedge_settlement_interval = hedge_settlement_interval
        self.hedge_settlement_day = hedge_settlement_day
        self.roll_horizon = roll_horizon
        self.pnl_currency = pnl_currency
        self.nav_publication_period = nav_publication_period
        self.roll_date_zero_threshold = roll_date_zero_threshold
        self.unrealised_mark_to_market = unrealised_mark_to_market
        self.target_deviation = target_deviation
        self.cash_balances = cash_balances
        self.exposure = exposure
        self.pco_share_class = pco_share_class
        self.settlements = settlements
        self.show_cash = show_cash
        self.show_exposure = show_exposure
        self.enable_rfq = enable_rfq
        self.fixing_descriptions = fixing_descriptions
        self.pco_origin = pco_origin
        self.version = version
        self.trades = trades
        self.investment_ratio = investment_ratio
        self.name = name

    @property
    def base_currency(self) -> Union[Currency, str]:
        """Base currency"""
        return self.__base_currency

    @base_currency.setter
    def base_currency(self, value: Union[Currency, str]):
        self._property_changed('base_currency')
        self.__base_currency = get_enum_value(Currency, value)        

    @property
    def local_currency(self) -> Union[Currency, str]:
        """Local currency"""
        return self.__local_currency

    @local_currency.setter
    def local_currency(self, value: Union[Currency, str]):
        self._property_changed('local_currency')
        self.__local_currency = get_enum_value(Currency, value)        

    @property
    def fund_calendar(self) -> str:
        """Holiday Calendar of Fund"""
        return self.__fund_calendar

    @fund_calendar.setter
    def fund_calendar(self, value: str):
        self._property_changed('fund_calendar')
        self.__fund_calendar = value        

    @property
    def calculation_currency(self) -> Union[PCOCurrencyType, str]:
        """Calculation currency type"""
        return self.__calculation_currency

    @calculation_currency.setter
    def calculation_currency(self, value: Union[PCOCurrencyType, str]):
        self._property_changed('calculation_currency')
        self.__calculation_currency = get_enum_value(PCOCurrencyType, value)        

    @property
    def hedge_settlement_interval(self) -> Tuple[PCOParameterValues, ...]:
        """Default tenor of hedging for each currency"""
        return self.__hedge_settlement_interval

    @hedge_settlement_interval.setter
    def hedge_settlement_interval(self, value: Tuple[PCOParameterValues, ...]):
        self._property_changed('hedge_settlement_interval')
        self.__hedge_settlement_interval = value        

    @property
    def hedge_settlement_day(self) -> Tuple[PCOParameterValues, ...]:
        """Settlement date of each currency"""
        return self.__hedge_settlement_day

    @hedge_settlement_day.setter
    def hedge_settlement_day(self, value: Tuple[PCOParameterValues, ...]):
        self._property_changed('hedge_settlement_day')
        self.__hedge_settlement_day = value        

    @property
    def roll_horizon(self) -> Tuple[PCOParameterValues, ...]:
        """Number of days to roll before settlement for each currency"""
        return self.__roll_horizon

    @roll_horizon.setter
    def roll_horizon(self, value: Tuple[PCOParameterValues, ...]):
        self._property_changed('roll_horizon')
        self.__roll_horizon = value        

    @property
    def pnl_currency(self) -> Tuple[PCOParameterValues, ...]:
        """One of Local and Base"""
        return self.__pnl_currency

    @pnl_currency.setter
    def pnl_currency(self, value: Tuple[PCOParameterValues, ...]):
        self._property_changed('pnl_currency')
        self.__pnl_currency = value        

    @property
    def nav_publication_period(self) -> Tuple[PCOParameterValues, ...]:
        """Days it takes for a subscription or redemption show up in NAV after it happens"""
        return self.__nav_publication_period

    @nav_publication_period.setter
    def nav_publication_period(self, value: Tuple[PCOParameterValues, ...]):
        self._property_changed('nav_publication_period')
        self.__nav_publication_period = value        

    @property
    def roll_date_zero_threshold(self) -> bool:
        """If true, rebalance this program when rolling"""
        return self.__roll_date_zero_threshold

    @roll_date_zero_threshold.setter
    def roll_date_zero_threshold(self, value: bool):
        self._property_changed('roll_date_zero_threshold')
        self.__roll_date_zero_threshold = value        

    @property
    def unrealised_mark_to_market(self) -> PCOUnrealisedMarkToMarket:
        """History of unrealised mark to market of open trades for each currency"""
        return self.__unrealised_mark_to_market

    @unrealised_mark_to_market.setter
    def unrealised_mark_to_market(self, value: PCOUnrealisedMarkToMarket):
        self._property_changed('unrealised_mark_to_market')
        self.__unrealised_mark_to_market = value        

    @property
    def target_deviation(self) -> Tuple[PCOTargetDeviation, ...]:
        """History of target deviation for each currency"""
        return self.__target_deviation

    @target_deviation.setter
    def target_deviation(self, value: Tuple[PCOTargetDeviation, ...]):
        self._property_changed('target_deviation')
        self.__target_deviation = value        

    @property
    def cash_balances(self) -> Tuple[PCOCashBalance, ...]:
        """Cash flows for each currency"""
        return self.__cash_balances

    @cash_balances.setter
    def cash_balances(self, value: Tuple[PCOCashBalance, ...]):
        self._property_changed('cash_balances')
        self.__cash_balances = value        

    @property
    def exposure(self) -> PCOExposure:
        """Total exposure for portfolio"""
        return self.__exposure

    @exposure.setter
    def exposure(self, value: PCOExposure):
        self._property_changed('exposure')
        self.__exposure = value        

    @property
    def pco_share_class(self) -> PCOShareClass:
        """Data for a PCO share class"""
        return self.__pco_share_class

    @pco_share_class.setter
    def pco_share_class(self, value: PCOShareClass):
        self._property_changed('pco_share_class')
        self.__pco_share_class = value        

    @property
    def settlements(self) -> Tuple[PCOSettlements, ...]:
        """History of settlements for each currency"""
        return self.__settlements

    @settlements.setter
    def settlements(self, value: Tuple[PCOSettlements, ...]):
        self._property_changed('settlements')
        self.__settlements = value        

    @property
    def show_cash(self) -> bool:
        """If cash table is shown in UI"""
        return self.__show_cash

    @show_cash.setter
    def show_cash(self, value: bool):
        self._property_changed('show_cash')
        self.__show_cash = value        

    @property
    def show_exposure(self) -> bool:
        """If exposure table is shown in UI"""
        return self.__show_exposure

    @show_exposure.setter
    def show_exposure(self, value: bool):
        self._property_changed('show_exposure')
        self.__show_exposure = value        

    @property
    def enable_rfq(self) -> bool:
        """If RFQ is enabled for the program"""
        return self.__enable_rfq

    @enable_rfq.setter
    def enable_rfq(self, value: bool):
        self._property_changed('enable_rfq')
        self.__enable_rfq = value        

    @property
    def fixing_descriptions(self) -> Tuple[str, ...]:
        """List of available fixing for this program"""
        return self.__fixing_descriptions

    @fixing_descriptions.setter
    def fixing_descriptions(self, value: Tuple[str, ...]):
        self._property_changed('fixing_descriptions')
        self.__fixing_descriptions = value        

    @property
    def pco_origin(self) -> str:
        """Origin of PCO Report"""
        return self.__pco_origin

    @pco_origin.setter
    def pco_origin(self, value: str):
        self._property_changed('pco_origin')
        self.__pco_origin = value        

    @property
    def version(self) -> str:
        """Version"""
        return self.__version

    @version.setter
    def version(self, value: str):
        self._property_changed('version')
        self.__version = value        

    @property
    def trades(self) -> Tuple[PCOTrade, ...]:
        """Array of PCO trades"""
        return self.__trades

    @trades.setter
    def trades(self, value: Tuple[PCOTrade, ...]):
        self._property_changed('trades')
        self.__trades = value        

    @property
    def investment_ratio(self) -> str:
        """Investment ratio"""
        return self.__investment_ratio

    @investment_ratio.setter
    def investment_ratio(self, value: str):
        self._property_changed('investment_ratio')
        self.__investment_ratio = value        


class Portfolio(Base):
        
    @camel_case_translate
    def __init__(
        self,
        currency: Union[Currency, str],
        name: str,
        id_: str = None,
        created_by_id: str = None,
        created_time: datetime.datetime = None,
        description: str = None,
        entitlements: Entitlements = None,
        entitlement_exclusions: EntitlementExclusions = None,
        identifiers: Tuple[Identifier, ...] = None,
        last_updated_by_id: str = None,
        last_updated_time: datetime.datetime = None,
        owner_id: str = None,
        report_ids: Tuple[str, ...] = None,
        short_name: str = None,
        underlying_portfolio_ids: Tuple[str, ...] = None,
        tags: Tuple[str, ...] = None,
        type_: Union[PortfolioType, str] = None,
        parameters: dict = None,
        aum_source: Union[RiskAumSource, str] = None
    ):        
        super().__init__()
        self.__id = id_
        self.created_by_id = created_by_id
        self.created_time = created_time
        self.currency = currency
        self.description = description
        self.entitlements = entitlements
        self.entitlement_exclusions = entitlement_exclusions
        self.identifiers = identifiers
        self.last_updated_by_id = last_updated_by_id
        self.last_updated_time = last_updated_time
        self.name = name
        self.owner_id = owner_id
        self.report_ids = report_ids
        self.short_name = short_name
        self.underlying_portfolio_ids = underlying_portfolio_ids
        self.tags = tags
        self.__type = get_enum_value(PortfolioType, type_)
        self.parameters = parameters
        self.aum_source = aum_source

    @property
    def id(self) -> str:
        """Marquee unique portfolio identifier"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self._property_changed('id')
        self.__id = value        

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
    def currency(self) -> Union[Currency, str]:
        """Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP vs GBp)"""
        return self.__currency

    @currency.setter
    def currency(self, value: Union[Currency, str]):
        self._property_changed('currency')
        self.__currency = get_enum_value(Currency, value)        

    @property
    def description(self) -> str:
        """Free text description of portfolio. Description provided will be indexed in the
           search service for free text relevance match"""
        return self.__description

    @description.setter
    def description(self, value: str):
        self._property_changed('description')
        self.__description = value        

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
    def identifiers(self) -> Tuple[Identifier, ...]:
        """Array of identifier objects which can be used to locate this item in searches
           and other services"""
        return self.__identifiers

    @identifiers.setter
    def identifiers(self, value: Tuple[Identifier, ...]):
        self._property_changed('identifiers')
        self.__identifiers = value        

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
    def name(self) -> str:
        """Display name of the portfolio"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self._property_changed('name')
        self.__name = value        

    @property
    def owner_id(self) -> str:
        """Marquee unique identifier for user who owns the object."""
        return self.__owner_id

    @owner_id.setter
    def owner_id(self, value: str):
        self._property_changed('owner_id')
        self.__owner_id = value        

    @property
    def report_ids(self) -> Tuple[str, ...]:
        """Array of report identifiers related to the object"""
        return self.__report_ids

    @report_ids.setter
    def report_ids(self, value: Tuple[str, ...]):
        self._property_changed('report_ids')
        self.__report_ids = value        

    @property
    def short_name(self) -> str:
        """Short name or alias for the portfolio"""
        return self.__short_name

    @short_name.setter
    def short_name(self, value: str):
        self._property_changed('short_name')
        self.__short_name = value        

    @property
    def underlying_portfolio_ids(self) -> Tuple[str, ...]:
        """Underlying portfolio Ids"""
        return self.__underlying_portfolio_ids

    @underlying_portfolio_ids.setter
    def underlying_portfolio_ids(self, value: Tuple[str, ...]):
        self._property_changed('underlying_portfolio_ids')
        self.__underlying_portfolio_ids = value        

    @property
    def tags(self) -> Tuple[str, ...]:
        """Metadata associated with the object. Provide an array of strings which will be
           indexed for search and locating related objects"""
        return self.__tags

    @tags.setter
    def tags(self, value: Tuple[str, ...]):
        self._property_changed('tags')
        self.__tags = value        

    @property
    def type(self) -> Union[PortfolioType, str]:
        """Portfolio type differentiates the portfolio categorization"""
        return self.__type

    @type.setter
    def type(self, value: Union[PortfolioType, str]):
        self._property_changed('type')
        self.__type = get_enum_value(PortfolioType, value)        

    @property
    def parameters(self) -> dict:
        return self.__parameters

    @parameters.setter
    def parameters(self, value: dict):
        self._property_changed('parameters')
        self.__parameters = value        

    @property
    def aum_source(self) -> Union[RiskAumSource, str]:
        """AUM to be considered in all portfolio calculations."""
        return self.__aum_source

    @aum_source.setter
    def aum_source(self, value: Union[RiskAumSource, str]):
        self._property_changed('aum_source')
        self.__aum_source = get_enum_value(RiskAumSource, value)        
