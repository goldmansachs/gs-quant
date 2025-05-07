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
from functools import wraps
from typing import List, Dict, Optional, Union, Final

from dateutil.relativedelta import relativedelta

from gs_quant.api.gs.hedges import GsHedgeApi
from gs_quant.api.gs.assets import GsAssetApi
from gs_quant.errors import MqValueError
from gs_quant.markets.factor import Factor
from gs_quant.markets.position_set import PositionSet, Position
from gs_quant.markets.securities import Asset
from gs_quant.models.risk_model import FactorRiskModel
from gs_quant.session import GsSession
from gs_quant.target.hedge import CorporateActionsTypes
import pandas as pd
import numpy as np
import math
import datetime as dt

_logger = logging.getLogger(__name__)


def resolve_assets_in_batches(identifiers: List[str],
                              fields: List[str] = None,
                              as_of_date: dt.date = dt.date.today(),
                              batch_size: int = 100,
                              **kwargs) -> List[Dict]:
    all_fields = ["id", "name", "bbid"]
    if fields:
        all_fields += fields
    identifiers_batches = np.array_split(identifiers, math.ceil(len(identifiers) / batch_size)) \
        if len(identifiers) > batch_size else [identifiers]

    all_assets_resolved = {}
    for batch in identifiers_batches:
        res = GsAssetApi.resolve_assets(identifier=list(batch),
                                        as_of=dt.datetime.combine(as_of_date, dt.datetime.min.time()),
                                        fields=all_fields,
                                        limit=1,
                                        **kwargs
                                        )
        all_assets_resolved = {**all_assets_resolved, **res}

    assets_resolved_as_records = []
    for identifier in all_assets_resolved:
        if all_assets_resolved[identifier]:
            assets_resolved_as_records.append({"identifier": identifier, **all_assets_resolved[identifier][0]})

    return assets_resolved_as_records


class OptimizationConstraintUnit(Enum):
    DECIMAL = 'Decimal'
    NOTIONAL = 'Notional'
    PERCENT = 'Percent'


class OptimizerObjective(Enum):
    MINIMIZE_FACTOR_RISK = 'Minimize Factor Risk'


class OptimizerRiskType(Enum):
    VARIANCE = 'Variance'


class OptimizerObjectiveTerm:
    DEFAULT_RISK_PARAMS: Final = {
        'factor_weight': 1,
        'specific_weight': 1,
        'risk_type': OptimizerRiskType.VARIANCE,
    }

    def __init__(self, weight: float = 1, params: Dict[str, float] = DEFAULT_RISK_PARAMS):
        self.__weight = weight
        self.__params = {**self.DEFAULT_RISK_PARAMS, **params}

    @property
    def params(self) -> Dict:
        return self.__params

    @params.setter
    def params(self, params: Dict[str, float]):
        self.__params = {**self.DEFAULT_RISK_PARAMS, **params}

    @property
    def weight(self) -> float:
        return self.__weight

    @weight.setter
    def weight(self, weight: float):
        self.__weight = weight

    def to_dict(self) -> Dict:
        payload = {
            'factorWeight': self.__params['factor_weight'],
            'specificWeight': self.__params['specific_weight'],
            'riskType': self.__params['risk_type'].value,
            'weight': self.__weight,
        }
        return payload


class OptimizerObjectiveParameters:

    def __init__(
        self,
        objective: OptimizerObjective = OptimizerObjective.MINIMIZE_FACTOR_RISK,
        terms: List[OptimizerObjectiveTerm] = [OptimizerObjectiveTerm.DEFAULT_RISK_PARAMS]
    ):
        self.__objective = objective
        self.__terms = terms

    @property
    def objective(self):
        return self.__objective

    @objective.setter
    def objective(self, objective: OptimizerObjective):
        self.__objective = objective

    @property
    def terms(self):
        return self.__terms

    @terms.setter
    def terms(self, terms: List[OptimizerObjectiveTerm]):
        self.__terms = terms

    def to_dict(self):
        if len(self.__terms) != 1:
            raise MqValueError('Only single risk term is supported')
        return {'parameters': self.__terms[0].to_dict()}


class OptimizerType(Enum):
    AXIOMA_PORTFOLIO_OPTIMIZER = 'Axioma Portfolio Optimizer'


class PrioritySetting(Enum):
    ZERO = '0'
    ONE = '1'
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'


class TurnoverNotionalType(Enum):
    NET = 'Net'
    LONG = 'Long'
    GROSS = 'Gross'


class AssetUniverse:
    def __init__(self,
                 identifiers: List[str],
                 asset_ids: List[str] = None,
                 as_of_date: dt.date = dt.date.today()):
        self.__identifiers = identifiers
        self.__as_of_date = as_of_date
        self.__asset_ids = asset_ids

    @property
    def identifiers(self):
        return self.__identifiers

    @identifiers.setter
    def identifiers(self, identifiers: List[str]):
        self.__identifiers = identifiers

    @property
    def asset_ids(self):
        return self.__asset_ids

    @asset_ids.setter
    def asset_ids(self, asset_ids: List[str]):
        self.__asset_ids = asset_ids

    @property
    def as_of_date(self):
        return self.__as_of_date

    @as_of_date.setter
    def as_of_date(self, date: dt.date):
        self.__as_of_date = date

    def resolve(self):
        if not self.__asset_ids:
            assets_resolved_as_records = resolve_assets_in_batches(identifiers=self.identifiers,
                                                                   as_of_date=self.as_of_date,
                                                                   batch_size=250
                                                                   )

            assets_resolved_df = (pd.DataFrame(assets_resolved_as_records).set_index("identifier")
                                  .reindex(self.identifiers))

            self.asset_ids = assets_resolved_df['id'].values.tolist()


