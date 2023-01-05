// ページの一部だけをreloadする関数
function ajaxUpdate(url, element, scroll_needed=false) {
    // urlを加工し、キャッシュされないurlにする。
    url = url + '?ver=' + new Date().getTime();
 
    // ajaxオブジェクト生成
    var ajax = new XMLHttpRequest;
 
    // ajax通信open
    ajax.open('GET', url, true);
 
    // ajax返信時の処理
    ajax.onload = function () {
        // ajax返信から得たHTMLでDOM要素を更新
        element.innerHTML = ajax.responseText;
        if (scroll_needed) {
            const dm_content = document.getElementById("dm-content");
            dm_content.scrollTo(0, dm_content.scrollHeight);            
        }
    };

    // ajax開始
    ajax.send(null);
}

const dm_sub_btn = document.getElementById("dm_sub_btn");
const url = TemplateVar.ajax_url
const div = document.getElementById("dm-content")
const dm_sender = document.getElementById('dm-form').children[1].children[1];
const ch = dm_sender.clientHeight;

document.addEventListener('DOMContentLoaded', () => {
    // ページ読み込み時にajaxでdmを読み込む
    ajaxUpdate(url, div, true);
    const dm_content = document.getElementById("dm-content");
    dm_content.scrollTo(0, dm_content.scrollHeight);

    // 
    dm_sender.addEventListener('input', () =>{
        dm_sender.style.height = ch + 'px';
        const sh = dm_sender.scrollHeight;
        dm_sender.style.height = sh + 'px';
    })
})

window.addEventListener('load', function () {
    setInterval(function () {
        ajaxUpdate(url, div);
    }, 6000);
});

dm_sub_btn.addEventListener('click', (event) => {
    event.preventDefault();
    const dm_text = document.getElementById('dm-form').children[1].children[1].value;
    const url = TemplateVar.url

    fetch(url, {
        method: 'POST',
        body: `dm_text=${dm_text}&dm_room_id=${TemplateVar.dm_room_id}`,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
            'X-CSRFToken': TemplateVar.csrf_token,
        },
    }).then(response => {
        return response.json();
    }).then(response => {
        console.log(response);
        var url = TemplateVar.ajax_url;
 
        var div = document.getElementById('dm-content');
        ajaxUpdate(url, div, true);
    }).catch(error => {
        console.log(error);
    });

    // dmフォームの入力欄を空にする
    document.getElementById('dm-form').children[1].children[1].value = "";

    // dmフォームの入力欄の高さを元に戻す
    dm_sender.style.height = ch + 'px';
    const sh = dm_sender.scrollHeight;
    dm_sender.style.height = sh + 'px';
})

