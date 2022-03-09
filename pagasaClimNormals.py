from pdfminer.high_level import extract_text_to_fp
import os


# Reading the pdf version of the climatological normals
# Input:    Directory wherein the PDF files are being stored
# Output:   Read data stored in a text file
def extract_text(directory):
    for file_name in os.listdir(directory):
        file = os.path.join(directory, file_name)
        if os.path.isfile(file):
            with open(file, 'rb') as fin:
                station_name = file_name.removesuffix('.pdf')
                with open(station_name + ".txt", 'w+') as fout:
                    extract_text_to_fp(fin, fout, output_type="text")
                    fout.close()
                fin.close()


# Reading the pdf version of the climatological normals
# Input:    Text file, file name of the text file
# Output:   Official station name stored in the text file
def get_station_name(extracted_text, station):
    # For the text files, these have different delimiters for the station name
    # Thus, list was used to group text files with the same delimiters for the station name
    republic_delim_list = ["ALABAT"]
    climatological_delim_list = ["AMBULONG", "COTABATO", "CALAYAN"]
    tstm_delim_list = ["APARRI", "BATANES RADAR", "CASIGURAN"]
    ltng_delim_list = ["BAGUIO", "BORONGAN", "BUTUAN", "CALAPAN"]
    windspd_delim_list = ["BALER RADAR"]
    no_delim_list = ["CABANATUAN", "CATARMAN", "CUBI POINT", "GENERAL SANTOS", "ITBAYAT", "TACLOBAN"]
    rainfall_delim_list = ["CATBALOGAN", "CLARK", "CORON"]
    temperature_delim_list = ["CUYO", "DAET", "DAGUPAN", "DAVAO CITY", "DIPOLOG", "GUIUAN", "HINATUAN", "IBA",
                              "INFANTA",
                              "LAOAG", "LUMBIA-EL SALVADOR", "MAASIN", "MACTAN", "MALAYBALAY", "MASBATE", "PORT AREA",
                              "PUERTO PRINCESA", "ROMBLON", "ROXAS CITY", "SAN JOSE", "SANGLEY POINT", "SCIENCE GARDEN",
                              "SURIGAO", "TAGBILARAN-DAUIS", "TAYABAS", "TUGUEGARAO", "VIGAN-SINAIT", "VIRAC SYNOP",
                              "ZAMBOANGA"]
    period_delim_list = ["DUMAGUETE", "LEGAZPI"]
    latitude_delim_list = ["ILOILO", "TANAY"]

    station_index = extracted_text.find("STATION")

    end_index = 0
    if station in republic_delim_list:
        end_index = extracted_text.find("Republic")
    elif station in climatological_delim_list:
        end_index = extracted_text.find("CLIMATOLOGICAL")
    elif station in tstm_delim_list:
        end_index = extracted_text.find("TSTM")
    elif station in ltng_delim_list:
        end_index = extracted_text.find("LTNG")
    elif station in windspd_delim_list:
        end_index = extracted_text.find("WINDSPD")
    elif station in no_delim_list:
        end_index = extracted_text.find("NO.")
    elif station in rainfall_delim_list:
        end_index = extracted_text.find("RAINFALL")
    elif station in temperature_delim_list:
        end_index = extracted_text.find("TEMPERATURE")
    elif station in period_delim_list:
        end_index = extracted_text.find("PERIOD")
    elif station in latitude_delim_list:
        end_index = extracted_text.find("LATITUDE")

    # STATION: consists of eight characters, so advance the index by 9 to obtain the station name
    station_name = extracted_text[station_index + 9:end_index]
    return station_name


