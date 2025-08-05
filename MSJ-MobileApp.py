import streamlit as st
from streamlit_option_menu import option_menu
import json
import os
import pandas as pd
import streamlit.components.v1 as components

# --- Detect if running on mobile ---
components.html("""
    <script>
        const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
        window.parent.postMessage({ isMobile: isMobile }, "*");
    </script>
""", height=0)

# Set manually for now; will be True if accessed from mobile
is_mobile = st.query_params.get("mobile", "false") == "true"

# --- Data Setup ---
DATA_FILE = "dataMSJ.json"
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        MSJ_list = json.load(f)
else:
    MSJ_list = []

# --- Page Config ---
st.set_page_config(
    page_title="My Spiritual Journey",
    layout="centered",  # Changed from "wide" to "centered" for mobile
    initial_sidebar_state="collapsed",
)

st.markdown("## 🙏 My Devotional Playlist")

# --- Navigation Menu ---
selected = option_menu(
    menu_title=None,
    options=["Sloka", "Song", "About"],
    icons=["🕉️", "om", "question-circle"],
    menu_icon=None,
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#f0f4f8"},
        "nav-link": {
            "font-size": "15px",
            "color": "#1e1e1e",
            "margin": "4px",
            "transition": "all 0.3s ease-in-out",
            "border-radius": "5px",
        },
        "nav-link-selected": {
            "background-color": "#1F77B4",
            "color": "white",
            "font-weight": "600",
        },
    }
)

# --- Sidebar Input Form ---
with st.sidebar:
    with st.form("new_sloka_form"):
        st.header("➕ Add Sloka / Song")
        title = st.text_input("Title")
        entry_type = st.selectbox("Select Type", ["Sloka", "Song"])
        god = st.text_input("God's Name")
        lyrics = st.text_input("Lyrics URL")
        audio = st.text_input("Audio URL")
        submitted = st.form_submit_button("Add")

        if submitted and title and god and lyrics:
            MSJ_list.append({
                "title": title,
                "type": entry_type,
                "god": god,
                "lyrics": lyrics,
                "audio": audio,
            })
            with open(DATA_FILE, "w") as f:
                json.dump(MSJ_list, f, indent=2)
            st.success("✅ Added!")
            st.experimental_rerun()

# --- Main View ---
if selected in ["Sloka", "Song"]:
    list_to_show = [s for s in MSJ_list if s["type"] == selected]
    
    search_term = st.text_input("🔍 Search by God's Name").strip().lower()
    if search_term:
        list_to_show = [s for s in list_to_show if search_term in s["god"].lower()]

    df = pd.DataFrame(list_to_show)

    if df.empty:
        st.info("No data to display.")
    else:
        if 'type' in df.columns:
            df = df.drop(columns=['type'])

        # Title-case column names
        df.columns = [col.title() for col in df.columns]

        # Convert links to markdown format
        df["Lyrics"] = df["Lyrics"].apply(lambda url: f"[🎧 Lyrics]({url})" if url else "")
        df["Audio"] = df["Audio"].apply(lambda url: f"[🎧 Listen]({url})" if url else "")

        # Display as markdown table (works well on mobile)
        st.markdown("### 📜 Entries")
        st.markdown(df.to_markdown(index=False), unsafe_allow_html=True)

elif selected == "About":
    st.markdown("### 🙏 Welcome to My Devotional Playlist App")
    st.markdown("""
    - 📖 Add and browse slokas and devotional songs
    - 🔍 Filter by God's name
    - 🎧 Clickable links to listen or read lyrics
    """)

