require 'date'
require 'rubygems'
require 'mini_magick'
require 'exifr'
# What we need:
# Git, Java, Convert (Image magic) exifr
# yuicompressor in ~/bin/yuicompressor-2.4.2.jar
#
# This is a very specific script to my setup and probably won't work for anyone else -
# I don't really plan to rewrite it to be so either.

desc "Compile"
task :default => [:prep, :generate_thumbs, :generate_gallery, :compile]

desc "Setup the env"
task :prep do
	puts "Starting prep"
	sh "rm -rf /tmp/7tharochdale.org.uk/"
	sh "mkdir -p /tmp/7tharochdale.org.uk/"
	sh "cp -r * /tmp/7tharochdale.org.uk/"
end

desc "Compile site"
task :compile do
	puts "Starting compile"
	Dir.chdir("/tmp/7tharochdale.org.uk/")
	sh "rm -rf _site"
	sh "jekyll"
end

task :push => [:prep, :generate_thumbs, :generate_gallery ,:compile, :minify_assests, :commit]
desc "Commit site"
task :commit do
	puts "Starting commit"
	# This was all nicely using the git ruby stuff but it had major issues with branching so nvm
	Dir.chdir("/tmp/7tharochdale.org.uk/_site/")
	sh "git init"
	sh "git add *"
	sh "git commit -am 'Adding latest code (rake)'"
	sh "git branch live"
	sh "git checkout live"
	sh "git remote add origin git@github.com:DamianZaremba/7tharochdale.org.uk.git"
	sh "git push origin live --force"
	sh "rm -rf /tmp/7tharochdale.org.uk/"
end

task :server => [:prep, :generate_thumbs, :generate_gallery, :run_server]
desc "Run local server"
task :run_server do
	puts "Starting server"
	Dir.chdir("/tmp/7tharochdale.org.uk/")
	sh "jekyll --auto --server"
	sh "rm -rf /tmp/7tharochdale.org.uk/"
end

task :generate_thumbs do
	puts "Starting thumb generation"
	Dir['/tmp/7tharochdale.org.uk/content/assests/gallery/images/**/*.png',
		'/tmp/7tharochdale.org.uk/content/assests/gallery/images/**/*.jp*g'].each do |img|
		begin
			image = MiniMagick::Image.open(img)
			image.resize "150X150"
			new_path = img.sub("/gallery/images/", "/gallery/image_thumbnails/")
			new_dir = File.dirname(new_path)
			sh "mkdir -p #{new_dir}"
			image.write(new_path)
		rescue
			next
		end
	end

	Dir['/tmp/7tharochdale.org.uk/content/assests/gallery/video**/*.flv',
		'/tmp/7tharochdale.org.uk/content/assests/gallery/video**/*.m4v',
		'/tmp/7tharochdale.org.uk/content/assests/gallery/video**/*.swf',
		'/tmp/7tharochdale.org.uk/content/assests/gallery/video**/*.mp4'].each do |video|
		new_path = video.sub("/gallery/video/", "/gallery/video_splash/")
		new_dir = File.dirname(new_path)
		sh "mkdir -p #{new_dir}"
		sh "ffmpeg -i #{video} -r 1 -ss 00:00:05 -s 598x370 -an -qscale 1 #{new_path}.png; exit 0"
	end
    
end

