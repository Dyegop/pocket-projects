import sys
import os
import time
from dataclasses import dataclass
from collections import Counter
from typing import List

@dataclass
class LogRow:
    """
    Class representation of a row in a logfile from https://www.secrepo.com/squid/access.log.gz
    This class is intented to be used as part of LogFile class.
    """
    timestamp: float
    header_size: int
    ip_address: str
    response_code: str
    response_size: int
    request_method: str
    url: str
    username: str
    access_destination_type: str
    response_type: str

    def __getitem__(self, item):
        return getattr(self, item)



class LogFile:
    """
    Class representation of a LogFile.
    This class parse log file https://www.secrepo.com/squid/access.log.gz and allows you to get additional information.
    """
    def __init__(self, log_filepath: str, ignore_headers: bool = True):
        self.log_filepath: str = log_filepath
        self.ignore_headers = ignore_headers  # added option to ignore first row (empty in this case)
        self.rows: dict = {}

        self._load_LogFile()  # Open log file

    def _load_LogFile(self) -> None:
        # I have intentionally avoided the use of non built-in libraries to parse log file.
        # utf-8 enconding is required in this exercise.
        with open(self.log_filepath, mode='r', encoding='utf-8') as f:
            lines = f.readlines()[1:] if self.ignore_headers else f.readlines()
            line_number = 1
            for line in lines:
                try:
                    line = line.split()
                    self.rows[line_number] = LogRow(timestamp=float(line[0]),
                                                    header_size=int(line[1]),
                                                    ip_address=line[2],
                                                    response_code=line[3],
                                                    response_size=int(line[4]),
                                                    request_method=line[5],
                                                    url=line[6],
                                                    username=line[7],
                                                    access_destination_type=line[8],
                                                    response_type=line[9])
                    line_number += 1
                except (ValueError, IndexError) as err:  # Only those exceptions have been found
                    print(f"Error parsing line {line_number}: {err}. Continue to next line")

            # A regex implementation could be considered in order to fully ensure that every field in the log file
            # comes as expected.

    def frequent_ip_addresses(self, frequency: str) -> List[str]:
        """
        Return the most/less frequent IP address.
        Several IPs may be returned if all of them shared the number of ocurrencies.
        """
        all_ip_address = [row['ip_address'] for row in self.rows.values()]
        # I use collections module since it is built-in and works pretty fast.
        # It also allows us to obtain other output, e.g three most frequent IP addresses.
        counter = Counter(all_ip_address).most_common()

        # Code below will check what IPs are the most frequent
        # If several IPs shared the same max frequency, it returns all of them.
        # For example, if three different IPs appear 100 times, all those three IPs will be returned.
        if frequency == 'most_common':
            max_freq = max([ip[1] for ip in counter])
            most_common_IPs = [ip[0] for ip in counter if ip[1] == max_freq]
            return most_common_IPs
        elif frequency == 'less_common':
            min_freq = min([ip[1] for ip in counter])
            least_common_IPs = [ip[0] for ip in counter if ip[1] == min_freq]
            return least_common_IPs
        else:
            return ["Incorrect value for arg frequency"]

    def events_per_second(self) -> float:
        """ Return the number of events per second that are logged. """
        # I assume this value corresponds to total_events/total_time.
        # I consider total_time the difference between the min and the max timestamps.
        max_timestamp = max([row['timestamp'] for row in self.rows.values()])
        min_timestamp = min([row['timestamp'] for row in self.rows.values()])
        total_time = max_timestamp - min_timestamp
        total_events = len(self.rows)
        return total_events/total_time

    def total_bytes(self) -> int:
        """ Return the total amount of bytes exchanged (response + response header). """
        # I assume total amount of bytes must include response header and response body
        total_header_size = sum([row['header_size'] for row in self.rows.values()])
        total_response_size = sum([row['response_size'] for row in self.rows.values()])
        return total_header_size + total_response_size



# FOR TESTING
if __name__ == '__main__':
    START_TIME = time.time()
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    log_file_obj = LogFile(f"{ROOT_DIR}\\access.log")
    print(f"Memory usage of log_file_obj: {sys.getsizeof(log_file_obj)}")

    for i in range(1, 11):
        try:
            print(log_file_obj.rows[1].timestamp)
        except KeyError:
            print(f"Line {i} not found")

    print(log_file_obj.frequent_ip_addresses('most_common'))
    print(log_file_obj.frequent_ip_addresses('less_common'))
    print(log_file_obj.events_per_second())
    print(log_file_obj.total_bytes())

    print(f"Finished in: {time.time() - START_TIME}")
