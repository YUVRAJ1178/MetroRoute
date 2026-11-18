"""
map_renderer.py - SVG Map Generator for Complete DMRC Metro Network (232 Stations)
-----------------------------------------------------------------------------------
Generates an unobstructed, high-definition schematic transit map in SVG format
covering 232 real DMRC stations across all 10 lines.
Dynamically highlights the BFS shortest path with high-contrast electric blue tracks,
green origin pin, red destination pin, and station name callouts.
"""

from graph import STATION_COORDINATES, LINE_COLORS

# Major stations with permanent map labels
KEY_DISPLAY_STATIONS = {
    # Terminals
    "Samaypur Badli", "Millennium City Centre",
    "Dwarka Sector 21", "Noida Electronic City",
    "Rithala", "Shaheed Sthal (New Bus Adda)",
    "Vaishali", "Brigadier Hoshiar Singh",
    "Raja Nahar Singh (Ballabhgarh)",
    "Majlis Park", "Shiv Vihar",
    "Dhansa Bus Stand",
    "IGI Airport",

    # Key Interchanges & Prominent Stations
    "Shalimar Bagh",
    "Kashmere Gate",
    "Rajiv Chowk",
    "Central Secretariat",
    "Mandi House",
    "Hauz Khas",
    "Kalkaji Mandir",
    "Botanical Garden",
    "Janakpuri West",
    "New Delhi",
    "Inderlok",
    "Netaji Subhash Place",
    "Azadpur",
    "Dilli Haat INA",
    "Lajpat Nagar",
    "Anand Vihar",
    "Karkarduma",
    "Welcome",
    "Rajouri Garden",
    "Kirti Nagar",
    "Yamuna Bank",
    "Mayur Vihar-I",
    "Pitampura",
    "Vishwavidyalaya",
    "Karol Bagh",
    "Noida Sector 18",
    "IIT Delhi",
    "Dhaula Kuan"
}

INTERCHANGE_STATIONS = {
    "Kashmere Gate",
    "Rajiv Chowk",
    "Central Secretariat",
    "Mandi House",
    "Hauz Khas",
    "Kalkaji Mandir",
    "Botanical Garden",
    "Janakpuri West",
    "New Delhi",
    "Dwarka Sector 21",
    "Inderlok",
    "Netaji Subhash Place",
    "Azadpur",
    "Dilli Haat INA",
    "Lajpat Nagar",
    "Anand Vihar",
    "Karkarduma",
    "Welcome",
    "Rajouri Garden",
    "Kirti Nagar",
    "Yamuna Bank",
    "Mayur Vihar-I",
    "Ashok Park Main",
    "Dwarka"
}


