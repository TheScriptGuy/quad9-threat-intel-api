# How to operate this heavy machinery
 
## First create the image from Dockerfile
`
docker build -t <REPO>/quad9-threat-intel:<version> -f Dockerfile .
`

## Initial setup
Create the directory where you want the data to be downloaded to
`
mkdir /quad9-intel-data
`

Assuming scripts directory is in /quad9-threat-intel-api



## Create the container
`
docker create -v /quad9-threat-intel-api/scripts/:/scripts/ -v /quad9-intel-data/:/quad9-intel-data/ <REPO>/quad9-threat-intel:<version> /scripts/start.sh
`

## Update API Environment variables

Edit the start.sh script and insert your API token and number of connections needing to be made to Quad9

* `QUAD9_API_TOKEN=<INSERT API TOKEN>`
* `QUAD9_CONNECTIONS=<NUMBER OF CONNECETIONS>`

## Info to know about the python script

The python script writes the downloaded content into the /quad9-intel-data directory in the filename format of quad9.Year-Month-DayHHour.json
* quad9.2021-01-01H05.json  
* quad9.2021-01-01H22.json  
* quad9.2021-01-02H15.json 

The python script outputs content to files in chunks of 100,000 entries. If the script crashes, or the container stops, the variables in memory are output to disk according to the format above.

## To start the container
`docker start <container name>`

## To stop the container

`docker stop <container name>`


### Potential improvements on the horizon...who knows? ¯\_(ツ)_/¯
* Multiprocessing in addition to multithreading (is this worthwhile given that multiple containers can be spun up to create "multiprocessing"?)
* other?
