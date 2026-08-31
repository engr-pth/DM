import math
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Quantity Takeoff & Estimate Calculator",
    page_icon="🏗️",
    layout="wide",
)

st.title("🏗️ Detail Measurement & Estimate Calculator")
st.write(
    "အဆောက်အအုံဆောက်လုပ်ရေးအတွက် အသေးစိတ် ပမာဏတွက်ချက်မှုဇယား (Full Measurement Sheet)"
)

# Sidebar - Project Details
st.sidebar.header("📌 Project Details")
project_name = st.sidebar.text_input(
    "Project Name", "Two Storeyed RCC Building"
)
location = st.sidebar.text_input("Location", "Pyin Oo Lwin")
description = st.sidebar.text_input("Description", "Sub & Super Structure Work")

st.sidebar.divider()
st.sidebar.markdown(f"**Project:** {project_name}")
st.sidebar.markdown(f"**Location:** {location}")

# Items List
items_list = [
    "1. Site Cleaning Work (Sqft)",
    "2. Staking Works For Preparation of Foundation (Sqft)",
    "3. Earthwork Excavation For Foundation (Cuft)",
    "4. Hardcore With Sand Filling Work (Cuft)",
    "5. Lean Concrete (1:4:8) Work (Cuft)",
    "6. 9\"thk; Brick Retaining Wall Work (Cuft)",
    "7. (a) 12\"thk; Earth Filling Work (Cuft)",
    "7. (b) 6\"thk; Sandfilling Work (Cuft)",
    "7. (c) Plastic Sheet Laying Work (Sqft)",
    "7. (d) 4.5\"thk; (1:3:6) Concrete Work (Cuft)",
    "8. (i) Footing Concrete & Rebar Work",
    "8. (ii) Column Concrete & Rebar Work",
    "8. (iii) Beam Concrete & Rebar Work",
    "8. (iv) Slab Concrete & Rebar Work",
    "8. (v) Staircase Concrete & Rebar Work",
    "9. Backfilling Work (Cuft)",
    "10. Roofing Structure Work (Sqft / Rft)",
]

# Base Empty Template
default_empty_df = pd.DataFrame(
    [
        {
            "Section / Location": "",
            "Particular": "",
            "Nos (x)": 1,
            "Member (x)": 1,
            "Multiplier": 1,
            "L / Length (ft)": 0.0,
            "Deduction": 0.0,
            "Direct Total (ft)": 0.0,
        }
    ]
)

if "data_store" not in st.session_state:
    st.session_state.data_store = {}

# Set Up Initial Data for Roofing Structure
if "10. Roofing Structure Work (Sqft / Rft)" not in st.session_state.data_store:
    st.session_state.data_store["10. Roofing Structure Work (Sqft / Rft)"] = (
        pd.DataFrame(
            [
                # H Beam 6"x6"
                {
                    "Section / Location": "Shrine & Car Garage",
                    "Particular": 'H Beam 6"x6" (G.L-2\')',
                    "Nos (x)": 1,
                    "Member (x)": 1,
                    "Multiplier": 2,
                    "L / Length (ft)": 3.50,
                    "Deduction": 0.0,
                    "Direct Total (ft)": 0.0,
                },
                {
                    "Section / Location": "Shrine & Car Garage",
                    "Particular": 'H Beam 6"x6" (G.L-4)',
                    "Nos (x)": 1,
                    "Member (x)": 1,
                    "Multiplier": 2,
                    "L / Length (ft)": 10.00,
                    "Deduction": 0.0,
                    "Direct Total (ft)": 0.0,
                },
                {
                    "Section / Location": "Living Room",
                    "Particular": 'H Beam 6"x6" (G.L-2\')',
                    "Nos (x)": 1,
                    "Member (x)": 1,
                    "Multiplier": 2,
                    "L / Length (ft)": 4.58,
                    "Deduction": 0.0,
                    "Direct Total (ft)": 0.0,
                },
                # I Beam 6"x3"
                {
                    "Section / Location": "Shrine & Car Garage",
                    "Particular": 'I Beam 6"x3" (G.L-2\')',
                    "Nos (x)": 1,
                    "Member (x)": 1,
                    "Multiplier": 1,
                    "L / Length (ft)": 25.50,
                    "Deduction": 0.0,
                    "Direct Total (ft)": 0.0,
                },
                {
                    "Section / Location": "Shrine & Car Garage",
                    "Particular": 'I Beam 6"x3" (G.L-4)',
                    "Nos (x)": 1,
                    "Member (x)": 1,
                    "Multiplier": 1,
                    "L / Length (ft)": 7.00,
                    "Deduction": 0.0,
                    "Direct Total (ft)": 0.0,
                },
                # Prop Column 5"x2"x2.3mm
                {
                    "Section / Location": "Main Building Prop Column",
                    "Particular": 'Hollow 5"x2"x2.3mm (G.L-E)',
                    "Nos (x)": 1,
                    "Member (x)": 1,
                    "Multiplier": 1,
                    "L / Length (ft)": 6.00,
                    "Deduction": 0.0,
                    "Direct Total (ft)": 0.0,
                },
                {
                    "Section / Location": "Main Building Prop Column",
                    "Particular": 'Hollow 5"x2"x2.3mm (Bet G.L-1 & 2, 2\')',
                    "Nos (x)": 4,
                    "Member (x)": 1,
                    "Multiplier": 1,
                    "L / Length (ft)": 5.00,
                    "Deduction": 0.0,
                    "Direct Total (ft)": 0.0,
                },
                # Rafter
                {
                    "Section / Location": "Car Garage Rafter",
                    "Particular": 'Rafter Hollow 5"x2"x2.3mm',
                    "Nos (x)": 1,
                    "Member (x)": 1,
                    "Multiplier": 3,
                    "L / Length (ft)": 19.67,
                    "Deduction": 0.0,
                    "Direct Total (ft)": 0.0,
                },
                {
                    "Section / Location": "Main Building Rafter",
                    "Particular": 'Rafter Hollow 5"x2"x2.3mm (G.L-A~C)',
                    "Nos (x)": 1,
                    "Member (x)": 1,
                    "Multiplier": 4,
                    "L / Length (ft)": 33.00,
                    "Deduction": 0.0,
                    "Direct Total (ft)": 0.0,
                },
                # Purlin
                {
                    "Section / Location": "Car Garage Purlin",
                    "Particular": 'Purlin 2"x2"x1.3mm Hollow @ 2ft c/c',
                    "Nos (x)": 15,
                    "Member (x)": 1,
                    "Multiplier": 1,
                    "L / Length (ft)": 8.50,
                    "Deduction": 0.0,
                    "Direct Total (ft)": 0.0,
                },
                {
                    "Section / Location": "Main Building Vertical Purlin",
                    "Particular": 'Purlin 2"x2"x1.3mm Hollow',
                    "Nos (x)": 1,
                    "Member (x)": 1,
                    "Multiplier": 14,
                    "L / Length (ft)": 37.00,
                    "Deduction": 0.0,
                    "Direct Total (ft)": 0.0,
                },
            ]
        )
    )

