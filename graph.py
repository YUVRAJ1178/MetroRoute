"""
graph.py - Official Comprehensive Delhi-NCR Metro (DMRC + NCR) Network
-----------------------------------------------------------------------
This file implements:
1. An unweighted, undirected Graph using an Adjacency List (Python dictionary).
2. Breadth-First Search (BFS) using a Queue (collections.deque) to find
   the route with the minimum number of stops.
3. Path reconstruction using a parent dictionary.
4. Comprehensive real DMRC + NCR network data covering 264 stations across 12 lines:
   Red, Yellow, Blue, Blue Branch, Green, Violet, Pink (Ring), Magenta, Grey,
   Airport Express (with Yashobhoomi), Aqua Line (Noida Metro), and Rapid Metro Gurugram.
"""

from collections import deque

# Official Line Color Codes
LINE_COLORS = {
    "Red Line": "#E31B23",
    "Yellow Line": "#FDB813",
    "Blue Line": "#0066B2",
    "Blue Line Branch": "#0066B2",
    "Green Line": "#009639",
    "Violet Line": "#6F2C91",
    "Pink Line": "#E83D84",
    "Magenta Line": "#B82687",
    "Grey Line": "#808285",
    "Airport Express": "#F58220",
    "Aqua Line (Noida)": "#00B5E2",
    "Rapid Metro Gurugram": "#4682B4"
}

