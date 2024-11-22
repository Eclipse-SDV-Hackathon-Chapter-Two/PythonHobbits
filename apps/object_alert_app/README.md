# Object Alert app

The App show how data from the vehicle's camera is used to identify the region of interest and if objects identified within that region of interest then a warning is issued.

## Build

When running `restart-shift2sdv`, or explicitly the `build-apps` script, the Example App will be build and containerized automatically as `ghcr.io/eclipse-sdv-hackathon-chapter-two/shift2sdv/object_alert_app:latest`.

Of course, you are free to build manually if needed by calling the following command from the example_app folder:

```shell
podman build -t example_app:latest .
```

### Run

Start the app inside the devcontainer for local development:

```shell
python3 object_alert_app.py
```

### Testing with Sample data

Place the downloaded eCAL recording in a `measurements/` folder next to the current file.

Start the eCAL recording within the devcontainer, replace `<recording_folder>` with the recording folder you received from the hack coaches:

```shell
ecal_play -m measurements/<recording_folder>
```

```shell
ecal_mon_tui
```

This lists all eCAL topics with their contents and meta information the host or container can see.
