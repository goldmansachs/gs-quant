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

import datetime as dt
from types import SimpleNamespace

import pandas as pd
import pytest

import gs_quant.timeseries.measures_bonds as tm_bonds
from gs_quant.data.core import DataContext
from gs_quant.errors import MqValueError

# ---------- fixture helpers ----------


@pytest.fixture(autouse=True)
def _bypass_asset_from_spec(monkeypatch):
    """_asset_from_spec would otherwise call SecurityMaster.get_asset for
    non-Asset inputs, which needs a live session. Our SimpleNamespace fakes
    already expose get_identifier(), so pass them through unchanged."""
    monkeypatch.setattr(tm_bonds, '_asset_from_spec', lambda a: a)


def _fake_asset(ccy: str) -> SimpleNamespace:
    """Minimal Asset stand-in exposing get_identifier(BLOOMBERG_ID) -> currency string."""
    return SimpleNamespace(get_identifier=lambda _kind: ccy)


def _fake_dataset_frame(field: str, values) -> pd.DataFrame:
    dates = pd.date_range('2024-06-03', periods=len(values), freq='D', name='date')
    return pd.DataFrame({field: values, 'assetId': 'anything'}, index=dates)


# ---------- static universe ----------


def test_static_universe_expected_size():
    """Guardrail against accidental additions/removals to the static dict."""
    assert len(tm_bonds.GOVT_BOND_BENCHMARK_ASSETS) == 67


def test_static_universe_key_shape():
    for key, aid in tm_bonds.GOVT_BOND_BENCHMARK_ASSETS.items():
        assert isinstance(key, tuple) and len(key) == 2
        country, tenor = key
        assert isinstance(country, str) and len(country) == 2 and country.isupper()
        assert isinstance(tenor, str) and tenor[0].isdigit()
        assert isinstance(aid, str) and aid.startswith('MA')


# ---------- resolver ----------


def test_resolve_single_issuer_currency():
    assert tm_bonds._resolve_govt_bond_asset('USD', '10y') == 'MAG83D7K91YQ9R83'
    assert tm_bonds._resolve_govt_bond_asset('usd', '30y') == 'MAFY9FJA25HP254W'  # case insensitive


def test_resolve_eur_requires_country():
    with pytest.raises(MqValueError, match='covers multiple issuers'):
        tm_bonds._resolve_govt_bond_asset('EUR', '10y')


def test_resolve_eur_with_country_disambiguates():
    assert tm_bonds._resolve_govt_bond_asset('EUR', '10y', country='DE') == 'MASHSN4NEFSPRY6H'
    assert tm_bonds._resolve_govt_bond_asset('EUR', '10y', country='fr') == 'MATG50CY8FBM270H'
    assert tm_bonds._resolve_govt_bond_asset('EUR', '30y', country='IT') == 'MATWV7N6FHFN4RBQ'


def test_resolve_variant_tenor():
    """Variant labels are part of the tenor string itself."""
    assert tm_bonds._resolve_govt_bond_asset('EUR', '10y CTD', country='DE') == 'MAX7Q87QAFGTW8J0'
    assert tm_bonds._resolve_govt_bond_asset('EUR', '2y RESIDUAL', country='DE') == 'MA0T1TREEXSZ5F6X'
    assert tm_bonds._resolve_govt_bond_asset('EUR', '30y BUXL', country='DE') == 'MADNBG9MWW3Z4YMR'
    assert tm_bonds._resolve_govt_bond_asset('GBP', '10y CTD') == 'MA519K7HVND44VKM'
    assert tm_bonds._resolve_govt_bond_asset('GBP', '30y CTD') == 'MAM06BBVX7KRC9XF'


def test_resolve_missing_tenor_raises():
    with pytest.raises(MqValueError, match='No government bond'):
        tm_bonds._resolve_govt_bond_asset('JPY', '7y')  # JP has no 7y in the universe


def test_resolve_country_not_covered_by_currency():
    with pytest.raises(MqValueError, match='not covered'):
        tm_bonds._resolve_govt_bond_asset('USD', '10y', country='DE')


def test_resolve_unsupported_currency():
    with pytest.raises(MqValueError, match='No government bond coverage'):
        tm_bonds._resolve_govt_bond_asset('BRL', '10y')


def test_currency_to_govt_bond_asset_prefers_10y():
    assert tm_bonds._currency_to_govt_bond_asset(_fake_asset('USD')) == 'MAG83D7K91YQ9R83'
    assert tm_bonds._currency_to_govt_bond_asset(_fake_asset('GBP')) == 'MA28AJN2FYQG3PE0'
    assert tm_bonds._currency_to_govt_bond_asset(_fake_asset('JPY')) == 'MAY84CQEF1JNSSTA'
    # EUR: falls back to DE 10y (first covered country)
    assert tm_bonds._currency_to_govt_bond_asset(_fake_asset('EUR')) == 'MASHSN4NEFSPRY6H'


