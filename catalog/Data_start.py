from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from Database_Set import *

engine = create_engine('sqlite:///shopping.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Delete Shopping if exisitng.
session.query(Shopping).delete()
# Delete BrandName if exisitng.
session.query(BrandName).delete()
# Delete User if exisitng.
session.query(User).delete()

# Create sample users data
User1 = User(name="yelchuri Aakanksha",
             email="aakanksha.yelchuri@gmail.com",
             picture='http://www.enchanting-costarica.com/wp-content/'
                     'uploads/2018/02/jcarvaja17-min.jpg')
session.add(User1)
session.commit()
print ("Successfully Add First User")
# Create sample brand companys
Company1 = Shopping(name="Women's Fashion",
                    user_id=1)
session.add(Company1)
session.commit()

Company2 = Shopping(name="Men's Fashion",
                    user_id=1)
session.add(Company2)
session.commit

Company3 = Shopping(name="Accessories", user_id=1)
session.add(Company3)
session.commit()

Company4 = Shopping(name="Car,Motorbikes", user_id=1)
session.add(Company4)
session.commit()

Company5 = Shopping(name="Toys and Baby World", user_id=1)
session.add(Company5)
session.commit()

Company6 = Shopping(name="Electronic Gatgets", user_id=1)
session.add(Company6)
session.commit()

# Populare a shops with models for testing
# Using different users for shops names year also
Name1 = BrandName(name="Women's Dress",
                       year="2019",
                       color="black",
                       brand="AQUA",
                       price="750",
                       shoppingid=1,
                       user_id=1)
session.add(Name1)
session.commit()

Name2 = BrandName(name="Men's Dress",
                       year="2019",
                       color="blue",
                       brand="Denim",
                       price="1500",
                       shoppingid=2,
                       user_id=1)
session.add(Name2)
session.commit()

Name3 = BrandName(name="Hand Bags",
                       year="2018",
                       color="All colors",
                       brand="Guess",
                       price="5,000",
                       shoppingid=3,
                       user_id=1)
session.add(Name3)
session.commit()

Name4 = BrandName(name="Scooty",
                       year="2017",
                       color="purple",
                       brand="Activa 5G",
                       price="55,950",
                       shoppingid=4,
                       user_id=1)
session.add(Name4)
session.commit()

Name5 = BrandName(name="Toys",
                       year="2014",
                       color="orange",
                       brand="Disney",
                       price="600",
                       shoppingid=5,
                       user_id=1)
session.add(Name5)
session.commit()

Name6 = BrandName(name="Mobiles",
                       year="2019",
                       color="Black",
                       brand="Samsung",
                       price="13,000",
                       shoppingid=6,
                       user_id=1)
session.add(Name6)
session.commit()

print("Your Shopping database has been inserted successfully!")

