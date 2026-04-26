"""
UNIVERSITY PORTAL - SYSTEM CONSTANTS & STANDARDS
=====================================
Unified configuration for Nigerian University Portal
Aligned with NUC standards and global best practices

Version: 2.0.0
Last Updated: 2024
"""

from typing import List, Dict, Optional
from enum import Enum


# =============================================================================
# PART 1: NIGERIAN UNIVERSITIES REGISTRY
# =============================================================================
NIGERIAN_UNIVERSITIES = {
    "UNN": {"name": "University of Nigeria, Nsukka", "state": "Enugu", "year": 1960, "type": "Federal"},
    "UI": {"name": "University of Ibadan", "state": "Oyo", "year": 1948, "type": "Federal"},
    "UNILAG": {"name": "University of Lagos", "state": "Lagos", "year": 1962, "type": "Federal"},
    "OAU": {"name": "Obafemi Awolowo University", "state": "Osun", "year": 1961, "type": "Federal"},
    "UNILORIN": {"name": "University of Ilorin", "state": "Kwara", "year": 1975, "type": "Federal"},
    "UNIBEN": {"name": "University of Benin", "state": "Edo", "year": 1970, "type": "Federal"},
    "UNICAL": {"name": "University of Calabar", "state": "Cross River", "year": 1975, "type": "Federal"},
    "OAU": {"name": "Obafemi Awolowo University", "state": "Osun", "year": 1961, "type": "Federal"},
    "FUT_Minna": {"name": "Federal University of Technology, Minna", "state": "Niger", "year": 1983, "type": "Federal"},
    "FUT_Owerri": {"name": "Federal University of Technology, Owerri", "state": "Imo", "year": 1980, "type": "Federal"},
    "LAUTECH": {"name": "Ladoke Akintola University of Technology", "state": "Oyo", "year": 1990, "type": "State"},
    "UNIZIK": {"name": "Nnamdi Azikiwe University", "state": "Anambra", "year": 1990, "type": "Federal"},
    "ESUT": {"name": "Enugu State University of Science and Technology", "state": "Enugu", "year": 1990, "type": "State"},
    "RSUST": {"name": "Rivers State University", "state": "Rivers", "year": 1972, "type": "State"},
    "UNAD": {"name": "Nigerian Army University", "state": "Borno", "year": 2018, "type": "Military"},
}


# =============================================================================
# PART 2: NIGERIAN STATES & LOCAL GOVERNMENTS (COMPLETE)
# =============================================================================
NIGERIAN_STATES = [
    "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue", 
    "Borno", "Cross River", "Delta", "Ebonyi", "Edo", "Ekiti", "Enugu", 
    "Gombe", "Imo", "Jigawa", "Kaduna", "Kano", "Katsina", "Kebbi", 
    "Kogi", "Kwara", "Lagos", "Nasarawa", "Niger", "Ogun", "Ondo", 
    "Osun", "Oyo", "Plateau", "Sokoto", "Taraba", "Yobe", "Zamfara",
    "Federal Capital Territory"
]

