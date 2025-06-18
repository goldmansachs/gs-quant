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

import numpy as np
import pytest

import gs_quant.risk as risk
from gs_quant.base import RiskKey
from gs_quant.common import MarketDataPattern, RiskRequestParameters
from gs_quant.instrument import IRSwap, IRBasisSwap, IRSwaption, FXMultiCrossBinary, FXMultiCrossBinaryLeg, CommodSwap
from gs_quant.markets import HistoricalPricingContext, PricingContext, CloseMarket, MarketDataCoordinate
from gs_quant.markets.portfolio import Portfolio
from gs_quant.risk import MultiScenario, ResolvedInstrumentValues
from gs_quant.risk import Price, RollFwd, CurveScenario, ErrorValue, DataFrameWithInfo, AggregationLevel, PnlExplain
from gs_quant.risk.core import aggregate_risk, SeriesWithInfo, FloatWithInfo, StringWithInfo
from gs_quant.risk.results import MultipleScenarioFuture
from gs_quant.risk.results import MultipleScenarioResult
from gs_quant.risk.transform import ResultWithInfoAggregator
from gs_quant.test.utils.mock_calc import MockCalc

curvescen1 = CurveScenario(market_data_pattern=MarketDataPattern('IR', 'USD'), parallel_shift=5,
                           name='parallel shift5bp')
curvescen2 = CurveScenario(market_data_pattern=MarketDataPattern('IR', 'USD'), curve_shift=1, tenor_start=5,
                           tenor_end=30, name='curve shift1bp')
rollfwd = RollFwd(date=dt.date(2020, 11, 3), name='roll fwd scenario')
multiscenario = MultiScenario(scenarios=tuple((curvescen1, curvescen2)), name='multiscenario')


def get_attributes(p, risks, ctx='PricingCtx1', resolve=False, no_frame=False):
    contexts = {
        'Multiple': HistoricalPricingContext(dt.date(2020, 1, 14), dt.date(2020, 1, 15), market_data_location='LDN'),
        'PricingCtx1': PricingContext(dt.date(2020, 1, 14), market_data_location='LDN'),
        'Multiple2': HistoricalPricingContext(dt.date(2020, 1, 16), dt.date(2020, 1, 17), market_data_location='LDN'),
        'PricingCtx2': PricingContext(dt.date(2020, 1, 16), market_data_location='NYC'),
        'PricingCtx3': PricingContext(dt.date(2020, 1, 16), market_data_location='LDN'),
        'RollFwd': rollfwd, 'CurveScen1': curvescen1, 'CurveScen2': curvescen2, 'MultiScen': multiscenario}
    if resolve:
        p.resolve()
    if contexts.get(ctx):
        with contexts.get(ctx):
            res = p.calc(risks)
    elif ctx == 'Composite':
        with rollfwd, multiscenario:
            res = p.calc(risks)

    if not no_frame:
        frame = res.to_frame(None, None, None)
        return [col for col in frame.columns], res, frame
    else:
        return res


swap_1 = IRSwap("Pay", "5y", "EUR", fixed_rate=-0.005, name="5y")
swap_2 = IRSwap("Pay", "10y", "EUR", fixed_rate=-0.005, name="10y")
swap_3 = IRSwap("Pay", "5y", "USD", fixed_rate=-0.005, name="5y")
swap_4 = IRSwap("Pay", "10y", "USD", fixed_rate=-0.005, name="10y")
swap_5 = IRSwap("Pay", "5y", "GBP", fixed_rate=-0.005, name="5y")
swap_6 = IRSwap("Pay", "10y", "GBP", fixed_rate=-0.005, name="10y")
swap_7 = IRSwap("Pay", "5y", "JPY", fixed_rate=-0.005, name="5y")
swap_8 = IRSwap("Pay", "10y", "JPY", fixed_rate=-0.005, name="10y")
commod_swap = CommodSwap(name="Test")
eur_port = Portfolio([swap_1, swap_2], name="EUR")
usd_port = Portfolio([swap_3, swap_4], name="USD")
gbp_port = Portfolio([swap_5, swap_6], name="GBP")
jpy_port = Portfolio([swap_7, swap_8], name='JPY')
port1 = Portfolio([eur_port, gbp_port], name='EURGBP')
port2 = Portfolio([jpy_port, usd_port], name='USDJPY')
commod_port = Portfolio([commod_swap])
port = Portfolio([port1, port2])
swaption_port = Portfolio([IRSwaption("Receive", '5y', 'USD', expiration_date='2m', strike='atm', name='Swaption1'),
                           IRSwaption("Receive", '10y', 'USD', expiration_date='3m', strike='atm', name='Swaption2')])

