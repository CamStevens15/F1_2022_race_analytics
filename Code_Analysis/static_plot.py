# static_plot.py
# import necessary packages

from matplotlib import pyplot

import matplotlib.pyplot as plt

def static_track_temp(session):
    
    # create the figure and axis objects
    fig, ax = plt.subplots()
    # plot the data and customize
    ax.plot(session.weather_data['TrackTemp'])
    ax.set_xlabel('Laps')
    ax.set_ylabel('Temperature (*C)')
    plt.show()


def static_track_conditions(session):
    silverstone_tracktemp = session.weather_data[['TrackTemp',"AirTemp","Humidity","WindSpeed"]]

    silverstone_tracktemp.plot()
    pyplot.show()
