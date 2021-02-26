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
from typing import List, Dict
import pandas as pd

from gs_quant.api.gs.risk_models import GsRiskModelApi
from gs_quant.target.risk_models import RiskModelData, RiskModelCalendar, RiskModelFactor, \
    DataAssetsRequest, Measure, Format, UniverseIdentifier


class RiskModel:

    def __init__(self, model_id: str):
        self.model = GsRiskModelApi.get_risk_model(model_id)

    def delete(self):
        """ Delete existing risk model """
        return GsRiskModelApi.delete_risk_model(self.model.id)

    def get_id(self) -> str:
        """ Retrieve risk model id for existing risk model """
        return self.model.id

    def get_term(self) -> str:
        """ Retrieve risk model term for existing risk model """
        return self.model.term

    def get_coverage(self) -> str:
        """ Retrieve risk model coverage for existing risk model """
        return self.model.coverage

    def get_description(self) -> str:
        """ Retrieve risk model description for existing risk model """
        return self.model.description

    def get_name(self) -> str:
        """ Retrieve risk model name for existing risk model """
        return self.model.name

    def get_dates(self, start_date: dt.date = None, end_date: dt.date = None) -> List:
        """ Retrieve risk model dates for existing risk model """
        return GsRiskModelApi.get_risk_model_dates(self.model.id, start_date, end_date)

    def get_factor(self, factor_id: str) -> RiskModelFactor:
        """ Retrieve risk model factor from model and factor ids """
        return GsRiskModelApi.get_risk_model_factor(self.model.id, factor_id)

    def create_factor(self, factor: RiskModelFactor):
        """ Create a new risk model factor """
        GsRiskModelApi.create_risk_model_factor(self.model.id, factor)

    def update_factor(self, factor_id: str, factor: RiskModelFactor):
        """ Update existing risk model factor """
        GsRiskModelApi.update_risk_model_factor(self.model.id, factor_id, factor)

    def delete_factor(self, factor_id: str):
        """ Delete a risk model factor """
        GsRiskModelApi.delete_risk_model_factor(self.model.id, factor_id)

    def get_factor_data(self,
                        start_date: dt.date = None,
                        end_date: dt.date = None,
                        identifiers: List[str] = None,
                        include_performance_curve: bool = None) -> List[Dict]:
        """ Retrieve factor data for existing risk model """
        start_date = dt.datetime.strptime(
            GsRiskModelApi.get_risk_model_dates(self.model.id)[0], '%Y-%m-%d') if not start_date else start_date
        id_to_category_for_date_range = GsRiskModelApi.get_risk_model_data(model_id=self.model.id,
                                                                           start_date=start_date,
                                                                           end_date=end_date,
                                                                           assets=None,
                                                                           measures=[Measure.Factor_Id,
                                                                                     Measure.Factor_Category],
                                                                           limit_factors=False,
                                                                           data_format=None).get('results')
        factor_id_to_category = _build_id_to_category(id_to_category_for_date_range)
        factor_data = GsRiskModelApi.get_risk_model_factor_data(self.model.id,
                                                                start_date,
                                                                end_date,
                                                                identifiers,
                                                                include_performance_curve)
        for factor in factor_data:
            factor['factorCategory'] = factor_id_to_category.get(factor.get('identifier'), factor.get('name'))
        return factor_data

    def get_calendar(self, start_date: dt.date = None, end_date: dt.date = None) -> RiskModelCalendar:
        """ Retrieve risk model calendar for existing risk model between start and end date """
        calendar = GsRiskModelApi.get_risk_model_calendar(self.model.id)
        if not start_date and not end_date:
            return calendar
        start_idx = _get_closest_date_index(start_date, calendar.business_dates, 'after') if start_date else 0
        end_idx = _get_closest_date_index(end_date, calendar.business_dates, 'before') if end_date else len(
            calendar.business_dates)
        return RiskModelCalendar(calendar.business_dates[start_idx:end_idx + 1])

    def upload_calendar(self, calendar: RiskModelCalendar):
        """ Upload risk model calendar to existing risk model """
        return GsRiskModelApi.upload_risk_model_calendar(self.model.id, calendar)

    def get_asset_universe(self,
                           start_date: dt.date,
                           end_date: dt.date = None,
                           assets: DataAssetsRequest = None,
                           data_format: Format = None) -> List:
        """ Retrieve asset universe data for existing risk model """
        if not assets.universe and not end_date:
            end_date = start_date
        results = GsRiskModelApi.get_risk_model_data(model_id=self.model.id,
                                                     start_date=start_date,
                                                     end_date=end_date,
                                                     assets=assets,
                                                     measures=[Measure.Asset_Universe],
                                                     limit_factors=False,
                                                     data_format=data_format).get('results')
        return [{'date': data.get('date'), 'universe': data.get('assetData').get('universe')} for data in results]

    def get_historical_beta(self,
                            start_date: dt.date,
                            end_date: dt.date = None,
                            assets: DataAssetsRequest = None,
                            data_format: Format = None) -> Dict:
        """ Retrieve historical beta data for existing risk model """
        results = GsRiskModelApi.get_risk_model_data(model_id=self.model.id,
                                                     start_date=start_date,
                                                     end_date=end_date,
                                                     assets=assets,
                                                     measures=[Measure.Historical_Beta, Measure.Asset_Universe],
                                                     limit_factors=False,
                                                     data_format=data_format).get('results')
        return _build_asset_data_map(results, assets, 'historicalBeta')

    def get_total_risk(self,
                       start_date: dt.date,
                       end_date: dt.date = None,
                       assets: DataAssetsRequest = None,
                       data_format: Format = None) -> Dict:
        """ Retrieve total risk data for existing risk model """
        results = GsRiskModelApi.get_risk_model_data(model_id=self.model.id,
                                                     start_date=start_date,
                                                     end_date=end_date,
                                                     assets=assets,
                                                     measures=[Measure.Total_Risk, Measure.Asset_Universe],
                                                     limit_factors=False,
                                                     data_format=data_format).get('results')
        return _build_asset_data_map(results, assets, 'totalRisk')

    def get_specific_risk(self,
                          start_date: dt.date,
                          end_date: dt.date = None,
                          assets: DataAssetsRequest = None,
                          data_format: Format = None) -> Dict:
        """ Retrieve specific risk data for existing risk model """
        results = GsRiskModelApi.get_risk_model_data(model_id=self.model.id,
                                                     start_date=start_date,
                                                     end_date=end_date,
                                                     assets=assets,
                                                     measures=[Measure.Specific_Risk, Measure.Asset_Universe],
                                                     limit_factors=False,
                                                     data_format=data_format).get('results')
        return _build_asset_data_map(results, assets, 'specificRisk')

    def get_residual_variance(self,
                              start_date: dt.date,
                              end_date: dt.date = None,
                              assets: DataAssetsRequest = None,
                              data_format: Format = None) -> Dict:
        """ Retrieve residual variance data for existing risk model """
        if not assets:
            assets = DataAssetsRequest(UniverseIdentifier.gsid, [])
        if assets.identifier != UniverseIdentifier.gsid:
            raise ValueError('Cannot query residual variance by identifiers other than gsid')
        results = GsRiskModelApi.get_risk_model_data(model_id=self.model.id,
                                                     start_date=start_date,
                                                     end_date=end_date,
                                                     assets=assets,
                                                     measures=[Measure.Residual_Variance, Measure.Asset_Universe],
                                                     limit_factors=False,
                                                     data_format=data_format).get('results')
        return _build_asset_data_map(results, assets, 'residualVariance')

    def get_universe_factor_exposure(self,
                                     start_date: dt.date,
                                     end_date: dt.date = None,
                                     assets: DataAssetsRequest = None,
                                     data_format: Format = None) -> Dict:
        """ Retrieve universe factor exposure data for existing risk model """
        results = GsRiskModelApi.get_risk_model_data(model_id=self.model.id,
                                                     start_date=start_date,
                                                     end_date=end_date,
                                                     assets=assets,
                                                     measures=[Measure.Universe_Factor_Exposure,
                                                               Measure.Asset_Universe],
                                                     limit_factors=False,
                                                     data_format=data_format).get('results')
        return _build_asset_data_map(results, assets, 'factorExposure')

    def get_factor_returns_by_name(self,
                                   start_date: dt.date,
                                   end_date: dt.date = None,
                                   data_format: Format = None) -> Dict:
        """ Retrieve factor return data for existing risk model """
        results = GsRiskModelApi.get_risk_model_data(model_id=self.model.id,
                                                     start_date=start_date,
                                                     end_date=end_date,
                                                     assets=None,
                                                     measures=[Measure.Factor_Return, Measure.Factor_Name,
                                                               Measure.Factor_Id],
                                                     limit_factors=False,
                                                     data_format=data_format).get('results')
        factor_data = self.get_factor_data(start_date, end_date)
        return _build_factor_data_map(factor_data, results, 'factorName')

    def get_factor_returns_by_id(self,
                                 start_date: dt.date,
                                 end_date: dt.date = None,
                                 data_format: Format = None) -> Dict:
        """ Retrieve factor return data for existing risk model """
        results = GsRiskModelApi.get_risk_model_data(model_id=self.model.id,
                                                     start_date=start_date,
                                                     end_date=end_date,
                                                     assets=None,
                                                     measures=[Measure.Factor_Return, Measure.Factor_Name,
                                                               Measure.Factor_Id],
                                                     limit_factors=False,
                                                     data_format=data_format).get('results')
        factor_data = self.get_factor_data(start_date, end_date)
        return _build_factor_data_map(factor_data, results, 'id')

    def get_covariance_matrix(self,
                              start_date: dt.date,
                              end_date: dt.date = None,
                              data_format: Format = None) -> Dict:
        """ Retrieve covariance matrix data for existing risk model """
        return GsRiskModelApi.get_risk_model_data(model_id=self.model.id,
                                                  start_date=start_date,
                                                  end_date=end_date,
                                                  assets=None,
                                                  measures=[Measure.Covariance_Matrix, Measure.Factor_Name,
                                                            Measure.Factor_Id],
                                                  limit_factors=False,
                                                  data_format=data_format).get('results')

    def get_issuer_specific_covariance(self,
                                       start_date: dt.date,
                                       end_date: dt.date = None,
                                       assets: DataAssetsRequest = None,
                                       data_format: Format = None) -> Dict:
        """ Retrieve issuer specific covariance data for existing risk model """
        return GsRiskModelApi.get_risk_model_data(model_id=self.model.id,
                                                  start_date=start_date,
                                                  end_date=end_date,
                                                  assets=assets,
                                                  measures=[Measure.Issuer_Specific_Covariance],
                                                  limit_factors=False,
                                                  data_format=data_format).get('results')

    def get_factor_portfolios(self,
                              start_date: dt.date,
                              end_date: dt.date = None,
                              assets: DataAssetsRequest = None,
                              data_format: Format = None) -> Dict:
        """ Retrieve factor portfolios data for existing risk model """
        return GsRiskModelApi.get_risk_model_data(model_id=self.model.id,
                                                  start_date=start_date,
                                                  end_date=end_date,
                                                  assets=assets,
                                                  measures=[Measure.Factor_Portfolios],
                                                  limit_factors=False,
                                                  data_format=data_format).get('results')

    def get_data(self,
                 measures: List[Measure],
                 start_date: dt.date,
                 end_date: dt.date = None,
                 assets: DataAssetsRequest = None,
                 limit_factors: bool = None,
                 data_format: Format = None) -> Dict:
        """ Retrieve data for multiple measures for existing risk model """
        return GsRiskModelApi.get_risk_model_data(model_id=self.model.id,
                                                  start_date=start_date,
                                                  end_date=end_date,
                                                  assets=assets,
                                                  measures=measures,
                                                  limit_factors=limit_factors,
                                                  data_format=data_format)

    def upload_data(self, data: RiskModelData):
        """ Upload risk model data to existing risk model """
        GsRiskModelApi.upload_risk_model_data(self.model.id, data)

    def upload_partial_data(self, data: RiskModelData, target_universe_size: float = None):
        """ Upload partial risk model data to existing risk model, if repeats in partial upload,
            newer posted data will replace existing data on upload day """
        GsRiskModelApi.upload_risk_model_data(self.model.id,
                                              data,
                                              partial_upload=True,
                                              target_universe_size=target_universe_size)


