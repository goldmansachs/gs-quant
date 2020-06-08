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
import re
import string

ConstPoints = {
    "O/N": 0,
    "T/N": 0.1,
    "OIS FIX": 1,
    "CASH STUB": 1.1,
    "CASHSTUB": 1.1,
    "DEFAULT": 0,
    "IN": 0.1,
    "OUT": 0.2
}

# Regular expression for different types of market data coordinate points
EuroOrFraReg = \
    r"^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)+([0-9][0-9])$"
NumberReg = r"^([0-9]*)$"
MMMYYYYReg = r"^([a-zA-Z]{3}[0-9]{4})$"
DDMMMYYYYReg = r"^([1-3]*[0-9]{1}[a-zA-Z]{3}[0-9]{4})$"
SpikeQEReg = r"^(QE[0-9])-([0-9]{4})$"
FRAxReg = r"^([0-9]+)x([0-9]+)$"
RDatePartReg = r"^([-]*[0-9]+[mydwbfMYDWBF])([-]*[0-9]+[mydwbfMYDWBF])?$"
CashFXReg = r"^([-]*[0-9]+[mydwbfMYDWBF])([-]*[0-9]+[mydwbfMYDWBF])? XC$"
PricerCoordRegI = r"^(No )([0-9]*)$"
PricerCoordRegII = r"^(Pricer )([0-9]*)$"
PricerBFReg = r"^([-]*[0-9]+[mydwbfMYDWBFM])([-]*[0-9]+[mydwbfMYDWBF])([-]*[0-9]+[mydwbfMYDWBF])?$"
PricerBondSpreadReg = r"^[0-9][SQHT]([0-9]{2})[/][0-9][SQHT]([0-9]{2})"
SeasonalFrontReg = r"(Front|Back)"
infl_volReg = r"(Caplet|ZCCap|Swaption|ZCSwo)"
MMMReg = r"^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)$"
MMMYYReg = r"^(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC) ([0-9]{2})"
DatePairReg = r"^([0-9]{8})/([0-9]{8})$"
DatePairReg2 = r"^([0-9]{8}) ([0-9]{8})$"
FXVolAddonParmsReg = \
    r"(Spread Addon|Spread Init|Spread Final|Rho Addon|Rho Init|Rho Final|Vol Addon|Vol Init|Vol Final|HL|Addon HL)"
CopulaReg = r"(Rho$|Rho Rate|Rho Vol|RR|BF|Alpha|Beta|KO$|K0=L|K0=S)"
BondCoordReg = r"^[0-9]* ([0-9.]*) ([0-9]{2}/[0-9]{2}/[0-9]{4})$"
BondFutReg = r"^[A-Z]{3}([FGHJKMNQUVXZ])([0-9])$"
FFFutReg = r"^FF([FGHJKMNQUVXZ])([0-9])$"
RepoGCReg = r"^(ON|SN|TN|[0-9]+) (|Month |Week |Year |Day )GC$"
FloatingYear = r"^([0-9]*\.[0-9])[yY]$"
RelativeReg = r"^([0-9]+) (day|week|month|year|DAY|WEEK|MONTH|YEAR)$"

LYYReg = r"([FGHJKMNQUVXZ])([0-9]{2})"
DateRuleReg = r"^([-]*[0-9]+[mydwbfMYDWBFM])+$"
DDMMMYYReg = r"^([0-3]*[0-9]{1}[a-zA-Z]{3}[0-9]{2})$"

FutMonth = r"FGHJKMNQUVXZ"

DictDayRule = {
    'Month': 30,
    'MONTH': 30,
    'Week': 7,
    'WEEK': 7,
    'Year': 365,
    'YEAR': 365,
    'Day': 1,
    'DAY': 1,
    'd': 1,
    'D': 1,
    'w': 7,
    'W': 7,
    'b': 1,
    'B': 1,
    'f': 30,
    'F': 30,
    'm': 30,
    'M': 30,
    'y': 365,
    'Y': 365
}


