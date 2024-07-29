function displayResponseBox(data) {
    var responseBox = document.createElement("div");
    responseBox.classList.add("response-box");
  
    if (data.message) {
        responseBox.innerText = data.message;
        responseBox.style = setBoxStyle(true);
    } else if (data.error) {
        responseBox.innerText = data.error;
        responseBox.style = setBoxStyle(false);
    } else if (data.addedNote) {
        responseBox.innerText = "Η σημείωση προστέθηκε με επιτυχία";
        responseBox.style = setBoxStyle(true);
    } else {
        responseBox.innerText = "No message or error";
        responseBox.style = setBoxStyle(false);
    }
  
    appendAndAutoRemoveBox(responseBox);
}

function setBoxStyle(isSuccess) {
    return `position: fixed; right: 20px; bottom: 20px; color: white; padding: 10px;
            border-radius: 5px; box-sizing: border-box; max-width: 300px; word-wrap: break-word;
            background-color: ${isSuccess ? "rgba(0, 255, 0, 0.5)" : "rgba(255, 0, 0, 0.5)"};
            border: ${isSuccess ? "2px solid green" : "2px solid red"};`;
}
  
function appendAndAutoRemoveBox(responseBox) {
    var existingBoxes = document.getElementsByClassName("response-box");
    var bottomOffset = 20;
  
    for (var i = 0; i < existingBoxes.length; i++) {
        bottomOffset += existingBoxes[i].offsetHeight + 10;
    }
  
    responseBox.style.bottom = bottomOffset + "px";
    document.body.appendChild(responseBox);
  
    setTimeout(function() {
        document.body.removeChild(responseBox);
        updateBoxPositions();
    }, 5000);
}
  
function updateBoxPositions() {
    var existingBoxes = document.getElementsByClassName("response-box");
    var bottomOffset = 20;
  
    for (var i = existingBoxes.length - 1; i >= 0; i--) {
        existingBoxes[i].style.bottom = bottomOffset + "px";
        bottomOffset += existingBoxes[i].offsetHeight + 10;
    }
}