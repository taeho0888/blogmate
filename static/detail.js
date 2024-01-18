const BASE_URL = "http://127.0.0.1:8000";

document.addEventListener('DOMContentLoaded', function () {
    setupCreateScriptButton();
    setupCreateBlogButton();
    setupCopyToClipboardButton();
});

function setupCreateScriptButton() {
    document.querySelectorAll('.create-script-button').forEach(button => {
        button.addEventListener('click', function () {
            const videoId = this.getAttribute('data-video-id');
            createScript(videoId);
        });
    });
}

function setupCreateBlogButton() {
    document.querySelectorAll('.create-blog-button').forEach(button => {
        button.addEventListener('click', function () {
            const scriptId = this.getAttribute('data-script-id');
            createBlog(scriptId);
        });
    });
}

function setupCopyToClipboardButton() {
    document.querySelectorAll('.copy-button').forEach(button => {
        button.addEventListener('click', function () {
            const scriptText = this.nextElementSibling.textContent;
            navigator.clipboard.writeText(scriptText).then(function () {
                console.log('Script copied to clipboard successfully!');
                button.textContent = 'Copied!';
                setTimeout(() => { button.textContent = 'Copy'; }, 2000);
            }, function (err) {
                console.error('Could not copy text: ', err);
            });
        });
    });
}

function createScript(videoId) {
    fetch(`${BASE_URL}/script/${videoId}`, {
        method: 'POST',
        headers: {
            'Content-Type': "application/json",
        },
        body: JSON.stringify({id: videoId}),
    })
    .then(response => {
        if (response.ok) {
            window.location.reload();
        } else {
            console.error('자막 생성 응답 오류:', response.status);
        }
    })
    .catch(error => {
        console.error('자막 생성 오류:', error);
    });
}

function createBlog(scriptId) {
    fetch(`${BASE_URL}/blog/${scriptId}`, {
        method: 'POST',
        headers: {
            'Content-Type': "application/json",
        },
        body: JSON.stringify({script_id: scriptId}),
    })
    .then(response => {
        if (response.ok) {
            window.location.reload();
        } else {
            console.error('블로그 생성 응답 오류:', response.status);
        }
    })
    .catch(error => {
        console.error('블로그 생성 오류:', error);
    })
}

// You might want to include the startBlogStream function if you are streaming updates for blog creation
function startBlogStream(scriptId) {
    // Existing logic for handling blog creation stream
}

function updateBlogContent(data) {
    // Existing logic for updating the blog content area with the incoming data
}