# Major LGAs for each state
NIGERIAN_LGAS = {
    "Abia": ["Aba North", "Aba South", "Arochukwu", "Bende", "Ikwuano", "Isiala-Ngwa North", "Isiala-Ngwa South", "Isuikwuato", "Obing", "Ohafia", "Osisioma", "Ugunagbo", "Ukwa East", "Ukwa West", "Umu-Nneochi"],
    "Adamawa": ["Abuja", "Demsa", "Fufore", "Ganye", "Girei", "Gombi", "Hong", "Jada", "Lamurde", "Madagali", "Maiha", "Mayo-Belwa", "Michika", "Mubi North", "Mubi South", "Numana", "Shelleng", "Song", "Toungo", "Yola"],
    "Akwa Ibom": ["Abak", "Eastern Obolo", "Eket", "Esit Eket", "Essien Udim", "Etinan", "Ibeno", "Ibesikpo Asutan", "Ibiono Ibom", "Ikot Abasi", "Ikot Ekpene", "Ini", "Itu", "Mbo", "Mkpat-Enin", "Nsit Atai", "Nsit Ibom", "Nsit-Ugun", "Obot Akara", "Okobo", "Onna", "Oron", "Oruk Anam", "Udummy", "Ukanafun", "Uruan", "Uruke", "Uyo"],
    "Anambra": ["Aguata", "Ajali", "Anambra East", "Anambra West", "Anaocha", "Awka North", "Awka South", "Ayamelum", "Dunukofia", "Ekwusigo", "Idemili North", "Idemili South", "Ihiala", "Njikoka", "Nnewi North", "Nnewi South", "Ogidi", "Onitsha North", "Onitsha South", "Orumba North", "Orumba South", "Oyi"],
    "Bauchi": ["Alagarn", "Bama", "Bauchi", "Bogoro", "Dambam", "Darako", "Domo", "Gamawa", "Ganjuwa", "Giade", "Itas Gada", "Jamaare", "Katagum", "Kiyawa", "Madara", "Misau", "Ningi", "Shira", "Tafawa Balewa", "Toro", "Warji", "Zaku"],
    "Bayelsa": ["Brass", "Ekeremor", "Kolokuma-Opokuma", "Nembe", "Ogbia", "Sagbama", "Southern Ijaw", "Yenagoa"],
    "Benue": ["Ado", "Agatu", "Apa", "Buruku", "Gboko", "Guma", "Gwer East", "Gwer West", "Kastina-A", "Konshisha", "Kwande", "Logo", "Makurdi", "Obi", "Ogbadibo", "Ohimini", "Okpokwu", "Otukpo", "Tarka", "Ukum", "Ushongo", "Vandeikya"],
    "Borno": ["Abadam", "Askira-Uba", "Bama", "Bayo", "Biu", "Chibok", "Damboa", "Dikwa", "Gubio", "Guzamala", "Gwoza", "Kala-Balge", "Kukawa", "Kwaya Kusar", "Maiduguri", "Marte", "Mobbar", "Monguno", "Ngala", "Shani"],
    "Cross River": ["Abi", "Akamkpa", "Akpabuyo", "Bakassi", "Bekwarra", "Biase", "Bokal", "Calabar Municipal", "Calabar South", "Etung", "Ikom", "Obanliku", "Obubara", "Obudu", "Odukpani", "Ogoja", "Okpoma", "Ugep North", "Ugep South", "Yakkur"],
    "Delta": ["Aniocha North", "Aniocha South", "Bomadi", "Burutu", "Debe", "Ethiope East", "Ethiope West", "Ika North East", "Ika South", "Isoko North", "Isoko South", "Ndokwa East", "Ndokwa West", "Okpe", "Oshimili North", "Oshimili South", "Patani", "Sapele", "Udu", "Ughelli North", "Ughelli South", "Ukwuani", "Warri North", "Warri South", "Warri South West"],
    "Ebonyi": ["Abakaliki", "Afikpo North", "Afikpo South", " Ivo", "Ebonyi", "Ezza North", "Ezza South", "Ikwo", "Ishielu", "Izzi", "Ohaukwu", "Onicha", "Ohaozara", "Okpoto", "Oshare", "Ukaba", "Unuhu"],
    "Edo": ["Akoko-Edo", "Aston", "Egor", "Esan Central", "Esan North East", "Esan South East", "Esan West", "Etsako Central", "Etsako East", "Etsako West", "Igueben", "Ikpoba-Okha", "Ivi-Osse", "Oredo", "Orhionmwon", "Ovia North East", "Ovia North West", "Ovia South East", "Ovia South West", "Uhumwonde"],
    "Ekiti": ["Ado-Ekiti", "Aiyegbaju", "Efon", "Ekiti East", "Ekiti South West", "Ekiti-West", "Emure", " Gbonyin", "Ido-Osi", "Ijero", "Ikole", "Ile-Ife", "Irepodun", "Ise-Orun", "Moba", "Oye"],
    "Enugu": ["Aninri", "Awgu", "Awka North", "Awka South", "Enugu East", "Enugu North", "Enugu South", "Ezeagu", "Igbo-Etiti", "Igbo-Eze North", "Igbo-Eze South", "Isi-Uzo", "Nkanu East", "Nkanu West", "Nsukka", "Oji River", "Ugwuanke", "Uguo"],
    "Gombe": ["Akko", "Balanga", "Billiri", "Dukku", "Funakaye", "Gombe", "Kaltungo", "Kwami", "Nafada", "Shomgom", "Yer"],
    "Imo": ["Aboh-Mbaise", "Ahiazu-Mbaise", "Ehime-Mbano", "Ekwas", "Etsako", "Ideato North", "Ideato South", "Ihitte/Uboma", "Ikeduru", "Isu", "Mbaitoli", "Nnemili", "Nkwerre", "Nwangele", "Obowo", "Oguta", "Ohaji-Egbema", "Okigwe", "Orlu", "Orsu", "Oru East", "Oru West", "Owerri-Municipal", "Owerri-North", "Owerri-West", "Unush"],
    "Jigawa": ["Auyo", "Babura", "Birnin Kudu", "Birniwa", "Buji", "Django", "Garki", "Gumel", "Gwarin", "Hadejia", "Jahun", "Kafin Madaki", "Kaugama", "Kazaure", "Kiri Kasamma", "Malam Madori", "Mini", "Ringim", "Roni", "Sabon Birni", "Saga", "Shakar", "Suleiman Tankarkar", "Yankwako"],
    "Kaduna": ["Birnin Gwari", "Chikun", "Giwa", "Igabi", "Ikara", "Jemaa", "Kachia", "Kaduna North", "Kaduna South", "Kagarko", "Kano", "Karaye", "Kubau", "Kudan", "Lere", "Makarfi", "Sabon Gari", "Sango", "Soba", "Zaria"],
    "Kano": ["Ajingi", "Albasu", "Bagwai", "Bebe", "Bichi", "Bunkure", "Dala", "Dambatta", "Danbatta", "Doguwa", "Fagge", "Gaya", "Gezawa", "Gwale", "Gwarzo", "Kabo", "Kano Municipal", "Karaye", "Kibiya", "Kiru", "Kumbotso", "Kura", "Madobi", "Makoda", "Minjibir", "Nasarawa", "Rano", "Rimin Gata", "Rogo", "Shanono", "Sumaila", "Takai", "Tarauni", "Tofa", "Tsanyawa", "Tudun Wada", "Ungogo", "Warawa", "Wudil"],
    "Katsina": ["Bakori", "Batagarawa", "Batsari", "Baure", "Bindawa", "Charanchi", "Dandume", "Danja", "Dan Musa", "Daura", " Dutsi", "Dutsin-Ma", "Faskari", "Gozain", "Ingawa", "Jibia", "Kafur", "Kaita", "Kankara", "Kankia", "Katsina", "Kurfi", "Kusada", "Mai'Adua", "Malumfashi", "Mani", "Masanawa", "Matazu", "Mikoshi", "Miyetti", "Rimi", "Sabuwar Kuka", "Safana", "Sandamu", "Shinkafi", "Sikkal", "Sinmari", "Zango"],
    "Kebbi": ["Aleiro", "Arewa Dandi", "Argungu", "Augie", "Bagudo", "Birnin Kebbi", "Bunza", "Dandi", "D Was", "Fakai", "Gwandu", "Jedu", "Kalgo", "Koko/Besse", "Maiyama", "Ngaski", "Sakaba", "Shanga", "Suru", "Wasagu", "Yendi", "Zuru"],
    "Kogi": ["Adavi", "Ajaokuta", "Ankpa", "Bassa", "Dekina", "Ibaji", "Idah", "Igalamela-Odolu", "Ijumu", "Kabba/Bunu", "Koton Karfe", "Lokoja", "Mopa-Muro", "Ofu", "Ogori/Magongo", "Okehi", "Okengbo", "Olamaboro", "Omala", "Yagba East", "Yagba West"],
    "Kwara": ["ASA", "Baruten", "Edu", "Ekiti", "Ife", "Ilorin East", "Ilorin South", "Ilorin West", "Irepodun", "Isin", "Kaiama", "Moro", "Offa", "Oke Ero", "Oyun", "Paki", "Patigi", "Sanyi", "Toru"],
    "Lagos": ["Agege", "Ajeromi-Ifelodun", "Alimosho", "Amuwo-Odofin", "Apapa", "Badagry", "Epe", "Eti-Osa", "Ibeju-Lekki", "Ifako-Ijaye", "Ikeja", "Ikorodu", "Kosofe", "Lagos Island", "Lagos Mainland", "Mushin", "Ojo", "Oshodi-Isolo", "Shomolu", "Surulere"],
    "Nasarawa": ["Akwanga", "Awe", "Doma", "Karu", "Keana", "Keffi", "Kokona", "Lafia", "Nasarawa", "Nasarawa Egon", "Obi", "Toto", "Wamba"],
    "Niger": ["Agaie", "Agwara", "Bida", "Bobby", "Bosso", "Chanchaga", "Edati", "Gbako", "Gurman", "Katcha", "Kontagora", "Lapai", "Lavun", "Magama", "Mariga", "Mashegu", "Moa", "Munya", "Paikoro", "Rafi", "Rijau", "Shiroro", "Suleja", "Tafa", "Wushishi"],
    "Ogun": ["Abeokuta North", "Abeokuta South", "Ado-Odo Ota", "Ewekoro", "Ibadan North", "Ibadan North West", "Ibadan South East", "Ibadan South West", "Ifo", "Ijebu North", "Ijebu Ode", "Ikenne", "Imeko Afon", "Ipokia", "Obafemi Owode", "Odogbolu", "Ogun Waterside", "Remo North", "Remo South", "Sagamu"],
    "Ondo": ["Akoko North East", "Akoko North West", "Akoko South East", "Akoko South West", "Akure North", "Akure South", "Owo", "Ose", "Ode-Aye", "Ilara", "Ileoluji", "Irele", "Isua", "Ondo", "Ondo West", "Owo"],
    "Osun": ["Aiyedaade", "Aiyedire", "Atakunmosa East", "Atakunmosa West", "Atakunmosa", "Boluwaduro", "Boripe", "Ede North", "Ede South", "Egbedore", "Ejigbo", "Ife Central", "Ife East", "Ife North", "Ife South", "Ifedayo", "Ila", "Ilesha East", "Ilesha West", "Irepodun", "Irepodun", "Isokan", "Iwo", "Obaj", "Odo-Otin", "Odo-Oyu", "Ola Oluwa", "Olorunda", "Oriade", "Orolu", "Osogbo"],
    "Oyo": ["Afijio", "Akinyele", "Atiba", "Atisbo", "Egbeda", "Ibadan Central", "Ibadan North", "Ibadan North West", "Ibadan South East", "Ibadan South West", "Ibarapa Central", "Ibarapa East", "Ibarapa North", "Ido", "Irepo", "Iseyin", "Itisi", "Lagelu", "Ogbomosho North", "Ogbomosho South", "Ogo Oluwa", "Olorunsogo", "Oyo", "Oyo East", "Saki East", "Saki West", "Surulere"],
    "Plateau": ["Barkin Ladi", "Bassa", "Bokkos", "Jos East", "Jos North", "Jos South", "Kanam", "Kanke", "Langtang North", "Langtang South", "Mangu", "Mikang", "Pankshin", "Qua'an Pan", "Riyom", "Shendam", "Wase"],
    "Sokoto": ["Binji", "Bodinga", "Dange", "Gada", "Goronyo", "Gudu", "Gwadabawa", "Illela", "Isa", "Kabin", "Kalka", "Kangiwa", "Keta", "Kware", "Sokoto North", "Sokoto South", "Taloka", "Tangaza", "Tureta", "Wamako", "Wurno", "Yabo"],
    "Taraba": ["Ardo Kola", "Bali", "Donga", "Gashaka", "Gassol", "Ibi", "Jalingo", "Karin-Lamido", "Kurfi", "Lau", "Sardauna", "Takum", "Ussa", "Wukari", "Yorro", "Zing"],
    "Yobe": ["Bade", "Bursari", "Damaturu", "Fune", "Geidam", "Gujba", "Gulani", "Kagas", "Kukuwa", "Machina", "Nangere", "Nguru", "Potiskum", "Tarmu", "Yunus"],
    "Zamfara": ["Anka", "Bakura", "Birnin Magaji", "Bukkuyum", "Bungudu", "Chafe", "Dansage", "Doka", "Galadi", "Gasau", "Gummi", "Gusau", "Kaura Namoda", "Kiyawa", "Maradun", "Moriki", "Shinkafi", "Talata Mafara", "Zurmi"],
}


