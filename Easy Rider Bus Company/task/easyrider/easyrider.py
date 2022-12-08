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

    def check_stops(self) -> 'prints stop names of type Start, Transfer and Finish':
        if self.check_start_finish():
            all_stops = []  # list to keep already checked stops, in order to find transfer stops
            start_stops = []
            transfer_stops = []
            finish_stops = []
            # Iterate over all the stops
            for stop in self.db:
                stop_name = stop["stop_name"]
                stop_type = stop["stop_type"]
                if stop_type == "S":
                    start_stops.append(stop_name)
                if stop_name in all_stops:
                    transfer_stops.append(stop_name)
                if stop_type == "F":
                    finish_stops.append(stop_name)
                all_stops.append(stop_name)
            # Print result, removing duplicates with set
            start_stops = list(set(start_stops))
            start_stops.sort()
            transfer_stops = list(set(transfer_stops))
            transfer_stops.sort()
            finish_stops = list(set(finish_stops))
            finish_stops.sort()
            print(f"Start stops: {len(start_stops)} {start_stops}")
            print(f"Transfer stops: {len(transfer_stops)} {transfer_stops}")
            print(f"Finish stops: {len(finish_stops)} {finish_stops}")

    def check_start_finish(self) -> 'checks if all bus lines have Start and Finish stop':
        checked_bus_lines = []
        # Iterate over all the stops
        for stop in self.db:
            current_bus_line = stop["bus_id"]
            # If bus line not checked yet
            if current_bus_line not in checked_bus_lines:
                checked_bus_lines.append(current_bus_line)
                # Check that current bus line has exactly one Start and one Finish
                stop_type_s = False
                stop_type_f = False
                current_bus_line_stops = [stop for stop in self.db if stop["bus_id"] == current_bus_line]
                for current_stop in current_bus_line_stops:
                    stop_type = current_stop["stop_type"]
                    if stop_type == "S":
                        if not stop_type_s:
                            stop_type_s = True
                        else:
                            # Bus line has more than one Start stop
                            print(f"There is no start or end stop for the line: {current_bus_line}.")
                            return False
                    elif stop_type == "F":
                        if not stop_type_f:
                            stop_type_f = True
                        else:
                            # Bus line has more than one Finish stop
                            print(f"There is no start or end stop for the line: {current_bus_line}.")
                            return False
                if not stop_type_s or not stop_type_f:
                    # Bus line has missing Start or Finish stop
                    print(f"There is no start or end stop for the line: {current_bus_line}.")
                    return False
        return True

    def check_arrive_time(self) -> 'checks if arrive times are increasing and prints result':
        wrong_lines_stop = dict()  # dict to store wrong lines and the stop with wrong arrive time
        current_bus_line = self.db[0]["bus_id"]
        previous_a_time = ""
        # Iterate over all the stops
        for stop in self.db:
            # Current bus line
            if stop["bus_id"] == current_bus_line:
                if current_bus_line not in wrong_lines_stop:
                    # Check if it's a wrong stop to add it to wrong_lines_stop dict
                    if stop["a_time"] <= previous_a_time:
                        wrong_lines_stop[current_bus_line] = stop["stop_name"]
                    previous_a_time = stop["a_time"]
                else:
                    continue
            # Next bus line
            else:
                current_bus_line = stop["bus_id"]
                previous_a_time = stop["a_time"]
        # Print result
        print("Arrival time test:")
        if not wrong_lines_stop:
            print("OK")
        else:
            for bus_id, stop_name in wrong_lines_stop.items():
                print(f"bus_id line {bus_id}: wrong time on station {stop_name}")


database = json.loads(input())
stop_data_validator = BusStopDataAnalyzer(database)
stop_data_validator.check_arrive_time()
