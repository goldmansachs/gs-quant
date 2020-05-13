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
from gs_quant.api.gs.hedges import GsHedgeApi
import logging
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

_logger = logging.getLogger(__name__)


class Hedge:
    """
    A Marquee hedge.
    """

    @staticmethod
    def find_optimal_hedge(hedge_query: dict, hyperparams: dict, metric: str):
        """
        This function is designed to find the 'best' hedge from a list of hedges that are computed using a grid
        search over all hyperparameters passed in - where 'best' is defined by the metric argument passed in and
        whether we want to minimize or maximize this metric.

        :param hedge_query: dict, hedge data that is sent to the Marquee API as input to the new performance hedger
        :param hyperparams: dict, keys are hyperparameters (Lasso or Ridge) that map to lists of the values to use
                                  for one of these hyperparameters when running the new performance hedger.
        :param metric: str, the metric we want to optimize i.e. 'holdingError' or 'rSquared'
        :return: dict and float, the best hedge found using the algorithm and the value of the metric being
                                 optimized
        """
        hedge_results = {}
        opt_map = Hedge.create_optimization_mappings()
        optimization_type = opt_map[metric]
        print(f'We are trying to {optimization_type} {metric} and will return the optimized hedge & metric value...')
        hyperparam_grid = [(x, y) for x in hyperparams['Lasso'] for y in hyperparams['Ridge']]
        for pair in hyperparam_grid:
            hedge_params = hedge_query['parameters']
            hedge_params.lasso_weight, hedge_params.ridge_weight = pair[0], pair[1]
            hedge_query['parameters'] = hedge_params
            results = GsHedgeApi.calculate_hedge(hedge_query)
            print(f'Current Hedge is using the following values for Lasso/Ridge: {pair}')
            curr_results, curr_pair = results['result']['hedge'], pair
            hedge_results[curr_results[metric]] = (curr_results, curr_pair)
            print(f'Current Hedge value for {metric}: {curr_results[metric]}')
        optimized_metric = min(hedge_results.keys()) if optimization_type == 'minimize' else max(hedge_results.keys())
        optimized_hedge, optimized_hyperparams = hedge_results[optimized_metric][0], hedge_results[optimized_metric][1]
        print('******************************************************')
        print(f'The optimal pair of hyperparameters was {optimized_hyperparams}, achieving a value for {metric} '
              f'of {optimized_metric} during the out of sample period.')
        return optimized_hedge, optimized_metric

    @staticmethod
    def create_optimization_mappings() -> dict:
        """
        This function is designed to construct a mapping between metrics a user can choose to optimize when calling the
        New Performance Hedger and the way the metric should be optimized.

        :return: dict, the dictionary containing a mapping between metrics to optimize and how they should be optimized
        """
        opt_dict = {'rSquared': 'maximize', 'correlation': 'maximize', 'holdingError': 'minimize',
                    'trackingError': 'minimize', 'transactionCost': 'minimize', 'annualizedReturn': 'maximize'}
        return opt_dict

    @staticmethod
    def construct_portfolio_weights_and_asset_numbers(results: dict):
        """
        Function used to retrieve the constructed portfolio from a performance hedge, sort it, then calculate the
        weights for all assets and total number of assets and return these results.

        :param results: dict, the results of the performance hedge request made to the Marquee API
        :return: dict, list, list - the portfolio, portfolio weights, and number of assets
        """
        portfolio = results["result"]["hedge"]["constituents"]
        portfolio.sort(key=lambda x: x['weight'], reverse=True)
        weights = [asset['weight'] for asset in portfolio]
        asset_numbers = [i for i in range(len(portfolio))]
        return portfolio, weights, asset_numbers

    @staticmethod
    def plot_weights_against_number_of_assets(hedge_query: dict, hyperparams: dict, figsize: tuple = (18, 9)) -> \
            matplotlib.figure.Figure:
        """
        Function used to plot the effects that a particular hyperparameter (Lasso or Ridge) has
        on the results of a new performance hedge done through the Marquee API.

        :param hedge_query: dict, hedge data that is sent to the Marquee API as input to the new
                                  performance hedger
        :param hyperparams: dict, keys are hyperparameters (Lasso or Ridge) that map to lists of
                                  the values to use for one of these hyperparameters when running
                                  the new performance hedger. The hyperparameter not used will
                                  have a 'None' value.
        :param figsize: tuple, width and height of the plot in inches
        :return: matplotlib.figure.Figure - the figure of the plot (the top level container for
                                            all the plot elements)
        """
        lines = []
        hyperparam_to_plot = 'Lasso' if hyperparams['Lasso'] else 'Ridge'
        f, ax = plt.subplots(figsize=figsize)
        try:
            for i in range(len(hyperparams[hyperparam_to_plot])):
                hedge_params = hedge_query['parameters']
                if hyperparam_to_plot == 'Lasso':
                    hedge_params.lasso_weight = hyperparams[hyperparam_to_plot][i]
                else:
                    hedge_params.lasso_weight = 0
                if hyperparam_to_plot == 'Ridge':
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
            print(f'Constructing portfolio, weights, or asset numbers failed with {err} ... \
                  returning empty plot.')
        return f
