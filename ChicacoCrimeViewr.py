import sqlite3
from sqlite3 import Error
import os
import PySimpleGUI as sg
from geopy import *
from geopy.distance import great_circle
import geopy.geocoders
import math
import re
import datetime


# TODO: Function to take a dictionary and create / return a SQL query from it
# Working example query: SELECT caseNumber, dateTime, latitude, longitude FROM crimes WHERE latitude <= 42.467514844927535 AND latitude >= 41.30809455507246;
# This is for address of Chicago City Hall (121 N LaSalle St Chicago Illinois 60602)[41.8878047, -87.6325199])
def genQuery(inputDictionary):
    column_name = ''
    filter_counter = 0
    main_query_string = ''
    listbox_length = len(inputDictionary['listbox'])
    listbox_counter = 1

    # Parse dictionary for filter items present
    # Items considered NULL or not given if set to 'None'
    # -- Find all columns the user has entered they want returned in query -- #
    if inputDictionary['listbox'] != 'None':
        for item in inputDictionary['listbox']:
            if item == 'IUCR':
                item = 'iucr'
            elif item == 'Case #':
                item = 'caseNumber'
            elif item == 'Date':
                item = 'dateTime'
            elif item == 'Primary Type':
                item = 'primaryType'
            elif item == 'Description':
                item = 'description'
            elif item == 'Block':
                item = 'streetBlock'
            elif item == 'Beat':
                item = 'beat'
            elif item == 'District':
                item = 'district'
            elif item == 'Latitude':
                item = 'latitude'
            elif item == 'Longitude':
                item = 'longitude'

            if listbox_counter < listbox_length:
                column_name += str(item) + ', '
                listbox_counter += 1
            else:
                column_name += str(item)
                listbox_counter += 1
    if inputDictionary['iucr'] != None:
        filter_counter += 1
        main_query_string += '(' + 'iucr = ' + str(inputDictionary['iucr']) + ')'
    if inputDictionary['address'] != None:
        if filter_counter >= 1:
            filter_counter += 1
            lat = inputDictionary['address']
            lat_minmax = lat[0]
            long_minmax = lat[1]
            lat_min = lat_minmax[0]
            lat_max = lat_minmax[1]
            long_min = long_minmax[0]
            long_max = long_minmax[1]

            print('lat min: ' + str(lat_min))
            print('lat max: ' + str(lat_max))
            print('long min: ' + str(long_min))
            print('long max: ' + str(long_max))

            main_query_string += ' AND ' + '(' + 'latitude >= ' + str(lat_min) + ') AND (' + 'latitude <= ' + str(lat_max) + ') AND (' + 'longitude >= ' + str(long_min) + ') AND (' + 'longitude <= ' + str(long_max) + ')'
        else:
            filter_counter += 1
            lat = inputDictionary['address']
            lat_minmax = lat[0]
            long_minmax = lat[1]
            lat_min = lat_minmax[0]
            lat_max = lat_minmax[1]
            long_min = long_minmax[0]
            long_max = long_minmax[1]
            main_query_string += ' (' + 'latitude >= ' + str(lat_min) + ') AND (' + 'latitude <= ' + str(lat_max) + ') AND (' + 'longitude >= ' + str(long_min) + ') AND (' + 'longitude <= ' + str(long_max) + ')'
    if inputDictionary['primaryType'] != None:
        if filter_counter >= 1:
            filter_counter += 1
            main_query_string += ' AND (primaryType LIKE ' + '\"' + str(inputDictionary['primaryType']) + '\"' + ')'
        else:
            filter_counter += 1
            main_query_string += ' primaryType LIKE ' + '\"' + str(inputDictionary['primaryType']) + '\"'
    if (inputDictionary['startdate'] != None) and (inputDictionary['enddate'] != None):
        # Max range of dates is: 1/1/2012 00:00:00.000 to 9/9/2016 23:57:00.000
        if filter_counter >= 1:
            filter_counter += 1
            main_query_string += ' AND (dateTime BETWEEN date(' + '\"' + str(inputDictionary['startdate']) + '\"' + ') AND date(' + '\"' + str(inputDictionary['enddate']) + '\"' + '))'
        else:
            filter_counter += 1
            main_query_string += 'Date BETWEEN date(' + str(inputDictionary['startdate']) + ') AND date(' + str(inputDictionary['enddate'])
    if filter_counter >= 1:
        main_query_string += ';'

    # TODO: run regex against basesqlquery to confirm if the last item before the closing parenthesis is a comma, if so: remove it
    if len(main_query_string) == 0:
        baseSqlQuery = "SELECT " + column_name + " FROM crimes"
    elif len(main_query_string) > 0:
        baseSqlQuery = "SELECT " + column_name + " FROM crimes WHERE" + main_query_string
    print("Testing SQLquery Builder: " + baseSqlQuery)

    return baseSqlQuery



