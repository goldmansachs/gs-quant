"""
Copyright 2026 Goldman Sachs.
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

from typing import Optional

import pandas as pd

from gs_quant.api.gs.data import QueryType
from gs_quant.common import AssetClass, AssetType
from gs_quant.data import DataContext, Dataset
from gs_quant.errors import MqValueError
from gs_quant.markets.securities import Asset, AssetIdentifier
from gs_quant.timeseries.helper import plot_measure
from gs_quant.timeseries.measures import (
    ASSET_SPEC,
    ExtendedSeries,
    MeasureDependency,
    _asset_from_spec,
)
from gs_quant.timeseries.measures_rates import swap_rate

# ---------------------------------------------------------------------------
# Government bond benchmark measures (backed by IR_BOND_FUNDAMENTALS_STANDARD)
# ---------------------------------------------------------------------------

# Curated GS constant-maturity government bond benchmarks in the
# IR_BOND_FUNDAMENTALS_STANDARD dataset. Key is (country_iso2, tenor_string).
# Tenor strings are canonical benchmark buckets ('1y', '2y', ..., '30y') for
# on-the-run benchmarks. Non-benchmark variants encode the label directly in
# the tenor string, e.g. '10y CTD', '2y RESIDUAL', '30y BUXL'. Callers pass
# the same string they see here as the ``tenor`` argument.
_BOND_DATASET_ID = 'IR_BOND_FUNDAMENTALS_STANDARD'

GOVT_BOND_BENCHMARK_ASSETS: dict = {
    ('US', '1y'): 'MATW4P6BDYFFZQVF',  # US Treasury 1y GOVN
    ('US', '2y'): 'MATGFS48Y8W0JDXK',  # US Treasury 2y GOVN
    ('US', '3y'): 'MA9N14WM73NWPVBK',  # US Treasury 3y GOVN
    ('US', '5y'): 'MAN2V78G66YYZKN1',  # US Treasury 5y GOVN
    ('US', '7y'): 'MAVFPHREKDSWT53E',  # US Treasury 7y GOVN
    ('US', '10y'): 'MAG83D7K91YQ9R83',  # US Treasury 10y GOVN
    ('US', '20y'): 'MAH5EF324H1E47DM',  # US Treasury 20y GOVN
    ('US', '30y'): 'MAFY9FJA25HP254W',  # US Treasury 30y GOVN
    ('GB', '2y'): 'MAMPJAR38T35VW5T',  # GB GILT 2Y GOVN
    ('GB', '3y'): 'MA1N7HZVYQH7NE12',  # GILT Short 3y GOVN
    ('GB', '5y'): 'MAJRHEJZWARC8D2Z',  # GB GILT 5Y GOVN
    ('GB', '5y CTD'): 'MAA5T8Y7WP7AXZ59',  # GILT Medium 5y GOVN
    ('GB', '10y'): 'MA28AJN2FYQG3PE0',  # GB GILT 10Y GOVN
    ('GB', '10y CTD'): 'MA519K7HVND44VKM',  # GILT Long 10y GOVN
    ('GB', '30y'): 'MAXBTR6W4VX9E2CW',  # GB GILT 30Y GOVN
    ('GB', '30y CTD'): 'MAM06BBVX7KRC9XF',  # GILT ULONG 30y GOVN
    ('DE', '2y'): 'MA6EFW2ACF36XF5K',  # DE SCHATZ 2y GOVN
    ('DE', '2y RESIDUAL'): 'MA0T1TREEXSZ5F6X',  # DE BUND 2Y GOVN
    ('DE', '3y'): 'MA23XMGWCGRPF2HM',  # DE BUND 3Y GOVN
    ('DE', '5y'): 'MADYWH0J0R04NFTQ',  # DE BOBL 5y GOVN
    ('DE', '5y RESIDUAL'): 'MA1Y5VKXEH80K7YE',  # DE BUND 5Y GOVN
    ('DE', '10y'): 'MASHSN4NEFSPRY6H',  # DE BUND 10Y GOVN
    ('DE', '10y CTD'): 'MAX7Q87QAFGTW8J0',  # DE BUND 10y GOVN
    ('DE', '30y'): 'MA0HGCJ88BZWTKZ0',  # DE BUND 30Y GOVN
    ('DE', '30y BUXL'): 'MADNBG9MWW3Z4YMR',  # DE BUXL 30y GOVN
    ('FR', '2y'): 'MA4A9FTXXXTPZDAM',  # FR OAT 2Y GOVN
    ('FR', '3y'): 'MADA9S2650Z0X1NG',  # FR OAT 3Y GOVN
    ('FR', '5y'): 'MA1SPBBP54BTK600',  # FR OAT 5Y GOVN
    ('FR', '10y'): 'MATG50CY8FBM270H',  # FR OAT 10Y GOVN
    ('FR', '10y CTD'): 'MAXJ604TJHEHSX40',  # FR OAT 10y GOVN
    ('FR', '30y'): 'MAY5KAVEAH601Z9W',  # FR OAT 30Y GOVN
    ('IT', '2y'): 'MAAXP9Y90NWE60A3',  # IT BTP 2Y GOVN
    ('IT', '3y'): 'MAX4J7RMF08286YX',  # IT BTP 3Y GOVN
    ('IT', '5y'): 'MAEW45VCAHCQ3P6T',  # IT BTP 5Y GOVN
    ('IT', '7y'): 'MATD37YQG2JJ39XJ',  # IT BTP 7Y GOVN
    ('IT', '10y'): 'MAASZXJ3QRH32VPG',  # IT BTP 10Y GOVN
    ('IT', '30y'): 'MATWV7N6FHFN4RBQ',  # IT BTP 30Y GOVN
    ('ES', '2y'): 'MA4ZC93ABRJEWFTG',  # ES BONOS 2Y GOVN
    ('ES', '3y'): 'MA2FGP1V8YY9HHGY',  # ES BONOS 3Y GOVN
    ('ES', '5y'): 'MADMG089XVHA39XS',  # ES BONOS 5Y GOVN
    ('ES', '10y'): 'MARHEKQTZVD34T51',  # ES BONOS 10Y GOVN
    ('ES', '30y'): 'MAV6QCVBYCPSMZZJ',  # ES BONOS 30Y GOVN
    ('AT', '2y'): 'MAKZ3HSNG1NSYBCD',  # AT RAGB 2Y GOVN
    ('AT', '3y'): 'MAAA71Q4JH0S4K55',  # AT RAGB 3Y GOVN
    ('AT', '5y'): 'MAE6F5W80GHA3Z40',  # AT RAGB 5Y GOVN
    ('AT', '10y'): 'MAMZYAQ6308JG4Y6',  # AT RAGB 10Y GOVN
    ('AT', '30y'): 'MAYWPCSVKBWKAWY4',  # AT RAGB 30Y GOVN
    ('BE', '2y'): 'MAAJ85KH033QVW2C',  # BE OLO 2Y GOVN
    ('BE', '3y'): 'MAXAKAJY7256D3TW',  # BE OLO 3Y GOVN
    ('BE', '5y'): 'MAECJXWHRR8RQRK4',  # BE OLO 5Y GOVN
    ('BE', '10y'): 'MAKS8KHW7RTSK0XN',  # BE OLO 10Y GOVN
    ('BE', '30y'): 'MAXAEEXMV65BM1J2',  # BE OLO 30Y GOVN
    ('NL', '2y'): 'MAM73TDMS7QJHTEJ',  # NL DSL 2Y GOVN
    ('NL', '3y'): 'MAP94H5DMZ4RCJ0Y',  # NL DSL 3Y GOVN
    ('NL', '5y'): 'MA9J9QBSJGTTWM0M',  # NL DSL 5Y GOVN
    ('NL', '10y'): 'MA31Q4YN6TK9CMHF',  # NL DSL 10Y GOVN
    ('NL', '30y'): 'MA8C0QBMTXH7PFK7',  # NL DSL 30Y GOVN
    ('PT', '2y'): 'MA78YHDJSRPZVG9C',  # PT PGB 2Y GOVN
    ('PT', '3y'): 'MA0YXDRR8FFVETRV',  # PT PGB 3Y GOVN
    ('PT', '5y'): 'MATET5AED6M5NQNG',  # PT PGB 5Y GOVN
    ('PT', '10y'): 'MAYEA6W31RS6V0PR',  # PT PGB 10Y GOVN
    ('PT', '30y'): 'MAWSZCS0PH0F9F65',  # PT PGB 30Y GOVN
    ('JP', '2y'): 'MATFB3JQRS27W52X',  # JP JGB 2Y GOVN
    ('JP', '5y'): 'MA3PEDV5KYK61FTQ',  # JP JGB 5Y GOVN
    ('JP', '10y'): 'MAY84CQEF1JNSSTA',  # JP JGB 10Y GOVN
    ('JP', '20y'): 'MAGX6V7M6CD9YETN',  # JP JGB 20Y GOVN
    ('JP', '30y'): 'MAXYMS2F0Y61HRS4',  # JP JGB 30Y GOVN
}

# Currency -> covered issuer countries in GOVT_BOND_BENCHMARK_ASSETS.
# For multi-issuer currencies (EUR) the caller must supply ``country``.
CURRENCY_TO_GOVT_COUNTRIES: dict = {
    'USD': ('US',),
    'GBP': ('GB',),
    'JPY': ('JP',),
    'EUR': ('DE', 'FR', 'IT', 'ES', 'AT', 'BE', 'NL', 'PT'),
}


def _resolve_govt_bond_asset(currency: str, tenor: str, country: Optional[str] = None) -> str:
    """Resolve ``(currency, tenor[, country])`` to a Marquee assetId in
    :data:`GOVT_BOND_BENCHMARK_ASSETS`.

    ``country`` is required only when a currency covers multiple issuers
    (EUR: DE, FR, IT, ES, AT, BE, NL, PT). For single-issuer currencies
    (USD, GBP, JPY) the country is inferred.
    """
    currency = currency.upper()
    countries = CURRENCY_TO_GOVT_COUNTRIES.get(currency)
    if not countries:
        raise MqValueError(
            f'No government bond coverage for currency={currency}. Supported: {list(CURRENCY_TO_GOVT_COUNTRIES)}'
        )
    if country is None:
        if len(countries) > 1:
            raise MqValueError(f'currency={currency} covers multiple issuers {countries}; specify country=...')
        country = countries[0]
    else:
        country = country.upper()
        if country not in countries:
            raise MqValueError(f'country={country} not covered by currency={currency}. Available: {countries}')
    key = (country, tenor)
    if key not in GOVT_BOND_BENCHMARK_ASSETS:
        available = sorted(t for (c, t) in GOVT_BOND_BENCHMARK_ASSETS if c == country)
        raise MqValueError(
            f'No government bond for country={country} tenor={tenor!r} in {_BOND_DATASET_ID}. '
            f'Available tenors for {country}: {available}'
        )
    return GOVT_BOND_BENCHMARK_ASSETS[key]


def _currency_to_govt_bond_asset(asset_spec: ASSET_SPEC) -> str:
    """Return a representative govt-bond assetId for a currency.

    Used by ``@plot_measure`` / ``MeasureDependency`` for entitlement and
    dependency-graph checks; actual per-call resolution happens inside each
    measure via :func:`_resolve_govt_bond_asset`. Prefers the 10y benchmark of
    the default (first) country for the currency.
    """
    asset = _asset_from_spec(asset_spec)
    ccy = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
    countries = CURRENCY_TO_GOVT_COUNTRIES.get((ccy or '').upper())
    if not countries:
        raise MqValueError(f'No govt bond coverage for currency={ccy}')
    for country in countries:
        aid = GOVT_BOND_BENCHMARK_ASSETS.get((country, '10y'))
        if aid is not None:
            return aid
    for country in countries:
        for (c, _t), aid in GOVT_BOND_BENCHMARK_ASSETS.items():
            if c == country:
                return aid
    raise MqValueError(f'No govt bond found for currency={ccy}')


def _fetch_bond_series(asset_id: str, field: str) -> ExtendedSeries:
    """Fetch one column of ``IR_BOND_FUNDAMENTALS_STANDARD`` for a single
    asset over the current :class:`DataContext` window."""
    ds = Dataset(_BOND_DATASET_ID)
    df = ds.get_data(
        assetId=[asset_id],
        startDate=DataContext.current.start_date,
        endDate=DataContext.current.end_date,
    )
    if df.empty or field not in df.columns:
        series = ExtendedSeries(dtype=float)
    else:
        # IR_BOND_FUNDAMENTALS_STANDARD occasionally returns multiple rows per
        # date (e.g. when the same benchmark rolls to a new on-the-run bond mid
        # day). Keep the last snapshot per date so downstream arithmetic doesn't
        # Cartesian on duplicate index labels.
        col = df[field].sort_index()
        col = col[~col.index.duplicated(keep='last')]
        series = ExtendedSeries(col)
    series.dataset_ids = (_BOND_DATASET_ID,)
    return series


@plot_measure(
    (AssetClass.Cash,),
    (AssetType.Currency,),
    [MeasureDependency(id_provider=_currency_to_govt_bond_asset, query_type=QueryType.SPOT)],
)
def govt_bond_yield(
    asset: Asset,
    tenor: str,
    country: Optional[str] = None,
    yield_type: str = 'YTM',
    *,
    source: Optional[str] = None,
    real_time: bool = False,
) -> pd.Series:
    """GS end-of-day yield for a curated constant-maturity government bond benchmark.

    :param asset: currency asset loaded from security master (e.g. USD, EUR, GBP, JPY)
    :param tenor: benchmark tenor string as used in :data:`GOVT_BOND_BENCHMARK_ASSETS`.
                  Plain buckets ('1y', '2y', ..., '30y') return the on-the-run benchmark;
                  variant labels are appended to the tenor, e.g. ``'10y CTD'``,
                  ``'2y RESIDUAL'``, ``'30y BUXL'``.
    :param country: ISO2 country code, required only when the currency covers multiple
                    issuers (EUR: DE, FR, IT, ES, AT, BE, NL, PT). Optional for USD/GBP/JPY.
    :param yield_type: one of ``'YTM'`` (yieldToMaturity, default), ``'MID'`` (yield),
                       or ``'WORST'`` (yieldToWorst)
    :param source: name of function caller
    :param real_time: whether to retrieve intraday data instead of EOD (not implemented)
    :return: government bond yield in decimal (e.g. ``0.027375`` == 2.7375%)
    """
    if real_time:
        raise NotImplementedError('realtime govt_bond_yield not implemented')

    field_map = {'YTM': 'yieldToMaturity', 'MID': 'yield', 'WORST': 'yieldToWorst'}
    field = field_map.get(yield_type.upper())
    if field is None:
        raise MqValueError(f'yield_type must be one of {list(field_map)}; got {yield_type!r}')

    ccy = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
    asset_id = _resolve_govt_bond_asset(ccy, tenor, country)
    return _fetch_bond_series(asset_id, field)


@plot_measure(
    (AssetClass.Cash,),
    (AssetType.Currency,),
    [MeasureDependency(id_provider=_currency_to_govt_bond_asset, query_type=QueryType.PRICE)],
)
def govt_bond_price(
    asset: Asset,
    tenor: str,
    country: Optional[str] = None,
    dirty: bool = False,
    *,
    source: Optional[str] = None,
    real_time: bool = False,
) -> pd.Series:
    """GS end-of-day price for a curated constant-maturity government bond benchmark.

    :param dirty: if True return ``dirtyPrice`` (clean + accrued interest);
                  else ``price`` (clean).
    """
    if real_time:
        raise NotImplementedError('realtime govt_bond_price not implemented')
    ccy = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
    asset_id = _resolve_govt_bond_asset(ccy, tenor, country)
    return _fetch_bond_series(asset_id, 'dirtyPrice' if dirty else 'price')


@plot_measure(
    (AssetClass.Cash,),
    (AssetType.Currency,),
    [MeasureDependency(id_provider=_currency_to_govt_bond_asset, query_type=QueryType.SPOT)],
)
def govt_bond_duration(
    asset: Asset,
    tenor: str,
    country: Optional[str] = None,
    duration_type: str = 'MODIFIED',
    *,
    source: Optional[str] = None,
    real_time: bool = False,
) -> pd.Series:
    """Historical duration for a curated constant-maturity government bond benchmark.

    :param duration_type: ``'MODIFIED'`` (modifiedDuration, default),
                          ``'MACAULAY'`` (macaulayDuration), or ``'DOLLAR'`` (dollarDuration)
    """
    if real_time:
        raise NotImplementedError('realtime govt_bond_duration not implemented')
    field_map = {
        'MODIFIED': 'modifiedDuration',
        'MACAULAY': 'macaulayDuration',
        'DOLLAR': 'dollarDuration',
    }
    field = field_map.get(duration_type.upper())
    if field is None:
        raise MqValueError(f'duration_type must be one of {list(field_map)}; got {duration_type!r}')
    ccy = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
    asset_id = _resolve_govt_bond_asset(ccy, tenor, country)
    return _fetch_bond_series(asset_id, field)


@plot_measure(
    (AssetClass.Cash,),
    (AssetType.Currency,),
    [MeasureDependency(id_provider=_currency_to_govt_bond_asset, query_type=QueryType.SPOT)],
)
def govt_bond_zspread(
    asset: Asset,
    tenor: str,
    country: Optional[str] = None,
    *,
    source: Optional[str] = None,
    real_time: bool = False,
) -> pd.Series:
    """Zero-volatility spread of the constant-maturity govt bond benchmark to the
    swap curve, in decimal (e.g. ``0.001063`` == 10.63 bp)."""
    if real_time:
        raise NotImplementedError('realtime govt_bond_zspread not implemented')
    ccy = asset.get_identifier(AssetIdentifier.BLOOMBERG_ID)
    asset_id = _resolve_govt_bond_asset(ccy, tenor, country)
    return _fetch_bond_series(asset_id, 'zSpread')


@plot_measure(
    (AssetClass.Cash,),
    (AssetType.Currency,),
    [MeasureDependency(id_provider=_currency_to_govt_bond_asset, query_type=QueryType.SPOT)],
)
def swap_govt_spread(
    asset: Asset,
    tenor: str,
    benchmark_type: str,
    floating_rate_tenor: Optional[str] = None,
    forward_tenor: Optional[str] = None,
    country: Optional[str] = None,
    yield_type: str = 'YTM',
    *,
    source: Optional[str] = None,
    real_time: bool = False,
) -> pd.Series:
    """Historical spread between the par swap rate and the matched-tenor government
    bond yield (``swap_rate - govt_bond_yield``).

    Not to be confused with a two-leg swap product; this is a single-number
    spread between two independent curves. Composes :func:`swap_rate` and
    :func:`govt_bond_yield`; both are pulled with the same tenor bucket. If
    ``tenor`` contains a variant suffix (e.g. ``'10y CTD'``) the plain bucket
    (``'10y'``) is used for the swap leg while the full string selects the
    bond. Returned series is in decimal (e.g. ``0.0006`` == 6 bp).

    ``benchmark_type`` is required: the swap-vs-govt spread is meaningless
    without pinning the swap-curve convention (SOFR vs LIBOR, ESTR vs
    EURIBOR-6M, etc.), and silently defaulting would hide a material choice
    from the caller.

    :param asset: currency asset (e.g. USD)
    :param tenor: matched-maturity tenor, e.g. '2y', '5y', '10y', '30y', or a
                  variant like '10y CTD'
    :param benchmark_type: swap benchmark type e.g. 'SOFR', 'ESTR',
                           'EURIBOR-6M' - forwarded to swap_rate
    :param floating_rate_tenor: swap floating index tenor - forwarded to swap_rate
    :param forward_tenor: forward-starting point - forwarded to swap_rate; the bond
                          leg does not support forward-starting yields, so callers
                          should be aware this only shifts the swap leg. Defaults
                          to ``'Spot'`` (matches the bond leg and disambiguates the
                          swap-asset lookup).
    :param country: ISO2 country code for the bond leg (required for EUR)
    :param yield_type: yield convention for the bond leg (default 'YTM')
    :return: swap-govt spread in decimal
    """
    if real_time:
        raise NotImplementedError('realtime swap_govt_spread not implemented')

    plain_tenor = tenor.split()[0]  # '10y CTD' -> '10y'
    # Default to spot-starting: swap_rate's _check_forward_tenor passes None
    # through unchanged, which the asset-lookup API treats as "no filter" on
    # effective_date and returns every forward-start swap for the currency +
    # index + tenor (triggering "Specified arguments match multiple assets").
    # Bond yields are spot-only, so a spot swap is the sensible matched leg.
    swap_leg = swap_rate(
        asset,
        plain_tenor,
        benchmark_type=benchmark_type,
        floating_rate_tenor=floating_rate_tenor,
        forward_tenor=forward_tenor if forward_tenor is not None else 'Spot',
        source=source,
        real_time=False,
    )
    bond_leg = govt_bond_yield(
        asset,
        tenor,
        country=country,
        yield_type=yield_type,
        source=source,
        real_time=False,
    )

    # swap_rate returns percent; govt_bond_yield returns decimal
    # Normalize the swap leg to decimal so
    # the returned spread is in decimal
    spread = (swap_leg / 100.0 - bond_leg).dropna()
    result = ExtendedSeries(spread)
    result.dataset_ids = tuple(
        set(getattr(swap_leg, 'dataset_ids', ()) or ()) | set(getattr(bond_leg, 'dataset_ids', ()) or ())
    )
    return result
