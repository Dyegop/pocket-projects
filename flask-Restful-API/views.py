import park_data
from flask_restful import Resource
from flask import request, abort
from typing import List


# Parks object
parks = park_data.Parks("./input/park_info.csv")


# Help function
def _get_paginated_list(results: List, url_arg: str, start: str, limit: str) -> dict:
    """
    Returns a range of data from a list that is intended to be paginated for an API response.
    The start and limit parameters define the range of data that is returned.

    :param results: a list of results to have paginated
    :param url_arg: based API url.
    :param start: page number (from 1 to the last value, e.g 1 to 99)
    :param limit: max number of results per page
    :return: a dictionary with the response data
    """

    start = int(start)
    limit = int(limit)
    count = len(results)

    if count < start or limit < 0:
        abort(404)

    response = {'count': count, 'limit': limit, 'start': start}

    # Previous URL
    if start == 1:
        response['previous'] = ''
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        response['previous'] = f'{url_arg}?start={start_copy}&limit={limit_copy}'

    # Next URL
    if start + limit > count:
        response['next'] = ''
    else:
        start_copy = start + limit
        response['next'] = f'{url_arg}?start={start_copy}&limit={limit}'

    # Extract result according to bounds
    response['results'] = results[(start - 1):(start - 1 + limit)]

    return response



class ParksListAPI(Resource):
    def get(self):
        response_data = []

        # Request arguments (we are not validating data in this practice)
        start_date_arg = request.args.get('start_date')   # start_date filter for production datetimes
        end_date_arg = request.args.get('end_date')       # end_date filter for production datetimes
        start_arg = request.args.get('start', '1')    # initial value for pagination
        limit_arg = request.args.get('limit', '100')  # set the max number of rows for 'production' (100 by default)

        for park in parks.park_list:
            # Load park data
            parks.load_park(park, f'./input/{park}.csv')

            # Get park production
            if start_date_arg and end_date_arg:
                park_production = ([{'datetime': row['datetime'], 'MW': row['MW']}
                                    for index, row in parks[park].production.iterrows()
                                    if start_date_arg <= row['datetime'][0:10] <= end_date_arg])
            else:
                park_production = [{'datetime': row['datetime'],
                                    'MW': row['MW']} for index, row in parks[park].production.iterrows()]

            response_data.append({
                    'park_name': park,
                    'timezone': parks[park].timezone,
                    'energy_type': parks[park].energy_type,
                    'production': (_get_paginated_list(park_production, "/parks", start_arg, limit_arg)
                                   if park_production else {"count": 0,
                                                            "limit": limit_arg,
                                                            "start": start_arg,
                                                            "previous": "",
                                                            "next": "",
                                                            "results": []
                                                            }
                                   )
            })

        return {'parks': response_data}, 200


class ParkAPI(Resource):
    def get(self, park: str):
        # Capitalize park arg for compatibility
        park = park.capitalize()

        # Request arguments (we are not validating data in this practice)
        start_date_arg = request.args.get('start_date')
        end_date_arg = request.args.get('end_date')
        start_arg = request.args.get('start', '1')
        limit_arg = request.args.get('limit', '100')

        if park in parks.park_list:
            # Load park data
            parks.load_park(park, f'./input/{park}.csv')

            # Get park production
            if start_date_arg and end_date_arg:
                park_production = ([{'datetime': row['datetime'], 'MW': row['MW']}
                                    for index, row in parks[park].production.iterrows()
                                    if start_date_arg <= row['datetime'][0:10] <= end_date_arg])
            else:
                park_production = [{'datetime': row['datetime'],
                                    'MW': row['MW']} for index, row in parks[park].production.iterrows()]

            response_data = {
                'park_name': park,
                'timezone': parks[park].timezone,
                'energy_type': parks[park].energy_type,
                'production': (_get_paginated_list(park_production, "/parks", start_arg, limit_arg)
                               if park_production else {"count": 0,
                                                        "limit": limit_arg,
                                                        "start": start_arg,
                                                        "previous": "",
                                                        "next": "",
                                                        "results": []
                                                        }
                               )
            }

            return {'park': response_data}, 200

        else:
            return {
                "error": {
                    "code": 404,
                    "message": "Park not found"
                }
            }
