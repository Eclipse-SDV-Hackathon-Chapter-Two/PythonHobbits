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
from numpy import mean, var, diff
from stability_score import VehicleStabilityAnalyzer

logger = logging.getLogger("Health App")
stdout = logging.StreamHandler(stream=sys.stdout)
stdout.setLevel(logging.INFO)
logger.addHandler(stdout)
logger.setLevel(logging.INFO)

score = {
        "timestamp":0,
        "quick_acc":0,
        "quick_dec":0,
        "jerk":0,
        "rash":0
        }

# Callback for receiving messages

def detect_rash_driving(acceleration_data, window_size=120):
    # Assuming acceleration_data is a list of acceleration values     
    max_acc = max(acceleration_data)
    max_dec = min(acceleration_data)
    variance = var(acceleration_data)
    jerk = diff(acceleration_data).max()
    print(max_acc, max_dec, variance, jerk)
    # Example thresholds
    if (max_acc > 3.0):
        score["quick_acc"] = score["quick_acc"]+1
    if (max_dec < -3.0 ):
        score["quick_dec"] = score["quick_dec"]+1
    if (variance > 2.0 or jerk > 2.5):
        score["jerk"] = score["jerk"] + 1

def acc_process_signals(speed_input_queue):
    acc_ = []
    avg_var = []
    while True:
        if not acc_input_queue.empty():
            signal = acc_input_queue.get()
            acc_.append(signal)
            if len(acc_)==120:
                detect_rash_driving(acc_)

def save_vehicle_data_func(data_input_queue):
    speed = 0
    global_time = 0
    start_time =0
    count = 0
    start = True
    while True:
        if not data_input_queue.empty():
            signal = data_input_queue.get()
            if start:
                start_time = signal[0]
                start = False
            if signal[1] <=0.5 and count == 0:
                global_time = signal[0]
                speed +=1
                # speed.append(signal[1])
                count +=1
            if signal[1] <=0.5:
                speed+=1
            if signal[1] >0.5:
                global_time = 0
                speed = 0
            if speed >= 115:
                current_time = signal[0]
                if (current_time - global_time)/1e6 == 600:
                    with open("health.json", 'w') as file:
                        score["timestamp"] = current_time
                        health.send(str(score))
                        logger.info(f"[Health app]:{score}")
                        json.dump(score, file, indent=4)
                        score = {"timestamp":0,"quick_acc":0,"quick_dec":0,"jerk":0,"rash":0}
                speed = []

def stability_process_signals(signal_queue):
    analyzer = VehicleStabilityAnalyzer()
    yaw, steer, latacc = [], [],[]
    while True:
        if not signal_queue.empty():
            signal = signal_queue.get()
            yaw.append(signal[0])
            steer.append(signal[1])
            latacc.append(signal[2])
            
            if len(yaw) == 120:
                analyzer.add_vehicle_data(yaw, steer, latacc)
                stability_result = analyzer.calculate_stability_metrics()
                if stability_result["driver_alert"]["severity"] == "HIGH" or stability_result["driver_alert"]["severity"] == "CRITICAL" :
                    score["rash"]+=1
                yaw, steer, latacc = [], [],[]

def vehicle_callback(topic_name, msg, time):
    try:
        json_msg = json.loads(msg)
        acc_input_queue.put(json_msg["signals"]["longAcc"])

        data_input_queue.put((json_msg["header"]["timestamp"],
                              json_msg["signals"]["speed"]))
        
        stability_input_queue.put((json_msg["signals"]["yawrate"],
                             json_msg["signals"]["steeringWheelAngle"],
                             json_msg["signals"]["latAcc"]))
    except json.JSONDecodeError:
        logger.error(f"Error: Could not decode message: '{msg}'")
    except Exception as e:
        logger.error(f"Error: {e}")


if __name__ == "__main__":

    acc_input_queue = mp.Queue()
    stability_input_queue = mp.Queue()
    data_input_queue = mp.Queue()

    logger.info("Starting Health app...")

    # Initialize eCAL
    ecal_core.initialize(sys.argv, "Health App")

    acc_signals_process = mp.Process(target=acc_process_signals, args=(acc_input_queue,))
    acc_signals_process.start()

    stability_signals_process = mp.Process(target=stability_process_signals, args=(stability_input_queue,))
    stability_signals_process.start()

    save_vehicle_data = mp.Process(target=save_vehicle_data_func, args=(data_input_queue,))
    save_vehicle_data.start()

    # Create a subscriber that listens on the "traffic_sign_detection"
    vehicle = StringSubscriber("vehicle_dynamics")
    stability = StringSubscriber("vehicle_dynamics")
    health = StringPublisher("health")


    # Set the Callback
    vehicle.set_callback(vehicle_callback)
    
    # Just don't exit
    while ecal_core.ok():
        time.sleep(0.5)
    
    # finalize eCAL API
    ecal_core.finalize()