# 2D Schematic Coordinates for Metro Map (Canvas 1650 x 1420)
STATION_COORDINATES = {'Samaypur Badli': [800, 60], 'Azadpur': [800, 240], 'Kashmere Gate': [800, 360], 'New Delhi': [800, 520], 'Rajiv Chowk': [800, 600], 'Central Secretariat': [800, 720], 'Dilli Haat INA': [800, 870], 'Hauz Khas': [800, 1020], 'Qutub Minar': [800, 1160], 'Millennium City Centre': [800, 1340], 'Rithala': [200, 360], 'Netaji Subhash Place': [420, 360], 'Inderlok': [560, 360], 'Welcome': [1050, 360], 'Dilshad Garden': [1260, 360], 'Shaheed Sthal (New Bus Adda)': [1520, 360], 'Dwarka Sector 21': [120, 780], 'Dwarka': [200, 660], 'Janakpuri West': [350, 600], 'Rajouri Garden': [500, 600], 'Kirti Nagar': [600, 600], 'Karol Bagh': [720, 600], 'Mandi House': [900, 600], 'Yamuna Bank': [1050, 600], 'Mayur Vihar-I': [1180, 680], 'Botanical Garden': [1340, 760], 'Noida City Centre': [1440, 810], 'Noida Electronic City': [1540, 860], 'Anand Vihar': [1240, 480], 'Karkarduma': [1200, 500], 'Vaishali': [1380, 440], 'Brigadier Hoshiar Singh': [80, 480], 'Mundka': [250, 480], 'Ashok Park Main': [500, 480], 'Satguru Ram Singh Marg': [550, 540], 'Lajpat Nagar': [960, 890], 'Kalkaji Mandir': [1080, 1030], 'Badarpur Border': [1080, 1200], 'Raja Nahar Singh (Ballabhgarh)': [1080, 1360], 'Majlis Park': [680, 180], 'Shalimar Bagh': [560, 240], 'Punjabi Bagh West': [400, 480], 'Durgabai Deshmukh South Campus': [540, 780], 'Trilokpuri Sanjay Lake': [1240, 600], 'Shiv Vihar': [1150, 160], 'Terminal 1 IGI Airport': [400, 860], 'IIT Delhi': [680, 1020], 'Shivaji Stadium': [740, 550], 'Dhaula Kuan': [560, 720], 'Delhi Aerocity': [420, 820], 'IGI Airport': [300, 860], 'Dhansa Bus Stand': [80, 660], 'Rohini West': [244, 360], 'Rohini East': [288, 360], 'Pitampura': [332, 360], 'Kohat Enclave': [376, 360], 'Keshav Puram': [467, 360], 'Kanhaiya Nagar': [513, 360], 'Shastri Nagar': [608, 360], 'Pratap Nagar': [656, 360], 'Pul Bangash': [704, 360], 'Tis Hazari': [752, 360], 'Shastri Park': [883, 360], 'Seelampur': [967, 360], 'Shahdara': [1102, 360], 'Mansarovar Park': [1155, 360], 'Jhilmil': [1208, 360], 'Shaheed Nagar': [1292, 360], 'Raj Bagh': [1325, 360], 'Major Mohit Sharma Rajendra Nagar': [1358, 360], 'Shyam Park': [1390, 360], 'Mohan Nagar': [1422, 360], 'Arthala': [1455, 360], 'Hindon River': [1488, 360], 'Rohini Sector 18': [800, 96], 'Haiderpur Badli Mor': [800, 132], 'Jahangirpuri': [800, 168], 'Adarsh Nagar': [800, 204], 'Model Town': [800, 260], 'GTB Nagar': [800, 280], 'Vishwavidyalaya': [800, 300], 'Vidhan Sabha': [800, 320], 'Civil Lines': [800, 340], 'Chandni Chowk': [800, 413], 'Chawri Bazar': [800, 467], 'Patel Chowk': [800, 660], 'Udyog Bhawan': [800, 758], 'Lok Kalyan Marg': [800, 795], 'Jor Bagh': [800, 832], 'AIIMS': [800, 920], 'Green Park': [800, 970], 'Malviya Nagar': [800, 1067], 'Saket': [800, 1113], 'Chhatarpur': [800, 1180], 'Sultanpur': [800, 1200], 'Ghitorni': [800, 1220], 'Arjan Garh': [800, 1240], 'Guru Dronacharya': [800, 1260], 'Sikandarpur': [800, 1280], 'MG Road': [800, 1300], 'IFFCO Chowk': [800, 1320], 'Dwarka Sector 8': [130, 765], 'Dwarka Sector 9': [140, 750], 'Dwarka Sector 10': [150, 735], 'Dwarka Sector 11': [160, 720], 'Dwarka Sector 12': [170, 705], 'Dwarka Sector 13': [180, 690], 'Dwarka Sector 14': [190, 675], 'Dwarka Mor': [230, 648], 'Nawada': [260, 636], 'Uttam Nagar West': [290, 624], 'Uttam Nagar East': [320, 612], 'Janakpuri East': [380, 600], 'Tilak Nagar': [410, 600], 'Subhash Nagar': [440, 600], 'Tagore Garden': [470, 600], 'Ramesh Nagar': [533, 600], 'Moti Nagar': [567, 600], 'Shadipur': [630, 600], 'Patel Nagar': [660, 600], 'Rajendra Place': [690, 600], 'Jhandewalan': [747, 600], 'RK Ashram Marg': [773, 600], 'Barakhamba Road': [850, 600], 'Supreme Court': [950, 600], 'Indraprastha': [1000, 600], 'Akshardham': [1115, 640], 'Mayur Vihar Extension': [1207, 693], 'New Ashok Nagar': [1233, 707], 'Noida Sector 15': [1260, 720], 'Noida Sector 16': [1287, 733], 'Noida Sector 18': [1313, 747], 'Golf Course': [1390, 785], 'Sector 34': [1457, 818], 'Sector 52': [1473, 827], 'Sector 61': [1490, 835], 'Sector 59': [1507, 843], 'Sector 62': [1523, 852], 'Laxmi Nagar': [1088, 575], 'Nirman Vihar': [1125, 550], 'Preet Vihar': [1162, 525], 'Kaushambi': [1310, 460], 'Punjabi Bagh East': [479, 480], 'Shivaji Park': [458, 480], 'Madipur': [438, 480], 'Paschim Vihar East': [417, 480], 'Paschim Vihar West': [396, 480], 'Peeragarhi': [375, 480], 'Udyog Nagar': [354, 480], 'Maharaja Surajmal Stadium': [333, 480], 'Nangloi': [312, 480], 'Nangloi Railway Station': [292, 480], 'Rajdhani Park': [271, 480], 'Mundka Industrial Area': [226, 480], 'Ghevra': [201, 480], 'Tikri Kalan': [177, 480], 'Tikri Border': [153, 480], 'Pandit Shree Ram Sharma': [129, 480], 'Bahadurgarh City': [104, 480], 'Lal Qila': [820, 408], 'Jama Masjid': [840, 456], 'Delhi Gate': [860, 504], 'ITO': [880, 552], 'Janpath': [850, 660], 'Khan Market': [840, 762], 'JLN Stadium': [880, 805], 'Jangpura': [920, 848], 'Moolchand': [990, 925], 'Kailash Colony': [1020, 960], 'Nehru Place': [1050, 995], 'Govind Puri': [1080, 1054], 'Harkesh Nagar Okhla': [1080, 1079], 'Jasola Apollo': [1080, 1103], 'Sarita Vihar': [1080, 1127], 'Mohan Estate': [1080, 1151], 'Tughlakabad': [1080, 1176], 'Sarai': [1080, 1215], 'NHPC Chowk': [1080, 1229], 'Mewala Maharajpur': [1080, 1244], 'Sector 28': [1080, 1258], 'Badkhal Mor': [1080, 1273], 'Faridabad Old': [1080, 1287], 'Neelam Chowk Ajronda': [1080, 1302], 'Bata Chowk': [1080, 1316], 'Escorts Mujesar': [1080, 1331], 'Sant Surdas (Sihi)': [1080, 1345], 'Shakurpur': [410, 420], 'ESI Basaidarapur': [450, 540], 'Mayapuri': [510, 645], 'Naraina Vihar': [520, 690], 'Delhi Cantt': [530, 735], 'Sir M. Vishweshwaraiah Moti Bagh': [605, 802], 'Bhikaji Cama Place': [670, 825], 'Sarojini Nagar': [735, 848], 'South Extension': [880, 880], 'Vinobapuri': [1015, 838], 'Ashram': [1070, 785], 'Sarai Kale Khan Nizamuddin': [1125, 732], 'Mayur Vihar Pocket 1': [1210, 640], 'East Vinod Nagar–Mayur Vihar-II': [1240, 570], 'Mandawali–West Vinod Nagar': [1240, 540], 'IP Extension': [1240, 510], 'Karkarduma Court': [1162, 465], 'Krishna Nagar': [1125, 430], 'East Azad Nagar': [1088, 395], 'Jaffrabad': [1067, 327], 'Maujpur-Babarpur': [1083, 293], 'Bhajanpura': [1100, 260], 'Gokulpuri': [1117, 227], 'Johri Enclave': [1133, 193], 'Dabri Mor–Janakpuri South': [360, 652], 'Dashrath Puri': [370, 704], 'Palam': [380, 756], 'Sadar Bazar Cantonment': [390, 808], 'Shankar Vihar': [456, 892], 'Vasant Vihar': [512, 924], 'Munirka': [568, 956], 'R.K. Puram': [624, 988], 'Panchsheel Park': [856, 1022], 'Chirag Delhi': [912, 1024], 'Greater Kailash': [968, 1026], 'Nehru Enclave': [1024, 1028], 'Okhla NSIC': [1112, 996], 'Sukhdev Vihar': [1145, 962], 'Jamia Millia Islamia': [1178, 929], 'Okhla Vihar': [1210, 895], 'Jasola Vihar Shaheen Bagh': [1242, 861], 'Kalindi Kunj': [1275, 828], 'Okhla Bird Sanctuary': [1308, 794], 'Nangli': [160, 660], 'Najafgarh': [120, 660], 'Narela (Phase 4 - Proposed)': [120, 60], 'Yashobhoomi Dwarka Sector 25': [60, 800], 'Noida Sector 51': [1480, 860], 'Noida Sector 50': [1486, 886], 'Noida Sector 76': [1492, 912], 'Noida Sector 101': [1498, 938], 'Noida Sector 81': [1504, 964], 'NSEZ': [1510, 990], 'Noida Sector 83': [1516, 1016], 'Noida Sector 137': [1522, 1042], 'Noida Sector 142': [1528, 1068], 'Noida Sector 143': [1534, 1094], 'Noida Sector 144': [1540, 1120], 'Noida Sector 145': [1546, 1146], 'Noida Sector 146': [1552, 1172], 'Noida Sector 147': [1558, 1198], 'Noida Sector 148': [1564, 1224], 'Knowledge Park II': [1570, 1250], 'Pari Chowk': [1576, 1276], 'Alpha 1': [1582, 1302], 'Delta 1': [1588, 1328], 'GNIDA Office': [1594, 1354], 'Depot': [1600, 1380], 'Phase 2': [740, 1220], 'Belvedere Towers': [700, 1200], 'Cyber City': [660, 1200], 'Moulsari Avenue': [660, 1240], 'Phase 3': [700, 1260], 'Phase 1': [740, 1260], 'Sector 42-43': [840, 1280], 'Sector 53-54': [880, 1300], 'Sector 54 Chowk': [920, 1320], 'Sector 55-56': [960, 1340], 'Prashant Vihar': [480, 240], 'Deepali Chowk': [360, 280], 'Pushpanjali': [420, 260], 'Krishna Park Extension': [310, 620]}



