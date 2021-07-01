import os
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import pandas as pd
warnings.filterwarnings('ignore')


def persistXls(xls_report, path, filename, merge_cells=False, indentifier_marqueeid_map=pd.DataFrame()):
    xls_path = os.path.join(path, filename + '.xlsx')
    writer = pd.ExcelWriter(xls_path, options={'remove_timezone': True})
    for sheet, data in xls_report.items():
        data = pd.DataFrame(data)
        if 'assetId' in data.columns and len(indentifier_marqueeid_map) > 0:
            data = data.rename(columns={'assetId': 'marqueeid'}).merge(indentifier_marqueeid_map,
                                                                       how='left', on='marqueeid')
        pd.DataFrame(data).to_excel(writer, sheet, merge_cells=merge_cells)
    writer.save()
    writer.close()
    return xls_path


def plotGross(intraday, color_pal='Blues_r'):
    fig, ax = plt.subplots(figsize=(10, 4))
    pal = sns.color_palette(color_pal)
    intraday['gross'].plot.area(ax=ax, color=pal, alpha=0.4)
    ax.set_xlabel('Time/GMT')
    ax.set_title('Gross Remaining')
    ax.set_ylabel('Dollar')
    fig.tight_layout()


# Plot cost breakdown
def plotCost(intraday):
    intraday_cost = intraday.copy()
    initial_gross = intraday_cost.iloc[0].at['gross']
    intraday_cost = intraday_cost[1:]
    # convert to bps
    intraday_cost[['totalCostPermanent', 'totalCostSpread', 'totalCostVolatility']] /= initial_gross / 10000
    intraday_cost[['totalCostPermanent', 'totalCostSpread',
                   'totalCostVolatility']] = intraday_cost[['totalCostPermanent', 'totalCostSpread',
                                                            'totalCostVolatility']].cumsum()
    fig, ax = plt.subplots(figsize=(10, 4))
    pal = sns.color_palette('Blues_r')
    intraday_cost[['totalCostPermanent', 'totalCostSpread',
                   'totalCostVolatility']].plot.area(ax=ax, color=pal, alpha=0.4)
    ax.set_xlabel('Time/GMT')
    ax.set_title('Cost Contribution')
    ax.set_ylabel('Cost (bps)')
    fig.tight_layout()


# Plot Variance breakdown
def plotVar(intraday):
    initial_gross = intraday.iloc[0]['gross']
    risk_list = ['Factor', 'Specific', 'Diagonal']
    intraday = intraday.iloc[1:]
    for r in risk_list:
        intraday[r + 'Risk_bps^2'] = pow(10000 * intraday[r.lower() + 'Risk'] / initial_gross, 1)
    fig, ax = plt.subplots(figsize=(10, 4))
    pal = sns.color_palette('cubehelix', 8)
    intraday[['FactorRisk_bps^2', 'SpecificRisk_bps^2', 'DiagonalRisk_bps^2']].plot.area(ax=ax, color=pal, alpha=0.4)
    ax.legend(['Factor', 'Specific', 'Diagonal'], loc='upper right')
    ax.set_xlabel('Time/GMT')
    ax.set_title('Variance Contribution')
    ax.set_ylabel('Variance (bps)')
    fig.tight_layout()


# Plot Buy/Sell/Net
def plotBuySellNet(intraday):
    fig, ax = plt.subplots(figsize=(10, 4))
    (100 * intraday['buy'] / intraday['gross'].iloc[0]).plot(ax=ax, color=(0 / 235, 121 / 235, 114 / 235))
    (100 * intraday['sell'] / intraday['gross'].iloc[0]).plot(ax=ax, color=(142 / 235, 215 / 235, 205 / 235))
    (100 * intraday['net'] / intraday['gross'].iloc[0]).plot(ax=ax, color=(32 / 235, 189 / 235, 168 / 235))
    ax.axhline(linestyle='--')
    ax.set_xlabel('Time/GMT')
    ax.set_title('Buy/Sell/Net(%)')
    ax.set_ylabel('Dollar')
    fig.tight_layout()


def plotGrossRemaining(intraday):
    fig, ax = plt.subplots(figsize=(10, 4))
    (100 * intraday['gross'] / intraday['gross'].iloc[0]).plot(ax=ax, color="DarkBlue")
    ax.set_xlabel('Time/GMT')
    ax.set_title('Gross(%,LHS) and Participation Rate (%,RHS)')
    ax.set_ylabel('%')
    ax2 = ax.twinx()
    intraday['advAveragePercentage'].rolling('220min').mean().plot(ax=ax2, color='grey', style='--')
    fig.tight_layout()


# function defined to plot three metrics every run
def plotMultiStrategyPortfolioLevelAnalytics(results_dict_multi, metrics_list, title, ylabel, color_pal='Blues_r',
                                             urgency_list=['VERY_LOW', 'LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH']):
    agg_result = [pd.DataFrame(results_dict_multi[u]
                               ['analytics']['portfolioAnalyticsIntraday'])[metrics_list + ['time',
                                                                                            'gross', 'tradeDayNumber']]
                  .assign(urgency=u).assign(time=lambda x: pd.to_datetime(x['time']))
                  .set_index('time').pipe(lambda df: df[df['tradeDayNumber'] == 1]) for u in urgency_list]
    initial_gross = agg_result[0].iloc[0]['gross']
    fig, [ax1, ax2, ax3, ax4] = plt.subplots(4, 1, sharex=True, figsize=(10, 12))
    for m, ax, t, y in zip(metrics_list, [ax1, ax2, ax3, ax4], title, ylabel):
        df_plot = pd.concat(agg_result).reset_index().set_index(['time',
                                                                 'urgency'])[m].unstack().reindex(columns=urgency_list)
        df_plot = df_plot[1:]
        if m == 'totalCost':
            df_plot /= initial_gross / 10000
            df_plot = df_plot.cumsum()
        elif m == 'advAveragePercentage':
            df_plot = df_plot.rolling('120min').mean()
        df_plot.plot(ax=ax, alpha=0.5)
        ax.legend(urgency_list, loc='right')
        ax.set_xlabel('Time/GMT')
        ax.set_title(t)
        ax.set_ylabel(y)
    fig.tight_layout()
