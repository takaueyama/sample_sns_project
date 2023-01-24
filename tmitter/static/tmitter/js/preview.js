function main () {
    const input = document.querySelector('#id_picture1');
    const preview_image = document.getElementsByClassName('picture_preview')[0];

    input.addEventListener('change', (event) => {
        const [file] = event.target.files;
        if (file) {
            preview_image.setAttribute('src', URL.createObjectURL(file));
        } else {
            // 何もしない
        }
    })
}

main()