NIGERIAN_COUNTRIES = [
    # Africa (54 countries)
    "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cabo Verde", "Cameroon", 
    "Central African Republic", "Chad", "Comoros", "Democratic Republic of the Congo", "Republic of the Congo",
    "Djibouti", "Egypt", "Equatorial Guinea", "Eritrea", "Eswatini", "Ethiopia", "Gabon", "Gambia", 
    "Ghana", "Guinea", "Guinea-Bissau", "Ivory Coast", "Kenya", "Lesotho", "Liberia", "Libya", 
    "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius", "Morocco", "Mozambique", "Namibia", 
    "Niger", "Nigeria", "Rwanda", "São Tomé and Príncipe", "Senegal", "Seychelles", "Sierra Leone", 
    "Somalia", "South Africa", "South Sudan", "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", 
    "Zimbabwe",
    # Europe (44 countries)
    "Albania", "Andorra", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia",
    "Cyprus", "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", 
    "Hungary", "Iceland", "Ireland", "Italy", "Kosovo", "Latvia", "Liechtenstein", "Lithuania", 
    "Luxembourg", "Malta", "Moldova", "Monaco", "Montenegro", "Netherlands", "North Macedonia", "Norway", 
    "Poland", "Portugal", "Romania", "Russia", "San Marino", "Serbia", "Slovakia", "Slovenia", "Spain", 
    "Sweden", "Switzerland", "Ukraine", "United Kingdom", "Vatican City",
    # Asia (49 countries)
    "Afghanistan", "Armenia", "Azerbaijan", "Bahrain", "Bangladesh", "Bhutan", "Brunei", "Cambodia", "China", 
    "Georgia", "India", "Indonesia", "Iran", "Iraq", "Israel", "Japan", "Jordan", "Kazakhstan", "Kuwait", 
    "Kyrgyzstan", "Laos", "Lebanon", "Malaysia", "Maldives", "Mongolia", "Myanmar", "Nepal", "North Korea", 
    "Oman", "Pakistan", "Palestine", "Philippines", "Qatar", "Saudi Arabia", "Singapore", "South Korea", 
    "Sri Lanka", "Syria", "Taiwan", "Tajikistan", "Thailand", "Timor-Leste", "Turkey", "Turkmenistan", 
    "United Arab Emirates", "Uzbekistan", "Vietnam", "Yemen",
    # North America (23 countries/territories)
    "Antigua and Barbuda", "Bahamas", "Barbados", "Belize", "Canada", "Costa Rica", "Cuba", "Dominica", 
    "Dominican Republic", "El Salvador", "Grenada", "Guatemala", "Haiti", "Honduras", "Jamaica", "Mexico", 
    "Nicaragua", "Panama", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", 
    "Trinidad and Tobago", "United States",
    # South America (12 countries)
    "Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador", "Guyana", "Paraguay", "Peru", 
    "Suriname", "Uruguay", "Venezuela",
    # Oceania (14 countries/territories)
    "Australia", "Fiji", "Kiribati", "Marshall Islands", "Micronesia", "Nauru", "New Zealand", 
    "Palau", "Papua New Guinea", "Samoa", "Solomon Islands", "Tonga", "Tuvalu", "Vanuatu",
    # Caribbean & Caribbean Territories
    "Anguilla", "Aruba", "British Virgin Islands", "Cayman Islands", "Curaçao", "Guadeloupe", 
    "Martinique", "Montserrat", "Puerto Rico", "Sint Maarten", "Turks and Caicos Islands", "U.S. Virgin Islands",
]


