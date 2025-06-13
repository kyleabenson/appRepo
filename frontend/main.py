import streamlit as st
import requests
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="Now Playing",
    layout="centered",  # Use centered layout for a cleaner look
)

# --- Sidebar ---
with st.sidebar:
    st.title("Now Playing")
    st.write("""
        Share the music you're currently listening to with the world. 
        Enter the song details and a link to the track.
    """)
    st.info("Built with Streamlit", icon="🎵")

# --- Custom CSS for a Polished Look ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono&display=swap');

    /* General styling */
    body {
        font-family: 'Roboto Mono', monospace;
        background-color: #F0F2F6; /* A lighter, modern background */
        color: #333;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] * {
        color: #39542C !important; /* Green color for all text in the sidebar */
    }

    [data-testid="stSidebar"] h1 {
        color: #EFBF04 !important; /* Yellow color for the title */
    }

    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Styling for the form container */
    .stForm {
        background-color: #FFFFFF;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* Button styling */
    .stButton>button {
        background-color: #FF4B4B; /* A vibrant, modern button color */
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-size: 1rem;
        font-family: 'Roboto Mono', monospace;
        cursor: pointer;
        transition: background-color 0.3s;
    }

    .stButton>button:hover {
        background-color: #E03C3C; /* A slightly darker shade for hover */
    }

    /* Input fields */
    .stTextInput input, .stTextArea textarea {
        border: 1px solid #CCCCCC;
        border-radius: 8px;
        padding: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Main Content ---
st.header("Share Your Current Jam")

with st.form(key="now_playing_form"):
    song_name = st.text_input("Song Name")
    artist_name = st.text_input("Artist")
    song_url = st.text_input("URL to the Song")

    submit_button = st.form_submit_button(label="Share")

    if submit_button:
        if song_name and artist_name and song_url:
            timestamp = datetime.utcnow().isoformat()
            backend_url = "http://localhost:8000/nowplaying"
            payload = {
                "name": song_name,
                "artist": artist_name,
                "url": song_url,
                "timestamp": timestamp,
                "id": 450,
                "user_id": 20,
            }

            try:
                response = requests.post(backend_url, json=payload)
                if response.status_code == 200:
                    st.success("Successfully shared your song!")
                else:
                    st.error(f"Failed to share song. Status code: {response.status_code}")
                    st.error(f"Response: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please fill out all fields.")

# To run this app, save the code as `main.py` and run `streamlit run main.py` in your terminal.