class AssetConstraint:

    def __init__(self,
                 asset: Union[Asset, str],
                 minimum: float = 0,
                 maximum: float = 100,
                 unit: OptimizationConstraintUnit = OptimizationConstraintUnit.PERCENT):
        self.__asset = asset
        self.__minimum = minimum
        self.__maximum = maximum
        self.__unit = unit

    @property
    def asset(self) -> Union[Asset, str]:
        return self.__asset

    @asset.setter
    def asset(self, value: Union[Asset, str]):
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
            'assetId': self.asset if isinstance(self.asset, str) else self.asset.get_marquee_id(),
            'min': self.minimum * 100 if self.unit == OptimizationConstraintUnit.DECIMAL else self.minimum,
            'max': self.maximum * 100 if self.unit == OptimizationConstraintUnit.DECIMAL else self.maximum
        }

    @classmethod
    def build_many_constraints(cls,
                               asset_constraints: Union[pd.DataFrame, List[Dict]],
                               as_of_date: dt.date = dt.date.today(),
                               fail_on_unresolved_positions: bool = True,
                               **kwargs):
        """Create many asset constraints from a dataframe or a list of dictionaries
        :param asset_constraints: dataframe or list of dictionaries containing the asset constraints
        :param as_of_date: the date on which to resolve the assets
        :param fail_on_unresolved_positions: whether to raise an error if any assets cannot be resolved
        :param kwargs: additional arguments to pass to the resolve_assets_in_batches function.

        :return: list of AssetConstraint objects

        :raises MqValueError: if the input is missing required columns "identifier", "minimum", "maximum", or "unit"
        :raises MqValueError: if any assets cannot be resolved and fail_on_unresolved_positions is True
        :raises MqValueError: if the input asset constraints are in more than one unit

        **Examples**

        1. The input is a list of dictionaries
        >>> asset_constraints = AssetConstraint.build_many_constraints(
        >>>     [{"identifier": "AAPL UW", "minimum": 0, "maximum": 5, "unit": "Percent"},
        >>>      {"identifier": "MSFT UW", "minimum": 0, "maximum": 5, "unit": "Percent"},
        >>>      {"identifier": "NVDA UW", "minimum": 0, "maximum": 5, "unit": "Percent"}
        >>>      ],
        >>>     as_of_date=dt.date(2025, 2, 24))

        2. The input is a dataframe

        >>> asset_constraints = AssetConstraint.build_many_constraints(
        >>>     pd.DataFrame([{"identifier": "AAPL UW", "minimum": 0, "maximum": 5, "unit": "Percent"},
        >>>                   {"identifier": "MSFT UW", "minimum": 0, "maximum": 5, "unit": "Percent"},
        >>>                   {"identifier": "NVDA UW", "minimum": 0, "maximum": 5, "unit": "Percent"}]),
        >>>     as_of_date=dt.date(2025, 2, 24)
        >>>     )

        Additional arguments can also be provided to the function and these will be used to resolve assets.
        Below we are adding a `type` and `assetClass` argument to tell the internal GS Security master to only return
        Single Stocks, Equity Indices, and ETFs.

         >>> asset_constraints = AssetConstraint.build_many_constraints(
        >>>     pd.DataFrame([{"identifier": "AAPL UW", "minimum": 0, "maximum": 5, "unit": "Percent"},
        >>>                   {"identifier": "MSFT UW", "minimum": 0, "maximum": 5, "unit": "Percent"},
        >>>                   {"identifier": "NVDA UW", "minimum": 0, "maximum": 5, "unit": "Percent"}]),
        >>>     as_of_date=dt.date(2025, 2, 24),
        >>>     fail_on_unresolved_positions=True,
        >>>     type=["Single Stock", "Index", "ETF"],
        >>>     assetClass=["Equity"]
        >>>     )

        """

        asset_constraints_df = pd.DataFrame(asset_constraints) if isinstance(asset_constraints, list) \
            else asset_constraints
        missing_columns = [col for col in ['identifier', 'minimum', "maximum", "unit"]
                           if col not in asset_constraints_df.columns]
        if missing_columns:
            raise MqValueError(f"The input is missing required columns: {', '.join(missing_columns)}")

        if len(set(asset_constraints_df['unit'].values.tolist())) > 1:
            raise MqValueError('All asset constraints must be in the same unit')

        if 'assetId' not in asset_constraints_df:
            identifiers = asset_constraints_df['identifier'].values.tolist()

            assets_resolved_as_records = resolve_assets_in_batches(identifiers=identifiers,
                                                                   as_of_date=as_of_date,
                                                                   batch_size=250,
                                                                   **kwargs
                                                                   )

            asset_constraints_df = pd.merge(asset_constraints_df, pd.DataFrame(assets_resolved_as_records),
                                            on='identifier',
                                            how='left')

            if fail_on_unresolved_positions and asset_constraints_df['id'].isnull().any():
                missing_ids = asset_constraints_df[asset_constraints_df['id'].isnull()]['identifier'].values.tolist()
                raise MqValueError(
                    f"The following identifiers could not be resolved on {as_of_date.strftime('%Y-%m-%d')}: "
                    f"{', '.join(missing_ids)}")
            else:
                asset_constraints_df = asset_constraints_df[asset_constraints_df['id'].notnull()]

            asset_constraints_df = asset_constraints_df.rename(
                columns={'id': 'assetId'})[['assetId', 'minimum', 'maximum', 'unit']]

        asset_constraints_df = asset_constraints_df.to_dict(orient='records')

        return [cls(asset=row.get('assetId'),
                    minimum=row.get('minimum'),
                    maximum=row.get('maximum'),
                    unit=OptimizationConstraintUnit(row.get('unit'))) for row in asset_constraints_df]