# Converts Degrees Minutes Seconds (DMS) Coordinates into Decimal Degrees (DD)
# Input:    DMS in this format: degree_value(degree_symbol)minute_value'second_value"
# Output:   DD conversion of the DMS
# NOTE: Tested ONLY to be working for this project.
def dms2degrees(dms_value_string):
    # Find the symbols for the DMS coordinates. Read the values before these symbols. Then, convert minutes and seconds.
    # 1 degree = 60 minutes = 3600 seconds
    degree_symbol_index = dms_value_string.find(chr(176))
    degrees = float(dms_value_string[:degree_symbol_index])
    minute_symbol_index = dms_value_string.find("'")
    minutes = float(dms_value_string[degree_symbol_index + 1:minute_symbol_index]) / 60
    second_symbol_index = dms_value_string.find('"')
    seconds = float(dms_value_string[minute_symbol_index + 1:second_symbol_index]) / 3600

    degrees = round(degrees + minutes + seconds, 4)
    return degrees


# Obtain the latitude coordinate in a text file of a station
# Input:    Text file, station name
# Output:   Latitude in DD format
def get_latitude(extracted_text, station):
    # BAGUIO.txt and CORON.txt was directly manipulated because no " was read on its latitude value
    latitude_index = extracted_text.find("LATITUDE")

    # Different delimiters for the latitude coordinate
    republic_delim_list = ['CALAYAN']
    period_delim_list = ['BUTUAN', 'ILOILO', 'TANAY', 'VIRAC SYNOP']
    longitude_delim_list = ['AMBULONG', 'BAGUIO', 'BALER RADAR', 'CUBI POINT']
    station_delim_list = ['BATANES RADAR', 'PUERTO PRINCESA', 'TAGBILARAN-DAUIS']
    vapor_delim_list = ['CABANATUAN']
    temperature_delim_list = ['DUMAGUETE']

    if station in republic_delim_list:
        end_index = extracted_text.find('Republic')
    elif station in period_delim_list:
        end_index = extracted_text.find("PERIOD")
    elif station in longitude_delim_list:
        end_index = extracted_text.find("LONGITUDE")
    elif station in station_delim_list:
        end_index = extracted_text.find("STATION")
    elif station in vapor_delim_list:
        end_index = extracted_text.find("VAPOR")
    elif station in temperature_delim_list:
        end_index = extracted_text.find("TEMPERATURE")
    else:
        end_index = extracted_text.find("ELEVATION")
    latitude_value = extracted_text[latitude_index + 10: end_index]

    # For proper formatting of the latitude value (degree, minute, second)
    char_to_replace = {' ': '', 'o': chr(176), "''": '"'}
    for key, value in char_to_replace.items():
        latitude_value = latitude_value.replace(key, value)

    # Some data visualization tool, such as Tableau, only accepts coordinates in DD format.
    decimal_degrees = dms2degrees(latitude_value)
    return decimal_degrees


# Obtain the longitude coordinate in a text file of a station
# Input:    Text file, station name
# Output:   Longitude in DD format
def get_longitude(extracted_text, station):
    longitude_index = extracted_text.find("LONGITUDE")

    # Some longitude values were delimited with the text "ELEVATION" while most were delimited with "(1)(2)..."
    elevation_delim_list = ['AMBULONG', 'BAGUIO', 'BALER RADAR', 'CUBI POINT']
    if station in elevation_delim_list:
        end_index = extracted_text.find('ELEVATION')
    else:
        end_index = extracted_text.find('(1)(2)')
    longitude_value = extracted_text[longitude_index + 11: end_index]

    # For proper formatting of the latitude value (degree, minute, second)
    char_to_replace = {' ': '', 'o': chr(176), "''": '"'}
    for key, value in char_to_replace.items():
        longitude_value = longitude_value.replace(key, value)

    decimal_degrees = dms2degrees(longitude_value)
    return decimal_degrees


