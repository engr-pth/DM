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

# All Work Items List (Page 1 to Page 4 Items Included)
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
]

# Base Empty Template Structure
default_empty_df = pd.DataFrame(
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

# Initialize Session State Data Store
if "data_store" not in st.session_state:
    st.session_state.data_store = {}

# Populate initial templates for preview/demo
for item in items_list:
    if item not in st.session_state.data_store:
        if "6. 9\"thk; Brick Retaining Wall" in item:
            st.session_state.data_store[item] = pd.DataFrame(
                [
                    {
                        "Particular": "18\"thk; Brick Work (G.L-A)",
                        "No": 1,
                        "L (ft)": 23.08,
                        "B (ft)": 1.50,
                        "H (ft)": 0.25,
                        "Deduction": 0.0,
                    },
                    {
                        "Particular": "13-1/2\"thk; Brick Work (G.L-A)",
                        "No": 1,
                        "L (ft)": 23.08,
                        "B (ft)": 1.125,
                        "H (ft)": 0.25,
                        "Deduction": 0.0,
                    },
                    {
                        "Particular": "9\"thk; Brick Work (G.L-A)",
                        "No": 1,
                        "L (ft)": 23.08,
                        "B (ft)": 0.75,
                        "H (ft)": 3.50,
                        "Deduction": 0.0,
                    },
                ]
            )
        elif "7. (a) 12\"thk; Earth Filling" in item:
            st.session_state.data_store[item] = pd.DataFrame(
                [
                    {
                        "Particular": "G.L A to B",
                        "No": 1,
                        "L (ft)": 26.0,
                        "B (ft)": 5.0,
                        "H (ft)": 1.0,
                        "Deduction": 0.0,
                    },
                    {
                        "Particular": "Deduction (Retaining Wall Area)",
                        "No": 1,
                        "L (ft)": 221.31,
                        "B (ft)": 0.75,
                        "H (ft)": 1.0,
                        "Deduction": 165.98,
                    },
                ]
            )
        else:
            st.session_state.data_store[item] = default_empty_df.copy()


# Smart Content Calculation Function
def calculate_content(row, is_sqft=False):
    if is_sqft:
        total = (row["No"] * row["L (ft)"] * row["B (ft)"]) - row["Deduction"]
    else:
        total = (
            row["No"] * row["L (ft)"] * row["B (ft)"] * row["H (ft)"]
        ) - row["Deduction"]
    return round(total, 2)


# View Mode Selection
view_type = st.radio(
    "မြင်ကွင်းပုံစံ ရွေးချယ်ပါ -",
    ["ကဏ္ဍအလိုက် ချုံ့/ချဲ့ စာရင်း (Expander)", "စာမျက်နှာခွဲ စာရင်း (Tabs)"],
    horizontal=True,
)

summary_data = []
st.divider()


# Helper function to render data editor
def render_item_editor(item, key_prefix):
    is_sqft = "Sqft" in item
    df_input = st.session_state.data_store.get(item, default_empty_df.copy())

    # Dynamic Column Config
    col_config = {
        "No": st.column_config.NumberColumn(min_value=1, step=1, default=1),
        "L (ft)": st.column_config.NumberColumn(min_value=0.0, format="%.2f"),
        "B (ft)": st.column_config.NumberColumn(min_value=0.0, format="%.2f"),
        "Deduction": st.column_config.NumberColumn(
            min_value=0.0, format="%.2f", help="နှုတ်ရန်ရှိပါက ထည့်ပါ"
        ),
    }

    if is_sqft:
        disabled_cols = ["H (ft)"]
        col_config["H (ft)"] = st.column_config.NumberColumn(
            "H (ft)", help="Sqft ဖြစ်သဖြင့် ဖြည့်ရန်မလိုပါ", disabled=True
        )
    else:
        disabled_cols = []
        col_config["H (ft)"] = st.column_config.NumberColumn(
            "H (ft)", min_value=0.0, format="%.2f"
        )

    edited_df = st.data_editor(
        df_input,
        num_rows="dynamic",
        use_container_width=True,
        key=f"{key_prefix}_{item}",
        column_config=col_config,
        disabled=disabled_cols,
    )

    if not edited_df.empty:
        edited_df["Content"] = edited_df.apply(
            lambda r: calculate_content(r, is_sqft=is_sqft), axis=1
        )
        st.session_state.data_store[item] = edited_df

        total_qty = edited_df["Content"].sum()
        unit = "Sqft" if is_sqft else "Cuft"
        st.caption(f"**{item} - Total:** `{total_qty:,.2f} {unit}`")

        temp_df = edited_df.copy()
        if is_sqft:
            temp_df["H (ft)"] = "-"
        temp_df.insert(0, "Item Description", item)
        summary_data.append(temp_df)


# Render Views
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

# Export Summary Section
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
