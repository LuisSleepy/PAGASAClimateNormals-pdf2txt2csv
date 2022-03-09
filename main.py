# Creating CSV version of the climatological data of stations stored in a TXT file
# Input: TXT files containing the climatological data for each station
# Output: CSV files containing collated climatological data of 54 stations grouped every month
#
# Program Author: Jan Luis Antoc

import pandas as pd
from pagasaClimNormals import *

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    climate_normal_entries = []
    # Change folder_text depending on the folder name containing the txt files
    folder_text = "pagasaClimNormalsTxt"
    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

    # Iterate over the 12 months in a year
    # Make sure that the read version of PDF files (stored as txt) are all in a folder
    for month in months:
        # Iterate over the txt files available in the folder
        for file_name in os.listdir(folder_text):
            file = os.path.join(folder_text, file_name)
            if os.path.isfile(file):
                with open(file, 'rb') as fin:
                    contents = fin.read().decode("utf-8")
                    station = file_name.removesuffix('.txt')

                    climatological_data = get_climatological_data(contents, month)
                    clim_normals_entry = {"Station": get_station_name(contents, station),
                                          "Month": month,
                                          "Latitude": get_latitude(contents, station),
                                          "Longitude": get_longitude(contents, station),
                                          "Elevation": get_elevation(contents, station),
                                          "Period": get_period(contents, station),
                                          "Rainfall": climatological_data[0],
                                          "DaysWithRainfall": climatological_data[1],
                                          "MaxTemp": climatological_data[2],
                                          "MinTemp": climatological_data[3],
                                          "MeanTemp": climatological_data[4],
                                          "DryBulbTemp": climatological_data[5],
                                          "WetBulbTemp": climatological_data[6],
                                          "DewPointTemp": climatological_data[7],
                                          "VaporPressure": climatological_data[8],
                                          "RelHumidity": climatological_data[9],
                                          "MSLP": climatological_data[10],
                                          "WindDir": climatological_data[11],
                                          "WindSpeed": climatological_data[12],
                                          "CloudAmount": climatological_data[13],
                                          "DaysWithTSTM": climatological_data[14],
                                          "DaysWithLTNG": climatological_data[15]
                                          }
                    climate_normal_entries.append(clim_normals_entry)

        clim_df = pd.DataFrame(climate_normal_entries)
        clim_df.to_csv("DOST-PAGASA-ClimatologicalData-" + month + ".csv")

        # Clear the list for another month
        climate_normal_entries.clear()
