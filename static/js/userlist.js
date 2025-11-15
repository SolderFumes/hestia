let createButton = document.getElementById('createButton');
let createContainer = document.getElementById('createContainer');
let submitButton = document.getElementById('submit');
let user_names = document.getElementsByClassName('user_name');
let song_covers = document.getElementsByClassName('song_cover');
let song_names = document.getElementsByClassName('song_name');
let color_selectors = document.getElementsByClassName('color_selector');
const tenMB = 10000000
createButton.onclick = user_popup;

function user_popup() {
    createContainer.style.display = 'flex';
}

Array.from(user_names).forEach((nameP) => {
    nameP.addEventListener('click', (event) => {
        originalName = nameP.innerText;

        nameP.style.display = 'none';
        nameP.style.margin = '1rem';
        form = document.createElement('form');
        form.method = 'POST';
        nameP.parentNode.appendChild(form);

        input = document.createElement('input');
        input.required = true;
        input.placeholder = 'John Example';
        input.name = 'new_name';
        form.appendChild(input);

        type = document.createElement('input');
        type.name = 'type';
        type.value = 'update_name';
        type.style.display = 'none';
        form.appendChild(type);

        originalNameInput = document.createElement('input');
        originalNameInput.name = 'original_name';
        originalNameInput.value = originalName;
        originalNameInput.style.display = 'none'
        form.appendChild(originalNameInput);

        submit = document.createElement('input');
        submit.type = 'submit';
        submit.value = 'Change Name';
        form.appendChild(submit);
    });
});

songs_array = Array.from(song_covers).concat(Array.from(song_names));
songs_array.forEach((song_element) => {
    song_element.addEventListener('click', (event) => {
        // SO we want to be able to click either the song cover OR 
        // the song name and have it be replaced with a form.
        // We will add an event listener to every song cover and name.
        // We will then, on click, get the parent div of both the cover and name.
        // Now, we can un-display all of the children of the div, then display a form.
        // This solves the problem of creating two forms as it is (normally) impossible to
        // click something that has no display.
        parentDiv = song_element.parentNode;
        children = Array.from(parentDiv.children);
        children.forEach((child) => {child.style.display = 'none';});

        form = document.createElement('form');
        form.method = 'POST';
        parentDiv.appendChild(form);

        //We need to get the user's name to the backend.
        //We will messily traverse to parentDiv's parent, then get
        //The p with class user_name.
        superParentDiv = parentDiv.parentNode;
        userNameP = Array.from(superParentDiv.getElementsByClassName('user_name'))[0];
        userName = userNameP.innerText;
        //We will now make the input to pass the userName to the backend
        userNameInput = document.createElement('input');
        userNameInput.style.display = 'none';
        userNameInput.name = 'user_name'
        userNameInput.value = userName;
        form.appendChild(userNameInput);

        input = document.createElement('input');
        input.required = true;
        input.placeholder = 'https://spotify.com/example';
        input.name = 'new_song_url';
        input.pattern = 'https://.*';
        form.appendChild(input);

        type = document.createElement('input');
        type.name = 'type';
        type.value = 'update_song_url';
        type.style.display = 'none';
        form.appendChild(type);

        submit = document.createElement('input');
        submit.type = 'submit';
        submit.value = 'Change Music'
        form.appendChild(submit);
    });
});

Array.from(color_selectors).forEach((selectorP) => {
    selectorP.addEventListener('click', (event) => {
        selectorP.style.display = 'none';
        parentDiv = selectorP.parentNode;

        form = document.createElement('form');
        form.method = 'POST';
        parentDiv.appendChild(form);

        //We need to get the user's name to the backend.
        //We will messily traverse to parentDiv's parent, then get
        //The p with class user_name.
        superParentDiv = parentDiv.parentNode;
        userNameP = Array.from(superParentDiv.getElementsByClassName('user_name'))[0];
        userName = userNameP.innerText;
        //We will now make the input to pass the userName to the backend
        userNameInput = document.createElement('input');
        userNameInput.style.display = 'none';
        userNameInput.name = 'user_name'
        userNameInput.value = userName;
        form.appendChild(userNameInput);

        input = document.createElement('input');
        input.required = true;
        input.placeholder = 'r,g,b (0-255)';
        input.name = 'new_light_color';
        form.appendChild(input);

        type = document.createElement('input');
        type.name = 'type';
        type.value = 'update_light_color';
        type.style.display = 'none';
        form.appendChild(type);

        submit = document.createElement('input');
        submit.type = 'submit';
        submit.value = 'Change Light Color'
        form.appendChild(submit);
    });
});

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