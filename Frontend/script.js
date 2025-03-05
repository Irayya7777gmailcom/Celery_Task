// Improved script.js for CSV upload and processing
function uploadFile(event) {
    event.preventDefault(); // Prevents page refresh

    let fileInput = document.getElementById("fileInput");
    let file = fileInput.files[0];
    
    if (!file) {
        alert("Please select a file first.");
        return;
    }

    console.log("File selected:", file.name); // Debug log

    let formData = new FormData();
    formData.append("file", file);

    fetch("http://127.0.0.1:8000/upload/", {
        method: "POST",
        body: formData
    })
    .then(response => {
        console.log("Response status:", response.status); // Debug log
        return response.json();
    })
    .then(data => {
        console.log("Server response:", data); // Debug log
        
        if (data.task_id) {
            console.log("Task ID received:", data.task_id);
            checkTaskStatus(data.task_id);
        } else {
            console.error("No task ID received.");
            document.getElementById("result").innerText = "Error: No task ID received";
        }
    })
    .catch(error => {
        console.error("Upload error:", error);
        document.getElementById("result").innerText = `Error: ${error.message}`;
    });
}

function checkTaskStatus(taskId) {
    console.log("Checking task status for:", taskId); // Debug log

    fetch(`http://127.0.0.1:8000/task-status/${taskId}/`)
    .then(response => {
        console.log("Task status response:", response.status); // Debug log
        return response.json();
    })
    .then(data => {
        console.log("Full task status data:", data); // Comprehensive debug log

        const resultElement = document.getElementById("result");
        
        switch(data.status) {
            case "SUCCESS":
                resultElement.innerText = JSON.stringify(data.result, null, 2);
                break;
            case "FAILURE":
                resultElement.innerText = "Task failed! Error details: " + 
                    (data.error || "Unknown error occurred");
                break;
            case "PENDING":
            default:
                console.log("Task still in progress, retrying...");
                setTimeout(() => checkTaskStatus(taskId), 2000);
                break;
        }
    })
    .catch(error => {
        console.error("Error checking task status:", error);
        document.getElementById("result").innerText = `Status Check Error: ${error.message}`;
    });
}

// Attach event listener to button
document.addEventListener("DOMContentLoaded", function () {
    const uploadButton = document.getElementById("uploadButton");
    if (uploadButton) {
        uploadButton.addEventListener("click", uploadFile);
    } else {
        console.error("Upload button not found!");
    }
});