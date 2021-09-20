import os
import glob
import json
import uuid
import psycopg2

"""
usage: $ python dos-mock-requests.py
"""

number_of_requests = 5
maximum_origins = 1
maximum_destinations = 3000
minimum_destinations = 1
search_distance_meters = 60000
origin_easting = "448584"
origin_northing = "198826"
destination_volumes = [5, 50, 500, 1500, 3000]
output_directory = "rd_requests"

db_database = "pathwaysdos_dev"
db_user = "postgres"
db_password = "postgres"
db_host = "localhost"
db_port = "5432"


def create_requests():

    # create output directpry of not exists
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)
    else:
        # clear out output directory
        files = glob.glob(output_directory + "/*")
        for f in files:
            os.remove(f)

    # automate building of destination volumes?

    conn = get_db_connection()
    conn.execute(get_origin_sql(maximum_origins))
    origin = conn.fetchall()[0]

    request_num = 1
    for volume in destination_volumes:
        transaction_id = str(uuid.uuid4())
        conn.execute(get_services_for_radius_sql(origin[3], origin[4], volume))
        destinations = conn.fetchall()

        # build the request
        request = json.dumps(build_json_request(transaction_id, origin, destinations))

        # store the request
        filename = "rd_request_" + str(request_num) + ".json"
        filepath = output_directory + "/" + filename

        with open(filepath, "a") as f:
            f.write(request)
            f.close

        request_num += 1


def build_json_request(transaction_id, origin, destinations):
    destination_list = []

    index = 1
    for destination in destinations:
        entry = {"reference": "destination" + str(index), "latitude": destination[1], "longitude": destination[2]}

        destination_list.append(entry)
        index += 1

    request = {
        "transactionId": transaction_id,
        "origin": {"reference": "origin1", "latitude": origin[1], "longitude": origin[2]},
        "destinations": destination_list,
    }

    return request


def get_db_connection():
    conn = psycopg2.connect(database=db_database, user=db_user, password=db_password, host=db_host, port=db_port)

    return conn.cursor()


def get_origin_sql(limit):
    sql = (
        "select postcode, latitude, longitude, easting, northing from pathwaysdos.locations l where "
        "l.easting >= (" + origin_easting + " - 60000) "
        "and l.easting <= (" + origin_easting + " + 60000) "
        "and l.northing >= (" + origin_northing + " - 60000) "
        "and l.northing <= (" + origin_northing + " + 60000) "
        "and l.latitude is not null and l.longitude is not null order by random() limit " + str(limit) + ";"
    )

    return sql


def get_services_for_radius_sql(easting, northing, limit):

    meters = str(search_distance_meters)
    easting = str(easting)
    northing = str(northing)
    limit = str(limit)

    sql = (
        "select uid, latitude, longitude from pathwaysdos.services s where "
        "s.easting >= (" + origin_easting + " - " + meters + ") "
        "and s.easting <= (" + origin_easting + " + " + meters + ") "
        "and s.northing >= (" + origin_northing + " - " + meters + ") "
        "and s.northing <= (" + origin_northing + " + " + meters + ") "
        "and s.latitude is not null and s.longitude "
        "is not null order by random() limit  " + limit + ";"
    )
    return sql


if __name__ == "__main__":
    create_requests()
