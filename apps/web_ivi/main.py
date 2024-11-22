from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from uvicorn import run
import sys
from asyncio import sleep
from queue import Queue
import threading
import logging
import signal
from contextlib import asynccontextmanager

import ecal.core.core as ecal_core
from ecal.core.subscriber import StringSubscriber

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

stop_server_side_event = threading.Event()

data_str = "Hello"

@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Manages the lifespan of the FastAPI application.

    This function is a generator that performs actions at the startup and shutdown of the application.
    At startup, it sets up a signal handler for SIGINT to trigger a server-side event.
    At shutdown, it finalizes the eCAL core and logs the shutdown process.

    Args:
        _app (FastAPI): The FastAPI application instance.
    """
    # Run at startup
    signal.signal(signal.SIGINT, lambda: stop_server_side_event.set())

    yield
    # Run on shutdown
    # Finalize eCAL API
    ecal_core.finalize()
    logger.info('Shutting down...')

# create a route that delivers the statc/index.html file
app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/assets", StaticFiles(directory="static/assets"), name="assets")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def home():
    """
    Serves the web ivi page by returning a FileResponse object pointing to "static/index.html".

    Returns:
        FileResponse: A response object that serves the "static/index.html" file.
    """
    return FileResponse("static/test.html")

@app.get("/vehicle-dynamics")
async def vehicle_dynamics():
    """
    Asynchronous function to handle vehicle dynamics data streaming to the client browser.

    This function initializes the eCAL API, subscribes to the "vehicle_dynamics" topic,
    and sets a callback to handle incoming messages. It uses an asynchronous generator
    to yield vehicle dynamics data as server-sent events (SSE).

    Returns:
        StreamingResponse: A streaming response with vehicle dynamics data in SSE format.
    """
    async def vehicle_dynamics_generator():
        vehicle_dynamics_queue = Queue() # Already synchronized queue

        # Define an ecal callback triggered when receiving data through the ecal topic
        def callback_vehicle_dynamics(_topic_name, msg, _time):
            logger.info(msg)
            vehicle_dynamics_queue.put(msg)

        # Initialize ecal
        ecal_core.initialize(sys.argv, "WebIVI VehicleDynamics")

        # Subscribe to the vehicle_dynamics topic receiving json messages
        sub = StringSubscriber("vehicle_dynamics")

        # Set the Callback
        sub.set_callback(callback_vehicle_dynamics)

        while ecal_core.ok() and not stop_server_side_event.is_set():
            if not vehicle_dynamics_queue.empty():
                vehicle_dynamics_data = vehicle_dynamics_queue.get()
                logger.info(vehicle_dynamics_data)
                vehicle_dynamics_queue.task_done()
                vehicle_dynamics_queue = Queue()
                yield f"event: vehicle-dynamics\ndata: {vehicle_dynamics_data}\n\n"
            await sleep(0.1)

        # Finalize eCAL API
        ecal_core.finalize()
    return StreamingResponse(vehicle_dynamics_generator(), media_type="text/event-stream")

@app.get("/stability-info")
async def stability_info():

    async def stability_info_generator():
        stability_queue = Queue() # Already synchronized queue

        # Define an ecal callback triggered when receiving data through the ecal topic
        def callback_stability_info(_topic_name, msg, _time):
            logger.info(msg)
            stability_queue.put(msg)

        # Initialize ecal
        ecal_core.initialize(sys.argv, "WebIVI stability")

        # Subscribe to the vehicle_dynamics topic receiving json messages
        sub = StringSubscriber("stability")

        # Set the Callback
        sub.set_callback(callback_stability_info)

        while ecal_core.ok() and not stop_server_side_event.is_set():
            if not stability_queue.empty():
                stability_data = stability_queue.get()
                logger.info(stability_data)
                stability_queue.task_done()
                stability_queue = Queue()
                yield f"event: stability-info\ndata: {stability_queue}\n\n"
            await sleep(0.1)

        # Finalize eCAL API
        ecal_core.finalize()
    return StreamingResponse(stability_info_generator(), media_type="text/event-stream")



@app.get("/health-info")
async def health_info():

    async def health_info_generator():
        health_queue = Queue() # Already synchronized queue

        # Define an ecal callback triggered when receiving data through the ecal topic
        def callback_health_info(_topic_name, msg, _time):
            logger.info(msg)
            health_queue.put(msg)

        # Initialize ecal
        ecal_core.initialize(sys.argv, "health ")

        # Subscribe to the vehicle_dynamics topic receiving json messages
        sub = StringSubscriber("health")

        # Set the Callback
        sub.set_callback(callback_health_info)

        while ecal_core.ok() and not stop_server_side_event.is_set():
            if not health_queue.empty():
                health_data = health_queue.get()
                logger.info(health_data)
                health_queue.task_done()
                health_queue = Queue()
                yield f"event: health-info\ndata: {health_queue}\n\n"
            await sleep(0.1)

        # Finalize eCAL API
        ecal_core.finalize()
    return StreamingResponse(health_info_generator(), media_type="text/event-stream")

@app.get("/object-check")
async def object_check():

    async def object_check_generator():
        object_queue = Queue() # Already synchronized queue

        # Define an ecal callback triggered when receiving data through the ecal topic
        def callback_object_info(_topic_name, msg, _time):
            logger.info(msg)
            object_queue.put(msg)

        # Initialize ecal
        ecal_core.initialize(sys.argv, "object ")

        # Subscribe to the vehicle_dynamics topic receiving json messages
        sub = StringSubscriber("object_check")

        # Set the Callback
        sub.set_callback(callback_object_info)

        while ecal_core.ok() and not stop_server_side_event.is_set():
            if not object_check.empty():
                object_data = object_queue.get()
                logger.info(object_data)
                object_queue.task_done()
                object_queue = Queue()
                yield f"event: object-check\ndata: {object_queue}\n\n"
            await sleep(0.1)

        # Finalize eCAL API
        ecal_core.finalize()
    return StreamingResponse(object_check_generator(), media_type="text/event-stream")



if __name__ == "__main__":
    run(app, host="0.0.0.0", port=5500)
