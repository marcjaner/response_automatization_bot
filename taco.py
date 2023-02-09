from dataclasses import dataclass

@dataclass
class VPT_booking:
	booking_number: str
	name: str
	fullname: str
	email: str
	phone: str
	qty_people: int
	pick_up_arrival: str
	destination_arrival: str
	arrival_date: str
	arrival_time: str
	flight_n_arrival: str
	pick_up_departure: str
	destination_departure: str
	departure_date: str
	departure_time: str
	flight_n_departure: str
	baby_seat: str
	child_seat: str
	origin: str
	city: str
	total: int
	subtotal_first: int
	subtotal_second: int
	subtotal_third: int
	language : str
	type_transf: str
	status: str
	body : str



def get_booking_class(booking_info: list)-> VPT_booking:
	""" creates an instance of the booking class from the info found in the auxiliary list created previously """
	aux_class = VPT_booking(None,)
	return aux_class


def main():
    f = open("mail.txt")
    aux_class = VPT_booking(None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
    m = [[]]
    for word in f: 
        coso = word.split(":")
        m.append(coso)
    aux_class = VPT_booking(None, m[2][1][1:-1], None, m[3][1][1:-1], m[5][1][1:-3],m[19][1][1:-3],m[8][1][1:-3].lower().capitalize(), m[12][1][1:-3].lower().capitalize(), m[7][1][1:-3],m[9][1][1:] + ":" + m[9][2][:-3], m[10][1][2:-3], m[16][1][2:-3],"Palma Airport", m[14][1][1:-3], m[15][1][2:] + ":" + m[15][2][:-3],m[17][1][2:-3],None,None, None, None, None, None, None, None, None, None, None, None)
    print(aux_class)

main()