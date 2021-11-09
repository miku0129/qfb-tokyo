# Project - Book list 📚

### About 
---

I created a full-stack app to manage the book lists for the book club I belong to.
This is the final project deliverable for CS50x.<br>
所属するブッククラブで本のリストを管理するためにフルスタックのアプリを作成しました。CS50x の最終課題です。

From 2021/10/17 to 2021/11/7, Four weeks

### Video Demo
---

https://youtu.be/LKHt2ZldNg0

[![alt設定](http://img.youtube.com/vi/LKHt2ZldNg0/0.jpg)](https://www.youtube.com/watch?v=LKHt2ZldNg0)

### Tech
---

- Python 3.10.10
- pipenv, Flask
- Firebase for Firestore and Authentication.
- Heroku

### Structure
---

M: Data is stored in Firestore - Firebase<br>
C: Python and Flask manage data between the database and the view<br>
V: jinjya provide templates for the view<br>

### Development
---

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

### Challenges
---

The first challenge was that creating an environment for creating a product. Since I'd like to minimize my project, I needed to set up for my VSCode to debug.<br>
The second challenge was that finding the reason why libraries I installed was not found by terminal. I found that it was because different Python was used in VSCode and terminal if I installed several different version of Python.<br>
The third challenge was that finding the way to implement creck event in Python.   Since I thought it's important for a better user experience, I spent a time to research how to implement a button to vote a book. Then I decided to use jQuery and ajax.<br>
To solve those issues, I read error logs and researched with that words. Through this experience, I got confidence reading error messages.<br>

最初の課題は、製品を作るための環境作りでした。プロジェクトを最小化したいので、VSCodeでデバッグするための環境を整える必要がありました。<br>
2つ目の課題は、インストールしたライブラリがターミナルで見つからない原因を探ることでした。いくつかの異なるバージョンのPythonをインストールした場合、VSCodeとターミナルで異なるPythonが使われていることが原因だとわかりました。<br>
3つ目の課題は、Pythonでcreckイベントを実装する方法を見つけることでした。より良いユーザー体験のために重要だと思ったので、本に投票するためのボタンを実装する方法の研究に時間を費やしました。そして、jQueryとajaxを使うことにしました。<br>
このような問題を解決するために、私はエラーログを読み、その言葉を使って研究しました。このような経験を通して、エラーメッセージを読むことに自信を持つことができました。<br>。

### Futre features
---

- Users can leave comments for each book
- Users can create own icon with uploading picture
- Uploading book image
