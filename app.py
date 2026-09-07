import streamlit as st
import datetime
from map_agent import run_commute_planner

st.title("🚗 AI Commute & Traffic Agent")
st.markdown("Enter your route details below to generate a live traffic and transit strategy.")

origin = st.text_input("Starting Point (Origin)", "Isnapur X Roads Hyderabad")
destination = st.text_input("Destination", "Ameerpet Hyderabad")
phone_number = st.text_input("WhatsApp Phone Number (with country code)", "+919392778715")

if st.button("🚀 Generate Commute Strategy"):
    if not origin or not destination:
        st.warning("Please fill in the origin and destination.")
    else:
        with st.spinner("Fetching live traffic data and generating AI travel strategy..."):
            commute_advice = run_commute_planner(origin=origin, destination=destination)
            
        st.success("✅ Travel strategy generated successfully!")
        
        st.markdown("### 📋 Live Agent Travel Strategy")
        st.write(commute_advice)
        
        # WhatsApp web link for cloud deployment
        import urllib.parse
        encoded_message = urllib.parse.quote(f"Here is my daily commute strategy:\n{commute_advice}")
        whatsapp_url = f"https://wa.me/{phone_number.replace('+', '')}?text={encoded_message}"
        
        st.markdown(f"### 📲 Send via WhatsApp")
        st.markdown(f"Click the button below to instantly open WhatsApp with your message ready to send:")
        st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="background-color:#25D366; color:white; padding:10px 20px; border:none; border-radius:5px; font-weight:bold; cursor:pointer;">💬 Open WhatsApp & Send</button></a>', unsafe_allow_html=True)
