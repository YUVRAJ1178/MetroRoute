# 🚇 MetroRoute – Delhi-NCR Metro Network (268 Stations) & BFS Shortest Route Finder

A high-performance Data Structures and Algorithms (DSA) mini-project built for 3rd-year BTech CSE evaluation.

MetroRoute models the **entire Delhi-NCR transit network covering 268 stations across 12 lines (including Delhi Metro, Noida Metro Aqua Line, and Rapid Metro Gurugram)** as an **unweighted graph** using an **Adjacency List**. It implements a manual **Breadth-First Search (BFS)** algorithm to compute the shortest journey (minimum stops) between any two stations across Delhi, Noida, Greater Noida, Ghaziabad, Faridabad, Bahadurgarh, and Gurugram.

---

## 🌟 Key Features

1. **Manual BFS Shortest Path Algorithm**:
   - Pure Python data structures (`dict` adjacency list, `collections.deque` FIFO queue, and `parent` dictionary for path reconstruction).
   - Strict rule: **Zero external graph solver libraries** (no NetworkX) — 100% custom DSA logic.

2. **Official Comprehensive Network (268 Stations Across 12 Lines)**:
   - Full DMRC coverage: Red, Yellow, Blue (+ Vaishali branch), Green (+ Kirti Nagar branch), Violet, Pink (Ring Line), Magenta (+ Phase 4 corridor), Grey, Airport Express (+ Yashobhoomi), Aqua Line (Noida Metro), and Rapid Metro Gurugram.
   - Comprehensive **76-alias fuzzy/alias resolver** supporting popular landmarks, alternate spellings, and historic names (e.g. *HUDA City Centre*, *Pragati Maidan*, *GTB Nagar*, *Old Faridabad*, *Lal Quila*, *Prashant Vihar*, *Shalimar Bagh*).

3. **⏱️ Station Delays & Real-Time Train Arrival Scheduling**:
   - **Origin Headway Wait Delay**: Accounts for initial train arrival interval (~2.5 min standard headway; ~5.0 min Airport Express).
   - **Station Dwell Stop Delays**: Adds realistic passenger boarding/alighting delays (~35s intermediate dwell stop delay).
   - **Interchange Train Delay**: Computes average connecting train arrival delays (~3.0 min headway).
   - **Simulated Station ETA Timeline**: Every station in the itinerary displays its real-time clock ETA.

4. **🚶 Walking Distance to Metro Tracks & Platform Interchange Guide**:
   - **Station Entry Walk**: Accounts for walking from station entrance AFC gates to platform tracks (**~120 meters / ~2.0 min**).
   - **Station Exit Walk**: Accounts for walking from platform tracks to AFC exit gates (**~100 meters / ~1.5 min**).
   - **Interchange Walkway Distances**: Real-world platform-to-platform walking distances across 24 major interchange hubs (e.g., Rajiv Chowk: 180m / 3 min, Kashmere Gate: 280m / 4.5 min, Hauz Khas: 320m / 5 min, Botanical Garden: 160m / 2.5 min, Sector 52 ⇄ Noida Sector 51 walkway: 300m / 5 min).
   - **Track Distance**: Computes rail track distance (avg. 1.3 km per hop).

5. **🗺️ Interactive High-Contrast SVG Schematic Map**:
   - Clean white canvas transit map dynamically highlighting the BFS shortest route in electric blue, origin pin in green, destination pin in red, and permanent junction labels.

---

## 1. Network Scope (268 Stations Across 12 Lines)

