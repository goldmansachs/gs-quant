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
from typing import Dict, Any, Iterable

from dataclasses_json.cfg import _GlobalConfig

from gs_quant.target.workflow_quote import VisualStructuringReport

global_config = _GlobalConfig()


def quote_report_from_dict(quote_report_dict: Dict[str, Any]):
    if quote_report_dict is not None:
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
