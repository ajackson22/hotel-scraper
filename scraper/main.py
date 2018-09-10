import datetime
from datetime import timedelta
from scraper.data_store import store_availability, check_current_date
from scraper.hotel_scraper import find_availability

today = datetime.datetime.now()

checkin = today.date()
checkout = today.date() + timedelta(days=1)

start_date = today
end_date = start_date + timedelta(days=2)
d = start_date
while d < end_date:
    d += timedelta(days=1)
    checkin = d
    checkout = checkin + timedelta(days=1)
    availability = find_availability(checkin.date(), checkout.date(), 'Bora%20Bora,%20French%20Polynesia')
    previous_availabilty = check_current_date(str(checkin.date()))

    if (previous_availabilty):
        for avail in availability:
            if (previous_availabilty[avail] == availability[avail]):
                print(avail + ": Equal")
            else:
                print(avail + ": Not Equal")

    store_availability(checkin.date(), availability)
    # for hn in availability:
    #     print("\t" + hn + " - " + availability[hn])


