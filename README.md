bynario
=======
Just random code from bynario.com

*  feedly_link_checker.py: Python3 script for cleaning up feedly subscriptions

  ```python
  $> python3 feedly_link_checker.py feedly.opml
  498 entries found in feedly.opml
  Name: Binary poetry, URL:http://engineering.peertransfer.com/rss, Error Code:404
  [...]
  Name: puttycyg project updates - Google Code, URL:http://code.google.com/feeds/p/puttycyg/updates/basic, Error Code:404
  59 wrong entries found
  Removing... http://engineering.peertransfer.com/rss
  [...]
  Removing... http://code.google.com/feeds/p/puttycyg/updates/basic
  Creating feedly.opml_clean file...
  ``` 

* portLocker.py: Python2 script for blocking/unblocking ports (iptables) via dropbox file (more info in http://bynario.com/blog/2014/10/18/python-port-locker-slash-unlocker/)

* bat_Network_manager: BAT windows file for handling network configurations in Windows (more info in http://bynario.com/blog/2014/02/16/cmd-network-managing/)

* GPS_tags_to_google_map.py: Given a directory with NEF files, the script will extract the dates and GPS coordinates, will add a marker in a GMap and print the HTML code.

* DHT22tosqlite.py: Checking the DHT22 sensor and storing the data in SQLlite

* embedding_pexpect.py: Minimal pexpect module code embedded in a python script (base64)

* geolocation_tags.py: Extract GPS tags from a image (exif data)

* spotify_playlist.py: getting URI data from Spotify API 

* handle_tv_shows.py: Moving mp4 tv shows to folders based on name and season

* dropbox_gpg_magic_folder.py: (Prototype) Using gnupg, encrypt and decrypt files 

*	tiny_tcp_port_scanner.py: Small script for scanning open tcp ports in a hosts (because nmap is not always an option)

* GPS_tags_to_google_map.py: extract GPS tags from a list of photos and plot them in a google map

* simple_vinegere_cipher.py & simple_vinegere_cipher_decoder.py: Vinegere ciphers in python using Vigenere square
