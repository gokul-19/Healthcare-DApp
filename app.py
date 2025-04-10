import streamlit as st
from Functions.provider import Provider
import json
from web3 import Web3

# Load ABI
with open("Assets/ProviderCompiled.json", "r") as f:
    ProviderCompiled = json.load(f)

# Blockchain account config (replace your address/private key!)
address = "0x66aB6D9362d4F35596279692F0251Db635165871"
private_key = "0xbbfbee4961061d506ffbb11dfea64eba16355cbf1d9c29613126ba7fec0aed5d"

provider = Provider(address, ProviderCompiled, private_key)

# Streamlit UI
st.set_page_config(page_title="Blockchain Healthcare", layout="centered")
st.title("🩺 Healthcare on Blockchain")

menu = st.sidebar.selectbox("Choose Role", ["Register Report", "View Report"])

if menu == "Register Report":
    st.subheader("📥 Register Patient Report")

    patient_address = st.text_input("Patient Wallet Address")
    report_data = st.text_area("Enter Medical Report")

    if st.button("Register"):
        if patient_address and report_data:
            hash_val = Web3.keccak(text=report_data).hex()
            receipt = provider.register_patient_record(patient_address, hash_val)
            st.success(f"✅ Report stored. Tx Hash: {receipt.transactionHash.hex()}")
        else:
            st.warning("Please enter all fields.")

elif menu == "View Report":
    st.subheader("📂 View Patient Report")
    search_address = st.text_input("Enter Patient Wallet Address")

    if st.button("Fetch Report"):
        if search_address:
            report_hash = provider.get_patient_record(search_address)
            st.info(f"Stored Report Hash: {report_hash}")
        else:
            st.warning("Enter a wallet address.")
