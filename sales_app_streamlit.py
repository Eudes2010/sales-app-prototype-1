import streamlit as st

st.title("💰 Sales Management App")

if "sales_data" not in st.session_state:
    st.session_state.sales_data = {}

st.subheader("Add a New Person")
new_name = st.text_input("Enter name:")

if st.button("Add Person"):
    if new_name:
        st.session_state.sales_data[new_name] = 0
        st.success(f"{new_name} added successfully!")

st.subheader("Enter Sales")
selected_name = st.selectbox("Choose a person:", list(st.session_state.sales_data.keys()))

sales_amount = st.number_input("Enter sales amount:", min_value=0.0)

if st.button("Save Sale"):
    st.session_state.sales_data[selected_name] += sales_amount
    st.success(f"Recorded {sales_amount} for {selected_name}")

st.subheader("Sales Summary")
for name, total in st.session_state.sales_data.items():
    st.write(f"{name}: ${total:.2f}")

total_sales = sum(st.session_state.sales_data.values())
st.metric("Total Sales", f"${total_sales:.2f}")
