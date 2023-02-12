# Streamlit automatization app for booking and quotes

## Introduction

This **streamlit app** improves and makes considerably quicker the process of answering bookings and quote requests by automating all tasks that don't require any input. By reducing the amount of inputs that needs to be filled (most of them are really a *copy-paste* of the info provided by the customer when making the booking (i.e. quote) request), the time taken to answer a booking can be reduced from ~4 minutes to ~20 seconds

## How does it works?

The project structure is defined as follows:

The user interacts with the `streamlit app` where a coustomized UI allows the user to access all bookings and quotes requests and answer them by providing the needed imputs.

The `streamlit app` connects with the `outlook` module with implements all necessary functions needed to retrieve unread bookings and quotes from the outlook account, store the info of those emails as an instance of a `booking` or `quote` class and store them in an array of *unread bookings and quotes* that can be then accessed by the `streamlit app`. Moreover, it implements those functions needed to send the message once all necessary info has been inputed by the user.

The `outlook` module interacts with the `templates` module witch is in charge of creating the email body. The `templates` module implements a set of functions whose purpouse is to format the correct HTML file wich is also connected to its own CSS file. These HTML files act as templates and they provide email templates for accepting and rejecting a booking and answering a quote in English, German and Spanish.


## Code and modules
Definition of main functions and data structures for each module

### Booking and quote classes

Any instance of a booking or quote class holds all the information related to one particular request (i.e. booking or quote). Some of this data is extracted from the email sent by the customer through the available form in the website and the remaining data is either imputed by the user or calculated using the user inputs (i.e. prices)

The `Booking` class is defined as:

```python
@dataclass
class Booking:
	booking_number: str
	name: str
	fullname: str
	email: str
	phone: str
	pax: int
	pick_up_arrival: str
	destination_arrival: str
	arrival_date: str
	arrival_time: str
	flight_n_arrival: str
	pick_up_departure: str
	destination_departure: str
	departure_date: str
	pick_up_time: str
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

```

Where:
  - `booking_number` identifies every booking via a unique ID and it must be provided by the user when answering the booking4
  - `name`, `fullname`, `email` and `phone` contain the customer info and are extracted from the received email.
  - `pax` is the number of passengers of the requested transfer
  - `pick_up_arrival`, `destination_arrival`, `arrival_date`, `arrival_time`, `flight_n_arrival` are all provided by the user and represents the details of the arrival transfer if the user has requested a *round transfer* or the *one-way* transfer information otherwise.
