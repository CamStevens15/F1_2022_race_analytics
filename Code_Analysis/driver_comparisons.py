from matplotlib import pyplot as plt
import matplotlib as mpl
from matplotlib import cm
from matplotlib.pyplot import figure
from matplotlib.collections import LineCollection

import numpy as np
import pandas as pd

import fastf1 as ff1
from fastf1 import utils
from fastf1.core import Laps
from fastf1 import plotting

from timple.timedelta import strftimedelta


def main(year, grand_prix, session):
    ''' This calls on the fastf1 api and creates a session based on year,
     grand prix, and session(Quali, race, sprint) wanted '''
    # Setup plotting
    plotting.setup_mpl()

    # Enable the cache
    ff1.Cache.enable_cache('/Users/cameronstevens/Documents/Coding/F1_2022_race_analytics/cache') 

    # Get rid of some pandas warnings that are not relevant for us at the moment
    pd.options.mode.chained_assignment = None 

    # we only want support for timedelta plotting in this example
    ff1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme=None, misc_mpl_mods=False)

    #This loads the session for the Grand prix session of interest

    session = ff1.get_session(year, grand_prix, session)
    
    session.load() 

    return(session)
    # This is new with Fastf1 v.2.2
    

def plot_driver_speed_change(driver1, session):
    
    colormap = plt.cm.plasma

    lap = session.laps.pick_driver(driver1).pick_fastest()

    # Get telemetry data
    x = lap.telemetry['X']              # values for x-axis
    y = lap.telemetry['Y']              # values for y-axis
    color = lap.telemetry['Speed']      # value to base color gradient on

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

        # We create a plot with title and adjust some setting to make it look good.
    fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
    fig.suptitle(f'f"{session.event.year} {session.event.EventName} - {session.name} - {driver1} - Speed', size=24, y=0.97)


    # Adjust margins and turn of axis
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
    ax.axis('off')


    # After this, we plot the data itself.
    # Create background track line
    ax.plot(lap.telemetry['X'], lap.telemetry['Y'], color='black', linestyle='-', linewidth=16, zorder=0)

    # Create a continuous norm to map from data points to colors
    norm = plt.Normalize(color.min(), color.max())
    lc = LineCollection(segments, cmap=colormap, norm=norm, linestyle='-', linewidth=5)

    # Set the values used for colormapping
    lc.set_array(color)

    # Merge all line segments together
    line = ax.add_collection(lc)


    # Finally, we create a color bar as a legend.
    cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
    normlegend = mpl.colors.Normalize(vmin=color.min(), vmax=color.max())
    legend = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=colormap, orientation="horizontal")


    # Show the plot
    plt.show()

