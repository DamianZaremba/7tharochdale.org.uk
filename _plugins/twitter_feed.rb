module Jekyll
	class TwitterFeed < Liquid::Tag
		def initialize(tag_name, username, tokens)
			super
			@username = username.gsub(/"/, '\"').rstrip
		end

		def render(context)
			'<script type="text/javascript">' + 
				'new TWTR.Widget({' +
					'version: 2,' +
					'type: "profile",' +
					'rpp: 10,' +
					'interval: 6000,' +
					'width: 250,' +
					'height: 300,' +
					'theme: {' +
						'shell: {' +
							'background: "#4d2177",' +
							'color: "#ffffff"' +
						'},' +
						'tweets: {' +
							'background: "#4d2177",' +
							'color: "#ffffff",' +
							'links: "#83a40b"' +
						'}' +
					'},' +
					'features: {' +
						'scrollbar: true,' +
						'loop: true,' +
						'live: true,' +
						'hashtags: true,' +
						'timestamp: true,' +
						'avatars: true,' +
						'behavior: "all"' +
					'}' +
				'})' +
				'.render()' +
				'.setUser("' + @username + '")' +
				'.start();' +
			'</script>'
		end
	end
end

Liquid::Template.register_tag('twitter_feed', Jekyll::TwitterFeed)
