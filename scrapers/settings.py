#encoding: utf-8
import socket, os

hostname = socket.gethostname()

host = 'indisersa.database.windows.net'
username = 'otto'
password = 'Knoke@1958'
database = 'hotel_Info'

dates = [15, 30, 60, 90, 120]

cities = [
    'Guatemala City, Guatemala',
    'Antigua Guatemala, Guatemala',
]

path = os.getcwd()
