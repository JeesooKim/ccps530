import os
import requests
import operator
import re
import nltk
import json
from flask import Flask, render_template, request, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
from stop_words import stops
from collections import Counter
from bs4 import BeautifulSoup
#from datetime import timedelta
#import time
#from datetime import date
from sqlalchemy import create_engine
import itertools
import pandas as pd

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

engine =db.create_engine(os.environ['DATABASE_URL'])

from models import Result
from models import User

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
YEAR=2018
@app.route('/')
def index():
    """ query data from the results table """
    connection = None
    try:
        #https://towardsdatascience.com/sqlalchemy-python-tutorial-79a577141a91

        connection = engine.connect()
        metadata=db.MetaData()
        results = db.Table('results', metadata, autoload=True, autoload_with=engine)

        #print (results.columns.keys())
        #print(repr(metadata.tables['results']))

        #Equivalent to 'SELECT * FROM census'
        query = db.select([results.columns.id, results.columns.url, results.columns.result_no_stop_words, results.columns.timestamp])    
        #query="SELECT url, timestamp FROM results"
        ResultProxy = connection.execute(query)
        #print(ResultProxy)
        ResultSet = ResultProxy.fetchall()
        #ResultSet[:3]

        #print(ResultSet)

        '''
        users = db.Table('users', metadata, autoload=True, autoload_with=engine)
        query2 = db.select([users])            
        UserProxy = connection.execute(query2)        
        UserSet = UserProxy.fetchall()
        '''
        '''
        for record in ResultSet:
            i=0;
            for c in record:
                if i==2:
                    #print("\n*****************\n")
                    sorted_json_results = sorted(
                        c.items(),
                        key=operator.itemgetter(1),
                        reverse=True
                    )[:10]
                    #print(sorted_json_results)
                    #print("\n*****************\n")
                i += 1
        '''


        '''
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT url, timestamp FROM results")
        data= cur.fetchall()

        print("The number of records: ", cur.rowcount)
        '''
        #row = cur.fetchone()
 
        #while row is not None:
        #    print(row)
        #    row = cur.fetchone()
 
        #cur.close()
        connection.close()
    #except (Exception, psycopg2.DatabaseError) as error:
    except (Exception, engine.DatabaseError) as error:
        print("Error!")
        print(error)
    finally:
        if connection is not None:
            connection.close()

    #Get no_stop_words_count [3]
    #count=ResultProxy.rowcount
    #no_stop_words_count=ResultSet
    
    return render_template('index.html', results = ResultSet, year=YEAR) #, users=UserSet)
    #return render_template('index.html')

@app.route('/wordcount', methods=['GET', 'POST'])
def wordcount():    
    errors = []
    results = {}
    #if request.method=='GET':
    #    return('<form action="/test" method="post"><input type="submit" value="Send" /></form>')
    if request.method == "POST":
        # get url that the person has entered
        try:
            url = request.form['url']
            #print(url)
            r = requests.get(url)
            #print(r)
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
            return render_template('wordcount.html', errors=errors)
            #return render_template('wordcount', errors=errors)
        if r:
            # text processing
            #raw = BeautifulSoup(r.text).get_text()            
            raw = BeautifulSoup(r.text, "html.parser").get_text()
            nltk.data.path.append('./nltk_data/')  # set the path
            tokens = nltk.word_tokenize(raw)
            text = nltk.Text(tokens)
            # remove punctuation, count raw words
            nonPunct = re.compile('.*[A-Za-z].*')
            raw_words = [w for w in text if nonPunct.match(w)]
            raw_word_count = Counter(raw_words)
            # stop words
            no_stop_words = [w for w in raw_words if w.lower() not in stops]
            no_stop_words_count = Counter(no_stop_words)
            print(type(no_stop_words_count))
            print(no_stop_words_count)

            # save the results
            results = sorted(
                no_stop_words_count.items(),
                key=operator.itemgetter(1),
                reverse=True
            )[:10]
            
            try:
                result = Result(
                    url=url,
                    result_all=raw_word_count,
                    result_no_stop_words=no_stop_words_count
                )
                db.session.add(result)
                db.session.commit()
            except:
                errors.append("Unable to add item to database.")
    return render_template('wordcount.html', errors=errors, results=results, year=YEAR)
    #return render_template('wordcount', errors=errors, results=results)


