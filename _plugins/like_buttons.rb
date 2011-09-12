 module Jekyll
	class LikeButtons < Liquid::Tag
		def render(context)
			# G+
			'<g:plusone annotation="inline" href="' + 
			context['site']['basedomain'] + context['page']['url'] + '"></g:plusone>' +
			'<script type="text/javascript">window.___gcfg = {lang: "en-GB"};'+
			'(function() { var po = document.createElement("script");' +
			'po.type = "text/javascript"; po.async = true;' +
			'po.src = "https://apis.google.com/js/plusone.js";' +
			'var s = document.getElementsByTagName("script")[0]; ' +
			's.parentNode.insertBefore(po, s);' +
			'})();</script>' +

			# FB
			'<iframe src="http://www.facebook.com/plugins/like.php?href=' +
			context['site']['basedomain'] + context['page']['url'] +
			'&amp;layout=standard&amp;show_faces=false&amp;width=450&amp;action=like&amp;' +
			'font&amp;colorscheme=light&amp;height=35" scrolling="no" frameborder="0" style="border:' +
			'none; overflow:hidden; width:450px; height:35px;" allowTransparency="true"></iframe>' 
		end
	end
end

Liquid::Template.register_tag('like_buttons', Jekyll::LikeButtons)