def to_frame(data):
    return pd.DataFrame(data)


def _get_closest_date_index(date: dt.date, dates: List[str], direction: str) -> int:
    for i in range(50):
        for index in range(len(dates)):
            if direction == 'before':
                next_date = (date - dt.timedelta(days=i)).strftime('%Y-%m-%d')
            else:
                next_date = (date + dt.timedelta(days=i)).strftime('%Y-%m%-d')
            if next_date == dates[index]:
                return index
    return -1


def _build_asset_data_map(results: List, assets: DataAssetsRequest, measure: str) -> dict:
    if not results:
        return {}
    universe = assets.universe if assets.universe else results[0].get('assetData').get('universe')
    data_map = {}
    for asset in universe:
        date_list = {}
        for row in results:
            i = row.get('assetData').get('universe').index(asset)
            if i != -1:
                date_list[row.get('date')] = row.get('assetData').get(measure)[i]
        data_map[asset] = date_list
    return data_map


def _build_factor_data_map(factor_data: List, results: List, identifier: str) -> dict:
    factor_data = [data.get('identifier') for data in factor_data if data.get('type') == 'Factor']
    data_map = {}
    for factor in factor_data:
        date_list = {}
        factor_name = factor
        for row in results:
            for data in row.get('factorData'):
                if data.get('factorId') == factor:
                    factor_name = factor if identifier == 'id' else data.get(identifier)
                    date_list[row.get('date')] = data.get('factorReturn')
        data_map[factor_name] = date_list
    return data_map


def _build_id_to_category(id_to_category_for_date_range: List):
    id_list = list()
    category_list = list()
    for factor_data_on_date in id_to_category_for_date_range:
        factor_data = factor_data_on_date.get('factorData')
        for factor in factor_data:
            if factor.get('factorId') not in id_list:
                id_list.append(factor.get('factorId'))
                category_list.append(factor.get('factorCategory'))
    return dict(zip(id_list, category_list))
