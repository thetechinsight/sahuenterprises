import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

# === Page Setup ===
st.set_page_config(page_title="Sahu Enterprises | GSTR-5 Summary Generator", layout="wide", page_icon="📄")

# === Custom CSS for Branding ===
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 1rem;
    }
    .title {
        color: #4AAFD5;
        text-align: center;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #91B187;
        margin-bottom: 2rem;
    }
    .footer {
        text-align: center;
        font-size: 0.9rem;
        color: gray;
        margin-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# === Header Section ===
import base64

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_base64 = get_base64_of_bin_file("logo.png")

st.markdown(
    f"""
    <div style="display:flex; align-items:center; justify-content:center; gap:15px;">
        <img src="data:image/png;base64,{logo_base64}" width="172">
        <div>
            <div class="title">Sahu Enterprises</div>
            <div class="subtitle">GSTR-5 Summary Generator</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.divider()

# === Helper Functions ===
def find_value_horizontal(df, keyword):
    for r in range(df.shape[0]):
        for c in range(df.shape[1]):
            cell = str(df.iat[r, c]).strip()
            if keyword.lower() in cell.lower():
                for nc in range(c + 1, df.shape[1]):
                    val = str(df.iat[r, nc]).strip()
                    if val:
                        return val
    return ""

def extract_invoice_data(file_path):
    try:
        df = pd.read_excel(file_path, header=None, usecols="A:N", nrows=140)
    except Exception as e:
        if "xlrd" in str(e).lower():
            df = pd.read_excel(file_path, header=None, usecols="A:N", nrows=140, engine="xlrd")
        else:
            raise

    df = df.fillna("")

    # Header fields
    date_val = find_value_horizontal(df, "Date")
    name_val = find_value_horizontal(df, "Name")
    gstno_val = find_value_horizontal(df, "GSTIN")
    bilno_val = find_value_horizontal(df, "Invoice No.")

    # Format date nicely (e.g. 30-06-2025)
    try:
        if isinstance(date_val, (pd.Timestamp, datetime)):
            date_val = date_val.strftime("%d-%m-%Y")
        else:
            parsed = pd.to_datetime(str(date_val), errors="coerce")
            if pd.notna(parsed):
                date_val = parsed.strftime("%d-%m-%Y")
    except Exception:
        pass

    # Table data
    item_rows = df.loc[19:60, [2, 4, 8, 13]]
    item_rows.columns = ["HSN", "Qty", "Taxable", "Total"]

    for col in ["Qty", "Taxable", "Total"]:
        item_rows[col] = (
            item_rows[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.extract(r"([\d.]+)")
            .fillna("0")
            .astype(float)
        )

    item_rows = item_rows[item_rows["HSN"].astype(str).str.strip() != ""]
    item_rows["HSN"] = item_rows["HSN"].astype(str).str.strip()

    grouped = item_rows.groupby("HSN", as_index=False)[["Qty", "Taxable", "Total"]].sum()

    records = []
    for _, row in grouped.iterrows():
        taxable = round(row["Taxable"], 2)
        total_amt = round(row["Total"], 2)
        tax_18 = round(total_amt - taxable, 2)

        rec = {
            "DATE": date_val,
            "NAME": name_val,
            "GSTNO": gstno_val,
            "BILNO": bilno_val,
            "Taxable Value": taxable,
            "TAX 18%": tax_18,
            "Total Amt": total_amt,
            "HSN CODE": row["HSN"],
            "Piece": int(row["Qty"]),
            "File": Path(file_path).name,
        }
        records.append(rec)

    return records


def summarize_files(uploaded_files):
    records = []
    for uploaded_file in uploaded_files:
        try:
            temp_path = Path("temp") / uploaded_file.name
            temp_path.parent.mkdir(exist_ok=True)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            recs = extract_invoice_data(temp_path)
            records.extend(recs)
            temp_path.unlink(missing_ok=True)
        except Exception as e:
            st.warning(f"⚠️ Error in {uploaded_file.name}: {e}")
    return pd.DataFrame(records)


# === Upload Section ===
st.markdown("#### 📂 Upload Your Invoice Files")
# st.markdown("Upload one or more **Tax Invoice** files below (supports both `.xls` and `.xlsx`).")

uploaded_files = st.file_uploader(
    "Select Invoice Files",
    type=["xls", "xlsx"],
    accept_multiple_files=True,
    help="Hold Ctrl (or ⌘ on Mac) to select multiple invoices."
)

# === Generate Summary ===
if st.button("🚀 Generate GSTR-5 Summary"):
    if not uploaded_files:
        st.error("Please upload at least one file.")
    else:
        st.info("Processing your invoices...")

        output_path = Path("GSTR5_Summary.xlsx")
        df = summarize_files(uploaded_files)

        if df.empty:
            st.error("No valid data found in uploaded files. Please check your invoices.")
        else:
            st.success("✅ GSTR-5 Summary generated successfully!")
            st.dataframe(df, use_container_width=True)

            with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Summary")

            with open(output_path, "rb") as f:
                st.download_button(
                    "⬇️ Download GSTR-5 Summary",
                    data=f,
                    file_name="GSTR5_Summary.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )

# === Footer ===
st.markdown("<div class='footer'>© 2025 Sahu Enterprises | Built with ❤️</div>", unsafe_allow_html=True)
