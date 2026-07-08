MODE = "independent"
PENDING_MODE = None
MANUAL_LANE = None
PENDING_MANUAL_LANE = None
COORDINATED_LIMIT = 10

NEXT_JUNCTION = {
    "A": "B",
    "B": "C",
    "C": None
}

PREV_JUNCTION = {
    "A": None,
    "B": "A",
    "C": "B"
}
JUNCTIONS = {

    "A": {
        "signal": {"north":"red","south":"red","east":"red","west":"red"},
        "count": {"north":0,"south":0,"east":0,"west":0},
        "waiting_cycles": {"north":0,"south":0,"east":0,"west":0},

        "timer": 5,
        "emergency": False,

        "frame": None,

        "frames": {
            "north": None,
            "south": None,
            "east": None,
            "west": None
        },

        "current_green": None,
        "green_timer": 0,
        "last_lane": None,
        "startup_red": True
    },

    "B": {
        "signal": {"north":"red","south":"red","east":"red","west":"red"},
        "count": {"north":0,"south":0,"east":0,"west":0},
        "waiting_cycles": {"north":0,"south":0,"east":0,"west":0},

        "timer": 5,
        "emergency": False,

        "frame": None,

        "frames": {
            "north": None,
            "south": None,
            "east": None,
            "west": None
        },

        "current_green": None,
        "green_timer": 0,
        "last_lane": None,
        "startup_red": True
    },

    "C": {
        "signal": {"north":"red","south":"red","east":"red","west":"red"},
        "count": {"north":0,"south":0,"east":0,"west":0},
        "waiting_cycles": {"north":0,"south":0,"east":0,"west":0},

        "timer": 5,
        "emergency": False,

        "frame": None,

        "frames": {
            "north": None,
            "south": None,
            "east": None,
            "west": None
        },

        "current_green": None,
        "green_timer": 0,
        "last_lane": None,
        "startup_red": True
    }
}