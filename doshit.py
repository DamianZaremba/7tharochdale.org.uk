#!/usr/bin/env python
import os
from Cheetah.Template import Template
from distutils import dir_util
import time
import Image
import argparse
import pyexif
import tempfile

def setup(source_dir):
	dir_path = tempfile.mkdtemp()
	if os.path.isdir(source_dir):
		dir_util.copy_tree(source_dir, dir_path)
	os.chdir(dir_path)
	return dir_path

def cleanup(dir_path):
	if os.path.isdir(dir_path):
		dir_util.remove_tree(dir_path)

def compile_site():
	if os.path.isdir("_site"):
		os.removedirs("_site")
	os.system("jekyll")

def handle_gallery(albums):
	write_gallery_index(albums, albums[''])

	for album in albums:
		write_album_index(albums, albums[album])

		for image in albums[album]['images']:
			write_image_page(albums, albums[album]['images'][image])

def write_gallery_index(albums, album_data):
	if os.path.isfile('templates/album.tpl'):
		fh = open('templates/album.tpl', 'r')
		data = fh.read()
		fh.close()
	else:
		data = ''

	tdata = {
		'albums': albums,
		'album': album_data,
	}
	template = Template(data, tdata)
	album_path = os.path.realpath(os.path.join('content', 'gallery.html'))
	album_dir = os.path.realpath(os.path.join('content', 'gallery'))

	if not os.path.isdir(album_dir):
		print "Creating '%s'" % album_dir
		os.makedirs(album_dir)

	print "Writing out '%s'" % album_path
	fh = open(album_path, 'w')
	fh.write(str(template))
	fh.close()

def write_album_index(albums, album_data):
	if os.path.isfile('templates/album.tpl'):
		fh = open('templates/album.tpl', 'r')
		data = fh.read()
		fh.close()
	else:
		data = ''

	tdata = {
		'albums': albums,
		'album': album_data,
	}
	template = Template(data, tdata)
	album_path = os.path.realpath(os.path.join('content', 'gallery', album_data['path'] + '.html'))
	album_dir = os.path.realpath(os.path.join('content', 'gallery', album_data['path']))

	if not os.path.isdir(album_dir):
		print "Creating '%s'" % album_dir
		os.makedirs(album_dir)

	print "Writing out '%s'" % album_path
	fh = open(album_path, 'w')
	fh.write(str(template))
	fh.close()

def write_image_page(albums, image_data):
	if os.path.isfile('templates/image.tpl'):
		fh = open('templates/image.tpl', 'r')
		data = fh.read()
		fh.close()
	else:
		data = ''

	tdata = {
		'albums': albums,
		'image': image_data,
	}
	template = Template(data, tdata)

	image_path = os.path.realpath(os.path.join('content', 'gallery', image_data['album'], image_data['name'] + '.html'))
	print "Writing out '%s'" % image_path

	fh = open(image_path, 'w')
	fh.write(str(template))
	fh.close()

