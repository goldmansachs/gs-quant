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

from gs_quant.base import *
from gs_quant.common import *
import datetime
from typing import Dict, Optional, Tuple, Union
from dataclasses import dataclass, field
from dataclasses_json import LetterCase, config, dataclass_json
from enum import Enum


class Division(EnumBase, Enum):    
    
    SECDIV = 'SECDIV'
    IBD = 'IBD'
    RISK = 'RISK'
    GIR = 'GIR'
    EO = 'EO'
    KENSHO = 'KENSHO'    


class InvestmentRecommendationDirection(EnumBase, Enum):    
    
    Buy = 'Buy'
    Hold = 'Hold'
    Sell = 'Sell'
    Strategy = 'Strategy'    


class Language(EnumBase, Enum):    
    
    """ISO 639-1 language code for the content piece"""

    an = 'an'
    ar = 'ar'
    _as = 'as'
    av = 'av'
    ay = 'ay'
    az = 'az'
    ba = 'ba'
    be = 'be'
    bg = 'bg'
    bh = 'bh'
    bi = 'bi'
    bm = 'bm'
    bn = 'bn'
    bo = 'bo'
    br = 'br'
    bs = 'bs'
    ca = 'ca'
    ce = 'ce'
    ch = 'ch'
    co = 'co'
    cr = 'cr'
    cs = 'cs'
    cu = 'cu'
    cv = 'cv'
    cy = 'cy'
    da = 'da'
    de = 'de'
    dv = 'dv'
    dz = 'dz'
    ee = 'ee'
    el = 'el'
    en = 'en'
    eo = 'eo'
    es = 'es'
    et = 'et'
    eu = 'eu'
    fa = 'fa'
    ff = 'ff'
    fi = 'fi'
    fj = 'fj'
    fo = 'fo'
    fr = 'fr'
    fy = 'fy'
    ga = 'ga'
    gd = 'gd'
    gl = 'gl'
    gn = 'gn'
    gu = 'gu'
    gv = 'gv'
    ha = 'ha'
    he = 'he'
    hi = 'hi'
    ho = 'ho'
    hr = 'hr'
    ht = 'ht'
    hu = 'hu'
    hy = 'hy'
    hz = 'hz'
    ia = 'ia'
    id = 'id'
    ie = 'ie'
    ig = 'ig'
    ii = 'ii'
    ik = 'ik'
    io = 'io'
    _is = 'is'
    it = 'it'
    iu = 'iu'
    ja = 'ja'
    jv = 'jv'
    ka = 'ka'
    kg = 'kg'
    ki = 'ki'
    kj = 'kj'
    kk = 'kk'
    kl = 'kl'
    km = 'km'
    kn = 'kn'
    ko = 'ko'
    kr = 'kr'
    ks = 'ks'
    ku = 'ku'
    kv = 'kv'
    kw = 'kw'
    ky = 'ky'
    la = 'la'
    lb = 'lb'
    lg = 'lg'
    li = 'li'
    ln = 'ln'
    lo = 'lo'
    lt = 'lt'
    lu = 'lu'
    lv = 'lv'
    mg = 'mg'
    mh = 'mh'
    mi = 'mi'
    mk = 'mk'
    ml = 'ml'
    mn = 'mn'
    mr = 'mr'
    ms = 'ms'
    mt = 'mt'
    my = 'my'
    na = 'na'
    nb = 'nb'
    nd = 'nd'
    ne = 'ne'
    ng = 'ng'
    nl = 'nl'
    nn = 'nn'
    no = 'no'
    nr = 'nr'
    nv = 'nv'
    ny = 'ny'
    oc = 'oc'
    oj = 'oj'
    om = 'om'
    _or = 'or'
    os = 'os'
    pa = 'pa'
    pi = 'pi'
    pl = 'pl'
    ps = 'ps'
    pt = 'pt'
    qu = 'qu'
    rm = 'rm'
    rn = 'rn'
    ro = 'ro'
    ru = 'ru'
    rw = 'rw'
    sa = 'sa'
    sc = 'sc'
    sd = 'sd'
    se = 'se'
    sg = 'sg'
    si = 'si'
    sk = 'sk'
    sl = 'sl'
    sm = 'sm'
    sn = 'sn'
    so = 'so'
    sq = 'sq'
    sr = 'sr'
    ss = 'ss'
    st = 'st'
    su = 'su'
    sv = 'sv'
    sw = 'sw'
    ta = 'ta'
    te = 'te'
    tg = 'tg'
    th = 'th'
    ti = 'ti'
    tk = 'tk'
    tl = 'tl'
    tn = 'tn'
    to = 'to'
    tr = 'tr'
    ts = 'ts'
    tt = 'tt'
    tw = 'tw'
    ty = 'ty'
    ug = 'ug'
    uk = 'uk'
    ur = 'ur'
    uz = 'uz'
    ve = 've'
    vi = 'vi'
    vo = 'vo'
    wa = 'wa'
    wo = 'wo'
    xh = 'xh'
    yi = 'yi'
    yo = 'yo'
    za = 'za'
    zh = 'zh'
    zu = 'zu'    


