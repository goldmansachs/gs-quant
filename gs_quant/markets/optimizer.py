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
import logging
from enum import Enum
from typing import List

from dateutil.relativedelta import relativedelta

from gs_quant.api.gs.hedges import GsHedgeApi
from gs_quant.errors import MqValueError
from gs_quant.markets.factor import Factor
from gs_quant.markets.position_set import PositionSet, Position
from gs_quant.markets.securities import Asset
from gs_quant.models.risk_model import FactorRiskModel
from gs_quant.session import GsSession
from gs_quant.target.hedge import CorporateActionsTypes

_logger = logging.getLogger(__name__)


class OptimizationConstraintUnit(Enum):
    DECIMAL = 'Decimal'
    NOTIONAL = 'Notional'
    PERCENT = 'Percent'


class OptimizerObjective(Enum):
    MINIMIZE_FACTOR_RISK = 'Minimize Factor Risk'


class OptimizerType(Enum):
    AXIOMA_PORTFOLIO_OPTIMIZER = 'Axioma Portfolio Optimizer'


class AssetConstraint:

    def __init__(self,
                 asset: Asset,
                 minimum: float = 0,
                 maximum: float = 100,
                 unit: OptimizationConstraintUnit = OptimizationConstraintUnit.PERCENT):
        self.__asset = asset
        self.__minimum = minimum
        self.__maximum = maximum
        self.__unit = unit

    @property
    def asset(self) -> Asset:
        return self.__asset

    @asset.setter
    def asset(self, value: Asset):
        self.__asset = value

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
    def unit(self) -> OptimizationConstraintUnit:
        return self.__unit

    @unit.setter
    def unit(self, value: OptimizationConstraintUnit):
        self.__unit = value

    def to_dict(self):
        return {
            'assetId': self.asset.get_marquee_id(),
            'min': self.minimum * 100 if self.unit == OptimizationConstraintUnit.DECIMAL else self.minimum,
            'max': self.maximum * 100 if self.unit == OptimizationConstraintUnit.DECIMAL else self.maximum
        }


class CountryConstraint:

    def __init__(self,
                 country_name: str,
                 minimum: float = 0,
                 maximum: float = 100,
                 unit: OptimizationConstraintUnit = OptimizationConstraintUnit.PERCENT):
        if unit not in [OptimizationConstraintUnit.PERCENT, OptimizationConstraintUnit.DECIMAL]:
            raise MqValueError('Country constraints can only be set by percent or decimal.')
        self.__country_name = country_name
        self.__minimum = minimum
        self.__maximum = maximum
        self.__unit = unit

    @property
    def country_name(self) -> str:
        return self.__country_name

    @country_name.setter
    def country_name(self, value: str):
        self.__country_name = value

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
    def unit(self) -> OptimizationConstraintUnit:
        return self.__unit

    @unit.setter
    def unit(self, value: OptimizationConstraintUnit):
        if value not in [OptimizationConstraintUnit.PERCENT, OptimizationConstraintUnit.DECIMAL]:
            raise MqValueError('Country constraints can only be set by percent or decimal.')
        self.__unit = value

    def to_dict(self):
        return {
            'type': 'Country',
            'name': self.country_name,
            'min': self.minimum * 100 if self.unit == OptimizationConstraintUnit.DECIMAL else self.minimum,
            'max': self.maximum * 100 if self.unit == OptimizationConstraintUnit.DECIMAL else self.maximum
        }


