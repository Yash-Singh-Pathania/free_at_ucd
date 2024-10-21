import streamlit as st
import folium
from folium.plugins import Fullscreen
from streamlit_folium import st_folium
from sqlalchemy.orm import sessionmaker
from db import get_db_session
from models import Location
import base64

st.set_page_config(
    page_title="Free at UCD",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded"
)

db_session = get_db_session()

st.title("🍽️ Free at UCD")
m = folium.Map(location=[53.308, -6.224], zoom_start=15)

Fullscreen().add_to(m)

emoji = '⚫' 

locations = db_session.query(Location).all()

for loc in locations:
    popup_html = f"""
    <div style="font-family: Arial, sans-serif; font-size: 14px; max-width: 250px;">
        <h4 style="margin-bottom: 5px;">{loc.location_name}</h4>
        <table style="width: 100%;">
            <tr>
                <td style="vertical-align: top;"><b>Food Being Given Out:</b></td>
                <td>{loc.food_item}</td>
            </tr>
            <tr>
                <td style="vertical-align: top;"><b>Since When:</b></td>
                <td>{loc.since_when}</td>
            </tr>
            <tr>
                <td style="vertical-align: top;"><b>Till When:</b></td>
                <td>{loc.till_when}</td>
            </tr>
            <tr>
                <td style="vertical-align: top;"><b>Veg/Non-Veg:</b></td>
                <td>{loc.veg_nonveg}</td>
            </tr>
            <tr>
                <td style="vertical-align: top;"><b>Requirements:</b></td>
                <td>{loc.requirements}</td>
            </tr>
        </table>
    """
    if loc.picture:
        picture_b64 = base64.b64encode(loc.picture).decode('utf-8')
        popup_html += f'<img src="data:image/png;base64,{picture_b64}" width="200" style="margin-top: 10px;"><br>'

    popup_html += f'<a href="https://www.google.com/maps/dir/?api=1&destination={loc.lat},{loc.lon}" target="_blank" style="display: block; margin-top: 10px; text-align: center;">🗺️ Get Directions</a>'
    popup_html += "</div>"

    popup = folium.Popup(folium.IFrame(popup_html, width=250, height=350), max_width=250)

    icon = folium.DivIcon(
        html=f"""
        <div style="font-size: 24px; line-height: 24px; text-align: center;">
            {emoji}
        </div>
        """
    )

    folium.Marker(
        location=[float(loc.lat), float(loc.lon)],
        popup=popup,
        icon=icon,
        tooltip=loc.location_name  # Optional: keep the tooltip
    ).add_to(m)

st_data = st_folium(m, width=None, height=700)

st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: none;
}
.css-18e3th9 {
    padding: 1rem 0.5rem 1rem 0.5rem;
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
/* Adjust the map to be full width */
.element-container:nth-child(3) {
    width: 100%;
}
/* Mobile adjustments */
@media only screen and (max-width: 600px) {
    iframe {
        width: 100% !important;
        height: 80vh !important; /* Set height to 80% of viewport height */
    }
}
</style>
""", unsafe_allow_html=True)