# Comprehensive Station Aliases (including DMRC official portal variations, historic names, Hindi transliterations)
STATION_ALIASES = {
    'Shaheed Sthal(New Bus Adda)': 'Shaheed Sthal (New Bus Adda)',
    'Shaheed Sthal': 'Shaheed Sthal (New Bus Adda)',
    'New Bus Adda': 'Shaheed Sthal (New Bus Adda)',
    'Shyam park': 'Shyam Park',
    'Major Mohit Sharma': 'Major Mohit Sharma Rajendra Nagar',
    'Rajendra Nagar': 'Major Mohit Sharma Rajendra Nagar',
    'Jhil Mil': 'Jhilmil',
    'Netaji Subash Place': 'Netaji Subhash Place',
    'Pitam Pura': 'Pitampura',
    'Rohini Sector 18-19': 'Rohini Sector 18',
    'Guru Tegh Bahadur Nagar': 'GTB Nagar',
    'Jorbagh': 'Jor Bagh',
    'Qutab Minar': 'Qutub Minar',
    'Chhattarpur': 'Chhatarpur',
    'Huda City Centre': 'Millennium City Centre',
    'HUDA City Centre': 'Millennium City Centre',
    'Millennium City Centre Gurugram': 'Millennium City Centre',
    'Janak Puri West': 'Janakpuri West',
    'Janak Puri East': 'Janakpuri East',
    'R K Ashram Marg': 'RK Ashram Marg',
    'Barakhamba': 'Barakhamba Road',
    'Supreme Court (Pragati Maidan)': 'Supreme Court',
    'Pragati Maidan': 'Supreme Court',
    'Mayur Vihar Phase-1': 'Mayur Vihar-I',
    'Mayur Vihar Extention': 'Mayur Vihar Extension',
    'Noida City Center': 'Noida City Centre',
    'Noida Sector 34': 'Sector 34',
    'Noida Sector 52': 'Sector 52',
    'Noida Sector 61': 'Sector 61',
    'Noida Sector 59': 'Sector 59',
    'Noida Sector 62': 'Sector 62',
    'New Delhi-Airport Express': 'New Delhi',
    'Punjabi Bagh': 'Punjabi Bagh West',
    'Paschim Vihar (East)': 'Paschim Vihar East',
    'Paschim Vihar (West)': 'Paschim Vihar West',
    'Peera Garhi': 'Peeragarhi',
    'Mundka Industrial Area (MIA)': 'Mundka Industrial Area',
    'Ghevra Metro station': 'Ghevra',
    'Bahdurgarh City': 'Bahadurgarh City',
    'Sector 55-66 (Rapid Metro)': 'Sector 55-56',
    'Sector 55-56 (Rapid Metro)': 'Sector 55-56',
    'Sector 54 Chowk (Rapid Metro)': 'Sector 54 Chowk',
    'Sector 53-54 (Rapid Metro)': 'Sector 53-54',
    'Sector 42-43 (Rapid Metro)': 'Sector 42-43',
    'DLF Phase 1 (Rapid Metro)': 'Phase 1',
    'DLF Phase 1': 'Phase 1',
    'Sikandarpur (Rapid Metro)': 'Sikandarpur',
    'DLF Phase 2 (Rapid Metro)': 'Phase 2',
    'DLF Phase 2': 'Phase 2',
    'Belvedere Towers (Rapid Metro)': 'Belvedere Towers',
    'Cyber City (Rapid Metro)': 'Cyber City',
    'Moulsari Avenue (Rapid Metro)': 'Moulsari Avenue',
    'DLF Phase 3 (Rapid Metro)': 'Phase 3',
    'DLF Phase 3': 'Phase 3',
    'Lal Quila': 'Lal Qila',
    'Jawaharlal Nehru Stadium': 'JLN Stadium',
    'Okhla': 'Harkesh Nagar Okhla',
    'Jasola': 'Jasola Apollo',
    'Tughlaqabad': 'Tughlakabad',
    'N.H.P.C. Chowk': 'NHPC Chowk',
    'Sector 28 Faridabad': 'Sector 28',
    'Badkal Mor': 'Badkhal Mor',
    'Old Faridabad': 'Faridabad Old',
    'Sant Surdas - Sihi': 'Sant Surdas (Sihi)',
    'Raja Nahar Singh': 'Raja Nahar Singh (Ballabhgarh)',
    'Dabri Mor - Janakpuri South': 'Dabri Mor–Janakpuri South',
    'Sadar Bazaar Cantonment': 'Sadar Bazar Cantonment',
    'RK Puram': 'R.K. Puram',
    'JAMIA MILLIA ISLAMIA': 'Jamia Millia Islamia',
    'ESI BASAI DARAPUR': 'ESI Basaidarapur',
    'Maya Puri': 'Mayapuri',
    'Sir Vishweshwaraiah Moti Bagh': 'Sir M. Vishweshwaraiah Moti Bagh',
    'Sarai Kale Khan Hazrat Nizamuddin': 'Sarai Kale Khan Nizamuddin',
    'Sarai Kale Khan': 'Sarai Kale Khan Nizamuddin',
    'Hazrat Nizamuddin': 'Sarai Kale Khan Nizamuddin',
    'Mayur Vihar Pocket I': 'Mayur Vihar Pocket 1',
    'Vinod Nagar East': 'East Vinod Nagar–Mayur Vihar-II',
    'Mandawali - West Vinod Nagar': 'Mandawali–West Vinod Nagar',
    'Karkar Duma': 'Karkarduma',
    'Maujpur': 'Maujpur-Babarpur',
    'NSEZ Noida': 'NSEZ',
    'Pari Chowk Greater Noida': 'Pari Chowk',
    'Alpha 1 Greater Noida': 'Alpha 1',
    'Delta 1 Greater Noida': 'Delta 1',
    'Depot Greater Noida': 'Depot',
}

