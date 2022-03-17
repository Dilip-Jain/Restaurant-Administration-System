import pickle

menu={
    "French Fries":['s',106,100],
    "Chilli Cheese Toast":['s',115,100],
    "Garlic Bread":['s',98,100],
    "Sandwich":['s',175,100],
    "Veg. Burger":['s',72,100],
    "Plain Cheese Pizza":['s',190,100],
    "Capsicum, Onion Pizza":['s',210,100],
    "Jain Spl. Pizza":['s',250,100],
    "Tandoori Pizza":['s',250,100],
    "Super Veggie Pizza(Double Cheese)":['s',265,100],
    "Hot & Sour":['s',109,100],
    "Lemon & Coriander":['s',109,100],
    "Veg. Noodle Soup":['s',109,100],
    "Sweet Corn":['s',109,100],
    "Veg. Munchow":['s',109,100],
    "Pav Bhaji":['s',140,100],
    "Dahi Papri":['s',90,100],
    "Thali Special":['m',280,100],
    "Shahi Paneer":['m',210,100],
    "Malai Kofta":['m',210,100],
    "Kju Karri":['m',210,100],
    "Veg. Kolhapuri":['m',210,100],
    "Tandoori Roti":['m', 30,100],
    "Butter Naan":['m',58,100],
    "Tawa Paratha":['m',53,100],
    "Gulab Jamun":['d',60,100],
    "Halwa":['d',60,100],
    "Ice Cream":['d',60,100],
    "Ice Cream soda":['d',119,100],
    "Calcutta Pan":['d',50,100]
    }

f=open('menu','wb')
pickle.dump(menu,f)
f.close()
