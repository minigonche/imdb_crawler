# Script for extracting the database from MySql, once it has already been loaded

#For data base handling, uses 
import _mysql

#Single method for extracting the database
def get_db():
    return _mysql.connect(host="imdb-crawler.coxl8wirabtc.us-west-1.rds.amazonaws.com",user="imdb",
                      passwd="imdbcrawler",db="imdb")
#end of get_db 


#method that cleans strings
def clean(s):
    s = s[1:]
    return(s)

#Gets the movie ids and saves them inside a csv called movie_ids.csv
def load_movie_ids():
    try:
        file = open('movie_ids.csv', 'w')
        file.write('stat,id' + '\n')
        
        db=get_db()
        db.query("SELECT * FROM movie_ids")
        r=db.use_result()
        row = r.fetch_row(how = 1)
        i = 0
        
        while(len(row)>0):
            m_id = str(row[0]['id'])
            stat = clean(str(row[0]['stat']))
            file.write(m_id + ',' + stat + '\n')
            row = r.fetch_row(how = 1)
            i = (i + 1)
            if i%1000000 == 0:
                print(i)
    
    finally:
        db.close()
        file.close()

#end of load movies    


#Gets the movies  and saves them inside a csv called movies.csv
def load_movies(status = None):
    try:
        if(status == None):
            file = open('movies.csv', 'w')
        else:
            file = open('movies_' + status + '.csv', 'w')
        
        
        file.write('id, stat, original_title, browser_title, r_year, parental_grading, duration, rating, num_votes' + '\n')
        
        db=get_db()
        if(status == None):
            db.query("SELECT * FROM movies")
        else:
            db.query("SELECT * FROM movies " + "WHERE stat = '" + status + "'")
        
        r=db.use_result()
        row = r.fetch_row(how = 1)
        i = 0
        
        while(len(row)>0):
            m_id = str(row[0]['id'])
            stat = clean(str(row[0]['stat']))
            original_title = clean(str(row[0]['original_title']))
            browser_title = clean(str(row[0]['browser_title']))
            r_year = str(row[0]['r_year'])
            parental_grading = clean(str(row[0]['parental_grading']))
            duration = str(row[0]['duration'])
            rating = str(row[0]['rating'])
            num_votes = str(row[0]['num_votes'])
            
            file.write(m_id + ',' + stat + ',' + original_title + ',' + browser_title + ',' + r_year + ',' + parental_grading + ',' + duration + ',' + rating + ',' + num_votes + '\n')
            
            row = r.fetch_row(how = 1)
            i = (i + 1)
            if i%1000000 == 0:
                print(i)
    
    finally:
        db.close()
        file.close()



#end of load movies
load_movies('OK')



