# ccps530
Web Systems Development

Name: JEE SOO KIM
\r
Online Demo: https://wordcount-pro-jsk.herokuapp.com/
\r
Project Title: Flask App – Word count with Image Gallery
\r
Course: CCPS530
\r
Instructor: Ghassem Tofighi
\r\r
Requirements:
1.	Python/PHP Programming
•	Python programming
•	a Flask app that calculates word-frequency pairs based on the text from a given URL. 
•	https://realpython.com/flask-by-example-part-1-project-setup/
2.	DataConnection:CRUD

•	Create: Working
•	R: Working
•	U: ? (Need to debug)
•	D:Working
3.	Bootstrap Plugins

(1)	DataTables for Bootstrap
A extension of the DataTables jQuery plugin that integrates seamlessly with the Bootstrap 3 and 4 UI. 
https://startbootstrap.com/bootstrap-resources#plugins-other
Bootstrap 4
As with Bootstrap 3, DataTables can also be integrated seamlessly with Bootstrap 4. This integration is done simply by including the DataTables Bootstrap 4 files (CSS and JS) which sets the defaults needed for DataTables to be initialised as normal, as shown in this example.
https://datatables.net/examples/styling/bootstrap4.html
(2) 

4.	jQuery library features
(1)	Galleria Galleria-JavaScript Image Gallery
Galleria is a JavaScript Image Gallery. It’s built so that it simplifies your process of creating a beautiful image gallery. You don’t have to be a programming expert to use it. Just a few lines of code, add some pictures, and you’re done.
Galleria has a lot of great tools, which you can use to create your own image gallery. Galleria, you can see in the screenshot, is the free version, which you can customize as you want.
https://1stwebdesigner.com/jquery-gallery/#galleries
https://docs.galleria.io/article/15-beginners-guide
(2)	jQueryDataTable
DataTables is a plug-in for the jQuery Javascript library. It is a highly flexible tool, build upon the foundations of progressive enhancement, that adds all of these advanced features to any HTML table.
https://datatables.net/

Documentation:
Ref: https://github.com/IBM/watson-vehicle-damage-analyzer
Build a Flask app that (1) calculates word-frequency pairs based on the text from a given URL, following Part 1-3 according to Flask by Example, and (2) uploads image(s) and display image(s) using Galleria-JavaScript Image Gallery.

In this developer code pattern, we will create a Flask app using Python, Postgres, SQLAlchemy, Alembic, BeautifulSoup, Natural Language Toolkit(nltk), jQuery, and Bootstrap plugins. This Flask app sends a URL of a page and displays the top 10 most frequently used words in that page, analyzed by a count hashable objects, Counter, for words processed by BeautifulSoup and NLTK.
The Python library, BeautifulSoup will scrape and parse, then NLTK will break up the text into individual words and turn each word into an nltk text object.
When you have completed this Code Pattern, you will understand how to:
•	Set up a local development environment and then deploy an environment on Heroku.
•	Set up a PostgreSQL database along with SQLAlchemy and Alembic to handle migrations.
•	Create a Words counter and an Image Gallery in an application.
Flow
1.	User interacts with the web page and sends an URL.
2.	The URL on the web page is passed to the server on Heroku.
3.	The server processes the text of the web page using Beautiful Soup and NLTK for analysis.
4.	Count Hashable Objects, Counter, counts each word and the information are saved in the database as well as returned to the end user.
Included components
•	Beautiful Soup: a Python library for pulling data out of HTML and XML files
•	Natural Language Toolkit (NLTK): a leading platform for building Python programs to work with human language data
Featured Technologies
•	Flask: a micro web framework written in Python. 
•	Python: an interpreted high-level programming language for general-purpose programming.
•	jQuery: a fast, small, and feature-rich JavaScript library.
•	Bootstrap: an open source toolkit for developing with HTML, CSS, and JS.
Watch the Video
 

Steps
This code pattern contains (1) Local environment setup, and (2) Heroku setup/deploy.