# =============================================================================
# PART 3: ACADEMIC STANDARDS (NUC ALIGNED)
# =============================================================================
ACADEMIC_PROGRAMMES = {
    "Computer Science": {"code": "CSC", "duration": 4, "min_units": 120, "category": "Science"},
    "Information Technology": {"code": "IT", "duration": 4, "min_units": 120, "category": "Science"},
    "Software Engineering": {"code": "SENG", "duration": 5, "min_units": 150, "category": "Engineering"},
    "Computer Engineering": {"code": "CEN", "duration": 5, "min_units": 150, "category": "Engineering"},
    "Electrical Engineering": {"code": "ELE", "duration": 5, "min_units": 150, "category": "Engineering"},
    "Mechanical Engineering": {"code": "MCE", "duration": 5, "min_units": 150, "category": "Engineering"},
    "Civil Engineering": {"code": "CVE", "duration": 5, "min_units": 150, "category": "Engineering"},
    "Accounting": {"code": "ACC", "duration": 4, "min_units": 120, "category": "Management"},
    "Business Administration": {"code": "BA", "duration": 4, "min_units": 120, "category": "Management"},
    "Economics": {"code": "ECO", "duration": 4, "min_units": 120, "category": "Management"},
    "Medicine": {"code": "MED", "duration": 6, "min_units": 180, "category": "Health"},
    "Law": {"code": "LAW", "duration": 5, "min_units": 150, "category": "Law"},
    "Mass Communication": {"code": "MCM", "duration": 4, "min_units": 120, "category": "Arts"},
    "English": {"code": "ENG", "duration": 4, "min_units": 120, "category": "Arts"},
    "History": {"code": "HIS", "duration": 4, "min_units": 120, "category": "Arts"},
}


