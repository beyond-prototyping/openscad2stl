openscad2stl
============

Simple web service to convert [OpenSCAD](http://openscad.org/) files to [STL](http://en.wikipedia.org/wiki/STL_%28file_format%29).


Installation
------------

As a [docker](http://docker.io/) container:

    $ ID=$(docker run -p 5000 -d philippbosch/openscad2stl)
    $ docker port $ID 5000
    0.0.0.0:99999

The last command outputs the port (99999) that is bridged to the web server running inside the container.


Usage
-----

Either use the form on http://yourhost:99999/ (replace port number) or use curl, e.g.:

    $ curl -X POST -F file=@/Applications/OpenSCAD.app/Contents/Resources/examples/example001.scad http://yourhost:9999/ > example001.stl