# Obtain the elevation value in a text file of a station
# Input:    Text file, station name
# Output:   Elevation (in meters)
def get_elevation(extracted_text, station):
    elevation_index = extracted_text.find("ELEVATION")

    # Different delimiters for the elevation value
    header_delim_list = ['AMBULONG', 'BAGUIO', 'BALER RADAR', 'CUBI POINT']
    latitude_delim_list = ['BATANES RADAR', 'CABANATUAN', 'CALAYAN', 'PUERTO PRINCESA', 'TAGBILARAN-DAUIS']
    vapor_delim_list = ['BUTUAN', 'CALAPAN', 'CATARMAN']
    DIR_delim_list = ['CATBALOGAN', 'CLARK', 'CORON']

    if station == 'ALABAT':
        end_index = extracted_text.find('mPERIOD')
    elif station == 'BORONGAN':
        end_index = extracted_text.find('mRAINFALL')
    elif station == 'COTABATO':
        end_index = extracted_text.find("mDEW")
    elif station == 'ILOILO':
        end_index = extracted_text.find('mMONTHRAINFALL')
    elif station == 'LEGAZPI':
        end_index = extracted_text.find('mTEMPERATURE')
    elif station == 'TANAY':
        end_index = extracted_text.find('mRH')
    elif station in latitude_delim_list:
        end_index = extracted_text.find('mLATITUDE')
    elif station in vapor_delim_list:
        end_index = extracted_text.find('mVAPOR')
    elif station in DIR_delim_list:
        end_index = extracted_text.find('mDIR')
    elif station in header_delim_list:
        end_index = extracted_text.find('m(1)(2)')
    else:
        end_index = extracted_text.find('mSTATION')

    # Remove the excess spaces and characters. Ignore the "m" unit.
    elevation_value = (extracted_text[elevation_index + 11: end_index]).strip()
    return elevation_value


# Obtain the period value in a text file of a station
# Input:    Text file, station name
# Output:   Period (Format: XXXX - XXXX) wherein XXXX is a year
def get_period(extracted_text, station):
    period_index = extracted_text.find("PERIOD")

    # Different delimiters for the period value
    min_delim_list = ['BALER RADAR', 'CUBI POINT']
    elevation_delim_list = ['BATANES RADAR', 'CALAYAN', 'ILOILO', 'PUERTO PRINCESA', 'TAGBILARAN-DAUIS', 'TANAY',
                            'VIRAC SYNOP']
    longitude_delim_list = ['BORONGAN', 'BUTUAN', 'CABANATUAN', 'CALAPAN', 'MACTAN', 'PORT AREA']

    if station == 'ALABAT':
        end_index = extracted_text.find('STATION')
    elif station == 'AMBULONG':
        end_index = extracted_text.find('TSTM')
    elif station == 'BAGUIO':
        end_index = extracted_text.find('VAPOR')
    elif station in min_delim_list:
        end_index = extracted_text.find('MIN')
    elif station in elevation_delim_list:
        end_index = extracted_text.find('ELEVATION')
    elif station in longitude_delim_list:
        end_index = extracted_text.find('LONGITUDE')
    else:
        end_index = extracted_text.find('LATITUDE')

    period_value = (extracted_text[period_index + 8: end_index])
    return period_value


# Obtain the succeeding month for a given month
# Input:    Month (Format: XXX, e.g., JAN)
# Output:   Month (Same format with the Input)
def next_month_identifier(month):
    next_month = {
        'JAN': 'FEB',
        'FEB': 'MAR',
        'MAR': 'APR',
        'APR': 'MAY',
        'MAY': 'JUN',
        'JUN': 'JUL',
        'JUL': 'AUG',
        'AUG': 'SEP',
        'SEP': 'OCT',
        'OCT': 'NOV',
        'NOV': 'DEC'
    }
    # "Invalid month" statement seems to be not to be outputted as the month has been checkd in get_climatological_data
    return next_month.get(month, 'Invalid month')


