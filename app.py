import io
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Detail Measurement & Estimator", page_icon="🏗️", layout="wide"
)

st.title("🏗️ Detail Measurement & Quantity Estimator")
st.caption("Project: Two Storeyed RCC Building | Location: Pyin Oo Lwin")

# Session state မှာ Table Data ကို သိမ်းဆည်းရန် Initialize လုပ်ခြင်း
if "measurement_data" not in st.session_state:
    st.session_state.measurement_data = pd.DataFrame(
        columns=[
            "Item No",
            "Particular",
            "Nos",
            "L (ft)",
            "B (ft)",
            "H (ft)",
            "Quantity",
            "Unit",
            "Unit Price (MMK)",
            "Total Amount (MMK)",
        ]
    )

# ---------------------------------------------------------
# Sidebar - Input Form (အချက်အလက်များ ရိုက်ထည့်ရန်နေရာ)
# ---------------------------------------------------------
st.sidebar.header("📝 Measurement Input")

with st.sidebar.form("input_form", clear_on_submit=True):
    item_no = st.number_input("Item No.", min_value=1, step=1, value=1)
    particular = st.text_input(
        "Particular (လုပ်ငန်းအမျိုးအမည်)",
        placeholder="e.g. F1 Footing Excavation",
    )

    col1, col2 = st.columns(2)
    nos = col1.number_input("Nos (အရေအတွက်)", min_value=1.0, value=1.0, step=1.0)
    unit = col2.selectbox("Unit (ယူနစ်)", ["Cuft", "Sqft", "Rft", "Nos"])

    col_l, col_b, col_h = st.columns(3)
    length = col_l.number_input("L - Length (ft)", min_value=0.0, value=0.0, step=0.1)
    width = col_b.number_input("B - Breadth (ft)", min_value=0.0, value=0.0, step=0.1)
    height = col_h.number_input("H - Height (ft)", min_value=0.0, value=0.0, step=0.1)

    unit_price = st.number_input(
        "Unit Price / Rate (MMK)", min_value=0.0, value=0.0, step=100.0
    )

    submitted = st.form_submit_button("➕ Add Item to Sheet")

    if submitted:
        if particular.strip() == "":
            st.error("ကျေးဇူးပြု၍ Particular (လုပ်ငန်းအမည်) ဖြည့်စွက်ပေးပါ။")
        else:
            # Dimension / Quantity Calculation Logic
            if unit == "Cuft":
                qty = nos * length * width * height
            elif unit == "Sqft":
                qty = (
                    nos * length * width
                    if width > 0
                    else nos * length * (height if height > 0 else 1.0)
                )
            elif unit == "Rft":
                qty = nos * length
            else:  # Nos
                qty = nos

            total_amount = qty * unit_price

            # Create new record
            new_data = {
                "Item No": item_no,
                "Particular": particular,
                "Nos": nos,
                "L (ft)": length,
                "B (ft)": width,
                "H (ft)": height,
                "Quantity": round(qty, 2),
                "Unit": unit,
                "Unit Price (MMK)": unit_price,
                "Total Amount (MMK)": round(total_amount, 2),
            }

            # Add to Session State DataFrame
            st.session_state.measurement_data = pd.concat(
                [
                    st.session_state.measurement_data,
                    pd.DataFrame([new_data]),
                ],
                ignore_index=True,
            )
            st.success(f"'{particular}' ကို ထည့်သွင်းပြီးပါပြီ။")

# ---------------------------------------------------------
# Main Page - Summary & Editable Data Table
# ---------------------------------------------------------
df = st.session_state.measurement_data

# Dashboard Metrics Summary
total_qty_cuft = df[df["Unit"] == "Cuft"]["Quantity"].sum()
total_qty_sqft = df[df["Unit"] == "Sqft"]["Quantity"].sum()
total_cost = df["Total Amount (MMK)"].sum()

m1, m2, m3 = st.columns(3)
m1.metric("Total Earthwork/Volume", f"{total_qty_cuft:,.2f} Cuft")
m2.metric("Total Area", f"{total_qty_sqft:,.2f} Sqft")
m3.metric("Estimated Total Cost", f"{total_cost:,.2f} MMK")

st.divider()

# Interactive & Editable Table
st.subheader("📋 Measurement & Cost Sheet")

if not df.empty:
    # ဇယားထဲမှာ တိုက်ရိုက် ပြင်ဆင်နိုင်အောင် Data Editor သုံးထားပါတယ်
    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        key="data_editor",
    )

    # ပြင်ဆင်လိုက်ပါက Quantity နှင့် Total Amount ကို ပြန်တွက်ပေးခြင်း
    edited_df["Quantity"] = edited_df.apply(
        lambda r: (
            r["Nos"] * r["L (ft)"] * r["B (ft)"] * r["H (ft)"]
            if r["Unit"] == "Cuft"
            else (
                r["Nos"] * r["L (ft)"] * r["B (ft)"]
                if r["Unit"] == "Sqft"
                else (r["Nos"] * r["L (ft)"] if r["Unit"] == "Rft" else r["Nos"])
            )
        ),
        axis=1,
    )
    edited_df["Total Amount (MMK)"] = (
        edited_df["Quantity"] * edited_df["Unit Price (MMK)"]
    )
    st.session_state.measurement_data = edited_df

    # Clear and Export Buttons
    col_btn1, col_btn2 = st.columns([1, 5])

    if col_btn1.button("🗑️ Clear All Data"):
        st.session_state.measurement_data = pd.DataFrame(
            columns=df.columns
        )
        st.rerun()

    # Excel Download Functionality
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        edited_df.to_excel(writer, index=False, sheet_name="Measurement Sheet")
    excel_data = output.getvalue()

    col_btn2.download_button(
        label="📥 Download Excel Sheet",
        data=excel_data,
        file_name="Detail_Measurement_Sheet.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

else:
    st.info(
        "👈 ဘယ်ဘက် Sidebar Form မှာ Measurement အချက်အလက်များ စတင်ထည့်သွင်းပါ။"
    )