class SectorConstraint:

    def __init__(self,
                 sector_name: str,
                 minimum: float = 0,
                 maximum: float = 100,
                 unit: OptimizationConstraintUnit = OptimizationConstraintUnit.PERCENT):
        if unit not in [OptimizationConstraintUnit.PERCENT, OptimizationConstraintUnit.DECIMAL]:
            raise MqValueError('Sector constraints can only be set by percent or decimal.')
        self.__sector_name = sector_name
        self.__minimum = minimum
        self.__maximum = maximum
        self.__unit = unit

    @property
    def sector_name(self) -> str:
        return self.__sector_name

    @sector_name.setter
    def sector_name(self, value: str):
        self.__sector_name = value

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
    def unit(self) -> OptimizationConstraintUnit:
        return self.__unit

    @unit.setter
    def unit(self, value: OptimizationConstraintUnit):
        if value not in [OptimizationConstraintUnit.PERCENT, OptimizationConstraintUnit.DECIMAL]:
            raise MqValueError('Country constraints can only be set by percent.')
        self.__unit = value

    def to_dict(self):
        return {
            'type': 'Sector',
            'name': self.sector_name,
            'min': self.minimum * 100 if self.unit == OptimizationConstraintUnit.DECIMAL else self.minimum,
            'max': self.maximum * 100 if self.unit == OptimizationConstraintUnit.DECIMAL else self.maximum
        }


class FactorConstraint:

    def __init__(self,
                 factor: Factor,
                 max_exposure: float):
        """
        Constrain a factor by a max exposure
        :param factor: the factor to constrain
        :param max_exposure: the maximum exposure to the factor in the final portfolio
        """
        self.__factor = factor
        self.__max_exposure = max_exposure

    @property
    def factor(self) -> Factor:
        return self.__factor

    @factor.setter
    def factor(self, value: Factor):
        self.__factor = value

    @property
    def max_exposure(self) -> float:
        return self.__max_exposure

    @max_exposure.setter
    def max_exposure(self, value: float):
        self.__max_exposure = value

    def to_dict(self):
        return {
            'factor': self.factor.name,
            'exposure': self.max_exposure
        }


class OptimizerUniverse:

    def __init__(self,
                 assets: List[Asset],
                 explode_composites: bool = True,
                 exclude_initial_position_set_assets: bool = True,
                 exclude_corporate_actions_types: List[CorporateActionsTypes] = [],
                 exclude_hard_to_borrow_assets: bool = False,
                 exclude_restricted_assets: bool = False,
                 min_market_cap: float = None,
                 max_market_cap: float = None):
        """
        The universe of assets with which to construct an optimization
        :param assets: list of assets to include in the universe
        :param explode_composites: explode composites in the universe to include their constituents in the universe
        :param exclude_initial_position_set_assets: exclude assets in the initial holdings
        :param exclude_corporate_actions_types: exclude assets included under the list of corporate action types
        :param exclude_hard_to_borrow_assets: exclude assets with a borrow cost greater than or equal to 200 bps
        :param exclude_restricted_assets: exclude restricted assets
        :param min_market_cap: exclude assets below the requested minimum market cap
        :param max_market_cap: exclude assets above the requested maximum market cap
        """
        self.__assets = assets
        self.__explode_composites = explode_composites
        self.__exclude_initial_position_set_assets = exclude_initial_position_set_assets
        self.__exclude_corporate_actions_types = exclude_corporate_actions_types
        self.__exclude_hard_to_borrow_assets = exclude_hard_to_borrow_assets
        self.__exclude_restricted_assets = exclude_restricted_assets
        self.__min_market_cap = min_market_cap
        self.__max_market_cap = max_market_cap

    @property
    def assets(self) -> List[Asset]:
        return self.__assets

    @assets.setter
    def assets(self, value: List[Asset]):
        self.__assets = value

    @property
    def explode_composites(self) -> bool:
        return self.__explode_composites

    @explode_composites.setter
    def explode_composites(self, value: bool):
        self.__explode_composites = value

    @property
    def exclude_initial_position_set_assets(self) -> bool:
        return self.__exclude_initial_position_set_assets

    @exclude_initial_position_set_assets.setter
    def exclude_initial_position_set_assets(self, value: bool):
        self.__exclude_initial_position_set_assets = value

    @property
    def exclude_corporate_actions_types(self) -> List[CorporateActionsTypes]:
        return self.__exclude_corporate_actions_types

    @exclude_corporate_actions_types.setter
    def exclude_corporate_actions_types(self, value: List[CorporateActionsTypes]):
        self.__exclude_corporate_actions_types = value

    @property
    def exclude_hard_to_borrow_assets(self) -> bool:
        return self.__exclude_hard_to_borrow_assets

    @exclude_hard_to_borrow_assets.setter
    def exclude_hard_to_borrow_assets(self, value: bool):
        self.__exclude_hard_to_borrow_assets = value

    @property
    def exclude_restricted_assets(self) -> bool:
        return self.__exclude_restricted_assets

    @exclude_restricted_assets.setter
    def exclude_restricted_assets(self, value: bool):
        self.__exclude_restricted_assets = value

    @property
    def min_market_cap(self) -> float:
        return self.__min_market_cap

    @min_market_cap.setter
    def min_market_cap(self, value: float):
        self.__min_market_cap = value

    @property
    def max_market_cap(self) -> float:
        return self.__max_market_cap

    @max_market_cap.setter
    def max_market_cap(self, value: float):
        self.__max_market_cap = value

    def to_dict(self):
        as_dict = {
            'hedgeUniverse': {
                'assetIds': [asset.get_marquee_id() for asset in self.assets],
                'assetTypes': []
            },
            'excludeCorporateActions': len(self.exclude_corporate_actions_types) != 0,
            'excludeCorporateActionsTypes': [x.value for x in self.exclude_corporate_actions_types],
            'excludeHardToBorrowAssets': self.exclude_hard_to_borrow_assets,
            'excludeRestrictedAssets': self.exclude_restricted_assets,
            'excludeTargetAssets': self.exclude_initial_position_set_assets,
            'explodeUniverse': self.explode_composites,
        }
        if self.min_market_cap:
            as_dict['minMarketCap'] = self.min_market_cap
        if self.max_market_cap:
            as_dict['maxMarketCap'] = self.max_market_cap
        return as_dict