bs = IRBasisSwap(termination_date="2y", notional_currency="GBP", notional_amount="$405392/bp", effective_date="10y",
                 payer_rate_option="OIS", receiver_frequency="3m", name='IRBasisSwap')

bs_port = Portfolio([bs])
mixed_port = Portfolio([bs_port, gbp_port])

swaption_1 = IRSwaption('Pay', '5y', 'USD', expiration_date='1y', name='1y')
swaption_2 = IRSwaption('Pay', '5y', 'USD', expiration_date='3m', name='3m')
swaption_3 = IRSwaption('Pay', '5y', 'USD', expiration_date='6m', name='6m')

swaption_port1 = Portfolio((swaption_1, swaption_2, swaption_3))
swaption_port2 = Portfolio([swaption_1, swaption_2])
swap_port1 = Portfolio([swaption_port1, usd_port])
swap_port2 = Portfolio([swaption_port2, usd_port])
# Portfolio of swaption with an unmarked correlation
swaption_port3 = Portfolio(IRSwaption('Pay', termination_date='6m', effective_date='2y', expiration_date='3y'))

mcb = Portfolio(FXMultiCrossBinary(name='mcb', legs=(FXMultiCrossBinaryLeg(),)), name='mcb_port')


def default_pivot_table_test(res, with_dates=''):
    port_depth = len(max(res.portfolio.all_paths, key=len))
    pivot_df = res.to_frame()
    if with_dates == 'dated':
        assert pivot_df.index.name == 'dates'
    else:
        if with_dates == 'has_bucketed':
            if res.dates:
                assert pivot_df.index.names[-3:] == ['instrument_name', 'risk_measure', 'dates']
            else:
                assert pivot_df.index.names[-2:] == ['instrument_name', 'risk_measure']
            assert pivot_df.columns.values[-1] == 'value'
        else:
            if port_depth == 1:
                assert pivot_df.index.nlevels == port_depth

            if len(res._multi_scen_key) > 1:
                if len(res.risk_measures) > 1:
                    assert pivot_df.columns.names == ['risk_measure', 'scenario']
                else:
                    assert pivot_df.columns.name == 'scenario'
            else:
                if port_depth == 1:
                    assert pivot_df.columns.name == 'risk_measure'
                else:
                    assert pivot_df.columns.names[-1] == 'risk_measure'


def price_values_test(res, f, with_dates=''):
    port_depth = len(max(res.portfolio.all_paths, key=len)) + 1  # +1 for risk measure
    if with_dates == 'dated':
        port_depth += 1  # +1 for dates
    if len(res.risk_measures) > 1:
        res_val_map = [n for r in res for n in r[Price].values] if with_dates == 'dated' else [r[Price] for r in res]
    else:
        res_val_map = [n for r in res for n in r.values] if with_dates == 'dated' else list(res)

    f = f.replace('N/A', np.nan)[f['risk_measure'] == risk.Price].dropna(axis='columns')
    df_val_map = f['value'].values
    f = f.drop('value', axis=1)

    assert all(res_val_map == df_val_map)  # check if price values are correctly tabulated
    assert (port_depth == f.columns.size)  # check if index setting is correct


def test_multi_scenario(mocker):
    with MockCalc(mocker):
        _, r1, f1 = get_attributes(usd_port, risk.Price, resolve=True, ctx='MultiScen')
        _, r2, f2 = get_attributes(usd_port, (risk.Price, risk.DollarPrice), resolve=True, ctx='MultiScen')
        _, r3, f3 = get_attributes(port1, (risk.IRFwdRate, risk.Price), resolve=True, ctx='MultiScen')
        _, r4, f4 = get_attributes(port1, risk.Price, resolve=True, ctx='MultiScen')

    default_pivot_table_test(r1)
    default_pivot_table_test(r2)
    default_pivot_table_test(r3)
    default_pivot_table_test(r4)

    # test slicing
    swap_res = r1[swap_3]
    swap_res_idx = r1[0]
    assert isinstance(swap_res, MultipleScenarioResult)
    assert swap_res == swap_res_idx

    multi_rm_and_scen_res = r3[curvescen1]
    multi_scen_res = r4[curvescen1]
    assert multi_rm_and_scen_res._multi_scen_key[0] == multi_scen_res._multi_scen_key[0] == curvescen1

    # test futures
    futures = r1.futures
    assert len(futures) == 2
    assert isinstance(futures[0], MultipleScenarioFuture)
    assert isinstance(futures[0].result(), MultipleScenarioResult)


