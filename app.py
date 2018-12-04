import os
import requests
import operator
import re
import nltk
from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from stop_words import stops
from collections import Counter
from bs4 import BeautifulSoup
from sqlalchemy import create_engine

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

engine =db.create_engine(os.environ['DATABASE_URL'])

from models import Result

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
        query = db.select([results.columns.id, results.columns.url, results.columns.timestamp])    
        #query="SELECT url, timestamp FROM results"
        ResultProxy = connection.execute(query)
        #print(ResultProxy)
        ResultSet = ResultProxy.fetchall()
        #ResultSet[:3]
        
        '''
        users = db.Table('users', metadata, autoload=True, autoload_with=engine)
        query2 = db.select([users])            
        UserProxy = connection.execute(query2)        
        UserSet = UserProxy.fetchall()
        '''
        connection.close()
    #except (Exception, psycopg2.DatabaseError) as error:
    except (Exception, engine.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
    
    #return render_template('index.html', results = ResultSet, users=UserSet)
    return render_template('index.html', results = ResultSet)

@app.route('/wordcount', methods=['GET', 'POST'])
def wordcount():
    errors = []
    results = {}
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
    return render_template('wordcount.html', errors=errors, results=results)
    #return render_template('wordcount', errors=errors, results=results)

if __name__ == '__main__':
    app.run()