# Display labels mapping for selectbox options: Canonical Name -> Display Label
DISPLAY_LABELS = {
    'Millennium City Centre': 'Millennium City Centre (HUDA City Centre)',
    'Supreme Court': 'Supreme Court (Pragati Maidan)',
    'GTB Nagar': 'GTB Nagar (Guru Tegh Bahadur Nagar)',
    'Sector 52': 'Noida Sector 52',
    'Sector 34': 'Noida Sector 34',
    'Sector 61': 'Noida Sector 61',
    'Sector 59': 'Noida Sector 59',
    'Sector 62': 'Noida Sector 62',
    'Faridabad Old': 'Faridabad Old (Old Faridabad)',
    'JLN Stadium': 'JLN Stadium (Jawaharlal Nehru Stadium)',
    'Lal Qila': 'Lal Qila (Red Fort)',
    'Sarai Kale Khan Nizamuddin': 'Sarai Kale Khan (Hazrat Nizamuddin)',
    'Shaheed Sthal (New Bus Adda)': 'Shaheed Sthal (New Bus Adda)',
    'Netaji Subhash Place': 'Netaji Subhash Place (NSP)',
    'Pitampura': 'Pitampura (Pitam Pura)',
    'Jhilmil': 'Jhilmil (Jhil Mil)',
    'Rohini Sector 18': 'Rohini Sector 18-19',
    'Qutub Minar': 'Qutub Minar (Qutab Minar)',
    'Chhatarpur': 'Chhatarpur (Chhattarpur)',
    'Pari Chowk': 'Pari Chowk (Greater Noida)',
    'Alpha 1': 'Alpha 1 (Greater Noida)',
    'Delta 1': 'Delta 1 (Greater Noida)',
    'Depot': 'Depot (Greater Noida)',
    'NSEZ': 'NSEZ (Noida Special Economic Zone)',
    'Sector 55-56': 'Sector 55-56 (Rapid Metro Gurugram)',
    'Sector 54 Chowk': 'Sector 54 Chowk (Rapid Metro)',
    'Sector 53-54': 'Sector 53-54 (Rapid Metro)',
    'Sector 42-43': 'Sector 42-43 (Rapid Metro)',
    'Phase 1': 'DLF Phase 1 (Rapid Metro)',
    'Phase 2': 'DLF Phase 2 (Rapid Metro)',
    'Phase 3': 'DLF Phase 3 (Rapid Metro)',
    'Cyber City': 'Cyber City (Rapid Metro)',
    'Belvedere Towers': 'Belvedere Towers (Rapid Metro)',
    'Moulsari Avenue': 'Moulsari Avenue (Rapid Metro)',
    'Mayur Vihar-I': 'Mayur Vihar Phase-1',
    'Mayur Vihar Extension': 'Mayur Vihar Extension',
    'Mayur Vihar Pocket 1': 'Mayur Vihar Pocket 1',
    'East Vinod Nagar–Mayur Vihar-II': 'East Vinod Nagar (Mayur Vihar-II)',
    'Mandawali–West Vinod Nagar': 'Mandawali - West Vinod Nagar',
    'Maujpur-Babarpur': 'Maujpur-Babarpur',
    'Dabri Mor–Janakpuri South': 'Dabri Mor - Janakpuri South',
    'Sadar Bazar Cantonment': 'Sadar Bazar Cantonment',
    'R.K. Puram': 'R.K. Puram (RK Puram)',
    'Jamia Millia Islamia': 'Jamia Millia Islamia',
    'ESI Basaidarapur': 'ESI Basaidarapur',
    'Mayapuri': 'Mayapuri (Maya Puri)',
    'Karkarduma': 'Karkarduma (Karkar Duma)',
    'Sant Surdas (Sihi)': 'Sant Surdas - Sihi',
    'Raja Nahar Singh (Ballabhgarh)': 'Raja Nahar Singh (Ballabhgarh)',
    'Harkesh Nagar Okhla': 'Harkesh Nagar Okhla',
    'Jasola Apollo': 'Jasola Apollo',
    'Tughlakabad': 'Tughlakabad (Tughlaqabad)',
    'Badkhal Mor': 'Badkhal Mor (Badkal Mor)',
    'NHPC Chowk': 'NHPC Chowk (N.H.P.C. Chowk)',
    'Sector 28': 'Sector 28 Faridabad',
    'Prashant Vihar': 'Prashant Vihar (Rohini Sector 14)',
    'Shalimar Bagh': 'Shalimar Bagh',
}


