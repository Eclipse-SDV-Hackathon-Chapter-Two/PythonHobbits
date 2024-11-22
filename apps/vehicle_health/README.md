# Vehicle health Application

The App calculates a score for the driving pattern for a defined amount of time and stored. Data taken at fixed intervals here are used to consolidate a final score. For the purpose of simulation a json file is stored, with the data at fixed intervals.

## Build

When running `restart-shift2sdv`, or explicitly the `build-apps` script, the Example App will be build and containerized automatically as `ghcr.io/eclipse-sdv-hackathon-chapter-two/shift2sdv/vehicle_health:latest`.

```shell
podman build -t vehicle_health:latest .
```
