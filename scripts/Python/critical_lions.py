import numpy as np
import scipy.constants


# Function/formulas
def critical_mass(temp, mass, density):
    return (np.sqrt((375 * scipy.constants.k**3) / (4 * scipy.constants.pi * mass**4 * scipy.constants.G**3)) *
            np.sqrt(temp**3 / density))
# Assumptions
MASS_LION = 190 # kg
VOLUME_LION = .173 # m^3
ROOM_TEMP = 295 # K

print(critical_mass(ROOM_TEMP, MASS_LION, MASS_LION/VOLUME_LION))