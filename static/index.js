document.addEventListener('DOMContentLoaded', function () {
    const urlInput = document.getElementById('urlInput');
    const addButton = document.querySelector('.add-button');

    // Existing code for input validation
    urlInput.addEventListener('input', function () {
        const isValidUrl = validateUrl(this.value);
        addButton.disabled = !isValidUrl;
        addButton.style.backgroundColor = isValidUrl ? '#638fff' : '#d9d9d9';
    });

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

    // Function to validate the URL
    function validateUrl(url) {
        const parts = url.split('?v=');
        const isValidFormat = parts.length === 2 && parts[0].length > 0 && parts[1].length > 0;
        return isValidFormat;
    }

    // Event listener for the Add button
    addButton.addEventListener('click', function () {
        const videoUrl = urlInput.value;
        if (validateUrl(videoUrl)) {
            addVideo(videoUrl);
        } else {
            alert('Invalid URL. Please enter a valid URL.');
        }
    });

    // Function to send the POST request to add a video
    function addVideo(videoUrl) {
        const videoId = videoUrl.split("?v=")[1]
        console.log(videoId)

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

    document.querySelectorAll('.item-box').forEach(item => {
        item.addEventListener('click', function () {
            const videoId = this.getAttribute('data-video-id');
            window.location.href = `http://127.0.0.1:8000/detail/${videoId}`;
        });
    });

    document.querySelectorAll('.copy-button').forEach(button => {
        button.addEventListener('click', function () {
            const scriptText = this.nextElementSibling.textContent; // Get the script text
            navigator.clipboard.writeText(scriptText).then(function () {
                console.log('Script copied to clipboard successfully!');
                button.textContent = 'Copied!'; // Change button text or add more visual feedback if needed
                setTimeout(() => { button.textContent = '붙여넣기'; }, 2000); // Reset button text after 2 seconds
            }, function (err) {
                console.error('Could not copy text: ', err);
            });
        });
    });

    document.querySelectorAll('.delete-button').forEach(button => {
        button.addEventListener('click', function (event) {
            event.stopPropagation(); // Prevent triggering click on the item-box
            const videoId = this.getAttribute('data-video-id');
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
        });
    });

    document.querySelector('.create-script-button').addEventListener('click', function () {
        const videoId = this.getAttribute('data-video-id');
        fetch(`http://127.0.0.1:8000/script/${videoId}`, {
            method: 'POST',
        })
        .then(response => {
            if (response.ok) {
                window.location.reload();
            } else {
                console.error('Server responded with a non-OK status:', response.status);
            }
        })
        .catch(error => {
            console.error('Error creating script:', error);
        });
    });

    const createBlogButton = document.querySelector('.create-blog-button');
    if (createBlogButton) {
        createBlogButton.addEventListener('click', function () {
            const scriptId = this.getAttribute('data-script-id');
            startBlogStream(scriptId);
        });
    } else {
        console.log('Create blog button not found.');
    }

    function startBlogStream(scriptId) {
        const eventSource = new EventSource(`http://127.0.0.1:8000/blog/${scriptId}/stream`);
        eventSource.onmessage = function(event) {
            // Process the incoming event data
            updateBlogContent(event.data);
        };
        eventSource.onerror = function(error) {
            console.error("EventSource failed:", error);
            eventSource.close();
        };
    }

    function updateBlogContent(data) {
        // Update your blog content area with the incoming data
        const blogContent = document.querySelector('.blog-content');
        if (blogContent) {
            blogContent.textContent = data; // or append the data if it's a progressive update
        }
    }
});
