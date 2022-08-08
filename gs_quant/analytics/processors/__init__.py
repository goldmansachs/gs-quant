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

from .analysis_processors import DiffProcessor
from .econometrics_processors import SharpeRatioProcessor, VolatilityProcessor, CorrelationProcessor, ChangeProcessor, \
    ReturnsProcessor, BetaProcessor, FXImpliedCorrProcessor
from .special_processors import EntityProcessor, CoordinateProcessor
from .statistics_processors import PercentilesProcessor, PercentileProcessor, StdMoveProcessor, \
    CovarianceProcessor, ZscoresProcessor, MeanProcessor, VarianceProcessor, SumProcessor, StdDevProcessor
from .utility_processors import LastProcessor, AppendProcessor, AdditionProcessor, SubtractionProcessor, \
    MultiplicationProcessor, DivisionProcessor, MinProcessor, MaxProcessor, NthLastProcessor, OneDayProcessor
from .scale_processors import ScaleProcessor, BarMarkerProcessor, SpotMarkerProcessor, ScaleShape