class createReport:
    def __init__(self, provided_distance, coordinates):
        self.provided_dist = provided_distance
        self.coord = coordinates
        self.returned_results = ""

        pass


    def update_results(self, new_string):
        self.returned_results += new_string


    def createReportTemplate(self):
        report = "reportfile.html"
        pin_information = "<p>Hello world!<br />This is a nice popup.</p>"
        html_default_head = """
               
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Chicago Crimes 2012-2016 (Filtered Results)</title>
                    <meta charset="utf-8" />
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <link rel="shortcut icon" type="image/x-icon" href="docs/images/favicon.ico" />
                    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.5.1/dist/leaflet.css" integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ==" crossorigin=""/>
                    <script src="https://unpkg.com/leaflet@1.5.1/dist/leaflet.js" integrity="sha512-GffPMF3RvMeYyc1LWMHtK8EbPv0iNZ8/oTtHPx9/cc2ILxQ+u905qIwdpULaqDkyBKgOaB57QTMg7ztg8Jm2Og==" crossorigin=""></script>
                </head>
                <body>
                
                <div id="mapid" style="width: 1200px; height: 800px;"></div>
                
                """

        html_default_script = """
                <script>
                    // Variables for coordinates
                    var coordinates = {coord}

                    // Distance variables
                    var provided_distance = {provided_dist}
                    var distance_in_meters = (provided_distance * 1609.34)

                    // Map variables
                    var mymap = L.map('mapid').setView(coordinates, 11.35);
                    
                    """.format(coord = self.coord, provided_dist= self.provided_dist)

        html_default_script1 = """

                    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
                        maxZoom: 18,
                        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
                            '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
                            'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                        id: 'mapbox.streets'
                    }).addTo(mymap);

                    var LeafIcon = L.Icon.extend({
                        options: {
                            iconUrl: 'hacker.png',
                            iconAnchor:   [22, 94],
                            shadowAnchor: [4, 62],
                            popupAnchor:  [-3, -76]
                        }
                    });
                    
                    var HouseIcon = L.Icon.extend({
                        options: {
                            iconUrl: 'house.png',
                            iconAnchor:   [22, 94],
                            shadowAnchor: [4, 62],
                            popupAnchor:  [-3, -76]
                        }
                    });

                    // Types of icons
                    var defaultIcon = new LeafIcon({iconUrl: 'hacker.png'})
                    var homeIcon = new HouseIcon({iconUrl: 'house.png'})

                    // Draw the circle radius around the area of focus on the map
                    L.circle(coordinates, radius=distance_in_meters).addTo(mymap)

                    // Section to create the markers for each returned point from the Query
                    L.marker(coordinates, {iconAnchor: coordinates, icon: homeIcon}).bindPopup("<p>Hello world!<br />This is a nice popup.</p>").addTo(mymap);
                """


        html_default_script2 = """
                </script>
                </body>
                </html>
                """

        if os.path.exists(report):
            os.remove(report)
            report = open(report, "a")
            report.write(html_default_head + html_default_script + html_default_script1 + self.returned_results + html_default_script2)
            report.close()
        else:
            report = open(report, "a")
            report.write(html_default_head + html_default_script + html_default_script1 + self.returned_results + html_default_script2)
            report.close()