task :generate_gallery do
	puts "Starting gallery generation"
	Dir.chdir("/tmp/7tharochdale.org.uk/")
	albums = {}

	base_url = "{{ site.basedomain }}"
	thumbnail_url = "/assests/gallery/image_thumbnails"
	full_url = "/assests/gallery/images"
	gallery_path = "/gallery"

	Dir['content/assests/gallery/images/**/*'].each do |obj|
	if File.directory?(obj)
		dir = obj.sub("content/assests/gallery/images/", "")
		if albums[dir] == nil
		albums[dir] = {}
		albums[dir]["name"] = dir.sub("_", " ")
		albums[dir]["folder"] = dir
		albums[dir]["url"] = base_url + gallery_path + "/" + dir
		parent = dir.split("/")[0..-2].join("/")
		if parent == ""
			albums[dir]["parent"] = "Gallery"
			albums[dir]["parent_url"] = base_url + gallery_path
		else
			albums[dir]["parent"] = parent.sub("_", " ").sub(/^(\w)/) {|s| s.capitalize}
			albums[dir]["parent_url"] = base_url + gallery_path + "/" + parent
		end
		albums[dir]["images"] = {}
		end
		next
	end

	img = obj.sub("content/assests/gallery/images/", "")
	dir = File.dirname(img)
	name = File.basename(img)
	ext = File.extname(obj)

	begin
		if ext == ".png"
			image = EXIFR::PNG.new(obj)
		elsif ext == ".jpeg" or ext == ".jpg"
			image = EXIFR::JPEG.new(obj)
		else
			next # We don't support this
		end
	rescue
		next # error
	end

	description = image.comment
	if description == nil
		description = name
	end

	albums[dir]["images"][name] = {}
	albums[dir]["images"][name]['url'] = base_url + gallery_path + "/" + img
	albums[dir]["images"][name]['desc'] = description
	albums[dir]["images"][name]['name'] = name
	albums[dir]["images"][name]['gallery'] = dir
	albums[dir]["images"][name]['thumb'] = base_url + thumbnail_url + "/" + img

	sh "mkdir -p content/gallery/#{dir}"

	# Write out the sngle page (we deal with album indexes later)
	fdata = <<EOS
---
layout: default
title: #{description.sub(":", "")}
---

<div class="gallery_single">
<img src="#{base_url}/#{full_url}/#{img}" alt="#{description}" />
<p class="description">#{description}</p>
<p class="linkback">Back to <a href="#{base_url}/#{gallery_path}/#{dir}">#{dir}</a></p>
</div>

