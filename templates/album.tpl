---
layout: default
title: "Gallery - #if $album['name'] != '' then $album['name'] else 'home' #"
---

#if ('images' in $album and len($album['images']) > 0) or ('sub_albums' in $album and len($album['sub_albums']) > 0):
#if len($album['images']) > 0:
<div class="gallery_album_images">
    <table>
    <tr>
    #set $i = 0

	#for $image in $album['images']
	<td>
	<a href="$album['images'][$image]['url']">
	<img src="$album['images'][$image]['thumbnail_url']" alt="$album['images'][$image]['name']" /></a>
	<p>$album['images'][$image]['desc']</p>
	</td>

	#if $i == 6:
	</tr><tr>
	#end if	
	#set $i += 1

    #end for
    </tr>
    </table>
    #if 'parent' in $album and 'parent_url' in $album:
	<p class="linkback">Back to <a href="$album['parent_url']">$album['parent']</a></p>
	#end if
</div>
#end if

#if 'sub_albums' in $album and len($album['sub_albums']) > 0:
<div class="gallery_album_subalbums">
    <h3>Albums</h3>
    <table>
    <tr>
    #set $i = 0

	#for $album in $album['sub_albums']
	<td>
	#set $image_keys = $albums[$album]['images'].keys()
	#if len($image_keys) > 0:
		#set $image_path = $image_keys[0]
	#else
		#set $image_path = False
	#end if

	#if $image_path:
		#set $image = $albums[$album]['images'][$image_path]
		<a href="$albums[$album]['url']" title="Gallery - $albums[$album]['url']"><img src="$image['thumbnail_url']" alt="$albums[$album]['name']" /></a>
		<p>$albums[$album]['name']</p>
	#else
		<a href="$albums[$album]['url']" title="Gallery - $albums[$album]['url']"><img src="{{ site.basedomain }}/assests/gallery/missing_image.png" alt="$albums[$album]['name']" /></a>
		<p>$albums[$album]['name']</p>
	#end if
	</td>

	#if $i == 6:
	</tr><tr>
	#end if

	#set $i += 1
    #end for
    </tr>
    </table>
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
#else
<p>No gallery stuff found, please check back later!</p>
#end if
