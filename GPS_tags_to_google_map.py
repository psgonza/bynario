#!/usr/bin/env python
# Given a directory, the script will extract the dates and GPS coordinates, will add a marker in a Map and print the HTML file
# Dependencies: exifread
# Google Map API credentials
import exifread,sys,glob

G_API_KEY = '<GOOGLE_MAP_API_TOKEN>'

html="""<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <title>Complex icons</title>
    <style>
      html, body {
        height: 100%;
        margin: 0;
        padding: 0;
      }
      #map {
        height: 100%;
      }
    </style>
  </head>
  <body>
    <div id="map"></div>
    <script>

function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 10,
    center: {lat: xxxLATxxx, lng: xxxLONGxxx}
  });

  setMarkers(map);
}  

xxxCAPTURESxxx

function setMarkers(map) {
  for (var i = 0; i < captures.length; i++) {
    var capture = captures[i];
    var marker = new google.maps.Marker({
      position: { lat: capture[1], lng: capture[2] },
      map: map,
      title: capture[0],
      zIndex: capture[3]
    });
  }
}
    </script>
    <script async defer
        src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&signed_in=true&callback=initMap"></script>
  </body>
</html> """ 

def formatme(mydata,reference):
    coordenates=(str(mydata).replace("[","").replace("]","").replace(" ","").split(","))

    d=coordenates[0]
    m=coordenates[1]
    s=coordenates[2]
    
    ref = str(reference).strip()

    d = int(d.split("/")[0]) / int(d.split("/")[1]) if "/" in d else int(d)
    m = int(m.split("/")[0]) / int(m.split("/")[1]) if "/" in m else int(m)
    s = int(s.split("/")[0]) / int(s.split("/")[1]) if "/" in s else int(s)

    coor = d + (m / 60.0) + (s / 3600.0)
    return coor if ref == "N" or ref == "E" else -coor

def find_pics(pics_path):
    #Some more logic could be added here. Filtering by filetype, date, etc
    return glob.glob(pics_path + "/*")

def get_GPS_data(id,path):
    try:
        #Get the EXIF tags
        with open(path, 'rb') as f:
            tags = exifread.process_file(f,details=False)
    except Exception as e:
        data = ["skip"]

    #Check we got the GPS tag data
    if "GPS GPSLongitude" not in tags and "GPS GPSLongitudeRef" not in tags:
        data = ["skip"]
    else:
        data = [path,"{0}".format(tags["EXIF DateTimeOriginal"]),formatme(tags["GPS GPSLatitude"], \
                tags["GPS GPSLatitudeRef"]),formatme(tags["GPS GPSLongitude"], tags["GPS GPSLongitudeRef"]),id]

    return data

if __name__ == "__main__":
    try:
        path=sys.argv[1]
    except:
        print("Usage: " + sys.argv[0] + " <path>")
        sys.exit(1)

    #List of pictures to process
    pics_list=find_pics(path)

    #List of pics, dates, lat, long, id
    captures = [ get_GPS_data(_, pic) for _, pic in enumerate(pics_list) ]

    # Create the JS code with the list of coordenates
    html_loop = "var captures = ["
    for capture in captures:
        html_loop = html_loop + "".join("['" + str(capture[1]) + "'," + str(capture[2]) + "," + str(capture[3]) + \
                    "," + str(capture[4]) + "],\n") if "skip" not in capture else html_loop
    html_loop = html_loop[:-2] + "]; "
    
    #Update center LAT/LONG  coordenates
    html = html.replace("xxxLATxxx",str(captures[0][2]))
    html = html.replace("xxxLONGxxx",str(captures[0][3]))
    #Update list of points
    html = html.replace("xxxCAPTURESxxx",html_loop)
    #Update API KEY
    html = html.replace("YOUR_API_KEY",G_API_KEY)
    
    print(html)
