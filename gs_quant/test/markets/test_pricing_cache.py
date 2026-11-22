"""Tests for the in-memory pricing cache."""

from gs_quant.markets import PricingCache


class _Instrument:
    pass


class _RiskKey:
    market = object()


def test_pricing_cache_clear_removes_values():
    PricingCache.clear()
    instrument = _Instrument()
    risk_key = _RiskKey()

    PricingCache.put(risk_key, instrument, 42.0)
    assert PricingCache.get(risk_key, instrument) == 42.0

    PricingCache.clear()
    assert PricingCache.get(risk_key, instrument) is None
