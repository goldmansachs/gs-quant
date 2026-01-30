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
from typing import Tuple, List, Dict

from gs_quant.session import GsSession
from gs_quant.target.hedge import Hedge
from gs_quant.target.hedge import PerformanceHedgeParameters, ClassificationConstraint, AssetConstraint, Target

_logger = logging.getLogger(__name__)
CALCULATION_TIMEOUT = 180


class GsHedgeApi:
    """GS Hedge API client implementation"""

    @classmethod
    def get_many_hedges(cls, ids: List[str] = None, names: List[str] = None, limit: int = 100):
        url = f'/hedges?limit={limit}'
        if ids:
            url += f'&id={"&id=".join(ids)}'
        if names:
            url += f'&name={"&name=".join(names)}'
        return GsSession.current._get(url, cls=Hedge)

    @classmethod
    def create_hedge(cls, hedge: Dict) -> Hedge:
        return GsSession.current._post('/hedges', hedge, cls=Hedge)

    @classmethod
    def get_hedge(cls, hedge_id: str) -> Hedge:
        return GsSession.current._get(f'/hedges/{hedge_id}', cls=Hedge)

    @classmethod
    def get_hedge_data(cls, ids: List[str] = None, names: List[str] = None, limit: int = 100) -> List[Dict]:
        url = f'/hedges/data?limit={limit}'
        if ids:
            url += f'&id={"&id=".join(ids)}'
        if names:
            url += f'&name={"&name=".join(names)}'
        return GsSession.current._get(url, cls=Hedge)['results']

    @classmethod
    def get_hedge_results(cls, hedge_id: str, start_date: dt.date = None, end_date: dt.date = None) -> Dict:
        url = f'/hedges/results?id={hedge_id}'
        if start_date is not None:
            url += f'&startDate={start_date.strftime("%Y-%m-%d")}'
        if end_date is not None:
            url += f'&endDate={end_date.strftime("%Y-%m-%d")}'
        return GsSession.current._get(url)['results'][0]

    @classmethod
    def update_hedge(cls, hedge_id: str, hedge: Hedge) -> Hedge:
        return GsSession.current._put(f'/hedges/{hedge_id}', hedge, cls=Hedge)

    @classmethod
    def delete_hedge(cls, hedge_id: str):
        return GsSession.current._delete(f'/hedges/{hedge_id}', cls=Hedge)

    @classmethod
    def construct_performance_hedge_query(
        cls,
        hedge_target: str,
        universe: Tuple[str, ...],
        notional: float,
        observation_start_date: dt.date,
        observation_end_date: dt.date,
        backtest_start_date: dt.date,
        backtest_end_date: dt.date,
        use_machine_learning: bool = False,
        lasso_weight: float = None,
        ridge_weight: float = None,
        max_return_deviation: float = 5,
        max_adv_percentage: float = 15,
        max_leverage: float = 100,
        max_weight: float = 100,
        min_market_cap: float = None,
        max_market_cap: float = None,
        asset_constraints: Tuple[AssetConstraint, ...] = None,
        benchmarks: Tuple[str, ...] = None,
        classification_constraints: Tuple[ClassificationConstraint, ...] = None,
        exclude_corporate_actions: bool = False,
        exclude_corporate_actions_types: Tuple = None,
        exclude_hard_to_borrow_assets: bool = False,
        exclude_restricted_assets: bool = False,
        exclude_target_assets: bool = True,
        explode_universe: bool = True,
        market_participation_rate: float = 10,
        sampling_period: str = 'Daily',
    ) -> dict:
        """
        Function to construct a performance hedge query (for both the New Performance Hedger and Standard Hedger)
        by passing in required/optional arguments similar to the performance hedger on the Marquee UI.

        :param hedge_target: str, the target asset we hedge - in Marquee ID (MQID) form
        :param universe: Tuple[str, ...], the universe(s) used to create the hedge - in Marquee ID (MQID) form
        :param notional: float, the total notional dollar amount of the single asset to hedge
        :param observation_start_date: datetime.date, the observation start date of the hedge specified in datetime
                                                      form
        :param observation_end_date: datetime.date, the observation end date of the hedge specified in datetime form
        :param backtest_start_date: datetime.date, the backtest start date of the hedge specified in datetime
                                                   form
        :param backtest_end_date: datetime.date, the backtest end date of the hedge specified in datetime form
        :param use_machine_learning: bool, whether to run the New Performance Hedger or Standard Hedger
        :param lasso_weight: float, the value of Concentration (Lasso) include in the hedge if using the New Performance
                                    Hedger
        :param ridge_weight: float, the value of Diversity (Ridge) include in the hedge if using the New Performance
                                    Hedger
        :param max_return_deviation: float, the maximum amount that a hedge portfolio's returns can deviate from the
                                            target asset returns, as a percentage
        :param max_adv_percentage: float, the maximum trading liquidity of each asset in the hedge portfolio, as a
                                          percentage
        :param max_leverage: float, the maximum amount of equity used to construct the hedge, as a percentage (i.e.
                                    if equal to 60, then 60% equity and 40% cash are used)
        :param max_weight: float, the maximum weight that any individual asset can hold in the hedge portfolio
        :param min_market_cap: float, the minimum market cap to filter assets chosen in the hedge portfolio by
        :param max_market_cap: float, the maximum market cap to filter assets chosen in the hedge portfolio by
        :param asset_constraints: Tuple[AssetConstraint, ...], constraints on individual assets to limit how much weight
                                                               they can contribute in the hedge portfolio (i.e.
                                                               [{assetId: "MA4B66MW5E27UAL9SUX", min: 0.01, max: 100}])
        :param benchmarks: Tuple[str, ...], benchmarks to compare the hedge against
        :param classification_constraints: Tuple[ClassificationConstraint, ...], constraints on classifications such as
                                           Sector/Industry/etc. (i.e [{type: "Sector", min: 0, max: 38, name: "Energy"},
                                           …])
        :param exclude_corporate_actions: bool, whether to exclude assets in the hedge portfolio that have pending
                                                corporate actions (such as a merger)
        :param exclude_corporate_actions_types: Tuple[Union[CorporateActionsTypes, str], ...], if excluding assets with
                                                corporate actions, this includes all of the types of corporate actions
                                                (i.e. ["Mergers", "Spinoffs", "Reorganization"])
        :param exclude_hard_to_borrow_assets: bool, whether to exclude assets in the hedge portfolio that are harder
                                                    to borrow
        :param exclude_restricted_assets: bool, whether to exclude assets in the hedge portfolio that are considered
                                              restricted companies
        :param exclude_target_assets: bool, whether to exclude to the target asset in the hedge portfolio (important
                                          to leave this as true for a valid hedge)
        :param explode_universe: bool, whether to explode the underlying universe into its constituents in the hedge
        :param market_participation_rate: float, the percentage of market to use to incur transaction costs, used by
                                               Marquee
        :param sampling_period: str, the sampling period to use (i.e. 'Daily' or 'Weekly')
        :return: dict, the hedge query represented by a dictionary of inputs
        """
        hedge_dict = {
            'objective': 'Replicate Performance',
            'parameters': PerformanceHedgeParameters(
                Target(id=hedge_target),
                universe,
                notional,
                observation_start_date,
                observation_end_date,
                max_leverage,
                backtest_start_date,
                backtest_end_date,
                sampling_period,
                exclude_target_assets,
                exclude_corporate_actions,
                exclude_corporate_actions_types,
                exclude_hard_to_borrow_assets,
                exclude_restricted_assets,
                max_adv_percentage,
                explode_universe,
                max_return_deviation,
                max_weight,
                min_market_cap,
                max_market_cap,
                market_participation_rate,
                asset_constraints,
                classification_constraints,
                benchmarks,
                use_machine_learning,
                lasso_weight,
                ridge_weight,
            ),
        }
        return hedge_dict

    @classmethod
    def calculate_hedge(cls, hedge_query: dict) -> dict:
        """
        This function is designed to take in a performance hedge query and then return the hedge results (in the
        form of a dictionary) from calling the performance hedger API.

        :param hedge_query: dict, hedge data that is sent to the Marquee API as input to the performance hedger
        :return: dict, the results of calling the Marquee performance hedger
        """
        return GsSession.current._post('/hedges/calculations', payload=hedge_query, timeout=CALCULATION_TIMEOUT)

    @classmethod
    def share_hedge_group(
        cls,
        hedge_group_id: str,
        strategy_request: Dict,
        optimization_response: Dict,
        hedge_name: str = "Custom Hedge",
        group_name: str = "New Hedge Group",
        view_emails: List[str] = None,
        admin_emails: List[str] = None,
    ) -> Dict:
        """
        Share a saved hedge group with other users by updating entitlements using email addresses.

        :param hedge_group_id: The ID of the hedge group to share (from save response)
        :param strategy_request: The strategy_as_dict from run() - the request payload sent to optimizer
        :param optimization_response: The optimization_results from run() - the response from optimizer
        :param hedge_name: Name for the individual hedge
        :param group_name: Name for the hedge group
        :param view_emails: List of user email addresses to grant view access
        :param admin_emails: List of user email addresses to grant admin access
        :return: API response with updated entitlements

        Example:
            >>> from gs_quant.api.gs.hedges import GsHedgeApi
            >>> response = GsHedgeApi.share_hedge_group(
            ...     hedge_group_id="HEDGE123",
            ...     strategy_request=strategy_request,
            ...     optimization_response=optimization_response,
            ...     hedge_name="Factor Hedge",
            ...     group_name="My Hedge Group",
            ...     view_emails=["user1@example.com", "user2@example.com"]
            ... )
        """
        from gs_quant.entities.entitlements import User

        url = f"/hedges/groups/{hedge_group_id}"

        try:
            # First, GET the current hedge group to retrieve existing metadata
            hedge_group_data = GsSession.current._get(url)

            # Get current user's GUID from existing entitlements
            current_user_guid = hedge_group_data.get('ownerId', '')
            if current_user_guid:
                current_user_guid = f"guid:{current_user_guid}"

            # Build updated entitlements, preserving owner's access
            entitlements = hedge_group_data.get('entitlements', {})

            # Ensure owner always has access
            if current_user_guid:
                # Admin access
                if 'admin' not in entitlements:
                    entitlements['admin'] = []
                if current_user_guid not in entitlements['admin']:
                    entitlements['admin'].append(current_user_guid)

                # Edit access
                if 'edit' not in entitlements:
                    entitlements['edit'] = []
                if current_user_guid not in entitlements['edit']:
                    entitlements['edit'].append(current_user_guid)

                # View access
                if 'view' not in entitlements:
                    entitlements['view'] = []
                if current_user_guid not in entitlements['view']:
                    entitlements['view'].append(current_user_guid)

            # Convert emails to user GUIDs and add view access
            if view_emails:
                view_users = User.get_many(emails=view_emails)
                for user in view_users:
                    user_guid = f"guid:{user.id}"
                    if user_guid not in entitlements['view']:
                        entitlements['view'].append(user_guid)

            # Convert emails to user GUIDs and add admin access (admin users also need edit and view access)
            if admin_emails:
                admin_users = User.get_many(emails=admin_emails)
                for user in admin_users:
                    user_guid = f"guid:{user.id}"
                    if user_guid not in entitlements['admin']:
                        entitlements['admin'].append(user_guid)
                    if user_guid not in entitlements['edit']:
                        entitlements['edit'].append(user_guid)
                    if user_guid not in entitlements['view']:
                        entitlements['view'].append(user_guid)

            # Build the complete payload with updated entitlements
            payload = {
                "active": True,
                "entitlements": entitlements,
                "hedges": [
                    {
                        "entitlements": entitlements,
                        "id": hedge_group_data.get('hedgeIds', [])[0] if hedge_group_data.get('hedgeIds') else None,
                        "name": hedge_name,
                        "objective": strategy_request.get("objective", "Minimize Factor Risk"),
                        "parameters": strategy_request.get("parameters", {}),
                        "result": optimization_response.get("result", {}),
                    }
                ],
                "id": hedge_group_id,
                "name": group_name,
                "objective": strategy_request.get("objective", "Minimize Factor Risk"),
                "ownerId": hedge_group_data.get('ownerId', ''),
                "createdById": hedge_group_data.get('createdById', ''),
                "createdTime": hedge_group_data.get('createdTime', ''),
                "lastUpdatedById": hedge_group_data.get('lastUpdatedById', ''),
                "lastUpdatedTime": hedge_group_data.get('lastUpdatedTime', ''),
                "hedgeIds": hedge_group_data.get('hedgeIds', []),
            }

            # PUT the updated hedge group back
            result = GsSession.current._put(url, payload)

            print("Hedge group shared successfully!")
            print(f"  Hedge Group ID: {hedge_group_id}")
            print("\n  Updated Entitlements:")
            print(f"    View Access: {len(result.get('entitlements', {}).get('view', []))} users/groups")
            print(f"    Admin Access: {len(result.get('entitlements', {}).get('admin', []))} users/groups")

            return result

        except Exception as e:
            print(f"Failed to share hedge: {e}")
            raise

            print("Hedge group shared successfully!")
            print(f"  Hedge Group ID: {hedge_group_id}")
            print("\n  Updated Entitlements:")
            print(f"    View Access: {len(result.get('entitlements', {}).get('view', []))} users/groups")
            print(f"    Admin Access: {len(result.get('entitlements', {}).get('admin', []))} users/groups")

            return result

        except Exception as e:
            print(f"✗ Failed to share hedge: {e}")
            raise
