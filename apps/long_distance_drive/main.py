# Copyright (c) 2024 Elektrobit Automotive GmbH and others

# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# SPDX-License-Identifier: Apache-2.0

import sys, time, json, logging
from datetime import datetime, timedelta
import ecal.core.core as ecal_core
from ecal.core.subscriber import StringSubscriber
from ecal.core.publisher import StringPublisher
import multiprocessing as mp
import time
import numpy as np

logger = logging.getLogger("long_distance_detection")
stdout = logging.StreamHandler(stream=sys.stdout)
stdout.setLevel(logging.INFO)
logger.addHandler(stdout)
logger.setLevel(logging.INFO)

def long_distance_analysis(data_input_queue):
    stop = 0
    global_time = 0
    start_time =0
    count = 0
    start = True
    while True:
        if not data_input_queue.empty():
            signal = data_input_queue.get()
            if start:
                start_time = signal[0]
                end_time = start_time + 600_000_00 #simulating 1 minute of stop
                start = False
            if signal[1] <=0.5 and count == 0:
                global_time = signal[0]
                stop +=1
                count +=1
            if signal[1] <=0.5:
                stop+=1
            if signal[1] >0.5:
                global_time = 0
                stop = 0
            if signal[0] == end_time:
                if stop != 1150:
                    longdistance.send("Driver needs rest...")
                    logger.info(f"[Long Distance app]:Driver needs rest")

# Callback for receiving messages
def speed_callback(topic_name, msg, time):
    try:
        json_msg = json.loads(msg)
        speed_input_queue.put((json_msg["header"]["timestamp"], json_msg["signals"]["speed"]))
    except json.JSONDecodeError:
        logger.error(f"Error: Could not decode message: '{msg}'")
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    speed_input_queue = mp.Queue()
    logger.info("Starting example app...")

    # Initialize eCAL
    ecal_core.initialize(sys.argv, "Example App")

    # Create a subscriber that listens on the "traffic_sign_detection"
    vehicle = StringSubscriber("vehicle_dynamics")
    longdistance = StringPublisher("longdistance")

    # # Start the signal processing process
    process_signals_process = mp.Process(target=long_distance_analysis, args=(speed_input_queue,))
    process_signals_process.start()

    # Set the Callback
    vehicle.set_callback(speed_callback)
    
    # Just don't exit
    while ecal_core.ok():
        time.sleep(0.5)
    
    # finalize eCAL API
    ecal_core.finalize()