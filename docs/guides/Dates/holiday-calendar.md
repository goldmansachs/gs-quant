---
title: Holiday Calendars
excerpt: Understanding holiday calendars in GS Quant
datePublished: 2019/06/20
dateModified: 2019/06/20
gihubUrl: https://github.com/goldmansachs/gs-quant
keywords:
  - Holidays
  - Calendar
authors:
  - name: Roberto Ronderos
    github: robertoronderosjr
---

<note>In order to use the Holidays library, you need to request access to <a href='https://marquee.gs.com/s/developer/datasets/HOLIDAY'>Holidays Dataset</a></note>

GS Quant allows users to easily work with dates taking into account exchange holidays. Let's take a look at some provided methods from our date module that help us with these calculations very easily.

`is_business_day`: Determines whether each date passed to it is a business day. Returns a single boolean if a single date is passed. Otherwise, a tuple of booleans will be returned. Example:

```python
import datetime as dt
from gs_quant.datetime import is_business_day

is_today_a_business_day = is_business_day(dt.date.today(), calendars=('NYSE',)) # Returns single boolean, using NYSE exchange

are_business_dates = is_business_day([dt.date(2019, 7, 4), dt.date(2019, 7, 5)], calendars=('NYSE',)) # Returns (False, True) for the given dates, using NYSE exchange holidays
```

`business_day_offset`: Helpful if you are trying to apply an offset to the given date and move it to the nearest business date. Example:

```python
import datetime as dt

from gs_quant.datetime import business_day_offset

prev_bus_date = business_day_offset(dt.date.today(), -1, roll='preceding')
```

`business_day_count`: Useful to determine the number of business days between the given dates. Example:

```python
import datetime as dt

from gs_quant.datetime import business_day_count

today = dt.date.today()
bus_days = business_day_count(today, today + dt.timedelta(days=7))
```

If you need any other custom date calculations based on a holiday exchange calendar, you could use the GSCalendar class. This allows you to keep track of holiday dates for any given exchange. Example:

```python
from gs_quant.datetime import GsCalendar

calendar = GsCalendar.get("NYSE")
```

At this point, `calendar` will have a number of useful properties, including the `holidays` set which will list all the holidays for the given exchange.
