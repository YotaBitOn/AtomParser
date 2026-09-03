import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

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

ukraine_cities_map = {
    "Київ": "Kyiv",
    "Харків": "Kharkiv",
    "Одеса": "Odesa",
    "Дніпро": "Dnipro",
    "Донецьк": "Donetsk",
    "Львів": "Lviv",
    "Запоріжжя": "Zaporizhzhia",
    "Кривий Ріг": "Kryvyi Rih",
    "Севастополь": "Sevastopol",
    "Миколаїв": "Mykolaiv",
    "Маріуполь": "Mariupol",
    "Луганськ": "Luhansk",
    "Вінниця": "Vinnytsia",
    "Макіївка": "Makiivka",
    "Сімферополь": "Simferopol",
    "Херсон": "Kherson",
    "Полтава": "Poltava",
    "Чернігів": "Chernihiv",
    "Черкаси": "Cherkasy",
    "Житомир": "Zhytomyr",
    "Суми": "Sumy",
    "Хмельницький": "Khmelnytskyi",
    "Горлівка": "Horlivka",
    "Рівне": "Rivne",
    "Кропивницький": "Kropyvnytskyi",
    "Кам'янське": "Kamianske",
    "Чернівці": "Chernivtsi",
    "Кременчук": "Kremenchuk",
    "Івано-Франківськ": "Ivano-Frankivsk",
    "Тернопіль": "Ternopil",
    "Біла Церква": "Bila Tserkva",
    "Луцьк": "Lutsk",
    "Краматорськ": "Kramatorsk",
    "Мелітополь": "Melitopol",
    "Керч": "Kerch",
    "Нікополь": "Nikopol",
    "Слов'янськ": "Sloviansk",
    "Ужгород": "Uzhhorod",
    "Бердянськ": "Berdiansk",
    "Алчевськ": "Alchevsk",
    "Павлоград": "Pavlohrad",
    "Сєвєродонецьк": "Severodonetsk",
    "Євпаторія": "Evpatoria",
    "Лисичанськ": "Lysychansk",
    "Кам'янець-Подільський": "Kamianets-Podilskyi",
    "Бровари": "Brovary",
    "Конотоп": "Konotop",
    "Умань": "Uman",
    "Мукачево": "Mukachevo",
    "Олександрія": "Oleksandriia",
    "Кришталевий": "Kryshtalevyi",
    "Єнакієве": "Yenakiieve",
    "Шостка": "Shostka",
    "Бердичів": "Berdychiv",
    "Ялта": "Yalta",
    "Бахмут": "Bakhmut",
    "Кадіївка": "Kadiivka",
    "Дрогобич": "Drohobych",
    "Костянтинівка": "Kostiantynivka",
    "Ніжин": "Nizhyn",
    "Ізмаїл": "Izmail",
    "Новомосковськ": "Novomoskovsk",
    "Феодосія": "Feodosia",
    "Ковель": "Kovel",
    "Сміла": "Smila",
    "Червоноград": "Chervonohrad",
    "Калуш": "Kalush",
    "Первомайськ": "Pervomaisk",
    "Коростень": "Korosten",
    "Довжанськ": "Dovzhansk",
    "Покровськ": "Pokrovsk",
    "Коломия": "Kolomyia",
    "Бориспіль": "Boryspil",
    "Рубіжне": "Rubizhne",
    "Чорноморськ": "Chornomorsk",
    "Стрий": "Stryi",
    "Дружківка": "Druzhkivka",
    "Харцизьк": "Khartsyzk",
    "Прилуки": "Pryluky",
    "Лозова": "Lozova",
    "Чистякове": "Chystiakove",
    "Новоград-Волинський": "Novohrad-Volynskyi",
    "Енергодар": "Enerhodar",
    "Антрацит": "Antratsyt",
    "Нововолинськ": "Novovolynsk",
    "Горішні Плавні": "Horishni Plavni",
    "Ізюм": "Izium",
    "Шахтарськ": "Shakhtarsk",
    "Білгород-Дністровський": "Bilhorod-Dnistrovskyi",
    "Мирноград": "Myrnohrad",
    "Охтирка": "Okhtyrka",
    "Марганець": "Marhanets",
    "Фастів": "Fastiv",
    "Сніжне": "Snizhne",
    "Нова Каховка": "Nova Kakhovka",
    "Лубни": "Lubny",
    "Ровеньки": "Rovenky",
    "Жовті Води": "Zhovti Vody",
    "Брянка": "Brianka",
    "Світловодськ": "Svitlovodsk"
}

emp_mapping = {
    'Повна зайнятість' : 'Full Time',
    'Неповна зайнятість': 'Part Time',
}

numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ' ']

READ_MODE = 'json' # will be obtained from a config file
normalized_jobs = []

def connect_parser():
    gen = workua_parser.parse()
    #currecy yes, salary yes, location no

    counter = 0
    while True:
        try:
            job = next(gen)
        except StopIteration:
            logger.info(f'Finished parsing {counter} jobs')
            break
        if not job:
            logger.error(f'No job found, skipping...')
            continue

        norm(job)
        counter += 1
        print(f'Normed job #{counter}')
        print(f'\n\n\n\n\n')
        normalized_jobs.append(job)

def read_data():
    import json
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    counter = 0
    for job in data:
        norm(job)

        counter += 1
        print(f'Normed job #{counter}')
        print(f'\n\n\n\n\n')
        normalized_jobs.append(job)

def norm(job):
        normalized_job = job.copy()

        normalized_job['employment_type'] = emp_mapping.get(normalized_job['employment_type'])

        normalized_job['currency'] = None
        normalized_job['location_country'] = 'ukraine'

        for i in range(len(normalized_job['tags'])):
            normalized_job['tags'][i] = normalized_job['tags'][i].lower()

        salary = normalized_job['salary']

        if salary:
            salary = salary.replace(' ', '')
            normalized_job['currency'] = None
            for cur in CURRENCY_PATTERNS.keys():
                for pattern in CURRENCY_PATTERNS[cur]:
                    if pattern in salary:
                        normalized_job['currency'] = cur
                        salary = salary.replace(pattern, '')
                        break

            salary_numb = ''
            salary_numbs = []

            for symbol in salary:
                if symbol in numbers:
                    salary_numb += symbol
                elif salary_numb.strip():
                    salary_numbs.append(int(salary_numb))
                    salary_numb = ''
            if salary_numb.strip():
                salary_numbs.append(int(salary_numb))

            if len(salary_numbs):
                normalized_job['min_salary'] = min(salary_numbs)
                normalized_job['max_salary'] = max(salary_numbs)

            else:
                normalized_job['min_salary'] = None
                normalized_job['max_salary'] = None
        else:
            normalized_job['min_salary'] = None
            normalized_job['max_salary'] = None

        location = normalized_job['location']
        if location:
            location = location.split(',')
            if 'Вся Україна' in location:
                normalized_job['location_city'] = None
            if len(location) == 1:
                normalized_job['location_city'] = location[0].strip()
        else:
            normalized_job['location_city'] = None

        del normalized_job['salary']
        del normalized_job['location']
        for k, v in normalized_job.items():
            print(k, ' : ', v)

if READ_MODE == 'json':
    read_data()
elif READ_MODE == 'parser':
    import workua_parser
    connect_parser()