import etl_pipeline.jooble.jooble_parser as jooble_parser
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

currencies = ['$','€','£','¥','₹','₩','₽','']

CURRENCY_PATTERNS = {
    "UAH": [
        "uah", "грн", "гривень", "гривні", "гривня", "гривны", "гривен", "гривне",
        "₴", "uahn", "ukrainian hryvnia", "hryvnia", "hryvnas", "грни", "гр"
    ],
    "USD": [
        "usd", "$", "дол", "доллар", "долларов", "доллары", "долар", "доларів",
        "долари", "долл", "баксов", "баксы", "бакси", "баксів", "us dollar", "bucks"
    ],
    "EUR": [
        "eur", "€", "евро", "євро", "евр", "еврик", "евриков", "євріків",
        "euro", "euros", "eur"
    ],
    "PLN": [
        "pln", "zł", "zloty", "злотых", "злотий", "злотих", "зл", "zl",
        "polish zloty", "злоте"
    ],
    "GBP": [
        "gbp", "£", "pound", "pounds", "фунт", "фунтов", "фунтів", "фунти",
        "quid", "sterling"
    ],
    "CZK": [
        "czk", "Kč", "крон", "кроны", "кронi", "чешская крона", "чеська крона"
    ],
    "CAD": [
        "cad", "c$", "cad$", "канадский доллар", "канадський долар"
    ],
    "AUD": [
        "aud", "a$", "aud$", "австралийский доллар", "австралійський долар"
    ],
    "CHF": [
        "chf", "fr", "франк", "франков", "франків", "швейцарский франк"
    ],
    "USDT": [
        "usdt", "tether", "тезер", "криптодоллар", "криптодолар"
    ]
}

