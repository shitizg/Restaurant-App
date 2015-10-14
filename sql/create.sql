drop table if exists Alerts;
drop table if exists Users;
drop table if exists Role;
drop table if exists OrderedItems;
drop table if exists Orders;
drop table if exists MenuItems;
drop table if exists Item_Ingredients;
drop table if exists Ingredient_Inventory;
drop table if exists Complaints;
drop table if exists Meal_Type;
drop table if exists Categories;
drop table if exists Item_Categories;
drop table if exists Receipts;
drop table if exists Receipt;

create table Role (
   id integer primary key,
   name char(20) unique not null
);

insert into Role VALUES (1, "Manager");
insert into Role values (2, "Waiter");
insert into Role values (3, "Kitchen Assistant");

create table Users (
   id integer primary key,
   uname char(12) unique not null,
   password char(60) not null,
   role integer not null,
   foreign key(role) references Role(name)
);

insert into Users (uname, password, role) VALUES
   ('manager', '$2a$12$CyLyLDPA5NFTY48o3fANQOEsni38JgHBk3FNwdUFd1OwYMBZxN146', 1);
insert into Users (uname, password, role) VALUES
   ('waiter', '$2a$12$CyLyLDPA5NFTY48o3fANQOEsni38JgHBk3FNwdUFd1OwYMBZxN146', 2);
insert into Users (uname, password, role) VALUES
   ('assistant', '$2a$12$CyLyLDPA5NFTY48o3fANQOEsni38JgHBk3FNwdUFd1OwYMBZxN146', 3);

create table Meal_Type (
  id integer primary key,
  meal_type char(20) unique not null
);
insert into Meal_Type (id, meal_type) VALUES
    (0, 'Beverage');
insert into Meal_Type (id, meal_type) VALUES
    (1, 'Breakfast');
insert into Meal_Type (id, meal_type) VALUES
    (2, 'Lunch');
insert into Meal_Type (id, meal_type) VALUES
    (3, 'Dinner');

create table MenuItems  (
      id integer primary key,
      name char(20) unique not null,
      meal_type integer,
      price float not null,
      available boolean default true,
      description char(250),
      picture char(200),
      foreign key(meal_type) references Meal_Type(id)
);

insert into MenuItems (name, price, meal_type, description,picture) values
   ('Chicken', 10.0, 2, 'The Best Chicken','./static/chicken.jpg');
insert into MenuItems (name, price, meal_type, description,picture) values
   ('Pasta', 16.0, 2, 'Yummy Pasta','./static/pasta.jpg');
insert into MenuItems (name, price, description,picture) values
   ('Cheesecake', 5.0, 'A Dessert','./static/cheesecake.jpg');
insert into MenuItems (name, price, description,picture) VALUES
   ('Soda', 4.0, 'Sprite, Coke, or Fanta','./static/soda.jpg');

create table Orders (
   id integer primary key,
   waiter integer not null,
   status integer not null default 0,
   foreign key (waiter) references Users(id),
   check(status >= 0 and status < 3)
   );
insert into Orders (waiter) VALUES
   (2);

create table OrderedItems (
   order_id integer not null,
   item_id integer not null,
   qty integer not null default 1,
   position TIMESTAMP default CURRENT_TIMESTAMP,
   primary key (order_id, item_id),
   foreign key (order_id) references Orders(id)
);

insert into OrderedItems (order_id, item_id) VALUES
   (1,1);

create table Item_Ingredients(
   id integer not null,
   ingredient char(20) unique not null,
   qty integer not null default 1,
   primary key (id, ingredient)
);
insert into Item_Ingredients (id, ingredient, qty) VALUES
    (1, 'Raw Chicken', 1);
insert into Item_Ingredients (id, ingredient, qty) VALUES
    (2, 'pasta sauce', 1);
insert into Item_Ingredients (id, ingredient, qty) VALUES
    (2, 'noodles', 2);
insert into Item_Ingredients (id, ingredient, qty) VALUES
    (3, 'cheesecake mix', 1);
insert into Item_Ingredients (id, ingredient, qty) VALUES
    (4, 'fountain pop', 1);

create table Ingredient_Inventory(
   ingredient char(20) primary key unique not null,
   qty integer not null default 0,
   is_empty boolean default false
);
insert into Ingredient_Inventory(ingredient, qty) VALUES
  ('Raw Chicken', 10);
insert into Ingredient_Inventory(ingredient, qty) VALUES
  ('pasta sauce', 7);
insert into Ingredient_Inventory(ingredient, qty) VALUES
  ('noodles', 25);
insert into Ingredient_Inventory(ingredient, qty) VALUES
  ('cheesecake mix', 5);
insert into Ingredient_Inventory(ingredient, qty) VALUES
  ('fountain pop', 0);

create table Categories(
  id integer unique primary key,
  category char(50)
);

insert into Categories(id, category) VALUES
  (1, 'meat');
insert into Categories(id, category) VALUES
  (2, 'vegetarian');

create table Item_Categories(
  item_id integer,
  category_id integer,
  foreign key (category_id) references Categories(id),
  foreign key (item_id) references MenuItems(id),
  primary key (item_id, category_id)
);
insert into Item_Categories(item_id, category_id) VALUES
   (1,1);
insert into Item_Categories(item_id, category_id) VALUES
   (2,2);

create table Complaints(
  id integer unique primary key,
  complaint char(500) not null,
  waiter_id integer references Users(id),
  stime TIMESTAMP default CURRENT_TIMESTAMP
);

  INSERT INTO Complaints(complaint,waiter_id) VALUES
  ('Prices are too high. -Bill Nye',2);

create table Alerts(
  id integer unique primary key,
  order_id integer not null,
  stime TIMESTAMP default CURRENT_TIMESTAMP,
  foreign key (order_id) references Orders(id)
);

--paid is:	0 if default
--		1 if customer sent payment
--		2 if waiter confirmed payment
create table Receipts(
  id integer unique primary key,
  order_id integer unique not null,
  total float not null,
  paid integer default 0,
  foreign key (order_id) references Orders(id)
);

insert into Receipts(id, order_id, total, paid) values
   (0, 1, 0.0, 0);
