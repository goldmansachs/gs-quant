"""
Copyright 2019 Marko Kangrga.
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

from dateutil.parser import parse
import dateutil.rrule as rrule
import datetime
import collections
from pandas.tseries.holiday import (AbstractHolidayCalendar, Holiday,
                                    USMartinLutherKingJr, USPresidentsDay, 
                                    GoodFriday, USMemorialDay, USLaborDay,
                                    USThanksgivingDay, nearest_workday)
from pandas.tseries.offsets import CustomBusinessDay
import json
import pandas as pd
import numpy as np
import os
import sys
import requests


RISK_MODELS =  {
    'AXUS4M': 'Axioma US Medium Term (AXUS4M)',
     # Medium Horizon (3-6 month) US-focused risk model
    'AXWW21M': 'Axioma Worldwide Medium Term (AXWW21M)',
     # Medium Horizon (3-6 month) Global risk model
    'AXUS3MMACRO': 'Axioma US Medium Term Macro (AXUS3MMACRO)',
     # Medium Horizon (3-6 month) US-focused Macro risk model
    'AXUS4S': 'Axioma US Short Term (AXUS4S)',
     # Short Horizon (1-3 month) US-focused risk model
    'AXEU21M': 'Axioma European Medium Term (AXEU21M)',
     # Medium Horizon (3-6 month) European risk model
    'AXWW21S': 'Axioma Worldwide Short Term (AXWW21S)',
     # Short Horizon (1-3 month) Global risk model
    'AXEM21M': 'Axioma Emerging Markets Medium Term (AXEM21M)',
     # Medium Horizon (3-6 month) Emerging Market risk model
    'AXCNM': 'Axioma China Medium Term (AXCNM)',
     # Medium Horizon (3-6 month) China risk model
    'AXAP21S': 'Axioma Asia Pacific Short Term (AXAP21S)',
     # Short Horizon (1-3 month) Asia Pacific risk model
    'AXAP21M': 'Axioma Asia Pacific Medium Term (AXAP21M)',
     # Medium Horizon (3-6 month) Asia Pacific risk model
    'AXAPxJP21M': 'Axioma Asia Pacific ex-Japan Medium Term (AXAPxJP21M)',
     # Medium Horizon (3-6 month) Asia Pacific ex-Japan risk model
    'AXAU4M': 'Axioma Australia Medium Term (AXAU4M)',
     # Medium Horizon (3-6 month) Australia risk model
    'AXJP4M': 'Axioma Japan Medium Term (AXJP4M)',
     # Medium Horizon (3-6 month) Japan risk model
    'AXTWM': 'Axioma Taiwan Medium Term (AXTWM)',
     # Medium Horizon (3-6 month) Taiwan risk model
}

AUTH_URL =    'https://idfs.gs.com/as/token.oauth2'
MARQUEE_URL = 'https://api.marquee.gs.com'

_GLOBAL_URLS = dict(
    PORT_URL =              '/v1/portfolios',
    PORT_POSITIONS_URL =    '/v1/portfolios/{id}/positions',
    PORT_SCHEDULE_URL =     '/v1/portfolios/{id}/schedule',
    PORT_REPORTS_URL =      '/v1/portfolios/{id}/reports',
    PORT_ID_URL =           '/v1/portfolios/{id}',
    DATA_QUERY_URL =        '/v1/data/{id}',
    ASSET_QUERY_URL =       '/v1/assets/data/query',
    DATASETS_URL =          '/v1/data/datasets',
    REPORT_URL =            '/v1/reports',
    REPORT_JOBS_URL =       '/v1/reports/{id}/jobs',
    REPORT_STATUS_URL =     '/v1/reports/{id}/status',
    REPORT_RESCHEDULE_URL = '/v1/reports/jobs/{id}/reschedule',
    REPORT_ID_URL =         '/v1/reports/{id}',
)

def _add_to_globals():
    for k, v in _GLOBAL_URLS.items():
        globals()[k] = ''.join([MARQUEE_URL, v])
        
_add_to_globals()

class USTradingCalendar(AbstractHolidayCalendar):
    rules = [
        Holiday('New Years Day', month=1, day=1, observance=nearest_workday),
        USMartinLutherKingJr,
        USPresidentsDay,
        GoodFriday,
        USMemorialDay,
        Holiday('July 4th', month=7, day=4, observance=nearest_workday),
        USLaborDay,
        USThanksgivingDay,
        Holiday('Christmas', month=12, day=25, observance=nearest_workday)
    ]


nyse_cal = CustomBusinessDay(calendar=USTradingCalendar())
mkt_holidays = USTradingCalendar().holidays()


class Session():
    '''Marquee Session class.

    Used to initialize a Marquee session and perform API requests.

    Parameters
    ----------
    auth_json_filepath : json
        JSON format:
            {
             "auth_data": {
              "client_id": "",
              "client_secret": "",
              "scope": "read_content read_product_data read_financial_data
                        modify_financial_data read_user_profile run_analytics",
              "grant_type": "client_credentials"
             },
             "auth_guid": ""
            }

    verbose : bool, default True
    '''

    def __init__(self, auth_json_filepath, verbose=False):
        self.auth_json_filepath = auth_json_filepath
        self.verbose = verbose
        self.uploaded_portfolios = []


    def start(self, set_default_entitlements=False):
        '''Helper function start a Marquee session.

        Parameters
        ----------
        set_default_entitlements : bool, default False
            Sets 'view', 'edit' and 'admin' entitlements to current user

        '''
        access_token, my_guid, auth_data = self._get_marquee_session(
            self.auth_json_filepath)
        self.access_token = access_token
        self.my_guid = my_guid
        self.auth_data = auth_data
        if set_default_entitlements:
            self.entitlements = {
                'view':  ['guid:' + my_guid, 'guid:' + auth_data['client_id']],
                'edit':  ['guid:' + my_guid, 'guid:' + auth_data['client_id']],
                'admin': ['guid:' + my_guid, 'guid:' + auth_data['client_id']],
            }


    def _get_marquee_session(self, auth_json_filepath):
        '''Helper function to initialize and start a Marquee session.

        Parameters
        ----------
        auth_json_filepath : str
            Filename containing JSON authentication parameters
            to start a Marquee session in the following format:
                {
                 "auth_data": {
                  "client_id": "",
                  "client_secret": "",
                  "scope": "read_content read_product_data
                            read_financial_data modify_financial_data
                            read_user_profile run_analytics",
                  "grant_type": "client_credentials"
                 },
                 "auth_guid": ""
                }

        Returns
        -------
        access_token : str
        my_guid : str
        auth_data : json
        '''
        path = os.path.dirname('.')
        with open(os.path.join(path, auth_json_filepath), 'r') as fp:
            auth = json.load(fp)
            auth_data = auth['auth_data']
            my_guid = auth['auth_guid']

        # create Session instance
        self.sess = requests.Session()

        # Make a POST to retrieve access_token
        result = self._request(method='POST', url=AUTH_URL, data=auth_data)
        access_token = result['access_token']

        if self.verbose:
            print('Access token: {}'.format(access_token))

        # add access token to session header
        self.sess.headers.update({'Authorization':'Bearer ' + access_token})
        self.sess.headers.update({'Content-Type':'application/json'})
        return access_token, my_guid, auth_data


    def close_session(self):
        '''Close a Marquee session.'''
        self.sess.close()


    def _request(self, method, url, return_df=False, **kwargs): 
        '''Helper function to perform HTTP requests using the 'requests' module.
        
        Parameters
        ----------
        method : str, {'GET', 'POST', 'PUT','DELETE'}
            Request method to indicate the desired action to
            be performed for a given resource. 
        
        url : str
            HTTP request URL.

        return_df : bool, default False


        Returns
        -------
        data : json or Pandas DataFrame
        '''
        try:
            response = self.sess.request(method=method, url=url, **kwargs)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(e)
            result = json.loads(response.text)
            if isinstance(result, dict):
                for k, v in result.items():
                    if k == 'messages':
                        print('Message:\n', '\n'.join(v))
                    else:
                        print('{}: {}'.format(k, v))
            else:
                print(json.loads(response.text))
            sys.exit(1)

        data = json.loads(response.text)

        if return_df:
            data_temp = data.get('results', data.get(
                'data')) if isinstance(data, dict) else None
            data = data_temp or data
            try:
                data = pd.DataFrame(data)
            except:
                print('Error: Could not create DataFrame from data')
        return data


    def custom_request(self, method, request_url,
                       my_params=None, my_json=None, my_data=None):
        '''Helper function to perform custom HTTP requests
        using the 'requests' module.

        Parameters
        ----------
        method : str, {'GET', 'POST', 'PUT','DELETE'}
            Request method to indicate the desired action to
            be performed for a given resource. 

        url : str
            HTTP request URL.

        my_params : json
            Parameters to be passed as 'params' in a HTTP request

        my_json : json
            Json to be passed as 'json' in a HTTP request

        my_data : json
            Data to be passed as 'data' in a HTTP request

        Returns
        -------
        data : json or Pandas DataFrame    
        '''
        try:
            response = self.sess.request(method=method,
                                         url=request_url,
                                         params=my_params,
                                         json=my_json,
                                         data=my_data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(e)
            result = json.loads(response.text)
            if isinstance(result, dict):
                for k, v in result.items():
                    if k == 'messages':
                        print('Message:\n', '\n'.join(v))
                    else:
                        print('{}: {}'.format(k, v))
            else:
                print(json.loads(response.text))
            sys.exit(1)
        
        data = json.loads(response.text)
        return data

            
    def upload_portfolio(self, df_portfolio, port_name, start_date=None,
                         currency='USD', payload=None):
        '''Convenience method for uploading a portfolio to marquee
        from a Pandas DataFrame and scheduling a portfolio report.

        Parameters
        ----------
        df_portfolio : Pandas DataFrame
            Portfolio data as Pandas DataFrame in the following format:

            +----+------------+----------------+---------------------+
            |    |   quantity | positionDate   | assetId             |
            |----+------------+----------------+---------------------|
            |  0 |       2499 | 12/31/2017     | MA4B66MW5E27UANEQ6Q |
            |  1 |       4708 | 12/31/2017     | MA4B66MW5E27UAKVA6N |
            |  2 |       4520 | 12/31/2017     | MA9VHN7TW4A6YZ0P    |
            |  3 |       2586 | 12/31/2017     | MA4B66MW5E27UAL9SUW |
            |  4 |       5813 | 12/31/2017     | MA4B66MW5E27U9VBB93 |
            |  * |       **** | **/**/****     | ******************* |
            | 99 |       2875 | 12/31/2017     | MA4B66MW5E27U9YGMGX |
            +----+------------+----------------+---------------------+
            Note: column names must match

        start_date : str, datetime, default None
            Start date for generating a portfolio report.
            If not provided, first date is used.

        currency : str, default 'USD'
            Portfolio currency.

        payload : json
            Custom payload for specifying portfolio metrics.
            If provided, port_name and currency are ignored.
            See URL for details:
            https://marquee.gs.com/s/developer/docs/endpoint-reference/
                    portfolio-service/create-a-portfolio        
        '''
        df_portfolio.positionDate = pd.to_datetime(df_portfolio.positionDate)
        df_portfolio = df_portfolio[df_portfolio.positionDate.dt.dayofweek < 5]
        start_date = start_date or df_port_upload.positionDate \
                                                 .min().strftime('%Y-%m-%d')
        df_groupby_date = df_portfolio.groupby('positionDate')
        
        portfolio = []
        struct = {}

        for name, group in df_groupby_date:
            struct = {}
            struct.update({'positionDate':name.strftime('%Y-%m-%d')})
            struct.update({'positions':json.loads(
                group[['assetId','quantity']].to_json(orient='records'))})
            portfolio.append(struct)
        
        if not payload:
            payload = {
              'name': '{}'.format(port_name),
              'currency': currency,
              'entitlements': self.entitlements
            }
            
        result = self._request(method='POST', url=PORT_URL, json=payload)
        portfolio_id = result['id']
        if self.verbose: print('Portfolio ID: {}'.format(portfolio_id))
        
        request_url = PORT_POSITIONS_URL.format(id=portfolio_id)
        port_result = self._request(method='PUT',
                                    url=request_url,
                                    json=portfolio)

        return portfolio_id


    def create_risk_report(self, portfolio_id, start_date, end_date,
                           risk_model='AXWW21M', name=None):
        '''Convenience method for generating a Marquee Factor Risk Report. 

        Parameters
        ----------
        portfolio_id : str
            Marquee unique portfolio identifier.

        start_date : str, datetime, default None
            Start date for generating a Risk Report.

        end_date : str, datetime, default None
            End date for generating a Risk Report.

        risk_model : str, default 'AXWW21M'
            Risk model to be used for risk report calculation.
            One of: 
                 AXUS2M, AXWW21M, AXUS3M, AXUS3MMACRO, AXUS4M, AXUS4S,
                 AXEU21M, STSWWFR, AXWW21S, AXCNM, AXEM21M, AXJP2M,
                 AXAPxJP21M, AXAP21M, AXAP21S, AXAU4M, AXJP4M, AXTWM

            Axioma risk reports available:        
            'AXUS4M': 'Axioma US Medium Term (AXUS4M)',
             # Medium Horizon (3-6 month) US-focused risk model
            'AXWW21M': 'Axioma Worldwide Medium Term (AXWW21M)',
             # Medium Horizon (3-6 month) Global risk model
            'AXUS3MMACRO': 'Axioma US Medium Term Macro (AXUS3MMACRO)',
             # Medium Horizon (3-6 month) US-focused Macro risk model
            'AXUS4S': 'Axioma US Short Term (AXUS4S)',
             # Short Horizon (1-3 month) US-focused risk model
            'AXEU21M': 'Axioma European Medium Term (AXEU21M)',
             # Medium Horizon (3-6 month) European risk model
            'AXWW21S': 'Axioma Worldwide Short Term (AXWW21S)',
             # Short Horizon (1-3 month) Global risk model
            'AXEM21M': 'Axioma Emerging Markets Medium Term (AXEM21M)',
             # Medium Horizon (3-6 month) Emerging Market risk model
            'AXCNM': 'Axioma China Medium Term (AXCNM)',
             # Medium Horizon (3-6 month) China risk model
            'AXAP21S': 'Axioma Asia Pacific Short Term (AXAP21S)',
             # Short Horizon (1-3 month) Asia Pacific risk model
            'AXAP21M': 'Axioma Asia Pacific Medium Term (AXAP21M)',
             # Medium Horizon (3-6 month) Asia Pacific risk model
            'AXAPxJP21M': 'Axioma Asia Pacific ex-Japan Medium Term (AXAPxJP21M)',
             # Medium Horizon (3-6 month) Asia Pacific ex-Japan risk model
            'AXAU4M': 'Axioma Australia Medium Term (AXAU4M)',
             # Medium Horizon (3-6 month) Australia risk model
            'AXJP4M': 'Axioma Japan Medium Term (AXJP4M)',
             # Medium Horizon (3-6 month) Japan risk model
            'AXTWM': 'Axioma Taiwan Medium Term (AXTWM)',
             # Medium Horizon (3-6 month) Taiwan risk model

        batch : str, {'weekly', 'monthly', None}
            Specify batching period to speed up report generation.

        name : str
            Specify report name.

        See below URL for more information:
        https://marquee.gs.com/s/developer/docs/object-model/report-service/ReportParameters
        '''
        rpt_name = "{}: {}".format(name, RISK_MODELS[risk_model]) if name \
                   else "{}".format(RISK_MODELS[risk_model])

        payload = {
            "name": rpt_name,
            "parameters": {
                "fxHedged": True,
                "riskModel": risk_model,
                "stockLevelExposures": True,
                "explodePositions": True,
                },
            "positionSourceId": portfolio_id,
            "positionSourceType": "Portfolio",
            "type": "Portfolio Factor Risk",
        }
        
        report = self._request(method='POST', url=REPORT_URL, json=payload)

        return report


    def schedule_report(self, id, startDate, endDate, batch=None, **kwargs):
        '''
        Schedule report execution, which will run analytics for all dates
        across all positions between a given start and end date. Please
        contact developer@gs.com for questions about running large batches

        Definition: POST /v1/reports/{id}/schedule
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/report-service/schedule-report

        Parameters
        ----------
        id : string, (read-only)
            Report unique identifier
        startDate : date, (optional)
            ISO 8601-formatted date
        endDate : date, (optional)
            ISO 8601-formatted date
        parameters : Report Parameters dictionary, (optional)
            Parameters specific to the report type
        batch : str, {'weekly', 'monthly', None}
            Specify batching period to speed up report generation.

        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/reports/{id}/schedule'
        request_url = request_url.format(id=id)

        batched_dates = self.get_batches(startDate, endDate,
                                         batch_rule=batch,
                                         strftime="%Y-%m-%d")

        for batch_start, batch_end in batched_dates:
            result = self._request(method='POST',
                                   url=request_url,
                                   json={'startDate': batch_start,
                                         'endDate': batch_end})


    def schedule_portfolio_reports(self, id, startDate, endDate,
                                   batch, **kwargs):
        '''
        Schedule execution of reports for a portfolio

        Definition: POST /v1/portfolios/{id}/schedule
        Required scopes: run_analytics
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/portfolio-service/schedule-portfolio-reports

        Parameters
        ----------
        id : string, (read-only)
            Portfolio unique identifier
        startDate : date, (optional)
            ISO 8601-formatted date
        endDate : date, (optional)
            ISO 8601-formatted date
        batch : str, {'weekly', 'monthly', None}
            Specify batching period to speed up report generation.
        '''

        request_url = 'https://api.marquee.gs.com/v1/portfolios/{id}/schedule'
        request_url = request_url.format(id=id)

        batched_dates = self.get_batches(startDate, endDate,
                                         batch_rule=batch,
                                         strftime="%Y-%m-%d")

        for batch_start, batch_end in batched_dates:
            result = self._request(method='POST',
                                   url=request_url,
                                   json={'startDate': batch_start,
                                         'endDate': batch_end})


    def check_id(self, id_dict, fields=None, as_of=None):
        '''Convenience method for generating a Marquee Factor Risk Report. 

        Parameters
        ----------
        id_dict : dict
            Query dictionary.
            Example:
                {'bbid':['AAPL US','IBM US','MSFT US','GOOG US',
                         'AMZN US','TSLA US', 'LULU US']}

        fields : list of str, e.g. ["bbid", "ticker", "cusip", "id", "name"]
            Information to return from Marquee ID query.name

        as_of : str, datetime
            As of date to run search query. None defaults to today.

        Returns
        -------
        response : Pandas DataFrame

        Examples
        --------
            >>> from gs_utils.session import Session
            >>> sess = Session(auth_json_filepath='auth.json', verbose=True)
            >>> sess.start(set_default_entitlements=True)
            >>> sess.check_id({'bbid':['AAPL US','IBM US','MSFT US','GOOG US',
                                       'AMZN US','TSLA US', 'LULU US']})
            +----+---------+---------------------+-------------------------+----------+
            |    | bbid    | id                  | name                    | ticker   |
            |----+---------+---------------------+-------------------------+----------|
            |  0 | TSLA US | MA4B66MW5E27UANEQ6Q | Tesla Inc               | TSLA     |
            |  1 | LULU US | MA4B66MW5E27UAKVA6N | Lululemon Athletica Inc | LULU     |
            |  2 | GOOG US | MA9VHN7TW4A6YZ0P    | Alphabet Inc-CL C       | GOOG     |
            |  3 | MSFT US | MA4B66MW5E27UAL9SUW | Microsoft Corp          | MSFT     |
            |  4 | AAPL US | MA4B66MW5E27U9VBB93 | Apple Inc               | AAPL     |
            |  5 | AMZN US | MA4B66MW5E27U9YGMGX | Amazon.com Inc          | AMZN     |
            +----+---------+---------------------+-------------------------+----------+
        '''
        fields = fields or ["bbid", "ticker", "cusip", "isin", "id", "name"]
        as_of = as_of or '{dt:%Y-%m-%dT%TZ}'.format(
            dt=datetime.datetime.utcnow())
        asset_query = {
          "where": id_dict,
          'asOfTime': as_of,
          "limit": 1500,
          "fields": fields,
        }

        request_url = ASSET_QUERY_URL
        response = self._request(method='POST',
                                 url=request_url,
                                 json=asset_query,
                                 return_df=True)
        return response

    @staticmethod
    def get_batch_dates(start_date, end_date, batch_rule, inc=True):
        if batch_rule == 'weekly':
            rule_key = rrule.WEEKLY
        elif batch_rule == 'monthly':
            rule_key = rrule.MONTHLY
        else:
            raise ValueError("Invalid rule key: '{}'.",
                "Valid values are 'weekly' or 'monthly'.".format(batch_rule))
        start_date = nyse_cal.rollback(start_date)
        end_date = nyse_cal.rollback(end_date)
        if inc: yield start_date
        rule = rrule.rrule(rule_key, interval=1, byhour=0, byminute=0,
                           bysecond=0, dtstart=start_date)
        for x in rule.between(start_date, end_date, inc=False):
            yield nyse_cal.rollback(x)
        if inc: yield end_date

    def get_batches(self, start_date, end_date,
                    batch_rule='weekly', strftime=None):

        if not isinstance(start_date, datetime.date):
            start_date = parse(start_date)
        if not isinstance(end_date, datetime.date):
            end_date = parse(end_date)
        if batch_rule:
            date_list = list(self.get_batch_dates(start_date,
                                                  end_date,
                                                  batch_rule))
            
            batch_dates = [(x, date_list[i+1]) for i, x \
                            in enumerate(date_list[:-1])]
        else:
            batch_dates = [(start_date, end_date)]

        if strftime:
            batch_dates = [(b[0].strftime(strftime), b[1].strftime(strftime)) \
                           for b in batch_dates]

        return batch_dates

    # ---------------------------------------------
    # Automatically generated Marquee calls
    # ---------------------------------------------
    def get_many_portfolios(self, return_df=False, **kwargs):
        '''
        Get many portfolios

        Definition: GET /v1/portfolios
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/portfolio-service/get-many-portfolios

        Parameters
        ----------
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/portfolios'

        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def create_portfolio(self, return_df=False, **kwargs):
        '''
        Create a new portfolio in Marquee.

        Definition: POST /v1/portfolios
        Required scopes: modify_financial_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/portfolio-service/create-a-portfolio

        Parameters
        ----------
        currency : string
            Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP
            vs GBp)One of: ACUADPAEDAFAALLAMDANGAOAAOKshow more
        description : string, (optional)
            Free text description of portfolio. Description provided will be
            indexed in the search service for free text relevance match
        entitlements : Entitlements, (optional)
            Defines the entitlements of a given resource
        identifiers : array of Identifier, (optional)
            Array of identifier objects which can be used to locate this item in
            searches and other services
        name : string
            Display name of the portfolio
        ownerId : string, (optional)
            Marquee unique identifier for user who owns the object.
        reportIds : array of string, (optional)
            Array of report identifiers related to the object
        shortName : string, (optional)
            Short name or alias for the portfolio
        tags : array of string, (optional)
            Metadata associated with the object. Provide an array of strings which
            will be indexed for search and locating related objects
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/portfolios'

        data = self._request(method='POST',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def get_portfolio_data(self, return_df=False, **kwargs):
        '''
        Returns information about portfolios available in Marquee as a table.
        The caller can specify which fields are returned.

        Definition: GET /v1/portfolios/data
        Required scopes: read_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/portfolio-service/get-portfolio-data

        Parameters
        ----------
        limit : array of string, (optional)
            Maximum number of results to be returned in the result set.
        offset : array of string, (optional)
            Offset of first result to return from the server
        field : array of string, (optional)
            Fields to be returned from dataset. Optionally can specify function to
            be applied to field data (Deprecated)
        orderBy : array containing any of the following: string,, (optional)
            Field name by which to order results
        createdById : array of string, (optional)
            Filter by id of user who created the object
        tags : array of string, (optional)
            Filter by contents of tags, matches on words
        id : array of string, (optional)
            Filter by id
        ownerId : array of string, (optional)
            Filter by owner ID
        shortName : array of string, (optional)
            Filter by short name (exact match).
        currency : array of string, (optional)
            Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP
            vs GBp)One of: ACUADPAEDAFAALLAMDANGAOAAOKshow more
        name : array of string, (optional)
            Filter by name (exact match).
        description : array of string, (optional)
            Filter by asset description.
        lastUpdatedById : array of string, (optional)
            Filter by last updated user id
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/portfolios/data'

        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def get_portfolio_data_query(self, return_df=False, **kwargs):
        '''
        The Portfolios endpoint returns information about portfolios available
        in Marquee as a table. The caller can specify which fields are
        returned.

        Definition: POST /v1/portfolios/data/query
        Required scopes: read_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/portfolio-service/get-portfolio-data-query

        Parameters
        ----------
        format : string, (optional)
            Alternative format for data to be returned inOne of: ExcelMessagePack
        where : FieldFilterMap, (optional)

        asOfTime : date-time, (optional)
            ISO 8601-formatted timestamp
        date : date, (optional)
            ISO 8601-formatted date
        time : date-time, (optional)
            ISO 8601-formatted timestamp
        delay : integer, (optional)

        orderBy : array containing OrderBy, (optional)

        scroll : string, (optional)
            Time for which to keep the scroll search context alive, i.e. 1m (1
            minute) or 10s (10 seconds)
        scrollId : string, (optional)
            Scroll identifier to be used to retrieve the next batch of results
        fields : array containing Selector, (optional)

        limit : integer, (optional)
            Limit on the number of objects to be returned in the response. Can
            range between 1 and 10000
        offset : integer, (optional)
            The offset of the first result returned (default 0). Can be used in
            pagination to defined the first item in the list to be returned, for
            example if you request 100 objects, to query the next page you would
            specify offset = 100.
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/portfolios/data/query'

        data = self._request(method='POST',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def get_many_portfolios_query(self, return_df=False, **kwargs):
        '''
        The Portfolios endpoint returns information about portfolios available
        in Marquee. The response includes name, description and identifiers
        for each portfolio, and can be used to iterate in batches using a
        pagination object.

        Definition: POST /v1/portfolios/query
        Required scopes: read_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/portfolio-service/get-many-portfolios-query

        Parameters
        ----------
        format : string, (optional)
            Alternative format for data to be returned inOne of: ExcelMessagePack
        where : FieldFilterMap, (optional)

        asOfTime : date-time, (optional)
            ISO 8601-formatted timestamp
        date : date, (optional)
            ISO 8601-formatted date
        time : date-time, (optional)
            ISO 8601-formatted timestamp
        delay : integer, (optional)

        orderBy : array containing any of the following: string,, (optional)

        scroll : string, (optional)
            Time for which to keep the scroll search context alive, i.e. 1m (1
            minute) or 10s (10 seconds)
        scrollId : string, (optional)
            Scroll identifier to be used to retrieve the next batch of results
        fields : array containing any of the following: string,, (optional)

        limit : integer, (optional)
            Limit on the number of objects to be returned in the response. Can
            range between 1 and 10000
        offset : integer, (optional)
            The offset of the first result returned (default 0). Can be used in
            pagination to defined the first item in the list to be returned, for
            example if you request 100 objects, to query the next page you would
            specify offset = 100.
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/portfolios/query'

        data = self._request(method='POST',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def get_portfolio(self, id, return_df=False, **kwargs):
        '''
        Retrieve a portfolio based on its unique identifier. Returns a
        portfolio object which contains name, description, identifiers and
        other metadata.

        Definition: GET /v1/portfolios/{id}
        Required scopes: read_financial_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/portfolio-service/get-a-portfolio

        Parameters
        ----------
        id : string, (read-only)
            Marquee unique portfolio identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/portfolios/{id}'

        request_url = request_url.format(id=id)
        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def update_portfolio(self, id, return_df=False, **kwargs):
        '''
        Apply an update to an existing portfolio in Marquee. User must have
        edit entitlement on the portfolio in order to update.

        Definition: PUT /v1/portfolios/{id}
        Required scopes: modify_financial_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/portfolio-service/update-portfolio

        Parameters
        ----------
        id : string, (read-only)
            Marquee unique portfolio identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        currency : string
            Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP
            vs GBp)One of: ACUADPAEDAFAALLAMDANGAOAAOKshow more
        description : string, (optional)
            Free text description of portfolio. Description provided will be
            indexed in the search service for free text relevance match
        entitlements : Entitlements, (optional)
            Defines the entitlements of a given resource
        identifiers : array of Identifier, (optional)
            Array of identifier objects which can be used to locate this item in
            searches and other services
        name : string
            Display name of the portfolio
        ownerId : string, (optional)
            Marquee unique identifier for user who owns the object.
        reportIds : array of string, (optional)
            Array of report identifiers related to the object
        shortName : string, (optional)
            Short name or alias for the portfolio
        tags : array of string, (optional)
            Metadata associated with the object. Provide an array of strings which
            will be indexed for search and locating related objects
        '''

        request_url = 'https://api.marquee.gs.com/v1/portfolios/{id}'

        request_url = request_url.format(id=id)
        data = self._request(method='PUT',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def delete_portfolio(self, id, return_df=False, **kwargs):
        '''
        Remove a portfolio and related position data from Marquee by
        identifier. User must have edit entitlement on the asset in order to
        delete.

        Definition: DELETE /v1/portfolios/{id}
        Required scopes: modify_financial_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/portfolio-service/delete-portfolio

        Parameters
        ----------
        id : string, (read-only)
            Marquee unique portfolio identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/portfolios/{id}'

        request_url = request_url.format(id=id)
        data = self._request(method='DELETE',
                             url=request_url,
                             return_df=return_df)
        return data

    def get_portfolio_risk_models(self, id, return_df=False, **kwargs):
        '''
        Get available risk models for a portfolio based on region

        Definition: GET /v1/portfolios/{id}/models
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/portfolio-service/get-portfolio-risk-models

        Parameters
        ----------
        id : string, (optional)
            Marquee unique asset identifier.
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        asOfDate : array of date, (optional)
            Give risk models available as of this date
        '''

        request_url = 'https://api.marquee.gs.com/v1/portfolios/{id}/models'

        request_url = request_url.format(id=id)
        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def get_positions(self, id, return_df=False, **kwargs):
        '''
        Retrieve positions for portfolio and one or more dates

        Definition: GET /v1/portfolios/{id}/positions
        Required scopes: read_financial_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/portfolio-service/get-positions

        Parameters
        ----------
        id : string, (read-only)
            Marquee unique portfolio identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        startDate : array of date, (optional)
            Start date for positions
        endDate : array of date, (optional)
            End date for positions
        type : array of string, (optional)
            One of: openclose
        '''

        request_url = 'https://api.marquee.gs.com/v1/portfolios/{id}/positions'

        request_url = request_url.format(id=id)
        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def update_positions(self, id, return_df=False, **kwargs):
        '''
        Update position set for portfolio and one or more dates

        Definition: PUT /v1/portfolios/{id}/positions
        Required scopes: modify_financial_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/portfolio-service/update-positions

        Parameters
        ----------
        id : string, (read-only)
            Portfolio unique identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/portfolios/{id}/positions'

        request_url = request_url.format(id=id)
        data = self._request(method='PUT',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def get_positions_data(self, id, return_df=False, **kwargs):
        '''
        Retrieve positions for portfolio

        Definition: GET /v1/portfolios/{id}/positions/data
        Required scopes: read_financial_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/portfolio-service/get-positions-data

        Parameters
        ----------
        id : string, (read-only)
            Portfolio unique identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        fields : array of string, (optional)
            Fields requested
        format : array of string, (optional)
            One of: Excel
        startDate : array of date, (optional)
            Start date for positions
        endDate : array of date, (optional)
            End date for positions
        quantity : array of string, (optional)

        type : array of string, (optional)
            One of: openclose
        '''

        request_url = 'https://api.marquee.gs.com/v1/portfolios/{id}/positions/data'

        request_url = request_url.format(id=id)
        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def get_position_dates(self, id, return_df=False, **kwargs):
        '''
        Retrieve array of dates for which a given portfolio has position data.

        Definition: GET /v1/portfolios/{id}/positions/dates
        Required scopes: read_financial_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/portfolio-service/get-position-dates

        Parameters
        ----------
        id : string, (read-only)
            Marquee unique portfolio identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        type : array of string, (optional)
            One of: openclose
        '''

        request_url = 'https://api.marquee.gs.com/v1/portfolios/{id}/positions/dates'

        request_url = request_url.format(id=id)
        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def get_latest_positions_for_portfolio(self, id, return_df=False, **kwargs):
        '''
        Retrieve latest position data.

        Definition: GET /v1/portfolios/{id}/positions/last
        Required scopes: read_financial_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/portfolio-service/get-latest-positions-for-portfolio

        Parameters
        ----------
        id : string, (read-only)
            Marquee unique portfolio identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        type : array of string, (optional)
            One of: openclose
        '''

        request_url = 'https://api.marquee.gs.com/v1/portfolios/{id}/positions/last'

        request_url = request_url.format(id=id)
        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def get_latest_portfolio_positions_data(self, id, return_df=False, **kwargs):
        '''
        Retrieve the latest positions data for a portfolio

        Definition: GET /v1/portfolios/{id}/positions/last/data
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/portfolio-service/get-latest-portfolio-positions-data

        Parameters
        ----------
        id : string, (read-only)
            Portfolio unique identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        fields : array of string, (optional)
            Fields requested
        quantity : array of string, (optional)
            Quantity of a given position
        type : array of string, (optional)
            One of: openclose
        '''

        request_url = 'https://api.marquee.gs.com/v1/portfolios/{id}/positions/last/data'

        request_url = request_url.format(id=id)
        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def update_positions_for_date(self, id, date, return_df=False, **kwargs):
        '''
        Add or update position data for a given portfolio and date.

        Definition: PUT /v1/portfolios/{id}/positions/{date}
        Required scopes: modify_financial_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/portfolio-service/update-positions-for-date

        Parameters
        ----------
        id : string, (read-only)
            Marquee unique portfolio identifier
        date : date, (optional)
            ISO 8601-formatted date
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        positionDate : date, (optional)
            ISO 8601-formatted date
        lastUpdateTime : date-time, (optional)
            ISO 8601-formatted timestamp
        positions : array of Position, (optional)
            Array of quantity position objects.
        type : string, (optional)
            The composition type of a PortfolioOne of: openclose
        divisor : number, (optional)
            optional index divisor for a position set
        '''

        request_url = 'https://api.marquee.gs.com/v1/portfolios/{id}/positions/{date}'

        request_url = request_url.format(id=id, date=date)
        data = self._request(method='PUT',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def get_positions_for_date(self, id, date, return_df=False, **kwargs):
        '''
        Retrieve position date for a given portfolio and date.

        Definition: GET /v1/portfolios/{id}/positions/{date}
        Required scopes: read_financial_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/portfolio-service/get-positions-for-date

        Parameters
        ----------
        id : string, (read-only)
            Marquee unique portfolio identifier
        date : date, (optional)
            ISO 8601-formatted date
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        type : array of string, (optional)
            One of: openclose
        '''

        request_url = 'https://api.marquee.gs.com/v1/portfolios/{id}/positions/{date}'

        request_url = request_url.format(id=id, date=date)
        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def get_portfolio_reports(self, id, return_df=False, **kwargs):
        '''
        Get reports for a portfolio

        Definition: GET /v1/portfolios/{id}/reports
        Required scopes: read_financial_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/portfolio-service/get-portfolio-reports

        Parameters
        ----------
        id : string, (read-only)
            Marquee unique portfolio identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/portfolios/{id}/reports'

        request_url = request_url.format(id=id)
        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def create_asset(self, return_df=False, **kwargs):
        '''
        Create a new asset in Marquee.

        Definition: POST /v1/assets
        Required scopes: modify_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/asset-service/create-an-asset

        Parameters
        ----------
        assetClass : string
            Asset classification of security. Assets are classified into broad
            groups which exhibit similar characteristics and behave in a
            consistent way under different market conditionsOne of:
            CashCommodCreditCross AssetEquityFundFXMortgageRates
        currency : string, (optional)
            Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP
            vs GBp)One of: ACUADPAEDAFAALLAMDANGAOAAOKshow more
        description : string, (optional)
            Free text description of asset. Description provided will be indexed
            in the search service for free text relevance match
        domains : Domains, (optional)

        entitlements : Entitlements, (optional)
            Defines the entitlements of a given resource
        exchange : string, (optional)
            Name of marketplace where security, derivative or other instrument is
            traded
        identifiers : array of Identifier, (optional)
            Array of identifier objects which can be used to locate this item in
            searches and other services
        listed : boolean, (optional)
            Whether the asset is currently listed or not
        liveDate : date, (optional)
            ISO 8601-formatted date
        name : string
            Display name of the asset
        ownerId : string, (optional)
            Marquee unique identifier
        parameters : any of the following: Asset Parameters, Commod Config Parameters, Hedge Fund Parameters, Share Class Parameters, Instruments, (optional)

        assetStats : array of AssetStats, (optional)

        people : People, (optional)
            Key people associated with asset
        region : string, (optional)
            Regional classification for the assetOne of:
            AmericasAsiaEMEuropeGlobal
        reportIds : array of string, (optional)
            Array of report identifiers related to the object
        shortName : string, (optional)
            Short name or alias for the asset
        styles : array of string, (optional)
            Styles or themes associated with the asset (max 50)
        tags : array of string, (optional)
            Metadata associated with the object. Provide an array of strings which
            will be indexed for search and locating related objects
        type : string
            Asset type differentiates the product categorization or contract
            typeOne of: AccessBasisBasisSwapBenchmarkBenchmark RateBondCalendar
            SpreadCapCashCertificateshow more
        underlyingAssetIds : array of string, (optional)
            Underlying asset ids
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/assets'

        data = self._request(method='POST',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def get_many_assets(self, return_df=False, **kwargs):
        '''
        Get many asset objects from Marquee, iterate in batches using a
        pagination object.

        Definition: GET /v1/assets
        Required scopes: read_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/asset-service/get-many-assets

        Parameters
        ----------
        limit : array of string, (optional)
            Maximum number of results to be returned in the result set.
        offset : array of string, (optional)
            Offset of first result to return from the server
        scroll : array of string, (optional)
            Time for which to keep the scroll search context alive, i.e. 1m (1
            minute) or 10s (10 seconds).
        scrollId : array of string, (optional)
            Scroll identifier to be used to retrieve the next batch of results
        includeInactive : array of string, (optional)
            One of: truefalse
        orderBy : array containing any of the following: string,, (optional)
            Field name by which to order results
        createdById : array of string, (optional)
            Filter by id of user who created the object
        vehicleType : array of string, (optional)
            Type of investment vehicle. Only viewable after having been granted
            additional access to asset information.One of: Comingled HFCo-
            InvestmentUCITS'40 ActOther
        tags : array of string, (optional)
            Filter by contents of tags, matches on words
        regionalFocus : array of string, (optional)
            Section of the world a fund is focused on from an investment
            perspective. Same view permissions as the asset.One of: GlobalAsia ex-
            JapanChinaEmerging EuropeEuropeGlobal Emerging MarketsJapanLatin
            AmericaMiddle East / North AfricaNorth Americashow more
        optionType : array of string, (optional)
            One of: payerreceiver
        sectors : array of string, (optional)
            Filter by sector
        wpk : array of string, (optional)
            Filter by WPK (subject to licensing).
        exchange : array of string, (optional)
            Filter by GS exchange code
        ticker : array of string, (optional)
            Filter by Ticker.
        assetClass : array of string, (optional)
            Asset classification of security. Assets are classified into broad
            groups which exhibit similar characteristics and behave in a
            consistent way under different market conditionsOne of:
            CashCommodCreditCross AssetEquityFundFXMortgageRates
        ric : array of string, (optional)
            Filter by RIC (subject to licensing).
        id : array of string, (optional)
            Filter by id
        indexCreateSource : array of string, (optional)
            Source of basket create.One of: APICUBEHedgerMarquee UI
        bcid : array of string, (optional)
            Filter by Bloomberg Composite ID.
        bbid : array of string, (optional)
            Filter by Bloomberg ID.
        performanceFee : array containing, (optional)

        underlyingAssetIds : array of string, (optional)
            Filter by Marquee IDs of the underlying assets.
        bbidEquivalent : array of string, (optional)
            Filter by Bloomberg equivalent ID.
        valoren : array of string, (optional)
            Filter by Valoren (subject to licensing).
        portfolioManagers : array of string, (optional)
            Filter by id
        supraStrategy : array of string, (optional)
            Broad descriptor of a fund's investment approach. Same view
            permissions as the assetOne of: CompositeCreditEquityEquity HedgeEvent
            DrivenFund of FundsMacroMulti-StrategyOtherQuantshow more
        lmsId : array of string, (optional)

        strategy : array of string, (optional)
            More specific descriptor of a fund's investment approach. Same view
            permissions as the asset.One of: Active TradingActivistCo-Invest /
            SPVCommodityCommoditiesCompositeConservativeConvert ArbConvertible
            ArbitrageCredit Arbitrageshow more
        ownerId : array of string, (optional)
            Filter by owner ID
        assetClassificationsIsPrimary : array of string, (optional)
            Whether or not it is the primary exchange asset.One of: truefalse
        styles : array of array, (optional)
            Filter by asset style
        shortName : array of string, (optional)
            Filter by short name (exact match).
        mic : array of string, (optional)

        currency : array of string, (optional)
            Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP
            vs GBp)One of: ACUADPAEDAFAALLAMDANGAOAAOKshow more
        assetParametersExchangeCurrency : array of string, (optional)
            Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP
            vs GBp)One of: ACUADPAEDAFAALLAMDANGAOAAOKshow more
        managementFee : array containing, (optional)

        cusip : array of string, (optional)
            Filter by CUSIP (subject to licensing).
        name : array of string, (optional)
            Filter by name (exact match).
        aum : array containing, (optional)

        region : array of string, (optional)
            Regional classification for the assetOne of:
            AmericasAsiaEMEuropeGlobal
        liveDate : array containing, (optional)

        primeId : array of string, (optional)
            Filter by primeId.
        description : array of string, (optional)
            Filter by asset description.
        lastUpdatedById : array of string, (optional)
            Filter by last updated user id
        type : array of string, (optional)
            Asset type differentiates the product categorization or contract
            typeOne of: AccessBasisBasisSwapBenchmarkBenchmark RateBondCalendar
            SpreadCapCashCertificateshow more
        sedol : array of string, (optional)
            Filter by SEDOL (subject to licensing).
        marketCapCategory : array of string, (optional)
            Category of market capitalizations a fund is focused on from an
            investment perspective. Same view permissions as the asset.One of:
            AllLargeMidSmall
        strikePrice : array of string, (optional)

        listed : array of string, (optional)
            Whether the asset is listed or not.One of: truefalse
        g10Currency : array of string, (optional)
            Is a G10 asset.One of: truefalse
        isin : array of string, (optional)
            Filter by ISIN (subject to licensing).
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/assets'

        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def get_asset_data(self, return_df=False, **kwargs):
        '''
        Returns information about assets available in Marquee as a table. The
        caller can specify which fields are returned.

        Definition: GET /v1/assets/data
        Required scopes: read_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/asset-service/get-asset-data

        Parameters
        ----------
        limit : array of string, (optional)
            Maximum number of results to be returned in the result set.
        offset : array of string, (optional)
            Offset of first result to return from the server
        scroll : array of string, (optional)
            Time for which to keep the scroll search context alive, i.e. 1m (1
            minute) or 10s (10 seconds).
        scrollId : array of string, (optional)
            Scroll identifier to be used to retrieve the next batch of results
        asOfTime : array of date-time, (optional)
            Returns the state of the asset identifiers as of the given time
        field : array of string, (optional)
            Fields to be returned from dataset. Optionally can specify function to
            be applied to field data (Deprecated)
        orderBy : array containing any of the following: string,, (optional)
            Field name by which to order results
        createdById : array of string, (optional)
            Filter by id of user who created the object
        vehicleType : array of string, (optional)
            Type of investment vehicle. Only viewable after having been granted
            additional access to asset information.One of: Comingled HFCo-
            InvestmentUCITS'40 ActOther
        tags : array of string, (optional)
            Filter by contents of tags, matches on words
        regionalFocus : array of string, (optional)
            Section of the world a fund is focused on from an investment
            perspective. Same view permissions as the asset.One of: GlobalAsia ex-
            JapanChinaEmerging EuropeEuropeGlobal Emerging MarketsJapanLatin
            AmericaMiddle East / North AfricaNorth Americashow more
        optionType : array of string, (optional)
            One of: payerreceiver
        sectors : array of string, (optional)
            Filter by sector
        wpk : array of string, (optional)
            Filter by WPK (subject to licensing).
        exchange : array of string, (optional)
            Filter by GS exchange code
        ticker : array of string, (optional)
            Filter by Ticker.
        assetClass : array of string, (optional)
            Asset classification of security. Assets are classified into broad
            groups which exhibit similar characteristics and behave in a
            consistent way under different market conditionsOne of:
            CashCommodCreditCross AssetEquityFundFXMortgageRates
        ric : array of string, (optional)
            Filter by RIC (subject to licensing).
        id : array of string, (optional)
            Filter by id
        indexCreateSource : array of string, (optional)
            Source of basket create.One of: APICUBEHedgerMarquee UI
        bcid : array of string, (optional)
            Filter by Bloomberg Composite ID.
        bbid : array of string, (optional)
            Filter by Bloomberg ID.
        performanceFee : array containing, (optional)

        underlyingAssetIds : array of string, (optional)
            Filter by Marquee IDs of the underlying assets.
        bbidEquivalent : array of string, (optional)
            Filter by Bloomberg equivalent ID.
        valoren : array of string, (optional)
            Filter by Valoren (subject to licensing).
        portfolioManagers : array of string, (optional)
            Filter by id
        supraStrategy : array of string, (optional)
            Broad descriptor of a fund's investment approach. Same view
            permissions as the assetOne of: CompositeCreditEquityEquity HedgeEvent
            DrivenFund of FundsMacroMulti-StrategyOtherQuantshow more
        lmsId : array of string, (optional)

        strategy : array of string, (optional)
            More specific descriptor of a fund's investment approach. Same view
            permissions as the asset.One of: Active TradingActivistCo-Invest /
            SPVCommodityCommoditiesCompositeConservativeConvert ArbConvertible
            ArbitrageCredit Arbitrageshow more
        ownerId : array of string, (optional)
            Filter by owner ID
        assetClassificationsIsPrimary : array of string, (optional)
            Whether or not it is the primary exchange asset.One of: truefalse
        styles : array of array, (optional)
            Filter by asset style
        shortName : array of string, (optional)
            Filter by short name (exact match).
        mic : array of string, (optional)

        currency : array of string, (optional)
            Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP
            vs GBp)One of: ACUADPAEDAFAALLAMDANGAOAAOKshow more
        assetParametersExchangeCurrency : array of string, (optional)
            Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP
            vs GBp)One of: ACUADPAEDAFAALLAMDANGAOAAOKshow more
        managementFee : array containing, (optional)

        cusip : array of string, (optional)
            Filter by CUSIP (subject to licensing).
        name : array of string, (optional)
            Filter by name (exact match).
        aum : array containing, (optional)

        region : array of string, (optional)
            Regional classification for the assetOne of:
            AmericasAsiaEMEuropeGlobal
        liveDate : array containing, (optional)

        primeId : array of string, (optional)
            Filter by primeId.
        description : array of string, (optional)
            Filter by asset description.
        lastUpdatedById : array of string, (optional)
            Filter by last updated user id
        type : array of string, (optional)
            Asset type differentiates the product categorization or contract
            typeOne of: AccessBasisBasisSwapBenchmarkBenchmark RateBondCalendar
            SpreadCapCashCertificateshow more
        sedol : array of string, (optional)
            Filter by SEDOL (subject to licensing).
        marketCapCategory : array of string, (optional)
            Category of market capitalizations a fund is focused on from an
            investment perspective. Same view permissions as the asset.One of:
            AllLargeMidSmall
        strikePrice : array of string, (optional)

        listed : array of string, (optional)
            Whether the asset is listed or not.One of: truefalse
        g10Currency : array of string, (optional)
            Is a G10 asset.One of: truefalse
        isin : array of string, (optional)
            Filter by ISIN (subject to licensing).
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/assets/data'

        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def get_asset_data_query(self, return_df=False, **kwargs):
        '''
        The Assets endpoint returns information about assets available in
        Marquee as a table. The caller can specify which fields are returned.

        Definition: POST /v1/assets/data/query
        Required scopes: read_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/asset-service/get-asset-data-query

        Parameters
        ----------
        format : string, (optional)
            Alternative format for data to be returned inOne of: ExcelMessagePack
        where : FieldFilterMap, (optional)

        asOfTime : date-time, (optional)
            ISO 8601-formatted timestamp
        date : date, (optional)
            ISO 8601-formatted date
        time : date-time, (optional)
            ISO 8601-formatted timestamp
        delay : integer, (optional)

        orderBy : array containing any of the following: string,, (optional)

        scroll : string, (optional)
            Time for which to keep the scroll search context alive, i.e. 1m (1
            minute) or 10s (10 seconds)
        scrollId : string, (optional)
            Scroll identifier to be used to retrieve the next batch of results
        fields : array containing any of the following: string,, (optional)

        limit : integer, (optional)
            Limit on the number of objects to be returned in the response. Can
            range between 1 and 10000
        offset : integer, (optional)
            The offset of the first result returned (default 0). Can be used in
            pagination to defined the first item in the list to be returned, for
            example if you request 100 objects, to query the next page you would
            specify offset = 100.
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/assets/data/query'

        data = self._request(method='POST',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def get_many_assets_query(self, return_df=False, **kwargs):
        '''
        The Assets endpoint returns information about assets available in
        Marquee. The response includes name, description and identifiers for
        each asset, and can be used to iterate in batches using a pagination
        object.

        Definition: POST /v1/assets/query
        Required scopes: read_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/asset-service/get-many-assets-query

        Parameters
        ----------
        format : string, (optional)
            Alternative format for data to be returned inOne of: ExcelMessagePack
        where : FieldFilterMap, (optional)

        asOfTime : date-time, (optional)
            ISO 8601-formatted timestamp
        date : date, (optional)
            ISO 8601-formatted date
        time : date-time, (optional)
            ISO 8601-formatted timestamp
        delay : integer, (optional)

        orderBy : array containing any of the following: string,, (optional)

        scroll : string, (optional)
            Time for which to keep the scroll search context alive, i.e. 1m (1
            minute) or 10s (10 seconds)
        scrollId : string, (optional)
            Scroll identifier to be used to retrieve the next batch of results
        fields : array containing any of the following: string,, (optional)

        limit : integer, (optional)
            Limit on the number of objects to be returned in the response. Can
            range between 1 and 10000
        offset : integer, (optional)
            The offset of the first result returned (default 0). Can be used in
            pagination to defined the first item in the list to be returned, for
            example if you request 100 objects, to query the next page you would
            specify offset = 100.
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/assets/query'

        data = self._request(method='POST',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def create_asset_timeseries_data(self, return_df=False, **kwargs):
        '''
        Create timeseries data for asset and popluate asset stats

        Definition: POST /v1/assets/timeseries
        Required scopes: modify_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/asset-service/create-asset-timeseries-data

        Parameters
        ----------
        id : string, (read-only)
            Asset unique identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/assets/timeseries'

        data = self._request(method='POST',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def get_asset(self, id, return_df=False, **kwargs):
        '''
        Retrieve an asset based on its unique identifier. Returns an asset
        object which contains name, description, identifiers and other
        metadata.

        Definition: GET /v1/assets/{id}
        Required scopes: read_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/asset-service/get-an-asset

        Parameters
        ----------
        id : string, (read-only)
            Marquee unique asset identifier.
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/assets/{id}'

        request_url = request_url.format(id=id)
        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def update_asset(self, id, return_df=False, **kwargs):
        '''
        Apply an update to an existing asset in Marquee. User must have edit
        entitlement on the asset in order to update.

        Definition: PUT /v1/assets/{id}
        Required scopes: modify_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/asset-service/update-an-asset

        Parameters
        ----------
        id : string, (read-only)
            Marquee unique asset identifier.
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        assetClass : string
            Asset classification of security. Assets are classified into broad
            groups which exhibit similar characteristics and behave in a
            consistent way under different market conditionsOne of:
            CashCommodCreditCross AssetEquityFundFXMortgageRates
        currency : string, (optional)
            Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP
            vs GBp)One of: ACUADPAEDAFAALLAMDANGAOAAOKshow more
        description : string, (optional)
            Free text description of asset. Description provided will be indexed
            in the search service for free text relevance match
        domains : Domains, (optional)

        entitlements : Entitlements, (optional)
            Defines the entitlements of a given resource
        exchange : string, (optional)
            Name of marketplace where security, derivative or other instrument is
            traded
        identifiers : array of Identifier, (optional)
            Array of identifier objects which can be used to locate this item in
            searches and other services
        listed : boolean, (optional)
            Whether the asset is currently listed or not
        liveDate : date, (optional)
            ISO 8601-formatted date
        name : string
            Display name of the asset
        ownerId : string, (optional)
            Marquee unique identifier
        parameters : any of the following: Asset Parameters, Commod Config Parameters, Hedge Fund Parameters, Share Class Parameters, Instruments, (optional)

        assetStats : array of AssetStats, (optional)

        people : People, (optional)
            Key people associated with asset
        region : string, (optional)
            Regional classification for the assetOne of:
            AmericasAsiaEMEuropeGlobal
        reportIds : array of string, (optional)
            Array of report identifiers related to the object
        shortName : string, (optional)
            Short name or alias for the asset
        styles : array of string, (optional)
            Styles or themes associated with the asset (max 50)
        tags : array of string, (optional)
            Metadata associated with the object. Provide an array of strings which
            will be indexed for search and locating related objects
        type : string
            Asset type differentiates the product categorization or contract
            typeOne of: AccessBasisBasisSwapBenchmarkBenchmark RateBondCalendar
            SpreadCapCashCertificateshow more
        underlyingAssetIds : array of string, (optional)
            Underlying asset ids
        '''

        request_url = 'https://api.marquee.gs.com/v1/assets/{id}'

        request_url = request_url.format(id=id)
        data = self._request(method='PUT',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def delete_asset(self, id, return_df=False, **kwargs):
        '''
        Remove an asset from Marquee by identifier. User must have edit
        entitlement on the asset in order to delete.

        Definition: DELETE /v1/assets/{id}
        Required scopes: modify_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/asset-service/delete-an-asset

        Parameters
        ----------
        id : string, (read-only)
            Marquee unique asset identifier.
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/assets/{id}'

        request_url = request_url.format(id=id)
        data = self._request(method='DELETE',
                             url=request_url,
                             return_df=return_df)
        return data

    def get_asset_risk_models(self, id, return_df=False, **kwargs):
        '''
        Get available risk models for an asset based on region

        Definition: GET /v1/assets/{id}/models
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/asset-service/get-asset-risk-models

        Parameters
        ----------
        id : string, (optional)
            Marquee unique asset identifier.
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        asOfDate : array of date, (optional)
            Give risk models available as of this date
        '''

        request_url = 'https://api.marquee.gs.com/v1/assets/{id}/models'

        request_url = request_url.format(id=id)
        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def get_asset_positions(self, id, return_df=False, **kwargs):
        '''
        Retrieve positions for asset

        Definition: GET /v1/assets/{id}/positions
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/asset-service/get-asset-positions

        Parameters
        ----------
        id : string, (read-only)
            Marquee unique asset identifier.
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        field : array of, (optional)

        format : array of string, (optional)
            One of: Excel
        quantity : array of string, (optional)
            Quantity by which to scale by
        startDate : array of date, (optional)
            Start date for positions
        endDate : array of date, (optional)
            End date for positions
        type : array of string, (optional)
            One of: openclose
        '''

        request_url = 'https://api.marquee.gs.com/v1/assets/{id}/positions'

        request_url = request_url.format(id=id)
        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def get_asset_positions_data(self, id, return_df=False, **kwargs):
        '''
        Retrieve positions data for an asset

        Definition: GET /v1/assets/{id}/positions/data
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/asset-service/get-asset-positions-data

        Parameters
        ----------
        id : string, (read-only)
            Marquee unique asset identifier.
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        fields : array of, (optional)
            Field to be returned
        format : array of string, (optional)
            Alternative format for data to be returned inOne of: ExcelMessagePack
        quantity : array of string, (optional)
            Quantity of the given position
        startDate : array of date, (optional)
            Start date for positions
        endDate : array of date, (optional)
            End date for positions
        type : array of string, (optional)
            One of: openclose
        '''

        request_url = 'https://api.marquee.gs.com/v1/assets/{id}/positions/data'

        request_url = request_url.format(id=id)
        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def get_latest_asset_positions(self, id, return_df=False, **kwargs):
        '''
        Retrieve last positions for asset

        Definition: GET /v1/assets/{id}/positions/last
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/asset-service/get-latest-asset-positions

        Parameters
        ----------
        id : string, (read-only)
            Marquee unique asset identifier.
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        type : array of string, (optional)
            One of: openclose
        '''

        request_url = 'https://api.marquee.gs.com/v1/assets/{id}/positions/last'

        request_url = request_url.format(id=id)
        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def get_latest_asset_positions_data(self, id, return_df=False, **kwargs):
        '''
        Retrieve the latest positions data for an asset

        Definition: GET /v1/assets/{id}/positions/last/data
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/asset-service/get-latest-asset-positions-data

        Parameters
        ----------
        id : string, (read-only)
            Marquee unique asset identifier.
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        fields : array of, (optional)
            Field to be returned
        quantity : array of string, (optional)
            Quantity of the given position
        type : array of string, (optional)
            One of: openclose
        '''

        request_url = 'https://api.marquee.gs.com/v1/assets/{id}/positions/last/data'

        request_url = request_url.format(id=id)
        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def get_asset_positions_for_date(self, id, date, return_df=False, **kwargs):
        '''
        Retrieve positions for asset for a given date

        Definition: GET /v1/assets/{id}/positions/{date}
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/asset-service/get-asset-positions-for-a-date

        Parameters
        ----------
        id : string, (read-only)
            Marquee unique asset identifier.
        date : date, (optional)
            ISO 8601-formatted date
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        type : array of string, (optional)
            One of: openclose
        '''

        request_url = 'https://api.marquee.gs.com/v1/assets/{id}/positions/{date}'

        request_url = request_url.format(id=id, date=date)
        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def get_asset_stats_timeseries_curve(self, id, return_df=False, **kwargs):
        '''
        Retrieve calculated stats curve and most recent stats and stats
        history for a given asset.

        Definition: GET /v1/assets/{id}/timeseries
        Required scopes: read_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/asset-service/get-asset-stats-timeseries-curve

        Parameters
        ----------
        id : string, (read-only)
            Marquee unique asset identifier.
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        metrics : array of string, (optional)
            One of: performanceannualizedVolatilitysharpeRatiomaxDrawdowncorrelati
            onbetaratio
        startDate : array of date, (optional)
            Start date for stats curve calcuation
        endDate : array of date, (optional)
            End date for stats curve calcuation
        benchmarkIds : array of string, (optional)
            Benchmark ids
        window : array of string, (optional)
            Window size to calculate rolling stats curve
        includeStats : array of string, (optional)
            One of: truefalse
        intervals : array of string, (optional)
            Number of intervals for which to return real time output times, for
            example if 10, it will return 10 data points evenly spaced over the
            time/date range
        '''

        request_url = 'https://api.marquee.gs.com/v1/assets/{id}/timeseries'

        request_url = request_url.format(id=id)
        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def get_asset_xrefs(self, id, return_df=False, **kwargs):
        '''
        Get asset xrefs

        Definition: GET /v1/assets/{id}/xrefs
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/asset-service/get-asset-xrefs

        Parameters
        ----------
        id : str
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/assets/{id}/xrefs'

        request_url = request_url.format(id=id)
        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def put_asset_xrefs(self, id, return_df=False, **kwargs):
        '''
        Update asset xrefs

        Definition: PUT /v1/assets/{id}/xrefs
        Required scopes: modify_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/asset-service/put-asset-xrefs

        Parameters
        ----------
        id : string, (optional)
            Marquee unique asset identifier.
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/assets/{id}/xrefs'

        request_url = request_url.format(id=id)
        data = self._request(method='PUT',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def get_asset_xrefs_for_date(self, id, date, return_df=False, **kwargs):
        '''
        Get asset xrefs for date

        Definition: GET /v1/assets/{id}/xrefs/{date}
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/asset-service/get-asset-xrefs-for-date

        Parameters
        ----------
        id : str
        date : str
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/assets/{id}/xrefs/{date}'

        request_url = request_url.format(id=id, date=date)
        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def get_many_backtests(self, return_df=False, **kwargs):
        '''
        Retrieve all entitled backtests

        Definition: GET /v1/backtests
        Required scopes: read_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/backtest-service/get-many-backtests

        Parameters
        ----------
        limit : array of string, (optional)
            Maximum number of results to be returned in the result set.
        offset : array of string, (optional)
            Offset of first result to return from the server
        scroll : array of string, (optional)
            Time for which to keep the scroll search context alive, i.e. 1m (1
            minute) or 10s (10 seconds).
        scrollId : array of string, (optional)
            Scroll identifier to be used to retrieve the next batch of results
        orderBy : array containing any of the following: string,, (optional)
            Field name by which to order backtest results.
        createdById : array of string, (optional)
            Filter by id of user who created the object
        id : array of string, (optional)
            Filter by id
        ownerId : array of string, (optional)
            Filter by owner ID
        name : array of string, (optional)
            Filter by name (exact match).
        lastUpdatedById : array of string, (optional)
            Filter by last updated user id
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/backtests'

        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def create_backtest(self, return_df=False, **kwargs):
        '''
        Create a new backtest in marquee

        Definition: POST /v1/backtests
        Required scopes: modify_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/backtest-service/create-a-backtest

        Parameters
        ----------
        costNetting : boolean, (optional)
            Nets trading costs across the leaf nodes of the strategy.
        currency : string, (optional)
            Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP
            vs GBp)One of: ACUADPAEDAFAALLAMDANGAOAAOKshow more
        entitlements : Entitlements, (optional)
            Defines the entitlements of a given resource
        name : string
            Display name of the basket
        ownerId : string, (optional)
            Marquee unique identifier
        reportIds : array of string, (optional)
            Array of report identifiers related to the object
        parameters : any of the following: Basket Backtest Parameters, Volatility Backtest Parameters, Enhanced Beta Backtest Parameters, (optional)

        startDate : date, (optional)
            Start date of backtest selected by user. If not selected, defaults to
            start of backtest timeseries.
        endDate : date, (optional)
            End date of backtest selected by user. If not selected, defaults to
            end of backtest timeseries.
        type : string
            Type of Backtest.One of: BasketVolatilityEnhanced Beta
        assetClass : string
            Asset class of the backtest underliers.One of: CashCommodCreditCross
            AssetEquityFundFXMortgageRates
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/backtests'

        data = self._request(method='POST',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def update_backtest_reference_data(self, return_df=False, **kwargs):
        '''
        Update backtest reference

        Definition: PUT /v1/backtests/refData
        Required scopes: modify_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/backtest-service/update-backtest-reference-data

        Parameters
        ----------
        volatility : BacktestRefData.volatility, (optional)

        enhanced beta : Enhanced Beta Reference Data, (optional)
            Enhanced Beta backtest reference data
        basket : Basket Backtest Reference Data, (optional)
            Basket backtest reference data
        ownerId : string, (optional)
            Marquee unique identifier for user who owns the object.
        entitlements : Entitlements, (optional)
            Defines the entitlements of a given resource
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/backtests/refData'

        data = self._request(method='PUT',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def get_backtest_reference_data(self, return_df=False, **kwargs):
        '''
        Get backtest reference data

        Definition: GET /v1/backtests/refData
        Required scopes: read_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/backtest-service/get-backtest-reference-data

        Parameters
        ----------
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/backtests/refData'

        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def get_many_backtest_results(self, return_df=False, **kwargs):
        '''
        Returns statistics and performance curves for many backtests

        Definition: GET /v1/backtests/results
        Required scopes: read_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/backtest-service/get-many-backtest-results

        Parameters
        ----------
        limit : array of string, (optional)
            Maximum number of results to be returned in the result set.
        offset : array of string, (optional)
            Offset of first result to return from the server
        scroll : array of string, (optional)
            Time for which to keep the scroll search context alive, i.e. 1m (1
            minute) or 10s (10 seconds).
        scrollId : array of string, (optional)
            Scroll identifier to be used to retrieve the next batch of results
        orderBy : array containing any of the following: string,, (optional)
            Field name by which to order backtest results.
        ids : array of string, (optional)
            Filter by a unique backtest Id.
        comparisonIds : array of string, (optional)
            Marquee unique identifier of the entity to compare backtest
            performance.
        startDate : array of date, (optional)
            Start date for performance backtest data, defaults to start of time.
        endDate : array of date, (optional)
            End date for performance backtest data, defaults to today.
        createdById : array of string, (optional)
            Filter by id of user who created the object
        id : array of string, (optional)
            Filter by id
        ownerId : array of string, (optional)
            Filter by owner ID
        name : array of string, (optional)
            Filter by name (exact match).
        lastUpdatedById : array of string, (optional)
            Filter by last updated user id
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/backtests/results'

        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def get_backtest(self, id, return_df=False, **kwargs):
        '''
        Retrieve an backtest based on its unique identifier. Returns an
        backtest object which contains name, description, and other metadata.

        Definition: GET /v1/backtests/{id}
        Required scopes: read_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/backtest-service/get-a-backtest

        Parameters
        ----------
        id : string, (read-only)
            Marquee unique backtest identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/backtests/{id}'

        request_url = request_url.format(id=id)
        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def update_backtest(self, id, return_df=False, **kwargs):
        '''
        Apply an update to an existing backtest in Marquee. User must have
        edit entitlement on the backtest in order to update.

        Definition: PUT /v1/backtests/{id}
        Required scopes: modify_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/backtest-service/update-a-backtest

        Parameters
        ----------
        id : string, (read-only)
            Marquee unique backtest identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        costNetting : boolean, (optional)
            Nets trading costs across the leaf nodes of the strategy.
        currency : string, (optional)
            Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP
            vs GBp)One of: ACUADPAEDAFAALLAMDANGAOAAOKshow more
        entitlements : Entitlements, (optional)
            Defines the entitlements of a given resource
        name : string
            Display name of the basket
        ownerId : string, (optional)
            Marquee unique identifier
        reportIds : array of string, (optional)
            Array of report identifiers related to the object
        parameters : any of the following: Basket Backtest Parameters, Volatility Backtest Parameters, Enhanced Beta Backtest Parameters, (optional)

        startDate : date, (optional)
            Start date of backtest selected by user. If not selected, defaults to
            start of backtest timeseries.
        endDate : date, (optional)
            End date of backtest selected by user. If not selected, defaults to
            end of backtest timeseries.
        type : string
            Type of Backtest.One of: BasketVolatilityEnhanced Beta
        assetClass : string
            Asset class of the backtest underliers.One of: CashCommodCreditCross
            AssetEquityFundFXMortgageRates
        '''

        request_url = 'https://api.marquee.gs.com/v1/backtests/{id}'

        request_url = request_url.format(id=id)
        data = self._request(method='PUT',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def delete_backtest(self, id, return_df=False, **kwargs):
        '''
        Delete an existing backtest in Marquee by id. User must have edit
        entitlement on the backtest in order to delete.

        Definition: DELETE /v1/backtests/{id}
        Required scopes: modify_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/backtest-service/delete-a-backtest

        Parameters
        ----------
        id : string, (read-only)
            Marquee unique backtest identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/backtests/{id}'

        request_url = request_url.format(id=id)
        data = self._request(method='DELETE',
                             url=request_url,
                             return_df=return_df)
        return data

    def schedule_backtest(self, id, return_df=False, **kwargs):
        '''
        Schedule execution of reports for a backtest

        Definition: POST /v1/backtests/{id}/schedule
        Required scopes: run_analytics
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/backtest-service/schedule-a-backtest

        Parameters
        ----------
        id : string, (read-only)
            Marquee unique backtest identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/backtests/{id}/schedule'

        request_url = request_url.format(id=id)
        data = self._request(method='POST',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def get_catalog_entries(self, return_df=False, **kwargs):
        '''
        Get dataset metadata accessible to the user

        Definition: GET /v1/data/catalog
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/data-service/get-catalog-entries

        Parameters
        ----------
        dataSetId : array of string, (optional)
            Filter datasets by id
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/data/catalog'

        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def get_catalog_entry(self, dataSetId, return_df=False, **kwargs):
        '''
        Get metadata on a given dataset by unique identifier

        Definition: GET /v1/data/catalog/{dataSetId}
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/data-service/get-catalog-entry

        Parameters
        ----------
        dataSetId : string, (optional)
            Marquee unique identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/data/catalog/{dataSetId}'

        request_url = request_url.format(dataSetId=dataSetId)
        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def get_viewable_datasets(self, return_df=False, **kwargs):
        '''
        Get datasets that current user is allowed to view.

        Definition: GET /v1/data/datasets
        Required scopes: read_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/data-service/get-viewable-datasets

        Parameters
        ----------
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/data/datasets'

        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def create_dataset_definition(self, return_df=False, **kwargs):
        '''
        Create new dataset definition

        Definition: POST /v1/data/datasets
        Required scopes: modify_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/data-service/create-dataset-definition

        Parameters
        ----------
        ownerId : string, (optional)
            Marquee unique identifier for user who owns the object.
        id : string
            Unique id of dataset.
        name : string
            Name of dataset.
        description : string, (optional)
            Description of dataset.
        shortDescription : string, (optional)
            Short description of dataset.
        vendor : string
            One of: Goldman SachsThomson ReutersSolactiveBloombergAxiomaGoldman
            Sachs Prime ServicesGoldman Sachs Global Investment ResearchNational
            Weather ServiceWMHedge Fund Research, Inc.show more
        startDate : date, (optional)
            The start of this data set
        mdapi : MDAPI Fields, (optional)
            Defines MDAPI fields.
        dataProduct : string
            Product that dataset belongs to.
        entitlements : Entitlements, (optional)
            Defines the entitlements of a given resource
        queryProcessors : ProcessorEntity, (optional)
            Query processors for dataset.
        parameters : DataSetParameters
            Dataset parameters.
        dimensions : DataSetDimensions
            Dataset dimensions.
        defaults : DataSetDefaults, (optional)
            Default settings.
        filters : DataSetFilters, (optional)
            Filters to restrict the set of data returned.
        tags : array of string, (optional)
            Tags associated with dataset.
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/data/datasets'

        data = self._request(method='POST',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def get_dataset_availability(self, return_df=False, **kwargs):
        '''
        Get available datasets for symbol dimensions.

        Definition: GET /v1/data/datasets/availability
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/data-service/get-dataset-availability

        Parameters
        ----------
        assetId : array of string, (optional)
            Filter by assetId
        gsid : array of string, (optional)
            Filter by gsid
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/data/datasets/availability'

        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def update_dataset_definition(self, dataSetId, return_df=False, **kwargs):
        '''
        Update (overwrite) existing dataset definition

        Definition: PUT /v1/data/datasets/{dataSetId}
        Required scopes: modify_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/data-service/update-dataset-definition

        Parameters
        ----------
        dataSetId : string, (optional)
            Marquee unique identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        ownerId : string, (optional)
            Marquee unique identifier for user who owns the object.
        id : string
            Unique id of dataset.
        name : string
            Name of dataset.
        description : string, (optional)
            Description of dataset.
        shortDescription : string, (optional)
            Short description of dataset.
        vendor : string
            One of: Goldman SachsThomson ReutersSolactiveBloombergAxiomaGoldman
            Sachs Prime ServicesGoldman Sachs Global Investment ResearchNational
            Weather ServiceWMHedge Fund Research, Inc.show more
        startDate : date, (optional)
            The start of this data set
        mdapi : MDAPI Fields, (optional)
            Defines MDAPI fields.
        dataProduct : string
            Product that dataset belongs to.
        entitlements : Entitlements, (optional)
            Defines the entitlements of a given resource
        queryProcessors : ProcessorEntity, (optional)
            Query processors for dataset.
        parameters : DataSetParameters
            Dataset parameters.
        dimensions : DataSetDimensions
            Dataset dimensions.
        defaults : DataSetDefaults, (optional)
            Default settings.
        filters : DataSetFilters, (optional)
            Filters to restrict the set of data returned.
        tags : array of string, (optional)
            Tags associated with dataset.
        '''

        request_url = 'https://api.marquee.gs.com/v1/data/datasets/{dataSetId}'

        request_url = request_url.format(dataSetId=dataSetId)
        data = self._request(method='PUT',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def get_dataset_definition(self, dataSetId, return_df=False, **kwargs):
        '''
        Get dataset definition.

        Definition: GET /v1/data/datasets/{dataSetId}
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/data-service/get-dataset-definition

        Parameters
        ----------
        dataSetId : string
            Marquee unique identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/data/datasets/{dataSetId}'

        request_url = request_url.format(dataSetId=dataSetId)
        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def delete_dataset_definition(self, dataSetId, return_df=False, **kwargs):
        '''
        Delete dataset definition.

        Definition: DELETE /v1/data/datasets/{dataSetId}
        Required scopes: modify_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/data-service/delete-dataset-definition

        Parameters
        ----------
        dataSetId : string
            Marquee unique identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/data/datasets/{dataSetId}'

        request_url = request_url.format(dataSetId=dataSetId)
        data = self._request(method='DELETE',
                             url=request_url,
                             return_df=return_df)
        return data

    def bulk_query_last_data(self, return_df=False, **kwargs):
        '''
        Query last data points across multiple datasets.

        Definition: POST /v1/data/last/query/bulk
        Required scopes: read_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/data-service/bulk-query-last-data

        Parameters
        ----------
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/data/last/query/bulk'

        data = self._request(method='POST',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def stream_data(self, return_df=False, **kwargs):
        '''
        Receive a stream of data updates over a websocket. For details on
        streaming protocol and usage please contact the developer support team
        at developer@gs.com.

        Definition: GET /v1/data/stream
        Required scopes: read_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/data-service/stream-data

        Parameters
        ----------
        dataSetId : string, (optional)
            Marquee unique identifier
        format : string, (optional)
            Alternative format for data to be returned inOne of: ExcelMessagePack
        where : FieldFilterMap, (optional)
            Filters on data fields.
        startDate : date, (optional)
            ISO 8601-formatted date
        endDate : date, (optional)
            ISO 8601-formatted date
        startTime : date-time, (optional)
            ISO 8601-formatted timestamp
        endTime : date-time, (optional)
            ISO 8601-formatted timestamp
        asOfTime : date-time, (optional)
            ISO 8601-formatted timestamp
        idAsOfDate : date, (optional)
            ISO 8601-formatted date
        since : date-time, (optional)
            ISO 8601-formatted timestamp
        dates : array of date, (optional)
            Select and return specific dates from dataset query results.
        times : array of date-time, (optional)
            Select and return specific times from dataset query results.
        delay : integer, (optional)
            Number of minutes to delay returning data.
        intervals : integer, (optional)
            Number of intervals for which to return output times, for example if
            10, it will return 10 data points evenly spaced over the time/date
            range.
        pollingInterval : integer, (optional)
            When streaming, wait for this number of seconds between poll attempts.
        groupBy : array of, (optional)
            Fields that determine grouping of results. Defaults to the dimensions
            of the dataset.
        grouped : boolean, (optional)
            Set to true to return results grouped by a given context (set of
            dimensions).
        fields : array containing any of the following: string,, (optional)
            Fields to be returned.
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/data/stream'

        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def upload_data(self, dataSetId, return_df=False, **kwargs):
        '''
        Upload data to Marquee. You must specify all required dimensions for
        the given dataset, but can upload data for multiple dates and
        dimensions in one request.

        Definition: POST /v1/data/{dataSetId}
        Required scopes: modify_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/data-service/upload-data

        Parameters
        ----------
        dataSetId : string, (optional)
            Marquee unique identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/data/{dataSetId}'

        request_url = request_url.format(dataSetId=dataSetId)
        data = self._request(method='POST',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def get_data(self, dataSetId, return_df=False, **kwargs):
        '''
        Retrieve data for a set of dimensions and a date or time range from
        the specified dataset.

        Definition: GET /v1/data/{dataSetId}
        Required scopes: read_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/data-service/get-data

        Parameters
        ----------
        dataSetId : string, (optional)
            Marquee unique identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        fields : array of string, (optional)
            Fields to be returned from dataset. Optionally can specify function to
            be applied to field data
        startDate : array of date, (optional)
            First date for which to query dataset (inclusive)
        endDate : array of date, (optional)
            Last date for which to query dataset (inclusive)
        dates : array of date, (optional)
            Select and return specific dates from dataset query results.
        startTime : array of date-time, (optional)
            First time for which to query dataset (inclusive)
        endTime : array of date-time, (optional)
            Last time for which to query dataset (inclusive)
        times : array of date-time, (optional)
            Select and return specific times from dataset query results
        intervals : array of string, (optional)
            Number of intervals for which to return output times, for example if
            10, it will return 10 data points evenly spaced over the time/date
            range
        asOfTime : array of date-time, (optional)
            For bi-temporal datasets, will query as of the specified time
        idAsOfDate : array of date, (optional)
            If secondary identifiers are specified, find corresponding assets as
            of this date
        since : array of date-time, (optional)
            For bi-temporal datasets, only return data updated since this time
        grouped : array of string, (optional)
            One of: truefalse
        groupBy : array of string, (optional)
            Fields that determine grouping of results. Defaults to the dimensions
            of the data set
        format : array of string, (optional)
            Alternative format for data to be returned inOne of: ExcelMessagePack
        exchange : array of string, (optional)
            Filter by GS exchange code
        ticker : array of string, (optional)
            Filter by Ticker.
        bcid : array of string, (optional)
            Filter by Bloomberg Composite ID.
        bbid : array of string, (optional)
            Filter by Bloomberg ID.
        bbidEquivalent : array of string, (optional)
            Filter by Bloomberg equivalent ID.
        sedol : array of string, (optional)
            Filter by SEDOL (subject to licensing).
        '''

        request_url = 'https://api.marquee.gs.com/v1/data/{dataSetId}'

        request_url = request_url.format(dataSetId=dataSetId)
        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def get_dataset_coverage(self, dataSetId, return_df=False, **kwargs):
        '''
        Get coverage for a given dataset by returning the set of assets for
        which data exists

        Definition: GET /v1/data/{dataSetId}/coverage
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/data-service/get-dataset-coverage

        Parameters
        ----------
        dataSetId : string, (optional)
            Marquee unique identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        limit : array of string, (optional)
            Maximum number of results to be returned in the result set.
        offset : array of string, (optional)
            Offset of first result to return from the server
        scroll : array of string, (optional)
            Time for which to keep the scroll search context alive, i.e. 1m (1
            minute) or 10s (10 seconds).
        scrollId : array of string, (optional)
            Scroll identifier to be used to retrieve the next batch of results
        fields : array of string, (optional)
            Additional asset fields to be returned (for datasets that are queried
            by asset).
        '''

        request_url = 'https://api.marquee.gs.com/v1/data/{dataSetId}/coverage'

        request_url = request_url.format(dataSetId=dataSetId)
        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def get_last_data(self, dataSetId, return_df=False, **kwargs):
        '''
        Retrieve data for a set of dimensions and time range from the
        specified dataset. Implicitly applies the last function to each field
        (i.e. get the last occurring value of each field) and returns a single
        data point per asset. Useful in datasets where not all data points
        return the same fields each time. May only be used with time-based
        datasets.

        Definition: GET /v1/data/{dataSetId}/last
        Required scopes: read_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/data-service/get-last-data

        Parameters
        ----------
        dataSetId : string, (optional)
            Marquee unique identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        fields : array of string, (optional)
            Fields to be returned from dataset. Optionally can specify function to
            be applied to field data
        startTime : array of date-time, (optional)
            First time for which to query dataset (inclusive)
        endTime : array of date-time, (optional)
            Last time for which to query dataset (inclusive)
        times : array of date-time, (optional)
            Select and return specific times from dataset query results
        intervals : array of string, (optional)
            Number of intervals for which to return output times, for example if
            10, it will return 10 data points evenly spaced over the time/date
            range
        asOfTime : array of date-time, (optional)
            For bi-temporal, time-based datasets, will query as of the specified
            time
        since : array of date-time, (optional)
            For bi-temporal, time-based datasets, only return data updated since
            this time
        grouped : array of string, (optional)
            One of: truefalse
        groupBy : array of string, (optional)
            Fields that determine grouping of results. Defaults to the dimensions
            of the data set
        format : array of string, (optional)
            Alternative format for data to be returned inOne of: ExcelMessagePack
        exchange : array of string, (optional)
            Filter by GS exchange code
        ticker : array of string, (optional)
            Filter by Ticker.
        bcid : array of string, (optional)
            Filter by Bloomberg Composite ID.
        bbid : array of string, (optional)
            Filter by Bloomberg ID.
        bbidEquivalent : array of string, (optional)
            Filter by Bloomberg equivalent ID.
        sedol : array of string, (optional)
            Filter by SEDOL (subject to licensing).
        '''

        request_url = 'https://api.marquee.gs.com/v1/data/{dataSetId}/last'

        request_url = request_url.format(dataSetId=dataSetId)
        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def query_last_data(self, dataSetId, return_df=False, **kwargs):
        '''
        Performs the same function as the Get Last Data endpoint but passes
        the query as JSON in the request body.

        Definition: POST /v1/data/{dataSetId}/last/query
        Required scopes: read_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/data-service/query-last-data

        Parameters
        ----------
        dataSetId : string, (optional)
            Marquee unique identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        dataSetId : string, (optional)
            Marquee unique identifier
        format : string, (optional)
            Alternative format for data to be returned inOne of: ExcelMessagePack
        where : FieldFilterMap, (optional)
            Filters on data fields.
        startDate : date, (optional)
            ISO 8601-formatted date
        endDate : date, (optional)
            ISO 8601-formatted date
        startTime : date-time, (optional)
            ISO 8601-formatted timestamp
        endTime : date-time, (optional)
            ISO 8601-formatted timestamp
        asOfTime : date-time, (optional)
            ISO 8601-formatted timestamp
        idAsOfDate : date, (optional)
            ISO 8601-formatted date
        since : date-time, (optional)
            ISO 8601-formatted timestamp
        dates : array of date, (optional)
            Select and return specific dates from dataset query results.
        times : array of date-time, (optional)
            Select and return specific times from dataset query results.
        delay : integer, (optional)
            Number of minutes to delay returning data.
        intervals : integer, (optional)
            Number of intervals for which to return output times, for example if
            10, it will return 10 data points evenly spaced over the time/date
            range.
        pollingInterval : integer, (optional)
            When streaming, wait for this number of seconds between poll attempts.
        groupBy : array of, (optional)
            Fields that determine grouping of results. Defaults to the dimensions
            of the dataset.
        grouped : boolean, (optional)
            Set to true to return results grouped by a given context (set of
            dimensions).
        fields : array containing any of the following: string,, (optional)
            Fields to be returned.
        '''

        request_url = 'https://api.marquee.gs.com/v1/data/{dataSetId}/last/query'

        request_url = request_url.format(dataSetId=dataSetId)
        data = self._request(method='POST',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def query_data(self, dataSetId, return_df=False, **kwargs):
        '''
        Performs the same function as the Get Data endpoint but passes the
        query as JSON in the request body.

        Definition: POST /v1/data/{dataSetId}/query
        Required scopes: read_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/data-service/query-data

        Parameters
        ----------
        dataSetId : string, (optional)
            Marquee unique identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        dataSetId : string, (optional)
            Marquee unique identifier
        format : string, (optional)
            Alternative format for data to be returned inOne of: ExcelMessagePack
        where : FieldFilterMap, (optional)
            Filters on data fields.
        startDate : date, (optional)
            ISO 8601-formatted date
        endDate : date, (optional)
            ISO 8601-formatted date
        startTime : date-time, (optional)
            ISO 8601-formatted timestamp
        endTime : date-time, (optional)
            ISO 8601-formatted timestamp
        asOfTime : date-time, (optional)
            ISO 8601-formatted timestamp
        idAsOfDate : date, (optional)
            ISO 8601-formatted date
        since : date-time, (optional)
            ISO 8601-formatted timestamp
        dates : array of date, (optional)
            Select and return specific dates from dataset query results.
        times : array of date-time, (optional)
            Select and return specific times from dataset query results.
        delay : integer, (optional)
            Number of minutes to delay returning data.
        intervals : integer, (optional)
            Number of intervals for which to return output times, for example if
            10, it will return 10 data points evenly spaced over the time/date
            range.
        pollingInterval : integer, (optional)
            When streaming, wait for this number of seconds between poll attempts.
        groupBy : array of, (optional)
            Fields that determine grouping of results. Defaults to the dimensions
            of the dataset.
        grouped : boolean, (optional)
            Set to true to return results grouped by a given context (set of
            dimensions).
        fields : array containing any of the following: string,, (optional)
            Fields to be returned.
        '''

        request_url = 'https://api.marquee.gs.com/v1/data/{dataSetId}/query'

        request_url = request_url.format(dataSetId=dataSetId)
        data = self._request(method='POST',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def create_document(self, namespace, return_df=False, **kwargs):
        '''
        Accepts a file uploa adnd create a new root Document object using the
        file name (if present), content type, and size of the uploaded file.
        Default entitlements are view/edit/delete for owner (the user
        performing the upload). Adds a new Document object within {namespace}
        and returns its ID and other generated fields.

        Definition: POST /v1/documents/{namespace}
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/document-service/create-a-document

        Parameters
        ----------
        namespace : string
            Namespace the document should be created in
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/documents/{namespace}'

        request_url = request_url.format(namespace=namespace)
        data = self._request(method='POST',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def create_document_given_metadata(self, namespace, return_df=False, **kwargs):
        '''
        Creates a new document object given some metadata. The document will
        have content type application/octet-stream and size zero.

        Definition: POST /v1/documents/{namespace}/metadata
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/document-service/create-a-document-given-metadata

        Parameters
        ----------
        namespace : string
            Namespace the document should be created in
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        name : string
            Title of the document
        slug : string, (optional)
            Optional slug that could be used to refer to this document
        status : string, (optional)
            One of: DraftPublishedRetracted
        publishedDate : date-time, (optional)
            ISO 8601-formatted timestamp
        properties : DocumentProperties, (optional)

        entitlements : Entitlements, (optional)
            Entitlement demands to view, edit, and delete the document
        '''

        request_url = 'https://api.marquee.gs.com/v1/documents/{namespace}/metadata'

        request_url = request_url.format(namespace=namespace)
        data = self._request(method='POST',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def get_document(self, namespace, id, return_df=False, **kwargs):
        '''
        Retrieve content of a document using ID. Content is streamed with
        proper HTTP headers so that it can be directly consumed by a browser
        to render or download.

        Definition: GET /v1/documents/{namespace}/{id}
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/document-service/get-a-document

        Parameters
        ----------
        namespace : string
            Namespace the document belongs to
        id : string
            Unique identifier of the document
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/documents/{namespace}/{id}'

        request_url = request_url.format(namespace=namespace, id=id)
        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def update_document(self, namespace, id, return_df=False, **kwargs):
        '''
        Updates content of the document identified by {id} in {namespace},
        including the content type and size.

        Definition: PUT /v1/documents/{namespace}/{id}
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/document-service/update-a-document

        Parameters
        ----------
        namespace : string
            Namespace the document belongs to
        id : string
            Unique identifier of the document
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        version : array of string
            Version identifier of the document being updated
        '''

        request_url = 'https://api.marquee.gs.com/v1/documents/{namespace}/{id}'

        request_url = request_url.format(namespace=namespace, id=id)
        data = self._request(method='PUT',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def delete_document(self, namespace, id, return_df=False, **kwargs):
        '''
        Soft-deletes a document.

        Definition: DELETE /v1/documents/{namespace}/{id}
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/document-service/delete-a-document

        Parameters
        ----------
        namespace : string
            Namespace the document belongs to
        id : string
            Unique identifier of the document
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/documents/{namespace}/{id}'

        request_url = request_url.format(namespace=namespace, id=id)
        data = self._request(method='DELETE',
                             url=request_url,
                             return_df=return_df)
        return data

    def get_document_metadata(self, namespace, id, return_df=False, **kwargs):
        '''
        Retrieve metadata for a document using ID.

        Definition: GET /v1/documents/{namespace}/{id}/metadata
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/document-service/get-document-metadata

        Parameters
        ----------
        namespace : string
            Namespace the document belongs to
        id : string
            Unique identifier of the document
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/documents/{namespace}/{id}/metadata'

        request_url = request_url.format(namespace=namespace, id=id)
        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def update_document_metadata(self, namespace, id, return_df=False, **kwargs):
        '''
        Updates the document identified by {id} in {namespace}. Supports
        concurrency control via the version field.

        Definition: PUT /v1/documents/{namespace}/{id}/metadata
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/document-service/update-document-metadata

        Parameters
        ----------
        namespace : string
            Namespace the document belongs to
        id : string
            Unique identifier of the document
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        id : string
            Unique identifier of the document
        version : string
            Version identifier, used to control concurrent updates
        name : string
            Title of the document
        slug : string, (optional)
            Optional slug that could be used to refer to this document
        status : string, (optional)
            One of: DraftPublishedRetracted
        publishedDate : date-time, (optional)
            ISO 8601-formatted timestamp
        properties : DocumentProperties, (optional)

        entitlements : Entitlements, (optional)
            Entitlement demands to view, edit, and delete the document
        '''

        request_url = 'https://api.marquee.gs.com/v1/documents/{namespace}/{id}/metadata'

        request_url = request_url.format(namespace=namespace, id=id)
        data = self._request(method='PUT',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def get_many_groups(self, return_df=False, **kwargs):
        '''
        Retrieve multiple groups by ids or enumerate groups using a pagination
        object.

        Definition: GET /v1/groups
        Required scopes: read_user_profile
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/groups-service/get-many-groups

        Parameters
        ----------
        id : array of string, (optional)
            Filter by group id
        name : array of string, (optional)
            Filter by name
        oeId : array of string, (optional)
            Filter by oe id of the group
        ownerId : array of string, (optional)
            Filter by owner id of the group
        tags : array of string, (optional)
            Filter by tags
        userIds : array of string, (optional)
            Filter by user ids
        scrollId : array of string, (optional)
            Scroll identifier to be used to retrieve the next batch of results
        scrollTime : array of string, (optional)
            Time for which to keep the scroll search context alive, i.e. 1m (1
            minute) or 10s (10 seconds)
        limit : array of string, (optional)
            Limit on the number of objects to be returned in the response. Can
            range between 1 and 100
        offset : array of string, (optional)
            The offset of the first result returned (default 0). Can be used in
            pagination to defined the first item in the list to be returned, for
            example if you request 100 objects, to query the next page you would
            specify offset = 100.
        orderBy : array containing, (optional)
            Field name by which to order results
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/groups'

        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def get_many_hedges(self, return_df=False, **kwargs):
        '''
        Retrieve multiple saved hedges by ids or enumerate using a pagination
        object in Marquee.

        Definition: GET /v1/hedges
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/hedge-service/get-many-hedges

        Parameters
        ----------
        ids : array of string, (optional)
            Filter hedges by id
        limit : array of string, (optional)
            Maximum number of results to be returned in the result set.
        offset : array of string, (optional)
            Offset of first result to return from the server
        fields : array of, (optional)
            Fields to be returned from data set. Optionally can specify function
            to be applied to field data
        format : array of string, (optional)
            One of: Excel
        orderBy : array containing any of the following: string,, (optional)
            Field name by which to order results
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/hedges'

        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def create_hedge(self, return_df=False, **kwargs):
        '''
        Create an object that stores the inputs of a hedge in marquee.

        Definition: POST /v1/hedges
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/hedge-service/create-a-hedge

        Parameters
        ----------
        ownerId : string, (optional)
            Marquee unique identifier for user who owns the object.
        entitlements : Entitlements, (optional)
            Defines the entitlements of a given resource
        tags : array of string, (optional)
            Metadata associated with the object. Provide an array of strings which
            will be indexed for search and locating related objects
        name : string
            Display name of the hedge
        description : string, (optional)
            Free text description of a Hedge
        objective : string, (optional)
            The objective of the hedge.One of: Minimize Factor RiskReplicate
            Performance
        parameters : any of the following: Factor Hedge Parameters, Performance Hedge Parameters
            The parameters used in the hedge calculation.
        result : any of the following: Factor Hedge Result, Performance Hedge Result, (optional)
            Result of the hedge.
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/hedges'

        data = self._request(method='POST',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def calculate_hedge(self, return_df=False, **kwargs):
        '''
        Perform a hedging calculation on a Marquee Asset or Portfolio to
        achieve a given objective.

        Definition: POST /v1/hedges/calculations
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/hedge-service/calculate-a-hedge

        Parameters
        ----------
        objective : string
            The objective of the hedge.One of: Minimize Factor RiskReplicate
            Performance
        parameters : any of the following: Factor Hedge Parameters, Performance Hedge Parameters
            The parameters used in the hedge calculation.
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/hedges/calculations'

        data = self._request(method='POST',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def get_hedge_data(self, return_df=False, **kwargs):
        '''
        Returns information about Hedges available in Marquee as a table. The
        caller can specify which fields are returned.

        Definition: GET /v1/hedges/data
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/hedge-service/get-hedge-data

        Parameters
        ----------
        limit : array of string, (optional)
            Maximum number of results to be returned in the result set.
        offset : array of string, (optional)
            Offset of first result to return from the server
        ids : array of string, (optional)
            Filter hedges by id
        fields : array of, (optional)
            Fields to be returned from data set. Optionally can specify function
            to be applied to field data
        orderBy : array containing any of the following: string,, (optional)
            Field name by which to order results
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/hedges/data'

        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def get_hedge_data_query(self, return_df=False, **kwargs):
        '''
        Get hedge data query

        Definition: POST /v1/hedges/data/query
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/hedge-service/get-hedge-data-query

        Parameters
        ----------
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/hedges/data/query'

        data = self._request(method='POST',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def get_many_hedges_query(self, return_df=False, **kwargs):
        '''
        Return information about hedges available in marquee. The response
        includes name, description and identifiers for each portfolio, and can
        be used to iterate in batches using a pagination object.

        Definition: POST /v1/hedges/query
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/hedge-service/get-many-hedges-query

        Parameters
        ----------
        format : string, (optional)
            Alternative format for data to be returned inOne of: ExcelMessagePack
        where : FieldFilterMap, (optional)

        asOfTime : date-time, (optional)
            ISO 8601-formatted timestamp
        date : date, (optional)
            ISO 8601-formatted date
        time : date-time, (optional)
            ISO 8601-formatted timestamp
        delay : integer, (optional)

        orderBy : array containing any of the following: string,, (optional)

        scroll : string, (optional)
            Time for which to keep the scroll search context alive, i.e. 1m (1
            minute) or 10s (10 seconds)
        scrollId : string, (optional)
            Scroll identifier to be used to retrieve the next batch of results
        fields : array containing any of the following: string,, (optional)

        limit : integer, (optional)
            Limit on the number of objects to be returned in the response. Can
            range between 1 and 10000
        offset : integer, (optional)
            The offset of the first result returned (default 0). Can be used in
            pagination to defined the first item in the list to be returned, for
            example if you request 100 objects, to query the next page you would
            specify offset = 100.
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/hedges/query'

        data = self._request(method='POST',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def get_hedge_time_series_results(self, return_df=False, **kwargs):
        '''
        Returns time series data for hedge

        Definition: GET /v1/hedges/results
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/hedge-service/get-hedge-time-series-results

        Parameters
        ----------
        id : array of string, (optional)
            Filter by a unique hedge Id.
        startDate : array of date, (optional)
            Start date for performance hedge data, defaults to start of time.
        endDate : array of date, (optional)
            End date for performance hedge data, defaults to today.
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/hedges/results'

        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def get_hedge(self, id, return_df=False, **kwargs):
        '''
        Retrieve a saved hedge based on its unique identifier

        Definition: GET /v1/hedges/{id}
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/hedge-service/get-a-hedge

        Parameters
        ----------
        id : string
            Marquee unique identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/hedges/{id}'

        request_url = request_url.format(id=id)
        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def update_hedge(self, id, return_df=False, **kwargs):
        '''
        Update an existing hedge in Marquee.

        Definition: PUT /v1/hedges/{id}
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/hedge-service/update-a-hedge

        Parameters
        ----------
        id : string
            Marquee unique identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        ownerId : string, (optional)
            Marquee unique identifier for user who owns the object.
        entitlements : Entitlements, (optional)
            Defines the entitlements of a given resource
        tags : array of string, (optional)
            Metadata associated with the object. Provide an array of strings which
            will be indexed for search and locating related objects
        name : string
            Display name of the hedge
        description : string, (optional)
            Free text description of a Hedge
        objective : string, (optional)
            The objective of the hedge.One of: Minimize Factor RiskReplicate
            Performance
        parameters : any of the following: Factor Hedge Parameters, Performance Hedge Parameters
            The parameters used in the hedge calculation.
        result : any of the following: Factor Hedge Result, Performance Hedge Result, (optional)
            Result of the hedge.
        '''

        request_url = 'https://api.marquee.gs.com/v1/hedges/{id}'

        request_url = request_url.format(id=id)
        data = self._request(method='PUT',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def delete_hedge(self, id, return_df=False, **kwargs):
        '''
        Remove a hedge from Marquee by identifier.

        Definition: DELETE /v1/hedges/{id}
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/hedge-service/delete-a-hedge

        Parameters
        ----------
        id : string
            Marquee unique identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/hedges/{id}'

        request_url = request_url.format(id=id)
        data = self._request(method='DELETE',
                             url=request_url,
                             return_df=return_df)
        return data

    def create_index(self, return_df=False, **kwargs):
        '''
        Creates the asset, puts the positions, creates a report, and schedules
        the report if given positionedAsset object.

        Definition: POST /v1/indices
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/indices-service/create-index

        Parameters
        ----------
        ticker : string
            Ticker Identifier of the new asset (Prefix with 'GS' to publish to
            Bloomberg)
        name : string
            Display name of the index
        description : string, (optional)
            Free text description of asset. Description provided will be indexed
            in the search service for free text relevance match
        styles : array of string, (optional)
            Styles or themes associated with the asset (max 50), default to
            Bespoke
        relatedContent : GIRDomain, (optional)
            Links to content related to this index or any of its constituents
        hedgeId : string, (optional)
            Marquee unique identifier
        returnType : string, (optional)
            Determines the index calculation methodology with respect to dividend
            reinvestmente, default to Price ReturnOne of: Price ReturnGross Return
        positionSet : array of PositionPriceInput
            Information of constituents associated with the index.
        publishParameters : Publish Parameters, (optional)
            Asset publishing parameters to determine where and how to publish
            asset, default all to false
        pricingParameters : IndicesPriceParameters
            Parameters for pricing indices
        entitlements : Entitlements, (optional)
            Defines the entitlements of a given resource
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/indices'

        data = self._request(method='POST',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def rebalance_index(self, id, return_df=False, **kwargs):
        '''
        Rebalance an existing index with new weights.

        Definition: POST /v1/indices/{id}/rebalance
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/indices-service/rebalance-index

        Parameters
        ----------
        id : string, (optional)
            Unique identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        parameters : any of the following: ISelectRebalance, CustomBasketsRebalanceInputs
            The inputs used to rebalance an index.
        '''

        request_url = 'https://api.marquee.gs.com/v1/indices/{id}/rebalance'

        request_url = request_url.format(id=id)
        data = self._request(method='POST',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def create_report(self, return_df=False, **kwargs):
        '''
        Create a new report in Marquee.

        Definition: POST /v1/reports
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/report-service/create-a-report

        Parameters
        ----------
        entitlements : Entitlements, (optional)
            Defines the entitlements of a given resource
        measures : array of string, (optional)
            Enums for measures to be outputted for the reportOne of: pnllongExposu
            reshortExposureassetCountturnoverassetCountLongassetCountShortnetExpos
            uregrossExposureshow more
        name : string, (optional)
            Report name
        ownerId : string, (optional)
            Marquee unique identifier for user who owns the object.
        parameters : Report Parameters
            Parameters specific to the report type
        positionSourceId : string
            Marquee unique identifier
        positionSourceType : string
            Source object for position dataOne of:
            PortfolioAssetBacktestRiskRequest
        type : string
            Type of report to executeOne of: Portfolio Performance
            AnalyticsPortfolio Factor RiskPortfolio AgingAsset Factor RiskBasket
            CreateScenarioIselect BacktestBacktest RunAnalyticsRisk Calculation
        status : string, (optional)
            Status of report runOne of:
            newreadyexecutingcalculatingdoneerrorcancelledwaiting
        latestExecutionTime : date-time, (optional)
            ISO 8601-formatted timestamp
        latestEndDate : date, (optional)
            ISO 8601-formatted date
        percentageComplete : number, (optional)
            Percentage that the report has been completed so far
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/reports'

        data = self._request(method='POST',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def get_many_reports(self, return_df=False, **kwargs):
        '''
        Retrieve multiple reports by ids or enumerate using a pagination
        object.

        Definition: GET /v1/reports
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/report-service/get-many-reports

        Parameters
        ----------
        id : array of string, (optional)
            Filter by id
        limit : array of string, (optional)
            Limit on the number of objects to be returned in the response. Can
            range between 1 and 500
        offset : array of string, (optional)
            The offset of the first result returned (default 0).
        orderBy : array containing any of the following: string,, (optional)
            Field name by which to order results
        scroll : array of string, (optional)
            Time for which to keep the scroll search context alive, i.e. 1m (1
            minute) or 10s (10 seconds).
        scrollId : array of string, (optional)
            Scroll identifier to be used to retrieve the next batch of results
        createdById : array of string, (optional)
            Filter by id of user who created the object
        positionSourceId : array of string, (optional)
            Filter by id
        status : array of string, (optional)
            Status of report runOne of:
            newreadyexecutingcalculatingdoneerrorcancelledwaiting
        reportType : array of string, (optional)
            Type of report to executeOne of: Portfolio Performance
            AnalyticsPortfolio Factor RiskPortfolio AgingAsset Factor RiskBasket
            CreateScenarioIselect BacktestBacktest RunAnalyticsRisk Calculation
        positionSourceType : array of string, (optional)
            Source object for position dataOne of:
            PortfolioAssetBacktestRiskRequest
        ownerId : array of string, (optional)
            Filter by owner ID
        name : array of string, (optional)
            Filter by name (exact match).
        lastUpdatedById : array of string, (optional)
            Filter by last updated user id
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/reports'

        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def get_events(self, return_df=False, **kwargs):
        '''
        Retrieve events for reports

        Definition: GET /v1/reports/events
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/report-service/get-events

        Parameters
        ----------
        limit : array of string, (optional)
            Limit on the number of objects to be returned in the response. Can
            range between 1 and 500
        offset : array of string, (optional)
            The offset of the first result returned (default 0).
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/reports/events'

        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def post_events_for_reports(self, return_df=False, **kwargs):
        '''
        Post events for reports

        Definition: POST /v1/reports/events
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/report-service/post-events-for-reports

        Parameters
        ----------
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/reports/events'

        data = self._request(method='POST',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def get_events_for_date(self, date, return_df=False, **kwargs):
        '''
        Retrieve events for reports for a given date

        Definition: GET /v1/reports/events/{date}
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/report-service/get-events-for-date

        Parameters
        ----------
        date : date, (optional)
            ISO 8601-formatted date
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/reports/events/{date}'

        request_url = request_url.format(date=date)
        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def get_report_job(self, id, return_df=False, **kwargs):
        '''
        Retrieve a report job

        Definition: GET /v1/reports/jobs/{id}
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/report-service/get-report-job

        Parameters
        ----------
        id : string, (read-only)
            Report job unique identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        limit : array of string, (optional)
            Limit on the number of objects to be returned in the response.
        offset : array of string, (optional)
            The offset of the first result returned (default 0).
        '''

        request_url = 'https://api.marquee.gs.com/v1/reports/jobs/{id}'

        request_url = request_url.format(id=id)
        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def cancel_report_job(self, jobId, return_df=False, **kwargs):
        '''
        Cancel report job

        Definition: POST /v1/reports/jobs/{jobId}/cancel
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/report-service/cancel-report-job

        Parameters
        ----------
        jobId : string, (optional)
            Report job unique identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/reports/jobs/{jobId}/cancel'

        request_url = request_url.format(jobId=jobId)
        data = self._request(method='POST',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def reschedule_report_job(self, jobId, return_df=False, **kwargs):
        '''
        Create new report job for same parent job Id

        Definition: POST /v1/reports/jobs/{jobId}/reschedule
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/report-service/reschedule-report-job

        Parameters
        ----------
        jobId : string, (optional)
            Report job unique identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/reports/jobs/{jobId}/reschedule'

        request_url = request_url.format(jobId=jobId)
        data = self._request(method='POST',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def update_report_job_status(self, jobId, return_df=False, **kwargs):
        '''
        Update report job status

        Definition: POST /v1/reports/jobs/{jobId}/update
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/report-service/update-report-job-status

        Parameters
        ----------
        jobId : string, (optional)
            Report job unique identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        startDate : date, (optional)
            ISO 8601-formatted date
        endDate : date, (optional)
            ISO 8601-formatted date
        elapsedTime : number, (optional)
            Time taken to execute report (in milliseconds)
        percentageComplete : number, (optional)
            Percentage that the job has been completed so far
        executionTime : date-time, (optional)
            ISO 8601-formatted timestamp
        measures : array of string, (optional)
            Enums for measures to be outputted for the reportOne of: pnllongExposu
            reshortExposureassetCountturnoverassetCountLongassetCountShortnetExpos
            uregrossExposureshow more
        parameters : Report Parameters, (optional)
            Parameters specific to the report type
        parentId : string, (optional)
            Marquee unique identifier
        positionSourceId : string, (optional)
            Marquee unique identifier
        positionSourceType : string, (optional)
            Source object for position dataOne of:
            PortfolioAssetBacktestRiskRequest
        reportId : string, (optional)
            Marquee unique identifier
        reportType : string, (optional)
            Type of report to executeOne of: Portfolio Performance
            AnalyticsPortfolio Factor RiskPortfolio AgingAsset Factor RiskBasket
            CreateScenarioIselect BacktestBacktest RunAnalyticsRisk Calculation
        status : string, (optional)
            Status of report runOne of:
            newreadyexecutingcalculatingdoneerrorcancelledwaiting
        ownerId : string, (optional)
            Marquee unique identifier for user who owns the object.
        '''

        request_url = 'https://api.marquee.gs.com/v1/reports/jobs/{jobId}/update'

        request_url = request_url.format(jobId=jobId)
        data = self._request(method='POST',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def get_reports_status(self, return_df=False, **kwargs):
        '''
        Retrieve status for reports.

        Definition: GET /v1/reports/status
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/report-service/get-reports-status

        Parameters
        ----------
        startDate : array of date, (optional)
            Start date for reports status
        endDate : array of date, (optional)
            End date for reports status
        id : array of string, (optional)
            Ids for reports status
        limit : array of string, (optional)
            Limit on the number of objects to be returned in the response.
        offset : array of string, (optional)
            The offset of the first result returned (default 0).
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/reports/status'

        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def get_report(self, id, return_df=False, **kwargs):
        '''
        Retrieve report by id.

        Definition: GET /v1/reports/{id}
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/report-service/get-report

        Parameters
        ----------
        id : string, (read-only)
            Report unique identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/reports/{id}'

        request_url = request_url.format(id=id)
        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def update_report(self, id, return_df=False, **kwargs):
        '''
        Update report object given id.

        Definition: PUT /v1/reports/{id}
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/report-service/update-report

        Parameters
        ----------
        id : string, (read-only)
            Report unique identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        entitlements : Entitlements, (optional)
            Defines the entitlements of a given resource
        measures : array of string, (optional)
            Enums for measures to be outputted for the reportOne of: pnllongExposu
            reshortExposureassetCountturnoverassetCountLongassetCountShortnetExpos
            uregrossExposureshow more
        name : string, (optional)
            Report name
        ownerId : string, (optional)
            Marquee unique identifier for user who owns the object.
        parameters : Report Parameters
            Parameters specific to the report type
        positionSourceId : string
            Marquee unique identifier
        positionSourceType : string
            Source object for position dataOne of:
            PortfolioAssetBacktestRiskRequest
        type : string
            Type of report to executeOne of: Portfolio Performance
            AnalyticsPortfolio Factor RiskPortfolio AgingAsset Factor RiskBasket
            CreateScenarioIselect BacktestBacktest RunAnalyticsRisk Calculation
        status : string, (optional)
            Status of report runOne of:
            newreadyexecutingcalculatingdoneerrorcancelledwaiting
        latestExecutionTime : date-time, (optional)
            ISO 8601-formatted timestamp
        latestEndDate : date, (optional)
            ISO 8601-formatted date
        percentageComplete : number, (optional)
            Percentage that the report has been completed so far
        '''

        request_url = 'https://api.marquee.gs.com/v1/reports/{id}'

        request_url = request_url.format(id=id)
        data = self._request(method='PUT',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def delete_report(self, id, return_df=False, **kwargs):
        '''
        Remove a report from Marquee by identifier. User must have edit
        entitlement on the asset in order to delete.

        Definition: DELETE /v1/reports/{id}
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/report-service/delete-report

        Parameters
        ----------
        id : string, (read-only)
            Report unique identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/reports/{id}'

        request_url = request_url.format(id=id)
        data = self._request(method='DELETE',
                             url=request_url,
                             return_df=return_df)
        return data

    def get_report_jobs(self, id, return_df=False, **kwargs):
        '''
        Retrieve jobs for reports

        Definition: GET /v1/reports/{id}/jobs
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/report-service/get-report-jobs

        Parameters
        ----------
        id : string, (read-only)
            Report unique identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        limit : array of string, (optional)
            Limit on the number of objects to be returned in the response.
        offset : array of string, (optional)
            The offset of the first result returned (default 0).
        '''

        request_url = 'https://api.marquee.gs.com/v1/reports/{id}/jobs'

        request_url = request_url.format(id=id)
        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def get_status_for_report_jobs(self, id, return_df=False, **kwargs):
        '''
        Get status for jobs of a report

        Definition: GET /v1/reports/{id}/status
        Required scopes: None
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/report-service/get-status-for-report-jobs

        Parameters
        ----------
        id : string, (read-only)
            Report unique identifier
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        limit : array of string, (optional)
            Limit on the number of objects to be returned in the response.
        offset : array of string, (optional)
            The offset of the first result returned (default 0).
        '''

        request_url = 'https://api.marquee.gs.com/v1/reports/{id}/status'

        request_url = request_url.format(id=id)
        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def search_assets(self, return_df=False, **kwargs):
        '''
        Search for assets using a query string.

        Definition: GET /v1/search/assets
        Required scopes: read_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/search-service/search-assets

        Parameters
        ----------
        q : array of string, (optional)
            A simple query string
        qs : array of string, (optional)
            An advanced query string (supports field names, boost, AND/OR)
        limit : array of string, (optional)
            Maximum number of results to be returned in the result set.
        offset : array of string, (optional)
            Offset of first result to return from the server
        asOfTime : array of date-time, (optional)
            For querying with a specified as of time.
        fields : array of string, (optional)
            Fields to be returned.
        counts : array of, (optional)
            Fields for which to return term counts
        createdById : array of string, (optional)
            Filter by id of user who created the object
        vehicleType : array of string, (optional)
            Type of investment vehicle. Only viewable after having been granted
            additional access to asset information.One of: Comingled HFCo-
            InvestmentUCITS'40 ActOther
        tags : array of string, (optional)
            Filter by contents of tags, matches on words
        regionalFocus : array of string, (optional)
            Section of the world a fund is focused on from an investment
            perspective. Same view permissions as the asset.One of: GlobalAsia ex-
            JapanChinaEmerging EuropeEuropeGlobal Emerging MarketsJapanLatin
            AmericaMiddle East / North AfricaNorth Americashow more
        optionType : array of string, (optional)
            One of: payerreceiver
        sectors : array of string, (optional)
            Filter by sector
        wpk : array of string, (optional)
            Filter by WPK (subject to licensing).
        exchange : array of string, (optional)
            Filter by GS exchange code
        ticker : array of string, (optional)
            Filter by Ticker.
        assetClass : array of string, (optional)
            Asset classification of security. Assets are classified into broad
            groups which exhibit similar characteristics and behave in a
            consistent way under different market conditionsOne of:
            CashCommodCreditCross AssetEquityFundFXMortgageRates
        ric : array of string, (optional)
            Filter by RIC (subject to licensing).
        id : array of string, (optional)
            Filter by id
        indexCreateSource : array of string, (optional)
            Source of basket create.One of: APICUBEHedgerMarquee UI
        bcid : array of string, (optional)
            Filter by Bloomberg Composite ID.
        bbid : array of string, (optional)
            Filter by Bloomberg ID.
        performanceFee : array containing, (optional)

        underlyingAssetIds : array of string, (optional)
            Filter by Marquee IDs of the underlying assets.
        bbidEquivalent : array of string, (optional)
            Filter by Bloomberg equivalent ID.
        valoren : array of string, (optional)
            Filter by Valoren (subject to licensing).
        portfolioManagers : array of string, (optional)
            Filter by id
        supraStrategy : array of string, (optional)
            Broad descriptor of a fund's investment approach. Same view
            permissions as the assetOne of: CompositeCreditEquityEquity HedgeEvent
            DrivenFund of FundsMacroMulti-StrategyOtherQuantshow more
        lmsId : array of string, (optional)

        strategy : array of string, (optional)
            More specific descriptor of a fund's investment approach. Same view
            permissions as the asset.One of: Active TradingActivistCo-Invest /
            SPVCommodityCommoditiesCompositeConservativeConvert ArbConvertible
            ArbitrageCredit Arbitrageshow more
        ownerId : array of string, (optional)
            Filter by owner ID
        assetClassificationsIsPrimary : array of string, (optional)
            Whether or not it is the primary exchange asset.One of: truefalse
        styles : array of array, (optional)
            Filter by asset style
        shortName : array of string, (optional)
            Filter by short name (exact match).
        mic : array of string, (optional)

        currency : array of string, (optional)
            Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP
            vs GBp)One of: ACUADPAEDAFAALLAMDANGAOAAOKshow more
        assetParametersExchangeCurrency : array of string, (optional)
            Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP
            vs GBp)One of: ACUADPAEDAFAALLAMDANGAOAAOKshow more
        managementFee : array containing, (optional)

        cusip : array of string, (optional)
            Filter by CUSIP (subject to licensing).
        name : array of string, (optional)
            Filter by name (exact match).
        aum : array containing, (optional)

        region : array of string, (optional)
            Regional classification for the assetOne of:
            AmericasAsiaEMEuropeGlobal
        liveDate : array containing, (optional)

        primeId : array of string, (optional)
            Filter by primeId.
        description : array of string, (optional)
            Filter by asset description.
        lastUpdatedById : array of string, (optional)
            Filter by last updated user id
        type : array of string, (optional)
            Asset type differentiates the product categorization or contract
            typeOne of: AccessBasisBasisSwapBenchmarkBenchmark RateBondCalendar
            SpreadCapCashCertificateshow more
        sedol : array of string, (optional)
            Filter by SEDOL (subject to licensing).
        marketCapCategory : array of string, (optional)
            Category of market capitalizations a fund is focused on from an
            investment perspective. Same view permissions as the asset.One of:
            AllLargeMidSmall
        strikePrice : array of string, (optional)

        listed : array of string, (optional)
            Whether the asset is listed or not.One of: truefalse
        g10Currency : array of string, (optional)
            Is a G10 asset.One of: truefalse
        isin : array of string, (optional)
            Filter by ISIN (subject to licensing).
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/search/assets'

        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def search_assets_data(self, return_df=False, **kwargs):
        '''
        Execute a search of assets and return the results as a data set. The
        caller can specify which fields are returned.

        Definition: GET /v1/search/assets/data
        Required scopes: read_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/search-service/search-assets-data

        Parameters
        ----------
        q : array of string, (optional)
            A simple query string
        qs : array of string, (optional)
            An advanced query string (supports field names, boost, AND/OR)
        limit : array of string, (optional)
            Maximum number of results to be returned in the result set.
        offset : array of string, (optional)
            Offset of first result to return from the server
        fields : array of string, (optional)
            Fields to be returned.
        counts : array of, (optional)
            Fields for which to return term counts
        createdById : array of string, (optional)
            Filter by id of user who created the object
        vehicleType : array of string, (optional)
            Type of investment vehicle. Only viewable after having been granted
            additional access to asset information.One of: Comingled HFCo-
            InvestmentUCITS'40 ActOther
        tags : array of string, (optional)
            Filter by contents of tags, matches on words
        regionalFocus : array of string, (optional)
            Section of the world a fund is focused on from an investment
            perspective. Same view permissions as the asset.One of: GlobalAsia ex-
            JapanChinaEmerging EuropeEuropeGlobal Emerging MarketsJapanLatin
            AmericaMiddle East / North AfricaNorth Americashow more
        optionType : array of string, (optional)
            One of: payerreceiver
        sectors : array of string, (optional)
            Filter by sector
        wpk : array of string, (optional)
            Filter by WPK (subject to licensing).
        exchange : array of string, (optional)
            Filter by GS exchange code
        ticker : array of string, (optional)
            Filter by Ticker.
        assetClass : array of string, (optional)
            Asset classification of security. Assets are classified into broad
            groups which exhibit similar characteristics and behave in a
            consistent way under different market conditionsOne of:
            CashCommodCreditCross AssetEquityFundFXMortgageRates
        ric : array of string, (optional)
            Filter by RIC (subject to licensing).
        id : array of string, (optional)
            Filter by id
        indexCreateSource : array of string, (optional)
            Source of basket create.One of: APICUBEHedgerMarquee UI
        bcid : array of string, (optional)
            Filter by Bloomberg Composite ID.
        bbid : array of string, (optional)
            Filter by Bloomberg ID.
        performanceFee : array containing, (optional)

        underlyingAssetIds : array of string, (optional)
            Filter by Marquee IDs of the underlying assets.
        bbidEquivalent : array of string, (optional)
            Filter by Bloomberg equivalent ID.
        valoren : array of string, (optional)
            Filter by Valoren (subject to licensing).
        portfolioManagers : array of string, (optional)
            Filter by id
        supraStrategy : array of string, (optional)
            Broad descriptor of a fund's investment approach. Same view
            permissions as the assetOne of: CompositeCreditEquityEquity HedgeEvent
            DrivenFund of FundsMacroMulti-StrategyOtherQuantshow more
        lmsId : array of string, (optional)

        strategy : array of string, (optional)
            More specific descriptor of a fund's investment approach. Same view
            permissions as the asset.One of: Active TradingActivistCo-Invest /
            SPVCommodityCommoditiesCompositeConservativeConvert ArbConvertible
            ArbitrageCredit Arbitrageshow more
        ownerId : array of string, (optional)
            Filter by owner ID
        assetClassificationsIsPrimary : array of string, (optional)
            Whether or not it is the primary exchange asset.One of: truefalse
        styles : array of array, (optional)
            Filter by asset style
        shortName : array of string, (optional)
            Filter by short name (exact match).
        mic : array of string, (optional)

        currency : array of string, (optional)
            Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP
            vs GBp)One of: ACUADPAEDAFAALLAMDANGAOAAOKshow more
        assetParametersExchangeCurrency : array of string, (optional)
            Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP
            vs GBp)One of: ACUADPAEDAFAALLAMDANGAOAAOKshow more
        managementFee : array containing, (optional)

        cusip : array of string, (optional)
            Filter by CUSIP (subject to licensing).
        name : array of string, (optional)
            Filter by name (exact match).
        aum : array containing, (optional)

        region : array of string, (optional)
            Regional classification for the assetOne of:
            AmericasAsiaEMEuropeGlobal
        liveDate : array containing, (optional)

        primeId : array of string, (optional)
            Filter by primeId.
        description : array of string, (optional)
            Filter by asset description.
        lastUpdatedById : array of string, (optional)
            Filter by last updated user id
        type : array of string, (optional)
            Asset type differentiates the product categorization or contract
            typeOne of: AccessBasisBasisSwapBenchmarkBenchmark RateBondCalendar
            SpreadCapCashCertificateshow more
        sedol : array of string, (optional)
            Filter by SEDOL (subject to licensing).
        marketCapCategory : array of string, (optional)
            Category of market capitalizations a fund is focused on from an
            investment perspective. Same view permissions as the asset.One of:
            AllLargeMidSmall
        strikePrice : array of string, (optional)

        listed : array of string, (optional)
            Whether the asset is listed or not.One of: truefalse
        g10Currency : array of string, (optional)
            Is a G10 asset.One of: truefalse
        isin : array of string, (optional)
            Filter by ISIN (subject to licensing).
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/search/assets/data'

        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def search_assets_data_query(self, return_df=False, **kwargs):
        '''
        Execute a search of assets and return the results as a data set. The
        caller can specify which fields are returned. Same as the
        /search/data/assets endpoint, but through a POST allowing larger
        structured queries.

        Definition: POST /v1/search/assets/data/query
        Required scopes: read_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/search-service/search-assets-data-query

        Parameters
        ----------
        q : string, (optional)
            A simple query string
        qs : string, (optional)
            An advanced query string (supports field names, boost, AND/OR)
        asOfTime : date-time, (optional)
            ISO 8601-formatted timestamp
        where : FieldFilterMap, (optional)
            Filters on fields that match any of the provided terms
        fields : array containing any of the following: string,, (optional)
            Fields to be returned.
        limit : integer, (optional)
            Limit on the number of objects to be returned in the response. Can
            range between 1 and 1000
        offset : integer, (optional)
            The offset of the first result returned (default 0). Can be used in
            pagination to defined the first item in the list to be returned, for
            example if you request 100 objects, to query the next page you would
            specify offset = 100.
        counts : array of, (optional)
            Fields for which to return term counts
        orderBy : array containing any of the following: string,, (optional)

        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/search/assets/data/query'

        data = self._request(method='POST',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def search_assets_query(self, return_df=False, **kwargs):
        '''
        Search for assets using a query string.

        Definition: POST /v1/search/assets/query
        Required scopes: read_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/search-service/search-assets-query

        Parameters
        ----------
        q : string, (optional)
            A simple query string
        qs : string, (optional)
            An advanced query string (supports field names, boost, AND/OR)
        asOfTime : date-time, (optional)
            ISO 8601-formatted timestamp
        where : FieldFilterMap, (optional)
            Filters on fields that match any of the provided terms
        fields : array containing any of the following: string,, (optional)
            Fields to be returned.
        limit : integer, (optional)
            Limit on the number of objects to be returned in the response. Can
            range between 1 and 1000
        offset : integer, (optional)
            The offset of the first result returned (default 0). Can be used in
            pagination to defined the first item in the list to be returned, for
            example if you request 100 objects, to query the next page you would
            specify offset = 100.
        counts : array of, (optional)
            Fields for which to return term counts
        orderBy : array containing any of the following: string,, (optional)

        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/search/assets/query'

        data = self._request(method='POST',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def search_backtests(self, return_df=False, **kwargs):
        '''
        Search for backtests using a query string.

        Definition: GET /v1/search/backtests
        Required scopes: read_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/search-service/search-backtests

        Parameters
        ----------
        q : array of string, (optional)
            A simple query string
        qs : array of string, (optional)
            An advanced query string (supports field names, boost, AND/OR)
        limit : array of string, (optional)
            Maximum number of results to be returned in the result set.
        offset : array of string, (optional)
            Offset of first result to return from the server
        asOfTime : array of date-time, (optional)
            For querying with a specified as of time.
        fields : array of string, (optional)
            Fields to be returned.
        counts : array of, (optional)
            Fields for which to return term counts
        createdById : array of string, (optional)
            Filter by id of user who created the object
        vehicleType : array of string, (optional)
            Type of investment vehicle. Only viewable after having been granted
            additional access to asset information.One of: Comingled HFCo-
            InvestmentUCITS'40 ActOther
        tags : array of string, (optional)
            Filter by contents of tags, matches on words
        regionalFocus : array of string, (optional)
            Section of the world a fund is focused on from an investment
            perspective. Same view permissions as the asset.One of: GlobalAsia ex-
            JapanChinaEmerging EuropeEuropeGlobal Emerging MarketsJapanLatin
            AmericaMiddle East / North AfricaNorth Americashow more
        optionType : array of string, (optional)
            One of: payerreceiver
        sectors : array of string, (optional)
            Filter by sector
        wpk : array of string, (optional)
            Filter by WPK (subject to licensing).
        exchange : array of string, (optional)
            Filter by GS exchange code
        ticker : array of string, (optional)
            Filter by Ticker.
        assetClass : array of string, (optional)
            Asset classification of security. Assets are classified into broad
            groups which exhibit similar characteristics and behave in a
            consistent way under different market conditionsOne of:
            CashCommodCreditCross AssetEquityFundFXMortgageRates
        ric : array of string, (optional)
            Filter by RIC (subject to licensing).
        id : array of string, (optional)
            Filter by id
        indexCreateSource : array of string, (optional)
            Source of basket create.One of: APICUBEHedgerMarquee UI
        bcid : array of string, (optional)
            Filter by Bloomberg Composite ID.
        bbid : array of string, (optional)
            Filter by Bloomberg ID.
        performanceFee : array containing, (optional)

        underlyingAssetIds : array of string, (optional)
            Filter by Marquee IDs of the underlying assets.
        bbidEquivalent : array of string, (optional)
            Filter by Bloomberg equivalent ID.
        valoren : array of string, (optional)
            Filter by Valoren (subject to licensing).
        portfolioManagers : array of string, (optional)
            Filter by id
        supraStrategy : array of string, (optional)
            Broad descriptor of a fund's investment approach. Same view
            permissions as the assetOne of: CompositeCreditEquityEquity HedgeEvent
            DrivenFund of FundsMacroMulti-StrategyOtherQuantshow more
        lmsId : array of string, (optional)

        strategy : array of string, (optional)
            More specific descriptor of a fund's investment approach. Same view
            permissions as the asset.One of: Active TradingActivistCo-Invest /
            SPVCommodityCommoditiesCompositeConservativeConvert ArbConvertible
            ArbitrageCredit Arbitrageshow more
        ownerId : array of string, (optional)
            Filter by owner ID
        assetClassificationsIsPrimary : array of string, (optional)
            Whether or not it is the primary exchange asset.One of: truefalse
        styles : array of array, (optional)
            Filter by asset style
        shortName : array of string, (optional)
            Filter by short name (exact match).
        mic : array of string, (optional)

        currency : array of string, (optional)
            Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP
            vs GBp)One of: ACUADPAEDAFAALLAMDANGAOAAOKshow more
        assetParametersExchangeCurrency : array of string, (optional)
            Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP
            vs GBp)One of: ACUADPAEDAFAALLAMDANGAOAAOKshow more
        managementFee : array containing, (optional)

        cusip : array of string, (optional)
            Filter by CUSIP (subject to licensing).
        name : array of string, (optional)
            Filter by name (exact match).
        aum : array containing, (optional)

        region : array of string, (optional)
            Regional classification for the assetOne of:
            AmericasAsiaEMEuropeGlobal
        liveDate : array containing, (optional)

        primeId : array of string, (optional)
            Filter by primeId.
        description : array of string, (optional)
            Filter by asset description.
        lastUpdatedById : array of string, (optional)
            Filter by last updated user id
        type : array of string, (optional)
            Asset type differentiates the product categorization or contract
            typeOne of: AccessBasisBasisSwapBenchmarkBenchmark RateBondCalendar
            SpreadCapCashCertificateshow more
        sedol : array of string, (optional)
            Filter by SEDOL (subject to licensing).
        marketCapCategory : array of string, (optional)
            Category of market capitalizations a fund is focused on from an
            investment perspective. Same view permissions as the asset.One of:
            AllLargeMidSmall
        strikePrice : array of string, (optional)

        listed : array of string, (optional)
            Whether the asset is listed or not.One of: truefalse
        g10Currency : array of string, (optional)
            Is a G10 asset.One of: truefalse
        isin : array of string, (optional)
            Filter by ISIN (subject to licensing).
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/search/backtests'

        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def search_datasets(self, return_df=False, **kwargs):
        '''
        Search for datasets using a query string.

        Definition: GET /v1/search/datasets
        Required scopes: read_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/search-service/search-datasets

        Parameters
        ----------
        q : array of string, (optional)
            A simple query string
        qs : array of string, (optional)
            An advanced query string (supports field names, boost, AND/OR)
        limit : array of string, (optional)
            Maximum number of results to be returned in the result set.
        offset : array of string, (optional)
            Offset of first result to return from the server
        asOfTime : array of date-time, (optional)
            For querying with a specified as of time.
        fields : array of string, (optional)
            Fields to be returned.
        counts : array of, (optional)
            Fields for which to return term counts
        dataSetCategory : array of string, (optional)
            Filter by data set category.
        createdById : array of string, (optional)
            Filter by id of user who created the object
        tags : array of string, (optional)
            Filter by contents of tags, matches on words
        dataProduct : array of string, (optional)
            Filter by data product.
        underlyingDataSetId : array of string, (optional)
            Filter by underlying data set Id.
        assetClass : array of string, (optional)
            Asset classification of security. Assets are classified into broad
            groups which exhibit similar characteristics and behave in a
            consistent way under different market conditionsOne of:
            CashCommodCreditCross AssetEquityFundFXMortgageRates
        id : array of string, (optional)
            Filter by id
        shortDescription : array of string, (optional)
            Filter by short description
        ownerId : array of string, (optional)
            Filter by owner ID
        vendor : array of string, (optional)
            Vendor of dataset.One of: Goldman SachsThomson
            ReutersSolactiveBloombergAxiomaGoldman Sachs Prime ServicesGoldman
            Sachs Global Investment ResearchNational Weather ServiceWMHedge Fund
            Research, Inc.show more
        nonSymbolDimensions : array of string, (optional)
            Filter by non-symbol dimensions.
        frequency : array of string, (optional)
            Filter by frequency
        dataSetSubCategory : array of string, (optional)
            Filter by data set sub-category.
        name : array of string, (optional)
            Filter by name (exact match).
        description : array of string, (optional)
            Filter by asset description.
        lastUpdatedById : array of string, (optional)
            Filter by last updated user id
        coverage : array of string, (optional)
            Filter by coverage.
        measures : array of string, (optional)
            Filter by measure.
        symbolDimensions : array of string, (optional)
            Filter by symbol dimension.
        methodology : array of string, (optional)
            Filter by methodology.
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/search/datasets'

        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def search_kpis(self, return_df=False, **kwargs):
        '''
        Search for kpis using a query string.

        Definition: GET /v1/search/kpis
        Required scopes: read_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/search-service/search-kpis

        Parameters
        ----------
        q : array of string, (optional)
            A simple query string
        qs : array of string, (optional)
            An advanced query string (supports field names, boost, AND/OR)
        limit : array of string, (optional)
            Maximum number of results to be returned in the result set.
        offset : array of string, (optional)
            Offset of first result to return from the server
        asOfTime : array of date-time, (optional)
            For querying with a specified as of time.
        fields : array of string, (optional)
            Fields to be returned.
        counts : array of, (optional)
            Fields for which to return term counts
        createdById : array of string, (optional)
            Filter by id of user who created the object
        tags : array of string, (optional)
            Filter by contents of tags, matches on words
        id : array of string, (optional)
            Filter by id
        ownerId : array of string, (optional)
            Filter by owner ID
        name : array of string, (optional)
            Filter by name (exact match).
        description : array of string, (optional)
            Filter by asset description.
        lastUpdatedById : array of string, (optional)
            Filter by last updated user id
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/search/kpis'

        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def search_portfolios(self, return_df=False, **kwargs):
        '''
        Search for portfolios using a query string.

        Definition: GET /v1/search/portfolios
        Required scopes: read_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/search-service/search-portfolios

        Parameters
        ----------
        q : array of string, (optional)
            A simple query string
        qs : array of string, (optional)
            An advanced query string (supports field names, boost, AND/OR)
        limit : array of string, (optional)
            Maximum number of results to be returned in the result set.
        offset : array of string, (optional)
            Offset of first result to return from the server
        asOfTime : array of date-time, (optional)
            For querying with a specified as of time.
        fields : array of string, (optional)
            Fields to be returned.
        counts : array of, (optional)
            Fields for which to return term counts
        createdById : array of string, (optional)
            Filter by id of user who created the object
        tags : array of string, (optional)
            Filter by contents of tags, matches on words
        id : array of string, (optional)
            Filter by id
        ownerId : array of string, (optional)
            Filter by owner ID
        shortName : array of string, (optional)
            Filter by short name (exact match).
        currency : array of string, (optional)
            Currency, ISO 4217 currency code or exchange quote modifier (e.g. GBP
            vs GBp)One of: ACUADPAEDAFAALLAMDANGAOAAOKshow more
        name : array of string, (optional)
            Filter by name (exact match).
        description : array of string, (optional)
            Filter by asset description.
        lastUpdatedById : array of string, (optional)
            Filter by last updated user id
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/search/portfolios'

        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def search_portfolios_query(self, return_df=False, **kwargs):
        '''
        Search for portfolios using a query string.

        Definition: POST /v1/search/portfolios/query
        Required scopes: read_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/search-service/search-portfolios-query

        Parameters
        ----------
        q : string, (optional)
            A simple query string
        qs : string, (optional)
            An advanced query string (supports field names, boost, AND/OR)
        asOfTime : date-time, (optional)
            ISO 8601-formatted timestamp
        where : FieldFilterMap, (optional)
            Filters on fields that match any of the provided terms
        fields : array containing Selector, (optional)
            Fields to be returned.
        limit : integer, (optional)
            Limit on the number of objects to be returned in the response. Can
            range between 1 and 1000
        offset : integer, (optional)
            The offset of the first result returned (default 0). Can be used in
            pagination to defined the first item in the list to be returned, for
            example if you request 100 objects, to query the next page you would
            specify offset = 100.
        counts : array of, (optional)
            Fields for which to return term counts
        orderBy : array containing OrderBy, (optional)

        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/search/portfolios/query'

        data = self._request(method='POST',
                             url=request_url,
                             return_df=return_df,
                             json=kwargs)
        return data

    def search_reports(self, return_df=False, **kwargs):
        '''
        Search for reports using a query string.

        Definition: GET /v1/search/reports
        Required scopes: read_product_data
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/search-service/search-reports

        Parameters
        ----------
        q : array of string, (optional)
            A simple query string
        qs : array of string, (optional)
            An advanced query string (supports field names, boost, AND/OR)
        limit : array of string, (optional)
            Maximum number of results to be returned in the result set.
        offset : array of string, (optional)
            Offset of first result to return from the server
        asOfTime : array of date-time, (optional)
            For querying with a specified as of time.
        fields : array of string, (optional)
            Fields to be returned.
        counts : array of, (optional)
            Fields for which to return term counts
        orderBy : array containing any of the following: string,, (optional)
            Field name by which to order results
        createdById : array of string, (optional)
            Filter by id of user who created the object
        positionSourceId : array of string, (optional)
            Filter by id
        id : array of string, (optional)
            Filter by id
        status : array of string, (optional)
            Status of report runOne of:
            newreadyexecutingcalculatingdoneerrorcancelledwaiting
        reportType : array of string, (optional)
            Type of report to executeOne of: Portfolio Performance
            AnalyticsPortfolio Factor RiskPortfolio AgingAsset Factor RiskBasket
            CreateScenarioIselect BacktestBacktest RunAnalyticsRisk Calculation
        positionSourceType : array of string, (optional)
            Source object for position dataOne of:
            PortfolioAssetBacktestRiskRequest
        ownerId : array of string, (optional)
            Filter by owner ID
        name : array of string, (optional)
            Filter by name (exact match).
        lastUpdatedById : array of string, (optional)
            Filter by last updated user id
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/search/reports'

        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def get_many_users(self, return_df=False, **kwargs):
        '''
        Retrieve multiple users by ids or enumerate using a pagination object.

        Definition: GET /v1/users
        Required scopes: read_user_profile
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/user-service/get-many-users

        Parameters
        ----------
        id : array of string, (optional)
            Filter by user id
        email : array of string, (optional)
            Filter by email id
        login : array of string, (optional)
            Filter by login
        city : array of string, (optional)
            Filter by city
        country : array of string, (optional)
            Filter by country
        company : array of string, (optional)
            Filter by company
        rootOEId : array of string, (optional)
            Filter by rootOE id
        oeId : array of string, (optional)
            Filter by OE id
        oeAlias : nan, (optional)
            Filter by OE alias
        name : array of string, (optional)
            Filter by name
        firstName : array of string, (optional)
            Filter by firstName
        lastName : array of string, (optional)
            Filter by lastName
        internalID : array of string, (optional)
            Filter by internalID
        region : array of string, (optional)
            Filter by region
        kerberos : array of string, (optional)
            Filter by user kerberos
        analyticsId : array of string, (optional)
            Filter by user analyticsId
        tokens : array of string, (optional)
            Filter by user tokens
        roles : array of string, (optional)
            Filter by user roles
        groups : array of string, (optional)
            Filter by user group
        coverageApp : array of string, (optional)
            Filter by user coverage app
        coverageName : array of string, (optional)
            Filter by user coverage name
        coverageEmail : array of string, (optional)
            Filter by user coverage email
        coveragePhone : array of string, (optional)
            Filter by user coverage phone
        coverageGuid : array of string, (optional)
            Filter by user coverage guid
        scrollId : array of string, (optional)
            Scroll identifier to be used to retrieve the next batch of results
        scrollTime : array of string, (optional)
            Time for which to keep the scroll search context alive, i.e. 1m (1
            minute) or 10s (10 seconds)
        limit : array of string, (optional)
            Limit on the number of objects to be returned in the response. Can
            range between 1 and 100
        offset : array of string, (optional)
            The offset of the first result returned (default 0). Can be used in
            pagination to defined the first item in the list to be returned, for
            example if you request 100 objects, to query the next page you would
            specify offset = 100.
        orderBy : array containing, (optional)
            Field name by which to order results
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/users'

        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def get_research_users(self, return_df=False, **kwargs):
        '''
        Retrieve research user details.

        Definition: GET /v1/users/research
        Required scopes: read_user_profile
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/user-service/get-research-users

        Parameters
        ----------
        scrollId : array of string, (optional)
            Scroll identifier to be used to retrieve the next batch of results
        scrollTime : array of string, (optional)
            Time for which to keep the scroll search context alive, i.e. 1m (1
            minute) or 10s (10 seconds)
        limit : array of string, (optional)
            Limit on the number of objects to be returned in the response. Can
            range between 1 and 100
        offset : array of string, (optional)
            The offset of the first result returned (default 0). Can be used in
            pagination to defined the first item in the list to be returned, for
            example if you request 100 objects, to query the next page you would
            specify offset = 100.
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/users/research'

        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data

    def get_my_user_profile(self, return_df=False, **kwargs):
        '''
        Retrieve user details for current authenticated user.

        Definition: GET /v1/users/self
        Required scopes: read_user_profile
        Detailed documentation and usage can be found here:
        https://marquee.gs.com/s/developer/docs/endpoint-reference/user-service/get-my-user-profile

        Parameters
        ----------
        _ : array of string, (optional)
            Client cache-busting parameter
        return_df : bool
            Try and return a pandas DataFrame if True
            or default response if False
        '''

        request_url = 'https://api.marquee.gs.com/v1/users/self'

        data = self._request(method='GET',
                             url=request_url,
                             return_df=return_df,
                             params=kwargs)
        return data