class MaxFactorProportionOfRiskConstraint:

    def __init__(self,
                 max_factor_proportion_of_risk: float,
                 unit: OptimizationConstraintUnit = OptimizationConstraintUnit.PERCENT):
        if unit not in [OptimizationConstraintUnit.PERCENT, OptimizationConstraintUnit.DECIMAL]:
            raise MqValueError('Max Factor Proportion of Risk can only be set by percent or decimal.')
        if unit == OptimizationConstraintUnit.PERCENT:
            max_factor_proportion_of_risk = max_factor_proportion_of_risk / 100
        self.__max_factor_proportion_of_risk = max_factor_proportion_of_risk
        self.__unit = unit

    @property
    def max_factor_proportion_of_risk(self) -> float:
        return self.__max_factor_proportion_of_risk

    @max_factor_proportion_of_risk.setter
    def max_factor_proportion_of_risk(self, value: float):
        self.__max_factor_proportion_of_risk = value


class OptimizerConstraints:

    def __init__(self,
                 asset_constraints: List[AssetConstraint] = [],
                 country_constraints: List[CountryConstraint] = [],
                 sector_constraints: List[SectorConstraint] = [],
                 factor_constraints: List[FactorConstraint] = [],
                 max_factor_proportion_of_risk: MaxFactorProportionOfRiskConstraint = None):
        self.__asset_constraints = asset_constraints
        self.__country_constraints = country_constraints
        self.__sector_constraints = sector_constraints
        self.__factor_constraints = factor_constraints
        self.__max_factor_proportion_of_risk = max_factor_proportion_of_risk

    @property
    def asset_constraints(self) -> List[AssetConstraint]:
        return self.__asset_constraints

    @asset_constraints.setter
    def asset_constraints(self, value: List[AssetConstraint]):
        self.__asset_constraints = value

    @property
    def country_constraints(self) -> List[CountryConstraint]:
        return self.__country_constraints

    @country_constraints.setter
    def country_constraints(self, value: List[CountryConstraint]):
        self.__country_constraints = value

    @property
    def sector_constraints(self) -> List[SectorConstraint]:
        return self.__sector_constraints

    @sector_constraints.setter
    def sector_constraints(self, value: List[SectorConstraint]):
        self.__sector_constraints = value

    @property
    def factor_constraints(self) -> List[FactorConstraint]:
        return self.__factor_constraints

    @factor_constraints.setter
    def factor_constraints(self, value: List[FactorConstraint]):
        self.__factor_constraints = value

    @property
    def max_factor_proportion_of_risk(self) -> MaxFactorProportionOfRiskConstraint:
        return self.__max_factor_proportion_of_risk

    @max_factor_proportion_of_risk.setter
    def max_factor_proportion_of_risk(self, value: MaxFactorProportionOfRiskConstraint):
        self.__max_factor_proportion_of_risk = value

    def to_dict(self):
        types = set([c.unit for c in self.asset_constraints])
        if len(types) > 1:
            raise MqValueError('All asset constraints need to have the same unit')
        constrain_by_notional = len(self.asset_constraints) > 0 and types.pop() == OptimizationConstraintUnit.NOTIONAL
        as_dict = {
            'assetConstraints': [c.to_dict() for c in self.asset_constraints],
            'classificationConstraints': [c.to_dict() for c in self.country_constraints + self.sector_constraints],
            'factorConstraints': [c.to_dict() for c in self.factor_constraints],
            'constrainAssetsByNotional': constrain_by_notional
        }

        if self.max_factor_proportion_of_risk:
            as_dict['maxFactorMCTR'] = self.max_factor_proportion_of_risk.max_factor_proportion_of_risk

        return as_dict