def test_historical_multi_scenario(mocker):
    with MockCalc(mocker):
        with HistoricalPricingContext(dt.date(2020, 1, 14), dt.date(2020, 1, 15), market_data_location='LDN'):
            with multiscenario:
                res = Portfolio(swap_3).price()
                res_multi_rm = Portfolio(swap_3).calc((risk.Price, risk.IRFwdRate))

    default_pivot_table_test(res, with_dates='dated')
    default_pivot_table_test(res_multi_rm, with_dates='dated')

    # test slicing
    date_res = res[dt.date(2020, 1, 14)]
    assert all([isinstance(r, FloatWithInfo) for r in date_res.futures[0].result().values()])
    date_res_2 = res_multi_rm[swap_3][risk.Price][dt.date(2020, 1, 14)]
    assert all([isinstance(r, FloatWithInfo) for r in date_res_2.values()])

    scen_slice_res = res[curvescen2]
    assert all([isinstance(r, SeriesWithInfo) for r in scen_slice_res.futures[0].result().values()])
    assert isinstance(res_multi_rm[swap_3][risk.Price][curvescen2], SeriesWithInfo)

    # test futures
    futures = res.futures
    assert isinstance(futures[0], MultipleScenarioFuture)
    assert isinstance(futures[0].result(), MultipleScenarioResult)


def test_series_with_info_arithmetics(mocker):
    series_info = SeriesWithInfo([2.0, 4.0], [dt.date(2021, 4, 11), dt.date(2022, 4, 11)])
    scaled = series_info * 100
    assert isinstance(scaled, SeriesWithInfo)
    assert tuple(scaled.values) == (200., 400.)


def test_composite_multi_scenario(mocker):
    with MockCalc(mocker):
        c, res1, _ = get_attributes(usd_port, risk.Price, resolve=True, ctx='Composite')
        c2, res2, _ = get_attributes(eur_port, (risk.Price, risk.IRFwdRate), resolve=True, ctx='Composite')

    assert 'scenario' in c
    assert 'scenario' in c2
    assert 'risk_measure' in c2
    assert len(res1.risk_measures) == 1
    assert len(res2.risk_measures) == 2


def test_one_portfolio(mocker):
    with MockCalc(mocker):
        _, r1, f1 = get_attributes(eur_port, risk.Price)
        _, r2, f2 = get_attributes(eur_port, (risk.Price, risk.DollarPrice))
        _, _, f3 = get_attributes(Portfolio(swap_1, name='swap_1'), (risk.Price, risk.DollarPrice))
    price_values_test(r1, f1)
    price_values_test(r2, f2)

    default_pivot_table_test(r1)
    default_pivot_table_test(r2)

    # test slicing
    # slice one risk measure
    sub_r1 = r1[risk.Price]
    assert sub_r1 == r1
    # slice one instrument
    sub_r2 = r2[swap_1].to_frame().values[0]
    assert all(sub_r2 == f3['value'].values)

    # test aggregate
    agg_r1 = r1.aggregate().to_frame()
    agg_r2 = r2.aggregate().to_frame().values[0]
    assert agg_r1 == sum(f1['value'].values)
    assert all(
        agg_r2 == [sum(f2.loc[f2['risk_measure'] == rm]['value'].values) for rm in [risk.Price, risk.DollarPrice]])


