const header_modal = document.getElementById('headerModal');
const icon_modal = document.getElementById('iconModal');
const icon_close_button = document.getElementsByClassName('modalClose')[1];
const header_close_button = document.getElementsByClassName('modalClose')[0];
const icon_image_input = document.getElementById('icon_image_input')
const header_image_input = document.getElementById('header_image_input')
const form_paragraphs = document.getElementById('form').getElementsByTagName('p');
const num_of_image_chars = 15;

// 投稿画像の名前をランダマイズする
const generateRandomString = (num) => {
    const characters ='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
    let result = '';
    const charactersLength = characters.length;
    for (let i = 0; i < num; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
  
    return result;
}

document.addEventListener('DOMContentLoaded', function (){
    // form.as_p で自動的に表示されるもので不要なものを非表示にする
    for(let i = 0; i < 2; i++) {
        form_paragraphs[i].style.display = 'none';
    }

    let header_cropper = null
    header_image_input.addEventListener('change', function(changeFileEvent){
        if(header_cropper){
            header_cropper.destroy();
        }
        header_modal.style.display = 'block';
        const fReaderForURI = new FileReader();
        // Base64 エンコード
        fReaderForURI.readAsDataURL(changeFileEvent.target.files[0]);
        fReaderForURI.onload = () => {
            const imgEl = document.getElementById('header-cropper-tgt');
            imgEl.src = String(fReaderForURI.result);
            header_cropper = new Cropper(imgEl, {
                aspectRatio: 3 / 1,
                viewMode: 1,
                dragMode: "move",
                background: false,
                cropBoxMovable: false,
                minCropBoxHeight: 300,
                minCropBoxWidth: 900,
            });
        }

        document.getElementById('header-btn-crop-action').addEventListener('click', function(){
            /** @var {HTMLCanvasElement} croppedCanvas */
            header_modal.style.display = 'none';
            const croppedCanvas = header_cropper.getCroppedCanvas({
                // 出力画像のサイズ指定
                width: 1500,
                height: 500,
              });
            document.getElementById('header-preview').src = croppedCanvas.toDataURL();
            croppedCanvas.toBlob(function(imgBlob){
                const croppedImgFile = new File([imgBlob], generateRandomString(num_of_image_chars)+'.png' , {type: "image/png"});
                const dt = new DataTransfer();
                dt.items.add(croppedImgFile);
                document.querySelector('input[name="header_image"]').files = dt.files;
            });
        })
        header_image_input.value = '';
    })

    /** @var {Cropper|null} Cropperインスタンスを保持する関数 */
    let icon_cropper = null
    icon_image_input.addEventListener('change', function(changeFileEvent){
        if(icon_cropper){
            icon_cropper.destroy();
        }
        icon_modal.style.display = 'block';
        const fReaderForURI = new FileReader();
        fReaderForURI.readAsDataURL(changeFileEvent.target.files[0]);
        fReaderForURI.onload = () => {
            const imgEl = document.getElementById('icon-cropper-tgt');
            imgEl.src = String(fReaderForURI.result);
            icon_cropper = new Cropper(imgEl, {
                aspectRatio: 1 / 1,
                viewMode: 1,
                dragMode: "move",
                background: false,
                cropBoxMovable: false,
                minCropBoxHeight: 300,
                minCropBoxWidth: 300,
            });
        }

        document.getElementById('icon-btn-crop-action').addEventListener('click', function(){
            /** @var {HTMLCanvasElement} croppedCanvas */
            icon_modal.style.display = 'none';
            const croppedCanvas = icon_cropper.getCroppedCanvas({
                width: 300,
                height: 300,
              });
            document.getElementById('icon-preview').src = croppedCanvas.toDataURL()
            croppedCanvas.toBlob(function(imgBlob){
                const croppedImgFile = new File([imgBlob], generateRandomString(num_of_image_chars)+'.png' , {type: "image/png"});
                const dt = new DataTransfer();
                dt.items.add(croppedImgFile);
                document.querySelector('input[name="icon_image"]').files = dt.files;
            });
        })
        icon_image_input.value = '';
    })

    header_close_button.addEventListener('click', header_modal_close);
    function header_modal_close() {
        header_modal.style.display = 'none';
    }

    icon_close_button.addEventListener('click', icon_modal_close);
    function icon_modal_close() {
        icon_modal.style.display = 'none';
    }

    addEventListener('click', outsideClose);
    function outsideClose(e) {
      if (e.target == header_modal) {
        header_modal.style.display = 'none';
        const croppedCanvas = header_cropper.getCroppedCanvas({
            // 出力画像のサイズ指定
            width: 1500,
            height: 500,
          });
        document.getElementById('header-preview').src = croppedCanvas.toDataURL()
        croppedCanvas.toBlob(function(imgBlob){
            const croppedImgFile = new File([imgBlob], generateRandomString(num_of_image_chars)+'.png' , {type: "image/png"});
            const dt = new DataTransfer();
            dt.items.add(croppedImgFile);
            document.querySelector('input[name="header_image"]').files = dt.files;
        });
      }
      if (e.target == icon_modal) {
        icon_modal.style.display = 'none';
            /** @var {HTMLCanvasElement} croppedCanvas */
            icon_modal.style.display = 'none';
            const croppedCanvas = icon_cropper.getCroppedCanvas({
                // 出力画像のサイズ指定
                width: 300,
                height: 300,
              });
            document.getElementById('icon-preview').src = croppedCanvas.toDataURL()
            croppedCanvas.toBlob(function(imgBlob){
                const croppedImgFile = new File([imgBlob], generateRandomString(num_of_image_chars)+'.png' , {type: "image/png"});
                const dt = new DataTransfer();
                dt.items.add(croppedImgFile);
                document.querySelector('input[name="icon_image"]').files = dt.files;
            });
      }
    }
})