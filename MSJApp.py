import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import pyrebase
from firebase_config import auth, db

# --- Session State ---
if "user" not in st.session_state:
    st.session_state.user = None

# --- App Config ---
st.set_page_config(page_title="My Spiritual Journey", layout="centered")
st.title("🕉️ My Spiritual Journey")

# --- Login / Signup Screen ---
if not st.session_state.user:
    choice = st.selectbox("Login / Signup", ["Login", "Signup"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Submit"):
        try:
            if choice == "Signup":
                auth.create_user_with_email_and_password(email, password)
                st.success("✅ Signup successful. Please login.")
            else:
                user = auth.sign_in_with_email_and_password(email, password)
                st.session_state.user = user
                st.success("✅ Login successful!")
                st.rerun()
        except Exception as e:
            st.error(f"❌ Error: {e}")

# --- Main App (Visible only if user is logged in) ---
else:
    # Sidebar Navigation
    selected = option_menu(
        menu_title=None,
        options=["Sloka", "Song", "About", "Logout"],
        icons=["sun", "music-note-list", "info-circle", "box-arrow-in-right"],
        default_index=0,
        orientation="horizontal"
    )

    if selected == "Logout":
        st.session_state.user = None
        st.success("✅ Logged out.")
        st.rerun()

    # Sidebar Form to Add Entry
    st.sidebar.header("➕ Add Sloka / Song")
    with st.sidebar.form("new_form"):
        title = st.text_input("Title")
        entry_type = st.selectbox("Type", ["Sloka", "Song"])
        god = st.text_input("God's Name")
        lyrics = st.text_input("Lyrics URL")
        audio = st.text_input("Audio URL")
        submitted = st.form_submit_button("Add")

        if submitted:
            user_email = st.session_state.user["email"]
            user_id = user_email.replace('.', '_')
            db.child("users").child(user_id).push({
                "title": title,
                "type": entry_type,
                "god": god,
                "lyrics": lyrics,
                "audio": audio
            })
            st.success("✅ Entry saved!")
            st.rerun()

    # Load Data for Logged-in User
    user_email = st.session_state.user["email"]
    user_id = user_email.replace('.', '_')
    raw_data = db.child("users").child(user_id).get()
    entries = [item.val() for item in raw_data.each()] if raw_data.each() else []

    # Filter and Display
    if selected in ["Sloka", "Song"]:
        df = pd.DataFrame([e for e in entries if e["type"] == selected])

        search_term = st.text_input("🔍 Search by God's Name").strip().lower()
        if search_term:
            df = df[df["god"].str.lower().str.contains(search_term)]

        if not df.empty:
            df["Lyrics"] = df["lyrics"].apply(lambda url: f"[📖 Lyrics]({url})" if url else "")
            df["Audio"] = df["audio"].apply(lambda url: f"[🎧 Listen]({url})" if url else "")
            df = df[["title", "god", "Lyrics", "Audio"]]
            df.columns = [col.title() for col in df.columns]
            st.markdown("### 📜 Your Playlist")
            st.markdown(df.to_markdown(index=False), unsafe_allow_html=True)
        else:
            st.info("No entries found.")

    elif selected == "About":
        st.markdown("### 🙏 Welcome to My Devotional Playlist App")
        st.markdown("""
        - 📖 Add and browse slokas and devotional songs  
        - 🔍 Filter by God's name  
        - 🎧 Clickable links to listen or read lyrics  
        - 🔐 Each user's data is private  
        """)