class CountryConstraint:

    def __init__(self,
                 country_name: str,
                 minimum: float = 0,
                 maximum: float = 100,
                 unit: OptimizationConstraintUnit = OptimizationConstraintUnit.PERCENT):
        """
        Constrain notional held in any particular country in the resulting optimization

        :param country_name: country name
        :param minimum: minimum
        :param maximum: maximum
        :param unit: the unit in which the min and max values are passed in with (defaults to percent)
        """
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

    @classmethod
    def build_many_constraints(cls,
                               country_constraints: Union[pd.DataFrame, List[Dict]]):
        """
        Create many country constraints from a dataframe or a list of dictionaries
        :param country_constraints: dataframe or list of dictionaries containing the country constraints

        :return: list of CountryConstraint objects

        :raises MqValueError: if the input is missing required columns "country", "minimum", "maximum", or "unit"
        :raises MqValueError: if the input country constraints are in more than one unit

        **Examples**

        1. The input is a list of dictionaries
        >>> country_constraints = CountryConstraint.build_many_constraints(
        >>>     [{"country": "USA", "minimum": 0, "maximum": 5, "unit": "Percent"},
        >>>      {"country": "Canada", "minimum": 0, "maximum": 5, "unit": "Percent"},
        >>>      {"country": "Germany", "minimum": 0, "maximum": 5, "unit": "Percent"}
        >>>      ])

        2. The input is a dataframe
        >>> country_constraints = CountryConstraint.build_many_constraints(
        >>>     pd.DataFrame([{"country": "USA", "minimum": 0, "maximum": 5, "unit": "Percent"},
        >>>                   {"country": "Canada", "minimum": 0, "maximum": 5, "unit": "Percent"},
        >>>                   {"country": "Germany", "minimum": 0, "maximum": 5, "unit": "Percent"}])
        >>>     )
        """
        country_constraints = pd.DataFrame(country_constraints) \
            if isinstance(country_constraints, list) else country_constraints

        missing_columns = [col for col in ['country', 'minimum', 'maximum', 'unit']
                           if col not in country_constraints.columns]
        if missing_columns:
            raise MqValueError(f"The input is missing required columns: {', '.join(missing_columns)}")
        country_constraints_as_records = country_constraints.to_dict(orient='records')

        return [cls(country_name=row.get('industry'),
                    minimum=row.get('minimum'),
                    maximum=row.get('maximum'),
                    unit=OptimizationConstraintUnit(row.get('unit'))) for row in country_constraints_as_records]


class SectorConstraint:

    def __init__(self,
                 sector_name: str,
                 minimum: float = 0,
                 maximum: float = 100,
                 unit: OptimizationConstraintUnit = OptimizationConstraintUnit.PERCENT):
        """
        Constrain notional held in any particular GICS Sector in the resulting optimization

        :param sector_name: sector name
        :param minimum: minimum
        :param maximum: maximum
        :param unit: the unit in which the min and max values are passed in with (defaults to percent)
        """
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
            raise MqValueError('Sector constraints can only be set by percent.')
        self.__unit = value

    def to_dict(self):
        return {
            'type': 'Sector',
            'name': self.sector_name,
            'min': self.minimum * 100 if self.unit == OptimizationConstraintUnit.DECIMAL else self.minimum,
            'max': self.maximum * 100 if self.unit == OptimizationConstraintUnit.DECIMAL else self.maximum
        }

    @classmethod
    def build_many_constraints(cls,
                               sector_constraints: Union[pd.DataFrame, List[Dict]]):
        """
        Create many sector constraints from a dataframe or a list of dictionaries
        :param sector_constraints: dataframe or list of dictionaries containing the sector constraints

        :return: list of SectorConstraint objects

        :raises MqValueError: if the input is missing required columns "sector", "minimum", "maximum", or "unit"
        :raises MqValueError: if the input sector constraints are in more than one unit

        **Examples**

        1. The input is a list of dictionaries
        >>> sector_constraints = SectorConstraint.build_many_constraints(
        >>>     [{"sector": "Technology", "minimum": 0, "maximum": 5, "unit": "Percent"},
        >>>      {"sector": "Healthcare", "minimum": 0, "maximum": 5, "unit": "Percent"},
        >>>      {"sector": "Finance", "minimum": 0, "maximum": 5, "unit": "Percent"}
        >>>      ])

        2. The input is a dataframe
        >>> sector_constraints = SectorConstraint.build_many_constraints(
        >>>     pd.DataFrame([{"sector": "Technology", "minimum": 0, "maximum": 5, "unit": "Percent"},
        >>>                   {"sector": "Healthcare", "minimum": 0, "maximum": 5, "unit": "Percent"},
        >>>                   {"sector": "Finance", "minimum": 0, "maximum": 5, "unit": "Percent"}])
        >>>     )
        """
        sector_constraints = pd.DataFrame(sector_constraints) \
            if isinstance(sector_constraints, list) else sector_constraints

        missing_columns = [col for col in ['sector', 'minimum', 'maximum', 'unit']
                           if col not in sector_constraints.columns]
        if missing_columns:
            raise MqValueError(f"The input is missing required columns: {', '.join(missing_columns)}")
        sector_constraints_as_records = sector_constraints.to_dict(orient='records')

        return [cls(sector_name=row.get('sector'),
                    minimum=row.get('minimum'),
                    maximum=row.get('maximum'),
                    unit=OptimizationConstraintUnit(row.get('unit'))) for row in sector_constraints_as_records]


