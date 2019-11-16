import sqlite3
from sqlite3 import Error
import os
import PySimpleGUI as sg
from geopy import *
from geopy.distance import great_circle


class createReport:
    def __init__(self):
        print('Generating report')


    def createReportTemplate(self):
        report = "reportfile.html"
        html_default = """
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Quick Start - Leaflet</title>
                    <meta charset="utf-8" />
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <link rel="shortcut icon" type="image/x-icon" href="docs/images/favicon.ico" />
                    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.5.1/dist/leaflet.css" integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ==" crossorigin=""/>
                    <script src="https://unpkg.com/leaflet@1.5.1/dist/leaflet.js" integrity="sha512-GffPMF3RvMeYyc1LWMHtK8EbPv0iNZ8/oTtHPx9/cc2ILxQ+u905qIwdpULaqDkyBKgOaB57QTMg7ztg8Jm2Og==" crossorigin=""></script>
                </head>
                <body>
                
                <div id="mapid" style="width: 600px; height: 400px;"></div>
                <script>
                    var mymap = L.map('mapid').setView([51.505, -0.09], 13);
                    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
                        maxZoom: 18,
                        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
                            '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
                            'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                        id: 'mapbox.streets'
                    }).addTo(mymap);
                </script>
                </body>
                </html>
                """
        if os.path.exists(report):
            os.remove(report)
            report = open(report, "a")
            report.write(html_default)
            report.close()
        else:
            report = open(report, "a")
            report.write(html_default)
            report.close()


class sqlconnect:
    def __init__(self):
        print("init")

    # initiates connection to DB
    def create_connection(self):
        DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'chicagocrime.db')
        conn = None
        try:
            conn = sqlite3.connect(DEFAULT_PATH)
            print("Connected to DB successfully")
        except Error as e:
            print(e)
        return conn


    # Query Method for finding all items with a given IUCR record number
    def queryIUCR(self, conn, iucr_num):
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM crimes WHERE iucr LIKE {it}".format(it=iucr_num))
            ids = cursor.fetchall()
        return ids


class geolocater():
    def __init__(self):
        print("Creating Geolocater Unit")


    def getAddress(self, lat, long):
        geo = Nominatim(user_agent="ChicagoCrimeQuery")
        print("Attempting to find the closest street address for the lat / long pair: " + str(lat) + str(long))
        latlongstr = "" + str(lat) + "," + str(long) + ""
        location = geo.reverse(latlongstr)
        print("The address is: " + str(location))


    def getCoordinatePair(self, address):
        geo = Nominatim(user_agent="ChicagoCrimeQuery")
        print("Attempting to find the lat / long pair for the address given: ")
        location = geo.geocode(str(address))
        coord = "" + str(location.latitude) + ", " + str(location.longitude) + ""
        print("Coordinates: " + coord)


    def findDistance(self, start, finish):
        distance_mi = great_circle(start, finish).miles
        print(great_circle(start, finish).miles)
        return distance_mi



def main():
    #connobject = sqlconnect()
    #conn = connobject.create_connection()
    #with conn:
    #    crime_id = connobject.queryIUCR(conn, '0486')
    #    print(str(crime_id))

    new_report = createReport()
    new_report.createReportTemplate()


    newgeo = geolocater()
    newgeo.getAddress(33.9035792, -83.3390253)
    newgeo.getCoordinatePair("128, Milford Dr, Georgia, 30605")
    SIU = (37.7100209, -89.2247828)
    home_address = (33.9035792, -83.3390253)
    newgeo.findDistance(SIU, home_address)

    # Demo of how columns work
    # GUI has on row 1 a vertical slider followed by a COLUMN with 7 rows
    # Prior to the Column element, this layout was not possible
    # Columns layouts look identical to GUI layouts, they are a list of lists of elements.

    sg.ChangeLookAndFeel('BlueMono')

    #### Unique Value Counts -> Total: 1,456,715 ####
    # City Block -> 32,775
    # IUCR -> 366
    # Primary Type -> 34
    primaryTypeList = ["ALL OF THE ABOVE", "BATTERY", "PUBLIC PEACE VIOLATION","THEFT", "WEAPONS VIOLATION", "ROBBERY", "MOTOR VEHICLE THEFT",
                        "ASSAULT", "OTHER OFFENSE", "DECEPTIVE PRACTICE", "CRIMINAL DAMAGE", "CRIMINAL TRESPASS", "BURGLARY",
                       "STALKING", "CRIM SEXUAL ASSAULT", "NARCOTICS", "SEX OFFENSE", "OBSCENITY", "OFFENSE INVOLVING CHILDREN",
                       "KIDNAPPING", "HOMICIDE", "INTERFERENCE WITH PUBLIC OFFICER", "PROSTITUTION", "GAMBLING", "INTIMIDATION",
                       "ARSON", "LIQUOR LAW VIOLATION", "NON-CRIMINAL", "PUBLIC INDECENCY", "HUMAN TRAFFICKING", "CONCEALED CARRY LICENSE VIOLATION",
                       "NON - CRIMINAL", "OTHER NARCOTIC VIOLATION", "NON-CRIMINAL (SUBJECT SPECIFIED)"]
    # Description / Secondary Type -> 343
    # Beat -> 303
    # District -> 26
    # Latitude -> 368,078
    # Longitude -> 367,944

    # -- Column Layout -- #
    col = [[sg.Text('Input Date Range:', text_color='white'), sg.Input('Date Range', key='-date-')],
           [sg.Text('Select IUCR:', text_color='white'), sg.Input('Select IUCR', key='-iucr-')],
           [sg.Text('Select Primary Type:', text_color='white'), sg.OptionMenu(primaryTypeList, 'Select Primary Type')]
           ]

    col1 = [[sg.Text('Here you will input an address within Chicago city limits and a distance from this address:')],
        [sg.Text('Enter Desired Address:'), sg.Input('Address')],
        [sg.Text('Enter Distance (mi) from Address:'), sg.Input('Distance')]]


    # -- GUI Definition -- #
    layout = [[sg.Text('Select all options that will display when mapped.')],
              [sg.Listbox(values=('Case #', 'Date', 'Block', 'IUCR', 'Primary Type', 'Description', 'Beat', 'District', 'Latitude', 'Longitude'),
                          select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, no_scrollbar=True, size=(20, 12)), sg.Column(col), sg.Column(col1)],
              [sg.OK()]]


    # -- Window event loop -- #
    event, values = sg.Window('Chicago Crime Map', layout).Read()
    sg.popup('Values entered: ', event, values, values['-iucr-'], line_width=200)


if __name__ == '__main__':
    main()