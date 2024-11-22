# Stability Application

The Stability app uses vehicle dynamics data and identifies if vehicle is stable or not. Signals used here are Yawrate, Lateral acceleration and Steering angle. 
The eCAL data is sampled at 20Hz, so for each Variance, max and min of the above parameters are collected and used to provide a threshold value is the vehicle is wobbling or not. 

## Build

When running `restart-shift2sdv`, or explicitly the `build-apps` script, the Example App will be build and containerized automatically as `ghcr.io/eclipse-sdv-hackathon-chapter-two/shift2sdv/stability_app:latest`.

```shell
podman build -t example_app:latest .
```
### Run

Start the app inside the devcontainer for local development:

```shell
python3 example_app.py
```

### Testing with Funny driving

Place the downloaded eCAL recording in a `measurements/` folder next to the current file.

Start the eCAL recording within the devcontainer, replace `<recording_folder>` with the recording folder you received from the hack coaches:

```shell
ecal_play -m measurements/<recording_folder>
```
