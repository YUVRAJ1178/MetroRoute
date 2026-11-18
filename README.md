# 🚇 MetroRoute – Official Comprehensive Delhi-NCR Metro Network (264 Stations)

A complete, high-performance Data Structures and Algorithms (DSA) mini-project built for summer internship evaluation.

MetroRoute models the **entire Delhi-NCR transit network covering 264 stations across 12 lines (including Delhi Metro, Noida Metro Aqua Line, and Rapid Metro Gurugram)** as an **unweighted graph** using an **Adjacency List**. It implements a manual **Breadth-First Search (BFS)** algorithm to compute the shortest journey (minimum stops) between any two stations across Delhi, Noida, Greater Noida, Ghaziabad, Faridabad, Bahadurgarh, and Gurugram.

---

## 1. Network Scope (264 Stations Across 12 Lines)

1. 🔴 **Red Line (29 Stations)**: Rithala ↔ Rohini West ↔ Rohini East ↔ Pitampura ↔ Kohat Enclave ↔ Netaji Subhash Place ↔ Keshav Puram ↔ Kanhaiya Nagar ↔ Inderlok ↔ Shastri Nagar ↔ Pratap Nagar ↔ Pul Bangash ↔ Tis Hazari ↔ Kashmere Gate ↔ Shastri Park ↔ Seelampur ↔ Welcome ↔ Shahdara ↔ Mansarovar Park ↔ Jhilmil ↔ Dilshad Garden ↔ Shaheed Nagar ↔ Raj Bagh ↔ Major Mohit Sharma Rajendra Nagar ↔ Shyam Park ↔ Mohan Nagar ↔ Arthala ↔ Hindon River ↔ Shaheed Sthal (New Bus Adda)
2. 🟡 **Yellow Line (37 Stations)**: Samaypur Badli ↔ Rohini Sector 18 ↔ Haiderpur Badli Mor ↔ Jahangirpuri ↔ Adarsh Nagar ↔ Azadpur ↔ Model Town ↔ GTB Nagar ↔ Vishwavidyalaya ↔ Vidhan Sabha ↔ Civil Lines ↔ Kashmere Gate ↔ Chandni Chowk ↔ Chawri Bazar ↔ New Delhi ↔ Rajiv Chowk ↔ Patel Chowk ↔ Central Secretariat ↔ Udyog Bhawan ↔ Lok Kalyan Marg ↔ Jor Bagh ↔ Dilli Haat INA ↔ AIIMS ↔ Green Park ↔ Hauz Khas ↔ Malviya Nagar ↔ Saket ↔ Qutub Minar ↔ Chhatarpur ↔ Sultanpur ↔ Ghitorni ↔ Arjan Garh ↔ Guru Dronacharya ↔ Sikandarpur ↔ MG Road ↔ IFFCO Chowk ↔ Millennium City Centre
3. 🔵 **Blue Line Main (50 Stations)**: Dwarka Sector 21 ↔ Dwarka Sector 8 ↔ Dwarka Sector 9 ↔ Dwarka Sector 10 ↔ Dwarka Sector 11 ↔ Dwarka Sector 12 ↔ Dwarka Sector 13 ↔ Dwarka Sector 14 ↔ Dwarka ↔ Dwarka Mor ↔ Nawada ↔ Uttam Nagar West ↔ Uttam Nagar East ↔ Janakpuri West ↔ Janakpuri East ↔ Tilak Nagar ↔ Subhash Nagar ↔ Tagore Garden ↔ Rajouri Garden ↔ Ramesh Nagar ↔ Moti Nagar ↔ Kirti Nagar ↔ Shadipur ↔ Patel Nagar ↔ Rajendra Place ↔ Karol Bagh ↔ Jhandewalan ↔ RK Ashram Marg ↔ Rajiv Chowk ↔ Barakhamba Road ↔ Mandi House ↔ Supreme Court ↔ Indraprastha ↔ Yamuna Bank ↔ Akshardham ↔ Mayur Vihar-I ↔ Mayur Vihar Extension ↔ New Ashok Nagar ↔ Noida Sector 15 ↔ Noida Sector 16 ↔ Noida Sector 18 ↔ Botanical Garden ↔ Golf Course ↔ Noida City Centre ↔ Sector 34 ↔ Sector 52 ↔ Sector 61 ↔ Sector 59 ↔ Sector 62 ↔ Noida Electronic City
4. 🔵 **Blue Line Branch (8 Stations)**: Yamuna Bank ↔ Laxmi Nagar ↔ Nirman Vihar ↔ Preet Vihar ↔ Karkarduma ↔ Anand Vihar ↔ Kaushambi ↔ Vaishali
5. 🟢 **Green Line & Branch (23 Stations)**: Inderlok / Kirti Nagar ↔ Ashok Park Main ↔ Punjabi Bagh East ↔ Punjabi Bagh West (Interchange) ↔ Shivaji Park ↔ Madipur ↔ Paschim Vihar East ↔ Paschim Vihar West ↔ Peeragarhi ↔ Udyog Nagar ↔ Maharaja Surajmal Stadium ↔ Nangloi ↔ Nangloi Railway Station ↔ Rajdhani Park ↔ Mundka ↔ Mundka Industrial Area ↔ Ghevra ↔ Tikri Kalan ↔ Tikri Border ↔ Pandit Shree Ram Sharma ↔ Bahadurgarh City ↔ Brigadier Hoshiar Singh
6. 🟣 **Violet Line (34 Stations)**: Kashmere Gate ↔ Lal Qila ↔ Jama Masjid ↔ Delhi Gate ↔ ITO ↔ Mandi House ↔ Janpath ↔ Central Secretariat ↔ Khan Market ↔ JLN Stadium ↔ Jangpura ↔ Lajpat Nagar ↔ Moolchand ↔ Kailash Colony ↔ Nehru Place ↔ Kalkaji Mandir ↔ Govind Puri ↔ Harkesh Nagar Okhla ↔ Jasola Apollo ↔ Sarita Vihar ↔ Mohan Estate ↔ Tughlakabad ↔ Badarpur Border ↔ Sarai ↔ NHPC Chowk ↔ Mewala Maharajpur ↔ Sector 28 ↔ Badkhal Mor ↔ Faridabad Old ↔ Neelam Chowk Ajronda ↔ Bata Chowk ↔ Escorts Mujesar ↔ Sant Surdas (Sihi) ↔ Raja Nahar Singh (Ballabhgarh)
7. 🌸 **Pink Line Ring Line (38 Stations)**: Majlis Park ↔ Azadpur ↔ Shalimar Bagh ↔ Netaji Subhash Place ↔ Shakurpur ↔ Punjabi Bagh West ↔ ESI Basaidarapur ↔ Rajouri Garden ↔ Mayapuri ↔ Naraina Vihar ↔ Delhi Cantt ↔ Durgabai Deshmukh South Campus ↔ Sir M. Vishweshwaraiah Moti Bagh ↔ Bhikaji Cama Place ↔ Sarojini Nagar ↔ Dilli Haat INA ↔ South Extension ↔ Lajpat Nagar ↔ Vinobapuri ↔ Ashram ↔ Sarai Kale Khan Nizamuddin ↔ Mayur Vihar-I ↔ Mayur Vihar Pocket 1 ↔ Trilokpuri Sanjay Lake ↔ East Vinod Nagar–Mayur Vihar-II ↔ Mandawali–West Vinod Nagar ↔ IP Extension ↔ Anand Vihar ↔ Karkarduma ↔ Karkarduma Court ↔ Krishna Nagar ↔ East Azad Nagar ↔ Welcome ↔ Jaffrabad ↔ Maujpur-Babarpur ↔ Bhajanpura ↔ Gokulpuri ↔ Johri Enclave ↔ Shiv Vihar
8. 🌺 **Magenta Line (25 Stations)**: Janakpuri West ↔ Dabri Mor–Janakpuri South ↔ Dashrath Puri ↔ Palam ↔ Sadar Bazar Cantonment ↔ Terminal 1 IGI Airport ↔ Shankar Vihar ↔ Vasant Vihar ↔ Munirka ↔ R.K. Puram ↔ IIT Delhi ↔ Hauz Khas ↔ Panchsheel Park ↔ Chirag Delhi ↔ Greater Kailash ↔ Nehru Enclave ↔ Kalkaji Mandir ↔ Okhla NSIC ↔ Sukhdev Vihar ↔ Jamia Millia Islamia ↔ Okhla Vihar ↔ Jasola Vihar Shaheen Bagh ↔ Kalindi Kunj ↔ Okhla Bird Sanctuary ↔ Botanical Garden
9. ⚪ **Grey Line (4 Stations)**: Dwarka ↔ Nangli ↔ Najafgarh ↔ Dhansa Bus Stand
10. 🟠 **Airport Express Line (7 Stations)**: New Delhi ↔ Shivaji Stadium ↔ Dhaula Kuan ↔ Delhi Aerocity ↔ IGI Airport ↔ Dwarka Sector 21 ↔ Yashobhoomi Dwarka Sector 25
11. 🔷 **Aqua Line Noida Metro (21 Stations)**: Noida Sector 51 (Interchange with Sector 52) ↔ Noida Sector 50 ↔ Noida Sector 76 ↔ Noida Sector 101 ↔ Noida Sector 81 ↔ NSEZ ↔ Noida Sector 83 ↔ Noida Sector 137 ↔ Noida Sector 142 ↔ Noida Sector 143 ↔ Noida Sector 144 ↔ Noida Sector 145 ↔ Noida Sector 146 ↔ Noida Sector 147 ↔ Noida Sector 148 ↔ Knowledge Park II ↔ Pari Chowk ↔ Alpha 1 ↔ Delta 1 ↔ GNIDA Office ↔ Depot
12. 🚅 **Rapid Metro Gurugram (11 Stations)**: Sector 55-56 ↔ Sector 54 Chowk ↔ Sector 53-54 ↔ Sector 42-43 ↔ Phase 1 ↔ Sikanderpur (Interchange with Yellow Line) ↔ Phase 2 ↔ Belvedere Towers ↔ Cyber City ↔ Moulsari Avenue ↔ Phase 3

---

## 2. Algorithm Details (BFS)

- **Graph Model**: Unweighted, undirected adjacency list.
- **Queue Implementation**: `collections.deque` for constant $\mathcal{O}(1)$ push and pop operations.
- **Route Tracking**: `parent` dictionary mapping `child_station -> parent_station` to backtrack and reconstruct the path upon reaching the destination.
- **Time Complexity**: $\mathcal{O}(V + E)$ where $V = 264$ vertices and $E = 279$ edges. Runs in $\approx 0.5\text{ ms}$.
- **Space Complexity**: $\mathcal{O}(V)$ for the visited set, parent dictionary, and queue.

---

## 3. How to Run Locally

```powershell
cd r:\METRO
python -m streamlit run app.py
```

Access at `http://localhost:8501`

OR
'https://metroroute-es38.onrender.com/'
