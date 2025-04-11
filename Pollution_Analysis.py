import requests
import csv
import time

# WAQI API Key (Replace 'YOUR_API_KEY' with your actual API key)
API_KEY = "your api key"
BASE_URL = "https://api.waqi.info/feed/"

asian_states = {
    "Afghanistan": ["Badakhshan", "Badghis", "Baghlan", "Balkh", "Bamyan", "Daykundi", "Farah", "Faryab", "Ghazni", "Ghor", "Helmand", "Herat", "Jowzjan", "Kabul", "Kandahar", "Kapisa", "Khost", "Kunar", "Kunduz", "Laghman", "Logar", "Nangarhar", "Nimroz", "Nuristan", "Paktia", "Paktika", "Panjshir", "Parwan", "Samangan", "Sar-e Pol", "Takhar", "Urozgan", "Wardak", "Zabul"],
    "Armenia": ["Aragatsotn", "Ararat", "Armavir", "Gegharkunik", "Kotayk", "Lori", "Shirak", "Syunik", "Tavush", "Vayots Dzor", "Yerevan"],
    "Azerbaijan": ["Absheron", "Ganja-Gazakh", "Shirvan", "Lankaran", "Nakhchivan", "Guba-Khachmaz", "Kalbajar-Lachin", "Nagorno-Karabakh"],
    "Bahrain": ["Capital", "Central", "Muharraq", "Northern", "Southern"],
    "Bangladesh": ["Barisal", "Chittagong", "Dhaka", "Khulna", "Mymensingh", "Rajshahi", "Rangpur", "Sylhet"],
    "Bhutan": ["Bumthang", "Chukha", "Dagana", "Gasa", "Haa", "Lhuntse", "Mongar", "Paro", "Pemagatshel", "Punakha", "Samdrup Jongkhar", "Samtse", "Sarpang", "Thimphu", "Trashigang", "Trashiyangtse", "Trongsa", "Tsirang", "Wangdue Phodrang", "Zhemgang"],
    "Brunei": ["Belait", "Brunei-Muara", "Temburong", "Tutong"],
    "Cambodia": ["Banteay Meanchey", "Battambang", "Kampong Cham", "Kampong Chhnang", "Kampong Speu", "Kampong Thom", "Kampot", "Kandal", "Koh Kong", "Kratié", "Mondulkiri", "Oddar Meanchey", "Pailin", "Phnom Penh", "Preah Vihear", "Prey Veng", "Pursat", "Ratanakiri", "Siem Reap", "Sihanoukville", "Stung Treng", "Svay Rieng", "Takeo", "Tbong Khmum"],
    "China": ["Anhui", "Beijing", "Chongqing", "Fujian", "Gansu", "Guangdong", "Guangxi", "Guizhou", "Hainan", "Hebei", "Heilongjiang", "Henan", "Hong Kong", "Hubei", "Hunan", "Inner Mongolia", "Jiangsu", "Jiangxi", "Jilin", "Liaoning", "Macau", "Ningxia", "Qinghai", "Shaanxi", "Shandong", "Shanghai", "Shanxi", "Sichuan", "Tianjin", "Tibet", "Xinjiang", "Yunnan", "Zhejiang"],
    "Cyprus": ["Nicosia", "Limassol", "Larnaca", "Paphos", "Famagusta", "Kyrenia"],
    "East Timor (Timor-Leste)": ["Aileu", "Ainaro", "Baucau", "Bobonaro", "Cova Lima", "Dili", "Ermera", "Lautem", "Liquica", "Manatuto", "Manufahi", "Viqueque", "Oecusse"],
    "India": ["Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal", "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu", "Lakshadweep", "Delhi", "Puducherry", "Ladakh", "Jammu and Kashmir"],
    "Indonesia": ["Aceh", "Bali", "Bangka Belitung", "Banten", "Bengkulu", "Central Java", "Central Kalimantan", "Central Sulawesi", "East Java", "East Kalimantan", "East Nusa Tenggara", "Gorontalo", "Jakarta", "Jambi", "Lampung", "Maluku", "North Kalimantan", "North Maluku", "North Sulawesi", "North Sumatra", "Papua", "Riau", "South Kalimantan", "South Sulawesi", "South Sumatra", "Southeast Sulawesi", "West Java", "West Kalimantan", "West Nusa Tenggara", "West Papua", "West Sulawesi", "West Sumatra", "Yogyakarta"],
    "Iran": ["Tehran", "Isfahan", "Fars", "Kerman", "Khorasan", "Khuzestan", "Lorestan", "Mazandaran", "Qom", "Sistan and Baluchestan", "Yazd"],
    "Iraq": ["Al Anbar", "Babylon", "Baghdad", "Basra", "Diyala", "Dohuk", "Erbil", "Kirkuk", "Nineveh", "Sulaymaniyah"],
    "Israel": ["Jerusalem District", "Northern District", "Haifa District", "Central District", "Tel Aviv District", "Southern District"],
    "Japan": ["Hokkaido", "Tohoku", "Kanto", "Chubu", "Kinki", "Chugoku", "Shikoku", "Kyushu", "Okinawa"],
    "Jordan": ["Amman", "Irbid", "Zarqa", "Madaba", "Balqa", "Karak", "Tafilah", "Maan", "Aqaba"],
    "Kazakhstan": ["Almaty", "Akmola", "Aktobe", "Atyrau", "Karaganda", "Kostanay", "Kyzylorda", "Mangystau", "Pavlodar", "North Kazakhstan", "Turkistan"],
    "Kuwait": ["Al Asimah", "Hawalli", "Al Farwaniyah", "Al Jahra", "Mubarak Al-Kabeer", "Ahmadi"],
    "Kyrgyzstan": ["Bishkek", "Batken", "Chuy", "Issyk-Kul", "Jalal-Abad", "Naryn", "Osh", "Talas"],
    "Laos": ["Attapeu", "Bokeo", "Bolikhamsai", "Champasak", "Houaphanh", "Khammouane", "Luang Namtha", "Luang Prabang", "Oudomxay", "Phongsaly", "Salavan", "Savannakhet", "Sekong", "Vientiane Capital", "Vientiane Province", "Xaisomboun", "Xayaboury", "Xiangkhouang"],
    "Lebanon": ["Beirut", "Mount Lebanon", "North Lebanon", "Beqaa", "Nabatieh", "South Lebanon"],
    "Malaysia": ["Johor", "Kedah", "Kelantan", "Malacca", "Negeri Sembilan", "Pahang", "Perak", "Perlis", "Penang", "Sabah", "Sarawak", "Selangor", "Terengganu"],
    "Maldives": ["Male", "Addu City", "Fuvahmulah City", "Huvadhu Atoll", "North Thiladhunmathi Atoll", "South Thiladhunmathi Atoll", "North Miladhunmadulu Atoll", "South Miladhunmadulu Atoll", "Faadhippolhu Atoll", "North Maalhosmadulu Atoll", "South Maalhosmadulu Atoll", "Ari Atoll", "Felidhe Atoll", "Mulaku Atoll", "Nilandhe Atoll", "Kolhumadulu Atoll"],
    "Mongolia": ["Ulaanbaatar", "Arkhangai", "Bayankhongor", "Bayan-Ulgii", "Darkhan-Uul", "Dornod", "Dornogovi", "Dundgovi", "Govi-Altai", "Govisümber", "Khentii", "Khovd", "Khuvsgul", "Orkhon", "Selenge", "Sukhbaatar", "Tuv", "Umnugovi", "Uvurkhangai", "Zavkhan"],
    "Myanmar (Burma)": ["Ayeyarwady", "Bago", "Chin", "Kachin", "Kayah", "Kayin", "Magway", "Mandalay", "Mon", "Rakhine", "Sagaing", "Shan", "Tanintharyi", "Yangon"],
    "Nepal": ["Province 1", "Madhesh Province", "Bagmati Province", "Gandaki Province", "Lumbini Province", "Karnali Province", "Sudurpashchim Province"],
    "North Korea": ["Pyongyang", "Rason", "North Pyongan", "South Pyongan", "North Hamgyong", "South Hamgyong", "Kangwon", "North Hwanghae", "South Hwanghae", "Ryanggang", "Chagang"],
    "Oman": ["Muscat", "Dhofar", "Musandam", "Al Buraimi", "Ad Dakhiliyah", "Al Batinah North", "Al Batinah South", "Ash Sharqiyah North", "Ash Sharqiyah South", "Ad Dhahirah", "Al Wusta"],
    "Pakistan": ["Azad Kashmir", "Gilgit-Baltistan", "Islamabad Capital Territory", "Khyber Pakhtunkhwa", "Punjab", "Sindh", "Balochistan"],
    "Palestine": ["Gaza Strip", "West Bank"],
    "Philippines": ["Metro Manila", "Cordillera Administrative Region", "Ilocos Region", "Cagayan Valley", "Central Luzon", "Calabarzon", "Mimaropa", "Bicol Region", "Western Visayas", "Central Visayas", "Eastern Visayas", "Zamboanga Peninsula", "Northern Mindanao", "Davao Region", "Soccsksargen", "Caraga", "Bangsamoro"],
    "Qatar": ["Doha", "Al Rayyan", "Al Wakrah", "Al Khor", "Al Shamal", "Al Daayen", "Umm Salal", "Madinat ash Shamal"],
    "Saudi Arabia": ["Riyadh", "Mecca", "Medina", "Eastern Province", "Asir", "Jizan", "Najran", "Tabuk", "Al-Qassim", "Hail", "Northern Borders", "Al-Baha", "Al-Jawf"],
    "Singapore": ["Central Region", "East Region", "North Region", "North-East Region", "West Region"],
    "South Korea": ["Seoul", "Busan", "Daegu", "Incheon", "Gwangju", "Daejeon", "Ulsan", "Sejong", "Gyeonggi", "Gangwon", "North Chungcheong", "South Chungcheong", "North Jeolla", "South Jeolla", "North Gyeongsang", "South Gyeongsang", "Jeju"],
    "Sri Lanka": ["Western Province", "Central Province", "Southern Province", "Northern Province", "Eastern Province", "North Western Province", "North Central Province", "Uva Province", "Sabaragamuwa Province"],
    "Syria": ["Damascus", "Aleppo", "Homs", "Hama", "Latakia", "Idlib", "Tartus", "Deir ez-Zor", "Al-Hasakah", "Raqqa", "As-Suwayda", "Daraa", "Quneitra"],
    "Taiwan": ["Taipei", "New Taipei", "Taoyuan", "Taichung", "Tainan", "Kaohsiung", "Keelung", "Hsinchu City", "Hsinchu County", "Miaoli County", "Changhua County", "Nantou County", "Yunlin County", "Chiayi City", "Chiayi County", "Pingtung County", "Yilan County", "Hualien County", "Taitung County", "Penghu County", "Kinmen County", "Lienchiang County"],
    "Tajikistan": ["Dushanbe", "Gorno-Badakhshan", "Khatlon", "Sughd"],
    "Thailand": ["Bangkok", "Chiang Mai", "Nonthaburi", "Nakhon Ratchasima", "Samut Prakan", "Ubon Ratchathani", "Khon Kaen", "Chonburi", "Nakhon Si Thammarat", "Surat Thani"],
    "Turkey": ["Istanbul", "Ankara", "Izmir", "Bursa", "Antalya", "Adana", "Gaziantep", "Konya", "Çankaya", "Mersin"],
    "Turkmenistan": ["Ashgabat", "Ahal", "Balkan", "Dashoguz", "Lebap", "Mary"],
    "United Arab Emirates (UAE)": ["Abu Dhabi", "Dubai", "Sharjah", "Ajman", "Umm Al Quwain", "Ras Al Khaimah", "Fujairah"],
    "Uzbekistan": ["Tashkent", "Andijan", "Bukhara", "Fergana", "Jizzakh", "Karakalpakstan", "Namangan", "Navoi", "Qashqadaryo", "Samarqand", "Sirdaryo", "Surxondaryo", "Xorazm"],
    "Vietnam": ["Hanoi", "Ho Chi Minh City", "Da Nang", "Hai Phong"],
    "Yemen": ["Aden", "Sana'a", "Taiz", "Hodeidah", "Mukalla", "Sayun", "Ibb", "Dhamar", "Saada", "Al Mahwit", "Amran", "Al Bayda", "Marib", "Al Jawf", "Shabwah", "Hadramaut", "Dali", "Raymah", "Socotra"],
    "British Indian Ocean Territory": ["Diego Garcia"],
    "Cocos (Keeling) Islands": ["West Island", "Home Island"],
    "Christmas Island": ["Flying Fish Cove", "Poon Saan", "Silver City"]
    
}
european_states = {
    "Albania": ["Berat", "Dibër", "Durrës", "Elbasan", "Fier", "Gjirokastër", "Korçë", "Kukës", "Lezhë", "Shkodër", "Tiranë", "Vlorë"],
    "Andorra": ["Andorra la Vella", "Canillo", "Encamp", "Escaldes-Engordany", "La Massana", "Ordino", "Sant Julià de Lòria"],
    "Austria": ["Burgenland", "Carinthia", "Lower Austria", "Upper Austria", "Salzburg", "Styria", "Tyrol", "Vorarlberg", "Vienna"],
    "Belarus": ["Brest Region", "Gomel Region", "Grodno Region", "Minsk Region", "Mogilev Region", "Vitebsk Region", "Minsk City"],
    "Belgium": ["Brussels-Capital Region", "Flanders", "Wallonia"],  # Flanders and Wallonia further divided into provinces
    "Bosnia and Herzegovina": ["Federation of Bosnia and Herzegovina", "Republika Srpska", "Brčko District"],
    "Bulgaria": ["Blagoevgrad", "Burgas", "Dobrich", "Gabrovo", "Haskovo", "Kardzhali", "Kyustendil", "Lovech", "Montana", "Pazardzhik", "Pernik", "Pleven", "Plovdiv", "Razgrad", "Ruse", "Shumen", "Silistra", "Sliven", "Smolyan", "Sofia City", "Sofia Province", "Stara Zagora", "Targovishte", "Varna", "Veliko Tarnovo", "Vidin", "Vratsa", "Yambol"],
    "Croatia": ["Zagreb County", "Krapina-Zagorje County", "Sisak-Moslavina County", "Karlovac County", "Varaždin County", "Koprivnica-Križevci County", "Bjelovar-Bilogora County", "Primorje-Gorski Kotar County", "Lika-Senj County", "Virovitica-Podravina County", "Požega-Slavonia County", "Brod-Posavina County", "Zadar County", "Šibenik-Knin County", "Split-Dalmatia County", "Istria County", "Dubrovnik-Neretva County", "Međimurje County", "Zagreb City", "Vukovar-Srijem County"],
    "Czech Republic": ["Prague", "Central Bohemian Region", "South Bohemian Region", "Plzeň Region", "Karlovy Vary Region", "Ústí nad Labem Region", "Liberec Region", "Hradec Králové Region", "Pardubice Region", "Vysočina Region", "South Moravian Region", "Olomouc Region", "Zlín Region", "Moravian-Silesian Region"],
    "Denmark": ["Capital Region of Denmark", "Central Denmark Region", "North Denmark Region", "South Denmark Region", "Zealand Region", "Faroe Islands"],
    "Estonia": ["Harju County", "Hiiu County", "Ida-Viru County", "Jõgeva County", "Järva County", "Lääne County", "Lääne-Viru County", "Põlva County", "Pärnu County", "Rapla County", "Saare County", "Tartu County", "Valga County", "Viljandi County", "Võru County"],
    "Finland": ["Lapland", "North Ostrobothnia", "Kainuu", "North Karelia", "North Savo", "South Savo", "South Ostrobothnia", "Central Ostrobothnia", "Central Finland", "Pirkanmaa", "Satakunta", "Southwest Finland", "Päijät-Häme", "Kanta-Häme", "Uusimaa", "Kymenlaakso", "Åland"],
    "France": ["Auvergne-Rhône-Alpes", "Bourgogne-Franche-Comté", "Brittany", "Centre-Val de Loire", "Corsica", "Grand Est", "Hauts-de-France", "Île-de-France", "Normandy", "Nouvelle-Aquitaine", "Occitanie", "Pays de la Loire", "Provence-Alpes-Côte d'Azur"],
    "Germany": ["Baden-Württemberg", "Bavaria", "Berlin", "Brandenburg", "Bremen", "Hamburg", "Hesse", "Lower Saxony", "Mecklenburg-Vorpommern", "North Rhine-Westphalia", "Rhineland-Palatinate", "Saarland", "Saxony", "Saxony-Anhalt", "Schleswig-Holstein", "Thuringia"],
    "Greece": ["Attica", "Central Greece", "Central Macedonia", "Crete", "East Macedonia and Thrace", "Epirus", "Ionian Islands", "North Aegean", "Peloponnese", "South Aegean", "Thessaly", "West Greece", "West Macedonia"],
    "Hungary": ["Budapest", "Baranya", "Bács-Kiskun", "Békés", "Borsod-Abaúj-Zemplén", "Csongrád-Csanád", "Fejér", "Győr-Moson-Sopron", "Hajdú-Bihar", "Heves", "Jász-Nagykun-Szolnok", "Komárom-Esztergom", "Nógrád", "Pest", "Somogy", "Szabolcs-Szatmár-Bereg", "Tolna", "Vas", "Veszprém", "Zala"],
    "Iceland": ["Capital Region", "Southern Peninsula", "Western Region", "Westfjords", "Northwestern Region", "Northeastern Region", "Eastern Region", "Southern Region"],
    "Ireland": ["Connacht", "Leinster", "Munster", "Ulster"],
    "Italy": ["Abruzzo", "Basilicata", "Calabria", "Campania", "Emilia-Romagna", "Friuli Venezia Giulia", "Lazio", "Liguria", "Lombardy", "Marche", "Molise", "Piedmont", "Apulia", "Sardinia", "Sicily", "Tuscany", "Trentino-Alto Adige/Südtirol", "Umbria", "Aosta Valley", "Veneto"],
    "Kosovo": ["Prishtina", "Prizren", "Peja", "Gjakova", "Mitrovica", "Gjilan", "Ferizaj"],  # Political status contested
    "Latvia": ["Riga", "Pieriga", "Vidzeme", "Kurzeme", "Zemgale", "Latgale"],
    "Liechtenstein": ["Balzers", "Eschen", "Gamprin", "Mauren", "Planken", "Ruggell", "Schaan", "Schellenberg", "Triesen", "Triesenberg", "Vaduz"],
    "Lithuania": ["Vilnius County", "Kaunas County", "Klaipėda County", "Šiauliai County", "Panevėžys County", "Alytus County", "Marijampolė County", "Tauragė County", "Telšiai County", "Utena County"],
    "Luxembourg": ["Diekirch", "Grevenmacher", "Luxembourg"],
    "Malta": ["Northern Region", "Central Region", "Southern Region", "South Eastern Region", "Gozo Region"],
    "Moldova": ["Chișinău", "Bălți", "Cahul", "Ungheni", "Orhei", "Comrat", "Tiraspol", "Gagauzia", "Transnistria"],  # Transnistria political status contested
    "Monaco": ["Monaco-Ville", "La Condamine", "Monte Carlo", "Fontvieille"],
    "Montenegro": ["Andrijevica", "Bar", "Berane", "Bijelo Polje", "Budva", "Cetinje", "Danilovgrad", "Herceg Novi", "Kolašin", "Kotor", "Mojkovac", "Nikšić", "Plav", "Pljevlja", "Podgorica", "Rožaje", "Šavnik", "Tivat", "Ulcinj", "Žabljak"],
    "Netherlands": ["Drenthe", "Flevoland", "Friesland", "Gelderland", "Groningen", "Limburg", "North Brabant", "North Holland", "Overijssel", "South Holland", "Utrecht", "Zeeland", "Caribbean Netherlands"],
    "North Macedonia": ["Skopje", "Vardar", "Pelagonia", "Eastern Region", "Southeastern Region", "Southwestern Region", "Polog", "Northeastern Region"],
    "Norway": ["Oslo", "Agder", "Møre og Romsdal", "Nordland", "Innlandet", "Vestland", "Trøndelag", "Viken", "Troms og Finnmark", "Svalbard and Jan Mayen"],
    "Poland": ["Lower Silesian Voivodeship", "Kuyavian-Pomeranian Voivodeship", "Lublin Voivodeship", "Lubusz Voivodeship", "Łódź Voivodeship", "Lesser Poland Voivodeship", "Masovian Voivodeship", "Opole Voivodeship", "Podkarpackie Voivodeship", "Podlaskie Voivodeship", "Pomeranian Voivodeship", "Silesian Voivodeship", "Świętokrzyskie Voivodeship", "Warmian-Masurian Voivodeship", "Greater Poland Voivodeship", "West Pomeranian Voivodeship"],
    "Portugal": ["Azores", "Madeira", "Norte", "Centro", "Lisbon", "Alentejo", "Algarve"],
    "Romania": ["Bucharest", "Alba", "Arad", "Argeș", "Bacău", "Bihor", "Bistrița-Năsăud", "Botoșani", "Brașov", "Brăila", "Buzău", "Călărași", "Caraș-Severin", "Cluj", "Constanța", "Covasna", "Dâmbovița", "Dolj", "Galați", "Giurgiu", "Gorj", "Harghita", "Hunedoara", "Ialomița", "Iași", "Ilfov", "Maramureș", "Mehedinți", "Mureș", "Neamț", "Olt", "Prahova", "Sălaj", "Satu Mare", "Sibiu", "Suceava", "Teleorman", "Timiș", "Tulcea", "Vâlcea", "Vaslui", "Vrancea"],
    
}
oceania_states = {
    "Australia": ["New South Wales", "Victoria", "Queensland", "Western Australia", "South Australia", "Tasmania", "Australian Capital Territory", "Northern Territory", "Norfolk Island", "Coral Sea Islands Territory"],
    "Fiji": ["Central Division", "Eastern Division", "Northern Division", "Western Division"],
    "Kiribati": ["Gilbert Islands", "Line Islands", "Phoenix Islands"],
    "Marshall Islands": ["Ailinglaplap", "Ailuk", "Arno", "Aur", "Bikini", "Ebon", "Enewetak", "Jabat", "Jaluit", "Kili", "Kwajalein", "Lae", "Likiep", "Majuro", "Maloelap", "Mejit", "Namdrik", "Namu", "Rongelap", "Rongrik", "Toke", "Ujae", "Utrök", "Wotho", "Wotje"],
    "Micronesia": ["Chuuk", "Kosrae", "Pohnpei", "Yap"],
    "Nauru": ["Aiwo", "Anabar", "Anetan", "Anibare", "Baiti", "Boe", "Buada", "Denigomodu", "Ewa", "Ijuw", "Meneng", "Nibok", "Uaboe", "Yaren"],
    "New Zealand": ["Auckland", "Wellington", "Canterbury", "Otago", "Waikato", "Hawke's Bay", "Taranaki", "Manawatu-Wanganui", "Northland", "Southland", "Bay of Plenty", "Gisborne", "Nelson", "Marlborough", "Tasman", "West Coast", "Cook Islands", "Niue", "Tokelau"],
    "Palau": ["Aimeliik", "Airai", "Angaur", "Hatohobei", "Kayangel", "Koror", "Melekeok", "Ngaraard", "Ngarchelong", "Ngardmau", "Ngatpang", "Ngchesar", "Ngiwal", "Peleliu", "Sonsorol"],
    "Papua New Guinea": ["Central", "Chimbu", "Eastern Highlands", "East New Britain", "East Sepik", "Enga", "Gulf", "Hela", "Jiwaka", "Madang", "Manus", "Milne Bay", "Morobe", "New Ireland", "Northern", "Bougainville", "Southern Highlands", "West New Britain", "Western", "Western Highlands", "National Capital District"],
    "Samoa": ["A'ana", "Aiga-i-le-Tai", "Atua", "Fa'asaleleaga", "Gaga'emauga", "Gagaifomauga", "Palauli", "Satupa'itea", "Tuamasaga", "Va'a-o-Fonoti", "Vaisigano"],
    "Solomon Islands": ["Central Province", "Choiseul Province", "Guadalcanal Province", "Honiara", "Isabel Province", "Makira-Ulawa Province", "Malaita Province", "Rennell and Bellona Province", "Temotu Province", "Western Province"],
    "Tonga": ["'Eua", "Ha'apai", "Niuas", "Tongatapu", "Vava'u"],
    "Tuvalu": ["Funafuti", "Nanumea", "Nanumaga", "Niulakita", "Niutao", "Nui", "Nukufetau", "Nukulaelae", "Vaitupu"],
    "Vanuatu": ["Malampa", "Penama", "Sanma", "Shefa", "Tafea", "Torba"],
    "United States Territories (Oceania)": ["American Samoa", "Guam", "Northern Mariana Islands", "Wake Island"],
    "French Territories (Oceania)": ["New Caledonia", "French Polynesia", "Wallis and Futuna"],
}
africa_states = {
    "Algeria": ["Adrar", "Chlef", "Laghouat", "Oum El Bouaghi", "Batna", "Béjaïa", "Biskra", "Béchar", "Blida", "Bouira", "Tamanrasset", "Tébessa", "Tlemcen", "Tiaret", "Tizi Ouzou", "Djelfa", "Jijel", "Sétif", "Saïda", "Skikda", "Sidi Bel Abbès", "Annaba", "Guelma", "Constantine", "Médéa", "Mostaganem", "M'Sila", "Mascara", "Ouargla", "Oran", "El Bayadh", "Illizi", "Bordj Baji Mokhtar", "Béni Abbès", "Timimoun", "Touggourt", "Djanet", "In Salah", "In Guezzam"],
    "Angola": ["Bengo", "Benguela", "Bié", "Cabinda", "Cuando Cubango", "Cuanza Norte", "Cuanza Sul", "Cunene", "Huambo", "Huíla", "Luanda", "Lunda Norte", "Lunda Sul", "Malanje", "Moxico", "Namibe", "Uíge", "Zaire"],
    "Benin": ["Alibori", "Atacora", "Atlantique", "Borgou", "Collines", "Couffo", "Donga", "Littoral", "Mono", "Ouémé", "Plateau", "Zou"],
    "Botswana": ["Central", "Ghanzi", "Kgalagadi", "Kgatleng", "Kweneng", "North-East", "North-West", "South-East", "Southern"],
    "Burkina Faso": ["Boucle du Mouhoun", "Cascades", "Centre", "Centre-Est", "Centre-Nord", "Centre-Ouest", "Centre-Sud", "Est", "Hauts-Bassins", "Nord", "Plateau-Central", "Sahel", "Sud-Ouest"],
    "Burundi": ["Bujumbura Mairie", "Bubanza", "Bururi", "Cankuzo", "Cibitoke", "Gitega", "Karuzi", "Kayanza", "Kirundo", "Makamba", "Muramvya", "Mwaro", "Ngozi", "Rumonge", "Rutana", "Ruyigi"],
    "Cabo Verde": ["Boa Vista", "Brava", "Fogo", "Maio", "Sal", "Santiago", "Santo Antão", "São Nicolau", "São Vicente"],
    "Cameroon": ["Adamawa", "Centre", "East", "Far North", "Littoral", "North", "Northwest", "South", "Southwest", "West"],
    "Central African Republic": ["Bamingui-Bangoran", "Bangui", "Basse-Kotto", "Haute-Kotto", "Haut-Mbomou", "Kémo", "Lobaye", "Mambéré-Kadéï", "Mbomou", "Nana-Grebizi", "Nana-Mambere", "Ombella-M'Poko", "Ouaka", "Ouham", "Ouham-Pendé", "Sangha-Mbaéré", "Vakaga"],
    "Chad": ["Bahr el Gazel", "Borkou", "Ennedi-Est", "Ennedi-Ouest", "Guéra", "Hadjer-Lamis", "Kanem", "Lac", "Logone Occidental", "Logone Oriental", "Mandoul", "Mayo-Kebbi Est", "Mayo-Kebbi Ouest", "Moyen-Chari", "Ouaddaï", "Salamat", "Sila", "Tandjilé", "Tibesti", "Ville de N'Djamena"],
    "Comoros": ["Anjouan", "Grande Comore", "Mohéli"],
    "Congo, Democratic Republic of the": ["Bas-Uélé", "Équateur", "Haut-Katanga", "Haut-Lomami", "Hauts-Uélé", "Ituri", "Kasaï", "Kasaï-Central", "Kasaï-Oriental", "Kinshasa", "Kongo-Central", "Kwango", "Kwilu", "Lomami", "Lualaba", "Mai-Ndombe", "Mongala", "Nord-Kivu", "Nord-Ubangi", "Sankuru", "Sud-Kivu", "Sud-Ubangi", "Tanganika", "Tshopo", "Tshuapa"],
    "Congo, Republic of the": ["Brazzaville", "Bouenza", "Cuvette", "Cuvette-Ouest", "Kouilou", "Lékoumou", "Likouala", "Niari", "Plateaux", "Pointe-Noire", "Sangha"],
    "Cote d'Ivoire": ["Abidjan", "Bas-Sassandra", "Comoé", "Denguélé", "Gôh-Djiboua", "Lacs", "Lagunes", "Montagnes", "Sassandra-Marahoué", "Savanes", "Vallée du Bandama", "Woroba", "Yamoussoukro", "Zanzan"],
    "Djibouti": ["Ali Sabieh", "Arta", "Dikhil", "Djibouti", "Obock", "Tadjoura"],
    "Egypt": ["Alexandria", "Aswan", "Asyut", "Beheira", "Beni Suef", "Cairo", "Dakahlia", "Damietta", "Faiyum", "Gharbia", "Giza", "Ismailia", "Kafr el-Sheikh", "Luxor", "Matruh", "Minya", "Monufia", "New Valley", "North Sinai", "Port Said", "Qalyubia", "Qena", "Red Sea", "Sharqia", "Sohag", "South Sinai", "Suez"],
    "Equatorial Guinea": ["Annobón", "Bioko Norte", "Bioko Sur", "Centro Sur", "Djibloho", "Kié-Ntem", "Litoral", "Wele-Nzas"],
    "Eritrea": ["Anseba", "Debub", "Debubawi Keyih Bahri", "Gash-Barka", "Maekel", "Semenawi Keyih Bahri"],
    "Eswatini": ["Hhohho", "Lubombo", "Manzini", "Shiselweni"],
    "Ethiopia": ["Addis Ababa", "Afar", "Amhara", "Benishangul-Gumuz", "Dire Dawa", "Gambela", "Harari", "Oromia", "Sidama", "Somali", "South West Ethiopia Peoples' Region", "Tigray"],
    "Gabon": ["Estuaire", "Haut-Ogooué", "Moyen-Ogooué", "Ngounié", "Nyanga", "Ogooué-Ivindo", "Ogooué-Lolo", "Ogooué-Maritime", "Woleu-Ntem"],
    "Gambia": ["Banjul", "Central River", "Lower River", "North Bank", "Upper River", "West Coast"],
    "Ghana": ["Ahafo", "Ashanti", "Bono", "Bono East", "Central", "Eastern", "Greater Accra", "North East", "Northern", "Oti", "Savannah", "Upper East", "Upper West", "Volta", "Western", "Western North"],
    "Guinea": ["Boké", "Conakry", "Faranah", "Kankan", "Kindia", "Labé", "Mamou", "Nzérékoré"],
    "Guinea-Bissau": ["Bafatá", "Biombo", "Bissau", "Bolama", "Cacheu", "Gabú", "Oio", "Quinara", "Tombali"],
    "Kenya": ["Baringo", "Bomet", "Bungoma", "Busia", "Elgeyo-Marakwet", "Embu", "Garissa", "Homa Bay", "Isiolo", "Kajiado", "Kakamega", "Kericho", "Kiambu", "Kilifi", "Kirinyaga", "Kisii", "Kisumu", "Kitui", "Kwale", "Laikipia", "Lamu", "Machakos", "Makueni", "Mandera", "Marsabit", "Meru", "Migori", "Mombasa", "Murang'a", "Nairobi", "Nakuru", "Nandi", "Narok", "Nyamira", "Nyandarua", "Nyeri", "Samburu", "Siaya", "Taita-Taveta", "Tana River", "Trans Nzoia", "Turkana", "Uasin Gishu", "Vihiga", "Wajir", "West Pokot"],
    "Lesotho": ["Berea", "Butha-Buthe", "Leribe", "Mafeteng", "Maseru", "Mohale's Hoek", "Mokhotlong", "Qacha's Nek", "Quthing", "Thaba-Tseka"],
    "Liberia": ["Bomi", "Bong", "Gbarpolu", "Grand Bassa", "Grand Cape Mount", "Grand Gedeh", "Grand Kru", "Lofa", "Margibi", "Maryland", "Montserrado", "Nimba", "River Cess", "River Gee", "Sinoe"],
    "Libya": ["Benghazi", "Derna", "Ghat", "Jabal al Akhdar", "Jafara", "Jufra", "Kufra", "Murzuq", "Murqub", "Nalut", "Nuqat al Khams", "Sabha", "Sirte", "Tripoli", "Wadi al Hayaa", "Wadi al Shatii", "Zawiya"],
    "Madagascar": ["Antananarivo", "Antsiranana", "Fianarantsoa", "Mahajanga", "Toamasina", "Toliara"],
    "Malawi": ["Central Region", "Northern Region", "Southern Region"],
    "Mali": ["Bamako", "Gao", "Kayes", "Kidal", "Koulikoro", "Mopti", "Ségou", "Sikasso", "Taoudénit", "Ménaka"],
    "Mauritania": ["Adrar", "Assaba", "Brakna", "Dakhlet Nouadhibou", "Gorgol", "Guidimakha", "Hodh Ech Chargui", "Hodh El Gharbi", "Inchiri", "Nouakchott-Ouest", "Nouakchott-Nord", "Nouakchott-Sud", "Tagant", "Tiris Zemmour", "Trarza"],
    "Mauritius": ["Agaléga", "Black River", "Flacq", "Grand Port", "Moka", "Pamplemousses", "Plaines Wilhems", "Port Louis", "Rivière du Rempart", "Rodrigues", "Savanne"],
    "Morocco": ["Agadir-Ida Ou Tanane", "Al Haouz", "Al Hoceïma", "Aousserd", "Assa-Zag", "Azilal", "Béni Mellal", "Ben Slimane", "Berkane", "Boujdour", "Boulemane", "Casablanca", "Chefchaouen", "Chichaoua", "Chtouka-Aït Baha", "Dakhla", "Driouch", "El Hajeb", "El Jadida", "Errachidia", "Es-Semara", "Fahs-Anjra", "Fès", "Figuig", "Fquih Ben Salah", "Guelmim", "Guer"],
}
north_america_states = {
    "Canada": ["Alberta", "British Columbia", "Manitoba", "New Brunswick", "Newfoundland and Labrador", "Nova Scotia", "Ontario", "Prince Edward Island", "Quebec", "Saskatchewan", "Northwest Territories", "Nunavut", "Yukon"],
    "United States": ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming", "Puerto Rico", "U.S. Virgin Islands"],
    "Mexico": ["Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Chiapas", "Chihuahua", "Coahuila", "Colima", "Durango", "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", "Mexico City", "Mexico State", "Michoacán", "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"],
    "Belize": ["Belize", "Cayo", "Corozal", "Orange Walk", "Stann Creek", "Toledo"],
    "Guatemala": ["Alta Verapaz", "Baja Verapaz", "Chimaltenango", "Chiquimula", "El Progreso", "Escuintla", "Guatemala", "Huehuetenango", "Izabal", "Jalapa", "Jutiapa", "Petén", "Quetzaltenango", "Quiché", "Retalhuleu", "Sacatepéquez", "San Marcos", "Santa Rosa", "Sololá", "Suchitepéquez", "Totonicapán", "Zacapa"],
    "Honduras": ["Atlántida", "Choluteca", "Colón", "Comayagua", "Copán", "Cortés", "El Paraíso", "Francisco Morazán", "Gracias a Dios", "Intibucá", "Islas de la Bahía", "La Paz", "Lempira", "Ocotepeque", "Olancho", "Santa Bárbara", "Valle", "Yoro"],
    "El Salvador": ["Ahuachapán", "Cabañas", "Chalatenango", "Cuscatlán", "La Libertad", "La Paz", "La Unión", "Morazán", "San Miguel", "San Salvador", "San Vicente", "Santa Ana", "Sonsonate", "Usulután"],
    "Nicaragua": ["Boaco", "Carazo", "Chinandega", "Chontales", "Estelí", "Granada", "Jinotega", "León", "Madriz", "Managua", "Masaya", "Matagalpa", "Nueva Segovia", "Río San Juan", "Rivas", "North Caribbean Coast Autonomous Region", "South Caribbean Coast Autonomous Region"],
    "Costa Rica": ["Alajuela", "Cartago", "Guanacaste", "Heredia", "Limón", "Puntarenas", "San José"],
    "Panama": ["Bocas del Toro", "Coclé", "Colón", "Chiriquí", "Darién", "Herrera", "Los Santos", "Panamá", "Panamá Oeste", "Veraguas", "Emberá", "Guna Yala", "Ngäbe-Buglé"],
    "Cuba": ["Artemisa", "Camagüey", "Ciego de Ávila", "Cienfuegos", "Ciudad de La Habana", "Granma", "Guantánamo", "Holguín", "Isla de la Juventud", "Las Tunas", "Matanzas", "Mayabeque", "Pinar del Río", "Sancti Spíritus", "Santiago de Cuba", "Villa Clara"],
    "Dominican Republic": ["Azua", "Baoruco", "Barahona", "Dajabón", "Distrito Nacional", "Duarte", "Elías Piña", "El Seibo", "Espaillat", "Hato Mayor", "Hermanas Mirabal", "Independencia", "La Altagracia", "La Romana", "La Vega", "María Trinidad Sánchez", "Monseñor Nouel", "Monte Cristi", "Monte Plata", "Pedernales", "Peravia", "Puerto Plata", "Samaná", "San Cristóbal", "San José de Ocoa", "San Juan", "San Pedro de Macorís", "Sánchez Ramírez", "Santiago", "Santiago Rodríguez", "Valverde"],
    "Haiti": ["Artibonite", "Centre", "Grand'Anse", "Nippes", "Nord", "Nord-Est", "Nord-Ouest", "Ouest", "Sud", "Sud-Est"],
    "Jamaica": ["Clarendon", "Hanover", "Kingston", "Manchester", "Portland", "Saint Andrew", "Saint Ann", "Saint Catherine", "Saint Elizabeth", "Saint James", "Saint Mary", "Saint Thomas", "Trelawny", "Westmoreland"],
    "Bahamas": ["Acklins", "Berry Islands", "Bimini", "Black Point", "Cat Island", "Central Abaco", "Central Andros", "Central Eleuthera", "City of Freeport", "Crooked Island", "East Grand Bahama", "Exuma", "Grand Cay", "Harbour Island", "Hope Town", "Inagua", "Long Island", "Mangrove Cay", "Mayaguana", "Moore's Island", "North Abaco", "North Andros", "North Eleuthera", "Ragged Island", "Rum Cay", "San Salvador", "South Abaco", "South Andros", "South Eleuthera", "Spanish Wells", "West Grand Bahama"],
    "Barbados": ["Christ Church", "Saint Andrew", "Saint George", "Saint James", "Saint John", "Saint Joseph", "Saint Lucy", "Saint Michael", "Saint Peter", "Saint Philip", "Saint Thomas"],
    "Antigua and Barbuda": ["Antigua", "Barbuda", "Redonda"],
    "Dominica": ["Saint Andrew", "Saint David", "Saint George", "Saint John", "Saint Joseph", "Saint Luke", "Saint Mark", "Saint Patrick", "Saint Paul", "Saint Peter"],
    "Grenada": ["Saint Andrew", "Saint David", "Saint George", "Saint John", "Saint Mark", "Saint Patrick"],
    "Saint Kitts and Nevis": ["Christ Church Nichola Town", "Saint Anne Sandy Point", "Saint George Basseterre", "Saint George Gingerland", "Saint James Windward", "Saint John Capisterre", "Saint John Figtree", "Saint Paul Capisterre", "Saint Paul Charlestown", "Saint Peter Basseterre", "Saint Thomas Lowland", "Saint Thomas Middle Island", "Trinity Palmetto Point"],
    "Saint Lucia": ["Anse la Raye", "Castries", "Choiseul", "Dennery", "Gros Islet", "Laborie", "Micoud", "Soufrière", "Vieux Fort"],
    "Saint Vincent and the Grenadines": ["Charlotte", "Grenadines", "Saint Andrew", "Saint David", "Saint George", "Saint Patrick"],
    "Trinidad and Tobago": ["Arima", "Chaguanas", "Couva-Tabaquite-Talparo", "Diego Martin", "Penal-Debe", "Point Fortin", "Port of Spain", "Princes Town", "Rio Claro-Mayaro", "San Fernando", "San Juan-Laventille", "Sangre Grande", "Siparia", "Tobago"],
    "United Kingdom Territories": ["Bermuda", "Cayman Islands", "Turks and Caicos Islands", "Anguilla"],
    "Netherlands Territories": ["Aruba", "Curaçao", "Sint Maarten"],
    "French Territories": ["Saint Pierre and Miquelon", "Saint Barthélemy", "Saint Martin"],
}
south_america_states = {
    "Argentina": ["Buenos Aires", "Catamarca", "Chaco", "Chubut", "Córdoba", "Corrientes", "Entre Ríos", "Formosa", "Jujuy", "La Pampa", "La Rioja", "Mendoza", "Misiones", "Neuquén", "Río Negro", "Salta", "San Juan", "San Luis", "Santa Cruz", "Santa Fe", "Santiago del Estero", "Tierra del Fuego", "Tucumán", "Buenos Aires City"],
    "Bolivia": ["Chuquisaca", "Cochabamba", "Beni", "La Paz", "Oruro", "Pando", "Potosí", "Santa Cruz", "Tarija"],
    "Brazil": ["Acre", "Alagoas", "Amapá", "Amazonas", "Bahia", "Ceará", "Distrito Federal", "Espírito Santo", "Goiás", "Maranhão", "Mato Grosso", "Mato Grosso do Sul", "Minas Gerais", "Pará", "Paraíba", "Paraná", "Pernambuco", "Piauí", "Rio de Janeiro", "Rio Grande do Norte", "Rio Grande do Sul", "Rondônia", "Roraima", "Santa Catarina", "São Paulo", "Sergipe", "Tocantins"],
    "Chile": ["Arica y Parinacota", "Tarapacá", "Antofagasta", "Atacama", "Coquimbo", "Valparaíso", "Metropolitana de Santiago", "O'Higgins", "Maule", "Ñuble", "Biobío", "Araucanía", "Los Ríos", "Los Lagos", "Aysén", "Magallanes y de la Antártica Chilena"],
    "Colombia": ["Amazonas", "Antioquia", "Arauca", "Atlántico", "Bogotá", "Bolívar", "Boyacá", "Caldas", "Caquetá", "Casanare", "Cauca", "Cesar", "Chocó", "Córdoba", "Cundinamarca", "Guainía", "Guaviare", "Huila", "La Guajira", "Magdalena", "Meta", "Nariño", "Norte de Santander", "Putumayo", "Quindío", "Risaralda", "San Andrés y Providencia", "Santander", "Sucre", "Tolima", "Valle del Cauca", "Vaupés", "Vichada"],
    "Ecuador": ["Azuay", "Bolívar", "Cañar", "Carchi", "Chimborazo", "Cotopaxi", "El Oro", "Esmeraldas", "Galápagos", "Guayas", "Imbabura", "Loja", "Los Ríos", "Manabí", "Morona Santiago", "Napo", "Orellana", "Pastaza", "Pichincha", "Santa Elena", "Santo Domingo de los Tsáchilas", "Sucumbíos", "Tungurahua", "Zamora Chinchipe"],
    "Guyana": ["Barima-Waini", "Cuyuni-Mazaruni", "Demerara-Mahaica", "East Berbice-Corentyne", "Essequibo Islands-West Demerara", "Mahaica-Berbice", "Pomeroon-Supenaam", "Potaro-Siparuni", "Upper Demerara-Berbice", "Upper Takutu-Upper Essequibo"],
    "Paraguay": ["Asunción", "Alto Paraguay", "Alto Paraná", "Amambay", "Boquerón", "Caaguazú", "Caazapá", "Canindeyú", "Central", "Concepción", "Cordillera", "Guairá", "Itapúa", "Misiones", "Ñeembucú", "Paraguarí", "Presidente Hayes", "San Pedro"],
    "Peru": ["Amazonas", "Áncash", "Apurímac", "Arequipa", "Ayacucho", "Cajamarca", "Callao", "Cusco", "Huancavelica", "Huánuco", "Ica", "Junín", "La Libertad", "Lambayeque", "Lima", "Loreto", "Madre de Dios", "Moquegua", "Pasco", "Piura", "Puno", "San Martín", "Tacna", "Tumbes", "Ucayali"],
    "Suriname": ["Brokopondo", "Commewijne", "Coronie", "Marowijne", "Nickerie", "Para", "Paramaribo", "Saramacca", "Sipaliwini", "Wanica"],
    "Uruguay": ["Artigas", "Canelones", "Cerro Largo", "Colonia", "Durazno", "Flores", "Florida", "Lavalleja", "Maldonado", "Montevideo", "Paysandú", "Río Negro", "Rivera", "Rocha", "Salto", "San José", "Soriano", "Tacuarembó", "Treinta y Tres"],
    "Venezuela": ["Amazonas", "Anzoátegui", "Apure", "Aragua", "Barinas", "Bolívar", "Carabobo", "Cojedes", "Delta Amacuro", "Falcón", "Guárico", "Lara", "Mérida", "Miranda", "Monagas", "Nueva Esparta", "Portuguesa", "Sucre", "Táchira", "Trujillo", "Vargas", "Yaracuy", "Zulia", "Capital District", "Dependencias Federales"],
    "French Guiana": ["Cayenne", "Saint-Laurent-du-Maroni"],
    "United Kingdom Territories": ["Falkland Islands (Islas Malvinas)"],
    "Netherlands Territories": ["Bonaire"],
}
antarctica_data = {
    "Territorial Claims": {
        "Argentina": "Argentine Antarctica",
        "Australia": "Australian Antarctic Territory",
        "Chile": "Chilean Antarctic Territory",
        "France": "Adélie Land",
        "New Zealand": "Ross Dependency",
        "Norway": "Peter I Island",
        "Norway": "Queen Maud Land",
        "United Kingdom": "British Antarctic Territory",
    },
    "Unclaimed Territory": "Marie Byrd Land",
    "Research Stations": {
        "Argentina": ["Esperanza Base", "Marambio Base", "Orcadas Base", "San Martín Base", "Belgrano II Base", "Carlini Base"],
        "Australia": ["Casey Station", "Davis Station", "Mawson Station", "Macquarie Island Station", "Heard Island Station"],
        "Belgium": ["Princess Elisabeth Station"],
        "Brazil": ["Comandante Ferraz Antarctic Station"],
        "Chile": ["Eduardo Frei Montalva Station", "General Bernardo O'Higgins Research Station", "Professor Julio Escudero Base", "Arturo Prat Base", "Yelcho Base"],
        "China": ["Great Wall Station", "Zhongshan Station", "Kunlun Station", "Taishan Station"],
        "France": ["Dumont d'Urville Station", "Concordia Station (with Italy)"],
        "Germany": ["Neumayer Station III", "Kohnen Station"],
        "India": ["Maitri", "Bharati"],
        "Italy": ["Mario Zucchelli Station", "Concordia Station (with France)"],
        "Japan": ["Syowa Station", "Dome Fuji Station"],
        "South Korea": ["King Sejong Station", "Jang Bogo Station"],
        "New Zealand": ["Scott Base"],
        "Norway": ["Troll Station"],
        "Poland": ["Henryk Arctowski Polish Antarctic Station"],
        "Russia": ["Vostok Station", "Mirny Station", "Progress Station", "Bellingshausen Station", "Novolazarevskaya Station"],
        "South Africa": ["SANAE IV"],
        "Sweden": ["Wasa Research Station"],
        "Ukraine": ["Akademik Vernadsky Station"],
        "United Kingdom": ["Halley Research Station", "Rothera Research Station", "Signy Research Station"],
        "United States": ["Amundsen–Scott South Pole Station", "McMurdo Station", "Palmer Station"],
        "Uruguay": ["Artigas Antarctic Base"],
    },
    "Treaty Information": "Antarctic Treaty System",
}
# CSV file to store results
csv_filename = "World_AQI_Data.csv"