<div id="comments">
<script type="text/javascript">fb_like('{{ site.basedomain }}/{{ page.url }}');</script>
<div id="disqus_thread"></div>
<script type="text/javascript">
	var disqus_shortname = '7tharochdale';
	var disqus_identifier = '{{ page.url }}';
	var disqus_url = '{{ site.basedomain }}/{{ page.url }}';
	(function() {
		var dsq = document.createElement('script');
		dsq.type = 'text/javascript';
		dsq.async = true;
		dsq.src = 'http://' + disqus_shortname + '.disqus.com/embed.js';

		(document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
	})();
</script>
</div>
EOS

	# Write out this image index
	index_path = "content/#{gallery_path}/#{img}.html"
	fh = File.open(index_path, "w")
	fh.write(fdata)
	fh.close
	end

	## Now we loop over the album array and generate there indexes....
	albums.each do |i, album|
		adata = <<EOS
---
layout: default
title: Gallery #{album["name"]}
---

<div class="gallery_album_images">
EOS

		    # Build out the images list
		    images = album["images"]
		    x = 1
		    adata += "<table><tr>"
		    images.each do |i, image|
			if (x % 6) == 0
				adata += "</tr><tr>"
			end

			adata += <<EOS
			<td><a href="#{image["url"]}"><img src="#{image["thumb"]}" alt="#{image["desc"]}" /></a></td>
EOS
			x = x.succ
		    end
		    adata += "</tr></table>"

		adata += <<EOS
		<p class="linkback">Back to <a href="#{album["parent_url"]}">#{album["parent"]}</a></p>
</div>

EOS

		if Dir["content/#{gallery_path}/#{album["folder"]}/*"].reject{|o| not File.directory?(o)}.length > 0
		    adata += <<EOS
<div class="gallery_album_subalbums">
    <h3>Sub albums</h3>
EOS

		    # Build out the sub albums list
		    x = 1
		    Dir["content/#{gallery_path}/#{album["folder"]}/*"].reject{|o| not File.directory?(o)}.each do |dir|
			path = dir.sub("content/#{gallery_path}/", "")
			dname = path.split("/")[1..-1].join("/").sub("_", " ").sub(/^(\w)/) {|s| s.capitalize}
			if (x % 6) == 0
				adata += "</p><p>"
			end

			adata += <<EOS
				<p><a href="#{base_url}/#{gallery_path}/#{path}/">#{dname}</a></p>
EOS
			x.succ
		    end

		    adata += <<EOS
</div>
EOS
end

		    adata += <<EOS
<div id="comments">
	<script type="text/javascript">fb_like('{{ site.basedomain }}/{{ page.url }}');</script>
	<div id="disqus_thread"></div>
	<script type="text/javascript">
		var disqus_shortname = '7tharochdale';
		var disqus_identifier = '{{ page.url }}';
		var disqus_url = '{{ site.basedomain }}/{{ page.url }}';
		(function() {
			var dsq = document.createElement('script');
			dsq.type = 'text/javascript';
			dsq.async = true;
			dsq.src = 'http://' + disqus_shortname + '.disqus.com/embed.js';
	
			(document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
		})();
	</script>
</div>
EOS

		# Write the index page		
		index_path = "content/#{gallery_path}/#{album["folder"]}/index.html"
		index_dir = File.dirname(index_path)
		sh "mkdir -p #{index_dir}"
		fh = File.open(index_path, "w")
		fh.write(adata)
		fh.close
	end
	
	# Now write out teh final index - the gallery!
	adata = <<EOS
---
layout: default
title: Gallery
---

<div class="gallery_album_subalbums">
	<h3>Sub albums</h3>
	<p>
EOS

	x = 1
	Dir["content/#{gallery_path}/*"].reject{|o| not File.directory?(o)}.each do |dir|
		path = dir.sub("content/#{gallery_path}/", "")
		dname = path.sub("_", " ")
		if (x % 6) == 0
			adata += "</p><p>"
		end

		adata += <<EOS
		<a href="#{base_url}/#{gallery_path}/#{path}/">#{dname}</a>
EOS
		x.succ
	end
	adata += <<EOS
	</p>
</div>

<div id="comments">
	<script type="text/javascript">fb_like('{{ site.basedomain }}/{{ page.url }}');</script>
	<div id="disqus_thread"></div>
	<script type="text/javascript">
		var disqus_shortname = '7tharochdale';
		var disqus_identifier = '{{ page.url }}';
		var disqus_url = '{{ site.basedomain }}/{{ page.url }}';
		(function() {
			var dsq = document.createElement('script');
			dsq.type = 'text/javascript';
			dsq.async = true;
			dsq.src = 'http://' + disqus_shortname + '.disqus.com/embed.js';
	
			(document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
		})();
	</script>
</div>
EOS
	# Write the index page		
	index_path = "content/#{gallery_path}/index.html"
	fh = File.open(index_path, "w")
	fh.write(adata)
	fh.close
end

task :minify => [:compile, :minify_assests]
desc "Minify assests"
task :minify_assests do
	puts "Starting minify"
	Dir.chdir("/tmp/7tharochdale.org.uk/_site/")
	Dir['assests/**/*.js', 'assests/**/*.css'].each do |js|
		sh "java -jar ~/bin/yuicompressor-2.4.2.jar #{js} -o #{js} --charset utf-8"
	end
end

namespace "post" do
	desc "Given a title as an argument, create a new post file"
	task :new, [:title] do |t, args|
		now = DateTime::now()
		filename = "#{now.strftime '%Y-%m-%d'}-#{args.title.gsub(/[\s\W]/, '_').downcase}.markdown"
		path = File.join("content", "_posts", filename)

		if File.exist? path;
			raise RuntimeError.new("Won't overwrite path}");
		end

		File.open(path, 'w') do |file|
			file.write <<-EOS
---
layout: post
title: #{args.title}
tags: []
---

EOS
			end
	end
end