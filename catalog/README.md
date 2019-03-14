# Item Catalog
By Yelchuri Aakanksha

## Installation
* Vagrant
* Udacity Vagrantfile
* VirtualBox

### Steps to run this project
Download and install Vagrant.

Download and install VirtualBox.

Open terminal, and type:
- This command is used to initilize `vagrant init ubuntu/xenial64`

- To connect virtual machine: `vagrant up`
This will cause Vagrant to download the Ubuntu operating system and install it. This may take quite a while depending on how fast your Internet connection is.

After the above command succeeds, connect to the newly created VM by typing the following command:

- To login virtual machine: `vagrant ssh`
- Exit one directory by using commannd: `cd ..`
- Exit again one directory:`cd ..`
- Start catalog site: `cd vagrant` to navigate to the shared repository.

Download or clone this repository, and navigate to it.

### Install the following in command prompt

- sudo python3 -m pip install --upgrade flask
- pip install flask
- pip install sqlalchemy
- pip install requests
- pip install oauth2clients
### Run the following command to set up the database:

python3 database_set.py
Run the following command to insert dummy values. If you don't run this, the application will not run.

python3 Data_start.py
Run this application:

python3 main.py
Open http://localhost:8000/ in any Web browser.

### Usage
The item catalog provides a human-usable website as well as JSON endpoints for parsing.
To access the website, simply go to `localhost:8000`


### About
The Item Catalog project consists of developing an application that provides a list of items within a variety of categories, as well as provide a user registration and authentication system. This project uses persistent data storage to create a RESTful web application that allows users to perform Create, Read, Update, and Delete operations.

A user does not need to be logged in in order to read the categories or items uploaded. However, users who created an item are the only users allowed to edit or delete the item that they created.

This program uses third-party auth with Google. Some of the technologies used to build this application include Flask, OAuth2client, Sqlalchemy, and SQLite.

## In This Project
This project has one main Python module `main.py`. 
It runs the Flask application. 
A SQL database is created using the `Database_Set.py` module and you can populate the database with test data using `data_start.py`.
The Flask application uses stored HTML templates in the tempaltes folder to build the front-end of the application.

### Project Structure
```
.
├── Data_start.py
├── client_secrets.json
├── database_set.py
├── main.py
├── shopping.db
├── img
├── README.md
├── static
│   └── style.css
└── templates
    ├── addShopCategory.html
    ├── addShopDetails.html
    ├── admin_login.html
    ├── admin_loginFail.html
    ├── allShop.html
    ├── deleteShop.html
    ├── deleteShopCategory.html
    ├── editingShop.html
    ├── editShopCategory.html
    ├── login.html
    ├── mainpage.html
    ├── myhome.html
    ├──nav.html
    ├──ShopBrand.html
    ├──ShopTitles.html
```


## Skills used for this project
* Python
* HTML
* CSS
* Flask
* SQLAchemy
* OAuth
* Google Login

## Dependencies
- [Vagrant](https://www.vagrantup.com/)
- [Udacity Vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)


## Using Google Login
To get the Google login working there are a few additional steps:

1. Go to [Google Dev Console](https://console.developers.google.com)
2. Sign up or Login if prompted
3. Go to Credentials
4. Select Create Crendentials > OAuth Client ID
5. Select Web application
6. Enter name 'shopping zone'
7. Authorized JavaScript origins = 'http://localhost:8000'
8. Authorized redirect URIs = 'http://localhost:8000/login' && 'http://localhost:8000/gconnect'
9. Select Create
10. Copy the Client ID and paste it into the `data-clientid` in login.html and mainpage.html
11. On the Dev Console Select Download JSON
12. Rename JSON file to client_secrets.json
13. Place JSON file in Store directory that you cloned from here
14. Run application using `python /store/main.py`

## JSON Endpoints
The following are open to the public:

1) Shopping Zone JSON: `/Store/JSON`
    - Displays the Shopping Materials.Shopping Categories with designs.

2) Shop Categories JSON: `/Store/ShopCategories/JSON`
    - Displays all Shop Models
3) All Shop Editions: `'/Store/shops/JSON'`
	- Displays all Shop Models

4) Shopping Edition JSON: `/Store/<path:shop_name>/shops/JSON`
    - Displays Shopping models for a specific Shop zone

5) Shopping Category Edition JSON: `/Store/<path:shop_name>/<path:edition_name>/JSON`
    - Displays a specific Shopping category Model.
### Shopping Zone	
![open.png](https://github.com/yelchuriaakanksha/item/blob/master/img/open.png)

### Login
![loginn.png](https://github.com/yelchuriaakanksha/item/blob/master/img/loginn.png)

### Signin
![signin.png](https://github.com/yelchuriaakanksha/item/blob/master/img/signin.png)

![signin2.png](https://github.com/yelchuriaakanksha/item/blob/master/img/signin2.png)

![intro.png](https://github.com/yelchuriaakanksha/item/blob/master/img/into.png)

![category.png](https://github.com/yelchuriaakanksha/item/blob/master/img/category.png)

### Add New Shopping Category
![addcatg.png](https://github.com/yelchuriaakanksha/item/blob/master/img/addcatg.png)

### Delete Shopping Category
![delsports.png](https://github.com/yelchuriaakanksha/item/blob/master/img/delsports.png)

![deletion.png](https://github.com/yelchuriaakanksha/item/blob/master/img/deletion.png)

### Edit Shop Category
![editshopping.png](https://github.com/yelchuriaakanksha/item/blob/master/img/editshopping.png)

![edited.png](https://github.com/yelchuriaakanksha/item/blob/master/img/edited.png)

### Inserting Particular item
![shoppingdetails](https://github.com/yelchuriaakanksha/item/blob/master/img/shoppingdetails.png)

### Delete Particular Item
![deletecategory.png](https://github.com/yelchuriaakanksha/item/blob/master/img/deletecategory.png)

![delalert.png](https://github.com/yelchuriaakanksha/item/blob/master/img/delalert.png)

### Edit items
![editcatg.png](https://github.com/yelchuriaakanksha/item/blob/master/img/editcatg.png)

![editshop.png](https://github.com/yelchuriaakanksha/item/blob/master/img/editshop.png)

### Logout
![logout.png](https://github.com/yelchuriaakanksha/item/blob/master/img/logout.png)