def generate_dmrc_map_svg(metro, route_path=None, selected_start=None, selected_dest=None):
    """
    Renders the DMRC network as a modern, clean schematic transit map on a white canvas.
    Highlights the BFS shortest route with high-contrast electric blue tracks and green/red station pins.
    Also highlights selected origin and destination even before searching.
    """
    has_route = route_path is not None and len(route_path) > 0
    has_segments = route_path is not None and len(route_path) > 1
    route_set = set(route_path) if route_path else set()

    # Pre-calculate adjacent pairs along the route for segment highlighting
    route_edges = set()
    if has_segments:
        for i in range(len(route_path) - 1):
            u, v = route_path[i], route_path[i + 1]
            route_edges.add((u, v))
            route_edges.add((v, u))

    svg_parts = []

    # SVG Container - Clean borderless styling
    svg_parts.append("""
    <div style="width: 100%; display: flex; justify-content: center; background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 2px 12px rgba(0,0,0,0.04);">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1650 1420" width="100%" height="760" style="background-color: #ffffff; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
      <defs>
        <filter id="route-glow" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur stdDeviation="3.5" result="blur" />
          <feMerge>
            <feMergeNode in="blur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
        <filter id="pin-shadow" x="-30%" y="-30%" width="160%" height="160%">
          <feDropShadow dx="0" dy="2" stdDeviation="2.5" flood-opacity="0.25"/>
        </filter>
      </defs>
    """)

    # Subtle Background Grid
    svg_parts.append("""
      <!-- Background Grid -->
      <g stroke="#f1f5f9" stroke-width="1">
    """)
    for x in range(0, 1660, 50):
        svg_parts.append(f'<line x1="{x}" y1="0" x2="{x}" y2="1420" />')
    for y in range(0, 1440, 50):
        svg_parts.append(f'<line x1="0" y1="{y}" x2="1650" y2="{y}" />')
    svg_parts.append("</g>")

    # Yamuna River (Realistic geographical marker across East Delhi)
    svg_parts.append("""
      <!-- Yamuna River Waterway -->
      <path d="M 980 0 Q 940 260, 990 440 T 1070 660 T 1320 1420" fill="none" stroke="#e0f2fe" stroke-width="54" opacity="0.95" stroke-linecap="round" />
      <text x="1030" y="580" fill="#38bdf8" font-size="13" font-weight="700" letter-spacing="4" transform="rotate(76, 1030, 580)" opacity="0.85">YAMUNA RIVER</text>
    """)

    # Render Normal Track Segments
    svg_parts.append("<g id='base-tracks'>")
    for u, v, line_name in metro.track_segments:
        if u in STATION_COORDINATES and v in STATION_COORDINATES:
            x1, y1 = STATION_COORDINATES[u]
            x2, y2 = STATION_COORDINATES[v]
            color = LINE_COLORS.get(line_name, "#94a3b8")

            is_active_edge = (u, v) in route_edges
            if has_segments:
                edge_opacity = "0.15" if not is_active_edge else "0.15"
            else:
                edge_opacity = "0.95"

            svg_parts.append(
                f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                f'stroke="{color}" stroke-width="6.5" stroke-linecap="round" '
                f'opacity="{edge_opacity}" />'
            )
    svg_parts.append("</g>")

    # Render Highlighted Route Path (if active)
    if has_segments:
        svg_parts.append("<g id='highlighted-route' filter='url(#route-glow)'>")
        for i in range(len(route_path) - 1):
            u = route_path[i]
            v = route_path[i + 1]
            if u in STATION_COORDINATES and v in STATION_COORDINATES:
                x1, y1 = STATION_COORDINATES[u]
                x2, y2 = STATION_COORDINATES[v]
                # Outer electric sky-blue highlight glow band
                svg_parts.append(
                    f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                    f'stroke="#38bdf8" stroke-width="14" stroke-linecap="round" opacity="0.65" />'
                )
                # Inner sharp navy core track
                svg_parts.append(
                    f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                    f'stroke="#0284c7" stroke-width="7" stroke-linecap="round" opacity="1.0" />'
                )
        svg_parts.append("</g>")

    # Render Station Nodes
    svg_parts.append("<g id='stations'>")
    all_stations = metro.get_all_stations()

    for station in all_stations:
        if station not in STATION_COORDINATES:
            continue

        x, y = STATION_COORDINATES[station]
        is_interchange = station in INTERCHANGE_STATIONS
        is_on_route = station in route_set
        is_start = (route_path and station == route_path[0]) or (not route_path and station == selected_start)
        is_end = (route_path and station == route_path[-1]) or (not route_path and station == selected_dest)

        if has_route:
            node_opacity = "1.0" if is_on_route else "0.15"
        else:
            node_opacity = "1.0"

        # Interactive tooltip tag
        tooltip = f"<title>{station}</title>"

        # Special origin and destination markers
        if is_start and is_end:
            svg_parts.append(
                f'<g>{tooltip}'
                f'<circle cx="{x}" cy="{y}" r="15" fill="#22c55e" opacity="0.35"/>'
                f'<circle cx="{x}" cy="{y}" r="8" fill="#16a34a" stroke="#ffffff" stroke-width="3" filter="url(#pin-shadow)"/>'
                f'</g>'
            )
        elif is_start:
            svg_parts.append(
                f'<g>{tooltip}'
                f'<circle cx="{x}" cy="{y}" r="15" fill="#22c55e" opacity="0.35"/>'
                f'<circle cx="{x}" cy="{y}" r="8" fill="#16a34a" stroke="#ffffff" stroke-width="3" filter="url(#pin-shadow)"/>'
                f'</g>'
            )
        elif is_end:
            svg_parts.append(
                f'<g>{tooltip}'
                f'<circle cx="{x}" cy="{y}" r="15" fill="#ef4444" opacity="0.35"/>'
                f'<circle cx="{x}" cy="{y}" r="8" fill="#dc2626" stroke="#ffffff" stroke-width="3" filter="url(#pin-shadow)"/>'
                f'</g>'
            )
        elif is_on_route:
            svg_parts.append(
                f'<g>{tooltip}'
                f'<circle cx="{x}" cy="{y}" r="6.5" fill="#0284c7" stroke="#ffffff" stroke-width="2.5" filter="url(#pin-shadow)"/>'
                f'</g>'
            )
        elif is_interchange:
            svg_parts.append(
                f'<g>{tooltip}'
                f'<circle cx="{x}" cy="{y}" r="6.5" fill="#ffffff" stroke="#1e293b" stroke-width="2.5" opacity="{node_opacity}"/>'
                f'<circle cx="{x}" cy="{y}" r="3" fill="#1e293b" opacity="{node_opacity}"/>'
                f'</g>'
            )
        else:
            svg_parts.append(
                f'<g>{tooltip}'
                f'<circle cx="{x}" cy="{y}" r="4" fill="#ffffff" stroke="#475569" stroke-width="1.8" opacity="{node_opacity}"/>'
                f'</g>'
            )

        # Label display rules
        should_show_label = is_on_route or is_start or is_end or (not has_route and (station in KEY_DISPLAY_STATIONS or is_interchange))

        if should_show_label:
            label_x = x
            label_y = y - 9
            text_anchor = "middle"

            if is_start or is_end:
                font_weight = "800"
                font_size = "13px"
                text_color = "#15803d" if is_start else "#b91c1c"
            elif is_on_route:
                font_weight = "700"
                font_size = "11.5px"
                text_color = "#0f172a"
            elif station == "Shalimar Bagh":
                font_weight = "700"
                font_size = "11px"
                text_color = "#E83D84"
            else:
                font_weight = "600" if is_interchange else "500"
                font_size = "10px" if is_interchange else "9.5px"
                text_color = "#0f172a" if is_interchange else "#334155"

            svg_parts.append(
                f'<text x="{label_x}" y="{label_y}" fill="{text_color}" font-size="{font_size}" '
                f'font-weight="{font_weight}" text-anchor="{text_anchor}" opacity="{node_opacity}" '
                f'style="paint-order: stroke fill; stroke: #ffffff; stroke-width: 3.5px; stroke-linecap: round; stroke-linejoin: round;">'
                f'{station}</text>'
            )

    svg_parts.append("</g>")
    svg_parts.append("</svg></div>")
    return "".join(svg_parts)
