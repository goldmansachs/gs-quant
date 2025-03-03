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
import datetime as dt
import logging
from collections import defaultdict
from enum import Enum
from typing import Union, List, Dict, Optional

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta

from gs_quant.api.gs.assets import GsAssetApi
from gs_quant.api.gs.hedges import GsHedgeApi
from gs_quant.errors import MqValueError
from gs_quant.markets.position_set import PositionSet
from gs_quant.session import GsSession
from gs_quant.target.hedge import HedgeObjective, CorporateActionsTypes

_logger = logging.getLogger(__name__)


class FactorExposureCategory(Enum):
    COUNTRY = 'country'
    SECTOR = 'sector'
    INDUSTRY = 'industry'
    STYLE = 'style'


class ConstraintType(Enum):
    ASSET = "Asset"
    COUNTRY = "Country"
    REGION = "Region"
    SECTOR = "Sector"
    INDUSTRY = "Industry"
    ESG = "Esg"


class HedgeExclusions:
    """
    List of assets, countries, regions, sectors, and industries to exclude from the hedge universe
    """

    def __init__(self,
                 assets: List[str] = None,
                 countries: List[str] = None,
                 regions: List[str] = None,
                 sectors: List[str] = None,
                 industries: List[str] = None):
        self.__assets = assets
        self.__countries = countries
        self.__regions = regions
        self.__sectors = sectors
        self.__industries = industries

    @property
    def assets(self) -> List[str]:
        return self.__assets

    @assets.setter
    def assets(self, value: List[str]):
        self.__assets = value

    @property
    def countries(self) -> List[str]:
        return self.__countries

    @countries.setter
    def countries(self, value: List[str]):
        self.__countries = value

    @property
    def regions(self) -> List[str]:
        return self.__regions

    @regions.setter
    def regions(self, value: List[str]):
        self.__regions = value

    @property
    def sectors(self) -> List[str]:
        return self.__sectors

    @sectors.setter
    def sectors(self, value: List[str]):
        self.__sectors = value

    @property
    def industries(self) -> List[str]:
        return self.__industries

    @industries.setter
    def industries(self, value: List[str]):
        self.__industries = value

    def to_dict(self):
        response = {}
        all_constraints = []
        if self.countries:
            all_constraints = all_constraints + self._get_exclusions(self.countries, ConstraintType.COUNTRY)
        if self.regions:
            all_constraints = all_constraints + self._get_exclusions(self.regions, ConstraintType.REGION)
        if self.sectors:
            all_constraints = all_constraints + self._get_exclusions(self.sectors, ConstraintType.SECTOR)
        if self.industries:
            all_constraints = all_constraints + self._get_exclusions(self.industries, ConstraintType.INDUSTRY)
        if len(all_constraints) > 0:
            response['classificationConstraints'] = all_constraints
        if self.assets:
            response['assetConstraints'] = self._get_exclusions(self.assets, ConstraintType.ASSET)
        return response

    @staticmethod
    def _get_exclusions(exclusions_list: List, constraint_type: ConstraintType):
        return [Constraint(constraint_name=exclusion,
                           constraint_type=constraint_type,
                           minimum=0,
                           maximum=0).to_dict() for exclusion in exclusions_list]


class Constraint:

    def __init__(self,
                 constraint_name: str,
                 minimum: float = 0,
                 maximum: float = 100,
                 constraint_type: Optional[ConstraintType] = None):
        self.__constraint_name = constraint_name
        self.__minimum = minimum
        self.__maximum = maximum
        self.__constraint_type = constraint_type

    @property
    def constraint_name(self) -> str:
        return self.__constraint_name

    @constraint_name.setter
    def constraint_name(self, value: str):
        self.__constraint_name = value

    @property
    def minimum(self) -> float:
        return self.__minimum

    @minimum.setter
    def minimum(self, value: float):
        self.__minimum = value

    @property
    def maximum(self) -> float:
        return self.__maximum

    @maximum.setter
    def maximum(self, value: float):
        self.__maximum = value

    @property
    def constraint_type(self) -> Optional[ConstraintType]:
        return self.__constraint_type

    @constraint_type.setter
    def constraint_type(self, value: ConstraintType):
        self.__constraint_type = value

    @classmethod
    def from_dict(cls, as_dict: Dict):
        if as_dict.get('type') is not None:
            constraint_type = ConstraintType(as_dict.get('type'))
        elif as_dict.get('assetId') is not None:
            constraint_type = ConstraintType.ASSET
        else:
            constraint_type = ConstraintType.ESG
        return Constraint(constraint_name=as_dict.get('name') or as_dict.get('assetId'),
                          constraint_type=constraint_type,
                          minimum=as_dict.get('min'),
                          maximum=as_dict.get('max'))

    def to_dict(self):
        response = {
            'name': self.constraint_name,
            'min': self.minimum,
            'max': self.maximum
        }
        if self.constraint_type != ConstraintType.ESG and self.constraint_type != ConstraintType.ASSET:
            response['type'] = self.constraint_type.value
        if self.constraint_type == ConstraintType.ASSET:
            response['assetId'] = response['name']
            response.pop('name')

        return response


