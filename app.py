import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Detail Measurement Sheet", page_icon="🏗️", layout="wide"
)

st.title("🏗️ Two Storeyed RCC Building - Detail Measurement Sheet")
st.caption("Location: Pyin Oo Lwin | Description: Sub & Super Structure Work")

# Data structure
data = {
    "Item No": [1, 2, 3, 3, 4, 4],
    "Particular": [
        "Site Cleaning Work",
        "Staking Works",
        "Earthwork Excavation (Footing)",
        "Earthwork Excavation (Retaining Wall)",
        "Hardcore With Sand Filling (Footing)",
        "Hardcore With Sand Filling (Retaining Wall)",
    ],
    "Content / Quantity": [3160.50, 3160.50, 4295.00, 1958.30, 305.50, 208.07],
    "Unit": ["Sqft", "Sqft", "Cuft", "Cuft", "Cuft", "Cuft"],
}

df = pd.DataFrame(data)

# Summary Cards
col1, col2, col3 = st.columns(3)
col1.metric("Site Area", "3,160.50 Sqft")
col2.metric(
    "Total Earthwork Excavation",
    f"{df[df['Item No'] == 3]['Content / Quantity'].sum():,.2f} Cuft",
)
col3.metric(
    "Total Sand & Hardcore",
    f"{df[df['Item No'] == 4]['Content / Quantity'].sum():,.2f} Cuft",
)

st.divider()
st.subheader("📊 Detailed Measurement Summary")
st.dataframe(df, use_container_width=True)
