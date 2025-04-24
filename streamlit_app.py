import streamlit as st

class Train:
    def __init__(self, train_no, name, seats):
        self.train_no = train_no
        self.name = name
        self.seats = seats

class Passenger:
    def __init__(self, name):
        self.name = name
        self.next = None

class TicketBookingSystem:
    def __init__(self):
        self.trains = []
        self.head = None

    def add_train(self, train_no, name, seats):
        self.trains.append(Train(train_no, name, seats))
        self.trains.sort(key=lambda x: x.train_no)

    def search_train(self, train_no):
        low, high = 0, len(self.trains) - 1
        while low <= high:
            mid = (low + high) // 2
            if self.trains[mid].train_no == train_no:
                return self.trains[mid]
            elif self.trains[mid].train_no < train_no:
                low = mid + 1
            else:
                high = mid - 1
        return None

    def book_ticket(self, passenger_name):
        new_passenger = Passenger(passenger_name)
        if not self.head:
            self.head = new_passenger
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = new_passenger

    def cancel_ticket(self):
        if not self.head:
            return None
        cancelled_name = self.head.name
        self.head = self.head.next
        return cancelled_name

    def get_passenger_list(self):
        passengers = []
        temp = self.head
        while temp:
            passengers.append(temp.name)
            temp = temp.next
        return passengers

# Streamlit UI
st.title("🚆 Railway Ticket Booking System")
system = TicketBookingSystem()

# Add predefined trains
if 'initialized' not in st.session_state:
    system.add_train(101, "Pune Express", 100)
    system.add_train(202, "Delhi Shatabdi", 120)
    system.add_train(303, "Mumbai Local", 80)
    st.session_state.system = system
    st.session_state.initialized = True
else:
    system = st.session_state.system

menu = st.sidebar.selectbox("Choose Option", ["Search Train", "Book Ticket", "Cancel Ticket", "Show Passengers"])

if menu == "Search Train":
    train_no = st.number_input("Enter Train Number", step=1)
    if st.button("Search"):
        train = system.search_train(train_no)
        if train:
            st.success(f"Train Found: {train.name} with {train.seats} seats")
        else:
            st.error("Train not found.")

elif menu == "Book Ticket":
    name = st.text_input("Enter passenger name")
    if st.button("Book"):
        if name:
            system.book_ticket(name)
            st.success(f"Ticket booked for {name}")
        else:
            st.warning("Enter a valid name")

elif menu == "Cancel Ticket":
    if st.button("Cancel Ticket"):
        cancelled = system.cancel_ticket()
        if cancelled:
            st.success(f"Ticket cancelled for {cancelled}")
        else:
            st.warning("No bookings to cancel")

elif menu == "Show Passengers":
    passengers = system.get_passenger_list()
    if passengers:
        st.subheader("Passenger List")
        for p in passengers:
            st.write(f"- {p}")
    else:
        st.info("No passengers booked.")
