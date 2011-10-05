---
layout: master
title: "Gallery -> #if len($albums[$album]['parent_albums']) > 0
	#for $a in $albums[$album]['parent_albums']
		$a ->
	#end for
	#end if
$albums[$album]['name']"
---

#if (len($albums[$album]['images']) > 0) or (len($albums[$album]['sub_albums']) > 0):
#if len($albums[$album]['images']) > 0:
<div class="gallery_album_images">
    <table>
    <tr>
    #set $i = 0

	#for $image in $albums[$album]['images']
	<td>
	<a href="{{ site.basedomain }}/gallery/$image">
	<img src="{{ site.basedomain }}/assests/gallery/image_thumbnails/$image" alt="$albums[$album]['images'][$image]['description']" /></a>
	<p>$albums[$album]['images'][$image]['description']</p>
	</td>

	#if $i == 4:
	</tr><tr>
	#end if
	#set $i += 1

    #end for
    </tr>
    </table>
	<p class="linkback">Back to <a href="{{ site.basedomain }}/gallery/$albums[$album]['parent_path']">Gallery ->
	#if len($albums[$albums[$album]['parent_path']]['parent_albums']) > 0
		#for $a in $albums[$albums[$album]['parent_path']]['parent_albums']
			$a ->
		#end for
	#end if
	$albums[$albums[$album]['parent_path']]['name']</a></p>
</div>
#end if

#if len($albums[$album]['sub_albums']) > 0:
<div class="gallery_album_subalbums">
    <h3>Sub Albums</h3>
    <table>
    <tr>
    #set $i = 0

	#for $album in $albums[$album]['sub_albums']
	<td>
	#set $image_keys = $albums[$album]['images'].keys()
	#if len($image_keys) > 0:
		#set $image_path = $image_keys[0]
	#else
		#set $image_path = False
	#end if

	#if $image_path:
		<a href="{{ site.basedomain }}/gallery/$album" title="Gallery - $albums[$album]['name']">
			<img src="{{ site.basedomain }}/assests/gallery/image_thumbnails/$image_path" alt="Gallery - $albums[$album]['name']" />
		</a>
		<p>$albums[$album]['name']</p>
	#else
		<a href="{{ site.basedomain }}/gallery/$album" title="Gallery - $albums[$album]['name']">
			<img src="{{ site.basedomain }}/assests/gallery/missing_image.png" alt="Gallery - $albums[$album]['name']" />
		</a>
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
#else
<p>No gallery stuff found, please check back later!</p>
#end if
