require 'date'
# What we need:
# Git, Java, Convert (Image magic)
# yuicompressor in ~/bin/yuicompressor-2.4.2.jar
#
# This is a very specific script to my setup and probably won't work for anyone else -
# I don't really plan to rewrite it to be so either.

desc "Compile"
task :default => [:compile]

desc "Compile site"
task :compile do
	sh "rm -rf _site"
	sh "jekyll"
end

task :push => [:compile, :minify_assests, :commit]
desc "Commit site"
task :commit do
	# This was all nicely using the git ruby stuff but it had major issues with branching so nvm
	Dir.chdir("../7tharochdale.org.uk-live")
	sh "git init"
	sh "git add *"
	sh "git commit -am 'Adding latest code (rake)'"
	sh "git branch live"
	sh "git checkout live"
	sh "git remote add origin git@github.com:DamianZaremba/7tharochdale.org.uk.git"
	sh "git push origin live --force"
	sh "rm -rf ../7tharochdale.org.uk-live"
end

task :server => [:run_server]
desc "Run local server"
task :run_server do
	sh "jekyll --auto --server"
	sh "rm -rf ../7tharochdale.org.uk-live"
end

task :minify => [:compile, :minify_assests]
desc "Minify assests"
task :minify_assests do
	Dir['../7tharochdale.org.uk-live/assests/**/*.js'].each do |js|
		sh "java -jar ~/bin/yuicompressor-2.4.2.jar #{js} -o #{js} --charset utf-8"
	end

	Dir['../7tharochdale.org.uk-live/assests/**/*.css'].each do |css|
		sh "java -jar ~/bin/yuicompressor-2.4.2.jar #{css} -o #{css} --charset utf-8"
	end

	Dir['../7tharochdale.org.uk-live/assests/**/*.png'].each do |img|
		sh "convert -quality 0 #{img} #{img}"
	end

	Dir['../7tharochdale.org.uk-live/assests/**/*.jp*g'].each do |img|
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