GRADING_SCALE = [
    {"grade": "A", "min_score": 70, "max_score": 100, "points": 5.0, "class": "Excellent", "description": "Outstanding"},
    {"grade": "B", "min_score": 60, "max_score": 69, "points": 4.0, "class": "Very Good", "description": "Above average"},
    {"grade": "C", "min_score": 50, "max_score": 59, "points": 3.0, "class": "Good", "description": "Average"},
    {"grade": "D", "min_score": 45, "max_score": 49, "points": 2.0, "class": "Pass", "description": "Below average"},
    {"grade": "E", "min_score": 40, "max_score": 44, "points": 1.0, "class": "Fair Pass", "description": "Marginal"},
    {"grade": "F", "min_score": 0, "max_score": 39, "points": 0.0, "class": "Fail", "description": "Below standard"},
]


DEGREE_CLASSIFICATIONS = [
    {"class": "First Class", "cgpa_min": 4.5, "cgpa_max": 5.0, "honours": "Distinction"},
    {"class": "Second Class Upper", "cgpa_min": 3.5, "cgpa_max": 4.49, "honours": "Merit"},
    {"class": "Second Class Lower", "cgpa_min": 2.5, "cgpa_max": 3.49, "honours": "Credit"},
    {"class": "Third Class", "cgpa_min": 2.0, "cgpa_max": 2.49, "honours": "Pass"},
    {"class": "Pass", "cgpa_min": 1.5, "cgpa_max": 1.99, "honours": "Pass"},
    {"class": "Probation", "cgpa_min": 0.0, "cgpa_max": 1.49, "honours": "Academic Probation"},
]