def build_gallery():
	print "Building gallery"
	os.chdir('content/assests/gallery/images/')
	albums = {}

	albums[""] = {}
	albums[""]["images"] = {}
	albums[""]["name"] = ""
	albums[""]["path"] = ''
	albums[""]["sub_albums"] = []
	albums[""]["url"] = '{{ site.basedomain }}/assests/gallery'

	for root, subFolders, files in os.walk('.'):
		for folder in subFolders:
			album_dir = os.path.join(root, folder)
			if album_dir[0:2] == "./": album_dir = album_dir[2:]
			if album_dir[0:1] == ".": album_dir = album_dir[1:]

			parent_album_dir = os.path.relpath(os.path.join(album_dir, ".."))
			if parent_album_dir[0:2] == "./": parent_album_dir = parent_album_dir[2:]
			if parent_album_dir[0:1] == ".": parent_album_dir = parent_album_dir[1:]

			album_name_file = os.path.realpath(os.path.join(album_dir, 'ALBUM_DESCRIPTION'))
			if os.path.isfile(album_name_file):
				fh = open(album_name_file, 'r')
				album_name = fh.read()
				fh.close()
			else:
				album_name = album_dir.split('/')[-1].replace('_', ' ')

			parent_album_name_file = os.path.realpath(os.path.join(album_dir, 'ALBUM_DESCRIPTION'))
			if os.path.isfile(parent_album_name_file):
				fh = open(parent_album_name_file, 'r')
				parent_album_name = fh.read()
				fh.close()
			elif parent_album_dir == "":
				parent_album_name = "Gallery"
			else:
				parts = parent_album_dir.split('/')
				parent_album_name = parts[-1].replace('_', ' ')

			if parent_album_dir not in albums:
				albums[parent_album_dir] = {}
				albums[parent_album_dir]["images"] = {}
				albums[parent_album_dir]["sub_albums"] = []
			albums[parent_album_dir]["sub_albums"].append(album_dir)

			if album_dir not in albums:
				albums[album_dir] = {}
				albums[album_dir]["images"] = {}
				albums[album_dir]["sub_albums"] = []

			albums[album_dir]["name"] = album_name.strip()
			albums[album_dir]["path"] = album_dir
			albums[album_dir]["url"] = '{{ site.basedomain }}/gallery/%s' % album_dir
			albums[album_dir]["parent"] = parent_album_name.strip()
			albums[album_dir]["parent_url"] = '{{ site.basedomain }}/gallery/%s' % parent_album_dir

		for f in files:
			real_path = os.path.join(root, f)
			basename, extension = os.path.splitext(real_path)

			if extension.lower() in [".png", ".jpeg", ".jpg"]:
				album_dir = os.path.dirname(real_path)
				if album_dir[0:2] == "./": album_dir = album_dir[2:]
				if album_dir[0:1] == ".": album_dir = album_dir[1:]

				image_description = ''
				image_author = 'Unknown'

				desc_path = os.path.realpath(os.path.join(real_path, '-DESCRIPTION'))
				if os.path.isfile(desc_path):
					fh = open(desc_path, 'r')
					image_description = fh.read()
					fh.close()

				if image_description == '':
					try:
						image = pyexif.ExifEditor(real_path)
						image_description = image.getTag('Comment')
					except:
						pass

				author_path = os.path.realpath(os.path.join(real_path, '-AUTHOR'))
				if os.path.isfile(author_path):
					fh = open(author_path, 'r')
					image_author = fh.read()
					fh.close()

				image_path = real_path
				if image_path[0:2] == "./": image_path = image_path[2:]

				if album_dir not in albums:
					albums[album_dir] = {}
					albums[album_dir]["images"] = {}
					albums[album_dir]["sub_albums"] = []

				albums[album_dir]["images"][image_path] = {}
				albums[album_dir]["images"][image_path]["album"] = album_dir
				albums[album_dir]["images"][image_path]["author"] = image_author
				albums[album_dir]["images"][image_path]["url"] = '{{ site.basedomain }}/gallery/%s' % image_path
				albums[album_dir]["images"][image_path]["image_url"] = '{{ site.basedomain }}/assests/gallery/images/%s' % image_path
				albums[album_dir]["images"][image_path]["thumbnail_url"] = '{{ site.basedomain }}/assests/gallery/image_thumbnails/%s' % image_path
				albums[album_dir]["images"][image_path]["desc"] = image_description
				albums[album_dir]["images"][image_path]["name"] = os.path.basename(real_path)

	os.chdir('../../../../')
	handle_gallery(albums)

def build_thumbnails():
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
	for root, subFolders, files in os.walk('_site'):
		for f in files:
			path = os.path.realpath(os.path.join(root, f))
			basename, extension = os.path.splitext(path)

			if extension.lower() in [".js", ".css"]:
				os.system("java -jar ~/bin/yuicompressor-2.4.2.jar %s -o %s --charset utf-8" % (path, path))
			elif extension.lower() in [".png", ".jpeg", ".jpg"]:
				os.system("convert -quality 0 %s %s" % (path, path))

def deploy():
	if not os.path.isdir("_site"):
		print "Bailing from deploy"
		return False

	print "Pushing to github"
	os.chdir("_site")
	os.system("git init")
	os.system("git add *")
	os.system("git commit -am 'Adding latest code'")
	os.system("git branch live")
	os.system("git checkout live")
	os.system("git remote add origin git@github.com:DamianZaremba/7tharochdale.org.uk.git")
	os.system("git push origin live --force")
	os.chdir("../")

def run_server():
	print "Running server"
	build_gallery()
	build_thumbnails()

	if os.path.isdir("_site"):
		os.removedirs("_site")
	os.system("jekyll --auto --server")

def run_deploy():
	print "Running deploy"
	if os.path.isdir("_site"):
		os.removedirs("_site")

	build_gallery()
	build_thumbnails()
	minify_assets()
	compile_site()
	deploy()

def create_post(post_title):
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
	parser = argparse.ArgumentParser(description='Run commands related to deploying 7tharochdale.org.uk')
	parser.add_argument('-d', '--deploy', action='store_true', help='Run the deploy steps')
	parser.add_argument('-n', '--new', action='store', dest='new', help='Create a new post')

	base_dir = os.path.dirname(os.path.realpath(__file__))
	args = parser.parse_args()
	if args.deploy == True:
		tmp_dir = setup(base_dir)
		run_deploy()
		cleanup(tmp_dir)
	elif args.new:
		create_post(args.new)
	else:
		tmp_dir = setup(base_dir)
		run_server()
		cleanup(tmp_dir)