def test_currency_to_govt_bond_asset_unknown_currency():
    with pytest.raises(MqValueError, match='No govt bond coverage'):
        tm_bonds._currency_to_govt_bond_asset(_fake_asset('BRL'))


# ---------- yield / price / duration / zspread measures ----------


def test_govt_bond_yield_ytm(monkeypatch):
    captured = {}

    def fake_get_data(self, **kwargs):
        captured.update(kwargs)
        return _fake_dataset_frame('yieldToMaturity', [0.0273, 0.0269, 0.0265])

    monkeypatch.setattr('gs_quant.data.dataset.Dataset.get_data', fake_get_data)

    with DataContext(dt.date(2024, 6, 3), dt.date(2024, 6, 5)):
        s = tm_bonds.govt_bond_yield(_fake_asset('USD'), '10y')

    assert list(s.values) == [0.0273, 0.0269, 0.0265]
    assert s.dataset_ids == (tm_bonds._BOND_DATASET_ID,)
    assert captured['assetId'] == ['MAG83D7K91YQ9R83']
    assert captured['startDate'] == dt.date(2024, 6, 3)
    assert captured['endDate'] == dt.date(2024, 6, 5)


def test_govt_bond_yield_mid_and_worst(monkeypatch):
    def fake_get_data(self, **kwargs):
        idx = pd.date_range('2024-06-03', periods=2, freq='D', name='date')
        return pd.DataFrame(
            {'yield': [0.0271, 0.0270], 'yieldToWorst': [0.0272, 0.0271], 'yieldToMaturity': [0.0273, 0.0272]},
            index=idx,
        )

    monkeypatch.setattr('gs_quant.data.dataset.Dataset.get_data', fake_get_data)

    with DataContext(dt.date(2024, 6, 3), dt.date(2024, 6, 4)):
        mid = tm_bonds.govt_bond_yield(_fake_asset('USD'), '10y', yield_type='MID')
        worst = tm_bonds.govt_bond_yield(_fake_asset('USD'), '10y', yield_type='WORST')

    assert list(mid.values) == [0.0271, 0.0270]
    assert list(worst.values) == [0.0272, 0.0271]


def test_govt_bond_yield_variant_tenor(monkeypatch):
    """A variant tenor like '10y CTD' should route to the CTD assetId."""
    captured = {}

    def fake_get_data(self, **kwargs):
        captured.update(kwargs)
        return _fake_dataset_frame('yieldToMaturity', [0.0275])

    monkeypatch.setattr('gs_quant.data.dataset.Dataset.get_data', fake_get_data)

    with DataContext(dt.date(2024, 6, 3), dt.date(2024, 6, 3)):
        tm_bonds.govt_bond_yield(_fake_asset('EUR'), '10y CTD', country='DE')

    assert captured['assetId'] == ['MAX7Q87QAFGTW8J0']


def test_govt_bond_yield_invalid_yield_type():
    with pytest.raises(MqValueError, match='yield_type must be one of'):
        tm_bonds.govt_bond_yield(_fake_asset('USD'), '10y', yield_type='JUNK')


def test_govt_bond_price_clean_vs_dirty(monkeypatch):
    def fake_get_data(self, **kwargs):
        idx = pd.date_range('2024-06-03', periods=2, freq='D', name='date')
        return pd.DataFrame({'price': [98.5, 98.6], 'dirtyPrice': [98.7, 98.8]}, index=idx)

    monkeypatch.setattr('gs_quant.data.dataset.Dataset.get_data', fake_get_data)

    with DataContext(dt.date(2024, 6, 3), dt.date(2024, 6, 4)):
        clean = tm_bonds.govt_bond_price(_fake_asset('USD'), '10y')
        dirty = tm_bonds.govt_bond_price(_fake_asset('USD'), '10y', dirty=True)

    assert list(clean.values) == [98.5, 98.6]
    assert list(dirty.values) == [98.7, 98.8]


def test_govt_bond_duration_types(monkeypatch):
    def fake_get_data(self, **kwargs):
        idx = pd.date_range('2024-06-03', periods=1, freq='D', name='date')
        return pd.DataFrame(
            {'modifiedDuration': [19.8], 'macaulayDuration': [20.1], 'dollarDuration': [14.6]},
            index=idx,
        )

    monkeypatch.setattr('gs_quant.data.dataset.Dataset.get_data', fake_get_data)

    with DataContext(dt.date(2024, 6, 3), dt.date(2024, 6, 3)):
        assert tm_bonds.govt_bond_duration(_fake_asset('USD'), '10y').iloc[0] == 19.8
        assert tm_bonds.govt_bond_duration(_fake_asset('USD'), '10y', duration_type='MACAULAY').iloc[0] == 20.1
        assert tm_bonds.govt_bond_duration(_fake_asset('USD'), '10y', duration_type='DOLLAR').iloc[0] == 14.6


