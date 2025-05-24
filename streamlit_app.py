import streamlit as st
from math import pow
from PIL import Image

# Load and show the logo
logo = Image.open("nexcap_logo.png")
st.image(logo, width=300)  # Increased width for better visibility

st.title("NCL Reverse Mortgage Calc")

# Inputs
target_payment = st.number_input("Target Monthly Payment ($)", value=3000)
down_payment = st.number_input("Down Payment ($)", value=60000)
tax_rate = st.number_input("Property Tax Rate (%)", value=2.5)
insurance = st.number_input("Monthly Homeowner's Insurance ($)", value=100)
hoa = st.number_input("Monthly HOA Dues ($)", value=50)
interest_rate = st.number_input("Interest Rate (%)", value=6.5)

def calculate_purchase_price():
    monthly_interest = interest_rate / 100 / 12
    num_payments = 30 * 12

    def monthly_pi(loan_amt):
        if monthly_interest == 0:
            return loan_amt / num_payments
        return loan_amt * (monthly_interest * pow(1 + monthly_interest, num_payments)) / \
               (pow(1 + monthly_interest, num_payments) - 1)

    low = down_payment
    high = 2_000_000
    tolerance = 1

    while low < high:
        mid = (low + high) / 2
        loan_amt = mid - down_payment
        pi = monthly_pi(loan_amt)
        taxes = (mid * (tax_rate / 100)) / 12
        total = pi + taxes + insurance + hoa

        if abs(total - target_payment) <= tolerance:
            return round(mid, 2)
        elif total < target_payment:
            low = mid + tolerance
        else:
            high = mid - tolerance

    return round(low, 2)

if st.button("Calculate"):
    price = calculate_purchase_price()
    st.success(f"Estimated Maximum Purchase Price: **${price:,.2f}**")
