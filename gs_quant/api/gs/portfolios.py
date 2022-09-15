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
from typing import Tuple, Union, List, Dict

from gs_quant.common import PositionType
from gs_quant.common import RiskRequest, Currency
from gs_quant.instrument import Instrument
from gs_quant.session import GsSession
from gs_quant.target.portfolios import Portfolio, Position, PositionSet
from gs_quant.target.reports import Report
from gs_quant.target.risk_models import RiskModelTerm as Term
from gs_quant.target.workflow_quote import WorkflowPosition, WorkflowPositionsResponse, SaveQuoteRequest

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
    def get_position_set_by_position_type(cls, positions_type: str, positions_id: str,
                                          activity_type: str = 'position') -> Tuple[PositionSet, ...]:
        root = 'deals' if positions_type == 'ETI' else 'books/' + positions_type
        if activity_type != 'position':
            url = '/risk-internal/{}/{}/positions?activityType={}'.format(root, positions_id, activity_type)
        else:
            url = '/risk-internal/{}/{}/positions'.format(root, positions_id)

        results = GsSession.current._get(url, timeout=181)
        return tuple(cls._unpack_position_set(res) for res in results['positionSets'])

    @classmethod
    def _unpack_position_set(cls, kvs: dict) -> PositionSet:
        position_set = PositionSet.from_dict(kvs)
        # NY - this is rather unfortunate: we end up with instruments all with the name of the ETI
        for position in position_set.positions:
            position.instrument.name = None

        return position_set

    @classmethod
    def get_instruments_by_position_type(cls, positions_type: str,
                                         positions_id: str,
                                         activity_type: str) -> Tuple[Instrument, ...]:
        position_sets = cls.get_position_set_by_position_type(positions_type=positions_type,
                                                              positions_id=positions_id,
                                                              activity_type=activity_type)

        instruments = []
        for position_set in position_sets:
            for positions in position_set.positions:
                instrument = positions.instrument
                instrument.metadata = {
                    'trade_date': position_set.position_date, 'tags': positions.tags,
                    'external_ids': {id_['idType']: id_['idValue'] for id_ in positions.external_ids},
                    'party_from': positions.party_from, 'party_to': positions.party_to}
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
                                       prefer_instruments: bool = False) -> Tuple[Instrument, ...]:
        root = 'quote'
        url = '/risk{}/{}/{}'.format('-internal' if not prefer_instruments else '', root, workflow_id)
        results = GsSession.current._get(url, timeout=181)

        instruments = []
        for position in results.get('workflowPositions').get(workflow_id):
            for insts in position['positions']:
                instrument_values = insts['instrument']
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
    def update_positions(cls,
                         portfolio_id: str,
                         position_sets: List[PositionSet],
                         net_positions: bool = True) -> float:
        url = f'/portfolios/{portfolio_id}/positions?netPositions={str(net_positions).lower()}'
        return GsSession.current._put(url, position_sets)

    @classmethod
    def get_positions_data(cls,
                           portfolio_id: str,
                           start_date: dt.date,
                           end_date: dt.date,
                           fields: List[str] = None,
                           position_type: PositionType = None,
                           include_all_business_days: bool = False) -> List[dict]:
        start_date_str = start_date.isoformat()
        end_date_str = end_date.isoformat()
        url = f'/portfolios/{portfolio_id}/positions/data?startDate={start_date_str}&endDate={end_date_str}'
        if fields is not None:
            url += '&fields='.join([''] + fields)
        if position_type is not None:
            url += '&type=' + position_type.value
        if include_all_business_days:
            url += '&includeAllBusinessDays=true'

        return GsSession.current._get(url)['results']

    @classmethod
    def update_quote(cls, quote_id: str, request: RiskRequest):
        return GsSession.current._put('/risk-internal/quote/save/{id}'.format(id=quote_id), request)

    @classmethod
    def save_quote(cls, request: RiskRequest) -> str:
        return GsSession.current._post('/risk-internal/quote/save', request)['results']

    @classmethod
    def update_workflow_quote(cls, quote_id: str, request: SaveQuoteRequest):
        headers = {'Content-Type': 'application/x-msgpack'}
        return GsSession.current._put('/risk-internal/quote/workflow/save/{id}'.format(id=quote_id), tuple([request]),
                                      request_headers=headers)

    @classmethod
    def save_workflow_quote(cls, request: SaveQuoteRequest) -> str:
        headers = {'Content-Type': 'application/x-msgpack'}
        return GsSession.current._post('/risk-internal/quote/workflow/save', tuple([request]),
                                       request_headers=headers)['results']

    @classmethod
    def share_workflow_quote(cls, request: SaveQuoteRequest) -> str:
        headers = {'Content-Type': 'application/x-msgpack'}
        return GsSession.current._post('/risk-internal/quote/workflow/share', tuple([request]),
                                       request_headers=headers)['results']

    @classmethod
    def get_workflow_quote(cls, workflow_id: str) -> Tuple[WorkflowPosition]:
        url = f'/risk-internal/quote/workflow/{workflow_id}'
        results = GsSession.current._get(url, timeout=181)
        wf_pos_res = WorkflowPositionsResponse.from_dict(results)
        if wf_pos_res:
            return wf_pos_res.results
        else:
            return ()

    @classmethod
    def get_shared_workflow_quote(cls, workflow_id: str) -> Tuple[WorkflowPosition]:
        url = f'/risk-internal/quote/workflow/shared/{workflow_id}'
        results = GsSession.current._get(url, timeout=181)
        wf_pos_res = WorkflowPositionsResponse.from_dict(results)
        if wf_pos_res:
            return wf_pos_res.results
        else:
            return ()

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
                         start_date: dt.date = None,
                         end_date: dt.date = None,
                         backcast: bool = False) -> dict:
        payload = {'parameters': {'backcast': backcast}}
        if start_date is not None:
            payload['startDate'] = start_date.isoformat()
        if end_date is not None:
            payload['endDate'] = end_date.isoformat()
        return GsSession.current._post('/portfolios/{id}/schedule'.format(id=portfolio_id), payload)

    @classmethod
    def get_schedule_dates(cls,
                           portfolio_id: str,
                           backcast: bool = False) -> List[dt.date]:
        results = GsSession.current._get(f'/portfolios/{portfolio_id}/schedule/dates?backcast={str(backcast).lower()}')
        return [dt.datetime.strptime(results['startDate'], '%Y-%m-%d').date(),
                dt.datetime.strptime(results['endDate'], '%Y-%m-%d').date()]

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

    @classmethod
    def upload_custom_aum(cls,
                          portfolio_id: str,
                          aum_data: List[Dict],
                          clear_existing_data: bool = None) -> dict:
        url = f'/portfolios/{portfolio_id}/aum'
        payload = {'data': aum_data}
        if clear_existing_data:
            url += '?clearExistingData=true'
        return GsSession.current._post(url, payload)

    @classmethod
    def get_attribution(cls,
                        portfolio_id: str,
                        start_date: dt.date = None,
                        end_date: dt.date = None,
                        currency: Currency = None) -> Dict:
        url = f'/attribution/{portfolio_id}?'
        if start_date:
            url += f"&startDate={start_date.strftime('%Y-%m-%d')}"
        if end_date:
            url += f"&endDate={end_date.strftime('%Y-%m-%d')}"
        if currency:
            url += f"currency={currency.value}"
        return GsSession.current._get(url)['results']
