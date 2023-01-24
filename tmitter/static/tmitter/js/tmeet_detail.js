//  いいねの非同期処理
// idがpkのTmeetに対していいね処理を付与する
function like(e) {
    const pk = this.button.dataset.pk
    e.preventDefault();
    const url = TemplateVar.like_url;
    fetch(url, {
        method: 'POST',
        body: `tmeet_id=${pk}`,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
            'X-CSRFToken': TemplateVar.csrf_token,
        },
    }).then(response => {
        return response.json();
    }).then(response => {
        const counter = document.getElementById(`like-count-${pk}`)
        const icon = document.getElementById(`like-icon-${pk}`)
        counter.textContent = response.like_count
        if (response.method == 'create') {
            icon.textContent = "♥";
        } else {
            icon.textContent = "♡";
        } 
    }).catch(error => {
        console.log(error);
    });
}

// 検索結果を読み込む処理
function f(){
    const url = TemplateVar.target_url + '?page=' + page;
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        },
    }).then(response => {
        return response.json();
    }).then(response => {
        // 指定した要素の中の末尾に挿入
        tmeet_content.insertAdjacentHTML('beforeend', response.content);
        
        // ここにいいねの処理書く
        const like_buttons = document.getElementsByClassName('like');
        for (const button of like_buttons) {
            button.addEventListener('click', {button: button, handleEvent: like});            
        }
        for (const button of like_buttons) {
            tmeet_pks.push(button.dataset.pk);
        }
        if (response.max_page_number == page) {
            load_tmeet_btn.style.display = "none";
            load_tmeet_btn.style.display = "none";
            let message = document.createElement('p');
            message.textContent = '返信は以上です';
            tmeet_content.appendChild(message);
        } else {
            page++;
        }
    }).catch(error => {
        console.log(error);
    });
}

function delete_tmeet(delete_btn) {
    const pk = delete_btn.dataset.pk;
    e.preventDefault();
    const url = TemplateVar.delete_tmeet + '?tmeet_id=' + pk;
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        },
    }).then(response => {
        return response.json();
    }).then(response => {
        // console.log("削除が押されました");
        // console.log(response);
        if (response.deleted) {
            document.getElementById(`tmeet-${pk}`).style.display = "none";
        } else {
            // 何もしない
        }
    }).catch(error => {
        console.log(error);
    });
}

// 親Tmeetのページ
let parent_page = 1;
// let tmeet_pks = [];
let like_pks = [];
let delete_pks = [];
const reply_content = document.getElementById('reply_content');
const parent_content = document.getElementById('parent_content');
const load_reply_btn = document.getElementById('load_reply_btn');

document.addEventListener('DOMContentLoaded', function (){
    const url = TemplateVar.target_url + '?tmeet_id=' + TemplateVar.tmeet_id + '&page=' + parent_page;
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        },
    }).then(response => {
        return response.json();
    }).then(response => {
        // 指定した要素の中の末尾に挿入
        reply_content.insertAdjacentHTML('beforeend', response.content);

        // 新しく追加したlikeボタンにいいね機能を付与する
        const like_buttons = document.getElementsByClassName('like');
        for (const button of like_buttons) {
            if (!like_pks.includes(button.dataset.pk)) {
                button.addEventListener('click', {button: button, handleEvent: like});
            } 
        }
        for (const button of like_buttons) {
            like_pks.push(button.dataset.pk);
        }

        // 新しく追加したdeleteボタンに削除機能を付与する
        const delete_btns = document.getElementsByClassName("delete_btn");
        for (const delete_btn of delete_btns) {
            if (!delete_pks.includes(delete_btn.dataset.pk)){
                delete_btn.addEventListener('click', () => {
                    let check = confirm('Tmeetを削除してもよろしいですか？');
                    if (check) {
                        delete_tmeet(delete_btn);
                    }
                });
            }
        }
        for (const button of delete_btns) {
            delete_pks.push(button.dataset.pk);
        }

        if (response.max_page_number == 1 || response.max_page_number == 0) {
            load_reply_btn.style.display = "none";
            let message = document.createElement('p');
            if (response.max_page_number == 1) {
                message.textContent = '返信は以上です';
            }
            reply_content.appendChild(message);
        } else {
            parent_page++;
        }
    }).catch(error => {
        console.log(error);
    });
})

load_reply_btn.addEventListener('click', function (){
    const url = TemplateVar.target_url + '?tmeet_id=' + TemplateVar.tmeet_id + '&page=' + parent_page;
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        },
    }).then(response => {
        return response.json();
    }).then(response => {
        // 指定した要素の中の末尾に挿入
        reply_content.insertAdjacentHTML('beforeend', response.content);
        
        // 新しく追加したlikeボタンにいいね機能を付与する
        const like_buttons = document.getElementsByClassName('like');
        for (const button of like_buttons) {
            if (!like_pks.includes(button.dataset.pk)) {
                button.addEventListener('click', {button: button, handleEvent: like});
            }        
        }
        for (const button of like_buttons) {
            like_pks.push(button.dataset.pk);
        }

        // 新しく追加したdeleteボタンに削除機能を付与する
        const delete_btns = document.getElementsByClassName("delete_btn");
        for (const delete_btn of delete_btns) {
            if (!delete_pks.includes(delete_btn.dataset.pk)){
                delete_btn.addEventListener('click', () => {
                    let check = confirm('Tmeetを削除してもよろしいですか？');
                    if (check) {
                        delete_tmeet(delete_btn);
                    }
                });
            }
        }
        for (const button of delete_btns) {
            delete_pks.push(button.dataset.pk);
        }

        if (response.max_page_number == parent_page) {
            load_reply_btn.style.display = "none";
            let message = document.createElement('p');
            message.textContent = '返信は以上です';
            reply_content.appendChild(message);
        } else {
            parent_page++;
        }
        console.log(response.max_page_number+':'+ parent_page);
    }).catch(error => {
        console.log(error);
    });
})