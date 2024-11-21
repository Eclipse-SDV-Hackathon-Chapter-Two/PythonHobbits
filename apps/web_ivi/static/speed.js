function updateSpeedAndTorque(speed_km_h) {
  let speedDisplay = document.getElementById("speedintxt");
  let meterBar = document.getElementById("meter-bg-bar");
  let strokeDashoffset = parseFloat(
        window.getComputedStyle(meterBar).getPropertyValue("stroke-dashoffset")
      );
  
  speedDisplay.textContent = speed_km_h;
  if (speed_km_h <= 83){
    meterBar.setAttribute('stroke', "#f80b0b");}
  else{
  meterBar.setAttribute('stroke', "#0bf823");}
}

const eventSource1 = new EventSource("/vehicle-dynamics");
const eventSource2 = new EventSource("/stability-info");
const eventSource3 = new EventSource("/health-info");
const eventSource4 = new EventSource("/send-string3");

eventSource1.onopen = function (_event) {
    console.log("Connection to /vehicle-dynamics opened");
}

eventSource2.onopen = function (_event) {
  console.log("Connection to /stability-info opened");
}

eventSource3.onopen = function (_event) {
  console.log("Connection to /health-info opened");
}

eventSource4.onopen = function (_event) {
  console.log("Connection to /send-string3 opened");
}

eventSource1.addEventListener("vehicle-dynamics", function (event) {
    let raw_data = event.data;
    let vehicle_dynamics = JSON.parse(raw_data);
    console.log(vehicle_dynamics);
    let speed_km_h = parseInt(parseFloat(vehicle_dynamics.signals.speedDisplayed) * 3.6)
    console.log("Received speed_km_h: ", speed_km_h);
    updateSpeedAndTorque(speed_km_h);
});

// close the connection on error
eventSource1.onerror = function (event) {
  console.log("Error in receiving vehicle dynamics: " + event);
  eventSource.close();
}


eventSource2.addEventListener("stability-info", function (event) {
  let raw_data = event.data;
  console.log(raw_data)
  let textDisplay = document.getElementById("displaystr");
  textDisplay.textContent = raw_data;
});


eventSource2.onerror = function (event) {
console.log("Error in stability-info: " + event);
eventSource2.close();
}


eventSource3.addEventListener("health-info", function (event) {
  let raw_data = event.data;
  console.log(raw_data)
  //updateSpeedAndTorque(speed_km_h);
  let textDisplay = document.getElementById("displaystr2");
  textDisplay.textContent = raw_data;
});


eventSource3.onerror = function (event) {
console.log("Error in health-info: " + event);
eventSource3.close();
}

eventSource4.addEventListener("send-string3", function (event) {
  let raw_data = event.data;
  console.log(raw_data)
  //updateSpeedAndTorque(speed_km_h);
  let textDisplay = document.getElementById("displaystr3");
  textDisplay.textContent = raw_data;
});


eventSource4.onerror = function (event) {
console.log("Error in send-string3: " + event);
eventSource4.close();
}



// // Function to calculate the current speed based on the stroke-dashoffset
// function calculateSpeed() {
//   // Get the element
//   let meterBar = document.getElementById("meter-bg-bar");
//   // Get the current stroke-dashoffset
//   let strokeDashoffset = parseFloat(
//     window.getComputedStyle(meterBar).getPropertyValue("stroke-dashoffset")
//   );
//   // Calculate the current speed based on the stroke-dashoffset
//   // The maximum stroke-dashoffset is 615, which corresponds to a speed of 0 km/h
//   // The minimum stroke-dashoffset is 0, which corresponds to a speed of 180 km/h
//   let speed = ((615 - strokeDashoffset) / 615) * 180;
//   // Round the speed to the nearest integer
//   speed = Math.round(speed);
//   return speed;
// }
// Function to update the speed display
// function updateSpeedDisplay() {
  // Calculate the current speed
  // let speed = calculateSpeed();
  // // Get the speed display element
  // let speedDisplay = document.getElementById("speedintxt");
  // // Update the text content of the speed display element
  //speedDisplay.textContent = speed;
  // speedDisplay.textContent = speed + ' km/h';
// }
// Call the updateSpeedDisplay function every 100 milliseconds
//setInterval(updateSpeedDisplay, 100);