def get_driver_lap_comparison(driver1, driver2, session):
    
    '''This function is to take telementry data from each driver, and compare the respective
    lap times in regard to fastest lap time data.'''

    # Laps can now be accessed through the .laps object coming from the session
    laps_driver_1 = session.laps.pick_driver(driver1)
    laps_driver_2 = session.laps.pick_driver(driver2)

    # Select the fastest lap
    fastest_driver_1 = laps_driver_1.pick_fastest()
    fastest_driver_2 = laps_driver_2.pick_fastest()

    # Retrieve the telemetry and add the distance column
    telemetry_driver_1 = fastest_driver_1.get_telemetry().add_distance()
    telemetry_driver_2 = fastest_driver_2.get_telemetry().add_distance()

    # Make sure whe know the team name for coloring
    team_driver_1 = fastest_driver_1['Team']
    team_driver_2 = fastest_driver_2['Team']

    # extract delta time
    delta_time, ref_tel, compare_tel = utils.delta_time(fastest_driver_1, fastest_driver_2)



    plot_size = [15, 15]
    plot_title = f"{session.event.year} {session.event.EventName} - {session.name} - {driver1} VS {driver2}"
    #plot_ratios = [1, 3, 2, 1, 1, 2]
    plot_ratios = [1, 3, 2, 1, 1, 2, 1, 2]
    plot_filename = plot_title.replace(" ", "") + ".png"




    # Make plot a bit bigger
    plt.rcParams['figure.figsize'] = plot_size


    # Create subplots with different sizes
    #fig, ax = plt.subplots(6, gridspec_kw={'height_ratios': plot_ratios})
    # Create subplots with different sizes which includes DRS data
    fig, ax = plt.subplots(8, gridspec_kw={'height_ratios': plot_ratios})


    # Set the plot title
    ax[0].title.set_text(plot_title)


    # Delta line
    ax[0].plot(ref_tel['Distance'], delta_time)
    ax[0].axhline(0)
    ax[0].set(ylabel=f"Gap to {driver2} (s)")

    # Speed trace
    ax[1].plot(telemetry_driver_1['Distance'], telemetry_driver_1['Speed'], label=driver1, color=ff1.plotting.team_color(team_driver_1))
    ax[1].plot(telemetry_driver_2['Distance'], telemetry_driver_2['Speed'], label=driver2, color=ff1.plotting.team_color(team_driver_2))
    ax[1].set(ylabel='Speed')
    ax[1].legend(loc="lower right")

    # Throttle trace
    ax[2].plot(telemetry_driver_1['Distance'], telemetry_driver_1['Throttle'], label=driver1, color=ff1.plotting.team_color(team_driver_1))
    ax[2].plot(telemetry_driver_2['Distance'], telemetry_driver_2['Throttle'], label=driver2, color=ff1.plotting.team_color(team_driver_2))
    ax[2].set(ylabel='Throttle')

    # Brake trace
    ax[3].plot(telemetry_driver_1['Distance'], telemetry_driver_1['Brake'], label=driver1, color=ff1.plotting.team_color(team_driver_1))
    ax[3].plot(telemetry_driver_2['Distance'], telemetry_driver_2['Brake'], label=driver2, color=ff1.plotting.team_color(team_driver_2))
    ax[3].set(ylabel='Brake')

    # Gear trace
    ax[4].plot(telemetry_driver_1['Distance'], telemetry_driver_1['nGear'], label=driver1, color=ff1.plotting.team_color(team_driver_1))
    ax[4].plot(telemetry_driver_2['Distance'], telemetry_driver_2['nGear'], label=driver2, color=ff1.plotting.team_color(team_driver_2))
    ax[4].set(ylabel='Gear')

    # RPM trace
    ax[5].plot(telemetry_driver_1['Distance'], telemetry_driver_1['RPM'], label=driver1, color=ff1.plotting.team_color(team_driver_1))
    ax[5].plot(telemetry_driver_2['Distance'], telemetry_driver_2['RPM'], label=driver2, color=ff1.plotting.team_color(team_driver_2))
    ax[5].set(ylabel='RPM')

    # DRS trace
    ax[6].plot(telemetry_driver_1['Distance'], telemetry_driver_1['DRS'], label=driver1, color=ff1.plotting.team_color(team_driver_1))
    ax[6].plot(telemetry_driver_2['Distance'], telemetry_driver_2['DRS'], label=driver2, color=ff1.plotting.team_color(team_driver_2))
    ax[6].set(ylabel='DRS')
    ax[6].set(xlabel='Lap distance (meters)')


    ax[7].plot(telemetry_driver_1['Distance'], telemetry_driver_1['Time'],  label=driver1, color=ff1.plotting.team_color(team_driver_1))
    ax[7].plot(telemetry_driver_2['Distance'], telemetry_driver_2['Time'], label=driver2, color=ff1.plotting.team_color(team_driver_2))
    ax[7].set(ylabel='Laptime', xlabel='Lap')
    ax[7].legend(loc="upper center")


    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for a in ax.flat:
        a.label_outer()
        
    # Store figure
    plt.savefig(plot_filename, dpi=300)

# Would be nice to have a conditional statement that ensures the colours are not the same
    if ff1.plotting.team_color(team_driver_1) == ff1.plotting.team_color(team_driver_2):
        print('Same Team Color')
    
    plt.show()


def get_driver_from_session(year, grand_prix, driver1, session):
    '''This function gets the respective driver from the session of intererst
    from the fast f1 API.'''
    session = ff1.get_session(year, grand_prix, session)
    session.load() # This is new with Fastf1 v.2.2

    lap = session.laps.pick_driver(driver1).pick_fastest()
    colormap = plt.cm.plasma
    # Get telemetry data
    x = lap.telemetry['X']              # values for x-axis
    y = lap.telemetry['Y']              # values for y-axis
    color = lap.telemetry['Speed']      # value to base color gradient on

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

        # We create a plot with title and adjust some setting to make it look good.
    fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
    fig.suptitle(f'{grand_prix} {year} - {driver1} - Speed', size=24, y=0.97)

    # Adjust margins and turn of axis
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
    ax.axis('off')


    # After this, we plot the data itself.
    # Create background track line
    ax.plot(lap.telemetry['X'], lap.telemetry['Y'], color='black', linestyle='-', linewidth=16, zorder=0)

    # Create a continuous norm to map from data points to colors
    norm = plt.Normalize(color.min(), color.max())
    lc = LineCollection(segments, cmap=colormap, norm=norm, linestyle='-', linewidth=5)

    # Set the values used for colormapping
    lc.set_array(color)

    # Merge all line segments together
    line = ax.add_collection(lc)


    # Finally, we create a color bar as a legend.
    cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
    normlegend = mpl.colors.Normalize(vmin=color.min(), vmax=color.max())
    legend = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=colormap, orientation="horizontal")


    # Show the plot
    plt.show()






