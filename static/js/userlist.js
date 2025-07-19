let createButton = document.getElementById('createButton');
let createContainer = document.getElementById('createContainer');
let submitButton = document.getElementById('submit')
let tenMB = 10000000
createButton.onclick = user_popup;

function user_popup() {
    createContainer.style.display = 'flex';
}

const uploadBox = document.getElementById('upload_box');
const fileInput = document.getElementById('file_input');

//add two event listeners, toggle CSS class for drag-over
['dragenter', 'dragover'].forEach(eventType => { 
    uploadBox.addEventListener(eventType, event => {
        event.preventDefault();
        uploadBox.classList.add('drag-over'); // uploadBox is being dragged-over rn
    });
});

//un-toggle css class 
['dragleave'].forEach(eventType => {
    uploadBox.addEventListener(eventType, event => {
        event.preventDefault();
    });
});

uploadBox.addEventListener('drop', event => {
    event.preventDefault();
    uploadBox.classList.remove('drag-over');
    if (event.dataTransfer.files.length > 0) {
        fileInput.files = event.dataTransfer.files;
    }
});

fileInput.addEventListener('change', event => {
    let nameP = document.getElementById("fileName");
    let file = fileInput.files[0];
    if (file.size > tenMB) {
        nameP.innerText = `${file.name} is too big (${(file.size / 1024 / 1024).toFixed(3)} MB)! Max file size is 10 MB.`
        uploadBox.classList.add('error');
        submitButton.disabled = true;
    } else {
        uploadBox.classList.remove('error');
        nameP.innerText = `${file.name} ${(file.size / 1024 / 1024).toFixed(3)} MB`
        submitButton.disabled = false;
    }
});

document.querySelectorAll('.delButton').forEach(button => {
    button.addEventListener('click', async () => {
        const userName = button.dataset.user_name;
        const res = await fetch('/userlist', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_name: userName})
        });
        if (res.ok) {
            location.reload();
        }
    });
});