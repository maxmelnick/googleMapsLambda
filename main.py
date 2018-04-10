import googlemaps
from datetime import datetime
import os
import boto3
import logging
import json

# set up logging
logger = logging.getLogger('PyGoogleMaps')
logger.setLevel(logging.INFO)
if not len(logger.handlers):
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - ' +
                                  '%(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)


gmapsApiKey = os.getenv("GMAPS_API_KEY")

gmaps = googlemaps.Client(key=gmapsApiKey)

def getDirectionDuration(startLocation, endLocation):
	logger.info("Retrieving driving duration from Google Maps")
	directions_result = gmaps.directions(startLocation, endLocation)

	leg = directions_result[0]["legs"][0]
	duration = leg["duration"]

	result = {
		"utcTime": datetime.utcnow().isoformat(),
		"durationText": duration["text"],
		"durationSecs": duration["value"],
		"endAddress": leg["end_address"],
		"endLocation": leg["end_location"],
		"startAddress": leg["start_address"],
		"startLocation": leg["start_location"]
	}

	return result

def write_s3_file(data):
    logger.info("Writing file to S3.")
    bucket = os.getenv("GMAPS_BUCKET_NAME")
    path = os.getenv("GMAPS_BUCKET_PATH")
    s3 = boto3.client('s3')
    # data = json.dumps(data, indent=0)
    outData = ""
    for record in data:
        outData = outData + json.dumps(record) + "\n"
    date = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")
    s3.put_object(Bucket=bucket, Key="%s/%s.json" % (path, date), Body=outData)


def log_driving_duration():
    logger.info("Starting function to get driving duration")

    locationA = os.getenv("HOME_ADDRESS")
    locationB = os.getenv("WORK_ADDRESS")
    durations = []
    durations.append(getDirectionDuration(locationA, locationB))
    durations.append(getDirectionDuration(locationB, locationA))

    # write out file
    write_s3_file(durations)

    logger.info("Finished logging driving duration")


def lambda_handler(event=None, context=None):
    """ main Lambda event handling loop """
    log_driving_duration()


if __name__ == "__main__":
    log_driving_duration()

# directions_json = json.dumps(directions_result, sort_keys=True, indent=4, separators=(',', ': '))
# print(directions_json)

