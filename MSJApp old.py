import streamlit as st
from streamlit_option_menu import option_menu
import json
import os
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode
import pandas as pd

DATA_FILE = "dataMSJ.json"
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        MSJ_list = json.load(f)
else:
    MSJ_list = []

st.set_page_config(
    page_title="My Spiritual Journey",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown("## My Devotional Playlist")

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

st.sidebar.header("Add New Sloka / Song")
with st.sidebar.form("new_sloka_form"):
    title = st.text_input("Title")
    entry_type = st.selectbox("Select Type", ["Sloka", "Song"])
    god = st.text_input("God's Name")
    lyrics = st.text_input("Lyrics Url")
    audio = st.text_input("Audio Url")
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
        st.sidebar.success("Added!")
        st.experimental_rerun()

if selected in ["Sloka", "Song"]:
    list_to_show = [s for s in MSJ_list if s["type"] == selected]
    col1, _ = st.columns([2, 6])
    with col1:
        search_term = st.text_input(label="Enter God's name", key="search").strip().lower()
    if search_term:
        list_to_show = [s for s in list_to_show if search_term in s["god"].lower()]

    
    df = pd.DataFrame(list_to_show)
   
    if df.empty:
        st.info("No data to display.")
    else:
        if 'type' in df.columns:
            df = df.drop(columns=['type'])
        df.columns = [col.title() for col in df.columns]
        
        # That params.eGridCell.innerHTML trick is the most reliable way to render actual HTML inside AgGrid cells when using JsCode in Streamlit.
        lyrics_renderer = JsCode("""
        function(params) {
            if (!params.value) return '';
            params.eGridCell.innerHTML = `<a href="#" onclick="window.open('${params.value}', '_blank', 'width=800,height=600'); return false;">🎧 Lyrics</a>`

        }
        """)
        # That params.eGridCell.innerHTML trick is the most reliable way to render actual HTML inside AgGrid cells when using JsCode in Streamlit.
        audio_renderer = JsCode("""
        function(params) {
            if (!params.value) return '';
            params.eGridCell.innerHTML = `<a href="#" onclick="window.open('${params.value}', '_blank', 'width=800,height=600'); return false;">🎧 Listen</a>`;

        }
        """)

        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_column("Lyrics", cellRenderer=lyrics_renderer, html=True)
        gb.configure_column("Audio",  cellRenderer=audio_renderer, html=True)
        gb.configure_default_column(sortable=True, filter=True, resizable=True)
       
        gb.configure_grid_options(onGridReady=JsCode("""
            function(params) {
                params.api.sizeColumnsToFit();
            };
        """))
        grid_options = gb.build()
        
        #print(df.columns)
        AgGrid(
            df,
            gridOptions=grid_options,
            update_mode=GridUpdateMode.NO_UPDATE,
            allow_unsafe_jscode=True,
            height=350
        )

elif selected == "About":
    st.markdown("### 🙏 Welcome to My Devotional Playlist App")
    st.markdown("You can add and browse slokas and devotional songs.")

