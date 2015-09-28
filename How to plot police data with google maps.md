# How To: Plot Crime Data with Google Maps

## Step 1: Get the data,

I’m using the https://data.polic.uk api to get my data, the documentation for it you can find at https://data.police.uk/docs/ 

e.g.  if you put https://data.police.uk/api/crimes-street/all-crime?lat=52.629729&lng=-1.131592&date=2013-01 in your web browser this will give you all the crime that occurred at the latitude, longitude and date specified in the URL string.

## Step 2: Create a HTML file

```
<!DOCTYPE html>
<html>
  <head>
    <style>
      #map {
      width: 500px;
      height: 400px;
      }
    </style>
    <script src="https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=visualization"></script>
    <script>
      function initialize() {
        console.log("initialize()");
        var mapCanvas = document.getElementById('map');
        var mapOptions = {
          center: new google.maps.LatLng(44.5403, -78.5463),
          zoom: 8,
          mapTypeId: google.maps.MapTypeId.ROADMAP,
        }
        var map = new google.maps.Map(mapCanvas, mapOptions)

        data = [{"category":"anti-social-behaviour","location_type":"Force","location":{"latitude":"52.635598","street":{"id":883314,"name":"On or near\
 Yeoman Lane"},"longitude":"-1.129330"},"context":"","outcome_status":null,"persistent_id":"","id":20597163,"location_subtype":"","month":"2013-01"},\
{"category":"anti-social-behaviour","location_type":"Force","location":{"latitude":"52.624919","street":{"id":882317,"name":"On or near Coniston Aven\
ue"},"longitude":"-1.141892"},"context":"","outcome_status":null,"persistent_id":"","id":20608551,"location_subtype":"","month":"2013-01"},{"category\
":"anti-social-behaviour","location_type":"Force","location":{"latitude":"52.641139","street":{"id":884319,"name":"On or near Toronto Close"},"longit\
ude":"-1.122481"},"context":"","outcome_status":null,"persistent_id":"","id":20597984,"location_subtype":"","month":"2013-01"},{"category":"anti-soci\
al-behaviour","location_type":"Force","location":{"latitude":"52.637600","street":{"id":883324,"name":"On or near St Peters Lane"},"longitude":"-1.13\
5171"},"context":"","outcome_status":null,"persistent_id":"","id":20597945,"location_subtype":"","month":"2013-01"},{"category":"anti-social-behaviou\
r","location_type":"Force","location":{"latitude":"52.621287","street":{"id":882350,"name":"On or near Sports\/recreation Area"},"longitude":"-1.1368\
81"},"context":"","outcome_status":null,"persistent_id":"","id":20597937,"location_subtype":"","month":"2013-01"}];

        var points = [];
        for(i=0; i<data.length; i++){
          points.push(new google.maps.LatLng(data[i].location.latitude, data[i].location.longitude));
          map.setCenter(points[i]);
        }

        console.log(points);

        heatmap = new google.maps.visualization.HeatmapLayer({
          data: points,
          map: map
        });

        heatmap.set('radius', 20);
      }
      
      google.maps.event.addDomListener(window, 'load', initialize);
    </script>
  </head>
  <body>
    <div id="map"></div>
  </body>
</html>
```
## Breakdown
```
<script src="https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=visualization"></script>
```
You need this to use the google maps api. The `?v=3.exp&libraries=visualization` bit is optional but it's needed for doing heat maps.

```
function initialize()
```
This function basically does everything, sets up the map, adds the data in to it.

```
data = [{"category":"anti ...
```
I've just literally copy and pasted some of the data I got from step 1 into my HTML file. 

```
var points = [];
for(i=0; i<data.length; i++){
  points.push(new google.maps.LatLng(data[i].location.latitude, data[i].location.longitude));
  map.setCenter(points[i]);
}
```
Convert the data from the po po (which is in the form of JSON) into a format that the google maps api can use.

```
heatmap = new google.maps.visualization.HeatmapLayer({ ...
```
creates the heat map object

```
google.maps.event.addDomListener(window, 'load', initialize);
```
This bit is needed to call the `initialize` function as well as do all clever google things in the background so you can zoom, pinch, squeeze and all that stuff with google maps.

That's it, you should end up with something like this,
![Image of Po Po data]
(https://github.com/dvoong/peacehack/blob/master/peacehack/static/Screen%20Shot%202015-09-28%20at%2012.53.56.png)

## Extras
So copying and pasting your data from a webpage is not very dynamic, you may want to use some sort of content management system (CMS) to do that for you. That's what I did with Django, a CMS built with Python but for the sake of simplicity I left that all out. Feel free to look around this repo if you're curious. Basically there are two main components to it, a python function and a HTML template. The python function is,
```
import requests
def home(request):
    response = requests.get('https://data.police.uk/api/crimes-street/all-crime?lat=52.629729&lng=-1.131592&date=2013-01')
    entries = response.json()[:]
    return render(request, 'home.html', {'entries': entries})
```
This gets the data from the police api, converts it to a python dictionary and then combines that with a HTML template. You can imagine in your HTTP request you could include arguments like dates, locations, categories of crime to filter your results. The template looks like,

```
<html>
  <head>
    <style>
      #map {
      width: 500px;
      height: 400px;
      }
    </style>
    <script src="https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=visualization"></script>
    <script>
      function initialize() {
        console.log("initialize()");
        var mapCanvas = document.getElementById('map');
        var mapOptions = {
          center: new google.maps.LatLng(44.5403, -78.5463),
          zoom: 8,
          mapTypeId: google.maps.MapTypeId.ROADMAP,
        }
        var map = new google.maps.Map(mapCanvas, mapOptions)
        console.log(map);
        <!-- Here I was playing around with markers instead of a heat map -->
        <!-- for entry in entries %} -->
        <!-- vanr myLatLng = {lat: {{ entry.location.latitude }}, lng: {{ entry.location.longitude }} }; -->
        <!-- var marker = new google.maps.Marker({ -->
        <!--   position: myLatLng, -->
        <!--   map: map, -->
        <!--   title: 'Hello World!' -->
        <!-- }); -->
        <!-- endfor %} -->
        <!-- map.setCenter(marker.getPosition()); -->
        function getPoints() {
          output = [];
          {% for entry in entries %}
          latlng = new google.maps.LatLng({{ entry.location.latitude }}, {{ entry.location.longitude }})
          output.push(latlng)
	        {% endfor %}
	        map.setCenter(latlng);
          return output;
        }
        
        heatmap = new google.maps.visualization.HeatmapLayer({
        data: getPoints(),
        map: map
          });
          heatmap.set('radius', 20);
      
        }
        google.maps.event.addDomListener(window, 'load', initialize);
    </script>
  </head>
  <body>
    <div id="map"></div>
  </body>
</html>
```

See the bits with the `{%`, `{{` type things, those are commands to the template on where to make substitutions with data from the python dictionary. Message me if you need any more details, I glossed over quite a few things.
