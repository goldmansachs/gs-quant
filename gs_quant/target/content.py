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


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ChannelMetadata(Base):
    name: Optional[str] = field(default=None, metadata=field_metadata)
    channel_visibility: Optional[object] = field(default=None, metadata=field_metadata)
    restricted: Optional[bool] = field(default=None, metadata=field_metadata)
    streaming: Optional[bool] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Content(Base):
    body: str = field(default=None, metadata=field_metadata)
    mime_type: object = field(default=None, metadata=field_metadata)
    encoding: object = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


class Object(DictBase):
    pass


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Author(Base):
    id_: Optional[str] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    name: Optional[str] = field(default=None, metadata=field_metadata)
    division: Optional[Division] = field(default=None, metadata=field_metadata)
    email: Optional[str] = field(default=None, metadata=field_metadata)
    title: Optional[str] = field(default=None, metadata=field_metadata)
    kerberos: Optional[str] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BulkDeleteContentResponse(Base):
    status: Optional[int] = field(default=None, metadata=field_metadata)
    message: Optional[str] = field(default=None, metadata=field_metadata)
    data: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class Certification(Base):
    submission_id: str = field(default=None, metadata=field_metadata)
    version: str = field(default=None, metadata=field_metadata)
    submission_state: object = field(default=None, metadata=field_metadata)
    allowed_distribution: Tuple[Object, ...] = field(default=None, metadata=field_metadata)
    etask_process_instance_id: Optional[str] = field(default=None, metadata=field_metadata)
    tags: Optional[Tuple[None, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class DeleteContentResponse(Base):
    status: Optional[int] = field(default=None, metadata=field_metadata)
    message: Optional[str] = field(default=None, metadata=field_metadata)
    data: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class InvestmentRecommendationAsset(Base):
    asset_id: str = field(default=None, metadata=field_metadata)
    direction: Optional[InvestmentRecommendationDirection] = field(default=None, metadata=field_metadata)
    currency: Optional[str] = field(default=None, metadata=field_metadata)
    price: Optional[float] = field(default=None, metadata=field_metadata)
    price_target: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class InvestmentRecommendationCustomAsset(Base):
    asset_name: str = field(default=None, metadata=field_metadata)
    direction: Optional[InvestmentRecommendationDirection] = field(default=None, metadata=field_metadata)
    currency: Optional[str] = field(default=None, metadata=field_metadata)
    price: Optional[float] = field(default=None, metadata=field_metadata)
    price_target: Optional[float] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ContentResponse(Base):
    id_: Optional[str] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    version: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=field_metadata)
    entitlements: Optional[Entitlements] = field(default=None, metadata=field_metadata)
    entitlement_exclusions: Optional[EntitlementExclusions] = field(default=None, metadata=field_metadata)
    created_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    created_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    last_updated_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    channels: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    content: Optional[Content] = field(default=None, metadata=field_metadata)
    language: Optional[Language] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ContentUpdateRequest(Base):
    name: Optional[str] = field(default=None, metadata=field_metadata)
    entitlements: Optional[Entitlements] = field(default=None, metadata=field_metadata)
    entitlement_exclusions: Optional[EntitlementExclusions] = field(default=None, metadata=field_metadata)
    content: Optional[Content] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class InvestmentRecommendations(Base):
    assets: Tuple[InvestmentRecommendationAsset, ...] = field(default=None, metadata=field_metadata)
    custom_assets: Optional[Tuple[InvestmentRecommendationCustomAsset, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BulkContentUpdateRequestItem(Base):
    id_: Optional[str] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    update: Optional[ContentUpdateRequest] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ContentAuditFields(Base):
    id_: Optional[str] = field(default=None, metadata=config(field_name='id', exclude=exclude_none))
    version: Optional[str] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=field_metadata)
    entitlements: Optional[Entitlements] = field(default=None, metadata=field_metadata)
    entitlement_exclusions: Optional[EntitlementExclusions] = field(default=None, metadata=field_metadata)
    created_by_id: Optional[str] = field(default=None, metadata=field_metadata)
    authors: Optional[Tuple[Author, ...]] = field(default=None, metadata=field_metadata)
    created_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)
    last_updated_time: Optional[datetime.datetime] = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ContentParameters(Base):
    author_ids: Tuple[str, ...] = field(default=None, metadata=field_metadata)
    language: Language = field(default=None, metadata=field_metadata)
    status: Optional[object] = field(default=None, metadata=field_metadata)
    source: Optional[Division] = field(default=None, metadata=field_metadata)
    tags: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    slug: Optional[str] = field(default=None, metadata=field_metadata)
    attachments: Optional[Tuple[Content, ...]] = field(default=None, metadata=field_metadata)
    certification: Optional[Certification] = field(default=None, metadata=field_metadata)
    certification_type: Optional[object] = field(default=None, metadata=field_metadata)
    asset_ids: Optional[Tuple[str, ...]] = field(default=None, metadata=field_metadata)
    origin: Optional[Origin] = field(default=None, metadata=field_metadata)
    investment_recommendations: Optional[InvestmentRecommendations] = field(default=None, metadata=field_metadata)
    is_flow: Optional[bool] = field(default=None, metadata=field_metadata)
    is_research_summary: Optional[bool] = field(default=None, metadata=field_metadata)
    is_restricted: Optional[bool] = field(default=None, metadata=field_metadata)
    post_sharing_type: Optional[object] = field(default=None, metadata=field_metadata)
    channels_metadata: Optional[Tuple[ChannelMetadata, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class GetManyContentsResponse(Base):
    status: Optional[int] = field(default=None, metadata=field_metadata)
    message: Optional[str] = field(default=None, metadata=field_metadata)
    data: Optional[Tuple[ContentResponse, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class BulkContentUpdateResponse(Base):
    status: Optional[int] = field(default=None, metadata=field_metadata)
    message: Optional[str] = field(default=None, metadata=field_metadata)
    data: Optional[Tuple[ContentAuditFields, ...]] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ContentCreateRequest(Base):
    name: str = field(default=None, metadata=field_metadata)
    entitlements: Entitlements = field(default=None, metadata=field_metadata)
    entitlement_exclusions: EntitlementExclusions = field(default=None, metadata=field_metadata)
    content: Content = field(default=None, metadata=field_metadata)
    parameters: ContentParameters = field(default=None, metadata=field_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ContentCreateResponse(Base):
    status: Optional[int] = field(default=None, metadata=field_metadata)
    message: Optional[str] = field(default=None, metadata=field_metadata)
    data: Optional[ContentAuditFields] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)


@handle_camel_case_args
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(unsafe_hash=True, repr=False)
class ContentUpdateResponse(Base):
    status: Optional[int] = field(default=None, metadata=field_metadata)
    message: Optional[str] = field(default=None, metadata=field_metadata)
    data: Optional[ContentAuditFields] = field(default=None, metadata=field_metadata)
    name: Optional[str] = field(default=None, metadata=name_metadata)
