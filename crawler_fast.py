#This code sets the method that will iterate over all the movies on imdb
#and adds them to a data base (probably amazon)
#Crawler that does not load the complete http. Simply reqests the source for 
#the  and strings the crap out of it.

import time
#Import the numpy module for infinity
import numpy as np
#Imports system
import sys
#Imports the smtp library for sending emails
import smtplib
#For data base handling, uses 
import _mysql
#For the URL and HTTP request
import urllib3

#Creates the class movie for easy managing
class Movie:
    
    index = -1
    status = 'UC'
    original_title = ''
    browser_title = ''
    year = 0
    parental_grading = 'NA'
    duration = -1
    rating = 0.0
    num_votes = 0
    
    def __init__(self, index, status, original_title, browser_title, year, parental_grading, duration, rating, num_votes):
        self.index = index
        self.status = status
        self.original_title = original_title
        self.browser_title = browser_title
        self.year = year
        self.parental_grading = parental_grading
        self.duration = duration
        self.rating = rating
        self.num_votes = num_votes
    
    def print_movie(self):
        response = 'Index: ' + str(self.index) + '\n'
        response = response + 'Original Title: ' + str(self.original_title) + '\n'
        response = response + 'Browser Title: ' + str(self.browser_title) + '\n'
        response = response + 'Year: ' + str(self.year) + '\n'
        response = response + 'Parental Grading: ' + str(self.parental_grading) + '\n'
        response = response + 'Duration: ' + str(self.duration) + '\n'
        response = response + 'Rating: ' + str(self.rating) + '\n'
        response = response + 'Number of Votes: ' + str(self.num_votes) 
        
        return response

#End of class Movie    

#Finds the substring between the two given substrings.
#if it does not exists, it returns None
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return None
#end of find_between        
        
#method that determines if the given strings contains the substring  
def is_substring(s,sub):
    return(sub in s)
#end of is_substring

def clean(s):
    if(s is None):
        return(None)
    return s.replace(' ','')
#end of clean


def to_utf8(s):
    if(s is None):
        return(None)
    return(s.encode().decode('unicode-escape').encode('latin1').decode('utf-8','ignore'))        
#end of to_utf-8

#Method that interprets the time format of IMDB and extracts the number of minutes
def to_minutes(duration):
    """
        Parameters
        ----------
        duration : String
            the duration of the movie in the IMDB format. Usually #h##min, but can also
            be #min
    """
    
    duration = duration.replace(' ','')
    days = 0
    hours = 0
    minutes = 0
    
    if('d' in duration):
        days = int(duration.split('d')[0] )
        duration = duration.split('d')[1]
    
    
    if('h' in duration):
        hours = int( duration.split('h')[0])
        if(len(duration.split('h'))>1):
            duration = duration.split('h')[1]
    
    duration = duration.replace('min','') 
    duration = duration.replace('m','') 
    
    if(not duration == ''):
        minutes = int(duration)
    
    return days*24*60 + hours*60 + minutes
    
    
#Method that sends email from the gmail account given
def send_email(user, pwd, to_adress, subject, message):
    """
        Parameters
        ----------
        user : String
            The gmail user that will send the email
        pwd : String
            The users password
        to_adress : String
            The recipient's adress
        subject : String
            The subject of the email
        message : String
            The emails message
    """


    msg = "\r\n".join([
      "From: " + user,
      "To: " + to_adress,
      "Subject: " + subject,
      "",
      message
      ])

    server = smtplib.SMTP('smtp.zoho.com',587)
    server.starttls()
    server.ehlo()
    server.login(user, pwd)
    server.sendmail(user, to_adress, msg)
    server.quit()

#end of send_email

