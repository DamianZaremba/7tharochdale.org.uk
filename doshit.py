#!/usr/bin/env python
import os
from Cheetah.Template import Template
from distutils import dir_util
import time
import Image
import argparse
import pyexif
import tempfile

# Path we store a copy of the live site in (saves huge bw and forcing pushes)
LIVE_SITE_PATH = os.path.realpath(os.path.join(
	os.path.dirname(__file__),
	"../", "7tharochdale-live"
))
#DOMAIN = "7tharochdale.org.uk"
DOMAIN = "http://7tharochdale.dev.nodehost.co.uk"

def setup(source_dir):
	'''
	Creates a temporary dir and chdir's into it.
	Use for running the dev server in a clean env
	Also does the code copy to save code dublication
	'''
	dir_path = tempfile.mkdtemp()
	if os.path.isdir(source_dir):
		dir_util.copy_tree(source_dir, dir_path)
	os.chdir(dir_path)
	return dir_path

def cleanup(dir_path):
	'''
	Cleans up the temporary dir as created by setup
	'''
	if os.path.isdir(dir_path):
		dir_util.remove_tree(dir_path)

def compile_site():
	'''
	Calls Jekyll to actually compile (transform) the source
	'''
	if os.path.isdir("_site"):
		os.removedirs("_site")

	fh = open('_config.yml', 'r+')
	config = ""

	for line in fh.readlines():
		(key, value) = line.split(':', 1)
		if key == "basedomain": continue
		config += "%s: %s\n" % (key, value)
	config += "basedomain: %s\n" % DOMAIN

	fh.write(config)
	fh.close()
	os.system("jekyll")

def handle_gallery(albums):
	'''
	Builds the Jekyll gallery templates from some cheetah templates
	'''
	for album in albums:
		write_album_index(albums, album)

		for image in albums[album]['images']:
			write_image_page(albums, album, image)

def write_album_index(albums, album):
	'''
	This generates a single album's index template for Jekyll
	'''
	if os.path.isfile('templates/album.tpl'):
		fh = open('templates/album.tpl', 'r')
		data = fh.read()
		fh.close()
	else:
		data = ''

	tdata = {
		'albums': albums,
		'album': album,
	}
	template = Template(data, tdata)
	album_path = os.path.realpath(os.path.join('content', 'gallery', album, 'index.html'))
	album_dir = os.path.realpath(os.path.join('content', 'gallery', album))

	if not os.path.isdir(album_dir):
		print "Creating '%s'" % album_dir
		os.makedirs(album_dir)

	print "Writing out '%s'" % album_path
	fh = open(album_path, 'w')
	fh.write(str(template))
	fh.close()

def write_image_page(albums, album, image):
	'''
	This generates an images Jekyll template
	'''
	if os.path.isfile('templates/image.tpl'):
		fh = open('templates/image.tpl', 'r')
		data = fh.read()
		fh.close()
	else:
		data = ''

	tdata = {
		'albums': albums,
		'album': album,
		'image': image,
	}
	template = Template(data, tdata)

	image_path = os.path.realpath(os.path.join('content', 'gallery', image + '.html'))
	print "Writing out '%s'" % image_path

	fh = open(image_path, 'w')
	fh.write(str(template))
	fh.close()

