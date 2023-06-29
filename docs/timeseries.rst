
Timeseries Package
==================

Algebra
-------

.. currentmodule:: gs_quant.timeseries.algebra

.. autosummary::
   :toctree: functions

   abs_
   add
   and_
   ceil
   divide
   exp
   filter_
   filter_dates
   floor
   floordiv
   if_
   log
   multiply
   not_
   or_
   power
   repeat
   smooth_spikes
   sqrt
   subtract
   weighted_sum


Analysis
--------

.. currentmodule:: gs_quant.timeseries.analysis

.. autosummary::
   :toctree: functions

   diff
   first
   last
   last_value
   count
   lag


Backtesting
-----------

.. currentmodule:: gs_quant.timeseries.backtesting

.. autosummary::
   :toctree: functions

   basket
   basket_series

.. autosummary::
   :toctree: classes
   :template: timeseries_class.rst

   Basket

Date / Time
-----------


.. currentmodule:: gs_quant.timeseries.datetime

.. autosummary::
   :toctree: functions

   align
   interpolate
   value
   day
   weekday
   month
   year
   quarter
   date_range
   prepend
   union
   bucketize

.. autosummary::
   :toctree: classes
   :template: timeseries_class.rst

   Window


Econometrics
------------


.. currentmodule:: gs_quant.timeseries.econometrics

.. autosummary::
   :toctree: functions

   annualize
   beta
   change
   correlation
   excess_returns_
   index
   max_drawdown
   prices
   returns
   sharpe_ratio
   volatility


Statistics
----------

.. currentmodule:: gs_quant.timeseries.statistics

.. autosummary::
   :toctree: functions

   cov
   exponential_std
   generate_series
   max_   
   mean
   median   
   min_
   mode
   percentile
   percentiles
   product
   range_
   std
   sum_
   var
   winsorize
   zscores

.. autosummary::
   :toctree: classes
   :template: timeseries_class.rst

   LinearRegression
   RollingLinearRegression
   SIRModel
   SEIRModel

Technical Analysis
------------------


.. currentmodule:: gs_quant.timeseries.technicals

.. autosummary::
   :toctree: functions

   bollinger_bands
   moving_average
   exponential_moving_average
   exponential_volatility
   exponential_spread_volatility
   smoothed_moving_average
   relative_strength_index
   macd
   