1. 🔴 **Red Line (29 Stations)**: Rithala ↔ Rohini West ↔ Rohini East ↔ Pitampura ↔ Kohat Enclave ↔ Netaji Subhash Place ↔ Keshav Puram ↔ Kanhaiya Nagar ↔ Inderlok ↔ Shastri Nagar ↔ Pratap Nagar ↔ Pul Bangash ↔ Tis Hazari ↔ Kashmere Gate ↔ Shastri Park ↔ Seelampur ↔ Welcome ↔ Shahdara ↔ Mansarovar Park ↔ Jhilmil ↔ Dilshad Garden ↔ Shaheed Nagar ↔ Raj Bagh ↔ Major Mohit Sharma Rajendra Nagar ↔ Shyam Park ↔ Mohan Nagar ↔ Arthala ↔ Hindon River ↔ Shaheed Sthal (New Bus Adda)
2. 🟡 **Yellow Line (37 Stations)**: Samaypur Badli ↔ Rohini Sector 18 ↔ Haiderpur Badli Mor ↔ Jahangirpuri ↔ Adarsh Nagar ↔ Azadpur ↔ Model Town ↔ GTB Nagar ↔ Vishwavidyalaya ↔ Vidhan Sabha ↔ Civil Lines ↔ Kashmere Gate ↔ Chandni Chowk ↔ Chawri Bazar ↔ New Delhi ↔ Rajiv Chowk ↔ Patel Chowk ↔ Central Secretariat ↔ Udyog Bhawan ↔ Lok Kalyan Marg ↔ Jor Bagh ↔ Dilli Haat INA ↔ AIIMS ↔ Green Park ↔ Hauz Khas ↔ Malviya Nagar ↔ Saket ↔ Qutub Minar ↔ Chhatarpur ↔ Sultanpur ↔ Ghitorni ↔ Arjan Garh ↔ Guru Dronacharya ↔ Sikandarpur ↔ MG Road ↔ IFFCO Chowk ↔ Millennium City Centre (HUDA City Centre)
3. 🔵 **Blue Line Main (50 Stations)**: Dwarka Sector 21 ↔ Dwarka Sector 8 ↔ Dwarka Sector 9 ↔ Dwarka Sector 10 ↔ Dwarka Sector 11 ↔ Dwarka Sector 12 ↔ Dwarka Sector 13 ↔ Dwarka Sector 14 ↔ Dwarka ↔ Dwarka Mor ↔ Nawada ↔ Uttam Nagar West ↔ Uttam Nagar East ↔ Janakpuri West ↔ Janakpuri East ↔ Tilak Nagar ↔ Subhash Nagar ↔ Tagore Garden ↔ Rajouri Garden ↔ Ramesh Nagar ↔ Moti Nagar ↔ Kirti Nagar ↔ Shadipur ↔ Patel Nagar ↔ Rajendra Place ↔ Karol Bagh ↔ Jhandewalan ↔ RK Ashram Marg ↔ Rajiv Chowk ↔ Barakhamba Road ↔ Mandi House ↔ Supreme Court (Pragati Maidan) ↔ Indraprastha ↔ Yamuna Bank ↔ Akshardham ↔ Mayur Vihar-I ↔ Mayur Vihar Extension ↔ New Ashok Nagar ↔ Noida Sector 15 ↔ Noida Sector 16 ↔ Noida Sector 18 ↔ Botanical Garden ↔ Golf Course ↔ Noida City Centre ↔ Noida Sector 34 ↔ Noida Sector 52 ↔ Noida Sector 61 ↔ Noida Sector 59 ↔ Noida Sector 62 ↔ Noida Electronic City
4. 🔵 **Blue Line Branch (8 Stations)**: Yamuna Bank ↔ Laxmi Nagar ↔ Nirman Vihar ↔ Preet Vihar ↔ Karkarduma ↔ Anand Vihar ↔ Kaushambi ↔ Vaishali
5. 🟢 **Green Line & Branch (24 Stations)**: Inderlok / Kirti Nagar ↔ Ashok Park Main ↔ Punjabi Bagh East ↔ Punjabi Bagh West (Interchange) ↔ Shivaji Park ↔ Madipur ↔ Paschim Vihar East ↔ Paschim Vihar West ↔ Peeragarhi ↔ Udyog Nagar ↔ Maharaja Surajmal Stadium ↔ Nangloi ↔ Nangloi Railway Station ↔ Rajdhani Park ↔ Mundka ↔ Mundka Industrial Area ↔ Ghevra ↔ Tikri Kalan ↔ Tikri Border ↔ Pandit Shree Ram Sharma ↔ Bahadurgarh City ↔ Brigadier Hoshiar Singh
6. 🟣 **Violet Line (34 Stations)**: Kashmere Gate ↔ Lal Qila (Red Fort) ↔ Jama Masjid ↔ Delhi Gate ↔ ITO ↔ Mandi House ↔ Janpath ↔ Central Secretariat ↔ Khan Market ↔ JLN Stadium ↔ Jangpura ↔ Lajpat Nagar ↔ Moolchand ↔ Kailash Colony ↔ Nehru Place ↔ Kalkaji Mandir ↔ Govind Puri ↔ Harkesh Nagar Okhla ↔ Jasola Apollo ↔ Sarita Vihar ↔ Mohan Estate ↔ Tughlakabad ↔ Badarpur Border ↔ Sarai ↔ NHPC Chowk ↔ Mewala Maharajpur ↔ Sector 28 ↔ Badkhal Mor ↔ Faridabad Old ↔ Neelam Chowk Ajronda ↔ Bata Chowk ↔ Escorts Mujesar ↔ Sant Surdas (Sihi) ↔ Raja Nahar Singh (Ballabhgarh)
7. 🌸 **Pink Line Ring Line (39 Stations)**: Majlis Park ↔ Azadpur ↔ Shalimar Bagh ↔ Netaji Subhash Place ↔ Shakurpur ↔ Punjabi Bagh West ↔ ESI Basaidarapur ↔ Rajouri Garden ↔ Mayapuri ↔ Naraina Vihar ↔ Delhi Cantt ↔ Durgabai Deshmukh South Campus ↔ Sir M. Vishweshwaraiah Moti Bagh ↔ Bhikaji Cama Place ↔ Sarojini Nagar ↔ Dilli Haat INA ↔ South Extension ↔ Lajpat Nagar ↔ Vinobapuri ↔ Ashram ↔ Sarai Kale Khan Hazrat Nizamuddin ↔ Mayur Vihar-I ↔ Mayur Vihar Pocket 1 ↔ Trilokpuri Sanjay Lake ↔ East Vinod Nagar–Mayur Vihar-II ↔ Mandawali–West Vinod Nagar ↔ IP Extension ↔ Anand Vihar ↔ Karkarduma ↔ Karkarduma Court ↔ Krishna Nagar ↔ East Azad Nagar ↔ Welcome ↔ Jaffrabad ↔ Maujpur-Babarpur ↔ Bhajanpura ↔ Gokulpuri ↔ Johri Enclave ↔ Shiv Vihar
8. 🌺 **Magenta Line & Phase 4 Extension (31 Stations)**: Krishna Park Extension ↔ Janakpuri West ↔ Dabri Mor–Janakpuri South ↔ Dashrath Puri ↔ Palam ↔ Sadar Bazar Cantonment ↔ Terminal 1 IGI Airport ↔ Shankar Vihar ↔ Vasant Vihar ↔ Munirka ↔ R.K. Puram ↔ IIT Delhi ↔ Hauz Khas ↔ Panchsheel Park ↔ Chirag Delhi ↔ Greater Kailash ↔ Nehru Enclave ↔ Kalkaji Mandir ↔ Okhla NSIC ↔ Sukhdev Vihar ↔ Jamia Millia Islamia ↔ Okhla Vihar ↔ Jasola Vihar Shaheen Bagh ↔ Kalindi Kunj ↔ Okhla Bird Sanctuary ↔ Botanical Garden | *Phase 4 Corridor:* Deepali Chowk ↔ Pushpanjali ↔ Pitampura ↔ Prashant Vihar ↔ Haiderpur Badli Mor
9. ⚪ **Grey Line (4 Stations)**: Dwarka ↔ Nangli ↔ Najafgarh ↔ Dhansa Bus Stand
10. 🟠 **Airport Express Line (7 Stations)**: New Delhi ↔ Shivaji Stadium ↔ Dhaula Kuan ↔ Delhi Aerocity ↔ IGI Airport ↔ Dwarka Sector 21 ↔ Yashobhoomi Dwarka Sector 25
11. 🔷 **Aqua Line Noida Metro (21 Stations)**: Noida Sector 51 (Interchange with Sector 52) ↔ Noida Sector 50 ↔ Noida Sector 76 ↔ Noida Sector 101 ↔ Noida Sector 81 ↔ NSEZ ↔ Noida Sector 83 ↔ Noida Sector 137 ↔ Noida Sector 142 ↔ Noida Sector 143 ↔ Noida Sector 144 ↔ Noida Sector 145 ↔ Noida Sector 146 ↔ Noida Sector 147 ↔ Noida Sector 148 ↔ Knowledge Park II ↔ Pari Chowk ↔ Alpha 1 ↔ Delta 1 ↔ GNIDA Office ↔ Depot
12. 🚅 **Rapid Metro Gurugram (11 Stations)**: Sector 55-56 ↔ Sector 54 Chowk ↔ Sector 53-54 ↔ Sector 42-43 ↔ Phase 1 ↔ Sikanderpur (Interchange with Yellow Line) ↔ Phase 2 ↔ Belvedere Towers ↔ Cyber City ↔ Moulsari Avenue ↔ Phase 3