def build_gallery():
	'''
	This does all the name detection and directory transversal to build a dict
	of the gallery contents which is then used to actually write the templates
	'''
	print "Building gallery"
	os.chdir('content/assests/gallery/images/')
	albums = {}

	for root, subFolders, files in os.walk('.'):
		for folder in subFolders:
			# Figure out our relative dirs
			album_dir = os.path.join(root, folder)[2:]
			parent_album_dir = '/'.join(album_dir.split('/')[:-1])

			# Add the parent album dir to the albums if it doesn't exist
			if parent_album_dir not in albums:
					albums[parent_album_dir] = {
						"sub_albums": [], "images": {},
						"name": "Home", "parent_albums": [],
						"path": "", "parent_path": "",
					}

			# Add the album to the parent album's entry
			# only do this if they are different
			if album_dir != parent_album_dir:
				# Just in case...f
				if album_dir not in albums[parent_album_dir]["sub_albums"]:
					albums[parent_album_dir]["sub_albums"].append(album_dir)

			# Add the album to the albums if it doesn't exist
			if album_dir not in albums:
				albums[album_dir] = {"sub_albums": [], "images": {}}

			# Check if we need to figure out the name
			if "name" not in albums[album_dir]:
				# Check if there is an explicit name file
				album_name_file = os.path.realpath(os.path.join(album_dir, 'ALBUM_DESCRIPTION'))
				if os.path.isfile(album_name_file):
					fh = open(album_name_file, 'r')
					album_name = fh.read()
					fh.close()
				else:
					# Use magical guess work
					album_name = album_dir.split('/')[-1].replace('_', ' ')

				albums[album_dir]["name"] = album_name.strip()

			if "parent_path" not in albums[album_dir]:
				albums[album_dir]["parent_path"] = parent_album_dir

			if "parent_albums" not in albums[album_dir]:
				albums[album_dir]["parent_albums"] = []
				parts = parent_album_dir.split('/')
				i = len(parts)
				while i > 0:
					p = '/'.join(parts[:-i]).strip()
					print p
					if p != "":
						albums[album_dir]["parent_albums"].append(p)
					i -= 1

				if parent_album_dir != "":
					albums[album_dir]["parent_albums"].append(parent_album_dir)

		# Add all the image files to the gallery
		for f in files:
			# Get the real path + ext - this is used for generating the thumbs
			album_dir = root[2:]
			image_path = os.path.join(album_dir, f)
			basename, extension = os.path.splitext(image_path)

			# Figure out if we can support the format
			if extension.lower() in [".png", ".jpeg", ".jpg"]:
				# We fill this stuff in
				image_description = f
				image_author = 'Unknown'

				# Check if we even need to bother getting this image info
				if image_path not in albums[album_dir]["images"]:
					# Try and get the description file
					desc_path = os.path.realpath(os.path.join(image_path, '-DESCRIPTION'))
					if os.path.isfile(desc_path):
						fh = open(desc_path, 'r')
						image_description = fh.read()
						fh.close()
					else:
						# Try and get the EXIF comment
						try:
							image = pyexif.ExifEditor(real_path)
							image_description = image.getTag('Comment')
						except:
							pass

					# Try and read the authors file
					author_path = os.path.realpath(os.path.join(image_path, '-AUTHOR'))
					if os.path.isfile(author_path):
						fh = open(author_path, 'r')
						image_author = fh.read()
						fh.close()

				albums[album_dir]["images"][image_path] = {}
				albums[album_dir]["images"][image_path]["author"] = image_author
				albums[album_dir]["images"][image_path]["description"] = image_description

	os.chdir(TMP_DIR)
	handle_gallery(albums)

def build_thumbnails():
	'''
	This builds a thumbnail (or video still) for every item in the gallery
	'''
	for root, subFolders, files in os.walk('content/assests/gallery/images/'):
		for f in files:
			path = os.path.realpath(os.path.join(root, f))
			basename, extension = os.path.splitext(path)

			if extension.lower() in [".png", ".jpeg", ".jpg"]:
				new_path = path.replace('content/assests/gallery/images/', 'content/assests/gallery/image_thumbnails/', 1)
				image_dir = os.path.dirname(new_path)
				if not os.path.isdir(image_dir):
					os.makedirs(image_dir)

				print "Writing out thumbnail '%s'" % new_path
				try:
					image = Image.open(path)
					image.thumbnail((150, 150), Image.ANTIALIAS)
					image.save(new_path)
				except Exception, e:
					print e

	for root, subFolders, files in os.walk('content/assests/gallery/video/'):
		for f in files:
			path = os.path.realpath(os.path.join(root, f))
			basename, extension = os.path.splitext(path)

			if extension.lower() in [".flv", ".m4v", ".swf", ".mp4"]:
				new_path = path.replace('content/assests/gallery/video/', 'content/assests/gallery/video_splash/', 1)

				video_dir = os.path.dirname(new_path)
				if not os.path.isdir(video_dir):
					os.makedirs(video_dir)

				print "Writing out video splash '%s'" % new_path
				os.system("ffmpeg -i %s -r 1 -ss 00:00:05 -s 598x370 -an -qscale 1 %s.png" % (path, new_path))

