import re


class AmbiguousToken:

    def __init__(self):
        self.dateAndTimePatterns = [
            # MM/DD/YYYY or MM\DD\YYYY  MM-DD-YYYY
            "(([0][1-9])|([1][0-2]))[\\\/-](([0][1-9])|([1-2][0-9])|([3][0-1]))[\\\/-](([2][0-1])|([1][6-9]))[0-9][0-9]",
            # DD/MM/YYYY or DD\MM\YYYY or DD-MM-YYYY
            "([0-2][0-9]|[3][0-1])[\\\/-]([0]\d|[1][0-2])[\\\/-](([2][01])|([1][6-9]))\d{2}",
            # YYYY-MM-DD or YYYY\MM\DD or YYYY\MM\DD
            "((([2][01])|([1][6-9]))\d{2})[\\\/-]((0[1-9])|(1[0-2]))[\\\/-](0[1-9]|[12][0-9]|3[01])",
            # YYYY-DD-MM or YYYY\DD\MM or YYYY\DD\MM
            "((([2][01])|([1][6-9]))\d{2})[\\\/-](0[1-9]|[12][0-9]|3[01])[\\\/-]((0[1-9])|(1[0-2]))",
            # 00:00:00 to 12:00:00 or 00:00:00 AM to 12:00:00 PM
            "((0[0-9])|(1[0-2]))(\:)((0[0-9])|(1[0-9])|(2[0-9])|(3[0-9])|(4[0-9])|(5[0-9]))((\:)((0[0-9])|(1[0-9])|(2[0-9])|(3[0-9])|(4[0-9])|(5[0-9])))?([ ]?[ap]m)?",
            # 00:00:00 to 23:59:59
            "((1[3-9])|(2[0-3]))(\:)((0[0-9])|(1[0-9])|(2[0-9])|(3[0-9])|(4[0-9])|(5[0-9]))((\:)((0[0-9])|(1[0-9])|(2[0-9])|(3[0-9])|(4[0-9])|(5[0-9])))?",
            # dd (st,nd,th) MM ( yyyy or yy )
            "(((3[0-1])|(2[0-9])|(1[0-9])|([1-9]))(st|nd|th)?[ ])(((jan(uary)?)|(feb(ruary)?)|(mar(ch)?)|(may)|(apr(il)?)|(june?)|(july?)|(aug(ust)?)|(sep(tember)?)|((nov|dec)(ember)?)|(oct(ober)?))[ ]?)((([2][01])|([1][6-9]))?([0-9][0-9]))",
            # MM dd,yyyy  --> Jul 30,2015
            "(((jan(uary)?)|(feb(ruary)?)|(mar(ch)?)|(may)|(apr(il)?)|(june?)|(july?)|(aug(ust)?)|(sep(tember)?)|((nov|dec)(ember)?)|(oct(ober)?))[ ])(((3[0-1])|(2[0-9])|(1[0-9])|(0?[1-9]))),((([2][01])|([1][6-9]))([0-9][0-9]))",
            # CAP date time --> 2016-04-07T12:29:00-04:00
            "(?:[2-9]\d\d\d)-(?:1[012]|0?[1-9])?-(?:31(?!.(?:0?[2469]|11))|(?:30|29)(?!.0?2)|29(?=.0?2.(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00)))(?:T))|(?:2[0-8]|1\d|0?[1-9]))T(2[01234]|[01]\d):[0-5]\d:[0-5]\d[+-][01]\d:[0-5]\d"
        ]

        self.shortCurrency = ['$', '€', '¢', '£', '¥', 'zl', '%']  # ('@','#')
        self.currencySymbol = ['usd', 'eur', 'crc', 'gbp', 'jpy', 'pln', 'per']
        self.Currency = ['usa dolar', 'euro', 'costa rican colón', 'british pound sterling', 'japanese yen', 'polish zloty',
                    'percent']

        self.currencyNames = ['AED', 'AFN', 'ALL', 'AFN', 'ARS', 'AWG', 'AUD', 'AZN', 'BSD', 'BBD', 'BDT', 'BYR', 'BZD',
                         'BMD', 'BOB', 'BAM', 'BWP', 'BGN', 'BRL', 'BND', 'KHR', 'CAD', 'KYD', 'CLP', 'CNY', 'COP',
                         'CRC', 'HRK', 'CUP', 'CZK', 'DKK', 'DOP', 'XCD', 'EGP', 'SVC', 'EEK', 'EUR', 'FKP', 'FJD',
                         'GHC', 'GIP', 'GTQ', 'GGP', 'GYD', 'HNL', 'HKD', 'HUF', 'ISK', 'INR', 'IDR', 'IRR', 'IMP',
                         'ILS', 'JMD', 'JPY', 'JEP', 'KZT', 'KPW', 'KRW', 'KGS', 'LAK', 'LVL', 'LBP', 'LRD', 'LTL',
                         'MKD', 'MYR', 'MUR', 'MXN', 'MNT', 'MZN', 'NAD', 'NPR', 'ANG', 'NZD', 'NIO', 'NGN', 'NOK',
                         'OMR', 'PKR', 'PAB', 'PYG', 'PEN', 'PHP', 'PLN', 'QAR', 'RON', 'RUB', 'SHP', 'SAR', 'RSD',
                         'SCR', 'SGD', 'SBD', 'SOS', 'ZAR', 'LKR', 'SEK', 'CHF', 'SRD', 'SYP', 'TWD', 'THB', 'TTD',
                         'TRY', 'TRL', 'TVD', 'UAH', 'GBP', 'USD', 'UYU', 'UZS', 'VEF', 'VND', 'YER', 'ZWD']
        self.currencyCountry = ['United Arab Emirates dirham', 'Afghan afghani', 'Albania Lek', 'Afghanistan Afghani',
                           'Argentina Peso', 'Aruba Guilder', 'Australia Dollar', 'Azerbaijan New Manat',
                           'Bahamas Dollar', 'Barbados Dollar', 'Bangladeshi taka', 'Belarus Ruble', 'Belize Dollar',
                           'Bermuda Dollar', 'Bolivia Boliviano', 'Bosnia and Herzegovina Convertible Marka',
                           'Botswana Pula', 'Bulgaria Lev', 'Brazil Real', 'Brunei Darussalam Dollar', 'Cambodia Riel',
                           'Canada Dollar', 'Cayman Islands Dollar', 'Chile Peso', 'China Yuan Renminbi',
                           'Colombia Peso', 'Costa Rica Colon', 'Croatia Kuna', 'Cuba Peso', 'Czech Republic Koruna',
                           'Denmark Krone', 'Dominican Republic Peso', 'East Caribbean Dollar', 'Egypt Pound',
                           'El Salvador Colon', 'Estonia Kroon', 'Euro Member Countries',
                           'Falkland Islands (Malvinas) Pound', 'Fiji Dollar', 'Ghana Cedis', 'Gibraltar Pound',
                           'Guatemala Quetzal', 'Guernsey Pound', 'Guyana Dollar', 'Honduras Lempira',
                           'Hong Kong Dollar', 'Hungary Forint', 'Iceland Krona', 'India Rupee', 'Indonesia Rupiah',
                           'Iran Rial', 'Isle of Man Pound', 'Israel Shekel', 'Jamaica Dollar', 'Japan Yen',
                           'Jersey Pound', 'Kazakhstan Tenge', 'Korea  North Won', 'Korea South Won', 'Kyrgyzstan Som',
                           'Laos Kip', 'Latvia Lat', 'Lebanon Pound', 'Liberia Dollar', 'Lithuania Litas',
                           'Macedonia Denar', 'Malaysia Ringgit', 'Mauritius Rupee', 'Mexico Peso', 'Mongolia Tughrik',
                           'Mozambique Metical', 'Namibia Dollar', 'Nepal Rupee', 'Netherlands Antilles Guilder',
                           'New Zealand Dollar', 'Nicaragua Cordoba', 'Nigeria Naira', 'Norway Krone', 'Oman Rial',
                           'Pakistan Rupee', 'Panama Balboa', 'Paraguay Guarani', 'Peru Nuevo Sol', 'Philippines Peso',
                           'Poland Zloty', 'Qatar Riyal', 'Romania New Leu', 'Russia Ruble', 'Saint Helena Pound',
                           'Saudi Arabia Riyal', 'Serbia Dinar', 'Seychelles Rupee', 'Singapore Dollar',
                           'Solomon Islands Dollar', 'Somalia Shilling', 'South Africa Rand', 'Sri Lanka Rupee',
                           'Sweden Krona', 'Switzerland Franc', 'Suriname Dollar', 'Syria Pound', 'Taiwan New Dollar',
                           'Thailand Baht', 'Trinidad and Tobago Dollar', 'Turkey Lira', 'Turkey Lira', 'Tuvalu Dollar',
                           'Ukraine Hryvna', 'United Kingdom Pound', 'United States Dollar', 'Uruguay Peso',
                           'Uzbekistan Som', 'Venezuela Bolivar', 'Viet Nam Dong''Yemen Rial', 'Zimbabwe Dollar']

        self.ShortCommon = ['bro', 'mom', 'vip', '3d', 'ID', 'I.Q', 'DIY', 'T.G.I.F', 'R.I.P', 'KIT', 'POV', 'ASAP', 'FYI',
                       'YTD', 'OT', 'NDA', 'B2B', 'B2C', 'HR', 'PR', 'CEO', 'CFO', 'CTO', 'VP', 'MBA', 'CPA', 'OMG',
                       'NSFW', 'TBH', 'IMHO', 'BRB', 'TTYL', 'BTW', 'BC', 'PM', 'etc', 'RSVP', 'ATM', 'AKA', 'IQ',
                       'e.g', 'PIN', 'www', 'ISP', 'CD', 'OS', 'CPU', 'I/O', 'PC', 'IP', 'CEO', 'MGR', 'DEPT', 'ASST',
                       'DIR', 'ACCT', 'V.P']
        self.Commons = ['brother', 'mother', 'very important person', '3-dimensional', 'identification',
                   'Intelligence quotient', 'do-it-yourself', 'thanks God its friday', 'rest in peace', 'keep in touch',
                   'point of view', 'as soon as possible', 'for your information', 'Year-to-date', 'OverTime',
                   'Non-disclosure agreement', 'business to business', 'business to consumer', 'Human Resources',
                   'public relations', 'Cheif executive officer', 'Cheif financial officer', 'Cheif technology officer',
                   'Vice president', 'masters of business administration', 'certified public accountanty', 'oh my God',
                   'Not safe for work', 'to be honest', 'in my honest opinion', 'be right back', 'talk to you later',
                   'by the way', 'befor Christ', 'prime minister', 'et cetera', 'please respond',
                   'automated teller machine', 'also know as', 'intelligence quotient', 'for example',
                   'personal identification number', 'world wide web', 'internet server Provider', 'Compact Disk',
                   'operation System', 'central operation system', 'input/output', 'personal computer',
                   'internet protocol', 'Cheif executive officer', 'manager', 'department', 'association', 'director',
                   'account', 'vice-president']

        self.country = ['North Atlantic Treaty Organization', 'nato', 'afghanistan', 'af', 'albania', 'al', 'algeria', 'dz',
                   'american samoa', 'as', 'andorra', 'ad', 'angola', 'ao', 'anguilla', 'ai', 'antarctica', 'aq',
                   'antigua and barbuda', 'ag', 'argentina', 'ar', 'armenia', 'am', 'aruba', 'aw', 'australia', 'au',
                   'austria', 'at', 'azerbaijan', 'az', 'bahamas', 'bs', 'bahrain', 'bh', 'bangladesh', 'bd',
                   'barbados', 'bb', 'belarus', 'by', 'belgium', 'be', 'belize', 'bz', 'benin', 'bj', 'bermuda', 'bm',
                   'bhutan', 'bt', 'bolivia', 'bo', 'bosnia and herzegovina', 'ba', 'botswana', 'bw', 'bouvet island',
                   'bv', 'brazil', 'br', 'british indian ocean territory', 'io', 'brunei darussalam', 'bn', 'bulgaria',
                   'bg', 'burkina faso', 'bf', 'burundi', 'bi', 'cambodia', 'kh', 'cameroon', 'cm', 'canada', 'ca',
                   'cape verde', 'cv', 'cayman islands', 'ky', 'central african republic', 'cf', 'chad', 'td', 'chile',
                   'cl', 'china', 'cn', 'christmas island', 'cx', 'cocos islands', 'cc', 'colombia', 'co', 'comoros',
                   'km', 'congo', 'cg', 'democratic', 'cd', 'cook islands', 'ck', 'costa rica', 'cr', 'cote divoire',
                   'ci', 'croatia', 'hr', 'cuba', 'cu', 'cyprus', 'cy', 'czech', 'cz', 'denmark', 'dk', 'djibouti',
                   'dj', 'dominica', 'dm', 'dominican', 'do', 'east timor', 'tp', 'ecuador', 'ec', 'egypt', 'eg',
                   'el salvador', 'sv', 'equatorial guinea', 'gq', 'eritrea', 'er', 'estonia', 'ee', 'ethiopia', 'et',
                   'falkland islands', 'fk', 'faroe islands', 'fo', 'fiji', 'fj', 'finland', 'fi', 'france', 'fr',
                   'french guiana', 'gf', 'french polynesia', 'pf', 'french southern territories', 'tf', 'gabon', 'ga',
                   'gambia', 'gm', 'georgia', 'ge', 'germany', 'de', 'ghana', 'gh', 'gibraltar', 'gi', 'greece', 'gr',
                   'greenland', 'gl', 'grenada', 'gd', 'guadeloupe', 'gp', 'guam', 'gu', 'guatemala', 'gt', 'guinea',
                   'gn', 'guinea-bissau', 'gw', 'guyana', 'gy', 'haiti', 'ht', 'heard mcdonald islands', 'hm',
                   'holy see', 'va', 'honduras', 'hn', 'hong kong', 'hk', 'hungary', 'hu', 'iceland', 'is', 'india',
                   'in', 'indonesia', 'id', 'iran islamic republic', 'ir', 'iraq', 'iq', 'ireland', 'ie', 'israel',
                   'il', 'italy', 'it', 'jamaica', 'jm', 'japan', 'jp', 'jordan', 'jo', 'kazakstan', 'kz', 'kenya',
                   'ke', 'kiribati', 'ki', 'korea democratic peoples republic', 'kp', 'korea republic', 'kr', 'kuwait',
                   'kw', 'kyrgyzstan', 'kg', 'lao peoples democratic republic', 'la', 'latvia', 'lv', 'lebanon', 'lb',
                   'lesotho', 'ls', 'liberia', 'lr', 'libyan arab jamahiriya', 'ly', 'liechtenstein', 'li', 'lithuania',
                   'lt', 'luxembourg', 'lu', 'macau', 'mo', 'macedonia the former yugoslav republic', 'mk',
                   'madagascar', 'mg', 'malawi', 'mw', 'malaysia', 'my', 'maldives', 'mv', 'mali', 'ml', 'malta', 'mt',
                   'marshall islands', 'mh', 'martinique', 'mq', 'mauritania', 'mr', 'mauritius', 'mu', 'mayotte', 'yt',
                   'mexico', 'mx', 'micronesia federated states', 'fm', 'moldova republic', 'md', 'monaco', 'mc',
                   'mongolia', 'mn', 'montserrat', 'ms', 'morocco', 'ma', 'mozambique', 'mz', 'myanmar', 'mm',
                   'namibia', 'na', 'nauru', 'nr', 'nepal', 'np', 'netherlands', 'nl', 'netherlands antilles', 'an',
                   'new caledonia', 'nc', 'new zealand', 'nz', 'nicaragua', 'ni', 'niger', 'ne', 'nigeria', 'ng',
                   'niue', 'nu', 'norfolk island', 'nf', 'northern mariana islands', 'mp', 'norway', 'no', 'oman', 'om',
                   'pakistan', 'pk', 'palau', 'pw', 'palestinian territory occupied', 'ps', 'panama', 'pa',
                   'papua new guinea', 'pg', 'paraguay', 'py', 'peru', 'pe', 'philippines', 'ph', 'pitcairn', 'pn',
                   'poland', 'pl', 'portugal', 'pt', 'puerto rico', 'pr', 'qatar', 'qa', 'reunion', 're', 'romania',
                   'ro', 'russian federation', 'ru', 'rwanda', 'rw', 'saint helena', 'sh', 'saint kitts and nevis',
                   'kn', 'saint lucia', 'lc', 'saint pierre and miquelon', 'pm', 'saint vincent and the grenadines',
                   'vc', 'samoa', 'ws', 'san marino', 'sm', 'sao tome and principe', 'st', 'saudi arabia', 'sa',
                   'senegal', 'sn', 'seychelles', 'sc', 'sierra leone', 'sl', 'singapore', 'sg', 'slovakia', 'sk',
                   'slovenia', 'si', 'solomon islands', 'sb', 'somalia', 'so', 'south africa', 'za',
                   'south georgia and the south sandwich islands', 'gs', 'spain', 'es', 'srilanka', 'lk', 'sudan', 'sd',
                   'suriname', 'sr', 'svalbard and jan mayen', 'sj', 'swaziland', 'sz', 'sweden', 'se', 'switzerland',
                   'ch', 'syrian arab republic', 'sy', 'taiwan province of china', 'tw', 'tajikistan', 'tj',
                   'tanzania united republic', 'tz', 'thailand', 'th', 'togo', 'tg', 'tokelau', 'tk', 'tonga', 'to',
                   'trinidad and tobago', 'tt', 'tunisia', 'tn', 'turkey', 'tr', 'turkmenistan', 'tm',
                   'turks and caicos islands', 'tc', 'tuvalu', 'tv', 'uganda', 'ug', 'ukraine', 'ua',
                   'united arab emirates', 'ae', 'united kingdom', 'uk', 'united states', 'usa','united states amrican', 'usa',
                   'united states minor outlying islands', 'um', 'uruguay', 'uy', 'uzbekistan', 'uz', 'vanuatu', 'vu',
                   'venezuela', 've', 'vietnam', 'vn', 'virgin islands british', 'vg', 'virgin islands us', 'vi',
                   'wallis and futuna', 'wf', 'western sahara', 'eh', 'yemen', 'ye', 'yugoslavia', 'yu', 'zambia', 'zm',
                   'zimbabwe', 'zw', 'Overseas Private Investment Corporation', 'opic', 'United Nations', 'un',
                   'United Nations Educational Scientific and Cultural Organization', 'unesco',
                   'United Nations Childrens Emergency Fund', 'unicef']

        self.months = {
            "january" : 1 , "jan": 1,
            "february" : 2 ,"feb": 2,
            "march" : 3 ,"mar": 3,
            "april" : 4 ,"apr": 4,
            "may" : 5 ,
            "june" : 6 ,"jun": 6,
            "july" : 7 ,"jul": 7,
            "august" : 8 ,"aug": 8,
            "september" : 9 ,"sep": 9 ,
            "october" : 10 ,"oct": 10,
            "november" : 11 ,"nov": 11,
            "december" : 12 ,"dec" : 12
        }

    def dealWithDateTime(self , line):
        words = []
        pattern_id = 0
        for pattern in self.dateAndTimePatterns:
            rest = ""
            while (re.search(pattern, line)):
                result = re.search(pattern, line)
                #print ("round ({})".format(pattern_id))
                first = result.span()[0]
                second = result.span()[1]
                prefix = line[0:first]
                inner = line[first:second]
                suffix = line[second:len(line)]
                rest += prefix
                line = suffix
                normalFrm = self.normalizing(pattern_id,inner)
                words.append(normalFrm)

            pattern_id+=1
            line = rest + line

        return (words , line)



    def normalizing(self , pattern_id , date ):
        # formal format  [DD-MM-YYYY]

        if(pattern_id == 0) :
            # MM/DD/YYYY or MM\DD\YYYY  MM-DD-YYYY
            MM = date[0:2]
            DD = date[3:5]
            YY = date[6:]

        elif(pattern_id == 1) :
            # DD/MM/YYYY or DD\MM\YYYY or DD-MM-YYYY
            DD = date[0:2]
            MM = date[3:5]
            YY = date[6:]


        elif (pattern_id == 2):
            # YYYY-MM-DD or YYYY\MM\DD or YYYY/MM/DD
            YY = date[0:4]
            MM = date[5:7]
            DD = date[8:]

        elif (pattern_id == 3):
            # YYYY-DD-MM or YYYY\DD\MM or YYYY\DD\MM
            YY = date[0:4]
            DD = date[5:7]
            MM = date[8:]

        elif (pattern_id == 7):
            #MM dd,yyyy  --> Jul 30,2015
            YY = date[-4:]
            DD = date[-7:-5]
            MM = date[:-7].strip()
            MM = str(self.months[MM])
            #print(f"{DD} {MM} {YY}")

        elif (pattern_id == 6):
            # dd (st,nd,th) MM ( yyyy or yy )
            i = 0
            while i < len(date) and date[i].isdigit(): i+=1
            DD = date[0:i]

            j = len(date) -1
            while j >= 0 and date[j].isdigit(): j -= 1
            YY = date[j:].strip()

            if len(YY)==2:
                YY = "19" + YY
            YY = YY

            MM = date[i:j]
            if( MM[0] == " " ) :
                MM = MM.strip()
            else:
                MM = MM[3:]

            MM = str(self.months[MM])

        date = DD + "-" + MM + "-" + YY
        #print(f"date per seconds : {date}")
        return date


    def dealWithCommenAbbreviation(self , line):

        words = []
        line = " " + line + " "
        rest = " "
        # ShortCommon
        for i in range(0, len(self.ShortCommon)):
            while (re.search('\s' + self.ShortCommon[i].lower() + '\s', line)):
                result = re.search('\s' + self.ShortCommon[i].lower() + '\s', line)
                first = result.span()[0]
                second = result.span()[1]
                words.append(self.ShortCommon[i].lower())
                rest += line[0:first] + " "
                line = " " + line[second:len(line)]

        line = rest + line
        rest = ""

         # Commons
        for i in range(0, len(self.Commons)):
            while (re.search('\s' + self.Commons[i].lower() + '\s', line)):
                result = re.search('\s' + self.Commons[i].lower() + '\s', line)
                first = result.span()[0]
                second = result.span()[1]
                words.append(self.ShortCommon[i].lower())
                rest += line[0:first] + " "
                line = " " + line[second:len(line)]

        line = rest + line
        rest = ""

        # Currency
        for i in range(0, len(self.Currency)):
            while (re.search('\s' + self.Currency[i].lower() + '\s', line)):
                result = re.search('\s' + self.Currency[i].lower() + '\s', line)
                first = result.span()[0]
                second = result.span()[1]
                words.append(self.shortCurrency[i].lower())
                rest += line[0:first] + " "
                line = " " + line[second:len(line)]
        line = rest + line
        rest = ""

        # currencySymbol
        for i in range(0, len(self.currencySymbol)):
            while (re.search('\s' + self.currencySymbol[i].lower() + '\s', line)):
                result = re.search('\s' + self.currencySymbol[i].lower() + '\s', line)
                first = result.span()[0]
                second = result.span()[1]
                words.append(self.shortCurrency[i].lower())
                rest += line[0:first] + " "
                line = " " + line[second:len(line)]
        line = rest + line
        rest = ""

        # currencySymbol
        for i in range(0, len(self.currencyNames)):
            while (re.search('\s' + self.currencyNames[i].lower() + '\s', line)):
                result = re.search('\s' + self.currencyNames[i].lower() + '\s', line)
                first = result.span()[0]
                second = result.span()[1]
                words.append(self.currencyNames[i].lower())
                rest += line[0:first] + " "
                line = " " + line[second:len(line)]
        line = rest + line
        rest = ""

        # currencySymbol
        for i in range(0, len(self.currencyCountry)):
            while (re.search('\s' + self.currencyCountry[i].lower() + '\s', line)):
                result = re.search('\s' + self.currencyCountry[i].lower() + '\s', line)
                first = result.span()[0]
                second = result.span()[1]
                words.append(self.currencyNames[i].lower())
                rest += line[0:first] + " "
                line = " " + line[second:len(line)]
        line = rest + line
        rest = ""

        # country
        for i in range(0, len(self.country), 2):
            while (re.search('\s' + self.country[i].lower() + '\s', line)):
                result = re.search('\s' + self.country[i].lower() + '\s', line)
                first = result.span()[0]
                second = result.span()[1]
                words.append(self.country[i + 1].lower())
                rest += line[0:first] + " "
                line = " " + line[second:len(line)]

            line = rest + line
            rest = ""

            while (re.search('\s' + self.country[i + 1].lower() + '\s', line.replace('.', ''))):
                result = re.search('\s' + self.country[i + 1].lower() + '\s', line)
                first = result.span()[0]
                second = result.span()[1]
                words.append(self.country[i + 1].lower())
                rest += line[0:first] + " "
                line = " " + line[second:len(line)]

            line = rest + line
            rest = ""

        line = rest + line
        rest = ""

        textsplit = re.split("\s", line.lower())
        #print (textsplit)


        # shortCurrency
        for i in range(0, len(self.shortCurrency)):
            while (self.shortCurrency[i] in textsplit):
                textsplit.remove(self.shortCurrency[i])
                words.append(self.shortCurrency[i])

        # email
        for i, findemail in enumerate(textsplit):
            x = re.search("^\w+@[a-z_]+?\.[a-z]{2,3}$", findemail)
            if (x != None):
                textsplit[i] = textsplit[i].replace(x.group(), '')
                # line=line.replace(findemail,'')
                words.append(x.group())

        # URL
        for i, finduri in enumerate(textsplit):
            x = re.search("(www\.)?\w+\.[a-z]{2,3}", finduri)
            if (x != None):
                textsplit[i] = textsplit[i].replace(x.group(), '')
                # line=line.replace(finduri,'')
                words.append(x.group())


        # IPAddress
        for i, findIpAddress in enumerate(textsplit):
            x = re.search(
                "((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]|[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]|[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]|[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]|[0-9]))",
                findIpAddress)
            if (x != None):
                textsplit[i] = textsplit[i].replace(x.group(), '')
                words.append(x.group())

        line = ''
        for word in textsplit:
            line += word + ' '

        return (words, line)




#amb = AmbiguousToken()


#line = ' '
#line += ' 50 $ usa uk 2013/may/2 vip 3D acct 125.119.119.119  234 www.drfe.com s@dwerfe.gf'
#line += ' '
#words, line = amb.dealWithReularExpression(line.lower())
#print(words)
#print(line)