# Realistic Interchange Walking Distances & Platform Walk Times (meters & minutes)
INTERCHANGE_WALK_DATA = {
    'Rajiv Chowk': {
        'distance_m': 180,
        'walk_min': 3.0,
        'description': 'Underground concourse & escalators (Yellow ⇄ Blue platform)'
    },
    'Kashmere Gate': {
        'distance_m': 280,
        'walk_min': 4.5,
        'description': '3-level mega hub (Red ⇄ Yellow ⇄ Violet platforms)'
    },
    'Hauz Khas': {
        'distance_m': 320,
        'walk_min': 5.0,
        'description': 'Deep underground escalators (Yellow ⇄ Magenta platform)'
    },
    'Botanical Garden': {
        'distance_m': 160,
        'walk_min': 2.5,
        'description': 'Elevated viaduct link (Blue ⇄ Magenta platform)'
    },
    'Netaji Subhash Place': {
        'distance_m': 190,
        'walk_min': 3.0,
        'description': 'Pedestrian subway connection (Red ⇄ Pink platform)'
    },
    'Central Secretariat': {
        'distance_m': 110,
        'walk_min': 1.5,
        'description': 'Cross-platform island transfer (Yellow ⇄ Violet)'
    },
    'Mandi House': {
        'distance_m': 120,
        'walk_min': 2.0,
        'description': 'Direct subway passenger corridor (Blue ⇄ Violet platform)'
    },
    'Dilli Haat INA': {
        'distance_m': 140,
        'walk_min': 2.0,
        'description': 'Concourse interchange corridor (Yellow ⇄ Pink platform)'
    },
    'Lajpat Nagar': {
        'distance_m': 175,
        'walk_min': 2.5,
        'description': 'Integrated concourse walkway (Pink ⇄ Violet platform)'
    },
    'Anand Vihar': {
        'distance_m': 210,
        'walk_min': 3.5,
        'description': 'Foot over-bridge connecting elevated & underground platforms'
    },
    'Kirti Nagar': {
        'distance_m': 150,
        'walk_min': 2.5,
        'description': 'Ramped connector between Blue & Green branch'
    },
    'Inderlok': {
        'distance_m': 170,
        'walk_min': 2.5,
        'description': 'Elevated transition bridge (Red ⇄ Green platform)'
    },
    'Sector 52': {
        'distance_m': 300,
        'walk_min': 5.0,
        'description': 'Dedicated pathway to Noida Sector 51 (Aqua Line)'
    },
    'Noida Sector 51': {
        'distance_m': 300,
        'walk_min': 5.0,
        'description': 'Dedicated pathway to Sector 52 (Blue Line)'
    },
    'Dwarka Sector 21': {
        'distance_m': 140,
        'walk_min': 2.0,
        'description': 'Direct underground ramp (Blue ⇄ Airport Express)'
    },
    'Welcome': {
        'distance_m': 160,
        'walk_min': 2.5,
        'description': 'Concourse level link between Red & Pink Line'
    },
    'Yamuna Bank': {
        'distance_m': 70,
        'walk_min': 1.0,
        'description': 'Cross-platform island interchange (Blue Main ⇄ Branch)'
    },
    'Mayur Vihar-I': {
        'distance_m': 150,
        'walk_min': 2.5,
        'description': 'Elevated transfer bridge (Blue ⇄ Pink platform)'
    },
    'Azadpur': {
        'distance_m': 180,
        'walk_min': 3.0,
        'description': 'Connecting tunnel walkway (Yellow ⇄ Pink platform)'
    },
    'Rajouri Garden': {
        'distance_m': 160,
        'walk_min': 2.5,
        'description': 'Footbridge between elevated Blue & Pink platforms'
    },
    'Sikandarpur': {
        'distance_m': 190,
        'walk_min': 3.0,
        'description': 'Skywalk connecting Yellow Line to Rapid Metro'
    },
    'New Delhi': {
        'distance_m': 220,
        'walk_min': 3.5,
        'description': 'Underground concourse between Yellow Line & Airport Express'
    },
    'Kalkaji Mandir': {
        'distance_m': 170,
        'walk_min': 2.5,
        'description': 'Direct skywalk between Violet & Magenta platform'
    },
    'Janakpuri West': {
        'distance_m': 210,
        'walk_min': 3.5,
        'description': 'Longest escalator in India connecting Blue & Magenta Line'
    }
}


