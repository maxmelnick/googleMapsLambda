# googleMapsLambda

Code that can be deployed as an AWS Lambda function to log commute times from home to work to an s3 bucket. You can then use AWS Athena to query the data in s3.

## Local Development

Configure following environment variables:
- `GMAPS_BUCKET_NAME` (s3 bucket name to store data)
- `GMAPS_BUCKET_PATH` (s3 bucket path (e.g.,  folder) to store data)
- `HOME_ADDRESS`
- `WORK_ADDRESS`
- `GMAPS_API_KEY` ([Google Maps API Key](https://developers.google.com/maps/documentation/directions/) - note: you need to enable the directions API)

>[This site](http://www.dowdandassociates.com/blog/content/howto-set-an-environment-variable-in-mac-os-x-terminal-only/) explains how to set environment variables in the Mac terminal

```
# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

## Additional Lambda Configuration Requirements/Examples

* *Trigger:* Cloudwatch cron expression for Eastern time morning and evening commute times (note: Cloudwatch works in UTC) = `cron(0,15,30,45 11,12,13,19,20,21,22,23 ? * MON-FRI *)`
* *Function Code >> Handler:* `main.lambda_handler`
* *Environment variables:* see above
* *Execution role:* needs an AWS IAM role that has write access to the s3 bucket.

## Make Zip file for AWS Lambda Deployment

```
# create a directory for build assets
mkdir build

# install python dependencies to build directory
pip install -t $PWD/build -r requirements.txt

# copy src files to build directory
cp main.py $PWD/build/.

# create zip file
zip -r ./build/googleMapsLambda.zip ./build/*
```

