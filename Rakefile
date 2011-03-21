require 'date'
require 'rubygems'
require 'exifr'
# What we need:
# Git, Java, Convert (Image magic) exifr
# yuicompressor in ~/bin/yuicompressor-2.4.2.jar
#
# This is a very specific script to my setup and probably won't work for anyone else -
# I don't really plan to rewrite it to be so either.

desc "Compile"
task :default => [:prep, :generate_gallery, :compile]

desc "Setup the env"
task :prep do
	sh "rm -rf /tmp/7tharochdale.org.uk/"
	sh "mkdir -p /tmp/7tharochdale.org.uk/"
	sh "cp -r * /tmp/7tharochdale.org.uk/"
end

desc "Compile site"
task :compile do
	Dir.chdir("/tmp/7tharochdale.org.uk/")
	sh "rm -rf _site"
	sh "jekyll"
end

task :push => [:prep, :generate_gallery ,:compile, :minify_assests, :commit]
desc "Commit site"
task :commit do
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

task :server => [:prep, :generate_gallery, :run_server]
desc "Run local server"
task :run_server do
	sh "jekyll --auto --server"
	#sh "rm -rf /tmp/7tharochdale.org.uk/"
end

task :generate_gallery do
	Dir.chdir("/tmp/7tharochdale.org.uk/")
	albums = {}
	base_url = "{{ site.basedomain }}"
	thumbnail_url = "/assests/gallery/image_thumbnails"
	gallery_url = "/assests/gallery/images"
	gallery_data = "/gallery"

	Dir['content/assests/gallery/images/**/*.png', 'content/assests/gallery/images/**/*.jp*g'].each do |file|
		img = file.sub("content/assests/gallery/images/", "")
		dir = File.dirname(img)
		name = img.sub(dir, "")
		ext = File.extname(file)
		index_path = "content/#{gallery_data}/#{img}.html"

		if ext == ".png"
			image = EXIFR::PNG.new(file)
		elsif ext == ".jpeg" or ext == ".jpg"
			image = EXIFR::JPEG.new(file)
		end

		description = image.comment
		if description == nil
			description = name
		end

		if albums[dir] == nil
		    albums[dir] = {}
		end
		albums[dir][name] = {}
		albums[dir][name]['url'] = base_url + gallery_data + "/" + img
		albums[dir][name]['desc'] = description
		albums[dir][name]['name'] = name
		albums[dir][name]['thumb'] = base_url + thumbnail_url + "/" + img

		sh "mkdir -p content/gallery/#{dir}"

		# Write out the sngle page (we deal with album indexes later)
		fdata = <<EOS
------------
layout: default
title: #{description}
------------

<div class="gallery_single">
	<img src="#{base_url}/#{gallery_url}/#{img}" alt="#{description}" />
	<p class="description">#{description}</p>
</div>

<div id="comments>
    <iframe src="http://www.facebook.com/plugins/like.php?href={{ site.basedomain }}/{{ page.url }}&amp;
    layout=standard&amp;show_faces=false&amp;width=450&amp;action=like&amp;font=verdana&amp;colorscheme=light&amp;"
    height=25" scrolling="no" frameborder="0" style="border:none; overflow:hidden; width:450px; height:35px;"
    allowTransparency="true"></iframe>
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

	    puts "Writing out image page (#{index_path})"
	    fh = File.open(index_path, "w")
	    fh.write(fdata)
	    fh.close
	end

	# Build up the ablum index the write it to disk
	albums.each do |album, images|
	    name = album.sub("_", " ")
	    dir = "content/#{gallery_data}/#{album}/"
	    adata = ""
	    adata += <<EOS
------------
layout: default
title: #{name}
------------

<div class="gallery_album_subalbums">
EOS

	    # Build out the sub albums list
	    Dir["content/#{gallery_data}/#{album}/*"].reject{|o| not File.directory?(o)}.each do |dir|
		path = dir.sub("content/#{gallery_data}/#{album}/", "")
		dname = path.sub("_", " ")
		adata += <<EOS
	    <p><a href="#{base_url}/#{gallery_data}/#{path}/">#{base_url}/#{gallery_data}/#{dname}/</a></p>
EOS
	    end

	    adata += <<EOS
</div>

<div class="gallery_album_images">
EOS

	    # Build out the images list
	    images.each do |name,image|
		adata += <<EOS
	    <p><a href="#{image["url"]}">#{image["thumb"]}</a><br />#{image["desc"]}</p>
EOS
	    end

	    adata += <<EOS
</div>

<div id="comments>
    <iframe src="http://www.facebook.com/plugins/like.php?href={{ site.basedomain }}/{{ page.url }}&amp;
    layout=standard&amp;show_faces=false&amp;width=450&amp;action=like&amp;font=verdana&amp;colorscheme=light&amp;"
    height=25" scrolling="no" frameborder="0" style="border:none; overflow:hidden; width:450px; height:35px;"
    allowTransparency="true"></iframe>
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
	    index_path = "content/#{gallery_data}/#{album}/index.html"
	    puts "Writing out album page (#{index_path})"
	    fh = File.open(index_path, "w")
	    fh.write(adata)
	    fh.close
	end
	
	# Write out the gallery index
	    adata = <<EOS
------------
layout: default
title: Gallery
------------

<div class="gallery_album_subalbums">
EOS

	Dir["content/#{gallery_data}/*"].reject{|o| not File.directory?(o)}.each do |dir|
	    path = dir.sub("content/#{gallery_data}/", "")
	    dname = path.sub("_", " ")
		adata += <<EOS
	    <p><a href="#{base_url}/#{gallery_data}/#{path}/">#{base_url}/#{gallery_data}/#{dname}/</a></p>
EOS
	end
	    adata += <<EOS
</div>

<div id="comments>
    <iframe src="http://www.facebook.com/plugins/like.php?href={{ site.basedomain }}/{{ page.url }}&amp;
    layout=standard&amp;show_faces=false&amp;width=450&amp;action=like&amp;font=verdana&amp;colorscheme=light&amp;"
    height=25" scrolling="no" frameborder="0" style="border:none; overflow:hidden; width:450px; height:35px;"
    allowTransparency="true"></iframe>
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
	    index_path = "content/#{gallery_data}/index.html"
	    puts "Writing out album page (#{index_path})"
	    fh = File.open(index_path, "w")
	    fh.write(adata)
	    fh.close
	end

task :minify => [:compile, :minify_assests]
desc "Minify assests"
task :minify_assests do
	Dir.chdir("/tmp/7tharochdale.org.uk/_site/")
	Dir['assests/**/*.js', 'assests/**/*.css'].each do |js|
		sh "java -jar ~/bin/yuicompressor-2.4.2.jar #{js} -o #{js} --charset utf-8"
	end

	Dir['assests/**/*.png', 'assests/**/*.jp*g'].each do |img|
		sh "convert -quality 0 #{img} #{img}"
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
title: #{args.title}
tags: []
---

EOS
			end
		puts "Created #{path}"
	end
end