#Defines a method that extracts a movie given an index
def get_movie(index):
    """
        Parameters
        ----------
        index : int
            The index of the movie to be searched
        ----------
        Return
        [status, Movie] : Return the status of the given movie. The following are allowed:
            - UN: if the movie is unchecked
            - NR: if the movie has not yet been released
            - NV: if the movie has not yeat been voted
            - NA: if the the given index is a bad one
            - SE: if the given index corresponds to a series (or episode)
            - OK: if the movie was extracted correctly
            
         
         If the status is NA the movie returned is None     
    """
    

    #creates the dictionary with the in-between strings
    search_strings = {}
    
    #Browser title
    search_strings['browser_title'] = ['title_wrapper">\\n<h1 itemprop="name" class="','sp;','">','&nb']
    #Original title
    search_strings['original_title'] = ['originalTitle">' , '<span class="']
    #released
    search_strings['released'] = ['imdbRating']
    #duration
    search_strings['duration'] = ['<time itemprop="duration" datetime="' , '</time>','\\n','\\n']
    #voted
    search_strings['voted'] = ['notEnoughRatings']
    #rating
    search_strings['rating'] = ['<span itemprop="ratingValue">','</span>']
    #number of votes
    search_strings['num_votes'] = ['itemprop="ratingCount">','</span>']
    #is series
    search_strings['is_series'] = ['>Episode Guide<']
    #is episode
    search_strings['is_episode'] = ['Season','Episode','All Episodes']
    #year
    search_strings['year'] = ['<span id="titleYear">','</span>','\\n>','</a>)']
    

    
    #starts the parameters
    search_index = str(index).zfill(7)
    original_title = ''
    browser_title = ''
    year = 0
    parental_grading = 'NA'
    duration = -1
    rating = 0.0
    num_votes = 0
    
    movie = None
    
    try:
        #Loads the manager
        http = urllib3.PoolManager()
        
        
        #Gets the request
        r = http.request('GET', 'http://www.imdb.com/title/tt' + search_index + '/')
        
        #Checks if the movie exists
        if(r.status != 200):
            return ['NA', None]
        
        content = str(r.data)
        
        #Browser Title
        browser_title = find_between(content, search_strings['browser_title'][0], search_strings['browser_title'][1])
        if(not browser_title is None):
            browser_title = to_utf8(find_between(browser_title, search_strings['browser_title'][2], search_strings['browser_title'][3]))
        
        #Original Title
        original_title = to_utf8(find_between(content, search_strings['original_title'][0], search_strings['original_title'][1]))
        if(original_title is None):
            original_title = browser_title
            
        browser_title = browser_title.replace("'", " ")
        original_title = original_title.replace("'", " ")
        
        #Released
        released = is_substring(content, search_strings['released'][0])
        
        if(not released):
            status = 'NR'
            movie = Movie(index, status, original_title, browser_title, year, parental_grading, duration, rating, num_votes)
            return ['NR', movie]
            
        
        #Duration
        duration = find_between(content, search_strings['duration'][0], search_strings['duration'][1])
        if(not duration is None):
            duration = clean(find_between(duration, search_strings['duration'][2], search_strings['duration'][3]))
        
        if(duration is None):
            duration = -1
        else:
            duration = to_minutes(duration)
        
        
        
        #Not enough stars
        voted = not is_substring(content, search_strings['voted'][0])
        
        if(not voted):
            status = 'NV'
            movie = Movie(index, status, original_title, browser_title, year, parental_grading, duration, rating, num_votes)
            return ['NV', movie]
        
        #Rating
        rating = find_between(content, search_strings['rating'][0], search_strings['rating'][1])
        
        #number of votes
        num_votes = find_between(content, search_strings['num_votes'][0], search_strings['num_votes'][1])
        
        is_series = is_substring(content, search_strings['is_series'][0])


        is_episode = True
        for s in  search_strings['is_episode']:
        
            if(is_series):
                break
            
            
            is_episode = is_episode and  is_substring(content, s)
            
            if(not is_episode):
                break
        
        is_series = is_series or is_episode
        
        #Checks if the given index is a series (this is probably cheating, there must be a more standard method)
        if(is_series):
            status = 'SE'
            movie = Movie(index, status, original_title, browser_title, year, parental_grading, duration, rating, num_votes)
            return ['SE', movie]
        
        #Year
        year = find_between(content, search_strings['year'][0], search_strings['year'][1])
        if(not year is None):
            year = clean(find_between(year, search_strings['year'][2], search_strings['year'][3]))
        
        #Parental Grading

        status = 'OK'
        movie = Movie(index, status, original_title, browser_title, year, parental_grading, duration, rating, num_votes)
        return ['OK', movie]
    
    
    finally:
        
        #print('Browser and Display closed')
        sys.stdout.flush()

#end of get_movie


#Single method for extracting the database
def get_db():
    return _mysql.connect(host="imdb-crawler.coxl8wirabtc.us-west-1.rds.amazonaws.com",user="imdb",
                      passwd="imdbcrawler",db="imdb")
#end of get_db 

#inserts a given movie to the data_base
def insert_movie(movie):
    
    try:
        db = get_db()
        query = "INSERT INTO movies (id, stat, original_title, browser_title,r_year, parental_grading, duration, rating, num_votes) "
        query = query + "VALUES (" + str(movie.index) + ", '" + movie.status + "', '"+ movie.original_title + "', '" + movie.browser_title + "', "
        query = query + str(movie.year) + ", '" + movie.parental_grading + "', " + str(movie.duration) + ", " + str(movie.rating) + ", " + str(movie.num_votes) + ")"
        db.query(query)
    

    finally:
        db.close()
    


#Updates and id of a given movie
def update_id(movie_id, status):
    
    """
        Parameters
        ----------
        movie_id : int
            The index of the movie to be searched
        status :  String    
            The new index of the movie 
        ----------
    """
    try:
        db= get_db()
        query = "UPDATE movie_ids SET stat = '" + str(status) + "' WHERE id = " + str(movie_id)
        db.query(query)
    

    finally:
        db.close()
        
#end of update_id



#gets the status of a given id
def get_status(movie_id):
    try:
        db=get_db()
                   
        db.query("SELECT * FROM movie_ids WHERE id = " + str(movie_id))
        
        r=db.store_result()
        
        status = str(r.fetch_row(how = 1)[0]['stat'])
        status = status.replace('b','')
        status = status.replace("'","")
        
        return status
    
    finally:
        db.close()

#end of get_status        
    
    
    
    
#Checks if a given ID is uncheched    
def is_unckecked(movie_id):
    return get_status(movie_id) == 'UC'
#end of is_unckecked    
    

#Runs the random scheme for populating the data base
def run_random():
    
    while(True):
        
        try:
            #Gets the random index 
            index = np.random.randint(10000000)
#            print('----------------------------------------')
            
#            print(index)
            
            #Cheks if the movie is unchecked or not
            if(is_unckecked(index)):
                stat, movie = get_movie(index)
               
#                if(not stat == 'NA'):
#                    insert_movie(movie)
                    
#                update_id(index, stat)
                
#                print(stat)
#                if(stat != 'NA'):
#                    print(movie.print_movie())
                
                 
                print('ID: ' +  str(index) + ' Checked')
#                print('----------------------------------------')
                sys.stdout.flush()
            else:
                print('Movie already checked')
                sys.stdout.flush()
                
        except Exception as e: 
            print('Error in Index: ' +  str(index))
            print(str(e))
            print('----------------------------------------')
            print(' ')
            sys.stdout.flush()
            
        
if __name__ == "__main__":
    
    if(len(sys.argv) == 1 or sys.argv[1].upper() == 'RANDOM'):
        run_random()
        
    



