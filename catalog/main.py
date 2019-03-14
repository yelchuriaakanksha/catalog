from flask import Flask, render_template, url_for
from flask import request, redirect, flash, make_response, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Database_Set import Base, Shopping, BrandName, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
import datetime

engine = create_engine('sqlite:///shopping.db',
                       connect_args={'check_same_thread': False}, echo=True)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']
APPLICATION_NAME = "Store"

DBSession = sessionmaker(bind=engine)
session = DBSession()
# Creation of state token
mve_dg = session.query(Shopping).all()


# login
@app.route('/login')
def showLogin():

    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    mve_dg = session.query(Shopping).all()
    mvbe = session.query(BrandName).all()
    return render_template('login.html',
                           STATE=state, mve_dg=mve_dg, mvbe=mvbe)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validation of state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Authorization code
    code = request.data

    try:
        # Upgrade the authorization code
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check the validity of access token.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If error occurs in access token info, terminate.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verification of validity for access for this app.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user already connected.'),
                                 200)
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

    # check for  user existance, if it doesn't exist make a new one.
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
    output += ' " style = "width: 300px; height: 300px; border-radius: 150px;'
    '-webkit-border-radius: 150px; -moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output


def createUser(login_session):
        # Creating an User
    User1 = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(User1)
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
    except Exception as error:
        print(error)
        return None


@app.route('/')
@app.route('/home')
def home():
    mve_dg = session.query(Shopping).all()
    return render_template('myhome.html', mve_dg=mve_dg)


@app.route('/Store')
def Store():
    try:
        if login_session['username']:
            name = login_session['username']
            mve_dg = session.query(Shopping).all()
            mve = session.query(Shopping).all()
            mvbe = session.query(BrandName).all()
            return render_template('myhome.html', mve_dg=mve_dg,
                                   mve=mve, mvbe=mvbe, uname=name)
    except:
        return redirect(url_for('showLogin'))


@app.route('/Store/<int:mvid>/AllCompanys')
def shopBrand(mvid):
    mve_dg = session.query(Shopping).all()
    mve = session.query(Shopping).filter_by(id=mvid).one()
    mvbe = session.query(BrandName).filter_by(shoppingid=mvid).all()
    try:
        if login_session['username']:
            return render_template('ShopBrand.html', mve_dg=mve_dg,
                                   mve=mve, mvbe=mvbe,
                                   uname=login_session['username'])
    except:
        return render_template('ShopBrand.html',
                               mve_dg=mve_dg, mve=mve, mvbe=mvbe)


@app.route('/Store/addShopCategory', methods=['POST', 'GET'])
# Adding a new Shop Category to the Shopping list.
def addShopCategory():
    if request.method == 'POST':
        company = Shopping(name=request.form['name'],
                           user_id=login_session['user_id'])
        session.add(company)
        session.commit()
        return redirect(url_for('Store'))
    else:
        return render_template('addShopCategory.html', mve_dg=mve_dg)


@app.route('/Store/<int:mvid>/edit', methods=['POST', 'GET'])
# Edit the name of Shopping Category.
def editShopCategory(mvid):
    editShop = session.query(Shopping).filter_by(id=mvid).one()
    creator = getUserInfo(editShop.user_id)
    user = getUserInfo(login_session['user_id'])
    # If (logged in user != item owner) redirect them
    if creator.id != login_session['user_id']:
        flash("You cannot edit this Shopping Category."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('Store'))
    if request.method == "POST":
        if request.form['name']:
            editShop.name = request.form['name']
        session.add(editShop)
        session.commit()
        flash("Shopping Category Edited Successfully")
        return redirect(url_for('Store'))
    else:
        # mve_dg is global variable.
        # we can use them in entire application.
        return render_template('editShopCategory.html',
                               mv=editShop, mve_dg=mve_dg)


@app.route('/Store/<int:mvid>/delete', methods=['POST', 'GET'])
def deleteShopCategory(mvid):
    mv = session.query(Shopping).filter_by(id=mvid).one()
    creator = getUserInfo(mv.user_id)
    user = getUserInfo(login_session['user_id'])
    # If (logged in user != item owner) redirect them
    if creator.id != login_session['user_id']:
        flash("You cannot Delete this Shop Category."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('Store'))
    if request.method == "POST":
        session.delete(mv)
        session.commit()
        flash("Shopping Category Deleted Successfully")
        return redirect(url_for('Store'))
    else:
        return render_template('deleteShopCategory.html', mv=mv, mve_dg=mve_dg)


@app.route('/Store/addCompany/addShopDetails/<string:mvname>/add',
           methods=['GET', 'POST'])