Deploy this application locally and remotely
Perform steps 1-9:
1.	Clone the repo
2.	Set up a local development environment
2-1 Set up a virtual environment to use for this application
2-2 Install Flask
3.	Create a Heroku account, download and install the Heroku Toolbelt
4.	Set up a Postgres database
5.	Add in the back-end logic
6.	Deploy this application on Heroku
1. Clone the repo
Clone the ccps530 repo locally. In a terminal, run:
$ git clone https://github.com/JeesooKim/ccps530.git
$ cd ccps530
2. Set up a local development environment
2-1 Set up a virtual environment to use for this application:
$ pyvenv-3.5 env
$ call env/Scripts/activate


2-2 Install Flask:
$ pip install Flask==0.10.1
Add the installed libraries to our requirements.txt file:
$ pip freeze > requirements.txt

3. Create a Heroku account, download and install the Heroku Toolbelt
3-1 Create your new Heroku apps.
For example, let’s name your app “wordcount”:
$ heroku create wordcount

$ git remote add pro git@heroku.com:YOUR_APP_NAME.git

3-2 Push this app live to Heroku.
•	git push wordcount master
4. Set up a Postgres database to store the results of our word counts as well as SQLAlchemy, an Object Relational Mapper, and Alembic to handle database migrations
4-1 Install Postgres on your local computer
pip install psycopg2==2.7.6.1 Flask-SQLAlchemy===2.3.1 Flask-Migrate==1.8.0
$ pip freeze > requirements.txt

4-2 Once you have Postgres installed and running, create a database called wordcount_dev to use as our local development database:
$ psql
# create database wordcount_dev;
CREATE DATABASE
# \q

4-3 Upgrades to the database using the db upgrade command:
$ python manage.py db upgrade
  INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
  INFO  [alembic.runtime.migration] Will assume transactional DDL.
  INFO  [alembic.runtime.migration] Running upgrade  -> 63dba2060f71, empty message

 The database is now ready for us to use in our app:
$ psql
# \c wordcount_dev
You are now connected to database "wordcount_dev" as user "michaelherman".
# \dt

                List of relations
 Schema |      Name       | Type  |     Owner
--------+-----------------+-------+---------------
 public | alembic_version | table | michaelherman
 public | results         | table | michaelherman
(2 rows)

# \d results
                                     Table "public.results"
        Column        |       Type        |                      Modifiers
----------------------+-------------------+------------------------------------------------------
 id                   | integer           | not null default nextval('results_id_seq'::regclass)
 url                  | character varying |
 result_all           | json              |
 result_no_stop_words | json              |
Indexes:
    "results_pkey" PRIMARY KEY, btree (id)

4-4 Apply the migrations to the databases on Heroku
-Check if we have a database set up on the staging server run:
$ heroku config --app wordcount
=== wordcount Config Vars
APP_SETTINGS: config.StagingConfig

If you don’t see a database environment variable, we need to add the Postgres addon to the staging server. To do so, run the following command:
$ heroku addons:create heroku-postgresql:hobby-dev --app wordcount
  Creating postgresql-cubic-86416... done, (free)
  Adding postgresql-cubic-86416 to wordcount... done
  Setting DATABASE_URL and restarting wordcount... done, v8
  Database has been created and is available
   ! This database is empty. If upgrading, you can transfer
   ! data from another database with pg:copy
  Use `heroku addons:docs heroku-postgresql` to view documentation.

Confirm if you can see the connection settings for the database:
=== wordcount-stage Config Vars
APP_SETTINGS: config.StagingConfig
DATABASE_URL: postgres://azrqiefezenfrg:Zti5fjSyeyFgoc-U-yXnPrXHQv@ec2-54-225-151-64.

4-5 Run the migrations that we created to migrate our staging database by using the heroku runcommand:
$ heroku run python manage.py db upgrade --app wordcount
  Running python manage.py db upgrade on wordcount... up, run.5677
  INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
  INFO  [alembic.runtime.migration] Will assume transactional DDL.
  INFO  [alembic.runtime.migration] Running upgrade  -> 63dba2060f71, empty message
5. Test this application out.
5-1 Fire up the app to test it out:
$ python manage.py runserver

5-2 Navigate to http://localhost:5000/ and you should see the form staring back at you.

Sample Output Pages


Links
•	Demo on Youtube: https://youtu.be/JYp2B22QHaE
