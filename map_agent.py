import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize the Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Define your Google Maps tool function here (keep your existing implementation)
def check_live_traffic_and_routes(origin: str, destination: str) -> str:
    """Fetches live traffic and route data using Google Maps Directions API."""
    import requests
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        return "Error: GOOGLE_MAPS_API_KEY is missing in your .env file."
        
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&departure_time=now&key={api_key}"
    response = requests.get(url)
    return response.text

# Package the tool for Gemini
my_tools = [check_live_traffic_and_routes]

def run_commute_planner(origin: str, destination: str) -> str:
    """Queries Gemini with tools and returns the structured travel strategy text."""
    chat = client.chats.create(
        model='gemini-3.6-flash', # or your preferred model version
        config=types.GenerateContentConfig(
            tools=my_tools,
            temperature=0.3,
        )
    )

    query = (
        f"I am commuting from {origin} to {destination} today. "
        f"Check the live traffic using your Google Maps tool and local news for crowds, "
        f"then provide a structured travel strategy: Estimated Time, Potential Roadblocks, and Final Route Recommendation."
    )
    
    response = chat.send_message(query)
    
    # Crucial: Return the text so app.py can capture and display it
    return response.text

# Optional: If you still want to test map_agent.py directly from the terminal
if __name__ == "__main__":
    print(run_commute_planner(origin="Isanpur X Roads Hyderabad", destination="Secunderabad Railway Station Hyderabad"))