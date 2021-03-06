from flask import Flask, render_template, request
# import twitter_framework
import random
import string
from read_database import read_data
import json
import time
"""
This is the server, first you have to run this code, then you can view the website
by going to your browser and entering: localhost:5000
Be aware that if you make changes, you first have to stop the server with CRTL+C and
then run the server again, otherwise you get an error "address already in use" and then
you have to quit Python.
"""

def hashtag():
    print "Maussaus"

app = Flask(__name__)

# Open the index.html to find the comment that has to be replaced with a script
f = open('templates/index.html')
index = f.read()
f.close()
exclude = set(string.punctuation)


# Generate the script that should replace the comment in index.html
def generate_marker_js(lat, lng, query, message,timestamp, geo):
    # Every marker should have its unique id
    rand = random.randint(0, 100000)
    #Strip the messages from interpunction and line breaks (JS cannot handle most interpunctions)
    query = ''.join(ch for ch in query if ch not in exclude)
    message = ''.join(ch for ch in message if ch not in exclude)
    geo = ''.join(ch for ch in geo if ch not in exclude)
    query = query.replace('\n', ' ').replace('\r', '')
    message = message.replace('\n', ' ').replace('\r', '')

    t = time.strptime(timestamp, "%Y-%m-%d %H:%M")
    t = time.mktime(t) * 1000


    return """ var contentString_%d = '<div id="content">'+
            '<div id="siteNotice">'+
            '</div>'+
            '<h3 id="firstHeading" class="firstHeading"> %s </h3>'+
            '<div id="bodyContent">'+
            '<p> %s </p>'+
            '</div>'+
            '</div>';

            var infowindow_%d = new google.maps.InfoWindow({
            content: contentString_%d
            });

            var marker_%d = new google.maps.Marker({
            position: {lat: %f, lng: %f},
            map: map,
            title: '%s'
            });
            marker_%d.addListener('mouseover', function() {
            infowindow_%d.open(map, marker_%d);
            });

            // hide infowindow
            marker_%d.addListener('mouseout', function() {
                infowindow_%d.close(map, marker_%d);;
            });
            timestampArray.push([new Date(%d),"%s"]);
            """ % (rand, query, message, rand, rand, rand, lat, lng, query, rand, rand, rand,rand,rand,rand,t,geo) 

# Find the geo locations and messages from the tweets and send them to the client
def place_markers(index, query='#MakeAmericaGreatAgain'):


    marker_scripts_list = []
    for tweet in read_data():
        if tweet[10] == None:
            continue

        latitude = tweet[10][0]
        longitude = tweet[10][1]
        message = tweet[4]
        date = tweet[1]
        hashtags = tweet[7]
        geo = tweet[5]


        marker_scripts_list += [generate_marker_js(latitude, longitude, hashtags, message, date, geo)]
        

    marker_script = '\n'.join(marker_scripts_list)

    
    #timestamp_list = []
    #for tweet in tweets:
    #    if tweet['location'] != None:
    #        timestamp_list.append(tweet['timestamp'])
    #allstamps = ""
    #for timestamp in timestamp_list:
    #    allstamps += 'timestampArray.push(new Date("'+timestamp+'"));'
    
    index = index.replace("// place_markers_here", marker_script)
    index = index.replace(" <!--Current query-->", query)
    
    return index

index = place_markers(index)

def get_query_index(index, query = "#MakeAmericaGreatAgain"):
    index = place_markers(index, query)
    return index

# Start server
@app.route("/", methods=['POST', 'GET'])
def main():
    return index

@app.route('/query', methods=['POST', 'GET'])
def query():
    query=request.form['query']
    # Open the index.html to find the comment that has to be replaced with a script
    f = open('templates/index.html')
    index = f.read()
    f.close()
    exclude = set(string.punctuation)
    if(query[0] != "#"):
        print query
        print query[0]
        query = "#" + query
        print query
        
    index = get_query_index(index,query)
    return index

if __name__ == "__main__":
    app.run()
