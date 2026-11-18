"""
app.py - MetroRoute: Complete Delhi Metro (DMRC) Route Finder using BFS (232 Stations)
----------------------------------------------------------------------------------------
Streamlit User Interface featuring 232 real DMRC stations across all 10 lines,
manual Breadth-First Search (BFS), a clean white metro-map background, and an
unobstructed schematic metro map rendered via Streamlit Components.
"""

import sys
from pathlib import Path

# Ensure local directory is in Python search path
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

import streamlit as st
import streamlit.components.v1 as components
from graph import build_sample_metro_network, LINE_COLORS
from map_renderer import generate_dmrc_map_svg

# Page configuration
st.set_page_config(
    page_title="MetroRoute - DMRC Metro Route Finder",
    page_icon="🚇",
    layout="wide"
)

# ----------------- White Metro Map Background & Global High-Contrast CSS -----------------
st.markdown("""
    <style>
    /* Global Text Visibility: Ensure high-contrast dark text on white backgrounds */
    html, body, [class*="css"], .stApp, p, span, label, h1, h2, h3, h4, h5, h6, div {
        color: #0f172a !important;
    }

    /* Remove any default iframe borders */
    iframe, iframe[data-testid="stIFrame"] {
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        display: block !important;
    }

    /* Full viewport background styled as an authentic schematic metro network on clean WHITE */
    .stApp {
        background-color: #f8fafc !important;
        background-image: url("data:image/svg+xml,%3Csvg%20xmlns%3D%27http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%27%20width%3D%27340%27%20height%3D%27340%27%20viewBox%3D%270%200%20340%20340%27%3E%3Cdefs%3E%3Cpattern%20id%3D%27grid%27%20width%3D%2734%27%20height%3D%2734%27%20patternUnits%3D%27userSpaceOnUse%27%3E%3Cpath%20d%3D%27M%2034%200%20L%200%200%200%2034%27%20fill%3D%27none%27%20stroke%3D%27%23e2e8f0%27%20stroke-width%3D%270.8%27%20stroke-opacity%3D%270.8%27%2F%3E%3Ccircle%20cx%3D%2734%27%20cy%3D%2734%27%20r%3D%271%27%20fill%3D%27%23cbd5e1%27%20opacity%3D%270.9%27%2F%3E%3C%2Fpattern%3E%3C%2Fdefs%3E%3Crect%20width%3D%27340%27%20height%3D%27340%27%20fill%3D%27%23f8fafc%27%2F%3E%3Crect%20width%3D%27340%27%20height%3D%27340%27%20fill%3D%27url%28%23grid%29%27%2F%3E%3Cline%20x1%3D%270%27%20y1%3D%27300%27%20x2%3D%27300%27%20y2%3D%270%27%20stroke%3D%27%230066B2%27%20stroke-width%3D%275%27%20opacity%3D%270.12%27%20stroke-linecap%3D%27round%27%2F%3E%3Cline%20x1%3D%270%27%20y1%3D%27130%27%20x2%3D%27340%27%20y2%3D%27130%27%20stroke%3D%27%23E31B23%27%20stroke-width%3D%275%27%20opacity%3D%270.12%27%20stroke-linecap%3D%27round%27%2F%3E%3Cline%20x1%3D%27170%27%20y1%3D%270%27%20x2%3D%27170%27%20y2%3D%27340%27%20stroke%3D%27%23FDB813%27%20stroke-width%3D%275%27%20opacity%3D%270.15%27%20stroke-linecap%3D%27round%27%2F%3E%3Cline%20x1%3D%2730%27%20y1%3D%27340%27%20x2%3D%27340%27%20y2%3D%2730%27%20stroke%3D%27%23B82687%27%20stroke-width%3D%274%27%20opacity%3D%270.11%27%20stroke-linecap%3D%27round%27%2F%3E%3Cpath%20d%3D%27M%200%2050%20Q%20120%2050%2C%20210%20140%20T%20340%20230%27%20fill%3D%27none%27%20stroke%3D%27%236F2C91%27%20stroke-width%3D%274%27%20opacity%3D%270.11%27%20stroke-linecap%3D%27round%27%2F%3E%3Ccircle%20cx%3D%27170%27%20cy%3D%27130%27%20r%3D%277.5%27%20fill%3D%27%23ffffff%27%20stroke%3D%27%230066B2%27%20stroke-width%3D%272%27%20opacity%3D%270.3%27%2F%3E%3Ccircle%20cx%3D%27170%27%20cy%3D%27130%27%20r%3D%273.5%27%20fill%3D%27%23E31B23%27%20opacity%3D%270.3%27%2F%3E%3Ccircle%20cx%3D%27170%27%20cy%3D%27220%27%20r%3D%275%27%20fill%3D%27%23ffffff%27%20stroke%3D%27%23FDB813%27%20stroke-width%3D%271.5%27%20opacity%3D%270.3%27%2F%3E%3Ccircle%20cx%3D%27170%27%20cy%3D%2750%27%20r%3D%274%27%20fill%3D%27%2394a3b8%27%20opacity%3D%270.3%27%2F%3E%3Ccircle%20cx%3D%2760%27%20cy%3D%27130%27%20r%3D%274%27%20fill%3D%27%2394a3b8%27%20opacity%3D%270.3%27%2F%3E%3Ccircle%20cx%3D%27270%27%20cy%3D%27130%27%20r%3D%274%27%20fill%3D%27%2394a3b8%27%20opacity%3D%270.3%27%2F%3E%3Ccircle%20cx%3D%2785%27%20cy%3D%27215%27%20r%3D%274%27%20fill%3D%27%2394a3b8%27%20opacity%3D%270.3%27%2F%3E%3Ccircle%20cx%3D%27215%27%20cy%3D%2785%27%20r%3D%274%27%20fill%3D%27%2394a3b8%27%20opacity%3D%270.3%27%2F%3E%3C%2Fsvg%3E");
        background-repeat: repeat;
        background-size: 340px 340px;
        background-attachment: fixed;
    }

    /* Content container */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    
    /* Header Banner */
    .metro-hero {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 60%, #075985 100%);
        color: white !important;
        padding: 22px 26px;
        border-radius: 14px;
        margin-bottom: 22px;
        box-shadow: 0 6px 20px rgba(2, 132, 199, 0.2);
    }
    .metro-hero h1 {
        margin: 0;
        font-size: 2.15rem;
        font-weight: 700;
        color: #ffffff !important;
    }
    .metro-hero p {
        margin: 6px 0 0 0;
        font-size: 1.02rem;
        color: #e0f2fe !important;
    }

    /* Clean Card Container */
    .white-card {
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }

    /* Result summary box */
    .summary-card {
        background: #f0f9ff;
        border: 1px solid #bae6fd;
        border-left: 6px solid #0284c7;
        padding: 16px 18px;
        border-radius: 10px;
        margin: 16px 0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
    }
    .summary-card h4 {
        margin: 0 0 6px 0;
        color: #0369a1 !important;
        font-size: 1.15rem;
        font-weight: 700;
    }
    .stat-badge {
        font-size: 1.35rem;
        font-weight: 700;
        color: #0284c7 !important;
    }

    /* Interchange / Transfer alert */
    .transfer-alert {
        background: #fffbeb;
        border: 1px solid #fde68a;
        border-left: 5px solid #d97706;
        padding: 9px 12px;
        border-radius: 6px;
        margin: 8px 0;
        font-size: 0.9rem;
        color: #92400e !important;
    }

    /* Clean Station Node - Minimalist design WITHOUT lollipop circles */
    .station-node {
        display: flex;
        align-items: center;
        padding: 8px 12px;
        margin: 4px 0;
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        transition: all 0.15s ease;
    }
    .station-node:hover {
        border-color: #0284c7;
        background: #f8fafc;
    }
    .station-num {
        font-weight: 700;
        font-size: 0.9rem;
        color: #64748b !important;
        width: 32px;
        flex-shrink: 0;
    }
    .station-name {
        font-weight: 600;
        font-size: 0.96rem;
        color: #0f172a !important;
    }
    .station-pill {
        margin-left: auto;
        font-size: 0.75rem;
        padding: 3px 9px;
        border-radius: 12px;
        background: #eff6ff;
        color: #1d4ed8 !important;
        font-weight: 600;
        border: 1px solid #bfdbfe;
    }
    .station-pill.origin {
        background: #dcfce7;
        color: #15803d !important;
        border-color: #86efac;
    }
    .station-pill.dest {
        background: #fee2e2;
        color: #b91c1c !important;
        border-color: #fca5a5;
    }
    .station-pill.interchange {
        background: #fef3c7;
        color: #92400e !important;
        border-color: #fde68a;
    }

    /* Metro Lines Legend Bar */
    .legend-bar {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        align-items: center;
        background: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 10px 14px;
        border-radius: 8px;
        margin-bottom: 12px;
        font-size: 0.8rem;
    }
    .legend-item {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        font-weight: 600;
        color: #334155 !important;
    }
    .legend-dot {
        width: 12px;
        height: 6px;
        border-radius: 3px;
        display: inline-block;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- Initialize Graph (Live Dynamic Load) -----------------
def get_metro_network():
    return build_sample_metro_network()

metro = get_metro_network()
stations = metro.get_all_stations()
display_stations = metro.get_display_station_list()  # User-friendly display labels (e.g. "Millennium City Centre (HUDA City Centre)")

def display_to_canon(display_label):
    """Convert a display label back to the canonical station name for BFS."""
    return metro.resolve_station(display_label)

def canon_to_display(canon_name):
    """Convert a canonical station name to its display label."""
    return metro.get_station_display_label(canon_name)

# Default selection configuration (store canonical names, display via labels)
if "selected_start" not in st.session_state:
    st.session_state["selected_start"] = "Vishwavidyalaya" if "Vishwavidyalaya" in stations else stations[0]
if "selected_dest" not in st.session_state:
    st.session_state["selected_dest"] = "Hauz Khas" if "Hauz Khas" in stations else stations[1]
if "active_route" not in st.session_state:
    initial_path, initial_stops = metro.bfs_shortest_path(
        st.session_state["selected_start"], st.session_state["selected_dest"]
    )
    st.session_state["active_route"] = initial_path
    st.session_state["total_stops"] = initial_stops

# ----------------- App Header -----------------
st.markdown("""
    <div class="metro-hero">
        <h1>🚇 MetroRoute – Delhi Metro (DMRC) Route Finder</h1>
        <p>Interactive Transit Map & BFS Shortest Path Algorithm (Data Structures & Algorithms Project)</p>
    </div>
""", unsafe_allow_html=True)

# ----------------- 2-Column Responsive Layout -----------------
col_control, col_map = st.columns([1, 1.45], gap="large")

with col_control:
    st.markdown('<div class="white-card">', unsafe_allow_html=True)
    st.subheader("📍 Journey Planner")

    start_idx_canon = st.session_state["selected_start"]
    start_display_default = canon_to_display(start_idx_canon)
    start_display_idx = display_stations.index(start_display_default) if start_display_default in display_stations else 0
    start_display = st.selectbox(
        "Select Starting Station:",
        options=display_stations,
        index=start_display_idx,
        key="start_station_box",
        help="Type to search. Station names include popular aliases (e.g. 'HUDA City Centre', 'Okhla', 'Qutab Minar')."
    )
    start_station = display_to_canon(start_display)

    dest_idx_canon = st.session_state["selected_dest"]
    dest_display_default = canon_to_display(dest_idx_canon)
    dest_display_idx = display_stations.index(dest_display_default) if dest_display_default in display_stations else 1
    dest_display = st.selectbox(
        "Select Destination Station:",
        options=display_stations,
        index=dest_display_idx,
        key="dest_station_box",
        help="Type to search. Station names include popular aliases (e.g. 'Karkar Duma', 'Huda City Centre', 'Pitam Pura')."
    )
    dest_station = display_to_canon(dest_display)

    # Action Buttons: Swap Stations & Find Shortest Route
    btn_col1, btn_col2 = st.columns([1, 2])
    with btn_col1:
        if st.button("⇄ Swap", use_container_width=True, help="Swap starting and destination stations"):
            st.session_state["selected_start"] = dest_station  # canonical
            st.session_state["selected_dest"] = start_station  # canonical
            st.session_state["active_route"], st.session_state["total_stops"] = metro.bfs_shortest_path(
                dest_station, start_station
            )
            st.rerun()

    with btn_col2:
        find_clicked = st.button("🔍 Find Shortest Route", type="primary", use_container_width=True)

    if find_clicked:
        st.session_state["selected_start"] = start_station  # canonical
        st.session_state["selected_dest"] = dest_station    # canonical
        if start_station == dest_station:
            st.session_state["active_route"] = [start_station]
            st.session_state["total_stops"] = 0
        else:
            path, stops = metro.bfs_shortest_path(start_station, dest_station)
            st.session_state["active_route"] = path
            st.session_state["total_stops"] = stops

    st.markdown('</div>', unsafe_allow_html=True)

    # Fetch active route data
    route_path = st.session_state.get("active_route")
    total_stops = st.session_state.get("total_stops", 0)

    # Display Route Results
    if route_path is None:
        st.error(
            f"❌ **No Route Available!** Station **{dest_station}** is currently disconnected "
            f"or under construction."
        )
    elif len(route_path) == 1:
        st.info(f"ℹ️ **Origin and Destination are identical ({route_path[0]}).** Total stops: 0.")
    else:
        # Route Analysis: Identify transfers and legs
        analysis = metro.get_route_analysis(route_path)
        transfers = analysis["transfers"]

        st.markdown(f"""
            <div class="summary-card">
                <h4>✅ Shortest Route Found</h4>
                <div style="color: #334155; margin-bottom: 6px;">From <b>{route_path[0]}</b> ➔ <b>{route_path[-1]}</b></div>
                <div style="display: flex; gap: 20px;">
                    <div>Stops: <span class="stat-badge">{total_stops}</span></div>
                    <div>Stations: <span class="stat-badge">{len(route_path)}</span></div>
                    <div>Transfers: <span class="stat-badge">{len(transfers)}</span></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Show Transfer Warnings if line changes are required
        if transfers:
            for tf in transfers:
                st.markdown(f"""
                    <div class="transfer-alert">
                        🔄 <b>Interchange at {tf['station']}:</b> Change from <b>{tf['from_line']}</b> to <b>{tf['to_line']}</b>
                    </div>
                """, unsafe_allow_html=True)

        st.markdown("##### 🚶 Station-by-Station Itinerary:")
        for idx, station in enumerate(route_path):
            lines = metro.get_station_lines(station)
            is_start = idx == 0
            is_end = idx == len(route_path) - 1
            is_interchange = len(lines) > 1 and not (is_start or is_end)

            if is_start:
                pill_label = "Origin"
                pill_class = "station-pill origin"
            elif is_end:
                pill_label = "Destination"
                pill_class = "station-pill dest"
            elif is_interchange:
                pill_label = f"Interchange ({' / '.join(lines)})"
                pill_class = "station-pill interchange"
            else:
                pill_label = lines[0] if lines else "Line"
                pill_class = "station-pill"

            st.markdown(f"""
                <div class="station-node">
                    <span class="station-num">{idx + 1}.</span>
                    <span class="station-name">{station}</span>
                    <span class="{pill_class}">{pill_label}</span>
                </div>
            """, unsafe_allow_html=True)

with col_map:
    st.subheader(f"🗺️ Delhi Metro (DMRC) Schematic Map ({len(stations)} Stations)")

    # Clean Legend Bar above the map showing all lines
    st.markdown("""
        <div class="legend-bar">
            <span style="font-weight:700; color:#0f172a; margin-right:4px;">LINES:</span>
            <span class="legend-item"><span class="legend-dot" style="background:#E31B23;"></span> Red</span>
            <span class="legend-item"><span class="legend-dot" style="background:#FDB813;"></span> Yellow</span>
            <span class="legend-item"><span class="legend-dot" style="background:#0066B2;"></span> Blue</span>
            <span class="legend-item"><span class="legend-dot" style="background:#009639;"></span> Green</span>
            <span class="legend-item"><span class="legend-dot" style="background:#6F2C91;"></span> Violet</span>
            <span class="legend-item"><span class="legend-dot" style="background:#E83D84;"></span> Pink</span>
            <span class="legend-item"><span class="legend-dot" style="background:#B82687;"></span> Magenta</span>
            <span class="legend-item"><span class="legend-dot" style="background:#808285;"></span> Grey</span>
            <span class="legend-item"><span class="legend-dot" style="background:#F58220;"></span> Airport</span>
            <span class="legend-item"><span class="legend-dot" style="background:#00B5E2;"></span> Aqua</span>
            <span class="legend-item"><span class="legend-dot" style="background:#4682B4;"></span> Rapid</span>
            <span class="legend-item" style="margin-left:auto;"><span class="legend-dot" style="background:#0284c7; width:18px;"></span> <b>Shortest BFS Path</b></span>
        </div>
    """, unsafe_allow_html=True)

    # Render dynamic SVG map
    svg_map_html = generate_dmrc_map_svg(
        metro,
        route_path=route_path if route_path else None,
        selected_start=start_station,
        selected_dest=dest_station
    )
    components.html(svg_map_html, height=765, scrolling=False)

# ----------------- Technical Documentation Section -----------------
st.markdown("---")
col_info1, col_info2 = st.columns(2)

with col_info1:
    with st.expander("🎓 DSA Viva Quick Reference: How BFS Works Here", expanded=True):
        st.markdown(
            "- **Graph Model:** Unweighted, undirected graph using an **Adjacency List** (`dict` mapping station name to a `list` of neighbors).\n"
            "- **Why Breadth-First Search (BFS)?** Since each rail hop between adjacent stations has an unweighted cost of 1 stop, BFS traverses the graph level-by-level using a FIFO Queue (`collections.deque`). The first time the destination is reached, it is guaranteed to have the minimum number of stops.\n"
            "- **Route Reconstruction:** As BFS explores, it records each neighbor's predecessor in a `parent` dictionary (`parent[neighbor] = current`). Once the destination is reached, the path is reconstructed by backtracking to the origin and reversing.\n"
            f"- **Time Complexity:** O(V + E) where V = {len(stations)} stations and E = {len(metro.track_segments)} track connections.\n"
            "- **Space Complexity:** O(V) for the `visited` set, `parent` dictionary, and `queue`."
        )

with col_info2:
    with st.expander("ℹ️ About This Complete DMRC + NCR Network Model", expanded=True):
        st.markdown(
            f"- **Official Comprehensive Network ({len(stations)} Stations Across 12 Lines):**\n"
            "  - 🔴 **Red Line (29 stations):** Rithala ↔ Netaji Subhash Place ↔ Inderlok ↔ Kashmere Gate ↔ Welcome ↔ Dilshad Garden ↔ Shaheed Sthal\n"
            "  - 🟡 **Yellow Line (37 stations):** Samaypur Badli ↔ Azadpur ↔ Vishwavidyalaya ↔ Kashmere Gate ↔ Rajiv Chowk ↔ Central Secretariat ↔ INA ↔ Hauz Khas ↔ Millennium City Centre\n"
            "  - 🔵 **Blue Line Main (50 stations):** Dwarka Sec 21 ↔ Janakpuri West ↔ Rajouri Garden ↔ Kirti Nagar ↔ Rajiv Chowk ↔ Mandi House ↔ Yamuna Bank ↔ Noida Sec 18 ↔ Botanical Garden ↔ Noida Electronic City\n"
            "  - 🔵 **Blue Line Branch (8 stations):** Yamuna Bank ↔ Anand Vihar ↔ Vaishali\n"
            "  - 🟢 **Green Line (23 stations):** Inderlok / Kirti Nagar ↔ Ashok Park Main ↔ Punjabi Bagh East ↔ Paschim Vihar ↔ Mundka ↔ Brigadier Hoshiar Singh\n"
            "  - 🟣 **Violet Line (34 stations):** Kashmere Gate ↔ Mandi House ↔ Central Secretariat ↔ Lajpat Nagar ↔ Kalkaji Mandir ↔ Raja Nahar Singh Ballabhgarh\n"
            "  - 🌸 **Pink Line Ring Line (38 stations):** Majlis Park ↔ Azadpur ↔ Shalimar Bagh ↔ Netaji Subhash Place ↔ Rajouri Garden ↔ INA ↔ Lajpat Nagar ↔ Mayur Vihar-I ↔ Anand Vihar ↔ Welcome ↔ Shiv Vihar\n"
            "  - 🌺 **Magenta Line (25 stations):** Janakpuri West ↔ Terminal 1 Airport ↔ IIT Delhi ↔ Hauz Khas ↔ Kalkaji Mandir ↔ Botanical Garden\n"
            "  - ⚪ **Grey Line (4 stations):** Dwarka ↔ Nangli ↔ Najafgarh ↔ Dhansa Bus Stand\n"
            "  - 🟠 **Airport Express Line (7 stations):** New Delhi ↔ Shivaji Stadium ↔ Dhaula Kuan ↔ Delhi Aerocity ↔ IGI Airport ↔ Dwarka Sector 21 ↔ Yashobhoomi\n"
            "  - 🔷 **Aqua Line Noida Metro (21 stations):** Noida Sector 51 ↔ Sector 137 ↔ Knowledge Park II ↔ Pari Chowk ↔ Depot\n"
            "  - 🚅 **Rapid Metro Gurugram (11 stations):** Cyber City Loop ↔ Sikanderpur ↔ Sector 55-56"
        )