def test_dated_risk_values(mocker):
    with MockCalc(mocker):
        _, res1, frame1 = get_attributes(port, risk.Price, 'Multiple')
        _, res2, frame2 = get_attributes(port1, (risk.DollarPrice, risk.Price), 'Multiple')
        _, res3, frame3 = get_attributes(port1, risk.Price)
        _, res4, frame4 = get_attributes(port1, (risk.DollarPrice, risk.Price))
        _, res5, frame5 = get_attributes(gbp_port, (risk.DollarPrice, risk.Price), 'Multiple')
        _, res6, frame6 = get_attributes(jpy_port, risk.Price, 'Multiple')

    price_values_test(res1, frame1, 'dated')
    price_values_test(res2, frame2, 'dated')
    price_values_test(res5, frame5, 'dated')
    price_values_test(res6, frame6, 'dated')

    default_pivot_table_test(res1, 'dated')
    default_pivot_table_test(res2, 'dated')
    default_pivot_table_test(res5, 'dated')
    default_pivot_table_test(res6, 'dated')

    # test slicing
    sub_res1 = res1[risk.Price]
    assert sub_res1 == res1

    # slice one date
    slice_date_res2 = res2[dt.date(2020, 1, 14)]
    assert all(slice_date_res2.to_frame(None, None, None) == frame4)
    slice_date_res3 = slice_date_res2[risk.Price]
    assert all(slice_date_res3.to_frame(None, None, None) == frame3)

    # slice dates
    slice_date_res2 = res2[[dt.date(2020, 1, 14), dt.date(2020, 1, 15)]]
    assert all(slice_date_res2.to_frame(None, None, None) == frame2)

    # test aggregate
    agg_res5 = res5.aggregate().to_frame(None, None, None)

    def filter_lambda(x):
        return (x['risk_measure'] == risk.DollarPrice) & (x['dates'] == dt.date(2020, 1, 14))

    manual_agg_r5 = frame5.loc[frame5.apply(filter_lambda, axis=1)]['value'].values.sum()
    filter_agg_res5 = agg_res5.loc[agg_res5.apply(filter_lambda, axis=1)]['value'].values[0]
    assert filter_agg_res5 == manual_agg_r5

    sub_res6 = res6.aggregate().to_frame().loc[dt.date(2020, 1, 14)].values[0]
    manual_agg_r6 = frame6.loc[frame6['dates'] == dt.date(2020, 1, 14)]['value'].values.sum()
    assert sub_res6 == manual_agg_r6


def test_bucketed_risks(mocker):
    with MockCalc(mocker):
        _, res1, frame1 = get_attributes(eur_port, risk.IRDelta)
        _, res2, frame2 = get_attributes(port, risk.IRDelta)
        _, res3, frame3 = get_attributes(gbp_port, risk.IRDelta)
        _, res4, frame4 = get_attributes(port1, risk.IRDelta, 'Multiple')
        _, res5, frame5 = get_attributes(bs_port, risk.IRBasis(aggregation_level=AggregationLevel.Asset))
        _, res6, frame6 = get_attributes(jpy_port, risk.IRBasis(aggregation_level=AggregationLevel.Asset), 'Multiple')
        _, res7, frame7 = get_attributes(commod_port, risk.CommodDelta, "Multiple")

    def check_depth(res, f, with_dates=''):
        temp_res = list(res)[0].drop('value', axis=1)
        port_depth = len(max(res.portfolio.all_paths, key=len)) + temp_res.columns.size
        port_depth = port_depth + 2 if with_dates == 'dated' else port_depth + 1
        f_temp = f.drop('value', axis=1)
        assert (port_depth == f_temp.columns.size)

    check_depth(res1, frame1)
    check_depth(res2, frame2)
    check_depth(res3, frame3)
    check_depth(res4, frame4, 'dated')
    check_depth(res5, frame5)
    check_depth(res6, frame6, 'dated')
    check_depth(res7, frame7, 'dated')

    default_pivot_table_test(res1, 'has_bucketed')
    default_pivot_table_test(res2, 'has_bucketed')
    default_pivot_table_test(res3, 'has_bucketed')
    default_pivot_table_test(res4, 'has_bucketed')
    default_pivot_table_test(res5, 'has_bucketed')
    default_pivot_table_test(res6, 'has_bucketed')
    default_pivot_table_test(res7, 'has_bucketed')

    # test slicing
    # slice one portfolio
    sub_res2 = res2[gbp_port]
    assert all(sub_res2.to_frame() == res1.to_frame())

    # slice one date
    sub_res4 = res4[dt.date(2020, 1, 14)]
    assert all(sub_res4[gbp_port].to_frame(None, None, None) == frame3)
    # slice dates
    sub_res4b = res4[[dt.date(2020, 1, 14), dt.date(2020, 1, 15)]]
    assert all(sub_res4b.to_frame(None, None, None) == frame4)

    # test aggregate
    agg_r1 = res1.aggregate().to_frame()
    manual_agg_f1 = frame1.loc[frame1['mkt_point'] == '5Y']['value'].sum()
    np.testing.assert_almost_equal(agg_r1.loc[agg_r1['mkt_point'] == '5Y']['value'].values[0], manual_agg_f1, 8)

    def filter_lambda(x):
        return (x['dates'] == dt.date(2020, 1, 14)) & (x['mkt_asset'] == 'JPY OIS/JPY-3M')

    agg_r6 = res6.aggregate().to_frame()
    filter_agg_r6 = agg_r6.loc[agg_r6.apply(filter_lambda, axis=1)]['value'].values[0]
    manual_agg_f6 = frame6.loc[frame6.apply(filter_lambda, axis=1)]['value'].values.sum()
    np.testing.assert_almost_equal(filter_agg_r6, manual_agg_f6, 8)

    assert isinstance(res7[dt.date(2020, 1, 14)].result().futures[0].result(), DataFrameWithInfo)
    assert res7[dt.date(2020, 1, 14)].to_frame()["mkt_type"].iloc[0] == "CMD NRG"


