# How to operate this heavy machinery
 
## First create the image from Dockerfile
`
docker build -t calvin/quad9-threat-intel:2.3 -f Dockerfile .
`

## Create the container
`
docker create -v /projects/quad9-threat-intel-api/scripts/:/scripts/ -v /quad9-intel-data/:/quad9-intel-data/ calvin/quad9-threat-intel:2.3 /scripts/start.sh
`
## Update API Environment variables

Edit the start.sh script and insert your API token and number of connections needing to be made to Quad9

`
QUAD9_API_TOKEN=<INSERT API TOKEN>
QUAD9_CONNECTIONS=<NUMBER OF CONNECETIONS>
`

## To start the container
`docker start <container name>`

## To stop the container

`docker stop <container name>`


### Potential improvements on the horizon...who knows? ¯\_(ツ)_/¯
* Multiprocessing in addition to multithreading (is this worthwhile given that multiple containers can be spun up to create "multiprocessing".
* other?
