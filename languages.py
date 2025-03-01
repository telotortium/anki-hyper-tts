import enum

class Language(enum.Enum):
    af = ("Afrikaans")
    sq = ("Albanian")
    am = ("Amharic")
    ar = ("Arabic")
    hy = ("Armenian")
    az = ("Azerbaijani")
    eu = ("Basque")
    ba = ("Bashkir")
    bo = ("Tibetan")
    be = ("Belarusian")
    bn = ("Bangla")
    bs = ("Bosnian")
    bg = ("Bulgarian")
    ca = ("Catalan")
    ceb = ("Cebuano")
    ny = ("Chichewa")
    co = ("Corsican")
    hr = ("Croatian")
    cs = ("Czech")
    da = ("Danish")
    dv = ("Divehi")
    nl = ("Dutch")
    en = ("English")
    eo = ("Esperanto")
    et = ("Estonian")
    tl = ("Filipino")
    fi = ("Finnish")
    fr = ("French")
    fy = ("Frisian")
    gl = ("Galician")
    ka = ("Georgian")
    de = ("German")
    el = ("Greek")
    gu = ("Gujarati")
    ht = ("Haitian Creole")
    ha = ("Hausa")
    haw = ("Hawaiian")
    iw = ("Hebrew")
    iu = ("Inuktitut")
    hi = ("Hindi")
    hmn = ("Hmong")
    hu = ("Hungarian")
    is_ = ("Icelandic")
    ig = ("Igbo")
    id_ = ("Indonesian")
    ga = ("Irish")
    it = ("Italian")
    ja = ("Japanese")
    jw = ("Javanese")
    kn = ("Kannada")
    kk = ("Kazakh")
    km = ("Khmer")
    rw = ("Kinyarwanda")
    ko = ("Korean")
    ku = ("Kurdish (Central)")
    ky = ("Kyrgyz")
    lo = ("Lao")
    la = ("Latin")
    lv = ("Latvian")
    lt = ("Lithuanian")
    lb = ("Luxembourgish")
    mk = ("Macedonian")
    mg = ("Malagasy")
    ms = ("Malay")
    ml = ("Malayalam")
    mt = ("Maltese")
    mi = ("Maori")
    mr = ("Marathi")
    mn = ("Mongolian")
    mn_cyrl = ("Mongolian (Cyrillic)")
    cnr = ("Montenegrin")
    my = ("Myanmar (Burmese)")
    ne = ("Nepali")
    no = ("Norwegian")
    or_ = ("Odia")
    ps = ("Pashto")
    fa = ("Persian")
    pl = ("Polish")
    pt_br = ("Portuguese (Brazil)")
    pa = ("Punjabi")
    ro = ("Romanian")
    ru = ("Russian")
    sm = ("Samoan")
    gd = ("Scots Gaelic")
    st = ("Sesotho")
    sn = ("Shona")
    sd = ("Sindhi")
    si = ("Sinhala")
    sk = ("Slovak")
    sl = ("Slovenian")
    so = ("Somali")
    es = ("Spanish")
    es_mx = ("Spanish (Mexico)")
    su = ("Sundanese")
    sw = ("Swahili")
    sv = ("Swedish")
    tg = ("Tajik")
    ta = ("Tamil")
    tt = ("Tatar")
    te = ("Telugu")
    th = ("Thai")
    ti = ("Tigrinya")
    tr = ("Turkish")
    tk = ("Turkmen")
    uk = ("Ukrainian")
    ur = ("Urdu")
    ug = ("Uyghur")
    uz = ("Uzbek")
    vi = ("Vietnamese")
    cy = ("Welsh")
    xh = ("Xhosa")
    yi = ("Yiddish")
    yo = ("Yoruba")
    zu = ("Zulu")
    he = ("Hebrew")
    as_ = ("Assamese")
    fil = ("Filipino")
    fj = ("Fijian")
    fr_ca = ("French (Canada)")
    kmr = ("Kurdish (Northern)")
    mww = ("Hmong Daw")
    nb = ("Norwegian")
    otq = ("Querétaro Otomi")
    prs = ("Dari")
    pt_pt = ("Portuguese (Portugal)")
    sr_cyrl = ("Serbian (Cyrillic)")
    sr_latn = ("Serbian (Latin)")
    tlh_latn = ("Klingon (Latin)")
    tlh_piqd = ("Klingon (pIqaD)")
    to = ("Tongan")
    ty = ("Tahitian")
    yua = ("Yucatec Maya")
    yue = ("Chinese (Cantonese, Traditional)")
    zh_cn = ("Chinese (Simplified)")
    zh_tw = ("Chinese (Traditional)")
    zh_lit = ("Chinese (Literary)")


    def __init__(self, lang_name):
        self.lang_name = lang_name        