def test_cashflows_risk(mocker):
    with MockCalc(mocker):
        _, _, frame1 = get_attributes(eur_port, risk.Cashflows)
        _, _, frame2 = get_attributes(port1, risk.Cashflows)

    assert 'payment_date' in frame1.columns.values
    assert 'payment_date' in frame2.columns.values

    assert np.unique(frame1.risk_measure.values)[0] == risk.Cashflows
    assert np.unique(frame2.risk_measure.values)[0] == risk.Cashflows

    assert 'instrument_name' in frame1.columns.values
    assert 'instrument_name' in frame2.columns.values
    assert 'portfolio_name_0' in frame2.columns.values


def test_nested_portfolio(mocker):
    with MockCalc(mocker):
        cols1, res1, frame1 = get_attributes(port1, (risk.DollarPrice, risk.Price))
        cols2, res2, frame2 = get_attributes(port, (risk.DollarPrice, risk.Price))
        _, swap1_6_res, frame3 = get_attributes(Portfolio((swap_1, swap_6), name='swap_1_6'), risk.DollarPrice)
        _, res4, frame4 = get_attributes(port1, (risk.DollarPrice, risk.Price, risk.Theta))

    price_values_test(res1, frame1)
    price_values_test(res2, frame2)
    dollar_eur_frame1 = frame1[(frame1['portfolio_name_0'] == 'EUR') & (frame1['risk_measure'] == risk.DollarPrice)][
        'value'].values
    dollar_eur_frame2 = frame2[(frame2['portfolio_name_0'] == 'EURGBP') & (frame2['portfolio_name_1'] == 'EUR') &
                               (frame2['risk_measure'] == risk.DollarPrice)]['value'].values

    default_pivot_table_test(res1)
    default_pivot_table_test(res2)

    # test slicing
    # slice multiple instruments
    slice_res2 = res1[[swap_1, swap_6]][risk.DollarPrice].to_frame(None, None, None)['value'].values
    assert all(slice_res2 == swap1_6_res.to_frame(None, None, None)['value'].values)

    sub_frame1 = res1[risk.DollarPrice][swap_1].to_frame()
    assert sub_frame1 == dollar_eur_frame1[0]
    assert sub_frame1 == dollar_eur_frame2[0]

    sub_frame2 = res2[eur_port][risk.DollarPrice].to_frame(None, None, None)['value'].values
    assert all(dollar_eur_frame1 == sub_frame2)
    assert all(dollar_eur_frame2 == sub_frame2)
    # slice multiple risk measures
    sub_res4 = res4[[risk.Price, risk.DollarPrice]]
    assert all(sub_res4.to_frame() == res1.to_frame())


def test_diff_types_risk_measures(mocker):
    # when risk results from scalar and bucketed risk measures are be to tabulated together
    with MockCalc(mocker):
        _, res1, frame1 = get_attributes(eur_port, (risk.Price, risk.IRDelta))
        _, res2, frame2 = get_attributes(mixed_port, (risk.IRBasis, risk.Price))
        _, res3, frame3 = get_attributes(mixed_port,
                                         (risk.IRBasis(aggregation_level=AggregationLevel.Asset), risk.Price))
        _, res4, frame4 = get_attributes(eur_port, (risk.IRDelta, risk.Price), 'Multiple')
        _, res5, frame5 = get_attributes(mixed_port, (risk.Price, risk.IRBasis), 'Multiple')
        _, res6, frame6 = get_attributes(mixed_port,
                                         (risk.IRBasis(aggregation_level=AggregationLevel.Asset), risk.Price),
                                         'Multiple')

    price_values_test(res1, frame1)
    price_values_test(res2, frame2)
    price_values_test(res3, frame3)
    price_values_test(res4, frame4, 'dated')
    price_values_test(res5, frame5, 'dated')
    price_values_test(res6, frame6, 'dated')

    default_pivot_table_test(res1, 'has_bucketed')
    default_pivot_table_test(res2, 'has_bucketed')
    default_pivot_table_test(res3, 'has_bucketed')
    default_pivot_table_test(res4, 'has_bucketed')
    default_pivot_table_test(res5, 'has_bucketed')
    default_pivot_table_test(res6, 'has_bucketed')

    # test aggregate
    sub_res1 = res1.aggregate().to_frame()
    assert all(sub_res1.loc[risk.IRDelta]['value'].values == res1[risk.IRDelta].aggregate().to_frame()['value'].values)
    assert sub_res1.loc[risk.Price]['value'] == res1[risk.Price].aggregate().to_frame()


