from destination_data import Destination
from flight_search import FlightSearch
from datetime import datetime, timedelta

data_manager = Destination()
flight_search = FlightSearch()

ORIGIN_CITY_IATA = "LON"

# We determine the list of cities that we would like to visit.
sheet_data = data_manager.get_destination_data()

# Define the abbreviations of airports.
for row in sheet_data:
    if row['iataCode'] == '':
        row['iataCode'] = flight_search.get_destination_code(row['city'])

# We supplement the list of flights with previously defined codes.
data_manager.update_destination_codes()
# Updating the variable sheet_data for further use.
sheet_data = data_manager.get_destination_data()

# Creating a dictionary with directions.
destinations = {data["iataCode"]: {"id": data["id"], "city": data["city"], "price": data["lowestPrice"]} for data in
                sheet_data}

# Creating time limits for searching for tickets.
tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=6 * 30)

# Organize the search for air tickets according to our search parameters.
for destination_code in destinations:
    print(destination_code)
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination_code,
        from_time=tomorrow,
        to_time=six_month_from_today
    )
    print(flight.price)
    if flight is None:
        continue

    # Compare the real cost of air tickets with the desired one.
    if flight.price < destinations[destination_code]["price"]:
        users = data_manager.get_customer_emails()
        emails = [row["email"] for row in users]
        names = [row["firstName"] for row in users]

        message = f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."
print(message)