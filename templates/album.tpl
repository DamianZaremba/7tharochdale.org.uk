---
layout: default
title: "Gallery - #if $album['name'] != '' then $album['name'] else 'home' #"
---

<div class="gallery_album_images">
    <table>
	#for $image in $album['images']
	$album['images'][$image]['url']
    #end for
    </table>
    #if 'parent' in $album and 'parent_url' in $album:
	<p class="linkback">Back to <a href="$album['parent_url']">$album['parent']</a></p>
	#end if
</div>

#if 'sub_albums' in $album and len($album['sub_albums']) > 0:
<div class="gallery_album_subalbums">
    <h3>Sub albums</h3>
    #for $album in $album['sub_albums']
	$albums[$album]['name']
    #end for
</div>
#end if

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