class MetroGraph:
    """
    Represents the metro network as an unweighted, undirected graph.
    Vertices (nodes) = Metro stations
    Edges = Direct rail tracks connecting adjacent stations
    """

    def __init__(self):
        self.adjacency_list = {}
        self.station_lines = {}
        self.track_segments = []
        self.edge_lines = {}

    def add_station(self, station_name, line_name=None):
        if station_name not in self.adjacency_list:
            self.adjacency_list[station_name] = []
            self.station_lines[station_name] = set()

        if line_name:
            self.station_lines[station_name].add(line_name)

    def add_connection(self, station_a, station_b, line_name=None):
        self.add_station(station_a, line_name)
        self.add_station(station_b, line_name)

        if station_b not in self.adjacency_list[station_a]:
            self.adjacency_list[station_a].append(station_b)
        if station_a not in self.adjacency_list[station_b]:
            self.adjacency_list[station_b].append(station_a)

        key = tuple(sorted([station_a, station_b]))
        if line_name:
            self.edge_lines[key] = line_name
            segment = (station_a, station_b, line_name)
            rev_segment = (station_b, station_a, line_name)
            if segment not in self.track_segments and rev_segment not in self.track_segments:
                self.track_segments.append(segment)

    def get_all_stations(self):
        return sorted(list(self.adjacency_list.keys()))

    def get_station_lines(self, station_name):
        lines = self.station_lines.get(station_name, set())
        return sorted(list(lines)) if lines else ["General Network"]

    def get_edge_line(self, station_a, station_b):
        key = tuple(sorted([station_a, station_b]))
        return self.edge_lines.get(key, "Direct Line")

    
    def resolve_station(self, name):
        """
        Resolves any station name, alias, display label, or historical name
        to the exact canonical node name in the adjacency list.
        """
        if not name or not isinstance(name, str):
            return name
        name_clean = name.strip()
        if name_clean in self.adjacency_list:
            return name_clean

        # Check reverse of DISPLAY_LABELS
        for canon, disp in DISPLAY_LABELS.items():
            if name_clean == disp:
                return canon

        # Check STATION_ALIASES
        if name_clean in STATION_ALIASES:
            return STATION_ALIASES[name_clean]

        # Case and punctuation-insensitive match
        norm = name_clean.lower().replace('-', ' ').replace('–', ' ').replace('  ', ' ')
        for k, v in STATION_ALIASES.items():
            if k.lower().replace('-', ' ').replace('–', ' ').replace('  ', ' ') == norm:
                return v
        for canon, disp in DISPLAY_LABELS.items():
            if disp.lower().replace('-', ' ').replace('–', ' ').replace('  ', ' ') == norm:
                return canon
        for s in self.adjacency_list:
            if s.lower().replace('-', ' ').replace('–', ' ').replace('  ', ' ') == norm:
                return s

        return name_clean

    def get_display_station_list(self):
        """
        Returns a sorted list of user-friendly names that include common aliases
        and former names in parentheses for intuitive selectbox searching.
        """
        display_list = []
        for st in self.get_all_stations():
            label = DISPLAY_LABELS.get(st, st)
            display_list.append(label)
        return sorted(display_list)

    def get_station_display_label(self, station_name):
        canon = self.resolve_station(station_name)
        return DISPLAY_LABELS.get(canon, canon)

    def bfs_shortest_path(self, start_station, destination_station):
        start_station = self.resolve_station(start_station)
        destination_station = self.resolve_station(destination_station)
        if start_station not in self.adjacency_list or destination_station not in self.adjacency_list:
            return None, 0

        if start_station == destination_station:
            return [start_station], 0

        queue = deque([start_station])
        visited = {start_station}
        parent = {start_station: None}

        destination_found = False

        while queue:
            current_station = queue.popleft()

            if current_station == destination_station:
                destination_found = True
                break

            for neighbor in self.adjacency_list.get(current_station, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current_station
                    queue.append(neighbor)

        if not destination_found:
            return None, 0

        path = []
        curr = destination_station
        while curr is not None:
            path.append(curr)
            curr = parent[curr]

        path.reverse()
        total_stops = len(path) - 1

        return path, total_stops

    def get_route_analysis(self, path, departure_time=None):
        """
        Computes detailed journey metrics including:
        - Transfers and line switching details
        - Walking distance to metro tracks (at entry, exit, and interchange hubs)
        - Station dwell delays and train arrival wait times (headway delays)
        - Real-time simulated ETA itinerary for every station on the route
        """
        if not path or len(path) < 2:
            return {
                "transfers": [],
                "legs": [],
                "total_distance_km": 0.0,
                "total_walking_m": 0,
                "train_ride_min": 0,
                "station_dwell_min": 0.0,
                "transfer_walk_min": 0.0,
                "transfer_wait_min": 0.0,
                "origin_wait_min": 0.0,
                "total_time_min": 0,
                "itinerary": []
            }

        import datetime

        if departure_time is None:
            departure_time = datetime.datetime.now()

        legs = []
        transfers = []
        itinerary = []

        total_distance_km = 0.0
        # Walking from station entrance gate/concourse to platform track: ~120m (2 min)
        total_walking_m = 120
        current_time = departure_time + datetime.timedelta(minutes=2.0)

        # Initial train arrival / headway wait at origin platform
        first_leg_line = self.get_edge_line(path[0], path[1])
        initial_wait_min = 2.5 if "Airport" not in first_leg_line else 5.0
        current_time += datetime.timedelta(minutes=initial_wait_min)

        # Record Origin station
        itinerary.append({
            "station": path[0],
            "time_str": current_time.strftime("%I:%M %p"),
            "line": first_leg_line,
            "action": "Origin - Board Train",
            "dwell_sec": 0,
            "track_dist_km": 0.0,
            "walk_m": 120,
            "walk_to_track_m": 120,
            "walk_time_min": 2.0,
            "wait_delay_min": initial_wait_min,
            "is_interchange": False,
            "transfer_info": None
        })

        accumulated_dwell_min = 0.0
        accumulated_ride_min = 0.0
        accumulated_transfer_walk_min = 0.0
        accumulated_transfer_wait_min = 0.0

        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]
            line = self.get_edge_line(u, v)
            legs.append({"from": u, "to": v, "line": line})

            # Calculate inter-station distance and train running time
            if "Airport Express" in line:
                hop_dist = 3.8
                hop_ride_min = 3.2
            elif "Rapid Metro" in line:
                hop_dist = 1.0
                hop_ride_min = 1.8
            else:
                hop_dist = 1.3
                hop_ride_min = 2.1

            total_distance_km += hop_dist
            accumulated_ride_min += hop_ride_min
            current_time += datetime.timedelta(minutes=hop_ride_min)

            is_dest = (i + 1 == len(path) - 1)
            is_transfer = False
            tf_info = None

            if not is_dest:
                next_line = self.get_edge_line(v, path[i + 2])
                if next_line != line:
                    is_transfer = True
                    walk_data = INTERCHANGE_WALK_DATA.get(v, {
                        'distance_m': 150,
                        'walk_min': 2.5,
                        'description': 'Concourse walkway & escalators'
                    })
                    tf_walk_m = walk_data['distance_m']
                    tf_walk_min = walk_data['walk_min']
                    tf_wait_min = 3.0  # Average headway wait delay for connecting train

                    total_walking_m += tf_walk_m
                    accumulated_transfer_walk_min += tf_walk_min
                    accumulated_transfer_wait_min += tf_wait_min

                    tf_info = {
                        "station": v,
                        "from_line": line,
                        "to_line": next_line,
                        "walk_m": tf_walk_m,
                        "walk_min": tf_walk_min,
                        "wait_min": tf_wait_min,
                        "description": walk_data['description']
                    }
                    transfers.append(tf_info)
                    current_time += datetime.timedelta(minutes=(tf_walk_min + tf_wait_min))
                else:
                    # Intermediate station dwell delay (passenger boarding / train stop)
                    dwell_sec = 35
                    accumulated_dwell_min += dwell_sec / 60.0
                    current_time += datetime.timedelta(seconds=dwell_sec)
            else:
                # Destination: Walk from platform track to AFC exit gates (~100m, 1.5 min)
                total_walking_m += 100
                current_time += datetime.timedelta(minutes=1.5)

            itinerary.append({
                "station": v,
                "time_str": current_time.strftime("%I:%M %p"),
                "line": line if not is_transfer else next_line,
                "action": "Destination - Alight & Exit" if is_dest else ("Interchange Transfer" if is_transfer else "Station Stop"),
                "dwell_sec": 0 if (is_dest or is_transfer) else 35,
                "track_dist_km": round(hop_dist, 1),
                "walk_m": 100 if is_dest else (tf_info["walk_m"] if is_transfer else 0),
                "walk_min": 1.5 if is_dest else (tf_info["walk_min"] if is_transfer else 0.0),
                "wait_min": tf_info["wait_min"] if is_transfer else 0.0,
                "is_interchange": is_transfer,
                "transfer_info": tf_info
            })

        total_time_min = round(
            2.0 + initial_wait_min + accumulated_ride_min + accumulated_dwell_min
            + accumulated_transfer_walk_min + accumulated_transfer_wait_min + 1.5
        )

        return {
            "transfers": transfers,
            "legs": legs,
            "total_distance_km": round(total_distance_km, 1),
            "total_walking_m": total_walking_m,
            "train_ride_min": round(accumulated_ride_min),
            "station_dwell_min": round(accumulated_dwell_min, 1),
            "transfer_walk_min": round(accumulated_transfer_walk_min, 1),
            "transfer_wait_min": round(accumulated_transfer_wait_min, 1),
            "origin_wait_min": round(initial_wait_min, 1),
            "total_time_min": total_time_min,
            "itinerary": itinerary
        }