---

## 2. Algorithm Details (BFS)

- **Graph Model**: Unweighted, undirected adjacency list.
- **Queue Implementation**: `collections.deque` for constant $\mathcal{O}(1)$ push and pop operations.
- **Route Tracking**: `parent` dictionary mapping `child_station -> parent_station` to backtrack and reconstruct the path upon reaching the destination.
- **Time Complexity**: $\mathcal{O}(V + E)$ where $V = 268$ vertices and $E = 285$ edges. Runs in $\approx 0.5\text{ ms}$.
- **Space Complexity**: $\mathcal{O}(V)$ for the visited set, parent dictionary, and queue.

---

## 3. How to Run Locally

```powershell
# Clone or navigate to the repository
cd r:\METRO

# Install dependencies
pip install -r requirements.txt

# Run the unit test suite
python test_metro.py

# Launch the interactive Streamlit web app
streamlit run app.py
```

Access the application in your browser at `http://localhost:8501`.

---

## 4. How to Deploy Online

### Option A: Render (1-Click Deployment)
1. Sign in to [dashboard.render.com](https://dashboard.render.com) with GitHub.
2. Click **New +** ➔ **Web Service** ➔ Select `YUVRAJ1178/MetroRoute`.
3. Render automatically detects `render.yaml`.
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`
4. Click **Deploy Web Service** to get your free public URL (`https://metroroute-xxxx.onrender.com`).

### Option B: Streamlit Community Cloud
1. Visit [share.streamlit.io](https://share.streamlit.io).
2. Connect your GitHub account and select repository `YUVRAJ1178/MetroRoute`.
3. Set Main file path: `app.py`.
4. Click **Deploy!**
