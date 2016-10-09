#!/usr/bin/env python
# Given a directory, the script will extract the dates and GPS coordinates, will add a marker in a Map and print the HTML file
# Dependencies: exifread
# Google Map API credential
import exifread,sys,glob

G_API_KEY = '<YOUR_GOOGLE_MAP_JS_API>'

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
    #Some more logic could be added here
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
        data = [path,"{0}".format(tags["EXIF DateTimeOriginal"]),formatme(tags["GPS GPSLatitude"],tags["GPS GPSLatitudeRef"]),formatme(tags["GPS GPSLongitude"], tags["GPS GPSLongitudeRef"]),id]

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

    #HTML code
    html="""<!DOCTYPE html><html><head><meta name="viewport" content="initial-scale=1.0, user-scalable=no"><meta charset="utf-8"><title>Route Map</title>
    <style>html, body {height: 100%;margin: 0; padding: 0; } #map { height: 100%; }    </style></head>    <body><div id="map"></div>"""

    html = html + """
    <script>
    function initMap()
    {
    var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 14, center: {lat: """ + str(captures[0][2]) + ",lng:" + str(captures[0][3])+ "}}); setMarkers(map);} var captures = ["

    for capture in captures:
        html = html + "".join("['" + str(capture[1]) + "'," + str(capture[2]) + "," + str(capture[3]) + "," + str(capture[4]) + "],") if "skip" not in capture else html

    html = html[:-1] + """]; function setMarkers(map)
    {
    for (var i = 0; i < captures.length; i++) {
    var capture = captures[i];
    var image = 'data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2238%22%20height%3D%2238%22%20viewBox%3D%220%200%2038%2038%22%3E%3Cpath%20fill%3D%22%23808080%22%20stroke%3D%22%23ccc%22%20stroke-width%3D%22.5%22%20d%3D%22M34.305%2016.234c0%208.83-15.148%2019.158-15.148%2019.158S3.507%2025.065%203.507%2016.1c0-8.505%206.894-14.304%2015.4-14.304%208.504%200%2015.398%205.933%2015.398%2014.438z%22%2F%3E%3Ctext%20transform%3D%22translate%2819%2018.5%29%22%20fill%3D%22%23fff%22%20style%3D%22font-family%3A%20Arial%2C%20sans-serif%3Bfont-weight%3Abold%3Btext-align%3Acenter%3B%22%20font-size%3D%2212%22%20text-anchor%3D%22middle%22%3E' + capture[3] + '%3C%2Ftext%3E%3C%2Fsvg%3E';
    var marker = new google.maps.Marker({
    position: {lat: capture[1], lng: capture[2]},map: map,icon: image,title: capture[0],zIndex: capture[3]});}}</script>"""

    html = html + '<script async defer src="https://maps.googleapis.com/maps/api/js?key=' + G_API_KEY + '&signed_in=true&callback=initMap"></script></body></html>'

    print(html)
