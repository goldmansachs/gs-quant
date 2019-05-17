# Copyright 2019 Goldman Sachs.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# Plot Service will make use of appropriately decorated functions in this module.

import logging
import time
from enum import Enum
from gs_quant.api.gs.data import GsDataApi
from gs_quant.markets.securities import Asset
from gs_quant.target.common import AssetClass, FieldFilterMap
from gs_quant.timeseries.helper import plot_measure
from gs_quant.errors import MqTypeError, MqValueError
from numbers import Real
from pandas import Series

_logger = logging.getLogger(__name__)


def _to_fx_strikes(strikes):
    out = []
    for strike in strikes:
        if strike == 50:
            out.append('ATMS')
        elif strike < 50:
            out.append(f'{strike}DC')
        else:
            out.append(f'{abs(100 - strike)}DP')
    return out


class SkewReference(Enum):
    DELTA = 'delta'
    NORMALIZED = 'normalized'
    SPOT = 'spot'
    FORWARD = 'forward'


class VolReference(Enum):
    DELTA_CALL = 'delta_call'
    DELTA_PUT = 'delta_put'
    NORMALIZED = 'normalized'
    SPOT = 'spot'
    FORWARD = 'forward'


def _market_data_timed(q):
    start = time.perf_counter()
    df = GsDataApi.get_market_data(q)
    _logger.debug('market data query ran in %.3f ms', (time.perf_counter() - start) * 1000)
    return df


@plot_measure((AssetClass.FX, AssetClass.Equity), None)
def skew(asset: Asset, tenor: str, strike_reference: SkewReference, distance: Real, *, location: str = 'NYC',
         source: str = None, real_time: bool = False) -> Series:
    """
    Difference in implied volatility of equidistant out-of-the-money put and call options.

    :param asset: asset object loaded from security master
    :param tenor: relative date representation of expiration date e.g. 1m
    :param strike_reference: reference for strike level (for equities)
    :param distance: distance from at-the-money option
    :param location: location at which a price fixing has been taken (for FX assets)
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: skew curve
    """
    if real_time:
        raise MqValueError('real-time skew not supported')

    if strike_reference in (SkewReference.DELTA, None):
        b = 50
    elif strike_reference == SkewReference.NORMALIZED:
        b = 0
    else:
        b = 100

    kwargs = {}
    if strike_reference in (SkewReference.DELTA, None):
        # using delta call strikes so X DP is represented as (100 - X) DC
        q_strikes = [100 - distance, distance, b]
    else:
        q_strikes = [b - distance, b + distance, b]

    if asset.asset_class == AssetClass.FX:
        q_strikes = _to_fx_strikes(q_strikes)
        kwargs['location'] = location
        column = 'deltaStrike'  # should use SkewReference.DELTA for FX
    else:
        assert asset.asset_class == AssetClass.Equity
        if not strike_reference:
            raise MqTypeError('strike reference required for equities')
        if strike_reference != SkewReference.NORMALIZED:
            q_strikes = [x / 100 for x in q_strikes]
        kwargs['strikeReference'] = strike_reference.value
        column = 'relativeStrike'

    kwargs[column] = q_strikes
    _logger.info('where tenor=%s and %s', tenor, kwargs)
    where = FieldFilterMap(tenor=tenor, **kwargs)
    q = GsDataApi.build_market_data_query([asset.get_marquee_id()], 'Implied Volatility', where=where, source=source)
    _logger.info('q %s', q)
    df = _market_data_timed(q)

    curves = {k: v for k, v in df.groupby(column)}
    if len(curves) < 3:
        raise MqValueError('skew not available for given inputs')
    series = [curves[qs]['impliedVolatility'] for qs in q_strikes]
    return (series[0] - series[1]) / series[2]


@plot_measure((AssetClass.Equity,), None)
def implied_volatility(asset: Asset, tenor: str, strike_reference: VolReference, relative_strike: Real, *,
                       source: str = None, real_time: bool = False) -> Series:
    """
    Volatility of an asset implied by observations of market prices.

    :param asset: asset object loaded from security master
    :param tenor: relative date representation of expiration date e.g. 1m
    :param strike_reference: reference for strike level
    :param relative_strike: strike relative to reference
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD
    :return: implied volatility curve
    """
    # reading straight from data service, for now
    if asset.asset_class != AssetClass.Equity:
        raise MqValueError('implied volatility only implemented for equities')

    if strike_reference == VolReference.DELTA_PUT:
        relative_strike = abs(100 - relative_strike)

    relative_strike = relative_strike if strike_reference == VolReference.NORMALIZED else relative_strike / 100
    ref_string = "delta" if strike_reference in (VolReference.DELTA_CALL,
                                                 VolReference.DELTA_PUT) else strike_reference.value
    _logger.info('where tenor=%s, strikeReference=%s, relativeStrike=%s', tenor, ref_string, relative_strike)
    where = FieldFilterMap(tenor=tenor, strikeReference=ref_string, relativeStrike=relative_strike)
    q = GsDataApi.build_market_data_query([asset.get_marquee_id()], 'Implied Volatility', where=where, source=source,
                                          real_time=real_time)
    _logger.info('q %s', q)
    df = _market_data_timed(q)
    return Series() if df.empty else df['impliedVolatility']
