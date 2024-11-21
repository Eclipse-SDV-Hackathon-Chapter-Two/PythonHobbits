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
# import yaw_detection as yd
from stability_score import VehicleStabilityAnalyzer

logger = logging.getLogger("example_app")
stdout = logging.StreamHandler(stream=sys.stdout)
stdout.setLevel(logging.INFO)
logger.addHandler(stdout)
logger.setLevel(logging.INFO)

def stability_process_signals(signal_queue):
    analyzer = VehicleStabilityAnalyzer()
    yaw, steer, latacc = [], [],[]
    while True:
        if not signal_queue.empty():
            signal = signal_queue.get()
            yaw.append(signal[0])
            steer.append(signal[1])
            latacc.append(signal[2])
            
            if len(yaw) == 60:
                analyzer.add_vehicle_data(yaw, steer, latacc)
                stability_result = analyzer.calculate_stability_metrics()
                logger.info(f"[Stability app]:{stability_result}")
                # print(stability_result["driver_alert"])
                stabilityapp.send(str(stability_result["driver_alert"]))
                yaw, steer, latacc = [], [],[]

# Callback for receiving messages
def vehicle_callback(topic_name, msg, time):
    try:
        json_msg = json.loads(msg)
        stability_input_queue.put((json_msg["signals"]["yawrate"],
                             json_msg["signals"]["steeringWheelAngle"],
                             json_msg["signals"]["latAcc"]))
        # print(f"Received: {msg}")
    except json.JSONDecodeError:
        logger.error(f"Error: Could not decode message: '{msg}'")
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    stability_input_queue = mp.Queue()
    logger.info("Starting Stability app...")

    # Initialize eCAL
    ecal_core.initialize(sys.argv, "Stability App")

    # Create a subscriber that listens on the "traffic_sign_detection"
    vehicle = StringSubscriber("vehicle_dynamics")
    stabilityapp = StringPublisher("stability")

    # record_process = mp.Process(target=record_signal, args=(speed_input_queue,))
    # record_process.start()

    # Start the signal processing process
    process_signals_process = mp.Process(target=stability_process_signals, args=(stability_input_queue,))
    process_signals_process.start()

    # Set the Callback
    vehicle.set_callback(vehicle_callback)
    
    # Just don't exit
    while ecal_core.ok():
        time.sleep(0.5)
    
    # finalize eCAL API
    ecal_core.finalize()