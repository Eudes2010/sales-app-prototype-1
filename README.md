mport streamlit as st

st.title("💰 Sales Management App")

if "sales_data" not in st.session_state:
    st.session_state.sales_data = {}

st.subheader("Add a New Person")
new_name = st.text_input("Enter name:")
if st.button("Add Person"):
    if new_name in st.session_state.sales_data:
        st.warning("Person already exists!")
    elif new_name.strip() == "":
        st.warning("Please enter a name.")
    else:
        st.session_state.sales_data[new_name] = []
        st.success(f"{new_name} added successfully!")

st.subheader("Record a Sale")
selected_name = st.selectbox("Select person:", [""] + list(st.session_state.sales_data.keys()))
sale_amount = st.number_input("Enter sale amount (Ksh):", min_value=0.0, step=0.01)
if st.button("Add Sale"):
    if selected_name:
        st.session_state.sales_data[selected_name].append(sale_amount)
        st.success(f"Added sale of Ksh {sale_amount} for {selected_name}")
    else:
        st.warning("Please select a person first.")

st.subheader("View Total Sales")
for name, sales in st.session_state.sales_data.items():
    total = sum(sales)
    st.write(f"**{name}** → Total Sales: Ksh {total}")

st.subheader("Edit Person’s Name")
old_name = st.selectbox("Select name to edit:", [""] + list(st.session_state.sales_data.keys()), key="edit_name")
new_name_edit = st.text_input("Enter new name:", key="new_name")
if st.button("Rename"):
    if old_name and new_name_edit:
        st.session_state.sales_data[new_name_edit] = st.session_state.sales_data.pop(old_name)
        st.success(f"Renamed {old_name} to {new_name_edit}")