@app.route('/details/<id>')
def details(id):
    connection = None
    try:
        #https://towardsdatascience.com/sqlalchemy-python-tutorial-79a577141a91
        rowid=id
        #print(rowid)
        connection = engine.connect()

        metadata=db.MetaData()
        results = db.Table('results', metadata, autoload=True, autoload_with=engine)
        
        #query = db.select([results.columns.url, results.columns.result_no_stop_words, results.columns.timestamp]).where(results.columns.id == rowid)
        query = db.select([results.columns.result_no_stop_words]).where(results.columns.id == rowid)
        ResultProxy = connection.execute(query)        
        #ResultSet = ResultProxy.fetchall()
        ResultSet = ResultProxy.fetchone()
        #print(type(ResultSet))
        sorted_json_results = ResultSet
        #sorted_json_results = sorted(
        #        ResultSet.items(),
        #        key=operator.itemgetter(1),
        #        reverse=True
        #)[:10]

        print(sorted_json_results)
        connection.close()
    #except (Exception, psycopg2.DatabaseError) as error:
    except (Exception, engine.DatabaseError) as error:
        print("Error!")
        print(error)
    finally:
        if connection is not None:
            connection.close()
    return render_template("details.html", sorted_json_results=sorted_json_results, id=id,year=YEAR)
    #return render_template("details.html", url=url, timestamp=timestamp, sorted_json_results=sorted_json_results, year=YEAR)

@app.route("/image")
def image():
    return render_template("upload.html", year=YEAR)

@app.route("/upload", methods=['POST'])
def upload():
    print(APP_ROOT)

    target = os.path.join(APP_ROOT, 'images/')
    #print(target)

    if not os.path.isdir(target):
        os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    '''
    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)
        '''
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        print ("Accept incoming file:", filename)
        print ("Save it to:", destination)
        upload.save(destination)
        

    return render_template("complete.html",image_name=filename, year=YEAR)

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)

@app.route('/gallery')
def get_gallery():
    image_names = os.listdir('./images')
    print(image_names)
    return render_template("gallery.html", image_names=image_names, year=YEAR)

@app.route('/users', methods=['GET', 'POST'])
def users():
    """ query data from the results table """
    connection = None
    try:
        #https://towardsdatascience.com/sqlalchemy-python-tutorial-79a577141a91
        connection = engine.connect()
        metadata=db.MetaData()
        users = db.Table('users', metadata, autoload=True, autoload_with=engine)
        query = db.select([users])
        UserProxy = connection.execute(query)
        UserSet = UserProxy.fetchall()
        connection.close()    
    except (Exception, engine.DatabaseError) as error:
        print("Error!")
        print(error)
    finally:
        if connection is not None:
            connection.close()

    
    errors = []
    results = []
    #if request.method=='GET':
    #    return('<form action="/test" method="post"><input type="submit" value="Send" /></form>')
    if request.method == "POST":
        # get url that the person has entered
        try:
            name = request.form['username']
            password = request.form['userpassword']
            print(name + " " + password)

            name = request.form['username']
            password = request.form['userpassword']
                        
            results.append(name)
            results.append(password)
            # save the results            
            try:
                user = User(
                    username=name,
                    userpassword=password
                )
                print(user)
                db.session.add(user)
                db.session.commit()                
            except:
                errors.append("Unable to add user to database.")
            
        except:
            errors.append(
                "Unable to get inputs. Please make sure it's valid and try again."
            )
            return render_template('users.html', errors=errors)
            
    return render_template('users.html', year=YEAR, users=UserSet, results=results)

@app.route('/adduser', methods=['GET', 'POST'])
def adduser():

    errors = []
    results = []
    if request.method=='GET':
        #return('<form action="/test" method="post"><input type="submit" value="Send" /></form>')
        return render_template("adduser.html")
    elif request.method == "POST":
        # get url that the person has entered
        try:
            name = request.form['username']
            password = request.form['userpassword']
                        
            results.append(name)
            results.append(password)
            print(results)

            # save the results            
            try:
                print(name + " " + password)
                user = User(
                    username=name,
                    userpassword=password
                )
                print(user)
                db.session.add(user)
                db.session.commit()                
            except:
                errors.append("Unable to add user to database.")
            
        except:
            errors.append(
                "Unable to get inputs. Please make sure it's valid and try again."
            )
            return render_template('adduser.html', errors=errors)
    return render_template('adduser.html', year=YEAR, results=results)

