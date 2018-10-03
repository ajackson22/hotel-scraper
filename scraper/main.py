import datetime
from datetime import timedelta

from scraper.data_store import create_hotel_entry, store_availability
from scraper.hotel_scraper import find_availability

today = datetime.datetime.now()

checkin = today.date()
checkout = today.date() + timedelta(days=1)

start_date = today
end_date = start_date + timedelta(days=1)
d = start_date

hotel_brand = 'IHG'

create_hotel_entry(hotel_brand)

while d < end_date:
    d += timedelta(days=1)
    checkin = d
    checkout = checkin + timedelta(days=1)
    availability = find_availability(checkin.date(), checkout.date(), 'Bora%20Bora,%20French%20Polynesia')

    # store_availability(hotel_brand, str(checkin.date()), availability)



