"""
Copyright 2021 Goldman Sachs.
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
from gs_quant.markets.report import PerformanceReport
from gs_quant.models.risk_model import MacroRiskModel, DataAssetsRequest, RiskModelUniverseIdentifierRequest as \
    UniverseIdentifierRequest, FactorType
from gs_quant.api.gs.assets import GsAssetApi
from gs_quant.errors import MqValueError
from typing import List, Dict
import numpy as np
import pandas as pd
import datetime as dt


def build_macro_portfolio_exposure_df(df_constituents_and_notional: pd.DataFrame,
                                      universe_sensitivities_df: pd.DataFrame,
                                      factor_dict: Dict,
                                      factor_category_dict: Dict,
                                      factors_by_name: bool) -> pd.DataFrame:
    if factors_by_name:
        universe_sensitivities_df = universe_sensitivities_df.rename(columns=factor_dict)

    columns_to_keep = factor_dict.values() if factors_by_name else factor_dict.keys()
    columns_to_drop = list(set(universe_sensitivities_df.columns.values) - set(columns_to_keep))
    universe_sensitivities_df = universe_sensitivities_df.drop(columns=columns_to_drop)

    notional_df = df_constituents_and_notional.rename(columns={"name": "Asset Name", "netExposure": "Notional"})
    gsids_with_exposure = list(universe_sensitivities_df.index.values)
    if not gsids_with_exposure:
        print(f"The portfolio is not exposed to any of the requested macro factors {', '.join(columns_to_keep)}")
        return pd.DataFrame()

    notional_df = notional_df.loc[gsids_with_exposure]

    # Multiply asset notional by asset sensitivity for each factor
    column_names = universe_sensitivities_df.columns.values.tolist()
    universe_sensitivities_df /= 100
    for column in column_names:
        universe_sensitivities_df[column] = universe_sensitivities_df[column] * notional_df['Notional']

    universe_sensitivities_df = notional_df.merge(universe_sensitivities_df, on='Asset Identifier')

    if factor_category_dict:
        # In case we want to group factors by the macro factor categories they belong in
        # Two-level column labels (Macro Factor Category -> Macro Factor)
        universe_sensitivities_df.columns = pd.MultiIndex.from_tuples(
            map(lambda factor: (factor_category_dict.get(factor, "Asset Information"), factor),
                universe_sensitivities_df.columns), names=("Macro Factor Category", "Macro Factor"))
        # Aggregate columns to get portfolio total exposure to each macro factor
        sum_over_factors_df = universe_sensitivities_df.loc[:, universe_sensitivities_df.columns != (
            "Asset Information", "Asset Name")].agg(np.sum, axis="index").to_frame().transpose()

        # Append total portfolio exposure to universe_sensitivities df
        portfolio_exposure_df = pd.concat([universe_sensitivities_df, sum_over_factors_df])

        # Group and Aggregate by Factor Category to get portfolio-level exposure to each macro Factor Category
        sum_over_categories_df = sum_over_factors_df.transpose().groupby("Macro Factor Category").apply(np.sum).\
            transpose()
        factor_and_category_zip = dict(zip(
            portfolio_exposure_df.columns.get_level_values(1), portfolio_exposure_df.columns.get_level_values(0)))
        portfolio_exposure_per_category = list(
            map(lambda x: sum_over_categories_df.loc[0, factor_and_category_zip[x]], factor_and_category_zip.keys()))

        # Append exposure df with total portfolio macro Factor Category exposure
        portfolio_exposure_df = pd.concat([
            portfolio_exposure_df,
            pd.DataFrame(portfolio_exposure_per_category,
                         index=portfolio_exposure_df.columns.tolist(),
                         columns=["Portfolio Exposure Per Macro Factor Category"]).transpose()])
        portfolio_exposure_df = portfolio_exposure_df.rename(index={0: "Portfolio Exposure Per Macro Factor"})
        portfolio_exposure_df.loc["Portfolio Exposure Per Macro Factor", ("Asset Information", "Asset Name")] = np.NAN
        portfolio_exposure_df.loc[
            "Portfolio Exposure Per Macro Factor Category", ("Asset Information", "Asset Name")] = np.NAN

        # Sort macro Factor Categories by total exposure
        portfolio_exposure_df = portfolio_exposure_df.sort_values(
            by=["Portfolio Exposure Per Macro Factor Category"], axis='columns', ascending=False)

        name_col = portfolio_exposure_df.loc[:, ("Asset Information", "Asset Name")]
        notional_col = portfolio_exposure_df.loc[:, ("Asset Information", "Notional")]
        portfolio_exposure_df = portfolio_exposure_df.drop(
            columns=[("Asset Information", "Asset Name"), ("Asset Information", "Notional")])
        portfolio_exposure_df = pd.concat([name_col, notional_col, portfolio_exposure_df], axis="columns")
    else:
        sum_over_factors_df = universe_sensitivities_df.loc[:, universe_sensitivities_df.columns != 'Asset Name'].\
            agg(np.sum, axis="index").to_frame().transpose()
        portfolio_exposure_df = pd.concat([universe_sensitivities_df, sum_over_factors_df])

        portfolio_exposure_df = portfolio_exposure_df.rename(index={0: "Portfolio Exposure Per Macro Factor"})
        portfolio_exposure_df.loc["Portfolio Exposure Per Macro Factor", "Asset Name"] = np.NAN
        portfolio_exposure_df = portfolio_exposure_df.sort_values(
            by=["Portfolio Exposure Per Macro Factor"], axis='columns', ascending=False)

        name_col = portfolio_exposure_df['Asset Name']
        portfolio_exposure_df = portfolio_exposure_df.drop(columns=['Asset Name'])
        portfolio_exposure_df.insert(loc=0, column='Asset Name', value=name_col)

    portfolio_exposure_df.index.name = 'Asset Identifier'

    return portfolio_exposure_df


def build_portfolio_constituents_df(performance_report: PerformanceReport, date: dt.date) -> pd.DataFrame:
    constituents_df = performance_report.get_portfolio_constituents(fields=['netExposure'],
                                                                    start_date=date,
                                                                    end_date=date)
    if constituents_df.empty:
        raise MqValueError(f"Macro Exposure can't be calculated as the portfolio constituents could not be found on"
                           f" the requested date {date}. Make sure the portfolio performance report is up to date.")

    constituents_df = constituents_df[["assetId", "netExposure"]]
    constituents_df = (
        constituents_df.dropna()
                       .set_index("assetId")
                       .rename_axis("Asset Identifier")
    )
    assets_data = GsAssetApi.get_many_assets_data_scroll(fields=['name', 'gsid', 'id'],
                                                         as_of=dt.datetime(date.year, date.month, date.day),
                                                         limit=1000,
                                                         id=constituents_df.index.tolist())
    assets_data_df = (
        pd.DataFrame.from_records(assets_data).set_index("id")
                                              .fillna(value={"name": "Name not available"})
                                              .rename_axis("Asset Identifier")
    )

    # Merge the constituents dataframe and asset data dataframe to get gsid, asset name, notional
    constituents_and_notional_df = (
        assets_data_df.merge(constituents_df, on='Asset Identifier').reset_index(drop=True)
                                                                    .set_index("gsid")
                                                                    .rename_axis("Asset Identifier")
                                                                    .sort_index()
    )

    return constituents_and_notional_df


def build_sensitivity_df(universe: List, model: MacroRiskModel, date: dt.date,
                         factor_type: FactorType, by_name: bool) -> pd.DataFrame:

    universe_sensitivities_df = model.get_universe_sensitivity(start_date=date, end_date=date,
                                                               assets=DataAssetsRequest(
                                                                   UniverseIdentifierRequest.gsid, universe),
                                                               factor_type=factor_type,
                                                               get_factors_by_name=by_name)

    if universe_sensitivities_df.empty:
        print(f"None of the assets in the portfolio are exposed to the factors in model {model.id} ")
        return pd.DataFrame()

    universe_sensitivities_df = (
        universe_sensitivities_df.reset_index(level=1, drop=True)
                                 .rename_axis("Asset Identifier")
                                 .sort_index()
    )

    return universe_sensitivities_df


def build_exposure_df(notional_df: pd.DataFrame,
                      universe_sensitivities_df: pd.DataFrame,
                      factor_categories: List,
                      factor_data: pd.DataFrame,
                      by_name: bool) -> pd.DataFrame:

    # Multiply sensitivity with notional
    columns = universe_sensitivities_df.columns.values.tolist()
    universe_sensitivities_df /= 100
    for column in columns:
        universe_sensitivities_df[column] = universe_sensitivities_df[column] * notional_df['Notional']

    if factor_data.empty:
        if factor_categories:
            categories_names = [f.name for f in factor_categories] if by_name else [f.id for f in factor_categories]
            universe_sensitivities_df = universe_sensitivities_df[categories_names]

        universe_sensitivities_df = pd.concat([universe_sensitivities_df,
                                               universe_sensitivities_df.agg(np.sum).to_frame().rename(
                                                   columns={0: "Total Factor Category Exposure"}).T])

        universe_sensitivities_df = universe_sensitivities_df.sort_values(
            by="Total Factor Category Exposure", axis=1, ascending=False)
        notional_df = pd.concat(
            [notional_df,
             notional_df[["Notional"]].agg(np.sum).to_frame().rename(
                 columns={0: "Total Factor Category Exposure"}).T])

        exposure_df = notional_df.join(universe_sensitivities_df).rename_axis("Factor Category", axis=1)
    else:
        factor_data = factor_data.set_index("name") if by_name else factor_data.set_index("identifier")
        new_columns = \
            [(factor_data.loc[f, 'factorCategory'], f) for f in universe_sensitivities_df.columns.values] \
            if by_name else \
            [(factor_data.loc[f, 'factorCategoryId'], f) for f in universe_sensitivities_df.columns.values]
        universe_sensitivities_df = (
            universe_sensitivities_df.set_axis(pd.MultiIndex.from_tuples(new_columns), axis=1)
                                     .rename_axis(("Factor Category", "Factor"), axis=1)
        )
        universe_sensitivities_df = pd.concat([universe_sensitivities_df,
                                               universe_sensitivities_df.agg(np.sum).to_frame().rename(
                                                   columns={0: "Total Factor Exposure"}).T
                                               ])
        universe_sensitivities_df = universe_sensitivities_df.sort_values(
            by=["Total Factor Exposure"], axis=1, ascending=False)

        # Only return factors that are grouped in the factor categories that we passed; if empty return all factors
        if factor_categories:
            categories_names = [f.name for f in factor_categories] if by_name else [f.id for f in factor_categories]
            universe_sensitivities_df = universe_sensitivities_df[categories_names]

        notional_df = (
            pd.concat([
                notional_df,
                notional_df[["Notional"]].agg(np.sum).to_frame().rename(columns={0: "Total Factor Exposure"}).T
            ]).set_axis(pd.MultiIndex.from_tuples(
                [("Asset Information", "Asset Name"), ("Asset Information", "Notional")]), axis=1)
        )
        # Merge universe sensitivity with notional df
        exposure_df = notional_df.join(universe_sensitivities_df).rename_axis(("Factor Category", "Factor"), axis=1)

    return exposure_df
