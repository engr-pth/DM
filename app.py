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

# Full Structure Items List (Including Slab Work from Book1_3.xlsx)
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
    "8. (i) (a) Footing (1:2:4) Reinforced Concrete Work (Cuft)",
    "8. (i) (b) Footing Formwork (Sqft)",
    "8. (i) (c) Footing Rebar Work (16mmØ) (ft)",
    "8. (ii) (a) Column (1:2:4) Reinforced Concrete Work (Cuft)",
    "8. (ii) (b) Column Formwork (Sqft)",
    "8. (ii) (c) Column Rebar Work (16mmØ) (ft)",
    "8. (ii) (c) Column Rebar Work (10mmØ) (ft)",
    "8. (iii) (a) Beam (1:2:4) Reinforced Concrete Work (Cuft)",
    "8. (iii) (b) Beam Formwork (Sqft)",
    "8. (iii) (c) Beam Rebar Work (16mmØ) (ft)",
    "8. (iii) (c) Beam Rebar Work (10mmØ) (ft)",
    "8. (iv) (a) Slab (1:2:4) Reinforced Concrete Work (Cuft)",
    "8. (iv) (b) Slab Formwork (Sqft)",
    "8. (iv) (c) Slab Rebar Work (10mmØ) (ft)",
    "8. (iv) (c) Slab Rebar Work (12mmØ) (ft)",
]

# Base Empty Template Structure
default_empty_df = pd.DataFrame(
    [
        {
            "Particular": "",
            "Nos (x)": 1,
            "Member (x)": 1,
            "Multiplier": 1,
            "L / Length (ft)": 0.0,
            "B (ft)": 0.0,
            "H (ft)": 0.0,
            "Deduction": 0.0,
        }
    ]
)

# Initialize Session State Data Store
if "data_store" not in st.session_state:
    st.session_state.data_store = {}

# Populate initial templates with sample values from Book1_3.xlsx
for item in items_list:
    if item not in st.session_state.data_store:
        if "Slab (1:2:4) Reinforced Concrete Work" in item:
            st.session_state.data_store[item] = pd.DataFrame(
                [
                    {
                        "Particular": "1st Floor Slab - S1 (G.L-1 to 2)",
                        "Nos (x)": 1,
                        "Member (x)": 1,
                        "Multiplier": 1,
                        "L / Length (ft)": 13.00,
                        "B (ft)": 10.00,
                        "H (ft)": 0.417,
                        "Deduction": 0.0,
                    },
                    {
                        "Particular": "Landing Slab - LS",
                        "Nos (x)": 1,
                        "Member (x)": 1,
                        "Multiplier": 1,
                        "L / Length (ft)": 7.00,
                        "B (ft)": 4.57,
                        "H (ft)": 0.417,
                        "Deduction": 0.0,
                    },
                ]
            )
        elif "Slab Formwork" in item:
            st.session_state.data_store[item] = pd.DataFrame(
                [
                    {
                        "Particular": "1st Floor Slab Bottom Formwork",
                        "Nos (x)": 1,
                        "Member (x)": 1,
                        "Multiplier": 1,
                        "L / Length (ft)": 13.00,
                        "B (ft)": 10.00,
                        "H (ft)": 0.0,
                        "Deduction": 0.0,
                    },
                    {
                        "Particular": "Landing Slab Bottom Formwork",
                        "Nos (x)": 1,
                        "Member (x)": 1,
                        "Multiplier": 1,
                        "L / Length (ft)": 7.00,
                        "B (ft)": 6.00,
                        "H (ft)": 0.0,
                        "Deduction": 0.0,
                    },
                ]
            )
        elif "Slab Rebar Work (10mmØ)" in item:
            st.session_state.data_store[item] = pd.DataFrame(
                [
                    {
                        "Particular": "1st Floor Slab S1 - Main Bar (10mmØ @ 6\"c/c)",
                        "Nos (x)": 23,
                        "Member (x)": 1,
                        "Multiplier": 1,
                        "L / Length (ft)": 13.39,
                        "B (ft)": 0.0,
                        "H (ft)": 0.0,
                        "Deduction": 0.0,
                    },
                    {
                        "Particular": "Landing Slab - Distribution Bar (10mmØ @ 6\"c/c)",
                        "Nos (x)": 15,
                        "Member (x)": 1,
                        "Multiplier": 1,
                        "L / Length (ft)": 5.25,
                        "B (ft)": 0.0,
                        "H (ft)": 0.0,
                        "Deduction": 0.0,
                    },
                ]
            )
        elif "Slab Rebar Work (12mmØ)" in item:
            st.session_state.data_store[item] = pd.DataFrame(
                [
                    {
                        "Particular": "Landing Slab - Main Bar (12mmØ @ 6\"c/c)",
                        "Nos (x)": 10,
                        "Member (x)": 1,
                        "Multiplier": 1,
                        "L / Length (ft)": 7.786,
                        "B (ft)": 0.0,
                        "H (ft)": 0.0,
                        "Deduction": 0.0,
                    },
                ]
            )
        else:
            st.session_state.data_store[item] = default_empty_df.copy()


