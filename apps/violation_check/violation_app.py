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

import ecal.core.core as ecal_core
from ecal.core.subscriber import StringSubscriber
from ecal.core.publisher import StringPublisher
import multiprocessing as mp
import time
from numpy import mean

logger = logging.getLogger("example_app")
stdout = logging.StreamHandler(stream=sys.stdout)
stdout.setLevel(logging.INFO)
logger.addHandler(stdout)
logger.setLevel(logging.INFO)

speed_check = {
                "4": 10,
                "5": 100,
                "6": 130,
                "7": 20,
                "8": 30,
                "9": 40,
                "10": 5,
                "11": 50,
                "12": 60,
                "13": 70,
                "14": 80,
                "15": 90,
                "56":120}

warning_check = {
                "41": "warning_children",
                "42": "warning_construction",
                "43": "warning_crosswalk",
                "44": "warning_cyclists",
                "45": "warning_domestic_animals",
                "46": "warning_other_dangers",
                "47": "warning_poor_road_surface",
                "48": "warning_roundabout",
                "49": "warning_slippery_road",
                "50": "warning_speed_bumper",
                "51": "warning_traffic_light",
                "52": "warning_tram",
                "53": "warning_two_way_traffic",
                "54": "warning_wild_animals",
                "57": "warning_priority_at_next_intersection",
                "58": "prohibitory_no_vehicles",
                "59": "warning_bend",
                "60": "warning_road_narrows",
                "61": "warning_traffic_jam",
                "62": "warning_icy_road"
                }

# Callback for receiving messages


def traffic_process_signals(traffic_input_queue):
    traffic_signs = []
    while True:
        if not traffic_input_queue.empty():
            signal = traffic_input_queue.get()
            if signal in warning_check:
                print(warning_check[signal])

def speed_process_signals(speed_input_queue):
    """
    Speed signal is sampled at 20Hz, to monitor the speed change every 1 second
    """
    speed_ = []
    while True:
        if not speed_input_queue.empty():
            signal = speed_input_queue.get()
            speed_.append(signal)

            if len(speed_)==20:
                avg_speed = mean(speed_)
                #Tolerance value for speed is +/- 2.5
                upper_limit = avg_speed + 2.5
                lower_limit = avg_speed - 2.5
                if not traffic_input_queue.empty():
                    #desired speed is taken from the traffic signal detection
                    desiredSpeed = traffic_input_queue.get()
                    if desiredSpeed<= lower_limit:
                        logger.info("[Violation app]: Maintain optimum speed limit...")
                        violation.send("Maintain optimum speed limit...")
                        # print("Maintain optimum speed limit...")
                    if desiredSpeed>= upper_limit:
                        logger.info("[Violation app]: Too Fast reduce the speed...")
                        violation.send("Too Fast reduce the speed...")
                        # print("Too Fast reduce the speed")
                speed_ =[] 

def vehicle_callback(topic_name, msg, time):
    try:
        json_msg = json.loads(msg)
        speed_input_queue.put(json_msg["signals"]["speed"])
    except json.JSONDecodeError:
        logger.error(f"Error: Could not decode message: '{msg}'")
    except Exception as e:
        logger.error(f"Error: {e}")

def traffic_callback(topic_name, msg, time):
    try:
        json_msg = json.loads(msg)
        for index, val in enumerate(json_msg["confidences"]):
            #Detection with >50% confidence are taken into consideration
            if val>=0.5:
                if json_msg["class_ids"][index] in warning_check:
                    traffic_input_queue.put(json_msg["class_ids"][index])
                if json_msg["class_ids"][index] in speed_check:
                    speed_limit_queue.put(json_msg["class_ids"][index])
    except json.JSONDecodeError:
        logger.error(f"Error: Could not decode message: '{msg}'")
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":

    traffic_input_queue = mp.Queue()
    speed_input_queue = mp.Queue()
    speed_limit_queue = mp.Queue()
    logger.info("Starting violation check app...")

    # Initialize eCAL
    ecal_core.initialize(sys.argv, "violation check")

    traffic_signals_process = mp.Process(target=traffic_process_signals, args=(traffic_input_queue,))
    traffic_signals_process.start()

    speed_signals_process = mp.Process(target=speed_process_signals, args=(speed_input_queue,))
    speed_signals_process.start()

    # Create a subscriber that listens on the "traffic_sign_detection"
    traffic = StringSubscriber("traffic_sign_detection")
    vehicle = StringSubscriber("vehicle_dynamics")

    violation = StringPublisher("violations")


    # Set the Callback
    traffic.set_callback(traffic_callback)
    vehicle.set_callback(vehicle_callback)
    
    # Just don't exit
    while ecal_core.ok():
        time.sleep(0.5)
    
    # finalize eCAL API
    ecal_core.finalize()