STATE_MAPPING = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
    "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
    "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
    "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
    "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
    "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
    "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
    "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
    "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
    "WI": "Wisconsin", "WY": "Wyoming", "DC": "District of Columbia",
    # Common Territories
    "AS": "American Samoa", "GU": "Guam", "MP": "Northern Mariana Islands",
    "PR": "Puerto Rico", "VI": "Virgin Islands"
}
COUNTRY_MAPPING = {
    "AF": "afghanistan", "AX": "aland islands", "AL": "albania", "DZ": "algeria",
    "AS": "american samoa", "AD": "andorra", "AO": "angola", "AI": "anguilla",
    "AQ": "antarctica", "AG": "antigua and barbuda", "AR": "argentina", "AM": "armenia",
    "AW": "aruba", "AU": "australia", "AT": "austria", "AZ": "azerbaijan",
    "BS": "bahamas", "BH": "bahrain", "BD": "bangladesh", "BB": "barbados",
    "BY": "belarus", "BE": "belgium", "BZ": "belize", "BJ": "benin",
    "BM": "bermuda", "BT": "bhutan", "BO": "bolivia", "BA": "bosnia and herzegovina",
    "BW": "botswana", "BV": "bouvet island", "BR": "brazil", "IO": "british indian ocean territory",
    "BN": "brunei darussalam", "BG": "bulgaria", "BF": "burkina faso", "BI": "burundi",
    "KH": "cambodia", "CM": "cameroon", "CA": "canada", "CV": "cape verde",
    "KY": "cayman islands", "CF": "central african republic", "TD": "chad", "CL": "chile",
    "CN": "china", "CX": "christmas island", "CC": "cocos (keeling) islands", "CO": "colombia",
    "KM": "comoros", "CG": "congo", "CD": "congo, democratic republic", "CK": "cook islands",
    "CR": "costa rica", "CI": "cote d'ivoire", "HR": "croatia", "CU": "cuba",
    "CY": "cyprus", "CZ": "czech republic", "DK": "denmark", "DJ": "djibouti",
    "DM": "dominica", "DO": "dominican republic", "EC": "ecuador", "EG": "egypt",
    "SV": "el salvador", "GQ": "equatorial guinea", "ER": "eritrea", "EE": "estonia",
    "ET": "ethiopia", "FK": "falkland islands (malvinas)", "FO": "faroe islands", "FJ": "fiji",
    "FI": "finland", "FR": "france", "GF": "french guiana", "PF": "french polynesia",
    "TF": "french southern territories", "GA": "gabon", "GM": "gambia", "GE": "georgia",
    "DE": "germany", "GH": "ghana", "GI": "gibraltar", "GR": "greece",
    "GL": "greenland", "GD": "grenada", "GP": "guadeloupe", "GU": "guam",
    "GT": "guatemala", "GG": "guernsey", "GN": "guinea", "GW": "guinea-bissau",
    "GY": "guyana", "HT": "haiti", "HM": "heard island & mcdonald islands", "VA": "holy see (vatican city state)",
    "HN": "honduras", "HK": "hong kong", "HU": "hungary", "IS": "iceland",
    "IN": "india", "ID": "indonesia", "IR": "iran, islamic republic of", "IQ": "iraq",
    "IE": "ireland", "IM": "isle of man", "IL": "israel", "IT": "italy",
    "JM": "jamaica", "JP": "japan", "JE": "jersey", "JO": "jordan",
    "KZ": "kazakhstan", "KE": "kenya", "KI": "kiribati", "KR": "korea, republic of",
    "KW": "kuwait", "KG": "kyrgyzstan", "LA": "lao democratic republic", "LV": "latvia",
    "LB": "lebanon", "LS": "lesotho", "LR": "liberia", "LY": "libyan arab jamahiriya",
    "LI": "liechtenstein", "LT": "lithuania", "LU": "luxembourg", "MO": "macao",
    "MK": "macedonia", "MG": "madagascar", "MW": "malawi", "MY": "malaysia",
    "MV": "maldives", "ML": "mali", "MT": "malta", "MH": "marshall islands",
    "MQ": "martinique", "MR": "mauritania", "MU": "mauritius", "YT": "mayotte",
    "MX": "mexico", "FM": "micronesia, federated states of", "MD": "moldova", "MC": "monaco",
    "MN": "mongolia", "ME": "montenegro", "MS": "montserrat", "MA": "morocco",
    "MZ": "mozambique", "MM": "myanmar", "NA": "namibia", "NR": "nauru",
    "NP": "nepal", "NL": "netherlands", "AN": "netherlands antilles", "NC": "new caledonia",
    "NZ": "new zealand", "NI": "nicaragua", "NE": "niger", "NG": "nigeria",
    "NU": "niue", "NF": "norfolk island", "MP": "northern mariana islands", "NO": "norway",
    "OM": "oman", "PK": "pakistan", "PW": "palau", "PS": "palestinian territory, occupied",
    "PA": "panama", "PG": "papua new guinea", "PY": "paraguay", "PE": "peru",
    "PH": "philippines", "PN": "pitcairn", "PL": "poland", "PT": "portugal",
    "PR": "puerto rico", "QA": "qatar", "RE": "reunion", "RO": "romania",
    "RU": "russian federation", "RW": "rwanda", "BL": "saint barthelemy", "SH": "saint helena",
    "KN": "saint kitts and nevis", "LC": "saint lucia", "MF": "saint martin", "PM": "saint pierre and miquelon",
    "VC": "saint vincent and grenadines", "WS": "samoa", "SM": "san marino", "ST": "sao tome and principe",
    "SA": "saudi arabia", "SN": "senegal", "RS": "serbia", "SC": "seychelles",
    "SL": "sierra leone", "SG": "singapore", "SK": "slovakia", "SI": "slovenia",
    "SB": "solomon islands", "SO": "somalia", "ZA": "south africa", "GS": "south georgia & south sandwich islands",
    "ES": "spain", "LK": "sri lanka", "SD": "sudan", "SR": "suriname",
    "SJ": "svalbard and jan mayen", "SZ": "swaziland", "SE": "sweden", "CH": "switzerland",
    "SY": "syrian arab republic", "TW": "taiwan", "TJ": "tajikistan", "TZ": "tanzania",
    "TH": "thailand", "TL": "timor-leste", "TG": "togo", "TK": "tokelau",
    "TO": "tonga", "TT": "trinidad and tobago", "TN": "tunisia", "TR": "turkey",
    "TM": "turkmenistan", "TC": "turks and caicos islands", "TV": "tuvalu", "UG": "uganda",
    "UA": "ukraine", "AE": "united arab emirates", "GB": "united kingdom", "US": "united states",
    "UM": "united states minor outlying islands", "UY": "uruguay", "UZ": "uzbekistan", "VU": "vanuatu",
    "VE": "venezuela", "VN": "viet nam", "VG": "virgin islands, british", "VI": "virgin islands, u.s.",
    "WF": "wallis and futuna", "EH": "western sahara", "YE": "yemen", "ZM": "zambia",
    "ZW": "zimbabwe"
}

