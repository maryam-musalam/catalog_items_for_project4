# !/usr/bin/env python
import os
from sqlalchemy import func
from flask import Flask, render_template, request
from flask import redirect, url_for, flash, jsonify
from werkzeug import secure_filename
from flask import send_from_directory
from sqlalchemy.orm.exc import NoResultFound

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from db import Base, Categories, ElectronicItems, User

from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

engine = create_engine('sqlite:///electronic.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#UPLOAD_FOLDER = 'static'
# allowed formate for the image upload
#ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Electronic App"


app = Flask(__name__)
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(
                                 json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
                                 json.dumps('Failed to upgrade the\
                                            authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = (
           'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token
           )
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the
    # access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used
    # for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't\
                                            match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client ID \
                                           does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current \
                                            user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists. if it dosen't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;\
                -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
            'email'], image=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except NoResultFound:
        return None


# log out user
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current \
                                            user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    log = login_session['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % log
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        flash("you are logged out")
        return redirect(url_for('electronics'))
    else:
        response = make_response(json.dumps('Failed to revoke \
                                            token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Making an API Endpoint (GET Request)

# json for one item in one category
@app.route('/catalog/<path:cat_name>/<path:item_name>/json')
def oneitemjson(cat_name, item_name):
    category = session.query(Categories).filter_by(name=cat_name).one()
    item = session.query(ElectronicItems).filter_by(name=item_name,
                                                    id=category.id).one()
    return jsonify(item=[item.serialize])


# json all items in all categories
@app.route('/catalog/json')
def electronicsMenuJSON():
    categories = session.query(Categories).all()
    category = [i.serialize for i in categories]
    for i in range(len(category)):
        a = session.query(ElectronicItems).\
                 filter_by(category_id=category[i]["id"]).all()
        items = [item.serialize for item in a]
        if items:
            category[i]["Item"] = items
    return jsonify(Category=category)


@app.route('/')
@app.route('/Electronics')
def electronics():
    # show categories with last item in each category
    last_item = session.query(func.max(ElectronicItems.id))\
                .group_by(ElectronicItems.category_id).subquery()
    electronic = session.query(Categories, ElectronicItems).\
        outerjoin(ElectronicItems,
                  Categories.id == ElectronicItems.category_id)\
        .filter(ElectronicItems.id.in_(last_item)).all()
    if 'username' not in login_session:
        return render_template('electronic.html',
                               electronic=electronic)
    else:
        return render_template('electronicwithlogged.html',
                               electronic=electronic)


@app.route('/Electronics/<int:category_id>/menu')
def viewItems(category_id):
    # show all items based on category id
    cateogry = session.query(Categories).filter_by(id=category_id).one()
    creator = getUserInfo(cateogry.user_id)
    items = session.query(ElectronicItems).\
        filter_by(category_id=cateogry.id).all()
    if 'username' not in login_session:
        return render_template('menuitem.html',
                               items=items,
                               creator=creator)
    else:
        return render_template('menuitemwithuserloggedin.html',
                               items=items,
                               creator=creator)


@app.route('/Electronics/<int:category_id>/menu/<int:item_id>/')
def viewItemsInfo(category_id, item_id):
    # show info about item
    items = session.query(ElectronicItems)\
                   .filter_by(id=item_id).one()
    creator = getUserInfo(items.user_id)
    if ('username' not in login_session or
            creator.id != login_session['user_id']):
        return render_template('item_info.html',
                               items=items)
    else:
        return render_template('item_info_with_user.html',
                               items=items,
                               creator=creator)


# this will take us to add form
@app.route('/Electronics/new')
def addItem():
    return render_template('addItem.html')


# submit add form function
@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if 'username' not in login_session:
        flash("You are not allowed to access there")
        return redirect('/login')
    if request.method == 'POST':
        if request.form['name'] == '':
            flash("Name cant be empty")
            return redirect(request.url)
        if request.form['price'] == '':
            flash("price cant be empty")
            return redirect(request.url)
        if request.form['description'] == '':
            flash("description cant be empty")
            return redirect(request.url)
        if request.form['catagory'] == '':
            flash("you need to select category name")
            return redirect(request.url)
        newItem = ElectronicItems(name=request.form['name'],
                                  description=request.form['description'],
                                  price=request.form['price'],
                                  category_id=request.form['catagory'],
                                  user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash("new item has been added")
        return redirect(url_for('electronics'))
    else:
        return redirect(url_for('addItem'))


# edit item if the user is the owner
@app.route('/Electronics/<int:category_id>/<int:item_id>/edit',
           methods=['GET', 'POST'])
def editItem(category_id, item_id):
    editItem = session.query(ElectronicItems).filter_by(id=item_id).one()
    creator = getUserInfo(editItem.user_id)
    catagory = session.query(Categories).filter_by(
           id=editItem.category_id).one()
    if ('username' not in login_session or
            creator.id != login_session['user_id']):
        flash("You are not allowed to access there")
        return redirect('/login')
    if request.method == 'POST':
        if request.form['name']:
            editItem.name = request.form['name']
        if request.form['price']:
            editItem.price = request.form['price']
        if request.form['description']:
            editItem.description = request.form['description']

        session.add(editItem)
        session.commit()
        flash("item has been edit")
        return redirect(url_for('electronics'))
    else:
        return render_template('editmenu.html',
                               category_id=category_id,
                               item_id=item_id, i=editItem, catagory=catagory)


# delete item if user is the owner
@app.route('/Electronics/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(item_id):
    deleteItem = session.query(ElectronicItems).filter_by(id=item_id).one()
    creator = getUserInfo(deleteItem.user_id)
    if ('username' not in login_session or
            creator.id != login_session['user_id']):
        flash("You are not allowed to access there")
        return redirect('/login')
    if deleteItem.user_id != login_session['user_id']:
        return "<script> function myfunction()\
        { alert('you are not authorized to delete this\
        resturant. please create your own resturant \
        in order to delete.'); }</script>\
        <body onload='myfunction()'></body>"
    if request.method == 'POST':
        session.delete(deleteItem)
        flash("item has been deleted successfly")
        session.commit()
        return redirect(url_for('electronics'))
    else:
        return render_template('deleteitem.html', items=deleteItem)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
