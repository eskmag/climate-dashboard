import streamlit as st
from PIL import Image

st.set_page_config(page_title="Home | Bergen Climate Dashboard", layout="wide")

# Optional logo or header image
# st.image("assets/logo.png", width=150)

st.title("🌍 Bergen Climate Dashboard")
st.markdown("##### Understand how climate is changing in Bergen, Norway — through data.")

st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 What is this?")
    st.markdown("""
    This interactive dashboard provides insights into how climate patterns are evolving in Bergen, Norway.  
    You’ll find visualizations of:
    - 🔺 Temperature trends (daily, monthly, yearly)
    - 🌧️ Rainfall patterns over the last decade
    - 📈 Annual climate summaries

    All data comes from [Open-Meteo](https://open-meteo.com/) and is updated regularly.

    Whether you're a student, journalist, business, or climate advocate — this tool helps you **understand the local climate story** in a clear and data-driven way.
    """)

    st.subheader("🧭 How to use this app:")
    st.markdown("""
    1. Head to the **Climate Trends** tab to explore temperature and rainfall graphs.
    2. Use filters (coming soon) to explore specific time periods.
    3. (Optional) Download reports or data for your own use.
    """)

with col2:
    try:
        st.image("assets/bergen.avif", 
                 caption="Bergen, Norway", 
                 use_container_width=True)
    except:
        st.markdown("🏔️ **Bergen, Norway**")
        st.markdown("*Beautiful coastal city surrounded by mountains*")

st.markdown("---")

st.info("📍 Built with Python, Streamlit, and Open-Meteo data.")
st.caption("© 2025 - Bergen Climate Dashboard by [Your Name or GitHub Handle]")
