from tinydb import TinyDB, Query

db = TinyDB('../resources/db.json')


def store_availability(date, avail_dic):
    table = db.table('ihg')
    avail_dic['_id'] = str(date)
    query = Query()
    results = db.table('ihg').search(query._id == date)
    if (db.table('ihg').contains(query._id == date, query.)):
        table.insert(avail_dic)


def check_current_date(date):
    results = db.table('ihg').search(query._id == date)
    if (results):
        return results[0]