class OptimizerSettings:

    def __init__(self,
                 notional: float = 10000000,
                 allow_long_short: bool = False,
                 min_names: float = 0,
                 max_names: float = 100):
        """
        Optimizer settings
        :param notional: the max gross notional of the optimization
        :param allow_long_short: allow a long/short optimization
        :param min_names: minimum number of assets in the optimization
        :param max_names: maximum number of assets in the optimization
        """
        self.__notional = notional
        self.__allow_long_short = allow_long_short
        self.__min_names = min_names
        self.__max_names = max_names

    @property
    def notional(self) -> float:
        return self.__notional

    @notional.setter
    def notional(self, value: float):
        self.__notional = value

    @property
    def allow_long_short(self) -> bool:
        return self.__allow_long_short

    @allow_long_short.setter
    def allow_long_short(self, value: bool):
        self.__allow_long_short = value

    @property
    def min_names(self) -> float:
        return self.__min_names

    @min_names.setter
    def min_names(self, value: float):
        self.__min_names = value

    @property
    def max_names(self) -> float:
        return self.__max_names

    @max_names.setter
    def max_names(self, value: float):
        self.__max_names = value

    def to_dict(self):
        return {
            'hedgeNotional': self.notional,
            'allowLongShort': self.allow_long_short,
            'minNames': self.min_names,
            'maxNames': self.max_names
        }


