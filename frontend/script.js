const form = document.getElementById("input-form");
const functionButton = document.getElementById("function-btn");
const display = document.getElementById("display");

// rsa
const rsaEncryptionURL = "http://localhost:8000/rsa-encrypt";
const rsaDecryptionURL = "http://localhost:8000/rsa-decrypt";

//animation class
const animation_class = "text-writer-animation";
const defaultAlgorithmValue = "Select Algorithm";
const dropdown_contents = document.getElementById(
  "dropdown-content-algorithms",
);
const algorithm_selector = document.getElementById("algorithm-selector");

const algorithms = dropdown_contents.querySelectorAll("button");

const parameters = ["Message"];
const decrypt_parameters = ["encrypted", "private_key", "n"];
const decryptCheckbox = document.getElementById("decrypt");

const exportDataBtn = document.getElementById("exporter");

let previousJsonData = null;

exportDataBtn.onclick = () => {
  if (previousJsonData != null) {
    // Create a Blob with the content
    const blob = new Blob([JSON.stringify(previousJsonData)], {
      type: "application/json",
    });

    // Create a temporary download link
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "data.json"; // Set the file name

    // Trigger the download by clicking the link
    link.click();

    // Clean up
    URL.revokeObjectURL(link.href);
  }
};
decryptCheckbox.addEventListener("change", () => {
  if (
    decryptCheckbox.checked &&
    algorithm_selector.innerText != defaultAlgorithmValue
  ) {
    console.log(algorithm_selector.innerText);
    functionButton.innerText = "Decrypt";

    while (form.children.length >= 2) {
      form.removeChild(form.children[1]);
    }
    // remove second children from there
    decrypt_parameters.forEach((param) => {
      let newParameter = createNewParameter(param);
      form.appendChild(newParameter);
    });
  } else {
    functionButton.innerText = "Encrypt";
    console.log("Unchecked");
  }
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = new FormData(event.target);
  let message = jsonifyFormData(formData);
  // means it is encryption time
  if (!decryptCheckbox.checked) {
    callApi(message, rsaEncryptionURL);
  } else {
    callApi(message, rsaDecryptionURL);
  }
});

algorithms.forEach((algorithm_button) => {
  algorithm_button.onclick = () => {
    console.log(algorithm_button.name);
    // set the checkbox the default
    functionButton.innerText = "Encrypt";

    decryptCheckbox.checked = false;
    while (form.children.length >= 2) {
      form.removeChild(form.children[1]);
    }
    // remove second children from there
    parameters.forEach((param) => {
      let newParameter = createNewParameter(param);
      form.appendChild(newParameter);
    });

    algorithm_selector.innerText = algorithm_button.name;
  };
});
function jsonifyFormData(FormData) {
  let formObject = {};
  FormData.forEach((value, key) => {
    formObject[key] = value;
  });

  return formObject;
}

function createNewParameter(parameterName) {
  let newParameter = document.createElement("input");

  newParameter.type = "text";
  newParameter.placeholder = parameterName;
  newParameter.id = parameterName.toLowerCase();
  newParameter.name = parameterName.toLowerCase();

  return newParameter;
}
function capitalizeFirstLetter(val) {
  return String(val).charAt(0).toUpperCase() + String(val).slice(1);
}

async function callApi(message, url) {
  try {
    let data = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json", // Add Content-Type header for JSON
      },
      body: JSON.stringify(message), // Ensure message is a valid JSON string
    });

    console.log(JSON.stringify(message));
    if (!data.ok) {
      throw new Error("Network response was not ok");
    }

    let jsonData = await data.json(); // Await the JSON parsing
    previousJsonData = jsonData;
    let displayData = "";
    for (const key in jsonData) {
      if (jsonData.hasOwnProperty(key)) {
        displayData += `<span class="key">${capitalizeFirstLetter(key)}</span>: ${jsonData[key]}<br>`;
      }
    }

    display.innerHTML = displayData;
    display.addEventListener("animationend", () => {
      display.classList.remove(animation_class);
    });
  } catch (error) {
    console.error("Error: ", error);
  }

  display.classList.add(animation_class);
}
