# create a small python program that calculates Earth's position relative to the sun at any given time
import math
import matplotlib.pyplot as plt

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

    r = planets[planet]
    orb_period = calc_orb_period(r)

    w = (2 * math.pi) / orb_period

    x_position = r * (math.cos(init_angle + (w * time)))
    y_position = r * (math.sin(init_angle + (w * time)))

    return x_position, y_position


# generate list of orbital coordinates at given resolution
def positions_list(planet, resolution=100, init_angle=0):
    r = planets[planet]
    orb_period = calc_orb_period(r)

    time_points = [(i * orb_period / resolution) for i in range(resolution + 1)]
    positions = [(planet_position(planet, t, init_angle)) for t in time_points]

    return positions


# pretty print the position of the planet at each time point
def print_positions(positions):
    for i, (x, y) in enumerate(positions):
        print(f"Point {i+1}: ({x:.3}, {y:.3})")


def print_planet_at_time(planet, time, planet_position):
    print(f"At time {time} days, {planet} is at position: {planet_position}")


def plot_orbit(planet, resolution, time=100, init_angle=0):

    x, y = planet_position(planet, time, init_angle)

    positions = positions_list(planet, resolution)
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


def plot_all_orbits(resolution, time=100, init_angle=0):

    plt.figure(figsize=(8, 8))

    for planet in planets.keys():

        # for each planet, generate the x and y positions and store in dictionary to use in plotting orbit
        positions = positions_list(planet, resolution)
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


def animate_orbit():

    plt.figure(figsize=(8, 8))
    plt.axis("equal")
    plt.grid(True, alpha=0.3)
    plt.xlabel("AU")
    plt.ylabel("AU")
    plt.title("The Solar System")
    plt.scatter(0, 0, c="yellow", s=1000, label="Sun")
    plt.annotate(
        "Sun", xy=(0, 0), textcoords="offset points", xytext=(15, 15), ha="center"
    )

    planet_markers = {}

    for planet in planets.keys():

        # draw the orbital path for each planet
        positions = positions_list(planet, resolution)
        x_positions = [pos[0] for pos in positions]
        y_positions = [pos[1] for pos in positions]

        plt.plot(
            x_positions, y_positions, ls="--", label=f"{planet.capitalize()}'s Orbit"
        )

        # initialize the planet markers and store the Artist object in a dictionary for later update
        x, y = planet_position(planet)
        planet_markers[planet] = plt.scatter(x, y)

    # test updating marker by using new coordinates for earth at day 100
    offsets = [planet_position("earth", 100)]
    earth = planet_markers["earth"]
    earth.set_offsets(offsets)

    plt.show()



if __name__ == "__main__":

    # "planet name": orbital radius in AU
    planets = {"venus": 0.723, "earth": 1, "mars": 1.52}

    # for testing purposes, hardcode the planet and time
    planet = "mars"
    time = 100  # days
    resolution = 100
    init_angle = 0

    # plot_orbit(planet, resolution)
    # plot_all_orbits(resolution)
    animate_orbit()
