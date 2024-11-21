const speedTorqueRelation = [{
    speed: 0,
    torque: "D1"
}, {
    speed: 20,
    torque: "D2"
}, {
    speed: 30,
    torque: "D3"
}, {
    speed: 40,
    torque: "D4"
}, {
    speed: 70,
    torque: "D5"
}, {
    speed: 80,
    torque: "D6"
}, {
    speed: 100,
    torque: "D7"
}];

/* update the speed-value */
function updateSpeedAndTorque(speed_km_h) {
    // update the speed value fluently by a number
    let speedValue = document.getElementById("displayspeedval");
    // let torqueValue = document.getElementById("torque-value");

    // // check if the speed_km_h is greater or equal the last speed in the speedTorqueRelation
    // if (speedTorqueRelation.length > 0 && speed_km_h >= speedTorqueRelation[speedTorqueRelation.length - 1].speed) {
    //     torqueValue.textContent = speedTorqueRelation[speedTorqueRelation.length - 1].torque;
    // } else if (speed_km_h < 0) {
    //     torqueValue.textContent = "R"; // speed negative driving backwards
    // } else {
    //     let torque_out = speedTorqueRelation.find((element) => {
    //         return speed_km_h <= element.speed;
    //     });

    //     if (torque_out) {
    //         torqueValue.textContent = torque_out.torque;
    //     }
    // }

    speedValue.textContent = speed_km_h;
}

// read from server-side event
const eventSource = new EventSource("/vehicle-dynamics");

eventSource.onopen = function (_event) {
    console.log("Connection to /vehicle-dynamics opened");
}

// add event listener for the event
eventSource.addEventListener("vehicle-dynamics", function (event) {
    let raw_data = event.data;
    let vehicle_dynamics = JSON.parse(raw_data);
    console.log(vehicle_dynamics);
    let speed_km_h = parseInt(parseFloat(vehicle_dynamics.signals.speedDisplayed) * 3.6)
    console.log("Received speed_km_h: ", speed_km_h);
    updateSpeedAndTorque(speed_km_h);
});

// close the connection on error
eventSource.onerror = function (event) {
    console.log("Error: " + event);
    eventSource.close();
}