def norm():
    gen = jooble_parser.parse()

    normalized_jobs = []
    counter = 0
    while True:
        job = next(gen)
        normalized_job = job.copy()
        # done salary, currency,
        #salary
        multiplier = 1
        salary = normalized_job['salary'].replace('k', '000').strip()
        if salary:
            normalized_job['currency'] = None

            for cur in CURRENCY_PATTERNS.keys():
                for pattern in CURRENCY_PATTERNS[cur]:
                    if pattern in salary:
                        normalized_job['currency'] = cur
                        salary = salary.replace(pattern, '')
                        break
            if 'per hour' in salary:
                multiplier = 2080
                salary = salary.replace('per hour', '')

            elif 'per month' in salary:
                multiplier = 12
                salary = salary.replace('per month', '')

            if '-' in salary:
                min_salary, max_salary = salary.split('-')
                min_salary = min_salary.strip()
                max_salary = max_salary.strip()
                try:
                    if '.' in min_salary:
                        divider = len(min_salary) - min_salary.find('.') - 1
                        if 'k' in normalized_job['salary']:
                            divider -= 3
                        #print(f'{divider = }\n{len(min_salary) = }\n{min_salary.find('.') = }\n{min_salary = }')
                        #print('### here ###')
                        min_salary = min_salary.replace('.', '')
                        normalized_job['min_salary'] = int(min_salary) * multiplier // (10 ** divider)
                    else:
                        normalized_job['min_salary'] = int(min_salary) * multiplier

                    if '.' in max_salary:
                        divider = len(max_salary) - max_salary.find('.') - 1
                        if 'k' in normalized_job['salary']:
                            divider -= 3

                        #print(f'{divider = }\n{salary = }\n{salary.find(".") = }')
                        #print('### here ###')

                        max_salary = max_salary.replace('.', '')
                        normalized_job['max_salary'] = int(max_salary) * multiplier // (10 ** divider)
                    else:
                        normalized_job['max_salary'] = int(max_salary) * multiplier

                except ValueError:
                    normalized_job['min_salary'] = None
                    normalized_job['max_salary'] = None
                    logger.error(f'-Salary {salary} is not a number')
            else:
                try:
                    if '.' in salary:
                        divider = len(salary) - salary.find('.') - 1
                        if 'k' in normalized_job['salary']:
                            divider -= 3
                        #print(f'{divider = }\n{salary = }\n{salary.find(".") = }')
                        #print('### here ###')
                        min_salary = min_salary.replace('.', '')
                        normalized_job['min_salary'] = int(salary) * multiplier // (10 ** divider)
                        normalized_job['max_salary'] = int(salary) * multiplier // (10 ** divider)
                    else:
                        normalized_job['min_salary'] = int(salary) * multiplier
                        normalized_job['max_salary'] = int(salary) * multiplier

                except ValueError:
                    normalized_job['min_salary'] = None
                    normalized_job['max_salary'] = None
                    logger.error(f'Salary {salary} is not a number')
        else:
            normalized_job['min_salary'] = None
            normalized_job['max_salary'] = None
            normalized_job['currency'] = None

        #location
        location = normalized_job['location']
        normalized_job['location_city'] = None
        normalized_job['location_country'] = None
        if 'Remote' in location:
            normalized_job['location'] = None
        else:
            if ',' in location:
                normalized_job['location_city'] = location.split(',')[0].strip()

                try:
                    normalized_job['location_country'] = STATE_MAPPING[location.split(',')[1].strip().upper()] #country or state
                except KeyError:
                    normalized_job['location_country'] = None
                    logger.error(f'State {location.split(",")[1].strip()} is not a valid state')
            else:
                if location in STATE_MAPPING.values() or location.lower() in COUNTRY_MAPPING.values():
                    normalized_job['location_city'] = None
                    normalized_job['location_country'] = location
                else:
                    normalized_job['location_city'] = location
                    normalized_job['location_country'] = None

        normalized_job['last_updated'] = normalized_job['last_updated'].replace('T', ' ').split('.')[0]

        counter += 1

        del normalized_job['salary']

        #for key in normalized_job.keys():
        #    #print(key, ' : ', normalized_job[key])
        ##print(f' Normed job #{counter} ')

       # #print('\n\n\n\n')
        yield normalized_job

def normalize():
    gen = norm()
    while True:
        try:
            obj = next(gen)
        except StopIteration:
            logger.info('SI: No more jobs to normalize, finishing normalization')
            break
        except RuntimeError:
            logger.info('RE: No more jobs to normalize, finishing normalization')
            break
        if obj is None:
            logger.error('Job object is empty,  finishing normalization')
            break
        logger.info(f'Normed job:{obj.get("external_id")}, saving...')
        yield obj






