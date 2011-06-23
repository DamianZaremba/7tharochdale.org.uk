---
layout: default
title: "Gallery - #if $albums[$image['album']]['name'] != '' then $albums[$image['album']]['name'] else '' #
 #if $image['desc'] and $image['desc'] != '' then ' - ' + $image['desc'] else '' #
---

<div class="gallery_single">
<img src="$image['image_url']" alt="$image['desc']" />
<p class="description">Description: $image['desc']</p>
<p class="author">Author: $image['author']</p>
<p class="linkback">Back to <a href="$albums[$image['album']]['url']">$albums[$image['album']]['name']</a></p>
</div>

<div id="comments">
<script type="text/javascript">fb_like('{{ site.basedomain }}{{ page.url }}');</script>
<div id="disqus_thread"></div>
<script type="text/javascript">
	var disqus_shortname = '7tharochdale';
	var disqus_identifier = '{{ page.url }}';
	var disqus_url = '{{ site.basedomain }}{{ page.url }}';
	(function() {
		var dsq = document.createElement('script');
		dsq.type = 'text/javascript';
		dsq.async = true;
		dsq.src = 'http://' + disqus_shortname + '.disqus.com/embed.js';

		(document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
	})();
</script>
</div>