# =============================================================================
# PART 4: COURSE WEIGHTS & STRUCTURE
# =============================================================================
COURSE_WEIGHTS = {
    "ca_weight": 30.0,
    "exam_weight": 70.0,
    "min_ca": 0.0,
    "max_ca": 30.0,
    "min_exam": 0.0,
    "max_exam": 70.0,
    "total": 100.0,
    "pass_mark": 40.0,
}


ACADEMIC_LEVELS = [
    {"level": 100, "name": "100 Level", "description": "First Year", "year": 1},
    {"level": 200, "name": "200 Level", "description": "Second Year", "year": 2},
    {"level": 300, "name": "300 Level", "description": "Third Year", "year": 3},
    {"level": 400, "name": "400 Level", "description": "Fourth Year", "year": 4},
    {"level": 500, "name": "500 Level", "description": "Fifth Year", "year": 5},
    {"level": 600, "name": "600 Level", "description": "Sixth Year", "year": 6},
]


SEMESTERS = [
    {"id": "first", "name": "First Semester", "months": "Sep-Dec"},
    {"id": "second", "name": "Second Semester", "months": "Jan-May"},
    {"id": "rain", "name": "Rainfall Semester", "months": "Jul-Aug"},
]


# =============================================================================
# PART 5: IDENTIFICATION NUMBERS
# =============================================================================
IDENTIFICATION_FORMAT = {
    "nin": {"length": 11, "format": "XXXXXXXXXXX", "description": "National Identification Number"},
    "bvn": {"length": 11, "format": "XXXXXXXXXXX", "description": "Bank Verification Number"},
    "matric": {"format": "XXX/YYYY/NNN", "description": "Matriculation Number"},
    "jamb": {"length": 10, "format": "XXXXXXXXXX", "description": "JAMB Registration Number"},
    "passport": {"length": 9, "format": "AXXXXXXXX", "description": "International Passport"},
}


