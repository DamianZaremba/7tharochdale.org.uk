---
layout: master
title: "Gallery ->#if len($albums[$album]['parent_albums']) > 0
	#for $a in $albums[$album]['parent_albums']
 $albums[$a]['name'] ->
	#end for
	#end if
$albums[$album]['name'] -> $albums[$album]['images'][$image]['description']"
---

<div class="gallery_single">
<img src="{{ site.basedomain }}/assests/gallery/images/$image" alt="$albums[$album]["images"][$image]['description']" />
<p class="description">Description: $albums[$album]["images"][$image]['description']</p>
<p class="author">Author: $albums[$album]["images"][$image]['author']</p>
<p class="linkback">Back to <a href="{{ site.basedomain }}/gallery/$album">Gallery ->
#if len($albums[$album]['parent_albums']) > 0
	#for $a in $albums[$album]['parent_albums']
		$albums[$a]['name'] ->
	#end for
#end if
$albums[$album]['name']</a></p>
</div>

<div id="comments">
{% like_buttons %}
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
