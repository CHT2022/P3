from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from flask_table import Table, Col

#building flask table for showing recommendation results
class Results(Table):
    title = Col('Recommendation List')


app = Flask(__name__)

#Welcome Page
@app.route("/", methods=["GET", "POST"])
def welcome():
    if request.method=="POST":
        return render_template('result.html')
    return render_template('index.html')

#Results Page
@app.route("/result", methods=["GET", "POST"])
def result():
    if request.method == 'POST':
        
        #reading the original dataset
        df = pd.read_csv('fileapi.csv')

        #reading movie title given by user in the front-end
        film = request.form.get('titre')
       
        def recommend(m): 
              m=m.lower()
              if m in df['movie_title'].str.lower().unique():
                  m=m	
              else:
                  print('Ce film n''est pas dans notre database. Veuillez choisir un autre film.')
                  raise ValueError('The film is not in our database. Please choose another film.')                  
        	
              i = df.loc[df['movie_title'].str.lower() == m].index[0]
              cluster = df.iloc[i]['cluster_KMeans']
              dflist = df[(df['cluster_KMeans']==cluster) & (df.movie_title.str.lower() != m) & (df['imdb_score']>5)]
              dflist.sort_values('imdb_score', ascending=False)
              dflist = dflist.head(5)
              dflist = dflist.reset_index()
              return (dflist['movie_title'])

        try:
            output = recommend(film)
            table = Results(output)
            table.border = True
            return render_template('result.html', table=table)
        except ValueError as e:
            return render_template('index.html', error=e)
      

if __name__ == '__main__':
   app.run(debug = True)