class IndustryConstraint:

    def __init__(self,
                 industry_name: str,
                 minimum: float = 0,
                 maximum: float = 100,
                 unit: OptimizationConstraintUnit = OptimizationConstraintUnit.PERCENT):
        """
        Constrain notional held in any particular GICS Industry in the resulting optimization

        :param industry_name: industry name
        :param minimum: minimum
        :param maximum: maximum
        :param unit: the unit in which the min and max values are passed in with (defaults to percent)
        """
        if unit not in [OptimizationConstraintUnit.PERCENT, OptimizationConstraintUnit.DECIMAL]:
            raise MqValueError('Industry constraints can only be set by percent or decimal.')
        self.__industry_name = industry_name
        self.__minimum = minimum
        self.__maximum = maximum
        self.__unit = unit

    @property
    def industry_name(self) -> str:
        return self.__industry_name

    @industry_name.setter
    def industry_name(self, value: str):
        self.__industry_name = value

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
            raise MqValueError('Industry constraints can only be set by percent.')
        self.__unit = value

    def to_dict(self):
        return {
            'type': 'Industry',
            'name': self.industry_name,
            'min': self.minimum * 100 if self.unit == OptimizationConstraintUnit.DECIMAL else self.minimum,
            'max': self.maximum * 100 if self.unit == OptimizationConstraintUnit.DECIMAL else self.maximum
        }

    @classmethod
    def build_many_constraints(cls,
                               industry_constraints: Union[pd.DataFrame, List[Dict]]):
        """
        Create many industry constraints from a dataframe or a list of dictionaries
        :param industry_constraints: dataframe or list of dictionaries containing the industry constraints

        :return: list of IndustryConstraint objects

        :raises MqValueError: if the input is missing required columns "industry", "minimum", "maximum", or "unit"
        :raises MqValueError: if the input industry constraints are in more than one unit

        **Examples**

        1. The input is a list of dictionaries
        >>> industry_constraints = IndustryConstraint.build_many_constraints(
        >>>     [{"industry": "Software", "minimum": 0, "maximum": 5, "unit": "Percent"},
        >>>      {"industry": "Pharmaceuticals", "minimum": 0, "maximum": 5, "unit": "Percent"},
        >>>      {"industry": "Banking", "minimum": 0, "maximum": 5, "unit": "Percent"}
        >>>      ])

        2. The input is a dataframe
        >>> industry_constraints = IndustryConstraint.build_many_constraints(
        >>>     pd.DataFrame([{"industry": "Software", "minimum": 0, "maximum": 5, "unit": "Percent"},
        >>>                   {"industry": "Pharmaceuticals", "minimum": 0, "maximum": 5, "unit": "Percent"},
        >>>                   {"industry": "Banking", "minimum": 0, "maximum": 5, "unit": "Percent"}])
        >>>     )
        """
        industry_constraints = pd.DataFrame(industry_constraints) \
            if isinstance(industry_constraints, list) else industry_constraints

        missing_columns = [col for col in ['industry', 'minimum', 'maximum', 'unit']
                           if col not in industry_constraints.columns]
        if missing_columns:
            raise MqValueError(f"The input is missing required columns: {', '.join(missing_columns)}")
        industry_constraints_as_records = industry_constraints.to_dict(orient='records')

        return [cls(industry_name=row.get('industry'),
                    minimum=row.get('minimum'),
                    maximum=row.get('maximum'),
                    unit=OptimizationConstraintUnit(row.get('unit'))) for row in industry_constraints_as_records]


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

    @classmethod
    def build_many_constraints(cls,
                               factor_constraints: Union[pd.DataFrame, List[Dict]],
                               risk_model_id: str):
        """
        Create many factor constraints from a dataframe or a list of dictionaries
        :param factor_constraints: dataframe or list of dictionaries containing the factor constraints
        :param risk_model_id: the id of the risk model

        :return: list of FactorConstraint objects
        :raises MqValueError: if the input is missing required columns "factor" or "exposure"

        **Examples**
        1. The input is a list of dictionaries
        >>> factor_constraints = FactorConstraint.build_many_constraints(
        >>>     [{"factor": "Value", "exposure": 5000},
        >>>      {"factor": "Growth", "exposure": 1000},
        >>>      {"factor": "Beta", "exposure": 10000}
        >>>      ], "BARRA_USFAST")

        2. The input is a dataframe
        >>> factor_constraints = FactorConstraint.build_many_constraints(
        >>>     pd.DataFrame([{"factor": "Value", "exposure": 5000},
        >>>                   {"factor": "Growth", "exposure": 1000},
        >>>                   {"factor": "Beta", "exposure": 10000}
        >>>                   ]), "BARRA_USFAST")

        """
        factor_constraints_df = pd.DataFrame(factor_constraints) if isinstance(factor_constraints, list) \
            else factor_constraints

        missing_columns = [col for col in ['factor', 'exposure'] if col not in factor_constraints_df.columns]
        if missing_columns:
            raise MqValueError(f"The input is missing required columns: {', '.join(missing_columns)}")

        risk_model = FactorRiskModel.get(risk_model_id)
        factors = risk_model.get_many_factors(factor_names=factor_constraints_df['factor'].values.tolist())

        name_to_factor_obj = [{"factor": f.name, "factorObj": f} for f in factors]
        name_to_factor_obj_df = pd.DataFrame(name_to_factor_obj)

        factor_constraints_df = factor_constraints_df.merge(name_to_factor_obj_df, on='factor', how='inner')

        factor_constraints_df = (factor_constraints_df[["factorObj", "exposure"]]
                                 .rename(columns={"factorObj": "factor"}))

        all_constraints = factor_constraints_df.to_dict(orient='records')

        return [cls(factor=row.get('factor'), max_exposure=row.get('exposure')) for row in all_constraints]