def test_empty_calc_request(mocker):
    # when calc req is sent for rm that inst is insensitive to
    with MockCalc(mocker):
        _, r1, f1 = get_attributes(swap_port1, (risk.IRVega, risk.Price))
        _, r2, f2 = get_attributes(swap_port2, (risk.IRVega(aggregation_level=AggregationLevel.Asset), risk.Price))
        _, r3, f3 = get_attributes(swap_port1, (
            risk.IRVega(aggregation_level=AggregationLevel.Asset, currency='local'), risk.Price))
        _, r4, f4 = get_attributes(swap_port2, (risk.Price, risk.IRVega(currency='local')))
        _, r5, f5 = get_attributes(swap_port2, (risk.Price, risk.IRVega), 'Multiple')
        _, r6, f6 = get_attributes(swap_port1, (risk.IRVega(aggregation_level=AggregationLevel.Asset), risk.Price),
                                   'Multiple')
        _, r7, f7 = get_attributes(swap_port2, (
            risk.IRVega(aggregation_level=AggregationLevel.Asset, currency='local'), risk.Price), 'Multiple')
        _, r8, f8 = get_attributes(swap_port1, (risk.IRVega(currency='local'), risk.Price), 'Multiple')

    price_values_test(r1, f1)
    price_values_test(r2, f2)
    price_values_test(r3, f3)
    price_values_test(r4, f4)
    price_values_test(r5, f5, 'dated')
    price_values_test(r6, f6, 'dated')
    price_values_test(r7, f7, 'dated')
    price_values_test(r8, f8, 'dated')

    default_pivot_table_test(r1, 'has_bucketed')
    default_pivot_table_test(r2, 'has_bucketed')
    default_pivot_table_test(r3, 'has_bucketed')
    default_pivot_table_test(r4, 'has_bucketed')
    default_pivot_table_test(r5, 'has_bucketed')
    default_pivot_table_test(r6, 'has_bucketed')
    default_pivot_table_test(r7, 'has_bucketed')
    default_pivot_table_test(r8, 'has_bucketed')


