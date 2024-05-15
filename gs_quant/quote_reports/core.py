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
from typing import Dict, Any, Iterable, Union

from dataclasses_json.cfg import _GlobalConfig

from gs_quant.base import CustomComments
from gs_quant.target.workflow_quote import HedgeTypes
from gs_quant.workflow import VisualStructuringReport, BinaryImageComments, HyperLinkImageComments, \
    CustomDeltaHedge, DeltaHedge

global_config = _GlobalConfig()


def quote_report_from_dict(quote_report_dict: Union[Dict[str, Any], VisualStructuringReport]):
    if quote_report_dict is not None:
        if isinstance(quote_report_dict, VisualStructuringReport):
            return quote_report_dict
        type = quote_report_dict.get('reportType')
        if 'VisualStructuringReport' == type:
            report = VisualStructuringReport.from_dict(quote_report_dict)
            return report
    return None


def quote_reports_from_dicts(quote_report_dicts: Iterable[Dict[str, Any]]):
    if quote_report_dicts is not None:
        reports = []
        for quote_report_dict in quote_report_dicts:
            report = quote_report_from_dict(quote_report_dict)
            reports.append(report)
        return reports
    return None


def custom_comment_from_dict(in_dict: Union[Dict[str, Any], CustomComments]):
    if in_dict is not None:
        if isinstance(in_dict, CustomComments):
            return in_dict
        type = in_dict.get('commentType')
        if 'binaryImageComments' == type:
            out = BinaryImageComments.from_dict(in_dict)
            return out
        if 'hyperLinkImageComments' == type:
            out = HyperLinkImageComments.from_dict(in_dict)
            return out
    return None


def custom_comments_from_dicts(in_dicts: Iterable[Dict[str, Any]]):
    if in_dicts is not None:
        comments = []
        for in_dict in in_dicts:
            report = custom_comment_from_dict(in_dict)
            comments.append(report)
        return comments
    return None


def hedge_type_from_dict(hedge_type_dict: Union[Dict[str, Any], HedgeTypes]):
    if hedge_type_dict is not None:
        if isinstance(hedge_type_dict, HedgeTypes):
            return hedge_type_dict
        type = hedge_type_dict.get('type')
        if 'CustomDeltaHedge' == type:
            hedge_type = CustomDeltaHedge.from_dict(hedge_type_dict)
            return hedge_type
        if 'DeltaHedge' == type:
            hedge_type = DeltaHedge.from_dict(hedge_type_dict)
            return hedge_type
    return None


def hedge_type_from_dicts(in_dicts: Iterable[Dict[str, Any]]):
    if in_dicts is not None:
        hedge_types = []
        for in_dict in in_dicts:
            hedge_type = hedge_type_from_dict(in_dict)
            hedge_types.append(hedge_type)
        return hedge_types
    return None