# -- Class for creation of the SQL connection and to handle querying from the DB for the given dataset -- #
class sqlconnect:
    def __init__(self):
        minMaxLat = []
        minMaxLong = []
        pass

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

    # -- Query to find all crimes in db within a given distance -- #
    # TODO: Takes a tuple(lat, long) and returns all rows containing lat / long pairs within a given user-provided radius
    def queryCrimesCloseToLatitude(self, conn, longPair, latPair):
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM crimes WHERE (Longitude <= {long} AND Longitude >= {long1}) AND (Latitude <= {lat} AND Latitude >= {lat1})").format(long=longPair[0], long1=longPair[1], lat=latPair[0], lat1=latPair[1])
            ids = cursor.fetchall()
        return ids


    # -- Query first 100 rows -- #
    def queryDefault(self, conn):
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM crimes LIMIT 100")
            ids = cursor.fetchall()
        return ids

    # -- Used to run query returned from genQuery -- #
    def queryGeneric(self, conn, gen_query):
        with conn:
            cursor = conn.cursor()
            cursor.execute(gen_query)
            ids = cursor.fetchall()
        return ids

    # Query All
    def queryAllDates(self, conn):
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT dateTime FROM crimes LIMIT -1 OFFSET 1")
            ids = cursor.fetchall()
        return ids


# -- Class for translation and calculation of geocoordinates and distance values -- #
class geolocater():
    def __init__(self):
        pass

    def getAddress(self, lat, long):
        geo = Nominatim(user_agent="ChicagoCrimeQuery")
        print("Attempting to find the closest street address for the lat / long pair: " + str(lat) + str(long))
        latlongstr = "" + str(lat) + "," + str(long) + ""
        location = geo.reverse(latlongstr)
        print("The address is: " + str(location))


    def getCoordinatePair(self, address):
        geopy.geocoders.options.default_timeout = 7
        geo = Nominatim(user_agent="ChicagoCrimeQuery1")
        location = geo.geocode(str(address))
        coord = []
        coord.append(location.latitude)
        coord.append(location.longitude)
        print("Translated Coordinates for address : (" + str(address) + ")"+ str(coord))

        return coord


    # -- Find the distance between a pair of tuples consisting of ints (latitude, longitude)-- #
    def findDistance(self, start, finish):
        distance_mi = great_circle(start, finish).miles
        print(great_circle(start, finish).miles)
        return distance_mi


    # TODO: F(x) to find all db entries that are within the provided distance from the user provided Chicago address:
    # -- Convert Lat / Long pair and radius in miles to find a distance from a given point in lat / long converted to miles
    def convertLLMiles(self, latLongPair, userMiles):
        # -- Static Items -- #
        equatorLongitude = 69.172  # 1 Degree of longitude is widest at the equator at 69.172 miles
        latRatio = 1 / 69  # 1 degree of latitude / ~69 miles

        # -- Gather the information from the input -- #
        latitude = latLongPair[0]
        longitude = latLongPair[1]

        # -- Make the conversion -- #
        latRadians = math.radians(latitude)
        latCosine = math.cos(latRadians)
        degreeAtLatitude = latCosine * equatorLongitude
        ratio = (1 / degreeAtLatitude)

        minLong = longitude - (userMiles * ratio)
        maxLong = longitude + (userMiles * ratio)
        minLat = latitude - (userMiles * latRatio)
        maxLat = latitude + (userMiles * latRatio)
        print('The longitude min-max is: ' + str(longitude - (userMiles * ratio)) + ' , ' + str(
            longitude + (userMiles * ratio)))
        print('The latitude min-max is: ' + str(latitude - (userMiles * latRatio)) + ' , ' + str(
            latitude + (userMiles * latRatio)))

        minMaxLat = [minLat, maxLat]
        minMaxLong = [minLong, maxLong]

        return minMaxLat, minMaxLong