def test_adding_risk_results(mocker):
    with MockCalc(mocker):
        result1 = get_attributes(eur_port, risk.Price, no_frame=True)
        result2 = get_attributes(eur_port,
                                 (risk.IRDelta(aggregation_level=AggregationLevel.Asset, currency='local'), risk.Price),
                                 no_frame=True)
        result3 = get_attributes(swaption_port,
                                 (risk.IRDelta(aggregation_level=AggregationLevel.Asset, currency='local'), risk.Price),
                                 no_frame=True)
        result4 = get_attributes(port1, risk.Price, no_frame=True)
        result5 = get_attributes(swaption_port, risk.IRVega(aggregation_level=AggregationLevel.Asset, ), no_frame=True)
        result6 = get_attributes(jpy_port, (risk.Price,), 'RollFwd', no_frame=True)
        result7 = get_attributes(jpy_port, risk.Price, 'CurveScen1', no_frame=True)
        result8 = get_attributes(jpy_port, (risk.DollarPrice, risk.Price), 'CurveScen2', no_frame=True)

        # (2020, 1, 14) to (2020, 1, 15)
        result9 = get_attributes(port1, risk.Price, 'Multiple', no_frame=True)
        # (2020, 1, 16) to (2020, 1, 17)
        result10 = get_attributes(port1, risk.Price, 'Multiple2', no_frame=True)
        # (2020, 1, 14)
        result11 = get_attributes(port1, risk.Price, no_frame=True)
        # (2020, 1, 16), market_data_location='NYC'
        result12 = get_attributes(port1, risk.Price, 'PricingCtx2', no_frame=True)
        # (2020, 1, 16), market_data_location='LDN'
        result13 = get_attributes(port1, risk.Price, 'PricingCtx3', no_frame=True)

    # adding results with same portfolio but different risk measures
    add_1 = result3 + result5
    # adding results with different portfolio but same risk measures
    add_2 = result2 + result3
    # adding results with different portfolios and overlapping risk measures
    add_3 = result1 + result3
    # adding results with different portfolios and different risk measures
    add_4 = result1 + result5
    add_5 = result3 + result4

    # adding dates

    add_6 = result9 + result13
    add_7 = result11 + result13
    add_8 = result10 + result11
    add_9 = result9 + result10

    default_pivot_table_test(add_1, 'has_bucketed')
    default_pivot_table_test(add_2, 'has_bucketed')
    default_pivot_table_test(add_3, 'has_bucketed')
    default_pivot_table_test(add_4, 'has_bucketed')
    default_pivot_table_test(add_5, 'has_bucketed')
    default_pivot_table_test(add_6, 'dated')
    default_pivot_table_test(add_7, 'dated')
    default_pivot_table_test(add_8, 'dated')
    default_pivot_table_test(add_9, 'dated')

    # throw value error when adding results where at least one particular value is being calculated twice

    # adding results with same portfolio but overlapping risk measures
    with pytest.raises(ValueError):
        _ = result1 + result2

    # adding results with overlapping portfolios and different risk measures
    with pytest.raises(ValueError):
        _ = result2 + result4

    # adding results with overlapping portfolios and same risk measures
    with pytest.raises(ValueError):
        _ = result1 + result4

    # adding results with different scenarios
    with pytest.raises(ValueError):
        _ = result6 + result7
    with pytest.raises(ValueError):
        _ = result7 + result8

    # overlapping dates
    with pytest.raises(ValueError):
        _ = result9 + result11
    with pytest.raises(ValueError):
        _ = result10 + result13

    # adding results with different market locations
    with pytest.raises(ValueError):
        _ = result10 + result12
    with pytest.raises(ValueError):
        _ = result9 + result12
    with pytest.raises(ValueError):
        _ = result12 + result13
    with pytest.raises(ValueError):
        _ = result11 + result12


def test_unsupported_error_datums(mocker):
    with MockCalc(mocker):
        f1 = eur_port.calc(risk.IRAnnualImpliedVol).to_frame()
        _, _, f2 = get_attributes(swap_port1, risk.IRAnnualImpliedVol)
        _, _, f3 = get_attributes(swaption_port1, risk.IRAnnualImpliedVol)
        _, _, f4 = get_attributes(swaption_port3, risk.IRAnnualImpliedVol)

    # assert that unsupported datums do not appear to_frame()
    assert f1 is None
    assert all(f2['value'] == f3['value'])

    # assert that errorvalue appears in to_frame()
    assert isinstance(f4['value'].values[0], ErrorValue)


def test_resolution_of_error_trade(mocker):
    with MockCalc(mocker):
        error_trade = IRSwap(notional_currency='EUR', termination_date='10y', fixed_rate='bob')
        resolved_trade = error_trade.calc(ResolvedInstrumentValues)
        assert isinstance(resolved_trade, ErrorValue)

        try:
            _ = resolved_trade.fixed_rate  # this should fail
            assert 1 == 2
        except AttributeError as e:
            assert 'Error was' in str(e)


def test_resolve_to_frame(mocker):
    # makes sure resolving portfolio doesn't break to_frame
    with MockCalc(mocker):
        _, r1, f1 = get_attributes(eur_port, risk.Price, resolve=True)
        _, r2, f2 = get_attributes(port1, risk.Price, resolve=True)
        _, r3, f3 = get_attributes(jpy_port, risk.Price, 'RollFwd', resolve=True)
        _, r4, f4 = get_attributes(port1, risk.Price, 'CurveScen1', resolve=True)


def test_unnamed_portfolio(mocker):
    unnamed_1 = Portfolio((swap_1, swap_2))
    unnamed_2 = Portfolio((swap_3, swap_4))
    unnamed = Portfolio((unnamed_1, unnamed_2))
    with MockCalc(mocker):
        res = unnamed.calc(risk.IRFwdRate)
        df = res.to_frame()
        assert len(df) == 2
        assert list(df.index) == ['Portfolio_0', 'Portfolio_1']
        assert list(df.columns) == ['5y', '10y']


