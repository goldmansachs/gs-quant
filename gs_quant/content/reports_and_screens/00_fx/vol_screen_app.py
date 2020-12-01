from gs_quant.data import Dataset
from gs_quant.timeseries import percentiles, volatility, last_value
from gs_quant.datetime import business_day_offset
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import warnings
from datetime import date
import streamlit as st
from gs_quant.session import GsSession

warnings.filterwarnings('ignore')
sns.set(style="darkgrid", color_codes=True)

# external users should substitute their client id and secret; please skip this step if using internal jupyterhub
GsSession.use(client_id=None, client_secret=None, scopes=('run_analytics',))


def format_df(data_dict):
    df = pd.concat(data_dict, axis=1)
    df.columns = data_dict.keys()
    return df.fillna(method='ffill').dropna()


def volatility_screen(crosses, start_date, end_date, tenor='3m', plot=True):
    fxspot_dataset, fxvol_dataset = Dataset('FXSPOT'), Dataset('FXIMPLIEDVOL')
    spot_data, impvol_data, spot_fx, data = {}, {}, {}, {}
    for cross in crosses:
        spot = fxspot_dataset.get_data(start_date, end_date, bbid=cross)[['spot']].drop_duplicates(keep='last')
        spot_fx[cross] = spot['spot']
        spot_data[cross] = volatility(spot['spot'], tenor)  # realized vol
        vol = fxvol_dataset.get_data(start_date, end_date, bbid=cross, tenor=tenor, deltaStrike='DN', location='NYC')[
            ['impliedVolatility']]
        impvol_data[cross] = vol.drop_duplicates(keep='last') * 100

    spdata, ivdata = format_df(spot_data), format_df(impvol_data)
    diff = ivdata.subtract(spdata).dropna()
    for cross in crosses:
        data[cross] = {'Spot': last_value(spot_fx[cross]),
                       '{} Implied'.format(tenor): last_value(ivdata[cross]),
                       '{} Realized'.format(tenor): last_value(spdata[cross]),
                       'Diff': last_value(diff[cross]),
                       'Historical Implied Low': min(ivdata[cross]),
                       'Historical Implied High': max(ivdata[cross]),
                       '%-ile': last_value(percentiles(ivdata[cross]))
                       }
    df = pd.DataFrame(data)
    vol_screen = df.transpose()
    st.write(st.dataframe(vol_screen.style.highlight_max(axis=0)))
    if plot:
        for fx in vol_screen.index:
            plt.scatter(vol_screen.loc[fx]['%-ile'], vol_screen.loc[fx]['Diff'])
            plt.legend(vol_screen.index, loc='best', bbox_to_anchor=(0.9, -0.13), ncol=3)

        plt.xlabel('Percentile of Current Implied Vol')
        plt.ylabel('Implied vs Realized Vol')
        plt.title('Entry Point vs Richness')
        st.pyplot(plt)
    return


g10 = ['USDJPY', 'EURUSD', 'AUDUSD', 'GBPUSD', 'USDCAD', 'USDNOK', 'NZDUSD', 'USDSEK', 'USDCHF']

end = business_day_offset(date.today(), -1, roll='preceding')

st.title('Vol Monitor')

crosses = st.multiselect('FX Crosses',
                         g10, default='EURUSD')
tenors = st.selectbox('Tenor', ('1m', '3m', '6m', '1y'))

start = st.slider("Start Date", value=(date(2018, 1, 1), end), format="MM/DD/YY")

volatility_screen(crosses, start[0], start[1], tenors)
