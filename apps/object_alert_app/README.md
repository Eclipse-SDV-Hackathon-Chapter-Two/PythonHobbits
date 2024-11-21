# Example Application

The Example App show how data from the vehicle can be received by an application running in the vehicle.

## Build

When running `restart-shift2sdv`, or explicitly the `build-apps` script, the Example App will be build and containerized automatically as `ghcr.io/eclipse-sdv-hackathon-chapter-two/shift2sdv/example_app:latest`.

Of course, you are free to build manually if needed by calling the following command from the example_app folder:

```shell
podman build -t example_app:latest .
```

**Note:** Inside the test-vehicle the Example App will run on ARM-Platform. Test the build by running the command above and ask the hack coaches to build your image for ARM to run it inside the test vehicle.

## Running

The Example App is automatically started by Ankaios as there is an entry for it in the [shift2sdv_manifest.yaml](shift2sdv_manifest.yaml).

In the test vehicle the Example App container image will be started and managed by Eclipse Ankaios.

Talk to the hack coaches to build a multi-platform or ARM image before trying to run the app in the vehicle.

## Development

### Run

Start the app inside the devcontainer for local development:

```shell
python3 example_app.py
```

### Testing with mock data

Ask the hack coaches for an eCAL recording to play back a recorded driving scenario with eCAL and to receive the vehicle dynamics data in the Example App for development.

Place the downloaded eCAL recording in a `measurements/` folder next to the current file.

Start the eCAL recording within the devcontainer, replace `<recording_folder>` with the recording folder you received from the hack coaches:

```shell
ecal_play -m measurements/<recording_folder>
```

Start the Example App inside the devcontainer as shown above.

You should see logs of the JSON data received, and in the web browser the tachometer should show some speed values.

For debugging reasons you can start the eCAL Monitor terminal UI in a separate terminal window by running:

```shell
ecal_mon_tui
```

This lists all eCAL topics with their contents and meta information the host or container can see.
