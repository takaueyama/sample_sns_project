//  フォローの非同期処理
function follow(e) {
    const pk = this.button.dataset.pk;
    e.preventDefault();
    const url = TemplateVar.follow_url;
    fetch(url, {
        method: 'POST',
        body: `followed_user_id=${pk}`,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
            'X-CSRFToken': TemplateVar.csrf_token,
        },
    }).then(response => {
        return response.json();
    }).then(response => {
        const following_text = document.getElementById(`follow-${pk}`);

        if (response.method === 'follow') {
            following_text.textContent = "フォロー中";
        } else {
            following_text.textContent = "フォローする";
        } 
    }).catch(error => {
        console.log(error);
    });
}

let user_page = 1;
var user_pks =[];
let user_content = document.getElementById('user_content');
const load_user_btn = document.getElementById('load_user');

document.addEventListener('DOMContentLoaded', function (){
    if (TemplateVar.search_value !== TemplateVar.random_string) {
        const url = TemplateVar.user_content_url + '?page=' + user_page + '&q=' + TemplateVar.search_value;
        fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
            },
        }).then(response => {
            return response.json();
        }).then(response => {
            // 指定した要素の中の末尾に挿入
            user_content.insertAdjacentHTML('beforeend', response.content);
            const follow_buttons = document.getElementsByClassName("follow");
            for (const button of follow_buttons) {
                button.addEventListener('click', {button: button, handleEvent: follow});            
            }
            for (const button of follow_buttons) {
                user_pks.push(button.dataset.pk);
            }
            if (response.user_max_page_number == 0) {
                load_user_btn.style.display = 'none';
                let message = document.createElement('p');
                message.textContent = 'ユーザーの検索結果はありません';
                user_content.appendChild(message);
            } else if (response.user_max_page_number == 1) {
                load_user_btn.style.display = 'none';
                let message = document.createElement('p');
                message.textContent = 'ユーザーは以上です';
                user_content.appendChild(message);
            } else {
                user_page++;  
            }
        }).catch(error => {
            console.log(error);
        });
    }
});

if (TemplateVar.search_value !== TemplateVar.random_string){
    load_user_btn.addEventListener('click', function (){
        const url = TemplateVar.user_content_url + '?page=' + user_page + '&q=' + TemplateVar.search_value;
        fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
            },
        }).then(response => {
            return response.json();
        }).then(response => {
            // 指定した要素の中の末尾に挿入
            user_content.insertAdjacentHTML('beforeend', response.content);
            const follow_buttons = document.getElementsByClassName("follow");
            for (const button of follow_buttons) {
                button.addEventListener('click', {button: button, handleEvent: follow});            
            }
            for (const button of follow_buttons) {
                user_pks.push(button.dataset.pk);
            }
            if (response.user_max_page_number == 0) {
                load_user_btn.style.display = 'none';
                let message = document.createElement('p');
                message.textContent = 'ユーザーの検索結果はありません';
                user_content.appendChild(message);
            } else if (response.user_max_page_number == 1 || response.user_max_page_number <= user_page) {
                load_user_btn.style.display = 'none';
                let message = document.createElement('p');
                message.textContent = 'ユーザーは以上です';
                user_content.appendChild(message);
            } else {
                user_page++;  
            }
        }).catch(error => {
            console.log(error);
        });
    });
}