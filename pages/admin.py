import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from datetime import datetime
import base64
from streamlit_geolocation import streamlit_geolocation
import os
from models import Location
from PIL import Image
import io

# Import db session and engine from db.py
from db import get_db_session

# Initialize database session
db_session = get_db_session()

st.set_page_config(
    page_title="Free at UCD",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🔑 Admin Interface")

# Load admin code from environment variables
admin_code_input = st.text_input("Enter Admin Code", type="password")
admin_code = os.getenv('ADMIN_CODE')  # Replace with environment variable for production

if admin_code_input == admin_code:
    st.success("Admin Mode Activated")
    
    # Option to use current location
    use_current_location = st.checkbox("Use Current Location")
    
    if use_current_location:
        loc_data = streamlit_geolocation()
        if loc_data and 'lat' in loc_data and 'lng' in loc_data:
            lat = loc_data['lat']
            lon = loc_data['lng']
            st.success(f"Current Location: {lat}, {lon}")
        else:
            lat = None
            lon = None
            st.warning("Unable to retrieve current location.")
    else:
        lat = None
        lon = None
    
    st.write("**Select Location on Map**")
    
    # Initialize map
    if lat and lon:
        map_center = [lat, lon]
    else:
        map_center = [53.308, -6.224]  # Center on UCD
    
    m = folium.Map(location=map_center, zoom_start=15)
    
    # Add click listener to map
    m.add_child(folium.LatLngPopup())
    
    # Display map and get clicked location
    map_data = st_folium(m, width=700, height=500)
    
    if map_data and map_data["last_clicked"]:
        selected_lat = map_data["last_clicked"]["lat"]
        selected_lon = map_data["last_clicked"]["lng"]
        st.success(f"Selected Location: {selected_lat}, {selected_lon}")
    else:
        selected_lat = lat
        selected_lon = lon
    
    with st.form("Add Location"):
        st.write("**Add New Food Giveaway Location**")
        food_item = st.text_input("Food Being Given Out")
        since_when = st.time_input("Since When")
        till_when = st.time_input("Till When")
        veg_nonveg = st.selectbox("Veg/Non-Veg", ["Veg", "Non-Veg", "Both"])
        requirements = st.text_input("Specific Requirements")
        picture = st.file_uploader("Upload Picture of Kiosk", type=['png', 'jpg', 'jpeg'])
        location_name = st.text_input("Location Name or Address", value="Selected Location")
        
        submit = st.form_submit_button("Add Location")
        
        if submit:
            if selected_lat and selected_lon:
                if picture is not None:
                    image = Image.open(picture)
                    image = image.resize((500, 500))  # Adjust size as needed
                    img_byte_arr = io.BytesIO()
                    image.save(img_byte_arr, format='PNG')
                    picture_bytes = img_byte_arr.getvalue()
                else:
                    picture_bytes = None
                
                new_location = Location(
                    food_item=food_item,
                    since_when=since_when.strftime("%H:%M"),
                    till_when=till_when.strftime("%H:%M"),
                    veg_nonveg=veg_nonveg,
                    requirements=requirements,
                    lat=str(selected_lat),
                    lon=str(selected_lon),
                    picture=picture_bytes,
                    location_name=location_name
                )
                db_session.add(new_location)
                db_session.commit()
                st.success("📍 Location Added Successfully!")
            else:
                st.error("Please select a location on the map or use your current location.")
    
    st.markdown("---")
    
    st.header("🗑️ Delete Existing Locations")
    
    locations = db_session.query(Location).all()
    
    if locations:
        for loc in locations:
            with st.expander(f"{loc.location_name}"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**Food:** {loc.food_item}")
                    st.write(f"**Since:** {loc.since_when}")
                    st.write(f"**Till:** {loc.till_when}")
                    st.write(f"**Veg/Non-Veg:** {loc.veg_nonveg}")
                    st.write(f"**Requirements:** {loc.requirements}")
                with col2:
                    delete_button = st.button("Delete", key=f"delete_{loc.id}")
                    if delete_button:
                        db_session.delete(loc)
                        db_session.commit()
                        st.success(f"✅ Deleted '{loc.location_name}'")
                        st.experimental_rerun()
    else:
        st.info("No locations available to delete.")
    
else:
    st.error("🚫 Incorrect Admin Code")

# Styling and hiding Streamlit default sidebar
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
@media only screen and (max-width: 600px) {
    iframe {
        width: 100% !important;
        height: 400px !important;
    }
}
</style>
""", unsafe_allow_html=True)
