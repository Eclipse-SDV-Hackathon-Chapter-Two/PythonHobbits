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

from ankaios_sdk import Workload, Ankaios, WorkloadStateEnum, WorkloadSubStateEnum, AnkaiosLogLevel, Manifest, Request, CompleteState
import paho.mqtt.client as mqtt
import json
import os
import logging
import sys
import time

logger = logging.getLogger("symphony_provider")
stdout = logging.StreamHandler(stream=sys.stdout)
stdout.setLevel(logging.INFO)
logger.addHandler(stdout)
logger.setLevel(logging.INFO)

BROKER = os.environ.get('MQTT_BROKER_ADDR', 'localhost')
PORT = int(os.environ.get('MQTT_BROKER_PORT', '5600'))
VEHICLE_ID = os.environ.get('VIN')
BASE_TOPIC = f"vehicle/{VEHICLE_ID}"


VEHICLE_ID = os.environ.get('VIN')
count = 1

with Ankaios() as ankaios:

    # Callback when the client receives a CONNACK response from the MQTT server
    def on_connect(client, userdata, flags, reason_code, properties):
        client.subscribe(f"{BASE_TOPIC}/start")
        client.subscribe(f"{BASE_TOPIC}/stop")    # Callback when a PUBLISH message is received from the MQTT server

    def on_message(client, userdata, msg):
        try:
            logger.info(f"Received message on topic {msg.topic} with payload {msg.payload.decode()}")
             # Handle request for applying a manifest
            if msg.topic == f"{BASE_TOPIC}/start":
                workload = ankaios.get_workload("long_distance_drive")
                workload.update_agent_name("hpc2")
                ankaios.apply_workload(workload)
                logger.info(f"long_distance_drive activated")
            if msg.topic == f"{BASE_TOPIC}/stop":
                logger.info(f"long_distance_drive deactivated")
                workload = ankaios.get_workload("long_distance_drive")
                workload.update_agent_name("")
                ankaios.apply_workload(workload)
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    # Create an MQTT client instance
    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)    # Assign the callbacks
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message    # Connect to the MQTT broker
    mqtt_client.connect(BROKER, PORT, 60)    # Blocking call that processes network traffic, dispatches callbacks,
    # and handles reconnecting.
    mqtt_client.loop_forever()
