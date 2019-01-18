# sqlalcmey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base, Categories, ElectronicItems, User

engine = create_engine(
                       'sqlite:///electronic.db?check_same_thread=False'
                       )

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create dummy user
User1 = User(name="Mariam Musalam",
             email="maryam-musalam@hotmail.com",
             image='avatar.png')
session.add(User1)
session.commit()

# Menu for UrbanBurger
category1 = Categories(user_id=1,
                       name="Phones",
                       image="phones.jpg")

session.add(category1)
session.commit()

electronic_items1 = ElectronicItems(user_id=1,
                                    name="iphone 5",
                                    description="Capacity - 32 GB ",
                                    price="SR 999",
                                    categories=category1)

session.add(electronic_items1)
session.commit()


electronic_items2 = ElectronicItems(user_id=1,
                                    name="iphone 6",
                                    description="Highlights :Metal body",
                                    price="SAR 1139",
                                    categories=category1)

session.add(electronic_items2)
session.commit()


electronic_items3 = ElectronicItems(user_id=1,
                                    name="iphone 8",
                                    description="iPhone 8 Plus introduces",
                                    price="SAR 3699",
                                    categories=category1)

session.add(electronic_items3)
session.commit()


category2 = Categories(user_id=1,
                       name="Laptops",
                       image="laptops.jpg")

session.add(category2)
session.commit()

electronic_items1 = ElectronicItems(
                                    user_id=1,
                                    name="MacBook Air 13.3-inch",
                                    description="Thin, light, powerful",
                                    price="SAR 4898",
                                    categories=category2
                                    )

session.add(electronic_items1)
session.commit()


electronic_items2 = ElectronicItems(
                                    user_id=1,
                                    name="Acer - EXTENSE 15 EX2519 -C4U0",
                                    description="Smoothly and quickly",
                                    price="SAR 859",
                                    categories=category2
                                    )

session.add(electronic_items2)
session.commit()


electronic_items3 = ElectronicItems(
                                    user_id=1,
                                    name="iLife -IL.1406G.232WAS",
                                    description="Intel Atom processor",
                                    price="SAR 523",
                                    categories=category2
                                    )

session.add(electronic_items3)
session.commit()


category3 = Categories(user_id=1,
                       name="Tablets",
                       image="lapyop.jpg")

session.add(category3)
session.commit()


electronic_items1 = ElectronicItems(
                                    user_id=1,
                                    name="Yoga Tab 3 850F Tablet 16GB",
                                    description="Touchscreen display",
                                    price="SAR 799",
                                    categories=category3
                                    )

session.add(electronic_items1)
session.commit()


electronic_items2 = ElectronicItems(user_id=1,
                                    name="Original Box CHUWI Hi9 Air ",
                                    description="Android 8.0 System",
                                    price="SR 999",
                                    categories=category3)

session.add(electronic_items2)
session.commit()


category4 = Categories(user_id=1,
                       name="Accessories",
                       image="accessory.jpg")

session.add(category4)
session.commit()


electronic_items1 = ElectronicItems(
                                    user_id=1,
                                    name="QuietComfort 35 Series II",
                                    description="Noise-rejecting",
                                    price="SAR 1296",
                                    categories=category4
                                    )

session.add(electronic_items1)
session.commit()


electronic_items2 = ElectronicItems(
                                    user_id=1,
                                    name="1.5 Meter Micro USB Charging \
                                    Cable Braided",
                                    description="Imparts hassle free and",
                                    price="SAR 1296",
                                    categories=category4
                                    )

session.add(electronic_items2)
session.commit()

print "added menu items!"
