import exifread,sys

def formatme(mydata,reference):
    coordenates=(str(mydata).replace("[","").replace("]","").replace(" ","").split(","))

    d=coordenates[0]
    m=coordenates[1]
    s=coordenates[2]

    ref = str(reference).strip()

    if "/" in d:
        d = int(d.split("/")[0]) / int(d.split("/")[1])
    else:
        d=int(d)

    if "/" in m:
        m = int(m.split("/")[0]) / int(m.split("/")[1])
    else:
        m=int(m)

    if "/" in s:
        s = int(s.split("/")[0]) / int(s.split("/")[1])
    else:
        s=int(s)

    coor = d + (m / 60.0) + (s / 3600.0)
    return coor if ref == "N" or ref == "E" else -coor

try:
    path=sys.argv[1]
except:
    print("Usage: " + sys.argv[0] + " <photo>")
    sys.exit(1)

#Get the EXIF tags
with open(path, 'rb') as f:
    tags = exifread.process_file(f,details=False)

if not tags:
    print("No GPS DATA available")
    sys.exit(0)
else:
    print("Latitude:",formatme(tags["GPS GPSLatitude"],tags["GPS GPSLatitudeRef"]))
    print("Longitude:",formatme(tags["GPS GPSLongitude"],tags["GPS GPSLongitudeRef"]))
    print("Altitude:",tags["GPS GPSAltitude"])