# =============================================================================
# PART 6: BLOOD GENOTYPES & GROUPS
# =============================================================================
BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
GENOTYPES = ["AA", "AS", "SS", "AC", "CS"]
RELIGIONS = ["Christianity", "Islam", "Traditional", "Others", "None"]
MARITAL_STATUSES = ["Single", "Married", "Divorced", "Widowed", "Separated"]


# =============================================================================
# PART 7: USER ROLES (COMPREHENSIVE)
# =============================================================================
USER_ROLES = {
    "admin": {
        "name": "System Administrator",
        "level": 1,
        "description": "Full system access",
        "permissions": ["*"]
    },
    "student": {
        "name": "Student",
        "level": 10,
        "description": "Regular student user",
        "permissions": ["courses:read", "grades:read", "enroll:write"]
    },
    "lecturer": {
        "name": "Lecturer",
        "level": 5,
        "description": "Academic staff",
        "permissions": ["courses:write", "grades:write", "attendance:write"]
    },
    "hod": {
        "name": "Head of Department",
        "level": 4,
        "description": "Department head",
        "permissions": ["department:write", "reports:write"]
    },
    "dean": {
        "name": "Dean",
        "level": 3,
        "description": "Faculty head",
        "permissions": ["faculty:write", "reports:write"]
    },
    "registrar": {
        "name": "Registrar",
        "level": 2,
        "description": "Student records",
        "permissions": ["students:write", "transcripts:write"]
    },
    "finance_officer": {
        "name": "Finance Officer",
        "level": 2,
        "description": "Financial operations",
        "permissions": ["finance:write"]
    },
    "exam_officer": {
        "name": "Exam Officer",
        "level": 4,
        "description": "Exam management",
        "permissions": ["exam:write"]
    },
    "librarian": {
        "name": "Librarian",
        "level": 5,
        "description": "Library management",
        "permissions": ["library:write"]
    },
    "siwes_coordinator": {
        "name": "SIWES Coordinator",
        "level": 4,
        "description": "Industrial training",
        "permissions": ["siwes:write"]
    },
    "alumni_officer": {
        "name": "Alumni Officer",
        "level": 5,
        "description": "Alumni relations",
        "permissions": ["alumni:write"]
    },
}


# =============================================================================
# PART 8: PAYMENT GATEWAYS (NIGERIAN)
# =============================================================================
NIGERIAN_PAYMENT_METHODS = [
    {"id": "remita", "name": "Remita", "type": "Federal", "code": "*894#"},
    {"id": "paystack", "name": "Paystack", "type": "Card", "code": "PS"},
    {"id": "flutterwave", "name": "Flutterwave", "type": "Card", "code": "FW"},
    {"id": "bank_transfer", "name": "Bank Transfer", "type": "USSD", "code": "*894#"},
    {"id": "ussd", "name": "USSD Banking", "type": "USSD", "code": "*XXX#"},
]


# =============================================================================
# PART 9: EXPORT CONSTANTS
# =============================================================================
__all__ = [
    "NIGERIAN_UNIVERSITIES",
    "NIGERIAN_STATES",
    "NIGERIAN_LGAS",
    "NIGERIAN_COUNTRIES",
    "ACADEMIC_PROGRAMMES",
    "GRADING_SCALE",
    "DEGREE_CLASSIFICATIONS",
    "COURSE_WEIGHTS",
    "ACADEMIC_LEVELS",
    "SEMESTERS",
    "IDENTIFICATION_FORMAT",
    "BLOOD_GROUPS",
    "GENOTYPES",
    "RELIGIONS",
    "MARITAL_STATUSES",
    "USER_ROLES",
    "NIGERIAN_PAYMENT_METHODS",
]