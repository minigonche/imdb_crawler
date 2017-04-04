import urllib3


#Finds the substring between the two given substrings.
#if it does not exists, it returns None
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return None
        
        
#method that determines if the given strings contains the substring  
def is_substring(s,sub):
    return(sub in s)

def clean(s):
    if(s is None):
        return(None)
    return s.replace(' ','')

def to_utf8(s):
    if(s is None):
        return(None)
    return(s.encode().decode('unicode-escape').encode('latin1').decode('utf-8','ignore'))
    
#Loads the manager
http = urllib3.PoolManager()

title = '1756595'

#Gets the request
r = http.request('GET', 'http://www.imdb.com/title/tt' + title + '/')

print(r.status)
#Turns into string
content = str(r.data)

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







browser_title = find_between(content, search_strings['browser_title'][0], search_strings['browser_title'][1])
if(not browser_title is None):
    browser_title = find_between(browser_title, search_strings['browser_title'][2], search_strings['browser_title'][3])
    
original_title = to_utf8(find_between(content, search_strings['original_title'][0], search_strings['original_title'][1]))


released = is_substring(content, search_strings['released'][0])


duration = find_between(content, search_strings['duration'][0], search_strings['duration'][1])
if(not duration is None):
    duration = clean(find_between(duration, search_strings['duration'][2], search_strings['duration'][3]))

voted = not is_substring(content, search_strings['voted'][0])

rating = find_between(content, search_strings['rating'][0], search_strings['rating'][1])

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

year = find_between(content, search_strings['year'][0], search_strings['year'][1])
if(not year is None):
    year = clean(find_between(year, search_strings['year'][2], search_strings['year'][3]))


print(browser_title)
print(original_title)
print(released)
print(duration)
print(voted)
print(rating)
print(num_votes)
print(is_series)
print(year)