let createButton = document.getElementById('createButton');
createButton.onclick = user_popup;

function user_popup() {
    let createContainer = document.createElement('div');
    createContainer.className = 'createContainer'
    document.body.appendChild(createContainer);

    let createForm = document.createElement('form');
    createForm.method = 'POST';
    createForm.enctype = 'multipart/form-data';
    createContainer.appendChild(createForm);


    let uploadPicture = document.createElement('input');
    uploadPicture.type = 'file';
    uploadPicture.name = 'img';
    uploadPicture.required = true;
    createForm.appendChild(uploadPicture);

    let nameInput = document.createElement('input');
    nameInput.name = 'name';
    nameInput.placeholder = 'Name...';
    nameInput.required = true;
    createForm.appendChild(nameInput);

    let songInput = document.createElement('input');
    songInput.name = 'song_url';
    songInput.type = 'url';
    songInput.placeholder = 'https://spotify.com/example';
    songInput.pattern = 'https://.*'
    songInput.required = true;
    createForm.appendChild(songInput);

    let lightInput = document.createElement('input');
    lightInput.name = 'light_color';
    lightInput.required = true;
    lightInput.placeholder = 'R (0-255), G (0-255), B (0-255)';
    lightInput.pattern = '.{1,3},.{1,3},.{1,3}';
    createForm.appendChild(lightInput);

    let submit = document.createElement('input');
    submit.type = 'submit';
    submit.className = 'submit';
    createForm.appendChild(submit);
}
