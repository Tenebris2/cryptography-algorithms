const form = document.getElementById("input-form");
const jsonGetterButton = document.getElementById("json-getter");
const display = document.getElementById("display");
const url = "http://localhost:8000/api/rsa";
const animation_class = "text-writer-animation";
//jsonGetterButton.onclick = async () => {
//
//};

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData(event.target);

  let message = jsonifyFormData(formData);

  display.classList.add(animation_class);
  try {
    let data = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json", // Add Content-Type header for JSON
      },
      body: JSON.stringify(message), // Ensure message is a valid JSON string
    });

    if (!data.ok) {
      throw new Error("Network response was not ok");
    }

    let jsonData = await data.json(); // Await the JSON parsing
    let displayData = "";
    for (const key in jsonData) {
      if (jsonData.hasOwnProperty(key)) {
        displayData += `<span class="key">${key}</span>: ${jsonData[key]}`;
      }
    }

    display.innerHTML = displayData;
    display.addEventListener("animationend", () => {
      display.classList.remove(animation_class);
    });
  } catch (error) {
    console.error("Error: ", error);
  }
});

function jsonifyFormData(FormData) {
  let formObject = {};
  FormData.forEach((value, key) => {
    formObject[key] = value;
  });

  return formObject;
}
