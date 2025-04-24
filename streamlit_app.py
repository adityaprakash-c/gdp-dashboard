import streamlit as st
from collections import deque

# Page Configuration
st.set_page_config(page_title="🚆 Railway Ticket Booking", layout="centered")

# Custom CSS for decoration
st.markdown("""
    <style>
        body {
            background-color: #f0f4f8;
            font-family: 'Arial', sans-serif;
        }
        .title {
            color: #2c3e50;
            font-size: 2.5em;
            font-weight: bold;
            text-align: center;
            margin-top: 30px;
        }
        .header {
            color: #2980b9;
            font-size: 1.5em;
            text-align: center;
            font-weight: bold;
        }
        .info {
            color: #8e44ad;
            text-align: center;
            font-size: 1.2em;
        }
        .tab-header {
            font-size: 1.3em;
            font-weight: bold;
            color: #2980b9;
        }
        .success {
            background-color: #27ae60;
            color: white;
            font-weight: bold;
            padding: 10px;
            border-radius: 5px;
            margin: 10px;
        }
        .warning {
            background-color: #f39c12;
            color: white;
            font-weight: bold;
            padding: 10px;
            border-radius: 5px;
            margin: 10px;
        }
        .error {
            background-color: #e74c3c;
            color: white;
            font-weight: bold;
            padding: 10px;
            border-radius: 5px;
            margin: 10px;
        }
        .button {
            background-color: #2980b9;
            color: white;
            font-weight: bold;
            border-radius: 5px;
            padding: 10px;
        }
        .button:hover {
            background-color: #3498db;
        }
        .seats {
            text-align: center;
            font-size: 1.1em;
        }
    </style>
""", unsafe_allow_html=True)

# Constants
ROWS = 5  # Number of coaches
COLS = 4  # Number of seats per coach
MAX_WAITLIST = 5  # Maximum number of people on the waitlist

# Initialize session state
if "seats" not in st.session_state:
    st.session_state.seats = [[None for _ in range(COLS)] for _ in range(ROWS)]  # Seat grid initialization
if "waitlist" not in st.session_state:
    st.session_state.waitlist = deque()  # Waitlist initialization

# Access session data
seats = st.session_state.seats
waitlist = st.session_state.waitlist

# Book ticket function
def book_ticket(name):
    for i in range(ROWS):
        for j in range(COLS):
            if seats[i][j] is None:  # Find the first empty seat
                seats[i][j] = name
                return f"✅ Seat booked: Coach {i+1} Seat {j+1}"
    if len(waitlist) < MAX_WAITLIST:
        waitlist.append(name)  # Add to waitlist if no seat available
        return f"🕒 Added to waitlist (position {len(waitlist)})"
    return "❌ No seats or waitlist spots available"

# Cancel ticket function
def cancel_ticket(name):
    for i in range(ROWS):
        for j in range(COLS):
            if seats[i][j] == name:  # Find the seat booked by the passenger
                seats[i][j] = None  # Free the seat
                msg = f"🗑️ Ticket cancelled for {name}"
                if waitlist:  # Promote the first person from the waitlist to the freed seat
                    next_passenger = waitlist.popleft()
                    seats[i][j] = next_passenger
                    msg += f"\n🎉 {next_passenger} promoted from waitlist"
                return msg
    if name in waitlist:
        waitlist.remove(name)  # Remove from waitlist if found
        return f"🗑️ Removed {name} from waitlist"
    return "❌ Name not found"

# Streamlit UI
st.markdown("<div class='title'>🚆 Railway Ticket Booking System</div>", unsafe_allow_html=True)
st.markdown("""
    <div class='header'>Aditya Prakash Swastik Singh</div>
    <div class='info'>MIT WPU Pune</div>
    <div class='info'>A simple seat booking simulation using DSA concepts.</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📥 Book", "🗑️ Cancel", "📋 View Status"])

# Tab 1: Book a seat
with tab1:
    st.markdown("<div class='tab-header'>Book a Seat</div>", unsafe_allow_html=True)
    name = st.text_input("Enter passenger name to book")
    if st.button("Book Seat", key="book_button"):
        if name:
            st.success(book_ticket(name))
        else:
            st.warning("Please enter a valid name.")

# Tab 2: Cancel a ticket
with tab2:
    st.markdown("<div class='tab-header'>Cancel a Ticket</div>", unsafe_allow_html=True)
    cname = st.text_input("Enter passenger name to cancel")
    if st.button("Cancel Ticket", key="cancel_button"):
        if cname:
            st.success(cancel_ticket(cname))
        else:
            st.warning("Please enter a valid name.")

# Tab 3: View seat and waitlist status
with tab3:
    st.markdown("<div class='tab-header'>Seat and Waitlist Status</div>", unsafe_allow_html=True)
    st.subheader("🚈 Seats (Coach x Seat):")
    for i in range(ROWS):
        cols = st.columns(COLS)
        for j in range(COLS):
            label = seats[i][j] if seats[i][j] else "🟩 Empty"  # Show seat status
            cols[j].button(label, key=f"{i}-{j}", disabled=True)

    st.subheader("📜 Waitlist:")
    if waitlist:
        for i, name in enumerate(waitlist, 1):
            st.write(f"{i}. {name}")
    else:
        st.write("Waitlist is empty.")
