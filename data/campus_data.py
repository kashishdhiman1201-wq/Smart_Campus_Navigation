
# =====================================================
# SMART CAMPUS NAVIGATION & EMERGENCY EVACUATION SYSTEM
# Module: Campus Dataset
# =====================================================

# Campus Location Details

CAMPUS_LOCATIONS = {
    "MAIN_GATE": {
        "name": "Main Gate",
        "type": "Entry",
        "x": 100,
        "y": 400
    },

    "ADMIN": {
        "name": "Administration Block",
        "type": "Academic",
        "x": 250,
        "y": 400
    },

    "BLOCK_A": {
        "name": "Academic Block A",
        "type": "Academic",
        "x": 400,
        "y": 300
    },

    "BLOCK_B": {
        "name": "Academic Block B",
        "type": "Academic",
        "x": 400,
        "y": 500
    },

    "LIBRARY": {
        "name": "Central Library",
        "type": "Academic",
        "x": 550,
        "y": 200
    },

    "COMPUTER_LAB": {
        "name": "Computer Lab",
        "type": "Laboratory",
        "x": 550,
        "y": 400
    },

    "SCIENCE_LAB": {
        "name": "Science Laboratory",
        "type": "Laboratory",
        "x": 550,
        "y": 600
    },

    "CAFETERIA": {
        "name": "Cafeteria",
        "type": "Food",
        "x": 700,
        "y": 300
    },

    "AUDITORIUM": {
        "name": "Auditorium",
        "type": "Facility",
        "x": 700,
        "y": 500
    },

    "SPORTS": {
        "name": "Sports Complex",
        "type": "Sports",
        "x": 850,
        "y": 400
    },

    "HOSTEL_A": {
        "name": "Hostel A",
        "type": "Hostel",
        "x": 850,
        "y": 200
    },

    "HOSTEL_B": {
        "name": "Hostel B",
        "type": "Hostel",
        "x": 850,
        "y": 600
    },

    "MEDICAL": {
        "name": "Medical Centre",
        "type": "Medical",
        "x": 700,
        "y": 700
    },

    "PARKING": {
        "name": "Parking Area",
        "type": "Parking",
        "x": 250,
        "y": 600
    },

    "ASSEMBLY": {
        "name": "Emergency Assembly Ground",
        "type": "Safe Zone",
        "x": 1000,
        "y": 400
    }
}


# =====================================================
# CAMPUS PATHWAYS
# Distance is measured in meters
# =====================================================

CAMPUS_PATHWAYS = [
    ("MAIN_GATE", "ADMIN", 100),
    ("MAIN_GATE", "PARKING", 120),

    ("ADMIN", "BLOCK_A", 150),
    ("ADMIN", "BLOCK_B", 170),
    ("ADMIN", "PARKING", 100),

    ("BLOCK_A", "LIBRARY", 120),
    ("BLOCK_A", "COMPUTER_LAB", 130),
    ("BLOCK_B", "COMPUTER_LAB", 110),
    ("BLOCK_B", "SCIENCE_LAB", 140),

    ("LIBRARY", "CAFETERIA", 150),
    ("COMPUTER_LAB", "CAFETERIA", 100),
    ("COMPUTER_LAB", "AUDITORIUM", 130),
    ("SCIENCE_LAB", "AUDITORIUM", 120),

    ("CAFETERIA", "HOSTEL_A", 140),
    ("CAFETERIA", "SPORTS", 160),
    ("AUDITORIUM", "SPORTS", 150),
    ("AUDITORIUM", "HOSTEL_B", 140),

    ("HOSTEL_A", "SPORTS", 130),
    ("HOSTEL_B", "SPORTS", 120),
    ("SCIENCE_LAB", "MEDICAL", 180),
    ("MEDICAL", "HOSTEL_B", 130),

    ("SPORTS", "ASSEMBLY", 150),
    ("HOSTEL_A", "ASSEMBLY", 220),
    ("HOSTEL_B", "ASSEMBLY", 200),
    ("PARKING", "ASSEMBLY", 300)
]


# =====================================================
# EMERGENCY EXITS
# =====================================================

EMERGENCY_EXITS = [
    "MAIN_GATE",
    "ASSEMBLY"
]


# =====================================================
# SAFE ZONES
# =====================================================

SAFE_ZONES = [
    "ASSEMBLY"
]


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def get_location_name(location_id):
    """Return the readable name of a campus location."""

    location = CAMPUS_LOCATIONS.get(location_id)

    if location:
        return location["name"]

    return "Unknown Location"


def get_all_locations():
    """Return all available campus locations."""

    return CAMPUS_LOCATIONS


def get_all_pathways():
    """Return all campus pathways."""

    return CAMPUS_PATHWAYS


def get_emergency_exits():
    """Return all emergency exit locations."""

    return EMERGENCY_EXITS


def get_safe_zones():
    """Return all designated safe zones."""

    return SAFE_ZONES


# =====================================================
# DATASET VALIDATION
# =====================================================

def validate_campus_data():

    for source, destination, distance in CAMPUS_PATHWAYS:

        if source not in CAMPUS_LOCATIONS:
            return False

        if destination not in CAMPUS_LOCATIONS:
            return False

        if distance <= 0:
            return False

    for exit_location in EMERGENCY_EXITS:

        if exit_location not in CAMPUS_LOCATIONS:
            return False

    for safe_location in SAFE_ZONES:

        if safe_location not in CAMPUS_LOCATIONS:
            return False

    return True


if __name__ == "__main__":

    print("SMART CAMPUS DATASET")
    print("--------------------")

    print("Total Locations:", len(CAMPUS_LOCATIONS))
    print("Total Pathways:", len(CAMPUS_PATHWAYS))
    print("Emergency Exits:", len(EMERGENCY_EXITS))
    print("Safe Zones:", len(SAFE_ZONES))

    if validate_campus_data():
        print("Dataset Validation: Successful")
    else:
        print("Dataset Validation: Failed")