def test_leg_valuations(mocker):
    with MockCalc(mocker):
        # children legs return values
        _, r1, f1 = get_attributes(mcb, risk.FXSpot)

    assert isinstance(r1.futures[0].result(), DataFrameWithInfo)
    assert 'path' in f1.columns


def test_aggregation_with_heterogeous_types(mocker):
    with MockCalc(mocker):
        portfolio1 = Portfolio([IRSwaption('Pay', '10y', 'EUR', expiration_date='3m', name='EUR3m10ypayer')])
        portfolio2 = Portfolio([IRSwaption('Pay', '10y', 'EUR', expiration_date='6m', name='EUR6m10ypayer')])

        with PricingContext(csa_term='EUR-OIS', visible_to_gs=True):
            r1 = portfolio1.price()
        with PricingContext(csa_term='EUR-EuroSTR'):
            r2 = portfolio2.price()

        combined_result = r1 + r2

    with pytest.raises(ValueError):
        combined_result.aggregate()

    assert isinstance(combined_result.aggregate(allow_mismatch_risk_keys=True), float)


def test_aggregation_with_empty_measures(mocker):
    with MockCalc(mocker):
        swaptions = (IRSwaption(notional_currency='EUR', termination_date='7y', expiration_date='1y',
                                pay_or_receive='Receive', strike='ATM+35', name='EUR 1y7y'),
                     IRSwaption(notional_currency='EUR', termination_date='10y', expiration_date='2w',
                                pay_or_receive='Receive', strike='ATM+50', name='EUR 2w10y'))
        portfolio = Portfolio(swaptions)

        from_date = dt.date(2021, 11, 18)
        to_date = dt.date(2021, 11, 19)
        explain_2d = PnlExplain(CloseMarket(date=to_date))

        with PricingContext(pricing_date=from_date, visible_to_gs=True):
            portfolio.resolve()
            result_explain = portfolio.calc(explain_2d)

        total_risk = aggregate_risk(result_explain[explain_2d])['value'].sum()
        risk_swaption_1 = result_explain[0]['value'].sum()
        risk_swaption_2 = result_explain[1]['value'].sum()

        assert total_risk == risk_swaption_1 + risk_swaption_2


def test_filter_risk(mocker):
    with MockCalc(mocker):
        result = swap_1.calc(risk.IRDelta)

    coord = MarketDataCoordinate.from_string('IR_EUR_SWAP_5Y')

    df = result.filter_by_coord(coord)
    assert len(result) > 1
    assert len(df) == 1


def test_transformation(mocker):
    with MockCalc(mocker):
        ladder_res = usd_port.calc(risk.IRDelta)

    transformed_res = ladder_res.transform(ResultWithInfoAggregator())
    np.testing.assert_almost_equal(transformed_res.aggregate(), ladder_res.to_frame()['value'].sum())


def test_aggregation_with_identical_trades(mocker):
    with MockCalc(mocker):
        swaptions = (IRSwaption(notional_currency='EUR', termination_date='7y', expiration_date='1y',
                                pay_or_receive='Receive', strike='ATM+35', name='trade_1'),
                     IRSwaption(notional_currency='EUR', termination_date='7y', expiration_date='1y',
                                pay_or_receive='Receive', strike='ATM+35', name='trade_2'))
        portfolio = Portfolio(swaptions)

        delta = portfolio.calc(risk.IRDelta)
        transformed_res = delta.transform(ResultWithInfoAggregator())
        np.testing.assert_almost_equal(transformed_res.aggregate(), delta.to_frame()['value'].sum())


def test_scalar_with_info_on_instrument():
    # Historically there was a problem with setting risk results that were a scalar with info on an instrument
    # This was because of how copy.deepcopy would try and pickle/unpickle the class. This test checks that we can set
    # properties and still to_dict and _to_json the class
    risk_key = RiskKey("provider", "the_date", "mkt", RiskRequestParameters(), None, None)
    fwi = FloatWithInfo(risk_key, 1.56, )
    swi = StringWithInfo(risk_key, 'USD')

    swap = IRSwap(floating_rate_option=swi, fixed_rate=fwi)
    swap_dict = swap.to_dict()

    assert swap_dict["floatingRateOption"] == "USD"
    assert swap_dict["fixedRate"] == 1.56

    assert swap.to_json() is not None
