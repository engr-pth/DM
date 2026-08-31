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

# All Work Items List
items_list = [
    "1. Site Cleaning Work (Sqft)",
    "2. Staking Works For Preparation of Foundation (Sqft)",
    "3. Earthwork Excavation For Foundation (Cuft)",
    "4. Hardcore With Sand Filling Work (Cuft)",
    "5. Lean Concrete (1:4:8) Work (Cuft)",
    "6. Reinforced Concrete Footing Work (Cuft)",
    "7. Column Stump Concrete Work (Cuft)",
    "8. Plinth Beam Concrete Work (Cuft)",
]

# Initialize Session State Data Store for all items
if "data_store" not in st.session_state:
    st.session_state.data_store = {}

    # Pre-fill initial items
    for item in items_list:
        if "3. Earthwork Excavation" in item:
            st.session_state.data_store[item] = pd.DataFrame(
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
            )
        elif "4. Hardcore With Sand" in item:
            st.session_state.data_store[item] = pd.DataFrame(
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
            )
        else:
            st.session_state.data_store[item] = pd.DataFrame(
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


def calculate_content(row):
    h_val = row["H (ft)"] if row["H (ft)"] > 0 else 1.0
    total = (
        (row["No"] * row["L (ft)"] * row["B (ft)"] * h_val) - row["Deduction"]
    )
    return round(total, 2)


# View Mode Selection: Expanders or Tabs
view_type = st.radio(
    "မြင်ကွင်းပုံစံ ရွေးချယ်ပါ -",
    ["ကဏ္ဍအလိုက် ချုံ့/ချဲ့ စာရင်း (Expander)", "စာမျက်နှာခွဲ စာရင်း (Tabs)"],
    horizontal=True,
)

summary_data = []

st.divider()

if view_type == "ကဏ္ဍအလိုက် ချုံ့/ချဲ့ စာရင်း (Expander)":
    for item in items_list:
        with st.expander(f"📋 {item}", expanded=True):
            df_input = st.session_state.data_store[item]

            edited_df = st.data_editor(
                df_input,
                num_rows="dynamic",
                use_container_width=True,
                key=f"editor_{item}",
                column_config={
                    "No": st.column_config.NumberColumn(
                        min_value=1, step=1, default=1
                    ),
                    "L (ft)": st.column_config.NumberColumn(
                        min_value=0.0, format="%.2f"
                    ),
                    "B (ft)": st.column_config.NumberColumn(
                        min_value=0.0, format="%.2f"
                    ),
                    "H (ft)": st.column_config.NumberColumn(
                        min_value=0.0,
                        format="%.2f",
                        help="Sqft အတွက်ဖြစ်ပါက 1 သို့မဟုတ် 0 ထားပါ",
                    ),
                    "Deduction": st.column_config.NumberColumn(
                        min_value=0.0, format="%.2f"
                    ),
                },
            )

            if not edited_df.empty:
                edited_df["Content"] = edited_df.apply(
                    calculate_content, axis=1
                )
                st.session_state.data_store[item] = edited_df

                total_qty = edited_df["Content"].sum()
                unit = "Sqft" if "Sqft" in item else "Cuft"
                st.caption(
                    f"**{item} - Total:** `{total_qty:,.2f} {unit}`"
                )

                temp_df = edited_df.copy()
                temp_df.insert(0, "Item Description", item)
                summary_data.append(temp_df)

else:
    tabs = st.tabs(items_list)
    for idx, item in enumerate(items_list):
        with tabs[idx]:
            st.subheader(item)
            df_input = st.session_state.data_store[item]

            edited_df = st.data_editor(
                df_input,
                num_rows="dynamic",
                use_container_width=True,
                key=f"tab_editor_{item}",
                column_config={
                    "No": st.column_config.NumberColumn(
                        min_value=1, step=1, default=1
                    ),
                    "L (ft)": st.column_config.NumberColumn(
                        min_value=0.0, format="%.2f"
                    ),
                    "B (ft)": st.column_config.NumberColumn(
                        min_value=0.0, format="%.2f"
                    ),
                    "H (ft)": st.column_config.NumberColumn(
                        min_value=0.0, format="%.2f"
                    ),
                    "Deduction": st.column_config.NumberColumn(
                        min_value=0.0, format="%.2f"
                    ),
                },
            )

            if not edited_df.empty:
                edited_df["Content"] = edited_df.apply(
                    calculate_content, axis=1
                )
                st.session_state.data_store[item] = edited_df

                total_qty = edited_df["Content"].sum()
                unit = "Sqft" if "Sqft" in item else "Cuft"
                st.caption(
                    f"**{item} - Total:** `{total_qty:,.2f} {unit}`"
                )

                temp_df = edited_df.copy()
                temp_df.insert(0, "Item Description", item)
                summary_data.append(temp_df)

# Export Summary Section
st.divider()
st.subheader("📊 Grand Total Summary & Export")

if summary_data:
    full_sheet_df = pd.concat(summary_data, ignore_index=True)

    # Clean display
    st.dataframe(full_sheet_df, use_container_width=True)

    csv = full_sheet_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📄 Download Complete Measurement Sheet (CSV)",
        data=csv,
        file_name=f"{project_name}_Full_Measurement_Sheet.csv",
        mime="text/csv",
    )