class AudioLanguage(enum.Enum):
    af_ZA = (Language.af, "Afrikaans (South Africa)")
    am_ET = (Language.am, "Amharic (Ethiopia)")
    # arabic
    ar_AE = (Language.ar, "Arabic (United Arab Emirates)")
    ar_BH = (Language.ar, "Arabic (Bahrain)")
    ar_DZ = (Language.ar, "Arabic (Algeria)")
    ar_EG = (Language.ar, "Arabic (Egypt)")
    ar_IQ = (Language.ar, "Arabic (Iraq)")
    ar_JO = (Language.ar, "Arabic (Jordan)")
    ar_KW = (Language.ar, "Arabic (Kuwait)")
    ar_LY = (Language.ar, "Arabic (Libya)")
    ar_MA = (Language.ar, "Arabic (Morocco)")
    ar_QA = (Language.ar, "Arabic (Qatar)")
    ar_SA = (Language.ar, "Arabic (Saudi Arabia)")
    ar_SY = (Language.ar, "Arabic (Syria)")
    ar_TN = (Language.ar, "Arabic (Tunisia)")
    ar_XA = (Language.ar, "Arabic")
    ar_YE = (Language.ar, "Arabic (Yemen)")
    
    bg_BG = (Language.bg, "Bulgarian")
    bn_BD = (Language.bn, "Bangla (Bangladesh)")
    bn_IN = (Language.bn, "Bengali (India)")
    ca_ES = (Language.ca, "Catalan")
    cs_CZ = (Language.cs, "Czech")
    cy_GB = (Language.cy, "Welsh")
    da_DK = (Language.da, "Danish")
    de_AT = (Language.de, "German (Austria)")
    de_CH = (Language.de, "German (Switzerland)")
    de_DE = (Language.de, "German (Germany)")
    el_GR = (Language.el, "Greek")
    en_AU = (Language.en, "English (Australia)")
    en_CA = (Language.en, "English (Canada)")
    en_GB = (Language.en, "English (UK)")
    en_GB_WLS = (Language.en, "English (Welsh)")
    en_IE = (Language.en, "English (Ireland)")
    en_HK = (Language.en, "English (Hong Kong)")
    en_IN = (Language.en, "English (India)")
    en_KE = (Language.en, "English (Kenya)")
    en_NG = (Language.en, "English (Nigeria)")
    en_US = (Language.en, "English (US)")
    en_NZ = (Language.en, "English (New Zealand)")
    en_PH = (Language.en, "English (Philippines)")
    en_SG = (Language.en, "English (Singapore)")
    en_TZ = (Language.en, "English (Tanzania)")
    en_ZA = (Language.en, "English (South Africa)")
    eo_XX = (Language.eo, "Esperanto")
    # spanish
    es_AR = (Language.es, "Spanish (Argentina)")
    es_BO = (Language.es, "Spanish (Bolivia)")
    es_CL = (Language.es, "Spanish (Chile)")
    es_CO = (Language.es, "Spanish (Colombia)")
    es_CR = (Language.es, "Spanish (Costa Rica)")
    es_CU = (Language.es, "Spanish (Cuba)")
    es_DO = (Language.es, "Spanish (Dominican Republic)")
    es_EC = (Language.es, "Spanish (Ecuador)")
    es_ES = (Language.es, "Spanish (Spain)")
    es_GQ = (Language.es, "Spanish (Equatorial Guinea)")
    es_GT = (Language.es, "Spanish (Guatemala)")
    es_HN = (Language.es, "Spanish (Honduras)")
    es_LA = (Language.es, "Spanish (Latin America)")
    es_MX = (Language.es, "Spanish (Mexico)")
    es_NI = (Language.es, "Spanish (Nicaragua)")
    es_PA = (Language.es, "Spanish (Panama)")
    es_PE = (Language.es, "Spanish (Peru)")
    es_PR = (Language.es, "Spanish (Puerto Rico)")
    es_PY = (Language.es, "Spanish (Paraguay)")
    es_SV = (Language.es, "Spanish (El Salvador)")
    es_US = (Language.es, "Spanish (North America)")
    es_UY = (Language.es, "Spanish (Uruguay)")
    es_VE = (Language.es, "Spanish (Venezuela)")

    et_EE = (Language.et, "Estonian")
    fi_FI = (Language.fi, "Finnish")
    fil_PH = (Language.tl, "Filipino (Philippines)")
    fr_BE = (Language.fr, "French (Belgium)")
    fr_CA = (Language.fr_ca, "French (Canada)")
    fr_CH = (Language.fr, "French (Switzerland)")
    fr_FR = (Language.fr, "French (France)")
    ga_IE = (Language.ga, "Irish (Ireland)")
    gl_ES = (Language.gl, "Galician (Spain)")
    gd_GB = (Language.gd, "Gaelic (UK)")
    gu_IN = (Language.gu, "Gujarati (India)")
    he_IL = (Language.he, "Hebrew (Israel)")
    hi_IN = (Language.hi, "Hindi (India)")
    hr_HR = (Language.hr, "Croatian")
    hu_HU = (Language.hu, "Hungarian")
    id_ID = (Language.id_, "Indonesian")
    is_IS = (Language.is_, "Icelandic")
    it_IT = (Language.it, "Italian")
    ja_JP = (Language.ja, "Japanese")
    jv_ID = (Language.jw, "Javanese (Indonesia)")
    ko_KR = (Language.ko, "Korean")
    kk_KZ = (Language.kk, "Kazakh (Kazakhstan)")
    kn_IN = (Language.kn, "Kannada (India)")
    km_KH = (Language.km, "Khmer (Cambodia)")
    lo_LA = (Language.lo, "Lao (Lao People's Democratic Republic")
    lt_LT = (Language.lt, "Lithuanian")
    lv_LV = (Language.lv, "Latvian")
    mk_MK = (Language.mk, "Macedonian (Macedonia)")
    ml_IN = (Language.ml, "Malayalam (India)")
    mr_IN = (Language.mr, "Marathi (India)")
    ms_MY = (Language.ms, "Malay")
    mt_MT = (Language.mt, "Maltese (Malta)")
    my_MM = (Language.my, "Burmese (Myanmar [Burma])")
    nb_NO = (Language.nb, "Norwegian")
    nl_BE = (Language.nl, "Dutch (Belgium)")
    nl_NL = (Language.nl, "Dutch")
    pa_IN = (Language.pa, "Punjabi (India)")
    pl_PL = (Language.pl, "Polish")
    ps_AF = (Language.ps, "Pashto (Afghanistan)")
    pt_BR = (Language.pt_br, "Portuguese (Brazil)")
    pt_PT = (Language.pt_pt, "Portuguese (Portugal)")
    ro_RO = (Language.ro, "Romanian")
    ru_RU = (Language.ru, "Russian")
    si_LK = (Language.si, "Sinhala (Sri Lanka)")
    sk_SK = (Language.sk, "Slovak")
    sl_SI = (Language.sl, "Slovenian")
    so_SO = (Language.so, "Somali (Somalia)")
    sr_RS = (Language.sr_cyrl, "Serbian (Serbia)")
    su_ID = (Language.su, "Sundanese (Indonesia)")
    sv_SE = (Language.sv, "Swedish")
    sw_KE = (Language.sw, "Swahili (Kenya)")
    sw_TZ = (Language.sw, "Swahili (Tanzania)")
    ta_IN = (Language.ta, "Tamil (India)")
    ta_LK = (Language.ta, "Tamil (Sri Lanka)")
    ta_SG = (Language.ta, "Tamil (Singapore)")
    te_IN = (Language.te, "Telugu (India)")
    th_TH = (Language.th, "Thai")
    tr_TR = (Language.tr, "Turkish (Turkey)")
    ur_IN = (Language.ur, "Urdu (India)")
    ur_PK = (Language.ur, "Urdu (Pakistan)")
    uk_UA = (Language.uk, "Ukrainian (Ukraine)")
    uz_UZ = (Language.uz, "Uzbek (Uzbekistan)")
    vi_VN = (Language.vi, "Vietnamese")
    zh_CN = (Language.zh_cn, "Chinese (Mandarin, Simplified)")
    zh_HK = (Language.yue, "Chinese (Cantonese, Traditional)")
    zh_TW = (Language.zh_tw, "Chinese (Taiwanese Mandarin)")
    fa_IR = (Language.fa, "Persian (Iran)")
    zu_ZA = (Language.zu, "Zulu (South Africa)")

    def __init__(self, lang, audio_lang_name):
        self.lang = lang
        self.audio_lang_name = audio_lang_name    