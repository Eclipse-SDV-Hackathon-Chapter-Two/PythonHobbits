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

#--------------|---x1,y1--------------------x2,y2---|---------------
FRAME_NUMBER =20
car_x1_position = 100
car_y1_position = 600
car_x2_position = 400
car_y2_position = 600

legend = {
    0.0 : 'Pedestrian',
    1.0 : 'bicycle',
    2.0 : 'car',
    3.0 : 'motorcycle',
    5.0 : 'bus',
    6.0 : 'train',
    7.0 : 'truck',
    9.0 : 'traffic light',
    11.0 :'stop_sign',
    12.0 : 'parking_meter'
}

logger = logging.getLogger("Object_Alert")
stdout = logging.StreamHandler(stream=sys.stdout)
stdout.setLevel(logging.INFO)
logger.addHandler(stdout)
logger.setLevel(logging.INFO)


def analyze_current_state(objects_data):
    for obj in objects_data:
        num_objects = len(obj['class_ids']) 
        for i in range(num_objects):
            obj_id = obj['class_ids'][i]
            # print("Analysing ",legend[obj_id])
            if obj_id >= 9:
                # print(obj_id)
                continue
            obj_position = obj['xyxy']

            #Finding the object's position
            x1 = obj_position[i][0]
            y1 = obj_position[i][1]
            x2 = obj_position[i][2]
            y2 = obj_position[i][3]

            
            #Finding the centre of the object
            #centre_x,centre_y = (x1+x2) //2 , (y1+y2) //2

            #print(centre_x, centre_y)

            #Object within the range
            if (x2 >= 450 and y2 >= 450 and y2 < 500):
                msg = f"{legend[obj_id]} detected within the range."
                obj_pub.send(msg)
                print(msg)
                # obj_result_queue.put(msg)
            
            #Objects too close to the vehicle 
            if (x2 >= 350 and y2 >= 500 ):
                msg = f"{legend[obj_id]} too close to the vehicle."
                obj_pub.send(msg)
                print(msg)
                # obj_result_queue.put(msg)
    # return obj_result_queue

def object_alert(input_queue):
    objects_list = []
    frames_count=0
   
    while True:
        if not input_queue.empty():
            input1 = input_queue.get()
            objects_list.append(input1)
            frames_count += 1
            if len(objects_list) ==  FRAME_NUMBER:
                analyze_current_state(objects_list)
                frames_count = 0
                objects_list = []

# Callback for receiving messages
def callback(topic_name, msg, time):
    try:
        json_msg = json.loads(msg)
        
        obj_input_queue.put(json_msg)
        
        #object_alert(obj_input_queue,obj_result_queue)
    except json.JSONDecodeError:
        logger.error(f"Error: Could not decode message: '{msg}'")
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    obj_input_queue = mp.Queue()
    
    logger.info("Starting Object Alert app...")

    # Initialize eCAL
    ecal_core.initialize(sys.argv, "Object Alert App")

    # Create a subscriber that listens on the "object_detection"
    sub = StringSubscriber("object_detection")
    obj_pub = StringPublisher("detected_objects")

    process_signals_process = mp.Process(target=object_alert, args=(obj_input_queue,))
    process_signals_process.start()
    # Set the Callback
    sub.set_callback(callback)
    
    # Just don't exit
    while ecal_core.ok():
        time.sleep(0.5)
    
    # finalize eCAL API
    ecal_core.finalize()
