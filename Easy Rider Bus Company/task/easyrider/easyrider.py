import json
import re


def check_stop_data(stop_data: dict) -> dict:
    """
    Checks if stop_data match correct data types and required data are filled.
    Returns a dictionary {field: error} with same keys and the check result for each key as value:
    0 if field has valid type and is filled, 1 otherwise
    """
    result = {"bus_id": 1,
              "stop_id": 1,
              "stop_name": 1,
              "next_stop": 1,
              "stop_type": 1,
              "a_time": 1}

    if type(stop_data["bus_id"]) is int:
        result["bus_id"] = 0
    if type(stop_data["stop_id"]) is int:
        result["stop_id"] = 0

    # Stop name must be a two (or more) words string starting with capital letter
    stop_name_regexp = '^[A-Z][a-z]+ [a-zA-Z]+'
    stop_name = stop_data["stop_name"]
    if type(stop_name) is str and len(stop_name) > 0:# and re.match(stop_name_regexp, stop_name):
        result["stop_name"] = 0

    if type(stop_data["next_stop"]) is int:
        result["next_stop"] = 0

    # Stop type, if present, must be a character 'S', 'O' or 'F'
    stop_type_regexp = '^[SOF]?$'
    stop_type = stop_data["stop_type"]
    if type(stop_type) is str and re.match(stop_type_regexp, stop_type):
        result["stop_type"] = 0

    # Arrival time must have format HH:MM
    a_time_regexp = '^[0-9]{2}:[0-9]{2}$'
    a_time = stop_data["a_time"]
    if type(a_time) is str and re.match(a_time_regexp, a_time):
        result["a_time"] = 0

    return result


def validate_data(db: list) -> 'prints stop data field validation statistics':
    field_error = {"bus_id": 0,
                   "stop_id": 0,
                   "stop_name": 0,
                   "next_stop": 0,
                   "stop_type": 0,
                   "a_time": 0}
    # Iterate over all the stops and update number of total errors for each field
    for stop in db:
        stop_result = check_stop_data(stop)
        for field, error in stop_result.items():
            field_error[field] += error
    # Print result
    print(f"Type and required field validation: {sum(field_error.values())} errors")
    for field, error in field_error.items():
        print(f"{field}: {error}")


database = json.loads(input())
validate_data(database)