class HedgeConstraints:
    """
    List of assets, countries, sectors, and industries to constrain in the hedge universe
    """

    def __init__(self,
                 assets: List[Constraint] = None,
                 countries: List[Constraint] = None,
                 regions: List[Constraint] = None,
                 sectors: List[Constraint] = None,
                 industries: List[Constraint] = None,
                 esg: List[Constraint] = None):
        for con in assets or []:
            con.constraint_type = ConstraintType.ASSET
        for con in regions or []:
            con.constraint_type = ConstraintType.REGION
        for con in countries or []:
            con.constraint_type = ConstraintType.COUNTRY
        for con in sectors or []:
            con.constraint_type = ConstraintType.SECTOR
        for con in industries or []:
            con.constraint_type = ConstraintType.INDUSTRY
        for con in esg or []:
            con.constraint_type = ConstraintType.ESG
        self.__assets = assets
        self.__countries = countries
        self.__regions = regions
        self.__sectors = sectors
        self.__industries = industries
        self.__esg = esg

    @property
    def assets(self) -> List[Constraint]:
        return self.__assets

    @assets.setter
    def assets(self, value: List[Constraint]):
        self.__assets = value

    @property
    def countries(self) -> List[Constraint]:
        return self.__countries

    @countries.setter
    def countries(self, value: List[Constraint]):
        self.__countries = value

    @property
    def regions(self) -> List[Constraint]:
        return self.__regions

    @regions.setter
    def regions(self, value: List[Constraint]):
        self.__regions = value

    @property
    def sectors(self) -> List[Constraint]:
        return self.__sectors

    @sectors.setter
    def sectors(self, value: List[Constraint]):
        self.__sectors = value

    @property
    def industries(self) -> List[Constraint]:
        return self.__industries

    @industries.setter
    def industries(self, value: List[Constraint]):
        self.__industries = value

    @property
    def esg(self) -> List[Constraint]:
        return self.__esg

    @esg.setter
    def esg(self, value: List[Constraint]):
        self.__esg = value

    def to_dict(self):
        response = {}

        classification_constraints = []
        for constraint_type in [self.countries, self.regions, self.sectors, self.industries]:
            if constraint_type:
                classification_constraints += [con.to_dict() for con in constraint_type]
        if len(classification_constraints) > 0:
            response['classificationConstraints'] = classification_constraints

        esg_constraints = [con.to_dict() for con in self.esg] if self.esg else []
        if len(esg_constraints) > 0:
            response['esgConstraints'] = esg_constraints

        asset_constraints = [con.to_dict() for con in self.assets] if self.assets else []
        if len(asset_constraints) > 0:
            response['assetConstraints'] = asset_constraints

        return response


