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
from typing import Tuple, Union, List

from gs_quant.common import PositionType
from gs_quant.instrument import Instrument
from gs_quant.session import GsSession
from gs_quant.target.common import RiskRequest
from gs_quant.target.portfolios import Portfolio, Position, PositionSet
from gs_quant.target.reports import Report
from gs_quant.target.risk_models import Term

_logger = logging.getLogger(__name__)


class GsPortfolioApi:
    """GS Asset API client implementation"""

    @classmethod
    def get_portfolios(cls,
                       portfolio_ids: List[str] = None,
                       portfolio_names: List[str] = None,
                       limit: int = 100) -> Tuple[Portfolio, ...]:
        url = '/portfolios?'
        if portfolio_ids:
            url += f'&id={"&id=".join(portfolio_ids)}'
        if portfolio_names:
            url += f'&name={"&name=".join(portfolio_names)}'
        return GsSession.current._get(f'{url}&limit={limit}', cls=Portfolio)['results']

    @classmethod
    def get_portfolio(cls, portfolio_id: str) -> Portfolio:
        return GsSession.current._get('/portfolios/{id}'.format(id=portfolio_id), cls=Portfolio)

    @classmethod
    def get_portfolio_by_name(cls, name: str) -> Portfolio:
        ret = GsSession.current._get('/portfolios?name={}'.format(name))
        num_found = ret.get('totalResults', 0)

        if num_found == 0:
            raise ValueError('Portfolio {} not found'.format(name))
        elif num_found > 1:
            raise ValueError('More than one portfolio named {} found'.format(name))
        else:
            return Portfolio.from_dict(ret['results'][0])

    @classmethod
    def create_portfolio(cls, portfolio: Portfolio) -> Portfolio:
        return GsSession.current._post('/portfolios', portfolio, cls=Portfolio)

    @classmethod
    def update_portfolio(cls, portfolio: Portfolio):
        return GsSession.current._put('/portfolios/{id}'.format(id=portfolio.id), portfolio, cls=Portfolio)

    @classmethod
    def delete_portfolio(cls, portfolio_id: str) -> dict:
        return GsSession.current._delete('/portfolios/{id}'.format(id=portfolio_id))

    # manage portfolio positions

    @classmethod
    def get_positions(cls, portfolio_id: str, start_date: dt.date = None, end_date: dt.date = None,
                      position_type: str = 'close') -> Tuple[PositionSet, ...]:
        url = '/portfolios/{id}/positions?type={positionType}'.format(id=portfolio_id, positionType=position_type)
        if start_date is not None:
            url += '&startDate={sd}'.format(sd=start_date.isoformat())
        if end_date is not None:
            url += '&endDate={sd}'.format(sd=end_date.isoformat())

        res = GsSession.current._get(url)
        return tuple(PositionSet.from_dict(v) for v in res.get('positionSets', ()))

    @classmethod
    def get_positions_for_date(cls, portfolio_id: str, position_date: dt.date,
                               position_type: str = 'close') -> PositionSet:
        url = '/portfolios/{id}/positions/{date}?type={ptype}'.format(
            id=portfolio_id, date=position_date.isoformat(), ptype=position_type)
        position_sets = GsSession.current._get(url, cls=PositionSet)['results']
        return position_sets[0] if len(position_sets) > 0 else None

    @classmethod
    def get_instruments_by_position_type(cls, positions_type: str,
                                         positions_id: str) -> Tuple[Instrument, ...]:
        root = 'deals' if positions_type == 'ETI' else 'books/' + positions_type
        url = '/risk-internal/{}/{}/positions'.format(root, positions_id)
        results = GsSession.current._get(url, timeout=181)

        instruments = []
        for position in results.get('positionSets', ({'positions': ()},))[0]['positions']:
            instrument_values = position['instrument']
            instrument = Instrument.from_dict(instrument_values)
            name = instrument_values.get('name')
            if name:
                instrument.name = name

            instruments.append(instrument)

        return tuple(instruments)

    @classmethod
    def get_latest_positions(cls, portfolio_id: str, position_type: str = 'close') -> Union[PositionSet, dict]:
        url = '/portfolios/{id}/positions/last?type={ptype}'.format(id=portfolio_id, ptype=position_type)
        results = GsSession.current._get(url)['results']

        # Annoyingly, different types are returned depending on position_type

        if isinstance(results, dict) and 'positions' in results:
            results['positions'] = tuple(Position.from_dict(p) for p in results['positions'])

        return PositionSet.from_dict(results)

    @classmethod
    def get_instruments_by_workflow_id(cls, workflow_id: str,
                                       preferInstruments: bool = False) -> Tuple[Instrument, ...]:
        root = 'quote'
        url = '/risk{}/{}/{}'.format('-internal' if not preferInstruments else '', root, workflow_id)
        results = GsSession.current._get(url, timeout=181)

        instruments = []
        for position in results.get('workflowPositions').get(workflow_id)[0]['positions']:
            instrument_values = position['instrument']
            instrument = Instrument.from_dict(instrument_values)
            name = instrument_values.get('name')
            if name:
                instrument.name = name

            instruments.append(instrument)

        return tuple(instruments)

    @classmethod
    def get_position_dates(cls, portfolio_id: str) -> Tuple[dt.date, ...]:
        position_dates = GsSession.current._get('/portfolios/{id}/positions/dates'.format(id=portfolio_id))['results']
        return tuple(dt.datetime.strptime(d, '%Y-%m-%d').date() for d in position_dates)

    @classmethod
    def update_positions(cls, portfolio_id: str, position_sets: List[PositionSet]) -> float:
        return GsSession.current._put('/portfolios/{id}/positions'.format(id=portfolio_id), position_sets)

    @classmethod
    def get_positions_data(cls,
                           portfolio_id: str,
                           start_date: dt.date,
                           end_date: dt.date,
                           fields: List[str] = None,
                           position_type: PositionType = None) -> List[dict]:
        start_date_str = start_date.isoformat()
        end_date_str = end_date.isoformat()
        url = f'/portfolios/{portfolio_id}/positions/data?startDate={start_date_str}&endDate={end_date_str}'
        if fields is not None:
            url += '&fields='.join([''] + fields)

        if position_type is not None:
            url += '&type=' + position_type.value

        return GsSession.current._get(url)['results']

    @classmethod
    def update_quote(cls, portfolio_id: str, request: RiskRequest):
        return GsSession.current._put('/risk-internal/quote/save/{id}'.format(id=portfolio_id), request)

    @classmethod
    def save_quote(cls, request: RiskRequest) -> str:
        return GsSession.current._post('/risk-internal/quote/save', request)['results']

    @classmethod
    def save_to_shadowbook(cls, request: RiskRequest, name: str) -> str:
        return GsSession.current._put(f'/risk-internal/shadowbook/save/{name}', request)['results']

    @classmethod
    def get_risk_models_by_coverage(cls, portfolio_id: str, term: Term = Term.Medium):
        return GsSession.current._get(f'/portfolios/{portfolio_id}/models?sortByTerm={term.value}')['results']

    @classmethod
    def get_reports(cls, portfolio_id: str) -> Tuple[Report, ...]:
        return GsSession.current._get('/portfolios/{id}/reports'.format(id=portfolio_id), cls=Report)['results']

    @classmethod
    def schedule_reports(cls,
                         portfolio_id: str,
                         start_date: dt.date,
                         end_date: dt.date = None,
                         backcast: bool = False) -> dict:
        if end_date is None:
            payload = {'startDate': start_date.isoformat()}
        else:
            payload = {'startDate': start_date.isoformat(), 'endDate': end_date.isoformat()}
        if backcast:
            payload['parameters'] = {'backcast': True}
        return GsSession.current._post('/portfolios/{id}/schedule'.format(id=portfolio_id), payload)

    @classmethod
    def get_custom_aum(cls,
                       portfolio_id: str,
                       start_date: dt.date = None,
                       end_date: dt.date = None) -> dict:
        url = f'/portfolios/{portfolio_id}/aum?'
        if start_date:
            url += f"&startDate={start_date.strftime('%Y-%m-%d')}"
        if end_date:
            url += f"&endDate={end_date.strftime('%Y-%m-%d')}"
        return GsSession.current._get(url)['data']
