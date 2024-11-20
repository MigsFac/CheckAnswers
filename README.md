
## 1.問題集の答え番号を事前に入力、ひたすら答えを選んで答え合わせするアプリ

## 2.G検定で出てくるコサイン類似度やユークリッド距離、混同行列、特徴Mapの計算機

## 3.データベースを用いた用語集

## デモ：https://migsfactory.tech/

# 概要
## 1.答え合わせアプリ

191問、答え合わせする時間がもったいのと記録に残したい。本番のweb入力する雰囲気も味わえる。
時間も計れます。入力した一覧を見れるようにし、その問題番号をダブルクリックすると飛べます。
気になる問題にはチェックをつけておき、記録に残します。
試用を兼ねて、簡単なログイン機能も搭載。

<img width="497" alt="CheckAns1" src="https://github.com/user-attachments/assets/73a0796f-5c51-4882-8ec7-5ea7bf75ef54">
<img width="489" alt="CheckAns2" src="https://github.com/user-attachments/assets/5632560e-d6a2-4826-8958-2099179a8cfb">
<img width="484" alt="CheckAns3" src="https://github.com/user-attachments/assets/7a17bfe5-d664-4c5b-a2c8-36695b54aba5">
<img width="494" alt="CheckAns4" src="https://github.com/user-attachments/assets/99d0ed19-27b7-4112-b3c4-5daff157926a">

## 2.G検定用計算機

計算方法はわかってるのに計算するのが大変すぎるので、計算機を作ってみました。

<img width="703" alt="cosin" src="https://github.com/user-attachments/assets/bafc6ba3-b86f-4d52-87da-68e1ec17a844">
<img width="829" alt="FMap" src="https://github.com/user-attachments/assets/5948d493-eec4-4458-9ddb-d822e4db12b8">

## 3.データベースを用いた用語集

用語を登録しておいて、allからは読み仮名で検索可能。
大項目を選ぶとその内容と小項目が表示され、小項目を選択すると小項目の内容だけが表示されます。

<img width="958" alt="glossary1" src="https://github.com/user-attachments/assets/275b8001-ca70-43dd-8249-3bd3cc5d0c59">
<img width="965" alt="glossary2" src="https://github.com/user-attachments/assets/a2bf7dd7-d30e-4600-b422-32eb03536bf3">

# その他
デプロイするにあたりサーバーサイド処理がgithubでは困難とわかり、Renderに。
G検定ということでpythonの勉強もしたかったため、バックエンドはpythonのflaskを使用。
当初データベース運用にsqlite3を使用していたが、Renderに移す際にPostgreSQLに移行するためにSQLAlchemyに書き直しました。

# 使用技術
- python 3.10.6
- Flask 3.0.3
- SQLAlchemy 2.0.36
- JavaScript

# 連絡先
migsfactory[アット]gmail.com

&copy; 2024 Mig's Factory
