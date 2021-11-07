  ### アプリについて
  所属するブッククラブで本のリストを管理できるアプリです。
  毎回本を選出するのにリストを作る手間を省きたくフルスタックアプリを作成しました。<br>
  CS50xの最終課題成果物です。
  製作期間 2021/10/17 ~ 2021/11/7 約4週間
  
  ### Tech 
  
  Python 3.10.10
  
  pipenv 
  
  Flask 
  
  firebase for Firestore database, Authentication
  
  ### 開発
  ```
  
  #### 1. アプリ起動
  
  Python仮想環境を起動
  pipenv shell
  
  仮想環境内にてFlaskサーバー起動
  flask run 
  
  #### 2. アプリ開発
  
  1) 開発一般
  仮想環境内にてライブラリのインストール
  pipenv install [ライブラリ名]
  
  バージョン管理は git コマンドで行う
  
  2) デプロイ
  ヘロクにログインする
  heroku login
  
  デプロイ
  git push heroku main
  
  デプロイしたページを開く
  heroku open
  
  #### 3. アプリ停止
  
  Flaskサーバーの起動停止
  ctrl + C 
  
  Python仮想環境を起動停止
  pipenv exit 
  
  
  ```
  
  
  
 
  
  

  