def test_govt_bond_duration_invalid_type():
    with pytest.raises(MqValueError, match='duration_type must be one of'):
        tm_bonds.govt_bond_duration(_fake_asset('USD'), '10y', duration_type='NOPE')


def test_govt_bond_zspread(monkeypatch):
    def fake_get_data(self, **_):
        return _fake_dataset_frame('zSpread', [0.0011, 0.0010])

    monkeypatch.setattr('gs_quant.data.dataset.Dataset.get_data', fake_get_data)

    with DataContext(dt.date(2024, 6, 3), dt.date(2024, 6, 4)):
        s = tm_bonds.govt_bond_zspread(_fake_asset('EUR'), '10y', country='DE')
    assert list(s.values) == [0.0011, 0.0010]


def test_fetch_bond_series_empty_frame_returns_empty_series(monkeypatch):
    monkeypatch.setattr('gs_quant.data.dataset.Dataset.get_data', lambda self, **_: pd.DataFrame())
    with DataContext(dt.date(2024, 6, 3), dt.date(2024, 6, 4)):
        s = tm_bonds._fetch_bond_series('MAG83D7K91YQ9R83', 'yieldToMaturity')
    assert s.empty
    assert s.dataset_ids == (tm_bonds._BOND_DATASET_ID,)


def test_fetch_bond_series_missing_field_returns_empty_series(monkeypatch):
    def fake_get_data(self, **_):
        idx = pd.date_range('2024-06-03', periods=1, freq='D', name='date')
        return pd.DataFrame({'price': [100.0]}, index=idx)

    monkeypatch.setattr('gs_quant.data.dataset.Dataset.get_data', fake_get_data)
    with DataContext(dt.date(2024, 6, 3), dt.date(2024, 6, 3)):
        s = tm_bonds._fetch_bond_series('MAG83D7K91YQ9R83', 'yieldToMaturity')
    assert s.empty


def test_fetch_bond_series_dedupes_repeated_dates(monkeypatch):
    """IR_BOND_FUNDAMENTALS_STANDARD sometimes returns multiple rows per date
    (e.g. mid-day benchmark roll). We must keep the last row per date so
    downstream arithmetic doesn't Cartesian on duplicate index labels."""

    def fake_get_data(self, **_):
        idx = pd.DatetimeIndex(
            ['2024-06-03', '2024-06-04', '2024-06-04', '2024-06-05', '2024-06-05'],
            name='date',
        )
        return pd.DataFrame(
            {'yieldToMaturity': [0.040, 0.041, 0.0415, 0.042, 0.0425], 'assetId': 'x'},
            index=idx,
        )

    monkeypatch.setattr('gs_quant.data.dataset.Dataset.get_data', fake_get_data)
    with DataContext(dt.date(2024, 6, 3), dt.date(2024, 6, 5)):
        s = tm_bonds._fetch_bond_series('MAG83D7K91YQ9R83', 'yieldToMaturity')

    assert not s.index.duplicated().any()
    assert len(s) == 3
    # keep=last: latest snapshot for each date wins
    assert list(s.values) == [0.040, 0.0415, 0.0425]


# ---------- swap_govt_spread composition ----------


def test_swap_govt_spread_subtracts_bond_from_swap(monkeypatch):
    idx = pd.date_range('2024-06-03', periods=3, freq='D', name='date')
    # swap_rate returns percent (e.g. 4.50 == 4.50%)
    swap_series = tm_bonds.ExtendedSeries(pd.Series([4.50, 4.51, 4.52], index=idx))
    swap_series.dataset_ids = ('SWAP_DS',)

    monkeypatch.setattr(tm_bonds, 'swap_rate', lambda *a, **kw: swap_series)

    def fake_get_data(self, **_):
        # govt bond dataset returns decimal (e.g. 0.0430 == 4.30%)
        return _fake_dataset_frame('yieldToMaturity', [0.0430, 0.0429, 0.0428])

    monkeypatch.setattr('gs_quant.data.dataset.Dataset.get_data', fake_get_data)

    with DataContext(dt.date(2024, 6, 3), dt.date(2024, 6, 5)):
        spread = tm_bonds.swap_govt_spread(_fake_asset('USD'), '10y', 'SOFR')

    # Result is in decimal: (swap%/100) - bond_decimal
    expected = [0.0450 - 0.0430, 0.0451 - 0.0429, 0.0452 - 0.0428]
    assert [round(v, 6) for v in spread.values] == [round(v, 6) for v in expected]
    assert 'SWAP_DS' in spread.dataset_ids
    assert tm_bonds._BOND_DATASET_ID in spread.dataset_ids