def main():
    #newgeo = geolocater()
    #newgeo.getAddress(33.9035792, -83.3390253)
    #newgeo.getCoordinatePair("128, Milford Dr, Georgia, 30605")
    #newgeo.findDistance(SIU, home_address)

    # Testing conversion of lat/long pair to miles at given latitude
    #connobj = sqlconnect()
    #conn = connobj.create_connection()
    #with conn:
    #    connobj.convertLLMiles([37.26383, -83.3390153], 35)

    sg.ChangeLookAndFeel('BlueMono')

    #### Unique Value Counts -> Total: 1,456,715 ####
    # City Block -> 32,775
    # IUCR -> 366
    # Primary Type -> 34
    # Description / Secondary Type -> 343
    # Beat -> 303
    # District -> 26
    # Latitude -> 368,078
    # Longitude -> 367,944

    primaryTypeList = ["ALL OF THE ABOVE", "BATTERY", "PUBLIC PEACE VIOLATION","THEFT", "WEAPONS VIOLATION", "ROBBERY", "MOTOR VEHICLE THEFT",
                        "ASSAULT", "OTHER OFFENSE", "DECEPTIVE PRACTICE", "CRIMINAL DAMAGE", "CRIMINAL TRESPASS", "BURGLARY",
                       "STALKING", "CRIM SEXUAL ASSAULT", "NARCOTICS", "SEX OFFENSE", "OBSCENITY", "OFFENSE INVOLVING CHILDREN",
                       "KIDNAPPING", "HOMICIDE", "INTERFERENCE WITH PUBLIC OFFICER", "PROSTITUTION", "GAMBLING", "INTIMIDATION",
                       "ARSON", "LIQUOR LAW VIOLATION", "NON-CRIMINAL", "PUBLIC INDECENCY", "HUMAN TRAFFICKING", "CONCEALED CARRY LICENSE VIOLATION",
                       "NON - CRIMINAL", "OTHER NARCOTIC VIOLATION", "NON-CRIMINAL (SUBJECT SPECIFIED)"]

    # -- Column Layout -- #
    col = [[sg.Text('Date Range: ', text_color='white'), sg.CalendarButton('Start', key='-startdate-', default_date_m_d_y=(1, 1, 2012)), sg.CalendarButton('End', key='-enddate-', default_date_m_d_y=(5, 1, 2016))],
           [sg.Text('Select IUCR:', text_color='white'), sg.Input('Select IUCR', key='-iucr-')],
           [sg.Text('Select Primary Type:', text_color='white'), sg.OptionMenu(primaryTypeList, 'Select Primary Type', key='-primaryType-')]
           ]

    col1 = [[sg.Text('Here you will input an address within Chicago city limits and a distance from this address:')],
        [sg.Text('Enter Desired Address:'), sg.Input('Address', key='-address-')],
        [sg.Text('Enter Distance (mi) from Address:'), sg.Input('Distance', key='-distance-')]]


    # -- GUI Definition -- #
    layout = [[sg.Text('Select all options that will display when mapped.')],
              [sg.Listbox(default_values='None' , values=('Case #', 'Date', 'Block', 'IUCR', 'Primary Type', 'Description', 'Beat', 'District', 'Latitude', 'Longitude'),
                          select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, no_scrollbar=True, size=(20, 12), key='-listbox-'), sg.Column(col), sg.Column(col1)],
              [sg.Button('Submit')]]


    # -- Window event loop -- #
    #event, values = sg.Window('Chicago Crime Map', layout).Read()
    #sg.popup('Values entered: ', event, values, values['-iucr-'], line_width=200)

    # -- Testing -- #
    # STEP3 - the event loop
    window = sg.Window('Chicago Crime Map', layout)

    while True:
        event, values = window.read()  # Read the event that happened and the values dictionary
        if event in (None, 'Exit'):  # If user closeddow with X or if user clicked "Exit" button then exit
            break
        if event == 'Submit':
            print('You pressed the button')

            # -- Get information from the user's input once they press the Submit -- #
            queryStatement = []
            queryDict = dict(iucr = None, address = None, distance = None, primaryType = None, startdate = None, enddate = None)

            if values.get('-listbox-') != 'None':
                queryStatement.append((values['-listbox-']))
                if 'Longitude' not in values['-listbox-']:
                    #print("You didn't select longitude, we added it for you.") # TODO: Set to not force the long / lat where the user is aware
                    values['-listbox-'].append('Longitude')
                if 'Latitude' not in values['-listbox-']:
                    #print("You didn't select latitude, we added it for you.") # TODO: Set to not force the long / lat where the user is aware
                    values['-listbox-'].append('Latitude')
                queryDict.update({"listbox": values.get('-listbox-')})
            if values.get('-iucr-') != 'Select IUCR':
                queryStatement.append(values['-iucr-'])
                queryDict.update({"iucr": values.get('-iucr-')})
            if values.get('-address-') != 'Address' and values.get('-distance-') != 'Distance':
                test = geolocater()
                coordPair = test.getCoordinatePair(str(values.get('-address-')))
                coordPairAnswer = test.convertLLMiles(coordPair, int(values['-distance-']))
                queryStatement.append(values['-address-'])
                queryStatement.append(coordPairAnswer)
                queryDict.update({"address": coordPairAnswer})
                queryStatement.append(values['-distance-'])
                queryDict.update({"distance": values.get('-distance-')})
            if values.get('-primaryType-') != 'Select Primary Type':
                queryStatement.append(values['-primaryType-'])
                queryDict.update({"primaryType": values.get('-primaryType-')})
            if values.get('-startdate-') != None and values.get('-enddate-') != None:
                startdate = values['-startdate-']
                sd = startdate.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                enddate = values['-enddate-']
                ed = enddate.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                queryStatement.append(sd)
                queryStatement.append(ed)
                #queryStatement.append(startdate)
                #queryStatement.append(enddate)
                queryDict.update({"startdate": sd})
                queryDict.update({"enddate": ed})
                #queryDict.update({"startdate": startdate})
                #queryDict.update({"enddate": enddate})
            if len(queryStatement) >= 1:
                # Create the report here
                new_report = createReport("10", "[41.8878047, -87.6325199]")  # TODO: Need to update to take the query dictionary to load each row with the correct items into the popups

                print(queryStatement)
                print(queryDict)
                # Testing QUERY BUILDER
                fullQuery = genQuery(queryDict)
                connobject = sqlconnect()
                conn = connobject.create_connection()
                columnDict = queryDict['listbox']
                #print("Current query dictionary that will be used for headers: \n" + str(columnDict))
                #print("The type of columnDict variable is: " + str(type(columnDict)))
                with conn:
                    counter = len(columnDict)
                    crime_id = connobject.queryGeneric(conn, fullQuery)
                    final_output_string = ""
                    progress_counter = 0
                    for crime in crime_id:
                        this_coord = "[" + str(crime[-1]) + ", " + str(crime[-2]) + "]"
                        output_string = "L.marker({each_coord}, ".format(each_coord = this_coord) + "{iconAnchor: " + "{each_coord}, icon: defaultIcon".format(each_coord = this_coord) + "}).bindPopup(" +  "\"<p>"
                        #print(str(crime))
                        #print(type(crime)) -> Type of crime is tuple
                        counter = 0
                        for crime_tuple in crime:
                            output_string += str(columnDict[counter]) + " : " + str(crime_tuple) + "<br />"
                            counter += 1
                        output_string += "</p>\").addTo(mymap);"
                        final_output_string = output_string
                        new_report.update_results(final_output_string)
                        print(final_output_string)
                        print("Progress: " + str((progress_counter / len(crime_id)) * 100))
                        progress_counter += 1
                new_report.createReportTemplate()
                conn.close()
                # TODO: Expand on the createReport class to allow for more methods to complete the project
            if len(queryStatement) == 0:
                print("User did not input any filter requirements. Only querying the first 100 records.")
                connobject = sqlconnect()
                conn = connobject.create_connection()
                with conn:
                    crime_id = connobject.queryDefault(conn)
                    for crime in crime_id:
                        print(str(crime))
                conn.close()

if __name__ == '__main__':
    main()