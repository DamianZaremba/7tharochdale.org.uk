7th A Rochdale Scout Group website
===================================

Not the official version but probably will be (maybe) if I ever get around to finishing it!

Requirements
------------
# Python
* Cheetah
* Image
* pyexif

# Ruby
* Jekyll
* rdiscount
* gsl

General
-------
The site uses Jekyll for transforming the source into the live site

Blog
------
Add stuff into the _posts folder, use ./doshit.py --new <title> to add a correctly formatted file

Gallery
-------
We build the gallery from the dir structure, some helpful notes are as follows:

## Templates
See the templates/ folder - we use cheetah and a little jekyll

## Albums
By default the album name is the album folder with "_" substituted for " "
If you want to display a different name then add it into << album dir >>/ALBUM_DESCRIPTION

## Images
To add a description to images add stuff into
<< image file >>-DESCRIPTION

To add author info add stuff into
<< image file >>-AUTHOR