class OptimizerUniverse:

    def __init__(self,
                 assets: Union[List[Asset], AssetUniverse] = None,
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
        specify the identifier type
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
    def assets(self, assets: List[Asset]):
        self.__assets = assets

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
        if isinstance(self.assets, AssetUniverse):
            self.assets.resolve()
            asset_ids = self.assets.asset_ids
        else:
            asset_ids = [asset.get_marquee_id() for asset in self.assets]
        as_dict = {
            'hedgeUniverse': {
                'assetIds': asset_ids,
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


class MaxProportionOfRiskByGroupConstraint:

    def __init__(self,
                 factors: List[Factor],
                 max_factor_proportion_of_risk: float,
                 unit: OptimizationConstraintUnit = OptimizationConstraintUnit.PERCENT):
        """
        Constrain the maximum proportion of risk coming from a group of factors in the final optimized result.

        :param factors: the list of factors
        :param max_factor_proportion_of_risk: the maximum proportion of risk
        :param unit: unit of proportion of risk
        """
        if unit not in [OptimizationConstraintUnit.PERCENT, OptimizationConstraintUnit.DECIMAL]:
            raise MqValueError('Max Factor Proportion of Risk can only be set by percent or decimal.')
        if unit == OptimizationConstraintUnit.PERCENT:
            max_factor_proportion_of_risk = max_factor_proportion_of_risk / 100
        self.__factors = factors
        self.__max_factor_proportion_of_risk = max_factor_proportion_of_risk
        self.__unit = unit

    @property
    def factors(self) -> List[Factor]:
        return self.__factors

    @factors.setter
    def factors(self, value: List[Factor]):
        self.__factors = value

    @property
    def max_factor_proportion_of_risk(self) -> float:
        return self.__max_factor_proportion_of_risk

    @max_factor_proportion_of_risk.setter
    def max_factor_proportion_of_risk(self, value: float):
        self.__max_factor_proportion_of_risk = value

    def to_dict(self):
        return {
            'factors': [f.name for f in self.factors],
            'max': self.max_factor_proportion_of_risk
        }


class OptimizerConstraints:

    def __init__(self,
                 asset_constraints: List[AssetConstraint] = [],
                 country_constraints: List[CountryConstraint] = [],
                 sector_constraints: List[SectorConstraint] = [],
                 industry_constraints: List[IndustryConstraint] = [],
                 factor_constraints: List[FactorConstraint] = [],
                 max_factor_proportion_of_risk: MaxFactorProportionOfRiskConstraint = None,
                 max_proportion_of_risk_by_groups: List[MaxProportionOfRiskByGroupConstraint] = None):
        """Set of Constraints for the optimizer

        :param asset_constraints: list of asset constraints
        :param country_constraints: list of country constraints
        :param sector_constraints: list of sector constraints
        :param industry_constraints: list of industry constraints
        :param factor_constraints: list of factor constraints
        :param max_factor_proportion_of_risk: maximum proportion of risk
        :param max_proportion_of_risk_by_groups: maximum proportion of risk by groups
        """
        self.__asset_constraints = asset_constraints
        self.__country_constraints = country_constraints
        self.__sector_constraints = sector_constraints
        self.__industry_constraints = industry_constraints
        self.__factor_constraints = factor_constraints
        self.__max_factor_proportion_of_risk = max_factor_proportion_of_risk
        self.__max_proportion_of_risk_by_groups = max_proportion_of_risk_by_groups

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
    def industry_constraints(self) -> List[IndustryConstraint]:
        return self.__industry_constraints

    @industry_constraints.setter
    def industry_constraints(self, value: List[IndustryConstraint]):
        self.__industry_constraints = value

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

    @property
    def max_proportion_of_risk_by_groups(self) -> List[MaxProportionOfRiskByGroupConstraint]:
        return self.__max_proportion_of_risk_by_groups

    @max_proportion_of_risk_by_groups.setter
    def max_proportion_of_risk_by_groups(self, value: List[MaxProportionOfRiskByGroupConstraint]):
        self.__max_proportion_of_risk_by_groups = value

    def to_dict(self):
        types = set([c.unit for c in self.asset_constraints])
        if len(types) > 1:
            raise MqValueError('All asset constraints need to have the same unit')
        constrain_by_notional = len(self.asset_constraints) > 0 and types.pop() == OptimizationConstraintUnit.NOTIONAL
        classification_constraints = self.country_constraints + self.sector_constraints + self.industry_constraints
        as_dict = {
            'assetConstraints': [c.to_dict() for c in self.asset_constraints],
            'classificationConstraints': [c.to_dict() for c in classification_constraints],
            'factorConstraints': [c.to_dict() for c in self.factor_constraints],
            'constrainAssetsByNotional': constrain_by_notional
        }

        if self.max_factor_proportion_of_risk:
            as_dict['maxFactorMCTR'] = self.max_factor_proportion_of_risk.max_factor_proportion_of_risk

        if self.max_proportion_of_risk_by_groups:
            as_dict['maxFactorMCTRByGroup'] = [g.to_dict() for g in self.max_proportion_of_risk_by_groups]

        return as_dict


class ConstraintPriorities:

    def __init__(self,
                 min_sector_weights: PrioritySetting = None,
                 max_sector_weights: PrioritySetting = None,
                 min_industry_weights: PrioritySetting = None,
                 max_industry_weights: PrioritySetting = None,
                 min_region_weights: PrioritySetting = None,
                 max_region_weights: PrioritySetting = None,
                 min_country_weights: PrioritySetting = None,
                 max_country_weights: PrioritySetting = None,
                 style_factor_exposures: PrioritySetting = None,
                 ):
        """
        Priority of the constraint from 0-5 (prioritized in that order). The optimization will fail if it cannot meet a
        constraint with 0 priority.  A constraint with priority of 1-5 can be called a relaxed constraint, which means
        that the optimization will make its best effort to meet the constraint but will not fail if it cannot. A
        constraint with a lower priority will take precedence over a constraint with a higher priority.
        :param min_sector_weights: constraint priority of the minimum sector weight constraints
        :param max_sector_weights: constraint priority of the maximum sector weight constraints
        :param min_industry_weights: constraint priority of the minimum industry weight constraints
        :param max_industry_weights: constraint priority of the maximum industry weight constraints
        :param min_region_weights: constraint priority of the minimum region weight constraints
        :param max_region_weights: constraint priority of the maximum region weight constraints
        :param min_country_weights: constraint priority of the minimum country weight constraints
        :param max_country_weights: constraint priority of the maximum country weight constraints
        :param style_factor_exposures: constraint priority of the style factor exposure constraints
        """
        self.__min_sector_weights = min_sector_weights
        self.__max_sector_weights = max_sector_weights
        self.__min_industry_weights = min_industry_weights
        self.__max_industry_weights = max_industry_weights
        self.__min_region_weights = min_region_weights
        self.__max_region_weights = max_region_weights
        self.__min_country_weights = min_country_weights
        self.__max_country_weights = max_country_weights
        self.__style_factor_exposures = style_factor_exposures

    @property
    def min_sector_weights(self) -> PrioritySetting:
        return self.__min_sector_weights

    @min_sector_weights.setter
    def min_sector_weights(self, value: PrioritySetting):
        self.__min_sector_weights = value

    @property
    def max_sector_weights(self) -> PrioritySetting:
        return self.__max_sector_weights

    @max_sector_weights.setter
    def max_sector_weights(self, value: PrioritySetting):
        self.__max_sector_weights = value

    @property
    def min_industry_weights(self) -> PrioritySetting:
        return self.__min_industry_weights

    @min_industry_weights.setter
    def min_industry_weights(self, value: PrioritySetting):
        self.__min_industry_weights = value

    @property
    def max_industry_weights(self) -> PrioritySetting:
        return self.__max_industry_weights

    @max_industry_weights.setter
    def max_industry_weights(self, value: PrioritySetting):
        self.__max_industry_weights = value

    @property
    def min_region_weights(self) -> PrioritySetting:
        return self.__min_region_weights

    @min_region_weights.setter
    def min_region_weights(self, value: PrioritySetting):
        self.__min_region_weights = value

    @property
    def max_region_weights(self) -> PrioritySetting:
        return self.__max_region_weights

    @max_region_weights.setter
    def max_region_weights(self, value: PrioritySetting):
        self.__max_region_weights = value

    @property
    def min_country_weights(self) -> PrioritySetting:
        return self.__min_country_weights

    @min_country_weights.setter
    def min_country_weights(self, value: PrioritySetting):
        self.__min_country_weights = value

    @property
    def max_country_weights(self) -> PrioritySetting:
        return self.__max_country_weights

    @max_country_weights.setter
    def max_country_weights(self, value: PrioritySetting):
        self.__max_country_weights = value

    @property
    def style_factor_exposures(self) -> PrioritySetting:
        return self.__style_factor_exposures

    @style_factor_exposures.setter
    def style_factor_exposures(self, value: PrioritySetting):
        self.__style_factor_exposures = value

    def to_dict(self) -> Dict:
        as_dict = {
            'minSectorWeights': self.min_sector_weights,
            'maxSectorWeights': self.max_sector_weights,
            'minIndustryWeights': self.min_industry_weights,
            'maxIndustryWeights': self.max_industry_weights,
            'minRegionWeights': self.min_region_weights,
            'maxRegionWeights': self.max_region_weights,
            'minCountryWeights': self.min_country_weights,
            'maxCountryWeights': self.max_country_weights,
            'styleExposures': self.style_factor_exposures
        } if self is not None else {}
        as_dict = {k: as_dict[k].value for k in as_dict.keys() if as_dict[k] is not None}
        return as_dict if len(as_dict.keys()) > 0 else None


class OptimizerSettings:

    def __init__(self,
                 notional: float = 10000000,
                 allow_long_short: bool = False,
                 min_names: float = 0,
                 max_names: float = 100,
                 min_weight_per_constituent: float = None,
                 max_weight_per_constituent: float = None,
                 max_adv: float = 15,
                 constraint_priorities: ConstraintPriorities = None):
        """
        Optimizer settings

        :param notional: the max gross notional of the optimization
        :param allow_long_short: allow a long/short optimization
        :param min_names: minimum number of assets in the optimization
        :param max_names: maximum number of assets in the optimization
        :param min_weight_per_constituent: minimum weight of each constituent in the optimization
        :param max_weight_per_constituent: maximum weight of each constituent in the optimization
        :param max_adv: maximum average daily volume of each constituent in the optimization (in percent)
        :param constraint_priorities: constraint priorities
        """
        self.__notional = notional
        self.__allow_long_short = allow_long_short
        self.__min_names = min_names
        self.__max_names = max_names
        self.__min_weight_per_constituent = min_weight_per_constituent
        self.__max_weight_per_constituent = max_weight_per_constituent
        self.__max_adv = max_adv
        self.__constraint_priorities = constraint_priorities

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
    def min_weight_per_constituent(self) -> float:
        return self.__min_weight_per_constituent

    @min_weight_per_constituent.setter
    def min_weight_per_constituent(self, value: float):
        self.__min_weight_per_constituent = value

    @property
    def max_weight_per_constituent(self) -> float:
        return self.__max_weight_per_constituent

    @max_weight_per_constituent.setter
    def max_weight_per_constituent(self, value: float):
        self.__max_weight_per_constituent = value

    @property
    def max_names(self) -> float:
        return self.__max_names

    @max_names.setter
    def max_names(self, value: float):
        self.__max_names = value

    @property
    def max_adv(self) -> float:
        return self.__max_adv

    @max_adv.setter
    def max_adv(self, value: float):
        self.__max_adv = value

    @property
    def constraint_priorities(self) -> ConstraintPriorities:
        return self.__constraint_priorities

    @constraint_priorities.setter
    def constraint_priorities(self, value: ConstraintPriorities):
        self.__constraint_priorities = value

    def to_dict(self):
        as_dict = {
            'hedgeNotional': self.notional,
            'allowLongShort': self.allow_long_short,
            'minNames': self.min_names,
            'maxNames': self.max_names,
            'maxAdvPercentage': self.max_adv
        }
        if self.min_weight_per_constituent:
            as_dict['minWeight'] = self.min_weight_per_constituent * 100
        if self.max_weight_per_constituent:
            as_dict['maxWeight'] = self.max_weight_per_constituent * 100
        if self.constraint_priorities:
            as_dict['constraintPrioritySettings'] = self.constraint_priorities.to_dict()
        return as_dict


class TurnoverConstraint:

    def __init__(self,
                 turnover_portfolio: PositionSet,
                 max_turnover_percent: float,
                 turnover_notional_type: Optional[TurnoverNotionalType] = None):
        """
        Specifying a list of positions and max turnover from those positions in the optimization result

        :param turnover_portfolio: turnover portfolio
        :param max_turnover_percent: max turnover as a percent (ex: 80 = a minimal overlap of 20% in notional of the
        specified positions and the optimization
        """
        self.__turnover_portfolio = turnover_portfolio
        self.__max_turnover_percent = max_turnover_percent
        self.__turnover_notional_type = turnover_notional_type

    @property
    def turnover_portfolio(self) -> PositionSet:
        return self.__turnover_portfolio

    @turnover_portfolio.setter
    def turnover_portfolio(self, value: PositionSet):
        self.__turnover_portfolio = value

    @property
    def max_turnover_percent(self) -> float:
        return self.__max_turnover_percent

    @max_turnover_percent.setter
    def max_turnover_percent(self, value: float):
        self.__max_turnover_percent = value

    @property
    def turnover_notional_type(self):
        return self.__turnover_notional_type

    @turnover_notional_type.setter
    def turnover_notional_type(self, value: Optional[TurnoverNotionalType]):
        self.__turnover_notional_type = value

    def to_dict(self):
        positions = self.turnover_portfolio.positions
        payload = {
            'turnoverPortfolio': [{'assetId': p.asset_id, 'quantity': p.quantity} for p in positions],
            'maxTurnoverPercentage': self.max_turnover_percent
        }
        if self.turnover_notional_type:
            payload['turnoverNotionalType'] = self.turnover_notional_type.value
        return payload


def _ensure_completed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        if self._OptimizerStrategy__result is None:
            raise MqValueError('Please run the optimization before calling this method')
        return func(*args, **kwargs)

    return wrapper


class OptimizerStrategy:

    def __init__(self,
                 initial_position_set: PositionSet,
                 universe: OptimizerUniverse,
                 risk_model: FactorRiskModel,
                 constraints: OptimizerConstraints = None,
                 turnover: TurnoverConstraint = None,
                 settings: OptimizerSettings = None,
                 objective: OptimizerObjective = OptimizerObjective.MINIMIZE_FACTOR_RISK,
                 objective_parameters: OptimizerObjectiveParameters = None):
        """
        A strategy that can be passed into the optimizer and run

        :param initial_position_set: a position set correlating to your original holdings as of a specific date
        :param universe: universe from which to choose optimization assets
        :param risk_model: risk model with which to calculate risk
        :param constraints: constraints for the optimization
        :param turnover: turnover constraints for the optimization
        :param settings: settings for the optimization
        :param objective: objective for the optimization
        """
        self.__initial_position_set = initial_position_set
        self.__universe = universe
        self.__risk_model = risk_model
        self.__constraints = constraints
        self.__turnover = turnover
        self.__settings = settings
        self.__objective = objective
        self.__result = None
        self.__objective_parameters = objective_parameters

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
    def turnover(self) -> TurnoverConstraint:
        return self.__turnover

    @turnover.setter
    def turnover(self, value: TurnoverConstraint):
        self.__turnover = value

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

    @property
    def objective_parameters(self):
        return self.__objective_parameters

    @objective_parameters.setter
    def objective_parameters(self):
        return self.__objetive_parameters

    def to_dict(self, fail_on_unpriced_positions: bool = True):
        """Converts input to suitable json payload for optimizer. Does not modify initial_position_set"""
        if self.constraints is None:
            self.constraints = OptimizerConstraints()
        if self.settings is None:
            self.settings = OptimizerSettings()

        backtest_start_date = self.initial_position_set.date - relativedelta(weeks=1)
        positions_frame = self.initial_position_set.to_frame()
        if self.initial_position_set.reference_notional:
            positions_as_dict = positions_frame[['asset_id', 'weight']]
        else:
            positions_as_dict = positions_frame[['asset_id', 'quantity']]

        positions_as_dict = positions_as_dict.rename(columns={'asset_id': 'assetId'}).to_dict(orient='records')

        parameters = {
            'hedgeTarget': {
                'positions': positions_as_dict
            },
            'hedgeDate': self.initial_position_set.date.strftime('%Y-%m-%d'),
            'backtestStartDate': backtest_start_date.strftime('%Y-%m-%d'),
            'backtestEndDate': self.initial_position_set.date.strftime('%Y-%m-%d'),
            'comparisons': [],
            'fxHedged': False,
            'marketParticipationRate': 10
        }
        constraints = self.constraints.to_dict()
        for key in constraints:
            if constraints[key] is not None:
                parameters[key] = constraints[key]
        settings = self.settings.to_dict()
        for key in settings:
            if settings[key] is not None:
                parameters[key] = settings[key]
        universe = self.universe.to_dict()
        for key in universe:
            if universe[key] is not None:
                parameters[key] = universe[key]
        parameters['riskModel'] = self.risk_model.id
        if self.turnover:
            if self.turnover.turnover_portfolio.reference_notional is not None:
                self.turnover.turnover_portfolio.price()
            turnover_dict = self.turnover.to_dict()
            for key in turnover_dict:
                if turnover_dict[key] is not None:
                    parameters[key] = turnover_dict[key]

        # Price initial_position_set if needed
        if self.initial_position_set.reference_notional is not None:
            parameters['targetNotional'] = self.initial_position_set.reference_notional

        if self.__objective_parameters is not None:
            parameters['hedgeObjectiveParameters'] = self.__objective_parameters.to_dict()

        payload = {
            'positions': positions_as_dict,
            'parameters': {
                'currency': 'USD',
                'pricingDate': self.initial_position_set.date.strftime('%Y-%m-%d'),
                'useUnadjustedClosePrice': False,  # Optimizer uses adjusted prices for all calculations
                'frequency': 'End Of Day',
                'priceRegardlessOfAssetsMissingPrices': not fail_on_unpriced_positions,
                'fallbackDate': '5d'
            }
        }
        if self.initial_position_set.reference_notional is not None:
            payload['parameters']['targetNotional'] = self.initial_position_set.reference_notional
        try:
            price_results = GsSession.current._post('/price/positions', payload)
        except Exception as e:
            raise MqValueError(f'There was an error pricing your positions: {e}')
        if 'errorMessage' in price_results:
            if len(price_results.get('assetIdsMissingPrices', [])) > 0:
                _logger.warning(f'Marquee is missing prices on {self.initial_position_set.date} for '
                                f'the following assets: {price_results["assetIdsMissingPrices"]}. ')
            raise MqValueError(f'There was an error pricing your positions: {price_results["errorMessage"]}')
        if self.initial_position_set.reference_notional is None:
            parameters['targetNotional'] = price_results.get('actualNotional')
        else:
            parameters['hedgeTarget']['positions'] = [{'assetId': p['assetId'], 'quantity': p['quantity']}
                                                      for p in price_results.get('positions', [])]
        return {
            'objective': self.objective.value,
            'parameters': parameters
        }

    def run(self,
            optimizer_type: OptimizerType = OptimizerType.AXIOMA_PORTFOLIO_OPTIMIZER,
            fail_on_unpriced_positions: bool = True):
        """
        Run an optimization strategy, after which you can use the .get_optimization or get_optimized_position_set
        functions to pull results

        :param optimizer_type: optimizer type
        :param fail_on_unpriced_positions: whether to fail the calculations if some of the portfolio positions do not
        have pricing data in Marquee. If set to false, unpriced assets will be sifted out before the optimization is run
        """
        if optimizer_type is None:
            raise MqValueError('You must pass an optimizer type.')
        if optimizer_type == OptimizerType.AXIOMA_PORTFOLIO_OPTIMIZER:
            strategy_as_dict = self.to_dict(fail_on_unpriced_positions)
            counter = 5
            while counter > 0:
                try:
                    optimization_results = GsHedgeApi.calculate_hedge(strategy_as_dict)
                    if optimization_results.get('result') is None:
                        if 'errorMessage' in optimization_results:
                            raise MqValueError(f"The optimizer returned an error: "
                                               f"{optimization_results.get('errorMessage')}. "
                                               f"Please adjust the constraints"
                                               f"or contact the Marquee team for assistance")
                        elif counter == 1:
                            raise MqValueError(
                                'Error calculating an optimization. Please contact the Marquee team for assistance.')
                        counter -= 1
                    else:
                        self.__result = optimization_results['result']
                        counter = 0
                except Exception:
                    if counter == 1:
                        raise MqValueError(
                            'Error calculating an optimization. Please contact the Marquee team for assistance.')
                    counter -= 1

    def __construct_position_set_from_hedge_result(self, result_key: str, by_weight: bool = True):
        result = self.__result[result_key]
        return PositionSet(
            date=self.initial_position_set.date,
            reference_notional=result['netExposure'] if by_weight else None,
            positions=[Position(identifier=asset.get('bbid', asset['name']),
                                asset_id=asset['assetId'],
                                quantity=asset['shares'] if not by_weight else None,
                                weight=asset['weight']) for asset in result['constituents']])

    @_ensure_completed
    def get_optimization(self, by_weight: bool = False):
        """
        Get the optimization results

        :param by_weight: whether to return position set with weights instead of quantities
        """
        return self.__construct_position_set_from_hedge_result('hedge', by_weight)

    @_ensure_completed
    def get_optimized_position_set(self, by_weight: bool = False):
        """
        Get the optimized position set, which is a result of applying the optimization to the target

        :param by_weight: whether to return position set with weights instead of quantities
        """
        return self.__construct_position_set_from_hedge_result('hedgedTarget', by_weight)
