
import sys
import json
import time
from log_file import LogFile



if __name__ == "__main__":

    if len(sys.argv) == 2:
        log_filepath = sys.argv[1]

        print("----- Welcome to log analyzer tool -----")
        print("----- Log file downloaded from: https://www.secrepo.com/squid/access.log.gz -----")
        print("Loading log file...")

        try:
            log_file_obj = LogFile(log_filepath)
        except FileNotFoundError:
            print("File not found. Exiting...")
            raise sys.exit(1)
        else:
            print("Done")

        print("Analyzing log data...")
        most_frequent_IPs = log_file_obj.frequent_ip_addresses('most_common')
        least_frequent_IPs = log_file_obj.frequent_ip_addresses('less_common')
        events_per_sec = log_file_obj.events_per_second()
        bytes_exchanged = log_file_obj.total_bytes()
        print("Done")

        print("Saving data to json file...")
        with open('output/log_output.json', 'w') as outfile:
            now = time.strftime('%Y-%m-%dT:%H:%M:%S')
            json.dump({f'output_{now}': {'most_frequent_IPs': most_frequent_IPs,
                                         'least_frequent_IPs': least_frequent_IPs,
                                         'events_per_sec': events_per_sec,
                                         'bytes_exchanged': bytes_exchanged}}, outfile)

    else:
        print("At least one argument is expected")
        print("Please, provide path to your log file")
        raise sys.exit(1)

    print("Done")
