#This code sets the method that will iterate over all the movies on imdb
#and adds them to a data base (probably amazon)


#Imports teh Display, this is done so that the browser can be opened
from pyvirtualdisplay import Display
#Import the selnium module
from selenium import webdriver
#Imports the time library to make the program wait
import time
#Import the numpy module for infinity
import numpy as np
#Imports system
import sys
#Imports the smtp library for sending emails
import smtplib
#For data base handling, uses 
import _mysql

#Creates the class movie for easy managing
class Movie:
    
    index = -1
    original_title = ''
    browser_title = ''
    year = 0
    parental_grading = 'NA'
    duration = ''
    rating = 0.0
    num_votes = 0
    
    def __init__(self, index, original_title, browser_title, year, parental_grading, duration, rating, num_votes):
        self.index = index
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
    
    #Cretaes the display, without this the webDriver invocation fails
    display = Display(visible=0, size=(1024, 768))
    display.start()
    
    #Uses the Chrome driver, Firefox could not get pass the send form step
    browser = webdriver.Chrome()
    
    #starts the parameters
    search_index = str(index).zfill(7)
    original_title = ''
    browser_title = ''
    year = 0
    parental_grading = 'NA'
    duration = ''
    rating = 0.0
    num_votes = 0
    
    movie = None
    
    try:
        browser.get('http://www.imdb.com/title/tt' + search_index + '/')
        
        #Checks if the movie exisrs
        if(browser.execute_script("return document.getElementsByClassName('error_quote').length") > 0):
            return ['NA', None]
        
        #Browser Title
        browser_title = str(browser.execute_script("return document.getElementsByClassName('title_wrapper')[0].childNodes[1].innerHTML")).split('&nbsp;')[0]
        
        #Original Title
        if(browser.execute_script("return document.getElementsByClassName('originalTitle').length") > 0):
            original_title = str(browser.execute_script("return document.getElementsByClassName('originalTitle')[0].innerHTML")).split('<span')[0]
        
        #Released
        released = browser.execute_script("return document.getElementsByClassName('imdbRating').length") > 0
        
        if(not released):
            movie = Movie(index, original_title, browser_title, year, parental_grading, duration, rating, num_votes)
            return ['NR', movie]
            
        
        #Duration
        duration = str(browser.execute_script("return document.getElementsByTagName('time')[0].innerHTML")).replace('  ','').replace('\n','')
        
        #Not enough stars
        voted = browser.execute_script("return document.getElementsByClassName('notEnoughRatings').length") == 0
        
        if(not voted):
            movie = Movie(index, original_title, browser_title, year, parental_grading, duration, rating, num_votes)
            return ['NV', movie]
        
        #Rating
        rating = float(str(browser.execute_script("return document.getElementsByClassName('imdbRating')[0].childNodes[1].childNodes[1].childNodes[0].innerHTML")))
        
        #number of votes
        num_votes = int(str(browser.execute_script("return document.getElementsByClassName('imdbRating')[0].childNodes[3].childNodes[0].innerHTML")).replace('.','').replace(',',''))
        
        #Checks if the given index is a series (this is probably cheating, there must be a more standard method)
        if(browser.execute_script("return document.getElementsByClassName('title_wrapper')[0].childNodes[1].childNodes.length") == 1):
            movie = Movie(index, original_title, browser_title, year, parental_grading, duration, rating, num_votes)
            return ['SE', movie]
        
        #Year
        year = int(str(browser.execute_script("return document.getElementsByClassName('title_wrapper')[0].childNodes[1].childNodes[1].childNodes[1].innerHTML")))
        
        #Parental Grading
        parental_grading = str(browser.execute_script("return document.getElementsByClassName('subtext')[0].childNodes[1].getAttribute('content')"))
        
        movie = Movie(index, original_title, browser_title, year, parental_grading, duration, rating, num_votes)
        return ['OK', movie]
        

    
    finally:
        
        browser.quit()
        display.stop()
        print('Browser and Display closed')
        sys.stdout.flush()
        


#The methods that extracts the lowest lifeMiles value for a given trip
def extract_movies(min_id, max_id):
    """
        Parameters
        ----------
        min_id : int
            A seven digit number of the initial id of the movie to crawl
        max_id : int
            A seven digit number of the final id of the movie to crawl
    """
    
    #Cretaes the display, without this the webDriver invocation fails
    display = Display(visible=0, size=(1024, 768))
    display.start()
    
    #Uses the Chrome driver, Firefox could not get pass the send form step
    browser = webdriver.Chrome()
    
    try:
        browser.get('http://www.imdb.com/title/tt4123432/')
        
        #Browser Title
        browser_title = str(browser.execute_script("return document.getElementsByClassName('title_wrapper')[0].childNodes[1].innerHTML")).split('&nbsp;')[0]
        
        #Original Title
        original_title = None
        if(browser.execute_script("return document.getElementsByClassName('originalTitle').length") > 0):
            original_title = str(browser.execute_script("return document.getElementsByClassName('originalTitle')[0].innerHTML")).split('<span')[0]
        
        #Released
        released = browser.execute_script("return document.getElementsByClassName('imdbRating').length") > 0
        
        if(not released):
            print(original_title)
            print(browser_title)
            print('not released')
            sys.exit('ok')
        
        #Year
        year = str(browser.execute_script("return document.getElementsByClassName('title_wrapper')[0].childNodes[1].childNodes[1].childNodes[1].innerHTML"))
        
        #Parental Grading
        parental_grading = str(browser.execute_script("return document.getElementsByClassName('subtext')[0].childNodes[1].getAttribute('content')"))
        
        #Duration
        duration = str(browser.execute_script("return document.getElementsByTagName('time')[0].innerHTML")).replace('  ','').replace('\n','')
        
        #Not enough stars
        voted = browser.execute_script("return document.getElementsByClassName('notEnoughRatings').length") == 0
        
        if(not voted):
            print(original_title)
            print(browser_title)
            print(year)
            print(parental_grading)
            print(duration)
            print('not voted')
            sys.exit('ok')
        
        #Rating
        rating = str(browser.execute_script("return document.getElementsByClassName('imdbRating')[0].childNodes[1].childNodes[1].childNodes[0].innerHTML"))
        
        #number of votes
        num_votes = str(browser.execute_script("return document.getElementsByClassName('imdbRating')[0].childNodes[3].childNodes[0].innerHTML")).replace('.','').replace(',','')
        
        
        
        
        print(original_title)
        print(browser_title)
        print(year)
        print(parental_grading)
        print(duration)
        print(rating)
        print(num_votes)
        
    
    
    finally:
        
        browser.quit()
        display.stop()
        print('Browser and Display closed')
        sys.stdout.flush()
        


if __name__ == "__main__":
    
    movie = get_movie(4574334)[1]
    print(movie.print_movie())