def relative_date_add(date_rule: str, strict: bool = False) -> float:
    """Change the string in date rule format to the number of days. E.g 1d to 1, 1y to 365, 1m to 30, -1w to -7"""
    days = ''

    if re.search(DateRuleReg, date_rule) is not None:
        res = re.search(DateRuleReg, date_rule)
        date_str = res.group(1)
        if date_str[0] == '-':
            num = float(date_str[1:-1])
            days = '-'
        else:
            num = float(date_str[:-1])
        rule = date_str[-1:]
        if rule in DictDayRule:
            scale = DictDayRule[rule]
            days = days + str(num * scale)
            d = float(days)
            return d
        else:
            raise ValueError('There are no valid day rule for the point provided.')

    if strict:
        raise ValueError(f'invalid date rule {date_rule}')
    return 0


def point_sort_order(point: str, ref_date: dt.date = dt.date.today()) -> float:
    """
    Calculates a number that can be used to sort Mkt Points by it.

    :param point: The point string from MarketDataCoordinate.
    :param ref_date: Reference date, normally the pricing date.
    :return: The number of days from the reference date to the date specified by the point string

    **Examples**

    >>> import datetime as dt
    >>> days = point_sort_order(point = 'Dec20', ref_date=dt.date.today())
    """

    if not point or not isinstance(point, str):
        return 0

    const_value = ConstPoints.get(point.upper())
    if const_value is not None:
        return const_value

    parts = point.split(';')
    if len(parts) > 1:
        first = point_sort_order(parts[0])
        if not first:
            return 0

        return first + (0.1 * sum(point_sort_order(p, ref_date) for p in parts[1:]) / first)

    days = None

    if point == 'o/n':
        days = 0
    elif point == 't/n':
        days = 0.1
    elif point == 'Cash Stub':
        days = 1.1
    elif point == 'CashStub':
        days = 1.1
    elif point == 'Default':
        days = 0
    elif point == 'In':
        days = 0.1
    elif point == 'Out':
        days = 0.2
    elif re.search(infl_volReg, point) is not None:
        res = re.search(infl_volReg, point)
        infl_vol = res.group(1)
        if infl_vol == 'Caplet':
            days = 0
        elif infl_vol == 'ZCCap':
            days = 1
        elif infl_vol == 'Swaption':
            days = 2
        elif infl_vol == 'ZCSwo':
            days = 3
    elif re.search(CopulaReg, point) is not None:
        pass
    elif re.search(SeasonalFrontReg, point) is not None:
        res = re.search(SeasonalFrontReg, point)
        if res.group(1) == 'Front':
            days = 0
        else:
            days = 1
    elif re.search(MMMReg, point) is not None:
        res = re.search(MMMReg, point)
        date_str = '1' + res.group(1) + '2000'
        format_str = '%d%b%Y'
        days = (dt.datetime.strptime(date_str, format_str).date() - ref_date).days
    elif re.search(EuroOrFraReg, point) is not None:
        res = re.search(EuroOrFraReg, point)
        date_str = '15' + res.group(1) + res.group(2)
        format_str = '%d%b%y'
        days = (dt.datetime.strptime(date_str, format_str).date() - ref_date).days
    elif re.search(RDatePartReg, point) is not None:
        res = re.search(RDatePartReg, point)
        date_str = res.group(1)
        days = relative_date_add(date_str)
    elif re.search(CashFXReg, point) is not None:
        res = re.search(CashFXReg, point)
        date_str = res.group(1)
        days = relative_date_add(date_str)
    elif re.search(PricerBFReg, point) is not None:
        res = re.search(PricerBFReg, point)
        date_str = res.group(1)
        days = relative_date_add(date_str)
    elif re.search(FRAxReg, point) is not None:
        res = re.search(FRAxReg, point)
        date_str = res.group(1) + 'm'
        days = relative_date_add(date_str)
    elif re.search(SpikeQEReg, point) is not None:
        res = re.search(SpikeQEReg, point)
        qe = res.group(1)
        if qe == 'QE1':
            month = "Mar"
        elif qe == 'QE2':
            month = "Jun"
        elif qe == 'QE3':
            month = "Sep"
        elif qe == 'QE4':
            month = 'Dec'
        else:
            month = 'Dec'
        date_str = "1" + month + res.group(2)
        format_str = '%d%b%Y'
        days = (dt.datetime.strptime(date_str, format_str).date() - ref_date).days
    elif re.search(MMMYYYYReg, point) is not None:
        res = re.search(MMMYYYYReg, point)
        date_str = '1' + res.group(1)
        format_str = '%d%b%Y'
        days = (dt.datetime.strptime(date_str, format_str).date() - ref_date).days
    elif re.search(DDMMMYYYYReg, point) is not None:
        res = re.search(DDMMMYYYYReg, point)
        date_str = res.group(1)
        format_str = '%d%b%Y'
        days = (dt.datetime.strptime(date_str, format_str).date() - ref_date).days
    elif re.search(NumberReg, point) is not None:
        res = re.search(NumberReg, point)
        days = float(res.group(1))
    elif re.search(FloatingYear, point) is not None:
        res = re.search(FloatingYear, point)
        year = float(res.group(1))
        days = 365 * year
    elif re.search(PricerCoordRegI, point) is not None:
        res = re.search(PricerCoordRegI, point)
        days = float(res.group(2))
    elif re.search(PricerCoordRegII, point) is not None:
        res = re.search(PricerCoordRegII, point)
        days = float(res.group(2))
    elif re.search(PricerBondSpreadReg, point) is not None:
        pass
    elif re.search(LYYReg, point) is not None:
        res = re.search(LYYReg, point)
        month = FutMonth.find(res.group(1)) + 1
        year = res.group(2)
        date_str = year + '-' + str(month) + '-1'
        format_str = '%y-%m-%d'
        days = (dt.datetime.strptime(date_str, format_str).date() - ref_date).days
    elif re.search(DatePairReg, point) is not None:
        res = re.search(DatePairReg, point)
        date_str = res.group(2)
        format_str = '%Y%m%d'
        days = (dt.datetime.strptime(date_str, format_str).date() - ref_date).days
    elif re.search(DatePairReg2, point) is not None:
        res = re.search(DatePairReg2, point)
        date_str = res.group(2)
        format_str = '%Y%m%d'
        days = (dt.datetime.strptime(date_str, format_str).date() - ref_date).days
    elif re.search(MMMYYReg, point) is not None:
        res = re.search(MMMYYReg, point)
        date_str = '1' + res.group(1) + res.group(2)
        format_str = '%d%b%y'
        days = (dt.datetime.strptime(date_str, format_str).date() - ref_date).days
    elif re.search(FXVolAddonParmsReg, point) is not None:
        pass
    elif re.search(BondCoordReg, point) is not None:
        res = re.search(BondCoordReg, point)
        date_str = res.group(2)
        format_str = '%d/%m/%Y'
        days = (dt.datetime.strptime(date_str, format_str).date() - ref_date).days
    elif re.search(BondFutReg, point) is not None:
        res = re.search(BondFutReg, point)
        month = FutMonth.find(res.group(1)) + 1
        date_str = str(ref_date.year) + '-' + str(month) + '-1'
        format_str = '%Y-%m-%d'
        days = (dt.datetime.strptime(date_str, format_str).date() - ref_date).days
    elif re.search(FFFutReg, point) is not None:
        res = re.search(FFFutReg, point)
        month = FutMonth.find(res.group(1)) + 1
        date_str = str(ref_date.year) + '-' + str(month) + '-1'
        format_str = '%Y-%m-%d'
        days = (dt.datetime.strptime(date_str, format_str).date() - ref_date).days
    elif re.search(RepoGCReg, point) is not None:
        res = re.search(RepoGCReg, point)
        if point == 'ON GC':
            days = 0
        elif point == 'TN GC':
            days = 1
        elif point == 'SN GC':
            days = 2
        elif res.group(2).strip() in DictDayRule:
            scale = DictDayRule[res.group(2).strip()]
            num = float(res.group(1))
            days = num * scale
    elif re.search(RelativeReg, point) is not None:
        res = re.search(RelativeReg, point)
        rule = string.capwords(res.group(2))
        if rule in DictDayRule:
            scale = DictDayRule[rule]
            num = float(res.group(1))
            days = num * scale
    elif re.search(DDMMMYYReg, point) is not None:
        res = re.search(DDMMMYYReg, point)
        date_str = res.group(1)
        format_str = '%d%b%y'
        days = (dt.datetime.strptime(date_str, format_str).date() - ref_date).days
    return days
