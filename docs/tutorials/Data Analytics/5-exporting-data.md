---
title: 05 - Exporting to Excel
excerpt: Learn to query datasets available through GS Quant.
datePublished: 2019/04/03
keywords:
  - Excel
authors:
  - name: Roberto Ronderos
    github: robertoronderosjr
  - name: Nick Young
    github: nick-young-gs
links:
  - title: Pandas
    url: https://pandas.pydata.org/
  - title: XlsxWriter
    url: https://xlsxwriter.readthedocs.io/
  - title: Sessions
    url: https://developer.gs.com/docs/gsquant/1-sessions
  - title: Timeseries Functions
    url: https://developer.gs.com/docs/gsquant/tutorials/Data%20Analytics/timeseries-functions/
  - title: Virtual Environments
    url: https://docs.python.org/3.6/tutorial/venv.html
---

Structured risk in GS Quant is returned as Pandas Dataframes. These can easily be written to Excel, for use in presentations etc. Note that you will need [XlsxWriter](https://xlsxwriter.readthedocs.io/getting_started.html) installed for this to work.

## Get Dataframe

```python
import datetime
from gs_quant.data import Dataset

weather_ds = Dataset(Dataset.GS.WEATHER)
data_frame = weather_ds.get_data(datetime.date(2016, 1, 15), datetime.date(2016, 1, 16), city=['Boston', 'Austin'])
```
Output:
```python
Out[1]: 
     city        date    ...                    updateTime  windSpeed
0  Boston  2016-01-15    ...      2017-03-06T16:49:36.472Z        5.2
1  Boston  2016-01-16    ...      2017-03-06T16:49:36.472Z        6.9
2  Austin  2016-01-15    ...      2017-03-06T16:49:36.524Z        0.0
3  Austin  2016-01-16    ...      2017-03-06T16:49:36.524Z        0.0
[4 rows x 10 columns]
```

## Constructing an Excel Worksheet

```python
writer = pd.ExcelWriter(r'C:\Temp\Weather.xlsx', engine='xlsxwriter')       # Create workbook
panda_df.to_excel(writer, sheet_name='Weather')                             # Create a sheet called Weather


for measure, values in panda_df.items():
    pd.DataFrame({measure: values}).to_excel(writer, sheet_name=measure)    # Write values to the sheet

writer.save()
```

Now you can open the workbook directly in Excel