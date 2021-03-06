# Project - Book list ð

#### About 
---

As a final project deliverable for CS50x, I created a full-stack app to manage the book lists for the book club I belong to.
CS50x ã®æçµèª²é¡ã¨ãã¦ãæå±ããããã¯ã¯ã©ãã§æ¬ã®ãªã¹ããç®¡çããããã«ãã«ã¹ã¿ãã¯ã®ã¢ããªãä½æãã¾ããã

I did this project from 2021/10/17 to 2021/11/7. 
ä½ææéã¯ 2021/ 10/17 ãã 2021/11/7 ã§ãã

#### Video Demo: https://youtu.be/LKHt2ZldNg0

[![altè¨­å®](https://i.ibb.co/NNBtrtR/books-quote1.jpg)](https://www.youtube.com/watch?v=LKHt2ZldNg0)

#### Tech
---

- Python 3.10.10
- pipenv, Flask
- Firebase for Firestore and Authentication.
- Heroku

#### Structure
---

MCV model 
- M,  Data is stored in Firestore - Firebase
- C,  Python and Flask manage data between the database and the view
- V,  jinjya provide templates for the view

app.py contains main functions to contlolle model and view. It also initialized Firebase_admin to use Firestore and autentication. 
helpers.py contains functions which be used in app.py. I sepalated functions to make them readable. 
Pipfile and Pipfile.lock stores information about dependencies of my projects. 
Prockfile, requrements.txt and runtime.txt contains information to deploy my project to Heroku. <br>

MCV model 
- M, ãã¼ã¿ã¯Firestore - Firebaseã«ä¿å­ããã¦ãã¾ã
- C, Pythonã¨Flaskããã¼ã¿ãã¼ã¹ã¨ãã¥ã¼ã®éã®ãã¼ã¿ãç®¡çãã¾ã
- V, jinjyaã¯ãã¥ã¼ã®ããã®ãã³ãã¬ã¼ããæä¾ãã¾ã

app.pyã«ã¯ãã¢ãã«ã¨ãã¥ã¼ãæ¥ç¶ããããã®ä¸»è¦ãªé¢æ°ãå«ã¾ãã¦ãã¾ããã¾ããFirebase_adminãåæåããFirestoreã¨Autenticationãä½¿ç¨ãã¦ãã¾ãã
helpers.py ã¯ app.py ã§ä½¿ç¨ãããé¢æ°ãå«ãã§ãã¾ããèª­ã¿ãããããã«é¢æ°ãåãã¦ãã¾ãã
Pipfileã¨Pipfile.lockã¯ãç§ã®ãã­ã¸ã§ã¯ãã®ä¾å­é¢ä¿ã«ã¤ãã¦ã®æå ±ãæ ¼ç´ãã¦ãã¾ãã
Prockfile, requrements.txt, runtime.txtã«ã¯ãHerokuã«ãã­ã¸ã§ã¯ããããã­ã¤ããããã®æå ±ãæ ¼ç´ããã¦ãã¾ãã

#### Development
---

```

#### 1. ã¢ããªèµ·å

Pythonä»®æ³ç°å¢ãèµ·å
pipenv shell

ä»®æ³ç°å¢åã«ã¦Flaskãµã¼ãã¼èµ·å
flask run

#### 2. ã¢ããªéçº

1) éçºä¸è¬
ä»®æ³ç°å¢åã«ã¦ã©ã¤ãã©ãªã®ã¤ã³ã¹ãã¼ã«
pipenv install [ã©ã¤ãã©ãªå]

ãã¼ã¸ã§ã³ç®¡çã¯ git ã³ãã³ãã§è¡ã
éçºã¯ developãã©ã³ã, 
æ¬çªã¯ mainãã©ã³ãã§ç®¡çãã

ãããã°ã¯ VSCodeã®ãããã°ç»é¢ãéã
ä»»æã®å ´æã«ãã¬ã¼ã¯ãã¤ã³ããå¼µã
ãããã°å®è¡ãã¿ã³ãæ¼ä¸ããã
ãã®éã«ã¯
ä»®æ³ç°å¢ãéãã¦ãããã¨,
ãããã°ããããã©ã«ãããã©ã¼ã«ã¹ãããã¨ã
ãããã°çµäºæã³ãã³ãã¯  
deactivate

2) ããã­ã¤
ãã­ã¯ã«ã­ã°ã¤ã³ãã
heroku login

ããã­ã¤
git checkout main // ã­ã¼ã«ã«ã®ã¡ã¤ã³ã«ç§»å
git pull main // ãªã¢ã¼ãã®ã¡ã¤ã³ããææ°ã®ã³ã¼ããåå¾ãã
git push heroku main //ãã­ã¯ã«ããã­ã¤ãã

ããã­ã¤ãããã¼ã¸ãéã
heroku open

#### 3. ã¢ããªåæ­¢

Flaskãµã¼ãã¼ã®èµ·ååæ­¢
ctrl + C

Pythonä»®æ³ç°å¢ãèµ·ååæ­¢
pipenv exit

```

#### Description: 
---

The first challenge was that creating an environment for creating a product. Since I'd like to minimize my project, I needed to set up for my VSCode to debug.<br>
The second challenge was that finding the reason why libraries I installed was not found by terminal. I found that it was because different Python was used in VSCode and terminal if I installed several different version of Python.<br>
The third challenge was that finding the way to implement creck event in Python.   Since I thought it's important for a better user experience, I spent a time to research how to implement a button to vote a book. Then I decided to use jQuery and ajax.<br>
To solve those issues, I read error logs and researched with that words. Through this experience, I got confidence reading error messages.<br>

æåã®èª²é¡ã¯ãè£½åãä½ãããã®ç°å¢ä½ãã§ããããã­ã¸ã§ã¯ããæå°åãããã®ã§ãVSCodeã§ãããã°ããããã®ç°å¢ãæ´ããå¿è¦ãããã¾ããã<br>
2ã¤ç®ã®èª²é¡ã¯ãã¤ã³ã¹ãã¼ã«ããã©ã¤ãã©ãªãã¿ã¼ããã«ã§è¦ã¤ãããªãåå ãæ¢ããã¨ã§ãããããã¤ãã®ç°ãªããã¼ã¸ã§ã³ã®Pythonãã¤ã³ã¹ãã¼ã«ããå ´åãVSCodeã¨ã¿ã¼ããã«ã§ç°ãªãPythonãä½¿ããã¦ãããã¨ãåå ã ã¨ãããã¾ããã<br>
3ã¤ç®ã®èª²é¡ã¯ãPythonã§clickã¤ãã³ããå®è£ããæ¹æ³ãè¦ã¤ãããã¨ã§ãããããè¯ãã¦ã¼ã¶ã¼ä½é¨ã®ããã«éè¦ã ã¨æã£ãã®ã§ãæ¬ã«æç¥¨ããããã®ãã¿ã³ãå®è£ããæ¹æ³ã®ç ç©¶ã«æéãè²»ããã¾ãããããã¦ãjQueryã¨ajaxãä½¿ããã¨ã«ãã¾ããã<br>
ãã®ãããªåé¡ãè§£æ±ºããããã«ãç§ã¯ã¨ã©ã¼ã­ã°ãèª­ã¿ããã®è¨èãä½¿ã£ã¦ç ç©¶ãã¾ããããã®ãããªçµé¨ãéãã¦ãã¨ã©ã¼ã¡ãã»ã¼ã¸ãèª­ããã¨ã«èªä¿¡ãæã¤ãã¨ãã§ãã¾ããã<br>ã

#### Futre features
---

- Users can leave comments for each book
- Users can create own icon with uploading picture
- Uploading book image