def minify_assets():
	'''
	This strips down the css and js using yuicompressor
	'''
	for root, subFolders, files in os.walk('_site'):
		for f in files:
			path = os.path.realpath(os.path.join(root, f))
			basename, extension = os.path.splitext(path)

			if extension.lower() in [".js", ".css"]:
				os.system("java -jar ~/bin/yuicompressor-2.4.2.jar %s -o %s --charset utf-8" % (path, path))
			elif extension.lower() in [".png", ".jpeg", ".jpg"]:
				os.system("convert -quality 0 %s %s" % (path, path))

def push_site():
	'''
	This pushes the live site code to github
	'''
	if not os.path.isdir(LIVE_SITE_PATH):
		print "Bailing from deploy"
		return False

	print "Pushing to github"
	os.chdir(LIVE_SITE_PATH)
	os.system("find . -type f -not -path *.git/* -exec git add {} \;")
	os.system("git commit -am 'Adding latest code'")
	os.system("git push origin live")
	print "Push done!"

def clone_site():
	'''
	This clones the live site code into our live site path
	'''
	os.chdir(LIVE_SITE_PATH)
	os.system("git clone -b live ssh://git@github.com:22/DamianZaremba/7tharochdale.org.uk.git %s" % LIVE_SITE_PATH)
	os.system("git checkout live")
	os.chdir(TMP_DIR)

def pull_site():
	'''
	This pulls any changes into our live site path
	'''
	os.chdir(LIVE_SITE_PATH)
	os.system("git pull")
	os.chdir(TMP_DIR)

def run_server():
	'''
	This runs the dev server
	Note: misses any minification etc and just does the core functionality stuff
	'''
	print "Running server"
	build_gallery()
	build_thumbnails()

	if os.path.isdir("_site"):
		os.removedirs("_site")
	os.system("jekyll --auto --server")

def dev_to_live():
	'''
	This copies the code out of the _site folder into our live site path
	We don't transform into the live site path directory to stop Jekyll doing
	anything insane. Also rsync does a nice job of tidying.
	'''
	os.system("rsync -vr --delete --exclude='.git' '%s/_site/' '%s/'" % (TMP_DIR, LIVE_SITE_PATH))

def run_deploy():
	'''
	Runs a deployment to github
	Doesn't actually deploy the site but pushes the code into the live repo
	'''
	print "Running deploy"
	if os.path.isdir("_site"):
		os.system("rm -rf _site")

	if not os.path.isdir(LIVE_SITE_PATH):
		os.mkdir(LIVE_SITE_PATH)
		clone_site()

	pull_site()
	build_gallery()
	build_thumbnails()
	minify_assets()
	compile_site()
	dev_to_live()
	push_site()

def create_post(post_title):
	'''
	This creates a post with the correct name (the date)
	Much nicer to humans due to the way Jekyll handles dates
	'''
	name = "%s-%s.markdown" % (time.strftime("%Y-%m-%d"), post_title)
	file_path = os.path.join('content', '_posts', name.lower())

	if os.path.isfile('templates/post.tpl'):
		fh = open('templates/post.tpl', 'r')
		data = fh.read()
		fh.close()
	else:
		data = ''

	if os.path.isfile(file_path):
		print "Not overwriting %s" % file_path
		return

	print "Now edit: %s" % file_path
	data = data.replace('#{title}', post_title)
	fh = open(file_path, 'w')
	fh.write(data)
	fh.close()

if __name__ == "__main__":
	'''
	This just detects what options we have been give and determins what to do
	'''
	parser = argparse.ArgumentParser(description='Run commands related to deploying 7tharochdale.org.uk')
	parser.add_argument('-d', '--deploy', action='store_true', help='Run the deploy steps')
	parser.add_argument('-n', '--new', action='store', dest='new', help='Create a new post')

	base_dir = os.path.dirname(os.path.realpath(__file__))
	args = parser.parse_args()
	if args.deploy == True:
		TMP_DIR = setup(base_dir)
		run_deploy()
		cleanup(TMP_DIR)
	elif args.new:
		create_post(args.new)
	else:
		TMP_DIR = setup(base_dir)
		run_server()
		cleanup(TMP_DIR)
