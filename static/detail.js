const BASE_URL = "http://127.0.0.1:8000";
const controller = new AbortController();
const signal = controller.signal;


document.addEventListener('DOMContentLoaded', function () {
    // 안먹음.. 나중에 고치기
    const homeButton = document.querySelector('.home-button');
    if (homeButton) {
        homeButton.addEventListener('click', () => {
            controller.abort();
        });
    }

    setupCreateScriptButton();
    setupCopyScriptButton();
    setupCreateBlogButton();
    setupCopyBlogButton();
});

function setupCreateScriptButton() {
    document.querySelectorAll('.create-script-button').forEach(button => {
        button.addEventListener('click', function () {
            const videoId = this.getAttribute('data-video-id');
            createScript(videoId);
        });
    });
}

function setupCopyScriptButton() {
    const copyScriptButton = document.querySelector('.copy-script-button');
    if (copyScriptButton) {
        copyScriptButton.addEventListener('click', function () {
            const scriptContent = document.querySelector('.script-content').textContent;

            const textArea = document.createElement('textarea');
            textArea.value = scriptContent;
            document.body.appendChild(textArea);

            textArea.select();

            document.body.removeChild(textArea);

            copyScriptButton.textContent = '완료';
            setTimeout(() => { copyScriptButton.textContent = '복사'; }, 2000);
        });
    }
}

function setupCreateBlogButton() {
    document.querySelectorAll('.create-blog-button').forEach(button => {
        button.addEventListener('click', function () {
            const scriptId = this.getAttribute('data-script-id');
            createBlog(scriptId);
        });
    });
}

function setupCopyBlogButton() {
    const copyBlogButton = document.querySelector('.copy-blog-button');
    if (copyBlogButton) {
        copyBlogButton.addEventListener('click', function () {
            const blogContent = document.querySelector('.blog-content').innerHTML;

            const textArea = document.createElement('textarea');
            textArea.value = blogContent.replace(/<br>/g, '\n');
            document.body.appendChild(textArea);

            textArea.select();

            document.body.removeChild(textArea);

            copyBlogButton.textContent = '완료';
            setTimeout(() => { copyBlogButton.textContent = '복사'; }, 2000);
        });
    }
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
    showSkeletonUI();
    fetch(`${BASE_URL}/blog/${scriptId}`, {
        method: 'POST',
        headers: {
            'Content-Type': "application/json",
        },
        body: JSON.stringify({script_id: scriptId}),
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
    })
    .then(data => {
        hideSkeletonUI();
        window.location.reload();
    })
    .catch(error => {
        console.error('블로그 생성 오류:', error);
        hideSkeletonUI();
    });

    window.addEventListener('unload', () => controller.abort());
}

function showSkeletonUI() {
    const blogContent = document.querySelector('.blog-content');
    if (blogContent) {
        blogContent.innerHTML = '<div class="skeleton"></div>';
    }
}

function hideSkeletonUI() {
    const skeleton = document.querySelector('.skeleton');
    if (skeleton) {
        skeleton.remove();
    }
}