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

# Full Items List
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
    "11. Anti-Rust Painting Work (Sqft)",
    "12. 0.4mm thk; Amcan Roofing Sheet Work (Sqft)",
    "13. Flashing Covering Work (Rft / Nos)",
    "14. 8\"x8\" Gutter Work (Rft / Nos)",
    "15. Eave Board Work (Rft / Nos)",
    "16. Bamboo Scaffolding Work (Sqft)",
]

# Base Empty Template
default_empty_df = pd.DataFrame(
    [
        {
            "Particular": "",
            "Nos (x)": 1,
            "Member (x)": 1,
            "Multiplier": 1,
            "L / Length (ft)": 0.0,
            "B / Width (ft)": 0.0,
            "H / Height (ft)": 0.0,
            "Deduction": 0.0,
            "Direct Total": 0.0,
        }
    ]
)

# Global Session State Initializations
if "data_store" not in st.session_state:
    st.session_state.data_store = {}

if "active_items" not in st.session_state:
    # Default: All items are included initially
    st.session_state.active_items = {item: True for item in items_list}

# Initialize data store for each item
for item in items_list:
    if item not in st.session_state.data_store:
        st.session_state.data_store[item] = default_empty_df.copy()

# Sidebar Multi-Select / Checkbox Control to Include/Exclude Items
st.sidebar.divider()
st.sidebar.subheader("⚙️ Select Items to Include")

# Quick action buttons for toggle
col_btn1, col_btn2 = st.sidebar.columns(2)
if col_btn1.button("Select All", use_container_width=True):
    for k in st.session_state.active_items:
        st.session_state.active_items[k] = True
if col_btn2.button("Deselect All", use_container_width=True):
    for k in st.session_state.active_items:
        st.session_state.active_items[k] = False

# Individual item checkboxes in Sidebar
for item in items_list:
    st.session_state.active_items[item] = st.sidebar.checkbox(
        item, value=st.session_state.active_items[item], key=f"chk_{item}"
    )


# Calculation Function
def calculate_item_content(row, item_name):
    if "Direct Total" in row and row["Direct Total"] > 0:
        return round(float(row["Direct Total"]), 2)

    no = (
        row.get("Nos (x)", 1)
        * row.get("Member (x)", 1)
        * row.get("Multiplier", 1)
    )
    l_val = row.get("L / Length (ft)", 0.0)
    w_val = row.get("B / Width (ft)", 0.0)
    h_val = row.get("H / Height (ft)", 0.0)
    deduction = row.get("Deduction", 0.0)

    if "(Sqft)" in item_name:
        b_val = w_val if w_val > 0 else (h_val if h_val > 0 else 1.0)
        total = (no * l_val * b_val) - deduction
    elif "(Rft" in item_name or "(ft)" in item_name:
        total = (no * l_val) - deduction
    else:
        total = (no * l_val * w_val * h_val) - deduction

    return round(total, 2)


# View Mode Selection
view_type = st.radio(
    "မြင်ကွင်းပုံစံ ရွေးချယ်ပါ -",
    ["ကဏ္ဍအလိုက် ချုံ့/ချဲ့ စာရင်း (Expander)", "စာမျက်နှာခွဲ စာရင်း (Tabs)"],
    horizontal=True,
)

summary_data = []
st.divider()


def render_item_editor(item, key_prefix):
    is_active = st.session_state.active_items.get(item, True)

    # Top status indicator for inclusion
    if not is_active:
        st.warning(
            "⚠️ ဤ Item ကို တွက်ချက်မှုမှ ဖယ်ထုတ်ထားပါသည် (Excluded from Total Calculation)"
        )

    df_input = st.session_state.data_store.get(item, default_empty_df.copy())

    edited_df = st.data_editor(
        df_input,
        num_rows="dynamic",
        use_container_width=True,
        key=f"{key_prefix}_{item}",
    )

    if not edited_df.empty:
        edited_df["Total Content"] = edited_df.apply(
            lambda r: calculate_item_content(r, item), axis=1
        )
        st.session_state.data_store[item] = edited_df

        # If Item is ACTIVE, calculate totals and append to Summary Sheet
        if is_active:
            grand_total = edited_df["Total Content"].sum()

            if "(Sqft)" in item:
                st.caption(f"**{item} Total Area:** `{grand_total:,.2f} Sqft`")
            elif "(Cuft)" in item:
                st.caption(
                    f"**{item} Total Volume:** `{grand_total:,.2f} Cuft`"
                )
            else:
                st.caption(f"**{item} Total Quantity:** `{grand_total:,.2f}`")

            temp_df = edited_df.copy()
            temp_df.insert(0, "Item Description", item)
            summary_data.append(temp_df)


# Render Selected View Mode
if view_type == "ကဏ္ဍအလိုက် ချုံ့/ချဲ့ စာရင်း (Expander)":
    for item in items_list:
        is_active = st.session_state.active_items.get(item, True)
        title_prefix = "✅" if is_active else "❌ (Excluded)"
        with st.expander(f"{title_prefix} {item}", expanded=False):
            render_item_editor(item, "expander")
else:
    tabs = st.tabs(
        [
            (
                f"✅ {it[:15]}..."
                if st.session_state.active_items.get(it, True)
                else f"❌ {it[:15]}..."
            )
            for it in items_list
        ]
    )
    for idx, item in enumerate(items_list):
        with tabs[idx]:
            st.subheader(item)
            render_item_editor(item, "tab")

# Summary Section
st.divider()
st.subheader("📊 Active Grand Total Summary & Export")

if summary_data:
    full_sheet_df = pd.concat(summary_data, ignore_index=True)
    st.dataframe(full_sheet_df, use_container_width=True)

    csv = full_sheet_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📄 Download Selected Items Measurement Sheet (CSV)",
        data=csv,
        file_name=f"{project_name}_Selected_Measurement_Sheet.csv",
        mime="text/csv",
    )
else:
    st.info("⚠️ မည်သည့် Item မှ ရွေးချယ်မထားပါ (All items are excluded).")