def addShopDetails(mvname):
    mve = session.query(Shopping).filter_by(name=mvname).one()
    # Check if the loggedin user is not the owner of shop
    creator = getUserInfo(mve.user_id)
    user = getUserInfo(login_session['user_id'])
    # If (loggedin user != item owner) redirect them
    if creator.id != login_session['user_id']:
        flash("You can't add new book edition"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('shopBrand', mvid=mve.id))
    if request.method == 'POST':
        name = request.form['name']
        year = request.form['year']
        color = request.form['color']
        brand = request.form['brand']
        price = request.form['price']
        shoppingdetails = BrandName(name=name,
                                    year=year, 
                                    color=color,
                                    brand=brand,
                                    price=price,
                                    shoppingid=mve.id,
                                    user_id=login_session['user_id'])
        session.add(shoppingdetails)
        session.commit()
        return redirect(url_for('shopBrand', mvid=mve.id))
    else:
        return render_template('addShopDetails.html',
                               mvname=mve.name, mve_dg=mve_dg)


@app.route('/Store/<int:mvid>/<string:mvbname>/edit',
           methods=['GET', 'POST'])
# Edit the items of particular Shopping Category.
def editingShop(mvid, mvbname):
    mv = session.query(Shopping).filter_by(id=mvid).one()
    shoppingdetails = session.query(BrandName).filter_by(name=mvbname).one()
    # Check if the loggedin user is not the owner of shop
    creator = getUserInfo(mv.user_id)
    user = getUserInfo(login_session['user_id'])
    # If (loggedin user != item owner) redirect them
    if creator.id != login_session['user_id']:
        flash("You can't edit this book edition"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('shopBrand', mvid=mv.id))
    # POST methods
    if request.method == 'POST':
        shoppingdetails.name = request.form['name']
        shoppingdetails.year = request.form['year']
        shoppingdetails.color = request.form['color']
        shoppingdetails.brand = request.form['brand']
        shoppingdetails.price = request.form['price']
        session.add(shoppingdetails)
        session.commit()
        flash("Shopping Edited Successfully")
        return redirect(url_for('shopBrand', mvid=mvid))
    else:
        return render_template('editingShop.html',
                               mvid=mvid, shoppingdetails=shoppingdetails,
                               mve_dg=mve_dg)


@app.route('/Store/<int:mvid>/<string:mvbname>/delete',
           methods=['GET', 'POST'])
# Deleting particular item in Shopping Category.
def deleteShop(mvid, mvbname):
    mv = session.query(Shopping).filter_by(id=mvid).one()
    shoppingdetails = session.query(BrandName).filter_by(name=mvbname).one()
    # Checking if the logged in user is not the owner of shop
    creator = getUserInfo(mv.user_id)
    user = getUserInfo(login_session['user_id'])
    # If (loggedin user != item owner) redirect them
    if creator.id != login_session['user_id']:
        flash("You can't delete this item"
              "This is belongs to %s" % owner.name)
        return redirect(url_for('shopBrand', mvid=mv.id))
    if request.method == "POST":
        session.delete(shoppingdetails)
        session.commit()
        flash("Deleted shop Successfully")
        return redirect(url_for('shopBrand', mvid=mvid))
    else:
        return render_template('deleteShop.html',
                               mvid=mvid, shoppingdetails=shoppingdetails,
                               mve_dg=mve_dg)


@app.route('/logout')
# logout or disconnect.
def logout():
    access_token = login_session['access_token']
    print ('In gdisconnect access token is %s', access_token)
    print ('User name is: ')
    print (login_session['username'])
    if access_token is None:
        print ('Access Token is None')
        response = make_response(
            json.dumps('Current user not connected....'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = login_session['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(uri=url, method='POST', body=None, 
                       headers={'content-type': 
                                'application/x-www-form-urlencoded'})[0]

    print (result['status'])
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps(
                                'Successfully disconnected user..'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Successful logged out")
        return redirect(url_for('home'))
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/Store/JSON')
# JSON end points.
def allShopsJSON():
    shopcategories = session.query(Shopping).all()
    category_dict = [c.serialize for c in shopcategories]
    for c in range(len(category_dict)):
        shops = [i.serialize for i in session.query(
                 BrandName).filter_by(shoppingid=category_dict[c]["id"]).all()]
        if shops:
            category_dict[c]["shop"] = shops
    return jsonify(Shopping=category_dict)


@app.route('/Store/shopCategories/JSON')
def categoriesJSON():
    shops = session.query(Shopping).all()
    return jsonify(shopCategories=[c.serialize for c in shops])


@app.route('/Store/shops/JSON')
def itemsJSON():
    items = session.query(BrandName).all()
    return jsonify(shops=[i.serialize for i in items])


@app.route('/Store/<path:shop_name>/shops/JSON')
def categoryItemsJSON(shop_name):
    shopCategory = session.query(Shopping).filter_by(name=shop_name).one()
    shops = session.query(BrandName).filter_by(shopping=shopCategory).all()
    return jsonify(shopEdtion=[i.serialize for i in shops])


@app.route('/Store/<path:shop_name>/<path:edition_name>/JSON')
def ItemJSON(shop_name, edition_name):
    shopCategory = session.query(Shopping).filter_by(name=shop_name).one()
    shopEdition = session.query(BrandName).filter_by(
           name=edition_name, shopping=shopCategory).one()
    return jsonify(shopEdition=[shopEdition.serialize])

if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='127.0.0.1', port=8000)