class PerformanceHedgeParameters:
    """Parameters for a performance replication hedge calculation."""

    def __init__(
            self,
            initial_portfolio: PositionSet,
            universe: List[str],
            exclusions: Optional[HedgeExclusions] = None,
            constraints: Optional[HedgeConstraints] = None,
            observation_start_date: dt.date = None,
            sampling_period: str = 'Daily',
            max_leverage: float = 100,
            percentage_in_cash: Optional[float] = None,
            explode_universe: bool = True,
            exclude_target_assets: bool = True,
            exclude_corporate_actions_types: Optional[List[Union[CorporateActionsTypes, str]]] = None,
            exclude_hard_to_borrow_assets: bool = False,
            exclude_restricted_assets: bool = False,
            max_adv_percentage: float = 15,
            max_return_deviation: float = 5,
            max_weight: float = 100,
            min_market_cap: Optional[float] = None,
            max_market_cap: Optional[float] = None,
            market_participation_rate: float = 10,
            lasso_weight: float = 0,
            ridge_weight: float = 0,
            benchmarks: List[str] = None):
        self.__initial_portfolio = initial_portfolio
        self.__universe = universe
        self.__exclusions = exclusions
        self.__constraints = constraints
        self.__observation_start_date = observation_start_date
        self.__sampling_period = sampling_period
        self.__max_leverage = max_leverage
        self.__percentage_in_cash = percentage_in_cash
        self.__explode_universe = explode_universe
        self.__exclude_target_assets = exclude_target_assets
        self.__exclude_corporate_actions_types = exclude_corporate_actions_types
        self.__exclude_hard_to_borrow_assets = exclude_hard_to_borrow_assets
        self.__exclude_restricted_assets = exclude_restricted_assets
        self.__max_adv_percentage = max_adv_percentage
        self.__max_return_deviation = max_return_deviation
        self.__max_weight = max_weight
        self.__min_market_cap = min_market_cap
        self.__max_market_cap = max_market_cap
        self.__market_participation_rate = market_participation_rate
        self.__lasso_weight = lasso_weight
        self.__ridge_weight = ridge_weight
        self.__benchmarks = benchmarks

    @property
    def initial_portfolio(self) -> PositionSet:
        """The set of positions that make up the hedge target."""
        return self.__initial_portfolio

    @initial_portfolio.setter
    def initial_portfolio(self, value: PositionSet):
        self.__initial_portfolio = value

    @property
    def universe(self) -> List[str]:
        """A list of asset identifiers (asset IDs, bloomberg IDs, tickers, SEDOLs, etc) that make up the universe,
        which are resolved as of the observation end date."""
        return self.__universe

    @universe.setter
    def universe(self, value: List[str]):
        self.__universe = value

    @property
    def observation_start_date(self) -> dt.date:
        """ISO 8601-formatted date"""
        return self.__observation_start_date

    @observation_start_date.setter
    def observation_start_date(self, value: dt.date):
        self.__observation_start_date = value

    @property
    def exclusions(self) -> Optional[HedgeExclusions]:
        """Assets, countries, sectors, and industries to exclude from the hedge"""
        return self.__exclusions

    @exclusions.setter
    def exclusions(self, value: HedgeExclusions):
        self.__exclusions = value

    @property
    def constraints(self) -> Optional[HedgeConstraints]:
        """Assets, countries, sectors, and industries to constrain in the hedge"""
        return self.__constraints

    @constraints.setter
    def constraints(self, value: HedgeConstraints):
        self.__constraints = value

    @property
    def sampling_period(self) -> str:
        """The length of time in between return samples."""
        return self.__sampling_period

    @sampling_period.setter
    def sampling_period(self, value: str):
        self.__sampling_period = value

    @property
    def max_leverage(self) -> float:
        """Maximum percentage of the notional that can be used to hedge."""
        return self.__max_leverage

    @max_leverage.setter
    def max_leverage(self, value: float):
        self.__max_leverage = value

    @property
    def percentage_in_cash(self) -> Optional[float]:
        """Percentage of the hedge notional that will be in cash."""
        return self.__percentage_in_cash

    @percentage_in_cash.setter
    def percentage_in_cash(self, value: float):
        self.__percentage_in_cash = value

    @property
    def explode_universe(self) -> bool:
        """Explode the assets in the universe into their underliers to be used as the hedge
           universe."""
        return self.__explode_universe

    @explode_universe.setter
    def explode_universe(self, value: bool):
        self.__explode_universe = value

    @property
    def exclude_target_assets(self) -> bool:
        """Exclude assets in the target composition from being in the hedge."""
        return self.__exclude_target_assets

    @exclude_target_assets.setter
    def exclude_target_assets(self, value: bool):
        self.__exclude_target_assets = value

    @property
    def exclude_corporate_actions_types(self) -> Optional[List[Union[CorporateActionsTypes, str]]]:
        """Set of of corporate actions to be excluded in the hedge"""
        return self.__exclude_corporate_actions_types

    @exclude_corporate_actions_types.setter
    def exclude_corporate_actions_types(self, value: List[Union[CorporateActionsTypes, str]]):
        self.__exclude_corporate_actions_types = value

    @property
    def exclude_hard_to_borrow_assets(self) -> bool:
        """Whether hard to borrow assets should be excluded in the universe or not. True
           for exclude."""
        return self.__exclude_hard_to_borrow_assets

    @exclude_hard_to_borrow_assets.setter
    def exclude_hard_to_borrow_assets(self, value: bool):
        self.__exclude_hard_to_borrow_assets = value

    @property
    def exclude_restricted_assets(self) -> bool:
        """Whether to include assets in restricted trading lists or not."""
        return self.__exclude_restricted_assets

    @exclude_restricted_assets.setter
    def exclude_restricted_assets(self, value: bool):
        self.__exclude_restricted_assets = value

    @property
    def max_adv_percentage(self) -> float:
        """Maximum percentage notional to average daily dollar volume allowed for any hedge
           constituent."""
        return self.__max_adv_percentage

    @max_adv_percentage.setter
    def max_adv_percentage(self, value: float):
        self.__max_adv_percentage = value

    @property
    def max_return_deviation(self) -> float:
        """Maximum percentage difference in annualized return between the target and the
           hedge result."""
        return self.__max_return_deviation

    @max_return_deviation.setter
    def max_return_deviation(self, value: float):
        self.__max_return_deviation = value

    @property
    def max_weight(self) -> float:
        """Maximum weight of any constituent in hedge."""
        return self.__max_weight

    @max_weight.setter
    def max_weight(self, value: float):
        self.__max_weight = value

    @property
    def min_market_cap(self) -> Optional[float]:
        """Lowest market cap allowed for any hedge constituent."""
        return self.__min_market_cap

    @min_market_cap.setter
    def min_market_cap(self, value: float):
        self.__min_market_cap = value

    @property
    def max_market_cap(self) -> Optional[float]:
        """Highest market cap allowed for any hedge constituent."""
        return self.__max_market_cap

    @max_market_cap.setter
    def max_market_cap(self, value: float):
        self.__max_market_cap = value

    @property
    def market_participation_rate(self) -> float:
        """Maximum market participation rate used to estimate the cost of trading a
           portfolio of stocks. This does not effect the optimization."""
        return self.__market_participation_rate

    @market_participation_rate.setter
    def market_participation_rate(self, value: float):
        self.__market_participation_rate = value

    @property
    def benchmarks(self) -> List[str]:
        """Marquee unique identifiers of assets to be used as benchmarks."""
        return self.__benchmarks

    @benchmarks.setter
    def benchmarks(self, value: List[str]):
        self.__benchmarks = value

    @property
    def lasso_weight(self) -> float:
        """Value of the lasso hyperparameter for machine learning hedges."""
        return self.__lasso_weight

    @lasso_weight.setter
    def lasso_weight(self, value: float):
        self.__lasso_weight = value

    @property
    def ridge_weight(self) -> float:
        """Value of the ridge hyperparameter for machine learning hedges"""
        return self.__ridge_weight

    @ridge_weight.setter
    def ridge_weight(self, value: float):
        self.__ridge_weight = value

    def to_dict(self, resolved_identifiers):
        positions_to_price = []
        for position in self.initial_portfolio.positions:
            pos_to_price = {'assetId': position.asset_id}
            if position.quantity:
                pos_to_price['quantity'] = position.quantity
            if position.weight:
                pos_to_price['weight'] = position.weight
            positions_to_price.append(pos_to_price)
        payload = {
            'positions': positions_to_price,
            'parameters': {
                'currency': 'USD',
                'pricingDate': self.initial_portfolio.date.strftime('%Y-%m-%d'),
                'useUnadjustedClosePrice': True,
                'frequency': 'End Of Day'
            }
        }
        if self.initial_portfolio.reference_notional:
            payload['parameters']['targetNotional'] = self.initial_portfolio.reference_notional
            payload['parameters']['weightingStrategy'] = "Weight"

        try:
            price_results = GsSession.current._post('/price/positions', payload)
        except Exception as e:
            raise MqValueError(f'There was an error pricing your positions: {e}')
        if 'errorMessage' in price_results:
            raise MqValueError(f'There was an error pricing your positions: {price_results["errorMessage"]}')

        if self.initial_portfolio.reference_notional is None:
            self.initial_portfolio.reference_notional = price_results.get('actualNotional')
        positions_as_dict = [{'assetId': p['assetId'], 'quantity': p['quantity']} for p in
                             price_results.get('positions', [])]

        # Resolve any assets in the hedge universe, asset constraints, and asset exclusions
        hedge_date = self.initial_portfolio.date
        self.universe = [resolved_identifiers.get(asset, [{'id': asset}])[0].get('id') for asset in self.universe]
        if self.benchmarks is not None:
            self.benchmarks = [resolved_identifiers.get(asset, [{'id': asset}])[0].get('id')
                               for asset in self.benchmarks]
        if self.exclusions is not None:
            if self.exclusions.assets is not None:
                self.exclusions.assets = [resolved_identifiers.get(asset, [{'id': asset}])[0].get('id')
                                          for asset in self.exclusions.assets]
        if self.constraints is not None and self.constraints.assets is not None:
            for con in self.constraints.assets:
                if len(resolved_identifiers.get(con.constraint_name, [])) > 0:
                    con.constraint_name = resolved_identifiers.get(con.constraint_name)[0].get('id',
                                                                                               con.constraint_name)

        # Parse and return dictionary
        observation_start_date = self.observation_start_date or hedge_date - relativedelta(years=1)
        as_dict = {
            'hedgeTarget': {
                'positions': positions_as_dict
            },
            'universe': self.universe,
            'notional': self.initial_portfolio.reference_notional,
            'observationStartDate': observation_start_date.strftime("%Y-%m-%d"),
            'observationEndDate': hedge_date.strftime("%Y-%m-%d"),
            'backtestStartDate': observation_start_date.strftime("%Y-%m-%d"),
            'backtestEndDate': hedge_date.strftime("%Y-%m-%d"),
            'samplingPeriod': self.sampling_period,
            'maxLeverage': self.max_leverage,
            'explodeUniverse': self.explode_universe,
            'excludeTargetAssets': self.exclude_target_assets,
            'excludeHardToBorrowAssets': self.exclude_hard_to_borrow_assets,
            'excludeRestrictedAssets': self.exclude_hard_to_borrow_assets,
            'maxAdvPercentage': self.max_adv_percentage,
            'maxReturnDeviation': self.max_return_deviation,
            'maxWeight': self.max_weight,
            'marketParticipationRate': self.market_participation_rate,
            'useMachineLearning': True,
            'lassoWeight': self.lasso_weight,
            'ridgeWeight': self.ridge_weight
        }

        exclusions_as_dict = self.exclusions.to_dict() if self.exclusions else {}
        constraints_as_dict = self.constraints.to_dict() if self.constraints else {}
        if 'classificationConstraints' in exclusions_as_dict or 'classificationConstraints' in constraints_as_dict:
            exclusions = exclusions_as_dict.get('classificationConstraints', [])
            constraints = constraints_as_dict.get('classificationConstraints', [])
            as_dict['classificationConstraints'] = exclusions + constraints
        if 'assetConstraints' in exclusions_as_dict or 'assetConstraints' in constraints_as_dict:
            exclusions = exclusions_as_dict.get('assetConstraints', [])
            constraints = constraints_as_dict.get('assetConstraints', [])
            as_dict['assetConstraints'] = exclusions + constraints
        if 'esgConstraints' in constraints_as_dict:
            as_dict['esgConstraints'] = constraints_as_dict.get('esgConstraints', [])
        if self.percentage_in_cash is not None:
            as_dict['percentageInCash'] = self.percentage_in_cash
        if self.exclude_corporate_actions_types:
            as_dict['excludeCorporateActionTypes'] = [x.value for x in self.exclude_corporate_actions_types]
        if self.min_market_cap is not None:
            as_dict['minMarketCap'] = self.min_market_cap
        if self.max_market_cap is not None:
            as_dict['maxMarketCap'] = self.max_market_cap
        if self.benchmarks is not None and len(self.benchmarks):
            as_dict['benchmarks'] = self.benchmarks

        return as_dict

    def resolve_identifiers_in_payload(self, hedge_date) -> tuple:
        """
        The hedge payload has identifiers which need to be resolved
        The resolved values here are used to convert back from asset Id to provided identifier for benchmark curves
        """
        identifiers = [identifier for identifier in self.universe]
        if self.exclusions is not None and self.exclusions.assets is not None:
            identifiers = identifiers + [asset for asset in self.exclusions.assets]
        if self.benchmarks is not None:
            identifiers = identifiers + [asset for asset in self.benchmarks]
        if self.constraints is not None:
            if self.constraints.assets is not None:
                identifiers = identifiers + [asset.constraint_name for asset in self.constraints.assets]
        resolver = GsAssetApi.resolve_assets(identifier=identifiers,
                                             fields=['id'],
                                             as_of=hedge_date)
        return resolver


