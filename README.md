# How to operate this heavy machinery

First and foremost an honorary mention of the original Quad9 threat-intel-api https://github.com/Quad9DNS/threat-intel-api

I used their python script as a starting point and built on from there.

The Docker container things I worked on myself.

I'm open to positive feedback/input.

Now onwards to the instructions! Avante!
 

## First create the image from Dockerfile
```bash
docker build -t <REPO>/quad9-threat-intel:<version> -f Dockerfile .
```

## Initial setup
Create the directory where you want the data to be downloaded to
```bash
mkdir /quad9-intel-data
```

Assuming scripts directory is in /quad9-threat-intel-api



## Create the container
```bash
docker create -v /quad9-threat-intel-api/scripts/:/scripts/ \
              -v /quad9-intel-data/:/quad9-intel-data/ \
              <REPO>/quad9-threat-intel:<version> /scripts/start.sh
```

## Update API Environment variables

Edit the start.sh script and insert your API token and number of connections needing to be made to Quad9

```bash
QUAD9_API_TOKEN=<INSERT API TOKEN>
QUAD9_CONNECTIONS=<NUMBER OF CONNECETIONS>
```


## Info to know about the python script

The python script writes the downloaded content into the /quad9-intel-data directory in the filename format of 
quad9.Year-Month-DayHHour.json

Example file names:
* quad9.2021-01-01H05.json  
* quad9.2021-01-01H22.json  
* quad9.2021-01-02H15.json 

The python script outputs content to files in chunks of 100,000 entries. If the script crashes, or the container stops, the variables in memory are output to disk according to the format above.

## To start the container
```bash
docker start <container name>
```

## To stop the container
```bash
docker stop <container name>
```


### Potential improvements on the horizon...who knows? ¯\_(ツ)_/¯
* Multiprocessing in addition to multithreading (is this worthwhile given that multiple containers can be spun up to create "multiprocessing"?)
* other?
