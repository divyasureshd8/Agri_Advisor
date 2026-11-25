
// AUTOMATIC GPS LOCATION

function getLocation() {

    const result = document.getElementById("locationResult");

    if (!navigator.geolocation) {
        result.innerText = "GPS is not supported by your browser.";
        return;
    }

    result.innerText = "Detecting your location...";

    navigator.geolocation.getCurrentPosition(

        async function(position) {

            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;

            result.innerText =
                "Location detected! Latitude: " +
                latitude.toFixed(4) +
                ", Longitude: " +
                longitude.toFixed(4);

            // We will add reverse geocoding
            // to identify the state and district later.
        },

        function(error) {
            result.innerText =
                "Unable to detect location. Please select your district manually.";
        }
    );
}


// CROP RECOMMENDATION

async function recommendCrop() {

    const result = document.getElementById("result");

    const data = {
        N: document.getElementById("N").value,
        P: document.getElementById("P").value,
        K: document.getElementById("K").value,
        temperature: document.getElementById("temperature").value,
        humidity: document.getElementById("humidity").value,
        ph: document.getElementById("ph").value,
        rainfall: document.getElementById("rainfall").value
    };

    for (const key in data) {
        if (data[key].trim() === "" ||
            !Number.isFinite(Number(data[key]))) {
            result.innerText = "Please enter all seven valid values.";
            return;
        }
    }

    result.innerText = "Predicting suitable crop...";

    try {

        const response = await fetch(
            "https://YOUR-BACKEND-URL/predict",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            }
        );

        const output = await response.json();

        if (!response.ok) {
            throw new Error(output.error || "Prediction failed");
        }

        result.innerText =
            "Recommended Crop: " + output.recommended_crop;

    } catch (error) {

        result.innerText =
            "Backend connection error: " + error.message;

    }
          }
