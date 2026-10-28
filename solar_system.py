# create a small python program that calculates Earth's position relative to the sun at any given time
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# -------------------------------------------------------------------------------------
# FUNCTIONS
# -------------------------------------------------------------------------------------

# using Kepler's 3rd Law
def calc_orb_period(r):
    orb_period = math.sqrt(r**3)

    # convert to earth days
    orb_period = orb_period * 365.25

    return orb_period


# function to calculate position
def planet_position(planet, time=0, init_angle=0):

    r = planets[planet]["radius"]
    orb_period = calc_orb_period(r)

    w = (2 * math.pi) / orb_period

    x_position = r * (math.cos(init_angle + (w * time)))
    y_position = r * (math.sin(init_angle + (w * time)))

    return x_position, y_position

def time_points(planet, resolution=100):
    r = planets[planet]["radius"]
    orb_period = calc_orb_period(r)

    time_points = [(i * orb_period / resolution) for i in range(resolution + 1)]

    return time_points


# generate list of orbital coordinates at given resolution
def positions_list(planet, init_angle=0):

    time_points_list = time_points(planet)
    positions = [(planet_position(planet, t, init_angle)) for t in time_points_list]

    return positions

# -------------------------------------------------------------------------------------
# UTILITIES - printing
# -------------------------------------------------------------------------------------

# pretty print the position of the planet at each time point
def print_positions(positions):
    for i, (x, y) in enumerate(positions):
        print(f"Point {i+1}: ({x:.3}, {y:.3})")


def print_planet_at_time(planet, time, planet_position):
    print(f"At time {time} days, {planet} is at position: {planet_position}")

# -------------------------------------------------------------------------------------
# STATIC PLOTS
# -------------------------------------------------------------------------------------

def plot_orbit(planet, time=100, init_angle=0):

    x, y = planet_position(planet, time, init_angle)

    positions = positions_list(planet)
    x_positions = [pos[0] for pos in positions]
    y_positions = [pos[1] for pos in positions]

    plt.figure(figsize=(8, 8))
    plt.plot(x_positions, y_positions, ls="--")
    plt.scatter(0, 0, c="yellow", s=1000)
    plt.scatter(x, y, c="blue", s=100)
    plt.annotate(
        "Sun", xy=(0, 0), textcoords="offset points", xytext=(15, 15), ha="center"
    )
    plt.annotate(
        planet.capitalize(),
        xy=(x, y),
        textcoords="offset points",
        xytext=(10, 10),
        ha="center",
    )
    plt.grid(True, alpha=0.3)
    plt.title(f"{planet.capitalize()}'s Orbit Around the Sun")
    plt.xlabel("AU")
    plt.ylabel("AU")
    plt.axis("equal")
    plt.show()


def plot_all_orbits(time=100, init_angle=0):

    plt.figure(figsize=(8, 8))

    for planet in planets.keys():

        # for each planet, generate the x and y positions and store in dictionary to use in plotting orbit
        positions = positions_list(planet)
        x_positions = [pos[0] for pos in positions]
        y_positions = [pos[1] for pos in positions]

        plt.plot(
            x_positions, y_positions, ls="--", label=f"{planet.capitalize()}'s Orbit"
        )

        # for each planet compute position at day 100 to use as marker in plot
        x, y = planet_position(planet, time, init_angle)

        plt.scatter(x, y)
        plt.annotate(
            planet.capitalize(),
            xy=(x, y),
            textcoords="offset points",
            xytext=(10, 10),
            ha="center",
        )

    plt.scatter(0, 0, c="yellow", s=1000)
    plt.annotate(
        "Sun", xy=(0, 0), textcoords="offset points", xytext=(15, 15), ha="center"
    )
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.xlabel("AU")
    plt.ylabel("AU")
    plt.title(f"Planetary Orbits Around the Sun at Day {time}")
    plt.axis("equal")
    plt.show()


# -------------------------------------------------------------------------------------
# ANIMATED ORBITS
# -------------------------------------------------------------------------------------


def animate_orbit(num_frames, days_per_frame):

    plt.style.use('dark_background')

    # create figure
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.axis("equal")
    ax.set_axis_off()
    ax.set_title("Inner Solar System")

    # Glow layers (larger, more transparent markers underneath) for sun
    glow_sizes = [6000, 4000, 2500]
    glow_alphas = [0.1, 0.15, 0.2]

    for size, alpha in zip(glow_sizes, glow_alphas):
        ax.scatter(
            0, 0, s=size, color="#FBBF24", alpha=alpha, edgecolors="none", zorder=1
        )

    sun = ax.scatter(0, 0, c="#FBBF24", s=2000, label="Sun", alpha=1.0, zorder=2) # draw sun


    # xy property id's point being annotated, an annotations anchor point is changed by updating this xy attribute
    ax.annotate(
        "Sun", xy=(0, 0), textcoords="offset points", xytext=(22, 20), ha="center"
    )

    # planet_markers dictionary has (key:value) pairs of ("name" : Artist object)
    planet_markers = {}
    planet_labels = {}

    # create dyanmic time display label
    text_artist = ax.text(0.97, 0.97, "Day 0",
        transform=ax.transAxes, 
        ha='right', 
        va='top',
        fontsize=12, 
        bbox={
        "boxstyle": "round,pad=0.5",
        "facecolor": "#1B263B",
        "edgecolor": "#53647A",
        "alpha": 0.9
    })

    for planet in planets.keys():

        # draw the orbital path for each planet
        positions = positions_list(planet)
        x_positions = [pos[0] for pos in positions]
        y_positions = [pos[1] for pos in positions]

        ax.plot(
            x_positions, y_positions, 
            alpha=0.2,
            linewidth=0.5,
            label=f"{planet.capitalize()}'s Orbit",
            color='white'
        )

        # initialize the planet markers and store the Artist object in a dictionary for later update
        x, y = planet_position(planet)
        planet_markers[planet] = ax.scatter(x, y, color=f'{planets[planet]["colour"]}', s=planets[planet]["size"])

        # initialize annotations and store Artist labels in dictionary
        planet_labels[planet] = ax.annotate((f"{planet}").capitalize(), xy=(x, y), textcoords="offset points", xytext=(12, 12), ha="center")

    # define update function for FuncAnimation
    def update(frame):

        sim_time = frame * days_per_frame

        text_artist.set_text(f"Day {math.floor(sim_time)}")

        for planet, planet_artist in planet_markers.items():

            offset = planet_position(planet, sim_time)
            planet_artist.set_offsets([offset])
        
            label = planet_labels[planet]
            label.xy = offset
    
    # animation controller
    ani = FuncAnimation(
        fig,
        update,
        frames=range(num_frames),
        interval = 50, # ms
        blit=False,
        repeat=False
    )

    plt.show()




if __name__ == "__main__":

    # "planet name": {orbital radius in AU, colour code, size}
    
    planets = { 
        "mercury": {"radius": 0.387, "colour": '#A8A9AD', "size": 50},
        "venus": {"radius": 0.723, "colour": '#D9B779', "size": 324},
        "earth": {"radius": 1, "colour": '#60A5FA', "size": 400},
        "mars": {"radius": 1.52, "colour": '#D97757', "size": 100},
    }

    # for testing purposes, hardcode the planet and time
    planet = "mars"
    time = 100  # days
    resolution = 100
    init_angle = 0
    days = 365*2
    days_per_frame = 1.5
    num_frames = round(days/days_per_frame) + 1

    # plot_orbit(planet)
    # plot_all_orbits()
    animate_orbit(num_frames, days_per_frame)
