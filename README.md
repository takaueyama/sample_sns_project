# ポートフォリオ紹介
短文投稿SNS Tmitter (http://18.177.215.25)<br>
以下の情報でゲストログインが可能です。<br>
username: guest<br>
password: pasuwa-do<br><br>


以下の内容で解説しております。
* Tmitterの概要
* 実装機能
* 使用技術

# Tmitterの概要
## テーマ
T*m*itterは既存のSNSアプリ「T*w*itter」を模したアプリです。短文の投稿機能を中心に、通知、ダイレクトメッセージ等の基本的な機能を全般的に実装しています。<br>
詳しくは下記の実装機能をご覧ください。

## こだわり
ユーザーの利用の快適さを重視しました。具体的には、いいね、フォロー、投稿の読み込み、ダイレクトメッセージや通知を受け取る際にページ全体を更新することなく結果が反映されるように実装しました。これによりユーザーにアクションをする度の更新の待ち時間がないようにしました。

# 実装機能
※⑤以外の画像はTmitter機能を実際に使っているYouTube動画へのリンクです。クリックしてご確認ください。
## ①短文投稿
◆短文の投稿、画像も添付可能<br>
[![](https://img.youtube.com/vi/UgJMfXGQF0M/0.jpg)](https://www.youtube.com/watch?v=UgJMfXGQF0M)<br>
◆いいね機能<br>
[![](https://img.youtube.com/vi/htzmIU5MxQM/0.jpg)](https://www.youtube.com/watch?v=htzmIU5MxQM)<br>
◆返信機能<br>
[![](https://img.youtube.com/vi/yD5ktNOGQD4/0.jpg)](https://www.youtube.com/watch?v=yD5ktNOGQD4)<br>
◆削除機能<br>
[![](https://img.youtube.com/vi/nFwAm1nW-SY/0.jpg)](https://www.youtube.com/watch?v=nFwAm1nW-SY)<br>
## ②ユーザー機能
◆新規登録<br>
[![](https://img.youtube.com/vi/_1T74_K3i4Y/0.jpg)](https://www.youtube.com/watch?v=_1T74_K3i4Y)<br>
◆ログイン<br>
[![](https://img.youtube.com/vi/i9MXEAblSXQ/0.jpg)](https://www.youtube.com/watch?v=i9MXEAblSXQ)
<br>
◆ログアウト<br>
[![](https://img.youtube.com/vi/uFy7ylDRHlI/0.jpg)](https://www.youtube.com/watch?v=uFy7ylDRHlI)<br>
◆フォロー機能<br>
[![](https://img.youtube.com/vi/beLxK3GBo0U/0.jpg)](https://www.youtube.com/watch?v=beLxK3GBo0U)<br>
## ③検索
◆投稿とユーザーの部分一致検索<br>
[![](https://img.youtube.com/vi/TRxWIsag0m8/0.jpg)](https://www.youtube.com/watch?v=TRxWIsag0m8)<br>
## ④ダイレクトメッセージ
◆他のユーザーとショートメッセージのやり取りが可能<br>
[![](https://img.youtube.com/vi/Q5JFLQoZk3g/0.jpg)](https://www.youtube.com/watch?v=Q5JFLQoZk3g)<br>
◆画面の更新不要でリアルタイムでメッセージが更新されます<br>
[![](https://img.youtube.com/vi/8lKAEPyOdlw/0.jpg)](https://www.youtube.com/watch?v=8lKAEPyOdlw)<br>
## ⑤通知
◆自分が受け取ったフォロー、いいね、ダイレクトメッセージの一覧<br>
<img src="gif/notification.png" width="80%"><br>
◆新規の通知やダイレクトメッセージがあった際にリアルタイムで知らされます<br>
<img src="gif/bluecircle.png" width="80%"><br>

# 使用技術
◆フロントエンド<br>
* HTML/CSS<br>
* Javascript<br>

◆バックエンド<br>
* Python<br>
* Django（Pythonフレームワーク）<br>

◆インフラ<br>
* AWS EC2（仮想サーバー）<br>
* Gunicorn（Webアプリ起動）<br>
* Nginx（Webサーバー）<br>
* PostgreSQL（データベース）<br>
* Github（バージョン管理）<br>
