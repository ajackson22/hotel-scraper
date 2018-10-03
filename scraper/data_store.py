import sqlite3

conn = sqlite3.connect('../resources/hotels.db')

change_list = {}


def create_hotel_entry(hotel_brand):
    c = conn.cursor()

    command = "CREATE TABLE IF NOT EXISTS " + hotel_brand + " (date TEXT, hotel_name TEXT, points TEXT, PRIMARY KEY (date, hotel_name))"
    c.execute(command)


def check_existance(hotel_brand, date, hotel_name):
    c = conn.cursor()

    command = 'SELECT points FROM ' + hotel_brand + ' WHERE date=\'' + date + '\' AND hotel_name=\'' + hotel_name + '\''
    print(command)
    c.execute(command)

    row = c.fetchone()
    if (row):
        print(row[0])
        return row[0]
    return


def store_availability(hotel_brand, date, availabilty):
    c = conn.cursor()

    for hotel in availabilty:
        previous_db_value = check_existance(hotel_brand, date, hotel)
        if (previous_db_value):
            if (previous_db_value != availabilty[hotel]):
                change_alert(date, hotel, previous_db_value, availabilty[hotel])
                command = 'UPDATE ' + hotel_brand + ' SET points = \'' + availabilty[
                    hotel] + '\' WHERE date=\'' + date + '\' AND hotel_name=\'' + hotel + '\''
                print(command)
                c.execute(command)
                conn.commit()
        else:
            command = 'INSERT INTO ' + hotel_brand + ' VALUES (\'' + date + '\', \'' + hotel + '\', \'' + availabilty[
                hotel] + '\')'
            print(command)
            c.execute(command)
            conn.commit()


def change_alert(date, hotel_name, old_value, new_value):
    if (date not in change_list):
        change_list[date] = {}
    if (hotel_name not in change_list[date]):
        change_list[date][hotel_name] = {}
    change_list[date][hotel_name] = old_value + " -> " + new_value

    if (len(change_list.keys()) >= 7):
        print("Time to send alert!")
        print(change_list)
        change_list.clear()