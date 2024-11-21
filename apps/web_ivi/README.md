# Web IVI

![web_ivi_screenshot](web_ivi_screenshot.png)

The Demo Web IVI is a simple web application showing a three column layout with a speedometer in the first column, followed by a free to use info section and the torque meter as the third column. The intention is to provide you with a web based IVI that can be easily extended. The web IVI is intended to run inside the test vehicle and is used to display some information to the user during a drive. The web application is designed for simplicity, not for production use.

By default, the web backend receives vehicle dynamics data via the eCAL topic `vehicle_dynamics` (JSON) once a client browser connects to `http://127.0.0.1:5500`. The web backend passes the vehicle dynamics JSON to the client via [SSE (Server Side Event)](https://en.wikipedia.org/wiki/Server-sent_events). It extracts the current vehicle speed value `signals.speedDisplayed` from the JSON message and displays it within the speedometer. For simplicity, the torque-speed relationship is simulated within code.

The `div` with the id `info-screen` in `static/index.html` can be used to display custom information to the driver. Feel free to append data to it. If this does not suit your needs, you can also customize the whole Web IVI. Feel also free to extract and display any other relevant data from the `vehicle_dynamics` JSON data.

## Build

When running `restart-shift2sdv`, or explicitly the `build-apps` script, the Web IVI will be build and containerized automatically as `ghcr.io/eclipse-sdv-hackathon-chapter-two/shift2sdv/web_ivi:latest`.

Of course, you are free to build manually if needed by calling the following command from the web_ivi folder:

```shell
podman build -t web_ivi:latest .
```

**Note:** Inside the test-vehicle the Web IVI will run on ARM-Platform. Test the build by running the command above and ask the hack coaches to build your image for ARM to run it inside the test vehicle.

## Running

The Web IVI is automatically started by Ankaios as there is an entry for it in the [shift2sdv_manifest.yaml](shift2sdv_manifest.yaml).

In the test vehicle the Web IVI container image will be started and managed by Eclipse Ankaios. Finally, it will be displayed on a separate display within the test vehicle.

Talk to the hack coaches to build a multi-platform or ARM image before trying to run the app in the vehicle.

## Development

### Run

Start the app inside the devcontainer for local development:

```shell
uvicorn main:app --port 5500 --reload
```

Open the Google Chrome browser on `http://127.0.0.1:5500`.

**Note:** The app was tested on Google Chrome browser. Other browsers might not work.

### Testing with mock data

Ask the hack coaches for an eCAL recording to play back a recorded driving scenario with eCAL and to receive the vehicle dynamics data in the Web IVI for development.

Place the downloaded eCAL recording in a `measurements/` folder next to the current file.

Start the eCAL recording within the devcontainer, replace `<recording_folder>` with the recording folder you received from the hack coaches:

```shell
ecal_play -m measurements/<recording_folder>
```

Start the Web IVI inside the devcontainer as shown above.

You should see logs of the JSON data received, and in the web browser the tachometer should show some speed values.

For debugging reasons you can start the eCAL Monitor terminal UI in a separate terminal window by running:

```shell
ecal_mon_tui
```

This lists all eCAL topics with their contents and meta information the host or container can see.
