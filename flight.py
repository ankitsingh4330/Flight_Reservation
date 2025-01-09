import tkinter as tk
from tkinter import messagebox
from collections import deque

class FlightReservationSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Domestic Flight Reservation System")
        self.root.geometry("800x900")
        self.root.configure(bg="#f0f8ff")

    
        self.flights = {
            'AI 101 - Air India': {'from': 'Delhi', 'to': 'Mumbai', 'seats': 50, 'reserved': 0, 'price': 3500, 'waitlist': deque(), 'seats_avail': [True] * 50},
            'AI 202 - Air India': {'from': 'Mumbai', 'to': 'Bangalore', 'seats': 45, 'reserved': 0, 'price': 4500, 'waitlist': deque(), 'seats_avail': [True] * 45},
            'AI 303 - Air India': {'from': 'Bangalore', 'to': 'Chennai', 'seats': 40, 'reserved': 0, 'price': 3200, 'waitlist': deque(), 'seats_avail': [True] * 40},
            'AI 404 - Air India': {'from': 'Chennai', 'to': 'Kolkata', 'seats': 60, 'reserved': 0, 'price': 3800, 'waitlist': deque(), 'seats_avail': [True] * 60},
            'SG 505 - SpiceJet': {'from': 'Delhi', 'to': 'Goa', 'seats': 55, 'reserved': 0, 'price': 4200, 'waitlist': deque(), 'seats_avail': [True] * 55},
            'SG 606 - SpiceJet': {'from': 'Goa', 'to': 'Hyderabad', 'seats': 50, 'reserved': 0, 'price': 3100, 'waitlist': deque(), 'seats_avail': [True] * 50},
            '6E 707 - IndiGo': {'from': 'Hyderabad', 'to': 'Ahmedabad', 'seats': 48, 'reserved': 0, 'price': 2900, 'waitlist': deque(), 'seats_avail': [True] * 48},
            '6E 808 - IndiGo': {'from': 'Ahmedabad', 'to': 'Pune', 'seats': 45, 'reserved': 0, 'price': 3500, 'waitlist': deque(), 'seats_avail': [True] * 45},
            '6E 909 - IndiGo': {'from': 'Pune', 'to': 'Delhi', 'seats': 50, 'reserved': 0, 'price': 3700, 'waitlist': deque(), 'seats_avail': [True] * 50},
            'G8 1010 - GoAir': {'from': 'Kolkata', 'to': 'Delhi', 'seats': 60, 'reserved': 0, 'price': 4000, 'waitlist': deque(), 'seats_avail': [True] * 60},
            'G8 1111 - GoAir': {'from': 'Mumbai', 'to': 'Kochi', 'seats': 50, 'reserved': 0, 'price': 4500, 'waitlist': deque(), 'seats_avail': [True] * 50},
            'UK 1212 - Vistara': {'from': 'Delhi', 'to': 'Bangalore', 'seats': 55, 'reserved': 0, 'price': 4700, 'waitlist': deque(), 'seats_avail': [True] * 55},
            'UK 1313 - Vistara': {'from': 'Chennai', 'to': 'Mumbai', 'seats': 50, 'reserved': 0, 'price': 4400, 'waitlist': deque(), 'seats_avail': [True] * 50},
            'IX 1414 - Air India Express': {'from': 'Delhi', 'to': 'Lucknow', 'seats': 40, 'reserved': 0, 'price': 2600, 'waitlist': deque(), 'seats_avail': [True] * 40},
            'IX 1515 - Air India Express': {'from': 'Lucknow', 'to': 'Varanasi', 'seats': 45, 'reserved': 0, 'price': 2200, 'waitlist': deque(), 'seats_avail': [True] * 45},
            'SG 1616 - SpiceJet': {'from': 'Delhi', 'to': 'Jaipur', 'seats': 40, 'reserved': 0, 'price': 2000, 'waitlist': deque(), 'seats_avail': [True] * 40},
            '6E 1717 - IndiGo': {'from': 'Jaipur', 'to': 'Surat', 'seats': 38, 'reserved': 0, 'price': 2400, 'waitlist': deque(), 'seats_avail': [True] * 38},
            'AI 1818 - Air India': {'from': 'Surat', 'to': 'Mumbai', 'seats': 50, 'reserved': 0, 'price': 2800, 'waitlist': deque(), 'seats_avail': [True] * 50},
        }

        self.cancel_stack = []
        self.selected_seats = []  
        self.selected_flight = None

        
        self.create_widgets()

    def create_widgets(self):
        
        self.title_label = tk.Label(self.root, text="Domestic Flight Reservation System", font=('Helvetica', 18, 'bold'), bg="#4682b4", fg="white")
        self.title_label.pack(pady=10, fill=tk.X)

        
        self.flight_listbox = tk.Listbox(self.root, height=10, width=50, font=('Helvetica', 12), bg="#f0f8ff", fg="#00008b", selectbackground="#6495ed", selectforeground="white")
        self.flight_listbox.pack(pady=10)
        self.update_flight_listbox()

        
        self.book_button = tk.Button(self.root, text="Book Flight", width=20, font=('Helvetica', 12), bg="#32cd32", fg="white", command=self.book_flight)
        self.book_button.pack(pady=5)

        self.cancel_button = tk.Button(self.root, text="Cancel Last Booking", width=20, font=('Helvetica', 12), bg="#dc143c", fg="white", command=self.cancel_booking)
        self.cancel_button.pack(pady=5)

        
        self.info_label = tk.Label(self.root, text="Select a flight to view details and seat layout", font=('Helvetica', 12, 'italic'), bg="#f0f8ff", fg="#00008b")
        self.info_label.pack(pady=10)

        
        self.details_label = tk.Label(self.root, text="", font=('Helvetica', 12), bg="#f0f8ff", fg="#00008b", justify='left')
        self.details_label.pack(pady=10)

        
        self.seat_frame = tk.Frame(self.root, bg="#f0f8ff")
        self.seat_frame.pack(pady=10)

        
        self.flight_listbox.bind("<<ListboxSelect>>", self.display_flight_details)

    def update_flight_listbox(self):
        self.flight_listbox.delete(0, tk.END)
        for flight_name in self.flights:
            self.flight_listbox.insert(tk.END, flight_name)

    def display_flight_details(self, event):
        selected_index = self.flight_listbox.curselection()
        if selected_index:
            self.selected_flight = self.flight_listbox.get(selected_index)
            flight_info = self.flights[self.selected_flight]

            available_seats = flight_info['seats'] - flight_info['reserved']
            details = (
                f"From: {flight_info['from']}\n"
                f"To: {flight_info['to']}\n"
                f"Seats Available: {available_seats}\n"
                f"Price: ₹{flight_info['price']}\n"
            )
            self.details_label.config(text=details)
            self.display_seat_layout(flight_info)

    def display_seat_layout(self, flight_info):
        for widget in self.seat_frame.winfo_children():
            widget.destroy()

        for i in range(flight_info['seats']):
            status = flight_info['seats_avail'][i]
            color = "green" if status else "red"
            seat_button = tk.Button(self.seat_frame, text=str(i + 1), bg=color, fg="white", width=4, height=2,
                                     command=lambda i=i: self.select_seat(i + 1, flight_info))
            seat_button.grid(row=i // 10, column=i % 10, padx=5, pady=5)

    def select_seat(self, seat_number, flight_info):
        if seat_number in self.selected_seats:
            self.selected_seats.remove(seat_number)
            messagebox.showinfo("Seat Deselected", f"Seat {seat_number} deselected.")
        else:
            if len(self.selected_seats) < 8:
                if flight_info['seats_avail'][seat_number - 1]:
                    self.selected_seats.append(seat_number)
                    messagebox.showinfo("Seat Selected", f"Seat {seat_number} selected for booking.")
                else:
                    messagebox.showwarning("Seat Unavailable", f"Seat {seat_number} is already booked.")
            else:
                messagebox.showwarning("Selection Limit", "You can select up to 8 seats at a time.")

    def book_flight(self):
        if not self.selected_flight or not self.selected_seats:
            messagebox.showwarning("Booking Error", "Please select a flight and seats to book.")
            return

        flight_info = self.flights[self.selected_flight]
        booked_seats = []
        for seat_number in self.selected_seats:
            if flight_info['seats_avail'][seat_number - 1]:
                flight_info['seats_avail'][seat_number - 1] = False
                flight_info['reserved'] += 1
                self.cancel_stack.append(('book', self.selected_flight, seat_number))
                booked_seats.append(seat_number)
            else:
                messagebox.showwarning("Seat Unavailable", f"Seat {seat_number} is already booked.")

        if booked_seats:
            messagebox.showinfo("Booking Successful", f"Seats {', '.join(map(str, booked_seats))} booked successfully!")
            self.selected_seats.clear()
            self.display_seat_layout(flight_info)

    def cancel_booking(self):
        if self.cancel_stack:
            operation, flight, seat_number = self.cancel_stack.pop()
            if operation == 'book':
                self.flights[flight]['seats_avail'][seat_number - 1] = True
                self.flights[flight]['reserved'] -= 1
                messagebox.showinfo("Cancellation Successful", f"Booking for seat {seat_number} on {flight} has been cancelled.")
                self.display_seat_layout(self.flights[flight])
        else:
            messagebox.showwarning("Error", "No bookings to cancel.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FlightReservationSystem(root)
    root.mainloop()
