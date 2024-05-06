"""
Copyright 2024 Goldman Sachs.
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

import pandas as pd
import pytest

from gs_quant.errors import MqValueError
from gs_quant.markets.position_set import PositionSet, Position, GsPriceApi, PositionTag, PositionSetWeightingStrategy
import gs_quant.markets.position_set as position_set_module
from copy import deepcopy


def test_position_resolve_many(mocker):
    unresolved_position_sets = [
        PositionSet(date=dt.date(2024, 4, 30),
                    reference_notional=1000,
                    positions=[Position(identifier='GS UN',
                                        weight=0.5,
                                        tags=[PositionTag(name="tag1", value="tagvalue1")]),
                               Position(identifier='AAPL UW',
                                        weight=0.5,
                                        tags=[PositionTag(name="tag2", value="tagvalue2")])]),
        PositionSet(date=dt.date(2024, 5, 1),
                    reference_notional=1000,
                    positions=[Position(identifier='GS UN',
                                        weight=0.5,
                                        tags=[PositionTag(name="tag1", value="tagvalue1")]),
                               Position(identifier='AAPL UW',
                                        weight=0.5,
                                        tags=[PositionTag(name="tag2", value="tagvalue2")])])

    ]

    resolved_positions = [
        {"assetId": "MA4B66MW5E27UAHKG34", "name": "GS", "bbid": "GS UN", "tradingRestriction": True,
         "asOfDate": dt.datetime.strptime("2952-12-31", '%Y-%m-%d'),
         "startDate": dt.datetime.strptime("1952-01-01", '%Y-%m-%d'),
         "endDate": dt.datetime.strptime("2952-12-31", '%Y-%m-%d')},
        {"assetId": "MA4B66MW5E27U9VBB94", "name": "Apple", "bbid": "AAPL UW", "tradingRestriction": False,
         "asOfDate": dt.datetime.strptime("2952-12-31", '%Y-%m-%d'),
         "startDate": dt.datetime.strptime("1952-01-01", '%Y-%m-%d'),
         "endDate": dt.datetime.strptime("2952-12-31", '%Y-%m-%d')}
    ]

    xref_results = [
        {"assetId": "MA4B66MW5E27UAHKG34", "bbid": "GS UN", "delisted": 'no',
         "startDate": "1952-01-01", "endDate": "2952-12-31"},
        {"assetId": "MA4B66MW5E27U9VBB94", "bbid": "AAPL UW", "delisted": 'no',
         "startDate": "1952-01-01", "endDate": "2952-12-31"},
    ]

    mocker.patch.object(position_set_module, "_get_asset_temporal_xrefs",
                        return_value=(pd.DataFrame(xref_results), "bbid"))
    mocker.patch.object(position_set_module, "_resolve_many_assets", return_value=pd.DataFrame(resolved_positions))

    unresolved_position_sets_copy = deepcopy(unresolved_position_sets)
    PositionSet.resolve_many(unresolved_position_sets_copy)

    resolved_position_sets = [
        PositionSet(date=dt.date(2024, 4, 30),
                    reference_notional=1000,
                    positions=[Position(identifier='GS UN',
                                        asset_id="MA4B66MW5E27UAHKG34",
                                        name="GS",
                                        weight=0.5,
                                        tags=[PositionTag(name="tag1", value="tagvalue1")]),
                               Position(identifier='AAPL UW',
                                        asset_id="MA4B66MW5E27U9VBB94",
                                        name="Apple",
                                        weight=0.5,
                                        tags=[PositionTag(name="tag2", value="tagvalue2")])]),
        PositionSet(date=dt.date(2024, 5, 1),
                    reference_notional=1000,
                    positions=[Position(identifier='GS UN',
                                        asset_id="MA4B66MW5E27UAHKG34",
                                        name="GS",
                                        weight=0.5,
                                        tags=[PositionTag(name="tag1", value="tagvalue1")]),
                               Position(identifier='AAPL UW',
                                        asset_id="MA4B66MW5E27U9VBB94",
                                        name="Apple",
                                        weight=0.5,
                                        tags=[PositionTag(name="tag2", value="tagvalue2")])])
    ]

    for idx, pos_set in enumerate(unresolved_position_sets_copy):
        assert pos_set == resolved_position_sets[idx]

    # There are unresolved positions
    mocker.patch.object(position_set_module, "_get_asset_temporal_xrefs",
                        return_value=(pd.DataFrame([xref_results[1]]), "bbid"))
    mocker.patch.object(position_set_module, "_resolve_many_assets", return_value=pd.DataFrame([resolved_positions[1]]))

    unresolved_position_sets_copy = deepcopy(unresolved_position_sets)

    PositionSet.resolve_many(unresolved_position_sets_copy)

    expected_position_set = [
        PositionSet(date=dt.date(2024, 4, 30),
                    reference_notional=1000,
                    positions=[Position(identifier='AAPL UW',
                                        asset_id="MA4B66MW5E27U9VBB94",
                                        name="Apple",
                                        weight=0.5,
                                        tags=[PositionTag(name="tag2", value="tagvalue2")])],
                    unresolved_positions=[Position(identifier='GS UN',
                                                   name="GS",
                                                   weight=0.5,
                                                   tags=[PositionTag(name="tag1", value="tagvalue1")])]
                    ),
        PositionSet(date=dt.date(2024, 5, 1),
                    reference_notional=1000,
                    positions=[
                        Position(identifier='AAPL UW',
                                 asset_id="MA4B66MW5E27U9VBB94",
                                 name="Apple",
                                 weight=0.5,
                                 tags=[PositionTag(name="tag2", value="tagvalue2")])],
                    unresolved_positions=[Position(identifier='GS UN',
                                                   name="GS",
                                                   weight=0.5,
                                                   tags=[PositionTag(name="tag1", value="tagvalue1")])]
                    )
    ]

    unresolved_position_sets_copy.sort(key=lambda x: x.date)
    expected_position_set.sort(key=lambda x: x.date)

    for idx, position_set in enumerate(unresolved_position_sets_copy):
        assert position_set == expected_position_set[idx]
        assert len(position_set.unresolved_positions) == 1
        assert len(expected_position_set[idx].unresolved_positions) == 1

        actual_unresolved_position = position_set.unresolved_positions[0]
        expected_unresolved_position = expected_position_set[idx].unresolved_positions[0]
        assert actual_unresolved_position.__eq__(expected_unresolved_position)


@pytest.fixture()
def position_sets_with_tags_and_notional():
    return [
        PositionSet(date=dt.date(2024, 4, 30),
                    reference_notional=1000,
                    positions=[Position(identifier='GS UN',
                                        asset_id="MA4B66MW5E27UAHKG34",
                                        name="GS",
                                        weight=0.5,
                                        tags=[PositionTag(name="tag1", value="tagvalue1")]),
                               Position(identifier='AAPL UW',
                                        asset_id="MA4B66MW5E27U9VBB94",
                                        name="Apple",
                                        weight=0.5,
                                        tags=[PositionTag(name="tag2", value="tagvalue2")])]),
        PositionSet(date=dt.date(2024, 5, 1),
                    reference_notional=1000,
                    positions=[Position(identifier='GS UN',
                                        asset_id="MA4B66MW5E27UAHKG34",
                                        name="GS",
                                        weight=0.5,
                                        tags=[PositionTag(name="tag1", value="tagvalue1")]),
                               Position(identifier='AAPL UW',
                                        asset_id="MA4B66MW5E27U9VBB94",
                                        name="Apple",
                                        weight=0.5,
                                        tags=[PositionTag(name="tag2", value="tagvalue2")])])
    ]


@pytest.fixture()
def expected_position_pricing_result():
    return [{'date': '2024-04-30',
             'positions': [{'assetId': 'MA4B66MW5E27UAHKG34', 'weight': 0.42671,
                            'closePrice': 1000, 'fxClosePrice': 1, 'quantity': 1,
                            'notional': 1000, 'referenceWeight': 0.5},
                           {'assetId': 'MA4B66MW5E27U9VBB94', 'weight': 0.51099,
                            'closePrice': 1000, 'fxClosePrice': 1, 'quantity': 1,
                            'notional': 1000, 'referenceWeight': 0.5}], 'targetNotional': 1000},
            {'date': '2024-05-01',
             'positions': [{'assetId': 'MA4B66MW5E27UAHKG34', 'weight': 0.42671,
                            'closePrice': 1000, 'fxClosePrice': 1, 'quantity': 1,
                            'notional': 1000, 'referenceWeight': 0.5},
                           {'assetId': 'MA4B66MW5E27U9VBB94', 'weight': 0.51099,
                            'closePrice': 1000, 'fxClosePrice': 1, 'quantity': 1,
                            'notional': 1000, 'referenceWeight': 0.5}],
             'targetNotional': 1000}]


def test_position_price_many(mocker,
                             position_sets_with_tags_and_notional,
                             expected_position_pricing_result):
    # All positions on each holding date are priced

    mocker.patch.object(GsPriceApi, "price_many_positions",
                        return_value=expected_position_pricing_result)
    new_position_set_list = deepcopy(position_sets_with_tags_and_notional)
    PositionSet.price_many(new_position_set_list)

    expected_positions = {dt.date(2024, 4, 30): [Position(identifier='GS UN',
                                                          asset_id="MA4B66MW5E27UAHKG34",
                                                          name="GS",
                                                          weight=0.42671,
                                                          quantity=1,
                                                          tags=[PositionTag(name="tag1", value="tagvalue1")]),
                                                 Position(identifier='AAPL UW',
                                                          asset_id="MA4B66MW5E27U9VBB94",
                                                          name="Apple",
                                                          weight=0.51099,
                                                          quantity=1,
                                                          tags=[PositionTag(name="tag2", value="tagvalue2")])],
                          dt.date(2024, 5, 1): [Position(identifier='GS UN',
                                                         asset_id="MA4B66MW5E27UAHKG34",
                                                         name="GS",
                                                         weight=0.42671,
                                                         quantity=1,
                                                         tags=[PositionTag(name="tag1", value="tagvalue1")]),
                                                Position(identifier='AAPL UW',
                                                         asset_id="MA4B66MW5E27U9VBB94",
                                                         name="Apple",
                                                         weight=0.51099,
                                                         quantity=1,
                                                         tags=[PositionTag(name="tag2", value="tagvalue2")])]}

    [pos_set.positions.sort(key=lambda position: position.asset_id) for pos_set in new_position_set_list]
    [positions.sort(key=lambda position: position.asset_id) for positions in expected_positions.values()]

    for pos_set in new_position_set_list:
        assert pos_set.positions == expected_positions.get(pos_set.date)

    # weighting strategy passed is 'quantity' but positions do not have quantities
    with pytest.raises(MqValueError,
                       match="Unable to price positions without position weights and "
                             "daily reference notional or position quantities"):
        PositionSet.price_many(position_sets_with_tags_and_notional,
                               weighting_strategy=PositionSetWeightingStrategy.Quantity)

    # Invalid weighting strategies
    with pytest.raises(MqValueError,
                       match="Can only specify a weighting strategy of weight or quantity"):
        PositionSet.price_many(position_sets_with_tags_and_notional,
                               weighting_strategy=PositionSetWeightingStrategy.Market_Capitalization)

    # There are unpriced results
    mocker.patch.object(GsPriceApi, "price_many_positions",
                        return_value=[expected_position_pricing_result[1]])
    new_position_set_list = deepcopy(position_sets_with_tags_and_notional)
    PositionSet.price_many(new_position_set_list)

    first_position_set = new_position_set_list[0]
    positions = first_position_set.positions
    unpriced_positions = first_position_set.unpriced_positions

    assert not positions
    for position in unpriced_positions:
        if position.identifier == "GS UN":
            assert position.asset_id == "MA4B66MW5E27UAHKG34"
            assert position.weight == 0.5
            assert not position.quantity
            assert len(position.tags) == 1
            tag = position.tags[0]
            assert tag.name == "tag1"
            assert tag.value == "tagvalue1"

        else:
            assert position.asset_id == "MA4B66MW5E27U9VBB94"
            assert position.weight == 0.5
            assert not position.quantity
            assert len(position.tags) == 1
            tag = position.tags[0]
            assert tag.name == "tag2"
            assert tag.value == "tagvalue2"

    second_position_set = new_position_set_list[1]
    positions = second_position_set.positions
    unpriced_positions = second_position_set.unpriced_positions

    assert not unpriced_positions
    for position in positions:
        if position.identifier == "GS UN":
            assert position.asset_id == "MA4B66MW5E27UAHKG34"
            assert position.weight == 0.42671
            assert position.quantity == 1
            assert len(position.tags) == 1
            tag = position.tags[0]
            assert tag.name == "tag1"
            assert tag.value == "tagvalue1"

        else:
            assert position.asset_id == "MA4B66MW5E27U9VBB94"
            assert position.weight == 0.51099
            assert position.quantity == 1
            assert len(position.tags) == 1
            tag = position.tags[0]
            assert tag.name == "tag2"
            assert tag.value == "tagvalue2"

    # Positions do not have tags
    new_position_set_list = deepcopy(position_sets_with_tags_and_notional)
    position_sets_no_tags = [deepcopy(pos_set) for pos_set in new_position_set_list]
    for position_set_no_tag in position_sets_no_tags:
        [setattr(position, "tags", None) for position in position_set_no_tag.positions]

    mocker.patch.object(GsPriceApi, "price_many_positions",
                        return_value=expected_position_pricing_result)
    PositionSet.price_many(position_sets_no_tags)

    for position_set in position_sets_no_tags:
        priced_positions = position_set.positions
        for position in priced_positions:
            if position.identifier == "GS UN":
                assert position.asset_id == "MA4B66MW5E27UAHKG34"
                assert position.weight == 0.42671
                assert position.quantity == 1
                assert not position.tags

            else:
                assert position.asset_id == "MA4B66MW5E27U9VBB94"
                assert position.weight == 0.51099
                assert position.quantity == 1
                assert not position.tags

    # Positions with different tags and common underlying asset ID
    different_tags_common_asset_id_positions = [
        PositionSet(date=dt.date(2024, 4, 30),
                    reference_notional=1000,
                    positions=[Position(identifier='GS UN',
                                        asset_id="MA4B66MW5E27UAHKG34",
                                        name="GS",
                                        weight=0.5,
                                        tags=[PositionTag(name="tag1", value="tagvalue1")]),
                               Position(identifier='GS UN',
                                        asset_id="MA4B66MW5E27UAHKG34",
                                        name="GS",
                                        weight=-0.8,
                                        tags=[PositionTag(name="tag2", value="tagvalue2")]),
                               Position(identifier='AAPL UW',
                                        asset_id="MA4B66MW5E27U9VBB94",
                                        name="Apple",
                                        weight=0.5,
                                        tags=None)
                               ]
                    ),
        PositionSet(date=dt.date(2024, 5, 1),
                    reference_notional=1000,
                    positions=[Position(identifier='GS UN',
                                        asset_id="MA4B66MW5E27UAHKG34",
                                        name="GS",
                                        weight=0.5,
                                        tags=[PositionTag(name="tag1", value="tagvalue1")]),
                               Position(identifier='GS UN',
                                        asset_id="MA4B66MW5E27UAHKG34",
                                        name="GS",
                                        weight=-0.8,
                                        tags=[PositionTag(name="tag2", value="tagvalue2")]),
                               Position(identifier='AAPL UW',
                                        asset_id="MA4B66MW5E27U9VBB94",
                                        name="Apple",
                                        weight=0.5,
                                        tags=[PositionTag(name="tag3", value="tagvalue3")])
                               ]
                    )
    ]

    same_assets_different_weights_pricing_results = [
        {'date': '2024-04-30',
         'positions': [
             {'assetId': 'MA4B66MW5E27UAHKG34', 'weight': 0.38,
              'closePrice': 1000, 'fxClosePrice': 1, 'quantity': 1,
              'notional': 1000, 'referenceWeight': 0.5},
             {'assetId': 'MA4B66MW5E27UAHKG34', 'weight': -0.68,
              'closePrice': 1000, 'fxClosePrice': 1, 'quantity': -1.5,
              'notional': -1000, 'referenceWeight': -0.8},
             {'assetId': 'MA4B66MW5E27U9VBB94', 'weight': 0.41,
              'closePrice': 1000, 'fxClosePrice': 1, 'quantity': 1,
              'notional': 1000, 'referenceWeight': 0.5}],
         'targetNotional': 1000},
        {'date': '2024-05-01',
         'positions': [
             {'assetId': 'MA4B66MW5E27UAHKG34', 'weight': 0.42671,
              'closePrice': 1000, 'fxClosePrice': 1, 'quantity': 1,
              'notional': 1000, 'referenceWeight': 0.5},
             {'assetId': 'MA4B66MW5E27UAHKG34', 'weight': -0.72,
              'closePrice': 1000, 'fxClosePrice': 1, 'quantity': -1.5,
              'notional': -1000, 'referenceWeight': -0.8},
             {'assetId': 'MA4B66MW5E27U9VBB94', 'weight': 0.51099,
              'closePrice': 1000, 'fxClosePrice': 1, 'quantity': 1,
              'notional': 1000, 'referenceWeight': 0.5}],
         'targetNotional': 1000}
    ]
    mocker.patch.object(GsPriceApi, "price_many_positions",
                        return_value=same_assets_different_weights_pricing_results)
    PositionSet.price_many(different_tags_common_asset_id_positions)

    for position_set in different_tags_common_asset_id_positions:
        if position_set.date == dt.date(2024, 4, 30):
            for position in position_set.positions:
                if position.identifier == "GS UN":
                    assert position.asset_id == "MA4B66MW5E27UAHKG34"
                    assert position.name == "GS"
                    assert position.weight in [0.38, -0.68]
                    assert position.quantity in [1, -1.5]

                    if position.weight == 0.38:
                        assert position.tags[0] == PositionTag(name="tag1", value="tagvalue1")
                    else:
                        assert position.tags[0] == PositionTag(name="tag2", value="tagvalue2")
                else:
                    assert position.asset_id == "MA4B66MW5E27U9VBB94"
                    assert position.name == "Apple"
                    assert position.weight == 0.41
                    assert not position.tags

        else:
            for position in position_set.positions:
                if position.identifier == "GS UN":
                    assert position.asset_id == "MA4B66MW5E27UAHKG34"
                    assert position.name == "GS"
                    assert position.weight in [0.42671, -0.72]
                    assert position.quantity in [1, -1.5]

                    if position.weight == 0.42671:
                        assert position.tags[0] == PositionTag(name="tag1", value="tagvalue1")
                    else:
                        assert position.tags[0] == PositionTag(name="tag2", value="tagvalue2")
                else:
                    assert position.asset_id == "MA4B66MW5E27U9VBB94"
                    assert position.name == "Apple"
                    assert position.weight == 0.51099
                    assert position.tags[0] == PositionTag(name="tag3", value="tagvalue3")

    # There are empty positions in some position sets
    different_tags_common_asset_id_positions = [
        PositionSet(date=dt.date(2024, 4, 30),
                    reference_notional=1000,
                    positions=[]
                    ),
        PositionSet(date=dt.date(2024, 5, 1),
                    reference_notional=1000,
                    positions=[Position(identifier='GS UN',
                                        asset_id="MA4B66MW5E27UAHKG34",
                                        name="GS",
                                        weight=0.5,
                                        tags=[PositionTag(name="tag1", value="tagvalue1")]),
                               Position(identifier='GS UN',
                                        asset_id="MA4B66MW5E27UAHKG34",
                                        name="GS",
                                        weight=-0.8,
                                        tags=[PositionTag(name="tag2", value="tagvalue2")]),
                               Position(identifier='AAPL UW',
                                        asset_id="MA4B66MW5E27U9VBB94",
                                        name="Apple",
                                        weight=0.5,
                                        tags=[PositionTag(name="tag3", value="tagvalue3")])
                               ]
                    )
    ]

    mocker.patch.object(GsPriceApi, "price_many_positions",
                        return_value=[same_assets_different_weights_pricing_results[1]])

    PositionSet.price_many(different_tags_common_asset_id_positions)

    for position_set in different_tags_common_asset_id_positions:
        if position_set.date == dt.date(2024, 4, 30):
            assert not position_set.positions
            assert not position_set.unpriced_positions

        else:
            for position in position_set.positions:
                if position.identifier == "GS UN":
                    assert position.asset_id == "MA4B66MW5E27UAHKG34"
                    assert position.name == "GS"
                    assert position.weight in [0.42671, -0.72]
                    assert position.quantity in [1, -1.5]

                    if position.weight == 0.42671:
                        assert position.tags[0] == PositionTag(name="tag1", value="tagvalue1")
                    else:
                        assert position.tags[0] == PositionTag(name="tag2", value="tagvalue2")
                else:
                    assert position.asset_id == "MA4B66MW5E27U9VBB94"
                    assert position.name == "Apple"
                    assert position.weight == 0.51099
                    assert position.tags[0] == PositionTag(name="tag3", value="tagvalue3")

    # No positions have tags
    position_set_list_no_tags = deepcopy(position_sets_with_tags_and_notional)

    for pos_set in position_set_list_no_tags:
        [setattr(position, 'tags', None) for position in pos_set.positions]
    mocker.patch.object(GsPriceApi, "price_many_positions",
                        return_value=expected_position_pricing_result)
    PositionSet.price_many(position_set_list_no_tags)
    for position_set in position_set_list_no_tags:
        priced_positions = position_set.positions
        for position in priced_positions:
            if position.identifier == "GS UN":
                assert position.asset_id == "MA4B66MW5E27UAHKG34"
                assert position.name == "GS"
                assert position.weight == 0.42671
                assert position.quantity == 1
                assert not position.tags
            else:
                assert position.asset_id == "MA4B66MW5E27U9VBB94"
                assert position.name == "Apple"
                assert position.weight == 0.51099
                assert position.quantity == 1
                assert not position.tags