class OptimizerStrategy:

    def __init__(self,
                 initial_position_set: PositionSet,
                 universe: OptimizerUniverse,
                 risk_model: FactorRiskModel,
                 constraints: OptimizerConstraints = None,
                 settings: OptimizerSettings = None,
                 objective: OptimizerObjective = OptimizerObjective.MINIMIZE_FACTOR_RISK):
        """
        A strategy for [..]
        :param initial_position_set: a position set correlating to your original holdings as of a specific date
        :param universe: universe from which to choose optimization assets
        :param risk_model: risk model with which to calculate risk
        :param constraints: constraints for the optimization
        :param settings: settings for the optimization
        :param objective: objective for the optimization
        """
        self.__initial_position_set = initial_position_set
        self.__universe = universe
        self.__risk_model = risk_model
        self.__constraints = constraints
        self.__settings = settings
        self.__objective = objective
        self.__result = None

    @property
    def initial_position_set(self) -> PositionSet:
        return self.__initial_position_set

    @initial_position_set.setter
    def initial_position_set(self, value: PositionSet):
        self.__initial_position_set = value

    @property
    def universe(self) -> OptimizerUniverse:
        return self.__universe

    @universe.setter
    def universe(self, value: OptimizerUniverse):
        self.__universe = value

    @property
    def risk_model(self) -> FactorRiskModel:
        return self.__risk_model

    @risk_model.setter
    def risk_model(self, value: FactorRiskModel):
        self.__risk_model = value

    @property
    def constraints(self) -> OptimizerConstraints:
        return self.__constraints

    @constraints.setter
    def constraints(self, value: OptimizerConstraints):
        self.__constraints = value

    @property
    def settings(self) -> OptimizerSettings:
        return self.__settings

    @settings.setter
    def settings(self, value: OptimizerSettings):
        self.__settings = value

    @property
    def objective(self) -> OptimizerObjective:
        return self.__objective

    @objective.setter
    def objective(self, value: OptimizerObjective):
        self.__objective = value

    def to_dict(self):
        if self.constraints is None:
            self.constraints = OptimizerConstraints()
        if self.settings is None:
            self.settings = OptimizerSettings()

        backtest_start_date = self.initial_position_set.date - relativedelta(years=1)
        positions_as_dict = [{'assetId': p.asset_id, 'quantity': p.quantity}
                             for p in self.initial_position_set.positions]
        parameters = {
            'hedgeTarget': {
                'positions': positions_as_dict
            },
            'hedgeDate': self.initial_position_set.date.strftime('%Y-%m-%d'),
            'backtestStartDate': backtest_start_date.strftime('%Y-%m-%d'),
            'backtestEndDate': self.initial_position_set.date.strftime('%Y-%m-%d'),
            'comparisons': [],
            'fxHedged': False,
            'marketParticipationRate': 10,
            'maxAdvPercentage': 15
        }
        constraints = self.constraints.to_dict()
        for key in constraints:
            parameters[key] = constraints[key]
        settings = self.settings.to_dict()
        for key in settings:
            parameters[key] = settings[key]
        universe = self.universe.to_dict()
        for key in universe:
            parameters[key] = universe[key]
        parameters['riskModel'] = self.risk_model.id

        # Price initial_position_set if needed
        if self.initial_position_set.reference_notional is not None:
            parameters['targetNotional'] = self.initial_position_set.reference_notional
        else:
            payload = {
                'positions': positions_as_dict,
                'parameters': {
                    'currency': 'USD',
                    'pricingDate': self.initial_position_set.date.strftime('%Y-%m-%d'),
                    'useUnadjustedClosePrice': True,
                    'frequency': 'End Of Day'
                }
            }
            try:
                price_results = GsSession.current._post('/price/positions', payload)
            except Exception as e:
                raise MqValueError(f'There was an error pricing your positions: {e}')
            if 'errorMessage' in price_results:
                raise MqValueError(f'There was an error pricing your positions: {price_results["errorMessage"]}')
            parameters['targetNotional'] = price_results.get('actualNotional')

        return {
            'objective': self.objective.value,
            'parameters': parameters
        }

    def run(self,
            optimizer_type: OptimizerType = OptimizerType.AXIOMA_PORTFOLIO_OPTIMIZER):
        if optimizer_type is None:
            raise MqValueError('You must pass an optimizer type.')
        if optimizer_type == OptimizerType.AXIOMA_PORTFOLIO_OPTIMIZER:
            optimization_results = GsHedgeApi.calculate_hedge(self.to_dict())
            if optimization_results.get('result') is None:
                raise MqValueError('Error calculating an optimization. Please contact the Marquee team for assistance.')
            self.__result = optimization_results['result']

    def get_optimization(self):
        if self.__result is None:
            raise MqValueError('You must run your strategy before pulling the results.')
        optimization = self.__result['hedge']
        return PositionSet(date=self.initial_position_set.date,
                           positions=[Position(identifier=asset.get('bbid', asset['name']),
                                               asset_id=asset['assetId'],
                                               quantity=asset['shares']) for asset in optimization['constituents']])

    def get_optimized_position_set(self):
        if self.__result is None:
            raise MqValueError('You must run your strategy before pulling the results.')
        optimization = self.__result['hedgedTarget']
        return PositionSet(date=self.initial_position_set.date,
                           positions=[Position(identifier=asset.get('bbid', asset['name']),
                                               asset_id=asset['assetId'],
                                               quantity=asset['shares']) for asset in optimization['constituents']])