# Obtain the corresponding value for each climatological parameter
# Input:    Text file, station name
# Output:   List of values, from Amount of Rainfall to Number of Days with Lightning (refer to the PDF version of the
#           climatological normals
def get_climatological_data(extracted_text, month):
    months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

    # Run through the information indicated next to the input month in the txt file
    if month in months:
        # Find the index of the input month and the next month to it
        start_month_index = extracted_text.find(month)
        next_month = next_month_identifier(month)
        next_month_index = extracted_text.find(next_month)

        # A month consists of three characters, so advance the index to obtain only the string of information for
        # the specified month
        month_data = extracted_text[start_month_index + 3:next_month_index]
        # "." has been treated as a delimiter in reading the value for each climatological parameter
        rainfall_decimal_index = month_data.find('.')
        rainfall = month_data[:rainfall_decimal_index + 2]  # Rainfall - has one decimal value

        # The "." for the Maximum Temperature was used as a delimiter for the Number of Rainy Days and the Maximum
        # Temperature
        rainfall_days_start = month_data[rainfall_decimal_index + 2:next_month_index]
        max_temp_decimal = rainfall_days_start.find('.')
        rainfall_days = rainfall_days_start[:max_temp_decimal - 2]

        # All temperature values have one decimal value and a length of 4 (XX.X), including the decimal point
        max_temp = rainfall_days_start[max_temp_decimal - 2:max_temp_decimal + 2]

        min_temp = rainfall_days_start[max_temp_decimal + 2:max_temp_decimal + 6]
        mean_temp_start = rainfall_days_start[max_temp_decimal + 6:]

        mean_temp = mean_temp_start[:4]

        dry_bulb_temp_start = mean_temp_start[4:]
        dry_bulb_temp = dry_bulb_temp_start[:4]

        wet_bulb_temp_start = dry_bulb_temp_start[4:]
        wet_bulb_temp = wet_bulb_temp_start[:4]

        dew_point_temp_start = wet_bulb_temp_start[4:]
        dew_point_temp = dew_point_temp_start[:4]

        vapor_pressure_start = dew_point_temp_start[4:]
        vapor_pressure = vapor_pressure_start[:4]

        relative_humidity_start = vapor_pressure_start[4:]
        relative_humidity = relative_humidity_start[:2]

        # Exception for MSLP that is lower than 1000. Only one occurrence: For Vigan-Sinait during October
        mslp_start = relative_humidity_start[2:]
        mslp_delim_index = mslp_start.find(".")
        if mslp_delim_index == 3:
            mslp = mslp_start[:5]
            wind_dir_start = mslp_start[5:]
        else:
            mslp = mslp_start[:6]
            wind_dir_start = mslp_start[6:]

        wind_dir = wind_dir_start[:2]

        # Checking if the wind direction consists of two or three letters (e.g., NW, NNW)
        if wind_dir.isalpha():
            if wind_dir_start[:3].isalpha():
                wind_dir = wind_dir_start[:3]
                wind_speed_start = wind_dir_start[3:]
            else:
                wind_speed_start = wind_dir_start[2:]
        else:
            wind_dir = wind_dir[:1]
            wind_speed_start = wind_dir_start[1:]

        wind_speed = wind_speed_start[:1]

        cloud_amt_start = wind_speed_start[1:]
        cloud_amt = cloud_amt_start[:1]

        tstm_start = cloud_amt_start[1:]

        # Txt files have been modified. A "." delimiter has been inserted between the TSTM and LTNG values
        tstm_delim_index = tstm_start.find(".")
        tstm = tstm_start[:tstm_delim_index]
        ltng = tstm_start[tstm_delim_index + 1:tstm_delim_index + 2]  # To eliminate text after December values

        climatological_values = [rainfall, rainfall_days, max_temp, min_temp, mean_temp, dry_bulb_temp, wet_bulb_temp,
                                 dew_point_temp, vapor_pressure, relative_humidity, mslp, wind_dir, wind_speed,
                                 cloud_amt, tstm, ltng]

        return climatological_values
    else:
        raise TypeError("Invalid month input.")
