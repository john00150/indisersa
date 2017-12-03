#encoding: utf-8

host = 'indisersa.database.windows.net'
username = 'otto'
password = 'Knoke@1958'
database = 'hotel_Info'

dates = [15, 30, 60, 90, 120]

cities = [
    'Guatemala City, Guatemala',
    'Antigua Guatemala, Guatemala',
]

scrapers = [
#    {'path': 'C:\users\indisersa\Desktop\hotels\scrapers\marriott_scraper.py', 'name': 'marriott_scraper'},
    {'path': 'C:\users\indisersa\Desktop\hotels\scrapers\\radisson_scraper.py', 'name': 'radisson_scraper'},
    {'path': 'C:\users\indisersa\Desktop\hotels\scrapers\lodebernal_scraper.py', 'name': 'lodebernal_scraper'},
    {'path': 'C:\users\indisersa\Desktop\hotels\scrapers\\bestday_scraper.py', 'name': 'bestbay_scraper'},
    {'path': 'C:\users\indisersa\Desktop\hotels\scrapers\despegar_scraper.py', 'name': 'despegar_scraper'},
    {'path': 'C:\users\indisersa\Desktop\hotels\scrapers\elconventoantigua_scraper.py', 'name': 'elconventoantigua_scraper'},
    {'path': 'C:\users\indisersa\Desktop\hotels\scrapers\expedia_scraper.py', 'name': 'expedian_scraper'},
    {'path': 'C:\users\indisersa\Desktop\hotels\scrapers\\book_hotel_beds_scraper.py', 'name': 'book_hotel_beds_scraper'},
    {'path': 'C:\users\indisersa\Desktop\hotels\scrapers\hotels_scraper.py', 'name': 'hotels_scraper'},
    {'path': 'C:\users\indisersa\Desktop\hotels\scrapers\\booking_scraper.py', 'name': 'booking_scraper'},
]

log_path = 'C:\users\indisersa\Desktop\hotels\logs\launcher.log'