# Smart Content Calculation
def calculate_content(row, item_type):
    no = (
        row.get("Nos (x)", 1)
        * row.get("Member (x)", 1)
        * row.get("Multiplier", 1)
    )
    length = row.get("L / Length (ft)", 0.0)
    breadth = row.get("B (ft)", 0.0)
    height = row.get("H (ft)", 0.0)
    deduction = row.get("Deduction", 0.0)

    if "(ft)" in item_type:  # Rebar Linear Length
        total = (no * length) - deduction
    elif "Sqft" in item_type:  # Formwork / Area
        b_val = (
            breadth
            if breadth > 0
            else (height if height > 0 else 1.0)
        )
        total = (no * length * b_val) - deduction
    else:  # Volume (Cuft)
        total = (no * length * breadth * height) - deduction

    return round(total, 2)


# View Mode Selection
view_type = st.radio(
    "မြင်ကွင်းပုံစံ ရွေးချယ်ပါ -",
    ["ကဏ္ဍအလိုက် ချုံ့/ချဲ့ စာရင်း (Expander)", "စာမျက်နှာခွဲ စာရင်း (Tabs)"],
    horizontal=True,
)

summary_data = []
st.divider()


# Render Data Editor Table
def render_item_editor(item, key_prefix):
    df_input = st.session_state.data_store.get(item, default_empty_df.copy())

    col_config = {
        "Nos (x)": st.column_config.NumberColumn(
            min_value=1, step=1, default=1
        ),
        "Member (x)": st.column_config.NumberColumn(
            min_value=1, step=1, default=1
        ),
        "Multiplier": st.column_config.NumberColumn(
            min_value=1, step=1, default=1
        ),
        "L / Length (ft)": st.column_config.NumberColumn(
            min_value=0.0, format="%.3f"
        ),
        "B (ft)": st.column_config.NumberColumn(min_value=0.0, format="%.3f"),
        "H (ft)": st.column_config.NumberColumn(min_value=0.0, format="%.3f"),
        "Deduction": st.column_config.NumberColumn(
            min_value=0.0, format="%.2f"
        ),
    }

    disabled_cols = []
    if "(ft)" in item:
        disabled_cols = ["B (ft)", "H (ft)"]

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
            lambda r: calculate_content(r, item), axis=1
        )
        st.session_state.data_store[item] = edited_df

        total_qty = edited_df["Content"].sum()

        if "(ft)" in item:
            st.caption(f"**{item} - Total Length:** `{total_qty:,.2f} ft`")
            if "16mmØ" in item:
                ton_val = total_qty / 2084.42
                st.info(
                    f"💡 **16mmØ Rebar Estimate:** `{ton_val:,.3f} Ton` (Approx:"
                    " 53 Nos/Ton)"
                )
            elif "12mmØ" in item:
                ton_val = total_qty / 3461.30
                st.info(
                    f"💡 **12mmØ Rebar Estimate:** `{ton_val:,.3f} Ton` (Approx:"
                    " 88 Nos/Ton)"
                )
            elif "10mmØ" in item:
                ton_val = total_qty / 5304.00
                st.info(
                    f"💡 **10mmØ Rebar Estimate:** `{ton_val:,.3f} Ton` (Approx:"
                    " 135 Nos/Ton)"
                )
        elif "Sqft" in item:
            st.caption(f"**{item} - Total Area:** `{total_qty:,.2f} Sqft`")
        else:
            st.caption(f"**{item} - Total Volume:** `{total_qty:,.2f} Cuft`")

        temp_df = edited_df.copy()
        temp_df.insert(0, "Item Description", item)
        summary_data.append(temp_df)


# Render Selected View
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
