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
	sh "rm -rf /tmp/7tharochdale.org.uk/"
end

task :generate_gallery do
	Dir.chdir("/tmp/7tharochdale.org.uk/")
	images = {}
	base_url = "http://7tharochdale.org.uk.dev.nodehost.co.uk"
	thumbnail_url = "/assests/gallery/image_thumbnails"
	gallery_url = "/assests/gallery/images"

	Dir['content/assests/gallery/images/**/*.png', 'content/assests/gallery/images/**/*.jp*g'].each do |file|
		img = file.sub("content/assests/gallery/images/", "")
		dir = File.dirname(img)
		ext = File.extname(file)

		if ext == ".png"
			image = EXIFR::PNG.new(file)
		elsif ext == ".jpeg" or ext == ".jpg"
			image = EXIFR::JPEG.new(file)
		end

		description = image.comment
		if description == nil
			description = ""
		end


		images[dir] = {}
		images[dir]['url'] = base_url + gallery_url + dir
		images[dir]['desc'] = description
		images[dir]['thumb'] = base_url + thumbnail_url + dir

		sh "mkdir -p content/gallery/#{dir}"

		f = <<EOS
------------
layout: gallery/single
title: #{description}
------------

<div class="gallery_single">
	<img src="#{base_url}/#{thumbnail_url}/#{img}" alt="#{description}" />
	<p class="description">#{description}</p>
</div>

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
EOS

	end

	#puts "--> #{data}"
	HDATA = ""
	images.each do |album, image|
		HDATA << "  #{album}"
	end
	puts "#{HDATA}"
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