def build_sample_metro_network():
    metro = MetroGraph()

    # 1. Red Line (29 stations)
    red = [
        'Rithala', 'Rohini West', 'Rohini East', 'Pitampura', 'Kohat Enclave',
        'Netaji Subhash Place', 'Keshav Puram', 'Kanhaiya Nagar', 'Inderlok',
        'Shastri Nagar', 'Pratap Nagar', 'Pul Bangash', 'Tis Hazari',
        'Kashmere Gate', 'Shastri Park', 'Seelampur', 'Welcome', 'Shahdara',
        'Mansarovar Park', 'Jhilmil', 'Dilshad Garden', 'Shaheed Nagar',
        'Raj Bagh', 'Major Mohit Sharma Rajendra Nagar', 'Shyam Park',
        'Mohan Nagar', 'Arthala', 'Hindon River', 'Shaheed Sthal (New Bus Adda)'
    ]
    for i in range(len(red) - 1):
        metro.add_connection(red[i], red[i + 1], "Red Line")

    # 2. Yellow Line (37 stations)
    yellow = [
        'Samaypur Badli', 'Rohini Sector 18', 'Haiderpur Badli Mor', 'Jahangirpuri',
        'Adarsh Nagar', 'Azadpur', 'Model Town', 'GTB Nagar', 'Vishwavidyalaya',
        'Vidhan Sabha', 'Civil Lines', 'Kashmere Gate', 'Chandni Chowk', 'Chawri Bazar',
        'New Delhi', 'Rajiv Chowk', 'Patel Chowk', 'Central Secretariat',
        'Udyog Bhawan', 'Lok Kalyan Marg', 'Jor Bagh', 'Dilli Haat INA', 'AIIMS',
        'Green Park', 'Hauz Khas', 'Malviya Nagar', 'Saket', 'Qutub Minar',
        'Chhatarpur', 'Sultanpur', 'Ghitorni', 'Arjan Garh', 'Guru Dronacharya',
        'Sikandarpur', 'MG Road', 'IFFCO Chowk', 'Millennium City Centre'
    ]
    for i in range(len(yellow) - 1):
        metro.add_connection(yellow[i], yellow[i + 1], "Yellow Line")

    # 3. Blue Line Main (50 stations)
    blue_main = [
        'Dwarka Sector 21', 'Dwarka Sector 8', 'Dwarka Sector 9', 'Dwarka Sector 10',
        'Dwarka Sector 11', 'Dwarka Sector 12', 'Dwarka Sector 13', 'Dwarka Sector 14',
        'Dwarka', 'Dwarka Mor', 'Nawada', 'Uttam Nagar West', 'Uttam Nagar East',
        'Janakpuri West', 'Janakpuri East', 'Tilak Nagar', 'Subhash Nagar', 'Tagore Garden',
        'Rajouri Garden', 'Ramesh Nagar', 'Moti Nagar', 'Kirti Nagar', 'Shadipur',
        'Patel Nagar', 'Rajendra Place', 'Karol Bagh', 'Jhandewalan', 'RK Ashram Marg',
        'Rajiv Chowk', 'Barakhamba Road', 'Mandi House', 'Supreme Court', 'Indraprastha',
        'Yamuna Bank', 'Akshardham', 'Mayur Vihar-I', 'Mayur Vihar Extension',
        'New Ashok Nagar', 'Noida Sector 15', 'Noida Sector 16', 'Noida Sector 18',
        'Botanical Garden', 'Golf Course', 'Noida City Centre', 'Sector 34',
        'Sector 52', 'Sector 61', 'Sector 59', 'Sector 62', 'Noida Electronic City'
    ]
    for i in range(len(blue_main) - 1):
        metro.add_connection(blue_main[i], blue_main[i + 1], "Blue Line")

    # 4. Blue Line Branch (Yamuna Bank to Vaishali) (8 stations)
    blue_branch = [
        'Yamuna Bank', 'Laxmi Nagar', 'Nirman Vihar', 'Preet Vihar',
        'Karkarduma', 'Anand Vihar', 'Kaushambi', 'Vaishali'
    ]
    for i in range(len(blue_branch) - 1):
        metro.add_connection(blue_branch[i], blue_branch[i + 1], "Blue Line Branch")

    # 5. Green Line (21 stations main + branch + interchange)
    green = [
        'Inderlok', 'Ashok Park Main', 'Punjabi Bagh East', 'Punjabi Bagh West',
        'Shivaji Park', 'Madipur', 'Paschim Vihar East', 'Paschim Vihar West',
        'Peeragarhi', 'Udyog Nagar', 'Maharaja Surajmal Stadium', 'Nangloi',
        'Nangloi Railway Station', 'Rajdhani Park', 'Mundka',
        'Mundka Industrial Area', 'Ghevra', 'Tikri Kalan', 'Tikri Border',
        'Pandit Shree Ram Sharma', 'Bahadurgarh City', 'Brigadier Hoshiar Singh'
    ]
    for i in range(len(green) - 1):
        metro.add_connection(green[i], green[i + 1], "Green Line")

    green_branch = ['Ashok Park Main', 'Satguru Ram Singh Marg', 'Kirti Nagar']
    for i in range(len(green_branch) - 1):
        metro.add_connection(green_branch[i], green_branch[i + 1], "Green Line")

    # 6. Violet Line (34 stations)
    violet = [
        'Kashmere Gate', 'Lal Qila', 'Jama Masjid', 'Delhi Gate', 'ITO',
        'Mandi House', 'Janpath', 'Central Secretariat', 'Khan Market',
        'JLN Stadium', 'Jangpura', 'Lajpat Nagar', 'Moolchand', 'Kailash Colony',
        'Nehru Place', 'Kalkaji Mandir', 'Govind Puri', 'Harkesh Nagar Okhla',
        'Jasola Apollo', 'Sarita Vihar', 'Mohan Estate', 'Tughlakabad',
        'Badarpur Border', 'Sarai', 'NHPC Chowk', 'Mewala Maharajpur',
        'Sector 28', 'Badkhal Mor', 'Faridabad Old', 'Neelam Chowk Ajronda',
        'Bata Chowk', 'Escorts Mujesar', 'Sant Surdas (Sihi)',
        'Raja Nahar Singh (Ballabhgarh)'
    ]
    for i in range(len(violet) - 1):
        metro.add_connection(violet[i], violet[i + 1], "Violet Line")

    # 7. Pink Line (Ring Line) (38 stations)
    pink = [
        'Majlis Park', 'Azadpur', 'Shalimar Bagh', 'Netaji Subhash Place',
        'Shakurpur', 'Punjabi Bagh West', 'ESI Basaidarapur', 'Rajouri Garden',
        'Mayapuri', 'Naraina Vihar', 'Delhi Cantt', 'Durgabai Deshmukh South Campus',
        'Sir M. Vishweshwaraiah Moti Bagh', 'Bhikaji Cama Place', 'Sarojini Nagar',
        'Dilli Haat INA', 'South Extension', 'Lajpat Nagar', 'Vinobapuri', 'Ashram',
        'Sarai Kale Khan Nizamuddin', 'Mayur Vihar-I', 'Mayur Vihar Pocket 1',
        'Trilokpuri Sanjay Lake', 'East Vinod Nagar–Mayur Vihar-II',
        'Mandawali–West Vinod Nagar', 'IP Extension', 'Anand Vihar',
        'Karkarduma', 'Karkarduma Court', 'Krishna Nagar', 'East Azad Nagar',
        'Welcome', 'Jaffrabad', 'Maujpur-Babarpur', 'Bhajanpura', 'Gokulpuri',
        'Johri Enclave', 'Shiv Vihar'
    ]
    for i in range(len(pink) - 1):
        metro.add_connection(pink[i], pink[i + 1], "Pink Line")

    # 8. Magenta Line (including Phase 4 Krishna Park Ext and Prashant Vihar extension)
    magenta = [
        'Krishna Park Extension',
        'Janakpuri West', 'Dabri Mor–Janakpuri South', 'Dashrath Puri', 'Palam',
        'Sadar Bazar Cantonment', 'Terminal 1 IGI Airport', 'Shankar Vihar',
        'Vasant Vihar', 'Munirka', 'R.K. Puram', 'IIT Delhi', 'Hauz Khas',
        'Panchsheel Park', 'Chirag Delhi', 'Greater Kailash', 'Nehru Enclave',
        'Kalkaji Mandir', 'Okhla NSIC', 'Sukhdev Vihar', 'Jamia Millia Islamia',
        'Okhla Vihar', 'Jasola Vihar Shaheen Bagh', 'Kalindi Kunj',
        'Okhla Bird Sanctuary', 'Botanical Garden'
    ]
    for i in range(len(magenta) - 1):
        metro.add_connection(magenta[i], magenta[i + 1], "Magenta Line")

    # Magenta Line Phase 4 Corridor: Pitampura - Prashant Vihar - Haiderpur Badli Mor
    phase4_ext = ['Deepali Chowk', 'Pushpanjali', 'Pitampura', 'Prashant Vihar', 'Haiderpur Badli Mor']
    for i in range(len(phase4_ext) - 1):
        metro.add_connection(phase4_ext[i], phase4_ext[i + 1], "Magenta Line")

    # 9. Grey Line (4 stations)
    grey = ['Dwarka', 'Nangli', 'Najafgarh', 'Dhansa Bus Stand']
    for i in range(len(grey) - 1):
        metro.add_connection(grey[i], grey[i + 1], "Grey Line")

    # 10. Airport Express Line (7 stations)
    airport = [
        'New Delhi', 'Shivaji Stadium', 'Dhaula Kuan', 'Delhi Aerocity',
        'IGI Airport', 'Dwarka Sector 21', 'Yashobhoomi Dwarka Sector 25'
    ]
    for i in range(len(airport) - 1):
        metro.add_connection(airport[i], airport[i + 1], "Airport Express")

    # 11. Aqua Line (Noida Metro) (21 stations)
    aqua = [
        'Noida Sector 51', 'Noida Sector 50', 'Noida Sector 76', 'Noida Sector 101',
        'Noida Sector 81', 'NSEZ', 'Noida Sector 83', 'Noida Sector 137',
        'Noida Sector 142', 'Noida Sector 143', 'Noida Sector 144', 'Noida Sector 145',
        'Noida Sector 146', 'Noida Sector 147', 'Noida Sector 148', 'Knowledge Park II',
        'Pari Chowk', 'Alpha 1', 'Delta 1', 'GNIDA Office', 'Depot'
    ]
    for i in range(len(aqua) - 1):
        metro.add_connection(aqua[i], aqua[i + 1], "Aqua Line (Noida)")
    # Interchange Walkway between Blue Line Sector 52 and Aqua Line Noida Sector 51
    metro.add_connection('Sector 52', 'Noida Sector 51', "Walkway Interchange")

    # 12. Rapid Metro Gurugram (11 stations)
    # Loop
    rapid_loop = ['Sikandarpur', 'Phase 2', 'Belvedere Towers', 'Cyber City', 'Moulsari Avenue', 'Phase 3', 'Phase 1', 'Sikandarpur']
    for i in range(len(rapid_loop) - 1):
        metro.add_connection(rapid_loop[i], rapid_loop[i + 1], "Rapid Metro Gurugram")
    # Golf Course Road branch
    rapid_ext = ['Sikandarpur', 'Sector 42-43', 'Sector 53-54', 'Sector 54 Chowk', 'Sector 55-56']
    for i in range(len(rapid_ext) - 1):
        metro.add_connection(rapid_ext[i], rapid_ext[i + 1], "Rapid Metro Gurugram")

    # 13. Disconnected Station
    metro.add_station("Narela (Phase 4 - Proposed)", "Proposed Line")

    return metro