# Writing the headers if the file is empty
with open(csv_filename, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Continent", "Country", "City", "AQI", "PM2.5", "PM10", "NO2"])

def fetch_aqi(city):
    """Fetch AQI data for a given city from WAQI API."""
    url = f"{BASE_URL}{city}/?token={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if data["status"] == "ok":
            aqi = data["data"]["aqi"]
            pm25 = data["data"]["iaqi"].get("pm25", {}).get("v", "N/A")
            pm10 = data["data"]["iaqi"].get("pm10", {}).get("v", "N/A")
            no2 = data["data"]["iaqi"].get("no2", {}).get("v", "N/A")
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            return [timestamp, aqi, pm25, pm10, no2]
        else:
            return None
    except Exception as e:
        print(f"⚠️ Error fetching data for {city}: {e}")
        return None

# Dictionary of all continents and their cities
continents = {
    "Asia": asian_states,
    "Europe": european_states,
    "North America": north_america_states,
    "Oceania": oceania_states,
    "South America": south_america_states,
    "Africa": africa_states,
    "Antarctica": antarctica_data["Research Stations"]
}

# Set the CSV filename
csv_filename = "World_Data.csv"

# Fetch AQI data for all major cities in all continents
import csv

with open("output.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)  # Creates a CSV writer
    writer.writerow(["Column1", "Column2"])  # Writing the header row (optional)
    writer.writerow(["Data1", "Data2"])  # Writing a data row

    
    for continent, data in continents.items():
        if continent == "Antarctica":
            for country, stations in data.items():
                for station in stations:
                    print(f"📍 Fetching data for {station}, {country} in {continent}...")
                    result = fetch_aqi(station)
                    if result:
                        writer.writerow([result[0], continent, country, station, result[1], result[2], result[3], result[4]])
                    time.sleep(1)  # To avoid rate limits
        else:
            for country, cities in data.items():
                for city in cities:
                    print(f"📍 Fetching data for {city}, {country} in {continent}...")
                    result = fetch_aqi(city)
                    if result:
                        writer.writerow([result[0], continent, country, city, result[1], result[2], result[3], result[4]])
                    time.sleep(1)  # To avoid rate limits