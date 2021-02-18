#!/usr/bin/env python3

import asyncio
import websockets
import json
import sys
import os
import time
import argparse
import logging
import signal


def sigterm_handler(signal, frame):
    # save the state here or do whatever you want
    outputfile = open("/quad9-intel-data/container.txt","a",encoding="utf-8")
    outputfile.write("caught termination\n") 
    outputfile.close()   
    print('booyah! bye bye')
    WriteResultDataToFile(Quad9Data,False)
    sys.exit(0)

 

signal.signal(signal.SIGTERM, sigterm_handler)
signal.signal(signal.SIGINT, sigterm_handler)

#
# Connect to the Quad9 threat-intel api and receive domain block information
# You receive the auth_token from Quad9 and it is specific to a threat feed.
#
# Requires Python version 3.6 or greater
#
# usage:
#     ./tia_example.py  --auth_token <YOUR TOKEN>
#         This measures download speed
#
#     ./tia_example.py  --verbose  --auth_token <YOUR TOKEN>
#         To see the data being retrieved.

# Quad9Data = []
Quad9Data = {}
Quad9DataTotalElements = {}
websocket = {}

start = {}
end = {}
count = {}

def WriteResultDataToFile(parsed_data,local):
  global args
  global write_line_counter

  if args.output_dir:
    prepend_directory = args.output_dir
  else:
    prepend_directory = "./"
  
  if args.output_to_test:
      prepend_filename = "test_quad9."
  else:
      prepend_filename = "quad9."
  
  write_line_counter = 0
  
  write_start_time = time.perf_counter()
  #print("parsed data = " + str(parsed_data))
  #print("Start time - " + str(write_start_time))
  if not local:
    for key in parsed_data:
      #print("parsed_data[key] = " + str(parsed_data[key][0]))
          
      for timestamp in parsed_data[key]:
        parsed_file = open(prepend_directory + prepend_filename + timestamp + ".json","a",encoding="utf-8")
        for entries in parsed_data[key][timestamp]:
          #print(key, item)
          parsed_file.write(entries)
          write_line_counter += 1
        
        parsed_file.close()
  else:
    for timestamp in parsed_data:
      parsed_file = open(prepend_directory + prepend_filename + timestamp + ".json","a",encoding="utf-8")
      for entries in parsed_data[timestamp]:
        #print(key, item)
        parsed_file.write(entries)
        write_line_counter += 1
      
      parsed_file.close()
    
  write_end_time = time.perf_counter()
  #print("End time - " + str(write_end_time))
  #print(str(write_line_counter))
  
  print(f'Written lines {write_line_counter}, processing speed {write_line_counter/(write_end_time-write_start_time)}/sec')
  
  #write_end_time = 0
  #write_start_time = 0
  #write_line_counter = 0
  
  #print(str(write_line_counter))

async def readblockloop(connection_id):
    
    #logger = logging.getLogger('websockets')
    #logger.setLevel(logging.DEBUG)
    #logger.addHandler(logging.StreamHandler())
    #print("starting async with websockets")
    async with websockets.connect(args.connect_url,
            extra_headers={'Authorization': 'Token ' + args.auth_token}) as ws:
        #print("in async with websockets")
        global websocket
        global count
        global start
        global end
        
        count[connection_id] = 0
        start[connection_id] = time.perf_counter()
        
        global Quad9Data
        
        websocket[connection_id] = ws
        
        print("websocket = " + str(websocket[connection_id]))
        while True:
            try:
                
                message = await websocket[connection_id].recv()
                
                data = json.loads(message)
                
                if args.verbose:
                    print(f" {data}")
                #f.write(str(data) + "\n")
                
                line_timestamp = data["timestamp"][0:13].replace("T","H")
                
                
                if connection_id not in Quad9Data:
                  Quad9Data[connection_id] = {}
                  
                if line_timestamp not in Quad9Data[connection_id]:
                  Quad9Data[connection_id][line_timestamp] = []

                Quad9Data[connection_id][line_timestamp].append(message)
                Quad9DataTotalElements[connection_id] += 1
                
                
                if Quad9DataTotalElements[connection_id] % 100000 == 0:
                  WriteResultDataToFile(Quad9Data[connection_id],True)
                  Quad9Data[connection_id] = {}
                  Quad9DataTotalElements[connection_id] = 0
                
                
                # We do our processing here. Just a count per connection.
                count[connection_id] = count[connection_id] + 1
                if (count[connection_id] % 10000 == 0):
                    end[connection_id] = time.perf_counter()
                    print(f'Readblock{connection_id} {count[connection_id]} {count[connection_id]/(end[connection_id]-start[connection_id])}/sec')
                
                ack = dict(id=data['id'])


                if not args.noack:
                  await acks[connection_id].put(ack)
                #print(f" acks: {acks}")
            except Exception as e:
                print(type(e))
                print(e.args)
                print('Failed to receive message')
                break

async def process_acks(connection_id):
    global acks
    while True:
        ack = await acks[connection_id].get()
        try:
            await send_data(connection_id,ack)
        except:
            print('Connection ID = ' + str(connection_id) + ': Failed to send ack')
            break

async def send_data(connection_id,data):
    frame = json.dumps(data)
    global websocket
    await websocket[connection_id].send(frame)


def main():
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='Read from Quad9 threat-intel api')

    parser.add_argument('--verbose', action='store_true',
                        help='Dump out received json')

    parser.add_argument('--noack', action='store_true',
                        help='Disable acks so no data is confirmed read. Primarily for testing')

    # Optional arguments
    parser.add_argument('--auth_token', default="Token <YOUR TOKEN>",
                        help='Authorization token from quad9 to access the api')

    parser.add_argument('--connect_url', default='wss://tiapi.quad9.net',
                        help='url to access the api')
	
    parser.add_argument('--connections', default='1',
                        help='number of connections to establish to Quad9')
                        
    parser.add_argument('--output_to_test', action='store_true',
                        help='Prefix output files with "test_" so as to not affect production files. Useful for troubleshooting.')      
                        
    parser.add_argument('--output_dir', default='',
                        help='Send output into files in output_dir - make sure to include trailing slash.')
                        
    print("Encoding --> " + sys.getfilesystemencoding())
    
    global args
    args = parser.parse_args()
    print(args.connections);
    
    connections=int(args.connections)
    tasks = []
    if args.connections:
      for conn_number in range(0,connections):
        tasks.append(asyncio.ensure_future(readblockloop(conn_number)))
        tasks.append(asyncio.ensure_future(process_acks(conn_number)))
        
    global Quad9Data
    global count
    global start
    global end
    global acks
    
    acks = {}
    
    for i in range(0,connections):
      Quad9Data[i] = {}
      count[i] = {}
      start[i] = {}
      end[i] = {}
      websocket[i] = {}
      Quad9DataTotalElements[i] = 0
      acks[i] = asyncio.Queue()
  
    
      
    asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))
    
    #print(Quad9Data)

   
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        WriteResultDataToFile(Quad9Data,False)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

