import streamlit as st

# --- PAGE SETUP ---
about_page = st.Page(
    page = "/Users/danishaziz/Desktop/danish/streamlit_multipage_app/views/about_me.py",
    title = "About Me",
    icon = ":material/account_circle:",
    default=True,



)
project_1_page = st.Page(
    page = "/Users/danishaziz/Desktop/danish/streamlit_multipage_app/views/chatbot.py",
    title="Chat Bot",
    icon = ":material/smart_toy:",


)

# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
pg = st.navigation(
    {
        "Info":[about_page],
        "Projects":  [project_1_page],
    }

)

# --- SHARED ON ALL PAGES ---
st.logo("/Users/danishaziz/Desktop/danish/streamlit_multipage_app/assets/logo _infinity.jpg", size= "large")
st.sidebar.text("Made with ❤️ by Danish")

# ---RUN NAVIGATION ---
pg.run()