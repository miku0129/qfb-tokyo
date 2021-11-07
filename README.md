  # Project - Book list 📚
  
  #### Video Demo: https://youtu.be/LKHt2ZldNg0
  
  [![alt設定](http://img.youtube.com/vi/LKHt2ZldNg0/0.jpg)](https://www.youtube.com/watch?v=LKHt2ZldNg0)
  
  ### About
 
  I created a full-stack app to manage the book lists for the book club I belong to.
  This is the final project deliverable for CS50x.<br>
  所属するブッククラブで本のリストを管理するためにフルスタックのアプリを作成しました。
  CS50xの最終課題成果物です。
  
  From 2021/10/17 to 2021/11/7, Four weeks
  
  ### Tech 
  
  Python 3.10.10, pipenv, Flask , firebase for Firestore database and Authentication. 
  
  ### Structure 
  
  M: Data is stored in Fire store - Firebase<br> 
  C: Python and Flask manage data between the database and the view<br>
  V: jinjya provide templates for the view<br>
  
  ### Development
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
  
  ### Futre features
  
  * Users can leave comments for each book
  * Users can create own icon with uploading picture
  * Uploading book image
  
  
  
  
 
  
  

  
