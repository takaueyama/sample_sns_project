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
        const counter = document.getElementById(`like-count-${pk}`);
        const icon = document.getElementById(`like-icon-${pk}`);
        counter.textContent = response.like_count
        if (response.method == 'create') {
            icon.textContent = "♥";
        } else {
            icon.textContent = "♡";
        }
        console.log("いいねされました");
    }).catch(error => {
        console.log(error);
    });
}

// follow関数
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
        const follower_count = document.getElementById("follower_count");
        const follow_btn = following_text.parentElement

        if (response.method === 'follow') {
            following_text.textContent = "フォロー中";
            follow_btn.classList.replace('follow-action', 'unfollow-action');
            if (follower_count) {
                follower_count.textContent = Number(follower_count.textContent) + 1;
            }
            // console.log(following_text);
        } else {
            following_text.textContent = "フォロー";
            follow_btn.classList.replace('unfollow-action', 'follow-action');
            if (follower_count) {
                follower_count.textContent = Number(follower_count.textContent) - 1;
            }      
        }
        console.log("フォローボタンが押されました。");
    }).catch(error => {
        console.log(error);
    });
}

// function delete_tmeet(e) {
//     const pk = this.delete_btn.dataset.pk;
//     e.preventDefault();
//     const url = TemplateVar.delete_tmeet + '?tmeet_id=' + pk;
//     fetch(url, {
//         method: 'GET',
//         headers: {
//             'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
//         },
//     }).then(response => {
//         return response.json();
//     }).then(response => {
//         console.log(response);
//         if (response.deleted) {
//             document.getElementById(`tmeet-${pk}`).style.display = "none";
//         } else {

//         }
//         console.log("削除されました");
//     }).catch(error => {
//         console.log(error);
//     });
// }

function delete_tmeet(delete_btn) {
    const pk = delete_btn.dataset.pk;
    // e.preventDefault();
    const url = TemplateVar.delete_tmeet + '?tmeet_id=' + pk;
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        },
    }).then(response => {
        return response.json();
    }).then(response => {
        console.log(response);
        if (response.deleted) {
            document.getElementById(`tmeet-${pk}`).style.display = "none";
        } else {

        }
        console.log("削除されました");
    }).catch(error => {
        console.log(error);
    });
}

// 無限スクロール機能
let page = 1;
// keyがreply_contentのid、valueがpage
let target_content = document.getElementById(TemplateVar.target_content);
let loadingFlag = false;
let like_pks = [];
let delete_pks = [];
let follow_pks = [];

// ページ読み込みが完了したら
document.addEventListener('DOMContentLoaded', function (){
    const url = TemplateVar.target_content_url + 'page=1';
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        },
    }).then(response => {
        return response.json();
    }).then(response => {
        // 指定した要素の中の末尾に挿入
        target_content.insertAdjacentHTML('beforeend', response.content);

        // 終了判定
        if (response.max_page_number <= page) {
            document.getElementById("loading_message").style.display = "none";
            let message = document.createElement('p');
            if (response.max_page_number == 0) {
                message.textContent = '表示するコンテンツがありません';
            } else {
                message.textContent = '以上です';
            }
            
            target_content.appendChild(message);
            loadingFlag = true;
        } else {
            page++;
        }

        // 新しく追加したlikeボタンにいいね機能を付与する
        const like_buttons = document.getElementsByClassName("like");
        for (const button of like_buttons) {
            if (!like_pks.includes(button.dataset.pk)){
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
                // delete_btn.addEventListener('click', {delete_btn: delete_btn, handleEvent: delete_tmeet});
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

        // 新しく追加したfollowボタンにフォロー機能を付与する
        const follow_btns = document.getElementsByClassName("follow");
        for (const follow_btn of follow_btns) {
            if (!follow_pks.includes(follow_btn.dataset.pk)) {
                follow_btn.addEventListener('click', {button: follow_btn, handleEvent: follow});
            }
        }
        for (const button of follow_btns) {
            follow_pks.push(button.dataset.pk);
        }
        
    }).catch(error => {
        console.log(error);
    });
});


window.addEventListener('scroll', () => {
    if (!loadingFlag) {
        const bodyHeight = document.body.clientHeight // bodyの高さを取得
        const windowHeight = window.innerHeight // windowの高さを取得
        const bottomPoint = bodyHeight - windowHeight // ページ最下部までスクロールしたかを判定するための位置を計算
        const currentPos = window.pageYOffset // スクロール量を取得

        if (bottomPoint <= currentPos) { // スクロール量が最下部の位置を過ぎたかどうか
            loadingFlag = true
            const url = TemplateVar.target_content_url + 'page=' + String(page);
            fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                },
            }).then(response => {
                return response.json();
            }).then(response => {
                // 指定した要素の中の末尾に挿入
                target_content.insertAdjacentHTML('beforeend', response.content);
        
                // 終了判定
                if (page >= response.max_page_number) {
                    // 読み込み終了時
                    document.getElementById("loading_message").style.display = "none";
                    let message = document.createElement('p');
                    message.textContent = '以上です';
                    target_content.appendChild(message);
                    loadingFlag = true;
                } else {
                    // 読み込み未完時
                    loadingFlag = false;
                    page++;
                }
                const like_buttons = document.getElementsByClassName("like");
                for (const button of like_buttons) {
                    if (!like_pks.includes(button.dataset.pk)){
                        button.addEventListener('click', {button: button, handleEvent: like});
                    } 
                }
                for (const button of like_buttons) {
                    like_pks.push(button.dataset.pk);
                }
                // 新しく追加したdeleteボタンに削除機能を追加する
                const delete_btns = document.getElementsByClassName("delete_btn");
                for (const delete_btn of delete_btns) {
                    if (!delete_pks.includes(delete_btn.dataset.pk)){
                        // delete_btn.addEventListener('click', {delete_btn: delete_btn, handleEvent: delete_tmeet});
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

                // 新しく追加したfollowボタンにフォロー機能を追加する
                const follow_btns = document.getElementsByClassName("follow");
                for (const follow_btn of follow_btns) {
                    if (!follow_pks.includes(follow_btn.dataset.pk)) {
                        follow_btn.addEventListener('click', {button: follow_btn, handleEvent: follow});
                    }
                }
                for (const button of follow_btns) {
                    follow_pks.push(button.dataset.pk);
                }

            }).catch(error => {
                console.log(error);
            });
        }
    }
})