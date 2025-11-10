import streamlit as st
import pandas as pd
import os
import base64

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="💧 Monthly Consumption Tracker", layout="wide")

# ---------------------------------------------------------
# BACKGROUND IMAGE
# ---------------------------------------------------------
def set_background(image_file=None):
    if image_file and os.path.exists(image_file):
        with open(image_file, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        css = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """
    else:
        css = """
        <style>
        .stApp {
            background: linear-gradient(135deg, #0078D7, #00C9A7);
            background-size: cover;
        }
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)

set_background("background/bg.jpg")

# ---------------------------------------------------------
# PAGE STYLE
# ---------------------------------------------------------
st.markdown("""
<style>
.glass-card {
    background: rgba(255,255,255,0.9);
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}
.sidebar-title {
    font-size: 1.3rem;
    font-weight: bold;
    color: #00C9A7;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.markdown("<h1 style='text-align:center; color:white;'>💧 Monthly Water Consumption Tracker</h1>", unsafe_allow_html=True)

# ---------------------------------------------------------
# DATA DIRECTORY
# ---------------------------------------------------------
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# ---------------------------------------------------------
# SIDEBAR MENU
# ---------------------------------------------------------
st.sidebar.markdown("<p class='sidebar-title'>🏠 Main Menu</p>", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "Navigate:",
    ["🏡 Home", "📋 Manage Data", "💾 Saved Files", "📊 Compare Months", "ℹ️ About App"],
    label_visibility="collapsed"
)

# ---------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------
if menu == "🏡 Home":
    st.image("background/businessman.jpg", use_column_width=True)
    st.markdown("""
    <div class='glass-card'>
        <h2>Welcome to the Monthly Water Consumption Tracker 💧</h2>
        <p>This app helps you record, calculate, and track monthly water consumption for your company.</p>
        <ul>
            <li>Create and manage company/monthly records.</li>
            <li>Auto-calculate totals, payments, and balances.</li>
            <li>Compare performance between months.</li>
            <li>Save and re-open any previous month's data.</li>
        </ul>
        <p style='color:gray;'>Click <b>📋 Manage Data</b> on the left sidebar to get started.</p>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# MANAGE DATA PAGE
# ---------------------------------------------------------
elif menu == "📋 Manage Data":
    st.sidebar.markdown("---")
    st.sidebar.subheader("📅 Data Setup")
    company = st.sidebar.text_input("Company Name:", "Kitengela")
    month = st.sidebar.text_input("Month & Year (e.g., August 2025):", "August 2025")

    file_name = f"{company}_{month.replace(' ', '_')}.csv"
    file_path = os.path.join(DATA_DIR, file_name)

    columns = ["No.", "Name", "Current", "Old Meter", "New Meter", "1st Total", "Rate", "2nd Total", "Amount Paid", "Balance"]

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        st.success(f"✅ Loaded existing data for {company} - {month}")
    else:
        df = pd.DataFrame(columns=columns)
        st.info(f"🆕 No existing data found for {company} - {month}. You can start entering new data below.")

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader(f"📋 {company} — {month} Data Table")

    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        key="editor"
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # Auto calculations
    if not edited_df.empty:
        for col in ["Old Meter", "New Meter", "Rate", "Amount Paid", "1st Total", "2nd Total", "Current"]:
            edited_df[col] = pd.to_numeric(edited_df[col], errors="coerce").fillna(0)

        edited_df["1st Total"] = edited_df["New Meter"] - edited_df["Old Meter"]
        edited_df["2nd Total"] = edited_df["1st Total"] * edited_df["Rate"]
        edited_df["Balance"] = edited_df["2nd Total"] - edited_df["Amount Paid"]

        total_sales = edited_df["2nd Total"].sum()
        st.metric("💰 Total Monthly Sales", f"{total_sales:,.2f}")

    # Buttons
    st.sidebar.markdown("---")
    if st.sidebar.button("💾 Save File"):
        edited_df.to_csv(file_path, index=False)
        st.success(f"✅ File saved: {file_name}")

    if st.sidebar.button("🆕 New Month"):
        df = pd.DataFrame(columns=columns)
        st.session_state.editor = df
        st.info("🆕 New blank month created.")
        st.rerun()

# ---------------------------------------------------------
# SAVED FILES PAGE
# ---------------------------------------------------------
elif menu == "💾 Saved Files":
    st.subheader("📂 Saved Files")
    files = [f for f in os.listdir(DATA_DIR) if f.endswith(".csv")]

    if not files:
        st.info("No saved files found yet.")
    else:
        selected = st.selectbox("Select a saved file to open:", files)
        if st.button("📂 Open File"):
            file_path = os.path.join(DATA_DIR, selected)
            df = pd.read_csv(file_path)

            st.success(f"✅ Opened file: {selected}")
            st.data_editor(df, num_rows="dynamic", use_container_width=True, key="saved_view")

            # Show total calculation
            if "2nd Total" in df.columns:
                total_sales = df["2nd Total"].sum()
                st.metric("💰 Total Monthly Sales", f"{total_sales:,.2f}")

# ---------------------------------------------------------
# COMPARE MONTHS PAGE
# ---------------------------------------------------------
elif menu == "📊 Compare Months":
    st.subheader("📊 Compare Saved Months")
    files = [f for f in os.listdir(DATA_DIR) if f.endswith(".csv")]
    if len(files) < 2:
        st.warning("You need at least 2 saved months to compare.")
    else:
        c1, c2 = st.columns(2)
        with c1:
            f1 = st.selectbox("Select First Month", files, key="cmp1")
        with c2:
            f2 = st.selectbox("Select Second Month", files, key="cmp2")

        if st.button("🔍 Compare Now"):
            df1 = pd.read_csv(os.path.join(DATA_DIR, f1))
            df2 = pd.read_csv(os.path.join(DATA_DIR, f2))

            t1 = df1["2nd Total"].sum()
            t2 = df2["2nd Total"].sum()

            diff = t2 - t1
            st.write(f"💧 **{f1}:** {t1:,.2f}")
            st.write(f"💧 **{f2}:** {t2:,.2f}")
            st.write(f"📈 **Change:** {diff:,.2f}")

            st.bar_chart(pd.DataFrame({
                "Month": [f1, f2],
                "Total Sales": [t1, t2]
            }).set_index("Month"))

# ---------------------------------------------------------
# ABOUT PAGE
# ---------------------------------------------------------
elif menu == "ℹ️ About App":
    st.markdown("""
    <div class='glass-card'>
        <h2>About This App 💧</h2>
        <p>The <b>Monthly Water Consumption Tracker</b> was created to help small businesses or water supply companies easily manage meter readings and track monthly water sales.</p>
        <p>Developed by <b>Eudes</b> — powered by Streamlit.</p>
        <p>Version 2.0 — Enhanced Excel-style editing, data saving, and comparison features.</p>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown("<p style='text-align:center;color:white;'>Created by Eudes 💧 | Business Dashboard Edition</p>", unsafe_allow_html=True)