def test_swap_govt_spread_strips_variant_suffix_for_swap_leg(monkeypatch):
    """swap_govt_spread(..., tenor='10y CTD') should call swap_rate with '10y' but
    resolve the bond leg to the CTD assetId."""
    captured_swap = {}
    captured_bond = {}

    idx = pd.date_range('2024-06-03', periods=1, freq='D', name='date')
    swap_series = tm_bonds.ExtendedSeries(pd.Series([0.045], index=idx))
    swap_series.dataset_ids = ('SWAP_DS',)

    def fake_swap_rate(asset, tenor, **kw):
        captured_swap['tenor'] = tenor
        captured_swap['benchmark_type'] = kw.get('benchmark_type')
        captured_swap['forward_tenor'] = kw.get('forward_tenor')
        return swap_series

    def fake_get_data(self, **kwargs):
        captured_bond.update(kwargs)
        return _fake_dataset_frame('yieldToMaturity', [0.043])

    monkeypatch.setattr(tm_bonds, 'swap_rate', fake_swap_rate)
    monkeypatch.setattr('gs_quant.data.dataset.Dataset.get_data', fake_get_data)

    with DataContext(dt.date(2024, 6, 3), dt.date(2024, 6, 3)):
        tm_bonds.swap_govt_spread(_fake_asset('EUR'), '10y CTD', 'ESTR', country='DE')

    assert captured_swap['tenor'] == '10y'
    assert captured_swap['benchmark_type'] == 'ESTR'
    # Default to Spot: passing None through would match every forward-start
    # swap in the universe and raise 'Specified arguments match multiple assets'.
    assert captured_swap['forward_tenor'] == 'Spot'
    assert captured_bond['assetId'] == ['MAX7Q87QAFGTW8J0']


def test_swap_govt_spread_requires_benchmark_type():
    """benchmark_type is mandatory - the spread is meaningless without pinning
    the swap-curve convention (SOFR vs LIBOR, ESTR vs EURIBOR, etc.)."""
    with pytest.raises(TypeError, match='benchmark_type'):
        tm_bonds.swap_govt_spread(_fake_asset('USD'), '10y')  # type: ignore[call-arg]


# ---------- real_time=True is not implemented on any measure ----------


@pytest.mark.parametrize(
    'call',
    [
        lambda: tm_bonds.govt_bond_yield(_fake_asset('USD'), '10y', real_time=True),
        lambda: tm_bonds.govt_bond_price(_fake_asset('USD'), '10y', real_time=True),
        lambda: tm_bonds.govt_bond_duration(_fake_asset('USD'), '10y', real_time=True),
        lambda: tm_bonds.govt_bond_zspread(_fake_asset('USD'), '10y', real_time=True),
        lambda: tm_bonds.swap_govt_spread(_fake_asset('USD'), '10y', 'SOFR', real_time=True),
    ],
    ids=['yield', 'price', 'duration', 'zspread', 'swap_govt_spread'],
)
def test_measures_reject_real_time(call):
    with pytest.raises(NotImplementedError, match='realtime'):
        call()


# ---------- _currency_to_govt_bond_asset fallback paths ----------


def test_currency_to_govt_bond_asset_falls_back_to_non_10y(monkeypatch):
    """If a covered country has entries but no '10y' benchmark, the resolver
    should fall back to any available tenor for that country."""
    monkeypatch.setitem(tm_bonds.CURRENCY_TO_GOVT_COUNTRIES, 'ZZZ', ('ZZ',))
    monkeypatch.setitem(tm_bonds.GOVT_BOND_BENCHMARK_ASSETS, ('ZZ', '5y'), 'MAFAKE5YASSET000')
    assert tm_bonds._currency_to_govt_bond_asset(_fake_asset('ZZZ')) == 'MAFAKE5YASSET000'


def test_currency_to_govt_bond_asset_raises_when_no_entries(monkeypatch):
    """If a currency is registered but none of its countries have any entries
    in GOVT_BOND_BENCHMARK_ASSETS, resolution should raise MqValueError."""
    monkeypatch.setitem(tm_bonds.CURRENCY_TO_GOVT_COUNTRIES, 'ZZZ', ('ZZ',))
    with pytest.raises(MqValueError, match='No govt bond found'):
        tm_bonds._currency_to_govt_bond_asset(_fake_asset('ZZZ'))
