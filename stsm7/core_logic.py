import junctions_config

from junctions_config import (
    JUNCTIONS,
    COORDINATED_LIMIT,
    NEXT_JUNCTION
)

SEC_PER_VEHICLE = 2
MAX_GREEN = 110
MIN_GREEN = 5
MAX_WAIT = 2


def update_logic():

    for jid, j in JUNCTIONS.items():

        # -------------------------------
        # STARTUP ALL RED (ONLY ONCE)
        # -------------------------------
        if j["startup_red"]:

            j["timer"] -= 1

            if j["timer"] <= 0:
                j["startup_red"] = False

            continue

        # -------------------------------
        # EMERGENCY OVERRIDE
        # -------------------------------
        if j["emergency"]:

            j["signal"] = {
                "north": "green",
                "south": "red",
                "east": "red",
                "west": "red"
            }

            j["current_green"] = "north"
            j["green_timer"] = 10
            j["timer"] = 10

            continue

        # -------------------------------
        # ACTIVE SIGNAL
        # -------------------------------
        # Manual request received
        # Mode change request
        if (
            junctions_config.PENDING_MODE is not None
            and
            j["green_timer"] > 3
        ):
            j["green_timer"] = 3

        # Manual request
        if (
            junctions_config.MODE == "manual"
            and
            junctions_config.PENDING_MANUAL_LANE is not None
            and
            j["green_timer"] > 3
        ):
            j["green_timer"] = 3

        if j["green_timer"] > 0:

            j["green_timer"] -= 1
            j["timer"] = j["green_timer"]

            lane = j["current_green"]

            j["signal"] = {
                "north": "red",
                "south": "red",
                "east": "red",
                "west": "red"
            }

            if j["green_timer"] <= 5:
               j["signal"][lane] = "yellow"
            else:
                j["signal"][lane] = "green"

            if j["green_timer"] == 0:

                if junctions_config.PENDING_MODE is not None:

                    junctions_config.MODE = (
                    junctions_config.PENDING_MODE
                    )

                    junctions_config.PENDING_MODE = None
                if (
                    junctions_config.MODE == "manual"
                    and
                    junctions_config.PENDING_MANUAL_LANE is not None
                ):

                    junctions_config.MANUAL_LANE = (
                        junctions_config.PENDING_MANUAL_LANE
                )

                    junctions_config.PENDING_MANUAL_LANE = None

                j["current_green"] = None

            continue
                
        # -------------------------------
        # MANUAL MODE
        # -------------------------------
        if (
            junctions_config.MODE == "manual"
            and
            junctions_config.MANUAL_LANE is not None
        ):

            lane = junctions_config.MANUAL_LANE

        else:

            # -------------------------------
            # SELECT NEXT LANE
            # -------------------------------
            candidate_lanes = sorted(
                j["count"],
                key=lambda x: j["count"][x],
                reverse=True
            )

            # Tie-break rotation
            if (
                len(candidate_lanes) > 1
                and
                j["count"][candidate_lanes[0]]
                == j["count"][candidate_lanes[1]]
                and
                candidate_lanes[0] == j["last_lane"]
            ):
                candidate_lanes[0], candidate_lanes[1] = (
                    candidate_lanes[1],
                    candidate_lanes[0]
                )
            lane = None

            for candidate in candidate_lanes:

                blocked = False

                if junctions_config.MODE == "coordinated":

                    nxt = NEXT_JUNCTION.get(jid)

                    if nxt is not None:

                        if (
                            JUNCTIONS[nxt]["count"][candidate]
                            >= COORDINATED_LIMIT
                        ):
                            blocked = True

                if not blocked:
                    lane = candidate
                    break

            if lane is None:
                lane = candidate_lanes[0]

            # -------------------------------
            # FAIRNESS
            # -------------------------------
            for l in candidate_lanes:

                if (
                    j["waiting_cycles"][l] >= MAX_WAIT
                    and
                    j["count"][l] > 0
                ):
                    lane = l
                    break

        # -------------------------------
        # UPDATE WAITING CYCLES
        # -------------------------------
        for l in j["waiting_cycles"]:

            if l == lane:
                j["waiting_cycles"][l] = 0
            else:
                j["waiting_cycles"][l] += 1

        # -------------------------------
        # GREEN TIME
        # -------------------------------
        vehicle_count = j["count"][lane]

        green_time = vehicle_count * SEC_PER_VEHICLE
        green_time = max(MIN_GREEN, green_time)
        green_time = min(MAX_GREEN, green_time)

        # Manual mode = fixed time
        if junctions_config.MODE == "manual":
            green_time = 15

        # -------------------------------
        # APPLY SIGNAL
        # -------------------------------
        j["signal"] = {
            "north": "red",
            "south": "red",
            "east": "red",
            "west": "red"
        }

        j["signal"][lane] = "green"

        j["current_green"] = lane
        j["last_lane"] = lane
        j["green_timer"] = green_time
        j["timer"] = green_time