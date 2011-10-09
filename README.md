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
To add stuff into the _posts folder, use ./doshit.py --new <title> so the created file is correctly formatted.
Once the file is added you may edit it as usual, the only required part is the header is as follows:
    layout: post
    title: <new post title>
    author: <authors name>
    tags: <list of post tags>

The header is YAML formatted.

Gallery
-------
We build the gallery from the dir structure, some helpful notes are as follows:

## Templates
See the templates/ folder - we use cheetah to build the templates for jekyll to transform.

## Albums
By default the album name is the album folder with "_" substituted for " "
If you want to display a different name then add it into a file called ALBUM_DESCRIPTION in the albums folder

## Images
To add a description to images add stuff into a file called $image_file_name-DESCRIPTION

To add author info add stuff into $image_file_name-DESCRIPTION
