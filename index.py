from datetime import datetime, timedelta

# Room Class
class Room:
    def __init__(self, room_number, rate_per_night):
        self.room_number = room_number
        # self.room_type = room_type
        self.rate_per_night = rate_per_night
        self.is_available = True

    def check_availability(self):
        return self.is_available

    def update_availability(self, status):
        self.is_available = status

    def get_room_details(self):
        return {
            'room_number': self.room_number,
            # 'room_type': self.room_type,
            'rate_per_night': self.rate_per_night,
            'is_available': self.is_available
        }
    
    def calculate_rate(self, num_of_nights):
        return num_of_nights * self.rate_per_night

class SingleRoom(Room):
    def __init__(self, room_number):
        super().__init__(room_number, rate_per_night=100)

class DoubleRoom(Room):
    def __init__(self, room_number):
        super().__init__(room_number, rate_per_night=150)

class Suite(Room):
    def __init__(self, room_number):
        super().__init__(room_number, rate_per_night=300)


# Guest Class
class Guest:
    def __init__(self, guest_name, contact_info):
        self.guest_name = guest_name
        self.contact_info = contact_info
        self.reservations = []

    def add_reservation(self, reservation):
        self.reservations.append(reservation)

    def view_reservations(self):
        return self.reservations

    def update_guest_details(self, guest_name=None, contact_info=None):
        if guest_name:
            self.guest_name = guest_name
        if contact_info:
            self.contact_info = contact_info


# Reservation Class
class Reservation:
    def __init__(self, reservation_id, guest, room, check_in, check_out):
        self.reservation_id = reservation_id
        self.guest = guest
        self.room = room
        self.check_in = check_in
        self.check_out = check_out
        self.total_cost = self.calculate_total_cost()
        guest.add_reservation(self)

    def calculate_total_cost(self):
        num_of_nights = (self.check_out - self.check_in).days
        return self.room.calculate_rate(num_of_nights)

    def modify_reservation(self, new_check_in=None, new_check_out=None):
        if new_check_in:
            self.check_in = new_check_in
        if new_check_out:
            self.check_out = new_check_out
        self.total_cost = self.calculate_total_cost()

    def cancel_reservation(self):
        self.room.update_availability(True)
        self.guest.reservations.remove(self)


# Hotel Class
class Hotel:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.rooms = []
        self.reservations = []

    def add_room(self, room):
        self.rooms.append(room)

    def remove_room(self, room_number):
        self.rooms = [room for room in self.rooms if room.room_number != room_number]

    def check_availability(self, room_type=None):
        available_rooms = [
            room for room in self.rooms if room.check_availability() and (isinstance(room, room_type) if room_type else True)
        ]
        return available_rooms

    def make_reservation(self, guest, room, check_in, check_out):
        if room in self.check_availability(type(room)):
            reservation_id = len(self.reservations) + 1
            reservation = Reservation(reservation_id, guest, room, check_in, check_out)
            self.reservations.append(reservation)
            return reservation
        else:
            raise Exception("Room is not available for the selected dates.")

    def get_reservation(self, reservation_id):
        for reservation in self.reservations:
            if reservation.reservation_id == reservation_id:
                return reservation
        return None

    def get_all_reservations(self):
        return self.reservations

    def get_occupancy_rate(self):
        occupied_rooms = len([room for room in self.rooms if not room.check_availability()])
        total_rooms = len(self.rooms)
        return (occupied_rooms / total_rooms) * 100 if total_rooms else 0

    def get_revenue_by_room_type(self):
        revenue_by_type = {}
        for reservation in self.reservations:
            room_type = type(reservation.room).__name__
            revenue_by_type[room_type] = revenue_by_type.get(room_type, 0) + reservation.total_cost
        return revenue_by_type
