"""
Copyright 2018 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""

import datetime as dt

from gs_quant.api.gs.esg import GsEsgApi, ESGCard, ESGMeasure
from gs_quant.session import *


def test_get_risk_models(mocker):
    mock_response = {
        'pricingDate': '2021-04-08',
        'summary': {
            'gross': {
                'gPercentile': 97.57,
                'gRegionalPercentile': 88.94,
                'esPercentile': 89.52,
                'esDisclosurePercentage': 83.33,
                'esMomentumPercentile': 28.15
            },
            'long': {
                'gPercentile': 97.57,
                'gRegionalPercentile': 88.94,
                'esPercentile': 89.52,
                'esDisclosurePercentage': 83.33,
                'esMomentumPercentile': 28.15},
            'short': {
                'gPercentile': None,
                'gRegionalPercentile': None,
                'esPercentile': None,
                'esDisclosurePercentage': None,
                'esMomentumPercentile': None
            },
            'benchmark': {
                'gPercentile': 76.30923829640506,
                'gRegionalPercentile': 54.3718544735162,
                'esPercentile': 51.677217204614415,
                'esDisclosurePercentage': 54.89969169789053,
                'esMomentumPercentile': 48.186284955203256
            }
        },
        'bottomTenRanked': [
            {
                'measure': 'gPercentile',
                'results': [
                    {
                        'assetId': 'MA4B66MW5E27UAHKG34',
                        'name': 'The Goldman Sachs Group, Inc.',
                        'value': 97.57
                    }
                ]
            }, {
                'measure': 'esDisclosurePercentage',
                'results': [
                    {
                        'assetId': 'MA4B66MW5E27UAHKG34',
                        'name': 'The Goldman Sachs Group, Inc.',
                        'value': 83.33
                    }
                ]
            }
        ],
        'noESGData': {
            'gross': {
                'weight': 0.0,
                'assets': []
            },
            'long': {
                'weight': 0.0,
                'assets': []
            },
            'short': {
                'weight': 0.0,
                'assets': []
            },
            'benchmark': {
                'weight': 2.5402270308391683,
                'assets': [
                    {
                        'assetId': 'MA4B66MW5E27UALNB96',
                        'name': 'News Corp - Class B',
                        'weight': 0.026140889953506573
                    }, {
                        'assetId': 'MA4B66MW5E27UANLXX3',
                        'name': 'Under Armour Inc-Class C',
                        'weight': 0.02019587639265163
                    }, {
                        'assetId': 'MA4B66MW5E27UAGYZ49',
                        'name': 'Alphabet Inc-CL C',
                        'weight': 2.4141476728491242
                    }, {
                        'assetId': 'MA4B66MW5E27UAE4MGB',
                        'name': 'Discovery Inc-C',
                        'weight': 0.03970496421509619
                    }, {
                        'assetId': 'MA4B66MW5E27UAGEHL4',
                        'name': 'Fox Corp - Class A',
                        'weight': 0.040037627428790246
                    }
                ]
            }
        }
    }

    # mock GsSession
    mocker.patch.object(
        GsSession.__class__,
        'default_value',
        return_value=GsSession.get(
            Environment.QA,
            'client_id',
            'secret'))
    mocker.patch.object(GsSession.current, '_get', return_value=mock_response)

    # run test
    response = GsEsgApi.get_esg(entity_id='MPM9Y3434RDFVKA3',
                                benchmark_id='MA4B66MW5E27U8P32SB',
                                pricing_date=dt.date(2021, 4, 8),
                                measures=[ESGMeasure.G_PERCENTILE, ESGMeasure.ES_DISCLOSURE_PERCENTAGE],
                                cards=[ESGCard.SUMMARY, ESGCard.BOTTOM_TEN_RANKED])
    GsSession.current._get.assert_called_with(
        '/esg/MPM9Y3434RDFVKA3?&date=2021-04-08&benchmark=MA4B66MW5E27U8P32SB&measure=gPercentile&'
        'measure=esDisclosurePercentage&card=summary&card=bottomTenRanked')
    assert response == mock_response
