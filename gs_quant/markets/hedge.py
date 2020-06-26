"""
Copyright 2019 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicablNe law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""
from collections import defaultdict

from gs_quant.api.gs.hedges import GsHedgeApi
import logging
from typing import Union, List
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

_logger = logging.getLogger(__name__)


class Hedge:
    """
    A Marquee hedge.
    """

    @staticmethod
    def find_optimal_hedge(hedge_query: dict, hyperparams: dict, metric: str) -> \
            Union[dict, float]:
        """
        This function is designed to find the 'best' hedge from a list of hedges that are computed using a grid
        search over all hyperparameters passed in - where 'best' is defined by the metric argument passed in and
        whether we want to minimize or maximize this metric.

        :param hedge_query: dict, hedge data that is sent to the Marquee API as input to the new performance hedger
        :param hyperparams: dict, keys are hyperparameters (Concentration or Diversity) that map to lists of the values
                                  to use for one of these hyperparameters when running the new performance hedger.
        :param metric: str, the metric we want to optimize i.e. 'holdingError' or 'rSquared'
        :return: dict, float, and tuple, the best hedge found using the algorithm, the value of the metric being
                                 optimized, and the tuple of optimal hyperparameters
        """
        hedge_results = {}
        opt_map = Hedge.create_optimization_mappings()
        optimization_type = opt_map[metric]
        _logger.info(f'We are trying to {optimization_type} {metric} and will return the optimized hedge & '
                     f'metric value...')
        hyperparam_grid = [(x, y) for x in hyperparams['Concentration'] for y in hyperparams['Diversity']]
        for pair in hyperparam_grid:
            hedge_params = hedge_query['parameters']
            hedge_params.lasso_weight, hedge_params.ridge_weight = pair[0], pair[1]
            hedge_query['parameters'] = hedge_params
            results = GsHedgeApi.calculate_hedge(hedge_query)
            _logger.info(f'Current Hedge is using the following values for Concentration/Diversity: {pair}')
            curr_results, curr_pair = results['result']['hedge'], pair
            hedge_results[curr_results[metric]] = (curr_results, curr_pair)
            _logger.info(f'Current Hedge value for {metric}: {curr_results[metric]*100:.3}%')
        optimized_metric = min(hedge_results.keys()) if optimization_type == 'minimize' else max(hedge_results.keys())
        optimized_hedge, optimized_hyperparams = hedge_results[optimized_metric][0], hedge_results[optimized_metric][1]
        return optimized_hedge, optimized_metric, optimized_hyperparams

    @staticmethod
    def create_optimization_mappings() -> dict:
        """
        This function is designed to construct a mapping between metrics a user can choose to optimize when calling the
        New Performance Hedger and the way the metric should be optimized.

        :param none:
        :return: dict, the dictionary containing a mapping between metrics to optimize and how they should be optimized
        """
        opt_dict = {'rSquared': 'maximize', 'correlation': 'maximize', 'holdingError': 'minimize',
                    'trackingError': 'minimize', 'transactionCost': 'minimize', 'annualizedReturn': 'maximize'}
        return opt_dict

    @staticmethod
    def construct_portfolio_weights_and_asset_numbers(results: dict) -> Union[dict, List]:
        """
        Function used to retrieve the constructed portfolio from a performance hedge, sort it, then calculate the
        weights for all assets and total number of assets and return these results.

        :param results: dict, the results of the performance hedge request made to the Marquee API
        :return: dict, list, list - the portfolio, portfolio weights, and number of assets
        """
        portfolio = results["result"]["hedge"]["constituents"]
        portfolio.sort(key=lambda x: x['weight'], reverse=True)
        weights = [asset['weight'] for asset in portfolio]
        asset_numbers = list(range(len(portfolio)))
        return portfolio, weights, asset_numbers

    @staticmethod
    def plot_weights_against_number_of_assets(hedge_query: dict, hyperparams: dict, figsize: tuple = (18, 9)) -> \
            matplotlib.figure.Figure:
        """
        Function used to plot the effects that a particular hyperparameter (Concentration or Diversity) has
        on the results of a new performance hedge done through the Marquee API.

        :param hedge_query: dict, hedge data that is sent to the Marquee API as input to the new
                                  performance hedger
        :param hyperparams: dict, keys are hyperparameters (Concentration or Diversity) that map to lists of
                                  the values to use for one of these hyperparameters when running
                                  the new performance hedger. The hyperparameter not used will
                                  have a 'None' value.
        :param figsize: tuple, width and height of the plot in inches
        :return: matplotlib.figure.Figure - the figure of the plot (the top level container for
                                            all the plot elements)
        """
        lines = []
        hyperparam_to_plot = 'Concentration' if hyperparams['Concentration'] else 'Diversity'
        f, ax = plt.subplots(figsize=figsize)
        try:
            for i in range(len(hyperparams[hyperparam_to_plot])):
                hedge_params = hedge_query['parameters']
                if hyperparam_to_plot == 'Concentration':
                    hedge_params.lasso_weight = hyperparams[hyperparam_to_plot][i]
                else:
                    hedge_params.lasso_weight = 0
                if hyperparam_to_plot == 'Diversity':
                    hedge_params.ridge_weight = hyperparams[hyperparam_to_plot][i]
                else:
                    hedge_params.ridge_weight = 0
                hedge_query['parameters'] = hedge_params
                results = GsHedgeApi.calculate_hedge(hedge_query)
                portfolio, weights, asset_numbers = Hedge.construct_portfolio_weights_and_asset_numbers(results)
                x_ind = np.arange(len(asset_numbers))
                bar = ax.bar(x_ind, weights, align='center', alpha=0.6)
                lines.append(bar)
            plt.legend(lines, [hyperparam_to_plot + ' Percentage: ' + str(i) for i in
                               hyperparams[hyperparam_to_plot]], prop={'size': 18})
            plt.xlabel('Number of Assets', size=13)
            plt.ylabel('Weights', size=13)
            plt.title('Analyzing the effects of the ' + hyperparam_to_plot + ' hyperparameter on a hedge', size=22)
            plt.show()
        except Exception as err:
            _logger.warning(f'Constructing portfolio, weights, or asset numbers failed with {err} ... \
                  returning empty plot.')
        return f

    @staticmethod
    def asset_id_diffs(portfolio_asset_ids, thomson_reuters_asset_ids):
        """
        Function designed to find the assets that are contained in the portfolio but that we don't have
        Thomson Reuters data for.

        :param portfolio_asset_ids: list, the list of MQIDs representing all of the assets that we are computing
                                          rebalance costs for
        :param thomson_reuters_asset_ids: list, the list of MQIDs representing all of the assets that we have Thomson
                                                Reuters data for
        :return: list, the assets that we don't have Thomson Reuters data for and should exclude in the transaction cost
                       calculations
        """
        diffs = list(set(portfolio_asset_ids) - set(thomson_reuters_asset_ids))
        return diffs

    @staticmethod
    def create_transaction_cost_data_structures(portfolio_asset_ids, portfolio_quantities, thomson_reuters_eod_data,
                                                backtest_dates):
        """
        Function designed to create the data structures necessary to compute transaction costs based on rebalancing a
        portfolio of assets.

        :param portfolio_asset_ids: list, the asset_ids for each asset in the underlying portfolio that we want to
                                          compute transaction costs for
        :param portfolio_quantities: list, the number of shares for each asset in the underlying portfolio that we want
                                           to compute transaction costs for
        :param thomson_reuters_eod_data: Dataset, the data used to fetch prices for assets - in this case from Thomson
                                                  Reuters
        :param backtest_dates: list, the dates that the portfolio is held for (that we want to compute rebalance costs
                                     for)
        :return: Union[list, dict, ...], the data structures necessary for computing transaction (rebalance) costs
        """
        thomson_reuters_asset_ids = [asset_id for asset_id in thomson_reuters_eod_data.get_data(
            backtest_dates[-1], backtest_dates[-1], assetId=portfolio_asset_ids)['assetId']]
        diffs = Hedge.asset_id_diffs(portfolio_asset_ids, thomson_reuters_asset_ids)
        for diff in diffs:
            portfolio_asset_ids.remove(diff)

        # Map asset_id to quantity of shares from portfolio, while excluding assets that are found in the diffs since
        # there is no Thomson Reuters data on them
        id_quantity_map = {}
        for idx, asset_id in enumerate(portfolio_asset_ids):
            if asset_id not in diffs:
                id_quantity_map[asset_id] = portfolio_quantities[idx]

        # Map asset_id to list of prices of that asset over the transaction_cost_dates we want
        id_prices_map = defaultdict(lambda: list())
        prices_df = pd.DataFrame()
        for date in backtest_dates:
            data = thomson_reuters_eod_data.get_data(date, date, assetId=portfolio_asset_ids)
            prices_df = prices_df.append(data)
        for asset_id in portfolio_asset_ids:
            id_prices_map[asset_id] = list(prices_df.loc[prices_df['assetId'] == asset_id]['closePrice'])

        # Create list representing notional of each day in transaction_cost_days and map asset_ids to notional of each
        # asset on each day
        id_to_notional_map = {}
        notionals_assets = [abs(np.asarray(id_prices_map[asset_id]) * id_quantity_map[asset_id]) for asset_id in
                            portfolio_asset_ids]
        # Mapping asset_id to notionals of each day of that asset_id
        for idx, asset_id in enumerate(portfolio_asset_ids):
            id_to_notional_map[asset_id] = list(notionals_assets[idx])
        total_notionals_each_day = list(np.sum(notionals_assets, axis=0))

        # Create map of asset_ids to weights of total portfolio on each day
        id_to_weight_map = {}
        for idx, asset_id in enumerate(portfolio_asset_ids):
            id_to_weight_map[asset_id] = [i / j for i, j in
                                          zip(id_to_notional_map[portfolio_asset_ids[idx]], total_notionals_each_day)]
        return id_quantity_map, id_prices_map, id_to_notional_map, id_to_weight_map

    @staticmethod
    def t_cost(basis_points, notional_traded):
        """
        Function designed to compute the transaction costs associated with trading a notional
        amount of an asset to rebalance a portfolio.

        :param basis_points: float, the number of basis points to use as an approximation when computing transaction
                                    costs to trade each asset that is rebalanced and that will be converted to a
                                    percentage (e.g. 20.43)
        :param notional_traded: float, notional amount of the asset that is being traded to rebalance the portfolio
        :return: float, the total transaction cost of trading a particular notional amount of an asset
        """
        return (basis_points * 1e-4) * notional_traded

    @staticmethod
    def compute_notional_traded(notional_on_the_day, prev_weight, curr_weight):
        """
        Function used to compute the notional amount (USD) of an asset that will be traded on a particular day, using
        the weights of the asset from the previous day and the weights & notional from the current day.

        :param notional_on_the_day: float, notional amount of the asset that the portfolio contains on the current day
        :param prev_weight: float, the weighting of the corresponding asset (of the entire portfolio) on the previous
                                   day
        :param curr_weight: float, the weighting of the corresponding asset (of the entire portfolio) on the current day
        :return: float, the net notional amount of the asset traded on the current day
        """
        return sum([np.abs(curr_weight - prev_weight) * notional_on_the_day])

    @staticmethod
    def compute_tcosts(basis_points, asset_weights, asset_notionals, backtest_dates, portfolio_asset_ids):
        """
        Function to compute cumulative transaction costs associated with rebalancing a portfolio. In particular, for
        each day on which we compute the cumulative the rebalancing costs (USD), the weights of the constituents of the
        portfolio on the previous day are used to calculate how much of the notional amount of each asset is traded to
        execute the rebalance.

        :param basis_points: float, the number of basis points to use as an approximation when computing transaction
                                    costs to trade each asset that is rebalanced and that will be converted to a
                                    percentage (e.g. 20.43)
        :param asset_weights: dict, the dictionary mapping of asset_ids (MQIDs) to a list of weights where each weight
                                    represents the weighting of the corresponding asset (of the entire portfolio) on
                                    each day in the backtest period
        :param asset_notionals: dict, the dictionary mapping of asset_ids (MQIDs) to a list of floats where each float
                                      represents the notional amount of the corresponding asset (of the entire
                                      portfolio) on each day in the backtest period
        :param backtest_dates: list, the dates that the portfolio is held for (that we want to compute rebalance costs
                                     for)
        :param portfolio_asset_ids: list, the list of MQIDs representing all of the assets that we are computing
                                          rebalancing costs for
        :return: pd.Series, the cumulative transaction costs associated with rebalancing the portfolio across the
                            backtest period
        """
        tcosts_each_day = []
        for idx, date in enumerate(backtest_dates):
            tcost_today = 0
            for asset_id in portfolio_asset_ids:
                prev_weights = asset_weights[asset_id][0] if idx == 0 else asset_weights[asset_id][idx - 1]
                notional_on_the_day, curr_weights = asset_notionals[asset_id][idx], asset_weights[asset_id][idx]
                notional_to_trade = Hedge.compute_notional_traded(notional_on_the_day, prev_weights, curr_weights)
                transaction_cost = Hedge.t_cost(basis_points, notional_to_trade)
                tcost_today += transaction_cost
            tcosts_each_day.append(abs(tcost_today))
        cum_tcosts = pd.Series(np.cumsum(tcosts_each_day))
        return cum_tcosts

    @staticmethod
    def plot_transaction_costs_of_rebalancing(cumulative_transaction_costs, backtest_dates, figsize=(10, 6)):
        """
        Function used to plot the cumulative transaction costs associated with rebalancing a hedge. The plot axes
        include the backtest dates on the x-axis and the cumulative transaction costs (USD) on the y-axis.

        :param cumulative_transaction_costs: pd.Series, the cumulative transaction costs over the backtest period
        :param backtest_dates: list, the dates that the portfolio is held for (that we want to compute rebalance costs
                                     for)
        :param figsize: tuple, width and height of the plot in inches
        :return:
        """
        indices = [x for x in range(len(backtest_dates))]
        ax_costs = cumulative_transaction_costs.plot(figsize=figsize, linewidth=3)
        ax_costs.legend(['Weights-Based Performance Hedger'])
        plt.ylabel('Cumulative Costs (USD)', size=13)
        plt.xlabel('Backtest Period', size=13)
        plt.xticks(indices, backtest_dates, rotation='vertical', size=13)
        plt.title('Cumulative Costs to Rebalance Weights-Based Performance Hedger', size=22)
        plt.legend(labels=['Weights-Based Performance Hedger'], prop={'size': 18})
