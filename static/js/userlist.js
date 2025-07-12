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
    createForm.appendChild(uploadPicture);

    let nameInput = document.createElement('input');
    nameInput.name = 'name';
    nameInput.placeholder = 'Name...';
    createForm.appendChild(nameInput);

    let songInput = document.createElement('input');
    songInput.name = 'song_url';
    songInput.placeholder = 'Song URL...';
    createForm.appendChild(songInput);

    let lightInput = document.createElement('input');
    lightInput.type = 'number';
    lightInput.name = 'light_color';
    lightInput.placeholder = 'Light Color (r, g ,b)...';
    createForm.appendChild(lightInput);

    let submit = document.createElement('input');
    submit.type = 'submit';
    submit.className = 'submit';
    createForm.appendChild(submit);
}