# Generic Data Initialization for other items
for item in items_list:
    if item not in st.session_state.data_store:
        st.session_state.data_store[item] = default_empty_df.copy()


def calculate_roofing(row):
    if "Direct Total (ft)" in row and row["Direct Total (ft)"] > 0:
        return round(float(row["Direct Total (ft)"]), 2)
    no = (
        row.get("Nos (x)", 1)
        * row.get("Member (x)", 1)
        * row.get("Multiplier", 1)
    )
    length = row.get("L / Length (ft)", 0.0)
    deduction = row.get("Deduction", 0.0)
    return round((no * length) - deduction, 2)


view_type = st.radio(
    "မြင်ကွင်းပုံစံ ရွေးချယ်ပါ -",
    ["ကဏ္ဍအလိုက် ချုံ့/ချဲ့ စာရင်း (Expander)", "စာမျက်နှာခွဲ စာရင်း (Tabs)"],
    horizontal=True,
)

summary_data = []
st.divider()


def render_item_editor(item, key_prefix):
    df_input = st.session_state.data_store.get(item, default_empty_df.copy())

    if "Roofing Structure Work" in item:
        edited_df = st.data_editor(
            df_input,
            num_rows="dynamic",
            use_container_width=True,
            key=f"{key_prefix}_{item}",
        )
        if not edited_df.empty:
            edited_df["Content (Rft)"] = edited_df.apply(
                calculate_roofing, axis=1
            )
            st.session_state.data_store[item] = edited_df

            # Calculate Beam / Structural Summaries
            total_rft = edited_df["Content (Rft)"].sum()
            total_6m_nos = math.ceil(
                total_rft / 19.685
            )  # Convert Rft to 6M standard length numbers

            c1, c2 = st.columns(2)
            c1.metric("📐 Total Length (စုစုပေါင်းအလျား)", f"{total_rft:,.2f} Rft")
            c2.metric("📦 Estimated 6M Pipe/Beam Count", f"{total_6m_nos:,} Nos")

            temp_df = edited_df.copy()
            temp_df.insert(0, "Item Description", item)
            summary_data.append(temp_df)
    else:
        edited_df = st.data_editor(
            df_input,
            num_rows="dynamic",
            use_container_width=True,
            key=f"{key_prefix}_{item}",
        )
        if not edited_df.empty:
            st.session_state.data_store[item] = edited_df
            temp_df = edited_df.copy()
            temp_df.insert(0, "Item Description", item)
            summary_data.append(temp_df)


if view_type == "ကဏ္ဍအလိုက် ချုံ့/ချဲ့ စာရင်း (Expander)":
    for item in items_list:
        with st.expander(f"📋 {item}", expanded=False):
            render_item_editor(item, "expander")
else:
    tabs = st.tabs(items_list)
    for idx, item in enumerate(items_list):
        with tabs[idx]:
            st.subheader(item)
            render_item_editor(item, "tab")

st.divider()
st.subheader("📊 Grand Total Summary & Export")

if summary_data:
    full_sheet_df = pd.concat(summary_data, ignore_index=True)
    st.dataframe(full_sheet_df, use_container_width=True)

    csv = full_sheet_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📄 Download Complete Measurement Sheet (CSV)",
        data=csv,
        file_name=f"{project_name}_Full_Measurement_Sheet.csv",
        mime="text/csv",
    )
