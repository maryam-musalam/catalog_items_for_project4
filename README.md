# Project : Item Catalog 

This project is the second project in full stack web development nano-degree by udacity. 

## What the project is all about ? 

In this project we asked to build an application that allows user to register in a website and be able to post, edit and delete their own items. The website will provides a list of items within a variety of categories as well as it provide user registration and authentication system. 

## site scenario  : 

1-  when the user visit the site whiteout registering , her/she will be able to see all the categories of our site and by pressing the category name it will take them to the items page according to that category to brows them. As well as if the user click on specific item he/she will go see more info about that specific item. 

2- when the user login the site, he/she will be able to edit the items info or delete them. As well as adding new items in the provided categories with alerting messages showing the case of that action, plus the ability of logging out.


## what we used in this project :

1- Flask framework to built our site, more info : http://flask.pocoo.org <br>
2- fontawesome for icons : https://fontawesome.com <br>
3- bootstrap for styling , more info : https://getbootstrap.com/docs/4.1/getting-started/introduction/ <br>
4- sqlalchemy for the database : https://www.sqlalchemy.org <br>
5- for registration system  we used google OAuth2 . Learn more :https://developers.google.com/api-client-library/python/guide/aaa_oauth


‘’
Using Google Login
To get the Google login working there are a few additional steps:
1. Go to Google Dev Console
2. Sign up or Login if prompted
3. Go to Credentials
4. Select Create Crendentials > OAuth Client ID
5. Select Web application
6. Enter name ‘Electronic App’
7. Authorized JavaScript origins = 'http://localhost:8000’
8. Authorized redirect URIs = 'http://localhost:8000/login'  && 'http://localhost:8000/gconnect'
9. Select Create
10. Copy the Client ID and paste it into the data-clientid in login.html
11. On the Dev Console Select Download JSON
12. Rename JSON file to client_secrets.json
13. Place JSON file in catalog directory that you cloned from here
‘’

## What you need as pre-requiremnet to run this project?

1- Install the VirtualMachine from this link : https://www.virtualbox.org/wiki/Downloads.<br>
2- Install the  Vagrant from this link :  https://www.vagrantup.com/downloads.html.<br>
3- Download  a  FSND virtual machine  which contains vagrant setup files that configure the virtual machine and all other needed files from this link :  https://github.com/udacity/fullstack-nanodegree-vmand .<br>

After you done with all the above installations, in the terminal go to your directory where you download the  FSND virtual machine ( for example for me it's in project directory) and do the following: 
```
cd project/FSND-Virtual-Machin
cd vagrant
vagrant up 
vagrant shh
cd /vagrant 
mkdir catalog
cd catalog
```
 And then install all the files from this repo into catalog folder

Then run the database file like this 
```
python db.py
```
Then fill the database by running the electronicCategories.py file 
```
python electronicCategories.py
```

Then finally run the project app 
```
python project.py
```

And from google run to locally  :

http://localhost:8000/Electronics



## JSON endpoint 

In this project we have 2 json endpoints  , one to show all the categories along with their items and one showing specific item specified by category name and item name like showing below :
```
http://localhost:8000/catalog/json

http://localhost:8000/catalog/<path:cat_name>/<path:item_name>/json
Ex:
http://localhost:8000/catalog/Phones/iphone 5/json
```