from flask import Flask, render_template, request
import twitter_framework
import random
import string

"""
This is the server, first you have to run this code, then you can view the website
by going to your browser and entering: localhost:5000
Be aware that if you make changes, you first have to stop the server with CRTL+C and
then run the server again, otherwise you get an error "address already in use" and then
you have to quit Python.
"""

app = Flask(__name__)

# Open the index.html to find the comment that has to be replaced with a script
f = open('templates/index.html')
index = f.read()
f.close()
exclude = set(string.punctuation)


# Generate the script that should replace the comment in index.html
def generate_marker_js(lat, lng, query, message,timestamp):
    # Every marker should have its unique id
    rand = random.randint(0, 100000)
    #Strip the messages from interpunction and line breaks (JS cannot handle most interpunctions)
    query = ''.join(ch for ch in query if ch not in exclude)
    message = ''.join(ch for ch in message if ch not in exclude)
    query = query.replace('\n', ' ').replace('\r', '')
    message = message.replace('\n', ' ').replace('\r', '')
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
            timestampArray.push([new Date("%s"),"%s"]);
            """ % (rand, query, message, rand, rand, rand, lat, lng, query, rand, rand, rand,rand,rand,rand,timestamp,message) 

# Find the geo locations and messages from the tweets and send them to the client
def place_markers(index, query='#SaySomethingGoodAboutTwitter'):
    tweets = twitter_framework.extract_tweets(query)
    print tweets[0]

    marker_scripts_list = [generate_marker_js(tweet['location'][0], tweet['location'][1], query, tweet['message'],tweet['timestamp']) for tweet in tweets if tweet['location'] != None]
    marker_script = '\n'.join(marker_scripts_list)

    
    #timestamp_list = []
    #for tweet in tweets:
    #    if tweet['location'] != None:
    #        timestamp_list.append(tweet['timestamp'])
    #allstamps = ""
    #for timestamp in timestamp_list:
    #    allstamps += 'timestampArray.push(new Date("'+timestamp+'"));'
    
    index = index.replace("// place_markers_here", marker_script)
    #index = index.replace("// place_scatterplot_here", allstamps)
    
    return index

index = place_markers(index)

# Start server
@app.route("/", methods=['POST', 'GET'])
def main():
    return index


if __name__ == "__main__":
    app.run()
