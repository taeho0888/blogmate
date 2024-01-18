document.addEventListener('DOMContentLoaded', function () {
    const urlInput = document.getElementById('urlInput');
    const addButton = document.querySelector('.add-button');

    // Input validation for the URL input field
    urlInput.addEventListener('input', function () {
        const isValidUrl = validateUrl(this.value);
        addButton.disabled = !isValidUrl;
        addButton.style.backgroundColor = isValidUrl ? '#638fff' : '#d9d9d9';
    });

    // Trigger addVideo function when Enter key is pressed
    urlInput.addEventListener('keyup', function (event) {
        if (event.key === 'Enter') {
            const videoUrl = urlInput.value;
            if (validateUrl(videoUrl)) {
                addVideo(videoUrl);
            } else {
                alert('Invalid URL. Please enter a valid URL.');
            }
        }
    });

    // Trigger addVideo function when Add button is clicked
    addButton.addEventListener('click', function () {
        const videoUrl = urlInput.value;
        if (validateUrl(videoUrl)) {
            addVideo(videoUrl);
        } else {
            alert('Invalid URL. Please enter a valid URL.');
        }
    });

    // Setup listeners for delete buttons
    setupItemBoxNavigation();
    setupThumbnailNavigation();
    setupDeleteButtons();
});

// Validates the YouTube video URL
function validateUrl(url) {
    const parts = url.split('?v=');
    const isValidFormat = parts.length === 2 && parts[0].length > 0 && parts[1].length > 0;
    return isValidFormat;
}

// Sends a POST request to add a video
function addVideo(videoUrl) {
    const videoId = videoUrl.split("?v=")[1];

    fetch('http://127.0.0.1:8000/video', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({video_url: videoId}),
    })
    .then(response => {
        if (response.ok) {
            window.location.reload();
        } else {
            console.error('Server responded with a non-OK status:', response.status);
        }
    })
    .catch(error => {
        console.error('Error adding video:', error);
    });
}

// Sets up event listeners for delete buttons
function setupDeleteButtons() {
    document.querySelectorAll('.delete-button').forEach(button => {
        button.addEventListener('click', function (event) {
            event.stopPropagation(); // Prevent triggering click on the item-box
            const videoId = this.getAttribute('data-video-id');
            deleteVideo(videoId);
        });
    });
}

// Navigates to the detail page when an item-box is clicked
function setupItemBoxNavigation() {
    document.querySelectorAll('.item-box').forEach(item => {
        item.addEventListener('click', function () {
            const videoId = this.getAttribute('data-video-id');
            window.location.href = `http://127.0.0.1:8000/detail/${videoId}`;
        });
    });
}

function setupThumbnailNavigation() {
    document.querySelectorAll('.thumbnail').forEach(thumbnail => {
        thumbnail.addEventListener('click', function (event) {
            event.stopPropagation(); // Prevent triggering click on the item-box or other parent elements
            const videoUrl = this.getAttribute('data-video-url');
            window.open(`https://youtube.com/watch?v=${videoUrl}`, '_blank'); // Open in a new tab
        });
    });
}

// Sends a DELETE request to remove a video
function deleteVideo(videoId) {
    fetch(`http://127.0.0.1:8000/video/${videoId}`, {
        method: 'DELETE',
    })
    .then(response => {
        if (response.ok) {
            window.location.reload();
        } else {
            alert('Error deleting video');
        }
    })
    .catch(error => {
        console.error('Error deleting video:', error);
    });
}
