import streamlit as st
import datetime
import pywhatkit as kit
from map_agent import run_commute_planner  # Imports your core logic function

# App Title & UI layout
st.title("🚗 AI Commute & Traffic Agent")
st.markdown("Enter your route details below to generate a live traffic strategy and send it via WhatsApp.")

# Input fields for the user
origin = st.text_input("Starting Point (Origin)", "Isanpur X Roads Hyderabad")
destination = st.text_input("Destination", "Secunderabad Railway Station Hyderabad")
phone_number = st.text_input("WhatsApp Phone Number (with country code)", "+917794862004")

if st.button("🚀 Generate & Send Commute Strategy"):
    if not origin or not destination or not phone_number:
        st.warning("Please fill in all the fields.")
    else:
        with st.spinner("Fetching live traffic data and generating AI travel strategy..."):
            # 1. Run your commute planner function and get the advice text
            commute_advice = run_commute_planner(origin=origin, destination=destination)
            
        st.success("✅ Travel strategy generated successfully!")
        
        # Display the output directly on the app screen
        st.markdown("### 📋 Live Agent Travel Strategy")
        st.write(commute_advice)
        
        # 2. Automatically queue and send via WhatsApp using pywhatkit
        now = datetime.datetime.now()
        target_hour = now.hour
        target_minute = now.minute + 2  # Sets it for 2 minutes from now
        
        if target_minute >= 60:
            target_minute -= 60
            target_hour = (target_hour + 1) % 24

        st.info(f"📲 Queuing WhatsApp message to send to {phone_number} at {target_hour:02d}:{target_minute:02d} (60s wait time)...")
        
        try:
            kit.sendwhatmsg(
                phone_no=phone_number, 
                message="Here is my daily commute strategy:\n" + commute_advice,
                time_hour=target_hour,
                time_min=target_minute,
                wait_time=60,
                tab_close=True
            )
            st.success("✅ WhatsApp message successfully queued!")
        except Exception as e:
            st.error(f"❌ Error queueing WhatsApp message: {e}")