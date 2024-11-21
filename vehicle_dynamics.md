# Vehicle Dynamics

Retrieve in-vehicle sensor data by subscribing to the eCAL `vehicle_dynamics` topic.

The data received is in JSON format and looks like the following

```json
{
    "header": {
        "timestamp": "1730982505741887"
    },
    // potential sensor errors, can be ignored
    "errs": {
        // ...
    },
    // import in-vehicle signals like speed, acceleration and steering wheel angle, ...
    "signals": {
        "speed": 4.500004,
        "speedDisplayed": 4.722226,
        "speedPerWheel": [
            4.5041704,
            4.49167,
            4.508337,
            4.48542
        ],
        "longAcc": 0.0,
        "latAcc": -0.02,
        "yawrate": 0.00034906,
        "steeringWheelAngle": -0.064576104,
        "steeringWheelAngleSpeed": 0.0,
        "drvSteerTorque": 0.0,
        "timeSinceLastClick": 0.0,
        "wheelSteeringAngleFront": 0.0,
        "wheelSteeringAngleRear": 0.0
    },
    // variances, can be ignored
    "variances": {
        // ...
    },
    // timestamps, can be ignored
    "timestamps": {
        // ...
    }
}
```