import json
import re


class BusStopDataAnalyzer:
    stop_data_fields = ("stop_name",
                        "stop_type",
                        "a_time")

    def __init__(self, db):
        self.db = db

    def check_stop_data(self, stop_data: dict) -> dict:
        """
        Checks if stop_data match correct data types and required data are filled.
        Returns a dictionary {field: error} with same keys and the check result for each key as value:
        0 if field has valid type and is filled, 1 otherwise
        """
        result = dict.fromkeys(self.stop_data_fields, 1)

        # if type(stop_data["bus_id"]) is int:
        #     result["bus_id"] = 0
        # if type(stop_data["stop_id"]) is int:
        #     result["stop_id"] = 0

        # Stop name must be a two (or more) words string starting with capital letter
        stop_name_regexp = '([A-Z][a-z]+ )+(Road|Avenue|Boulevard|Street)$'
        stop_name = stop_data["stop_name"]
        if type(stop_name) is str and re.match(stop_name_regexp, stop_name):
            result["stop_name"] = 0

        # if type(stop_data["next_stop"]) is int:
        #     result["next_stop"] = 0

        # Stop type, if present, must be a character 'S', 'O' or 'F'
        stop_type_regexp = '[SOF]?$'
        stop_type = stop_data["stop_type"]
        if type(stop_type) is str and re.match(stop_type_regexp, stop_type):
            result["stop_type"] = 0

        # Arrival time must have format HH:MM
        a_time_regexp = '([01][0-9]|2[0-3]):[0-5][0-9]$'
        a_time = stop_data["a_time"]
        if type(a_time) is str and re.match(a_time_regexp, a_time):
            result["a_time"] = 0

        return result

    def validate_data(self) -> 'prints stop data field validation statistics':
        field_error = dict.fromkeys(self.stop_data_fields, 0)
        # Iterate over all the stops and update number of total errors for each field
        for stop in self.db:
            stop_result = self.check_stop_data(stop)
            for field, error in stop_result.items():
                field_error[field] += error
        # Print result
        print(f"Format validation: {sum(field_error.values())} errors")
        for field, error in field_error.items():
            print(f"{field}: {error}")

    def extract_lines(self) -> 'prints line names and number of stops':
        lines_stops = dict()  # {bus_id: stops}
        # Iterate over all the stops and update lines_stops dictionary
        for stop in self.db:
            bus_id = stop["bus_id"]
            if bus_id in lines_stops:
                lines_stops[bus_id] += 1
            else:
                lines_stops[bus_id] = 1
        # Print result
        print("Line names and number of stops:")
        for bus_id, stops in lines_stops.items():
            print(f"bus_id: {bus_id}, stops: {stops}")


database = json.loads(input())
stop_data_validator = BusStopDataAnalyzer(database)
stop_data_validator.extract_lines()