class Origin(EnumBase, Enum):    
    
    """Where the content originated from"""

    WEB = 'WEB'
    API = 'API'
    EMAIL = 'EMAIL'
    BLOG = 'BLOG'
    ARTICLE = 'ARTICLE'    


class QueryableStatus(EnumBase, Enum):    
    
    """Status/state of a content piece that can be queried by a user"""

    Draft = 'Draft'
    Published = 'Published'
    Replaced = 'Replaced'    


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Content(Base):
    body: str = None
    mime_type: object = None
    encoding: object = None


class Object(DictBase):
    pass


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Author(Base):
    id_: Optional[str] = field(default=None, metadata=config(field_name='id'))
    name: Optional[str] = None
    division: Optional[Division] = None
    email: Optional[str] = None
    title: Optional[str] = None
    kerberos: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BulkDeleteContentResponse(Base):
    status: Optional[int] = None
    message: Optional[str] = None
    data: Optional[Tuple[str, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Certification(Base):
    submission_id: str = None
    version: str = None
    submission_state: object = None
    allowed_distribution: Tuple[Object, ...] = None
    etask_process_instance_id: Optional[str] = None
    tags: Optional[Tuple[None, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DeleteContentResponse(Base):
    status: Optional[int] = None
    message: Optional[str] = None
    data: Optional[str] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class InvestmentRecommendationAsset(Base):
    asset_id: str = None
    direction: Optional[InvestmentRecommendationDirection] = None
    currency: Optional[str] = None
    price: Optional[float] = None
    price_target: Optional[float] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class InvestmentRecommendationCustomAsset(Base):
    asset_name: str = None
    direction: Optional[InvestmentRecommendationDirection] = None
    currency: Optional[str] = None
    price: Optional[float] = None
    price_target: Optional[float] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ContentResponse(Base):
    id_: Optional[str] = field(default=None, metadata=config(field_name='id'))
    version: Optional[str] = None
    name: Optional[str] = None
    entitlements: Optional[Entitlements] = None
    entitlement_exclusions: Optional[EntitlementExclusions] = None
    created_by_id: Optional[str] = None
    created_time: Optional[datetime.datetime] = None
    last_updated_time: Optional[datetime.datetime] = None
    channels: Optional[Tuple[str, ...]] = None
    content: Optional[Content] = None
    language: Optional[Language] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ContentUpdateRequest(Base):
    name: Optional[str] = None
    entitlements: Optional[Entitlements] = None
    entitlement_exclusions: Optional[EntitlementExclusions] = None
    content: Optional[Content] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class InvestmentRecommendations(Base):
    assets: Tuple[InvestmentRecommendationAsset, ...] = None
    custom_assets: Optional[Tuple[InvestmentRecommendationCustomAsset, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BulkContentUpdateRequestItem(Base):
    id_: Optional[str] = field(default=None, metadata=config(field_name='id'))
    update: Optional[ContentUpdateRequest] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ContentAuditFields(Base):
    id_: Optional[str] = field(default=None, metadata=config(field_name='id'))
    version: Optional[str] = None
    name: Optional[str] = None
    entitlements: Optional[Entitlements] = None
    entitlement_exclusions: Optional[EntitlementExclusions] = None
    created_by_id: Optional[str] = None
    authors: Optional[Tuple[Author, ...]] = None
    created_time: Optional[datetime.datetime] = None
    last_updated_time: Optional[datetime.datetime] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ContentParameters(Base):
    author_ids: Tuple[str, ...] = None
    language: Language = None
    status: Optional[object] = None
    source: Optional[Division] = None
    tags: Optional[Tuple[str, ...]] = None
    slug: Optional[str] = None
    attachments: Optional[Tuple[Content, ...]] = None
    certification: Optional[Certification] = None
    certification_type: Optional[object] = None
    asset_ids: Optional[Tuple[str, ...]] = None
    origin: Optional[Origin] = None
    investment_recommendations: Optional[InvestmentRecommendations] = None
    is_flow: Optional[bool] = None
    is_research_summary: Optional[bool] = None
    is_restricted: Optional[bool] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class GetManyContentsResponse(Base):
    status: Optional[int] = None
    message: Optional[str] = None
    data: Optional[Tuple[ContentResponse, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BulkContentUpdateResponse(Base):
    status: Optional[int] = None
    message: Optional[str] = None
    data: Optional[Tuple[ContentAuditFields, ...]] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ContentCreateRequest(Base):
    name: str = None
    entitlements: Entitlements = None
    entitlement_exclusions: EntitlementExclusions = None
    content: Content = None
    parameters: ContentParameters = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ContentCreateResponse(Base):
    status: Optional[int] = None
    message: Optional[str] = None
    data: Optional[ContentAuditFields] = None


@fix_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ContentUpdateResponse(Base):
    status: Optional[int] = None
    message: Optional[str] = None
    data: Optional[ContentAuditFields] = None
