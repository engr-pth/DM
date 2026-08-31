import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Quantity Takeoff & Estimate Calculator",
    page_icon="🏗️",
    layout="wide",
)

st.title("🏗️ Detail Measurement & Estimate Calculator")
st.write("အဆောက်အအုံဆောက်လုပ်ရေးအတွက် အသေးစိတ် ပမာဏတွက်ချက်မှုဇယား")

# Project Info Inputs
st.sidebar.header("📌 Project Details")
project_name = st.sidebar.text_input(
    "Project Name", "Two Storeyed RCC Building"
)
location = st.sidebar.text_input("Location", "Pyin Oo Lwin")
description = st.sidebar.text_input("Description", "Sub & Super Structure Work")

st.sidebar.divider()
st.sidebar.markdown(f"**Project:** {project_name}")
st.sidebar.markdown(f"**Location:** {location}")

# Items setup
items_list = [
    "1. Site Cleaning Work (Sqft)",
    "2. Staking Works For Preparation of Foundation (Sqft)",
    "3. Earthwork Excavation For Foundation (Cuft)",
    "4. Hardcore With Sand Filling Work (Cuft)",
]

selected_item = st.selectbox("လုပ်ငန်းစဉ် အမျိုးအစား ကိုရွေးချယ်ပါ -", items_list)

# Initial sample templates for input dataframe
if "data_store" not in st.session_state:
    st.session_state.data_store = {
        "3. Earthwork Excavation For Foundation (Cuft)": pd.DataFrame(
            [
                {
                    "Particular": "F1 (7'-0\"x7'-0\")",
                    "No": 3,
                    "L (ft)": 8.0,
                    "B (ft)": 8.0,
                    "H (ft)": 5.0,
                    "Deduction": 0.0,
                },
                {
                    "Particular": "F2 (6'-0\"x6'-0\")",
                    "No": 5,
                    "L (ft)": 7.0,
                    "B (ft)": 7.0,
                    "H (ft)": 5.0,
                    "Deduction": 0.0,
                },
                {
                    "Particular": "F3 (5'-0\"x5'-0\")",
                    "No": 9,
                    "L (ft)": 6.0,
                    "B (ft)": 6.0,
                    "H (ft)": 5.0,
                    "Deduction": 0.0,
                },
            ]
        ),
        "4. Hardcore With Sand Filling Work (Cuft)": pd.DataFrame(
            [
                {
                    "Particular": "F1 (7'-0\"x7'-0\")",
                    "No": 3,
                    "L (ft)": 7.0,
                    "B (ft)": 7.0,
                    "H (ft)": 0.5,
                    "Deduction": 0.0,
                },
                {
                    "Particular": "F2 (6'-0\"x6'-0\")",
                    "No": 5,
                    "L (ft)": 6.0,
                    "B (ft)": 6.0,
                    "H (ft)": 0.5,
                    "Deduction": 0.0,
                },
            ]
        ),
    }

# Ensure dataframe exists for selected item
if selected_item not in st.session_state.data_store:
    st.session_state.data_store[selected_item] = pd.DataFrame(
        [
            {
                "Particular": "",
                "No": 1,
                "L (ft)": 0.0,
                "B (ft)": 0.0,
                "H (ft)": 0.0,
                "Deduction": 0.0,
            }
        ]
    )

st.subheader(f"📝 Measurement Data Entry: {selected_item}")

# Editable Table Input
edited_df = st.data_editor(
    st.session_state.data_store[selected_item],
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "No": st.column_config.NumberColumn(min_value=1, step=1, default=1),
        "L (ft)": st.column_config.NumberColumn(min_value=0.0, format="%.2f"),
        "B (ft)": st.column_config.NumberColumn(min_value=0.0, format="%.2f"),
        "H (ft)": st.column_config.NumberColumn(
            min_value=0.0, format="%.2f", help="Sqft အတွက်ဖြစ်ပါက 1 ဟုထားပါ"
        ),
        "Deduction": st.column_config.NumberColumn(
            min_value=0.0, format="%.2f"
        ),
    },
)

# Calculate Content
# If Sqft, multiplier for H is treated as 1 if H=0
def calculate_content(row):
    h_val = row["H (ft)"] if row["H (ft)"] > 0 else 1.0
    total = (
        (row["No"] * row["L (ft)"] * row["B (ft)"] * h_val) - row["Deduction"]
    )
    return round(total, 2)


if not edited_df.empty:
    edited_df["Content"] = edited_df.apply(calculate_content, axis=1)
    st.session_state.data_store[selected_item] = edited_df

    st.subheader("📊 Calculation Summary")
    st.dataframe(edited_df, use_container_width=True)

    item_total = edited_df["Content"].sum()
    unit = "Sqft" if "Sqft" in selected_item else "Cuft"

    st.metric(
        label=f"Total Quantity for [{selected_item}]",
        value=f"{item_total:,.2f} {unit}",
    )

# Export Functionality
st.divider()
st.subheader("📥 Export Summary Data")

# Combine all data
all_records = []
for item_name, df_item in st.session_state.data_store.items():
    if not df_item.empty:
        temp_df = df_item.copy()
        temp_df["Content"] = temp_df.apply(calculate_content, axis=1)
        temp_df["Item Description"] = item_name
        all_records.append(temp_df)

if all_records:
    final_export_df = pd.concat(all_records, ignore_index=True)
    csv = final_export_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📄 Export to CSV (Excel File)",
        data=csv,
        file_name=f"{project_name}_Measurement_Sheet.csv",
        mime="text/csv",
    )