class Hedge:
    """
    A Marquee hedge.
    """

    def __init__(self,
                 parameters,
                 objective: HedgeObjective
                 ):
        self.__parameters = parameters
        self.__objective = objective
        self.__result = {}

    @property
    def parameters(self):
        return self.__parameters

    @parameters.setter
    def parameters(self, value):
        self.__parameters = value

    @property
    def objective(self):
        return self.__objective

    @property
    def result(self) -> Dict:
        return self.__result

    def calculate(self) -> Dict:
        """
        Calculates the hedge
        :return: a dictionary with calculation results
        """
        resolved_identifiers = self.parameters.resolve_identifiers_in_payload(self.parameters.initial_portfolio.date)
        params = self.parameters.to_dict(resolved_identifiers)
        results = GsHedgeApi.calculate_hedge({'objective': self.objective.value,
                                              'parameters': params})
        if 'errorMessage' in results and 'result' not in results:
            raise MqValueError(f"Error calculating hedge: {results['errorMessage']}. Please adjust your constraints "
                               f"and try again.")
        calculation_results = results.get('result')
        formatted_results = self._format_hedge_calculate_results(calculation_results)
        formatted_results = self._enhance_result_with_benchmark_curves(formatted_results,
                                                                       calculation_results.get('benchmarks', []),
                                                                       resolved_identifiers)

        self.__result = formatted_results
        return formatted_results

    def get_constituents(self) -> pd.DataFrame:
        """
        Get metadata for hedge constituents
        :return: a DataFrame with results
        """
        constituents = self.result.get('Hedge', {}).get('Constituents', [])
        formatted_constituents = []
        for row in constituents:
            formatted_row = {}
            for key in row:
                formatted_row[key[0].capitalize() +
                              ''.join(map(lambda x: x if x.islower() else f' {x}', key[1:]))] = row[key]
            formatted_constituents.append(formatted_row)
        return pd.DataFrame(formatted_constituents)

    def get_statistics(self) -> pd.DataFrame:
        """
        Get all statistics available for the portfolio, hedge, and hedged portfolio
        :return: a Pandas DataFrame with results
        """
        results = {'Portfolio': {}, 'Hedge': {}, 'Hedged Portfolio': {}}
        for key in self.result:
            for inner_key in self.result[key]:
                if isinstance(self.result[key][inner_key], float):
                    results[key][inner_key] = self.result[key][inner_key]
        return pd.DataFrame(results)

    def get_backtest_performance(self) -> pd.DataFrame:
        """
        Get the backtest performance timeseries
        :return: a Pandas DataFrame with results
        """
        return self._get_timeseries('Backtest Performance')

    def get_backtest_correlation(self) -> pd.DataFrame:
        """
        Get the backtest_correlation timeseries of the hedge
        :return: a Pandas DataFrame with results
        """
        return self._get_timeseries('Backtest Correlation')

    def _get_timeseries(self, timeseries_name: str) -> pd.DataFrame:
        results = {}
        for key in self.result:
            if timeseries_name in self.result[key]:
                ts = self.result[key][timeseries_name]
                for data in ts:
                    date = data[0]
                    if date in results:
                        results[date][key] = data[1]
                    else:
                        results[date] = {'Date': date, key: data[1]}
        return pd.DataFrame(results.values()).set_index('Date')

    @staticmethod
    def _format_hedge_calculate_results(calculation_results):
        renamed_results = {
            'Portfolio': calculation_results.get('target'),
            'Hedge': calculation_results.get('hedge'),
            'Hedged Portfolio': calculation_results.get('hedgedTarget')
        }

        formatted_results = {}
        for key in renamed_results:
            formatted_results[key] = Hedge.format_dictionary_key_to_readable_format(renamed_results[key])

        return formatted_results

    @staticmethod
    def _enhance_result_with_benchmark_curves(formatted_results, benchmark_results, resolver):
        asset_id_to_provided_identifier_map = dict(
            (x['id'], provided_identifier)
            for provided_identifier, marquee_assets in resolver.items()
            for x in marquee_assets)

        if len(benchmark_results):
            for x in benchmark_results:
                benchmark_asset_id = asset_id_to_provided_identifier_map[x['assetId']]
                formatted_results[benchmark_asset_id] = Hedge.format_dictionary_key_to_readable_format(x)

        return formatted_results

    @staticmethod
    def format_dictionary_key_to_readable_format(renamed_results):
        formatted_results = {}
        for inner_key in renamed_results:
            formatted_results[inner_key[0].capitalize() + ''.join(map(lambda x: x if x.islower() else f' {x}',
                                                                      inner_key[1:]))] = renamed_results[inner_key]
        return formatted_results

    @staticmethod
    def find_optimal_hedge(hedge_query: dict, hyperparams: dict, metric: str) -> \
            Union[dict, float]:
        """
        This function is designed to find the 'best' hedge from a list of hedges that are computed using a grid
        search over all hyperparameters passed in - where 'best' is defined by the metric argument passed in and
        whether we want to minimize or maximize this metric.

        :param hedge_query: dict, hedge data that is sent to the Marquee API as input to the new performance hedger
        :param hyperparams: dict, keys are hyperparameters (Concentration or Diversity) that map to lists of the values
                                  to use for one of these hyperparameters when running the new performance hedger.
        :param metric: str, the metric we want to optimize i.e. 'holdingError' or 'rSquared'
        :return: dict, float, and List, the best hedge found using the algorithm, the value of the metric being
                                 optimized, and the List of optimal hyperparameters
        """
        hedge_results = {}
        opt_map = Hedge.create_optimization_mappings()
        optimization_type = opt_map[metric]
        _logger.info(f'We are trying to {optimization_type} {metric} and will return the optimized hedge & '
                     f'metric value...')
        hyperparam_grid = [(x, y) for x in hyperparams['Concentration'] for y in hyperparams['Diversity']]
        for pair in hyperparam_grid:
            hedge_params = hedge_query['parameters']
            hedge_params.lasso_weight, hedge_params.ridge_weight = pair[0], pair[1]
            hedge_query['parameters'] = hedge_params
            results = GsHedgeApi.calculate_hedge(hedge_query)
            _logger.info(f'Current Hedge is using the following values for Concentration/Diversity: {pair}')
            curr_results, curr_pair = results['result']['hedge'], pair
            hedge_results[curr_results[metric]] = (curr_results, curr_pair)
            _logger.info(f'Current Hedge value for {metric}: {curr_results[metric] * 100:.3}%')
        optimized_metric = min(hedge_results.keys()) if optimization_type == 'minimize' else max(hedge_results.keys())
        optimized_hedge, optimized_hyperparams = hedge_results[optimized_metric][0], hedge_results[optimized_metric][1]
        return optimized_hedge, optimized_metric, optimized_hyperparams

    @staticmethod
    def create_optimization_mappings() -> dict:
        """
        This function is designed to construct a mapping between metrics a user can choose to optimize when calling the
        New Performance Hedger and the way the metric should be optimized.

        :param none:
        :return: dict, the dictionary containing a mapping between metrics to optimize and how they should be optimized
        """
        opt_dict = {'rSquared': 'maximize', 'correlation': 'maximize', 'holdingError': 'minimize',
                    'trackingError': 'minimize', 'transactionCost': 'minimize', 'annualizedReturn': 'maximize'}
        return opt_dict

    @staticmethod
    def construct_portfolio_weights_and_asset_numbers(results: dict) -> Union[dict, List]:
        """
        Function used to retrieve the constructed portfolio from a performance hedge, sort it, then calculate the
        weights for all assets and total number of assets and return these results.

        :param results: dict, the results of the performance hedge request made to the Marquee API
        :return: dict, list, list - the portfolio, portfolio weights, and number of assets
        """
        portfolio = results["result"]["hedge"]["constituents"]
        portfolio.sort(key=lambda x: x['weight'], reverse=True)
        weights = [asset['weight'] for asset in portfolio]
        asset_numbers = list(range(len(portfolio)))
        return portfolio, weights, asset_numbers

    @staticmethod
    def asset_id_diffs(portfolio_asset_ids, thomson_reuters_asset_ids):
        """
        Function designed to find the assets that are contained in the portfolio but that we don't have
        Thomson Reuters data for.

        :param portfolio_asset_ids: list, the list of MQIDs representing all of the assets that we are computing
                                          rebalance costs for
        :param thomson_reuters_asset_ids: list, the list of MQIDs representing all of the assets that we have Thomson
                                                Reuters data for
        :return: list, the assets that we don't have Thomson Reuters data for and should exclude in the transaction cost
                       calculations
        """
        diffs = list(set(portfolio_asset_ids) - set(thomson_reuters_asset_ids))
        return diffs

    @staticmethod
    def create_transaction_cost_data_structures(portfolio_asset_ids, portfolio_quantities, thomson_reuters_eod_data,
                                                backtest_dates):
        """
        Function designed to create the data structures necessary to compute transaction costs based on rebalancing a
        portfolio of assets.

        :param portfolio_asset_ids: list, the asset_ids for each asset in the underlying portfolio that we want to
                                          compute transaction costs for
        :param portfolio_quantities: list, the number of shares for each asset in the underlying portfolio that we want
                                           to compute transaction costs for
        :param thomson_reuters_eod_data: Dataset, the data used to fetch prices for assets - in this case from Thomson
                                                  Reuters
        :param backtest_dates: list, the dates that the portfolio is held for (that we want to compute rebalance costs
                                     for)
        :return: Union[list, dict], the data structures necessary for computing transaction (rebalance) costs
        """
        thomson_reuters_asset_ids = [asset_id for asset_id in thomson_reuters_eod_data.get_data(
            backtest_dates[-1], backtest_dates[-1], assetId=portfolio_asset_ids)['assetId']]
        diffs = Hedge.asset_id_diffs(portfolio_asset_ids, thomson_reuters_asset_ids)
        for diff in diffs:
            portfolio_asset_ids.remove(diff)

        # Map asset_id to quantity of shares from portfolio, while excluding assets that are found in the diffs since
        # there is no Thomson Reuters data on them
        id_quantity_map = {}
        for idx, asset_id in enumerate(portfolio_asset_ids):
            if asset_id not in diffs:
                id_quantity_map[asset_id] = portfolio_quantities[idx]

        # Map asset_id to list of prices of that asset over the transaction_cost_dates we want
        id_prices_map = defaultdict(lambda: list())
        prices_df = pd.DataFrame()
        for date in backtest_dates:
            data = thomson_reuters_eod_data.get_data(date, date, assetId=portfolio_asset_ids)
            prices_df = prices_df.append(data)
        for asset_id in portfolio_asset_ids:
            id_prices_map[asset_id] = list(prices_df.loc[prices_df['assetId'] == asset_id]['closePrice'])

        # Create list representing notional of each day in transaction_cost_days and map asset_ids to notional of each
        # asset on each day
        id_to_notional_map = {}
        notionals_assets = [abs(np.asarray(id_prices_map[asset_id]) * id_quantity_map[asset_id]) for asset_id in
                            portfolio_asset_ids]
        # Mapping asset_id to notionals of each day of that asset_id
        for idx, asset_id in enumerate(portfolio_asset_ids):
            id_to_notional_map[asset_id] = list(notionals_assets[idx])
        total_notionals_each_day = list(np.sum(notionals_assets, axis=0))

        # Create map of asset_ids to weights of total portfolio on each day
        id_to_weight_map = {}
        for idx, asset_id in enumerate(portfolio_asset_ids):
            id_to_weight_map[asset_id] = [i / j for i, j in
                                          zip(id_to_notional_map[portfolio_asset_ids[idx]], total_notionals_each_day)]
        return id_quantity_map, id_prices_map, id_to_notional_map, id_to_weight_map

    @staticmethod
    def t_cost(basis_points, notional_traded):
        """
        Function designed to compute the transaction costs associated with trading a notional
        amount of an asset to rebalance a portfolio.

        :param basis_points: float, the number of basis points to use as an approximation when computing transaction
                                    costs to trade each asset that is rebalanced and that will be converted to a
                                    percentage (e.g. 20.43)
        :param notional_traded: float, notional amount of the asset that is being traded to rebalance the portfolio
        :return: float, the total transaction cost of trading a particular notional amount of an asset
        """
        return (basis_points * 1e-4) * notional_traded

    @staticmethod
    def compute_notional_traded(notional_on_the_day, prev_weight, curr_weight):
        """
        Function used to compute the notional amount (USD) of an asset that will be traded on a particular day, using
        the weights of the asset from the previous day and the weights & notional from the current day.

        :param notional_on_the_day: float, notional amount of the asset that the portfolio contains on the current day
        :param prev_weight: float, the weighting of the corresponding asset (of the entire portfolio) on the previous
                                   day
        :param curr_weight: float, the weighting of the corresponding asset (of the entire portfolio) on the current day
        :return: float, the net notional amount of the asset traded on the current day
        """
        return sum([np.abs(curr_weight - prev_weight) * notional_on_the_day])

    @staticmethod
    def compute_tcosts(basis_points, asset_weights, asset_notionals, backtest_dates, portfolio_asset_ids):
        """
        Function to compute cumulative transaction costs associated with rebalancing a portfolio. In particular, for
        each day on which we compute the cumulative the rebalancing costs (USD), the weights of the constituents of the
        portfolio on the previous day are used to calculate how much of the notional amount of each asset is traded to
        execute the rebalance.

        :param basis_points: float, the number of basis points to use as an approximation when computing transaction
                                    costs to trade each asset that is rebalanced and that will be converted to a
                                    percentage (e.g. 20.43)
        :param asset_weights: dict, the dictionary mapping of asset_ids (MQIDs) to a list of weights where each weight
                                    represents the weighting of the corresponding asset (of the entire portfolio) on
                                    each day in the backtest period
        :param asset_notionals: dict, the dictionary mapping of asset_ids (MQIDs) to a list of floats where each float
                                      represents the notional amount of the corresponding asset (of the entire
                                      portfolio) on each day in the backtest period
        :param backtest_dates: list, the dates that the portfolio is held for (that we want to compute rebalance costs
                                     for)
        :param portfolio_asset_ids: list, the list of MQIDs representing all of the assets that we are computing
                                          rebalancing costs for
        :return: pd.Series, the cumulative transaction costs associated with rebalancing the portfolio across the
                            backtest period
        """
        tcosts_each_day = []
        for idx, date in enumerate(backtest_dates):
            tcost_today = 0
            for asset_id in portfolio_asset_ids:
                prev_weights = asset_weights[asset_id][0] if idx == 0 else asset_weights[asset_id][idx - 1]
                notional_on_the_day, curr_weights = asset_notionals[asset_id][idx], asset_weights[asset_id][idx]
                notional_to_trade = Hedge.compute_notional_traded(notional_on_the_day, prev_weights, curr_weights)
                transaction_cost = Hedge.t_cost(basis_points, notional_to_trade)
                tcost_today += transaction_cost
            tcosts_each_day.append(abs(tcost_today))
        cum_tcosts = pd.Series(np.cumsum(tcosts_each_day))
        return cum_tcosts


class PerformanceHedge(Hedge):

    def __init__(self,
                 parameters: PerformanceHedgeParameters = None,
                 **kwargs):
        super().__init__(parameters, HedgeObjective.Replicate_Performance)
