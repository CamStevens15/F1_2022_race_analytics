# live_plot_user_input.py

# import necessary packages
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

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

# initial data

data = session.weather_data['TrackTemp']

    # create figure and axes objects
fig, ax = plt.subplots()

    # animation function
def animate(i):
    with open('data.txt','r') as f:
        for line in f:
            data.append(int(line.strip()))
    ax.clear()
    ax.plot(data[-5:]) # plot the last 5 data points
    
     # call the animation
ani = FuncAnimation(fig, animate, interval=1000)

# show the plot
plt.show()