@app.route('/user_update/<id>', methods=['GET', 'POST'])
def user_update(id):
    userid=id
    if request.method == "GET":
        userid=id
        print(userid)
        return render_template('user_update.html', year=YEAR, id=id)
    elif request.method == 'POST':

        connection = None
        try:
            #https://towardsdatascience.com/sqlalchemy-python-tutorial-79a577141a91
            #id=request.form.get('id', type=int)
            print(userid)
            # change the values you want to update
            
            #record.username = updatename
            updatename = request.form['username']
            updatename = request.form.get('username')
            print(updatename)
            #record.userpassword = updatepw
            #updatepw = request.form.get('userpassword')            
            # query.get() method gets a Row by the primary_key
            #record = Row.query.get(userid)
            connection = engine.connect()
            metadata=db.MetaData()
            users = db.Table('users', metadata, autoload=True, autoload_with=engine)
            results= connection.execute(db.select([users])).fetchall() 
            df=pd.DataFrame(results)
            df.columns =results[0].keys()
            df.head(4)
            '''
            if not((updatename is None) and (updatepw is None)):
                if (not (updatename is None)) or (updatename != ''):
                    #record.username = updatename
                    updatename = request.form.get('username')
                    query = db.update(users).values(username = updatename)
                if (not (updatepw is None)) or (updatepw != ''):
                    print("here"+updatepw)
                    #record.userpassword = updatepw
                    updatepw = request.form.get('userpassword')
                    query = db.update(users).values(userpassword = updatepw)
                #query = db.update(users).values(salary = 100000)
                if not (updatepw)
                query = query.where(users.columns.Id == userid)
                results = connection.execute(query)
            '''
            
            if not updatename:
                #updatename = request.form.get('username')
                query = db.update(users).values(username = updatename)
                query = query.where(users.columns.Id == id)
                results = connection.execute(query)
                    #record.username = updatename
                
            results = connection.execute(db.select([users])).fetchall()
            df = pd.DataFrame(results)
            df.columns = results[0].keys()
            df.head(4)

            # commit changes
            db.session.commit()

            users = db.Table('users', metadata, autoload=True, autoload_with=engine)
            query = db.select([users])
            UserProxy = connection.execute(query)
            UserSet = UserProxy.fetchall()
        #except (Exception, psycopg2.DatabaseError) as error:
        except (Exception, engine.DatabaseError) as error:
            print("Error!")
            print(error)
        finally:
            if connection is not None:
                connection.close()
        #return render_template("details.html", sorted_json_results=sorted_json_results, id=id,year=YEAR)        
    # redirect back to your main view
    #return redirect(url_for('users'))
    return render_template('users.html', year=YEAR, users=UserSet)

@app.route('/user_delete/<id>', methods=['GET', 'POST'])
def user_delete(id):
    userid=id    
    if request.method == "GET":
        userid=id        
        return render_template('users.html', year=YEAR, userid=userid)
    elif request.method == 'POST':
        connection = None
        try:
            #https://towardsdatascience.com/sqlalchemy-python-tutorial-79a577141a91
            #id=request.form.get('id', type=int)
            print(userid)
            # change the values you want to update
            
            connection = engine.connect()
            metadata=db.MetaData()
            users = db.Table('users', metadata, autoload=True, autoload_with=engine)
            results= connection.execute(db.select([users])).fetchall()
            df=pd.DataFrame(results)
            df.columns =results[0].keys()
            df.head(4)

            # Build a statement to delete where salary < 100000
            query = db.delete(users)
            query = query.where(users.columns.id == userid)
            results = connection.execute(query)
            
            results = connection.execute(db.select([users])).fetchall()
            df = pd.DataFrame(results)
            df.columns = results[0].keys()
            df.head(4)

            # commit changes
            db.session.commit()

            users = db.Table('users', metadata, autoload=True, autoload_with=engine)
            query = db.select([users])
            UserProxy = connection.execute(query)
            UserSet = UserProxy.fetchall()


        #except (Exception, psycopg2.DatabaseError) as error:
        except (Exception, engine.DatabaseError) as error:
            print("Error!")
            print(error)
        finally:
            if connection is not None:
                connection.close()
        #return render_template("details.html", sorted_json_results=sorted_json_results, id=id,year=YEAR)        
    # redirect back to your main view
    #return redirect(url_for('users'))
    return render_template('/users.html', year=YEAR, users=UserSet)

if __name__ == '__main__':
    app.run()