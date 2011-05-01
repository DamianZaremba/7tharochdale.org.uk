$(function(){
	$(".switch, .switch_hide").hide();
	$(".switch_unhide").show();
});

function preLoadImages(imageArray){
	$.each(imageArray, function (i, val) {
		/* Lets just make a new dom img object and set it's src to this value, the browser should then cache the image making the hover effects work nicely with no loading delay! */
		cacheImage = document.createElement('img').src = val;
	});
}

function switch_menu_image(item) {
	/* Hack! */
	image_parts = item.getAttribute('src').split('/');
	image_path = image_parts.splice(0, image_parts.length-1).join("/");
	image_name = image_parts[image_parts.length-1];

	if(image_name.split('depressed_').length == 2){ // We are the depressed image
		replace_image = image_path+'/'+image_name.split('depressed_')[1];
	}else{ // We are the happy image (ha!)
		replace_image = image_path+'/depressed_'+image_name;
	}
	item.src = replace_image;
}

function switcher(show_id) {
	var show = $("#" + show_id);
	if (show.length) {
		$(".switch").fadeOut("slow");

		if (show.is(":visible")){
			return true;
		} else {
			show.fadeIn("slow");
			return true;
		}
	} else {
		alert("Sorry we could not find that information!");
		return false;
	}
}

function fb_like(page) {
	if(!page){
		page = window.location;
	}

	document.write('<iframe src="http://www.facebook.com/plugins/like.php?href=' +
	page + '&amp;layout=standard&amp;show_faces=false&amp;width=450&amp;action=like&amp;' +
	'font&amp;colorscheme=light&amp;height=35" scrolling="no" frameborder="0" style="border:' +
	'none; overflow:hidden; width:450px; height:35px;" allowTransparency="true"></iframe>');
}

/* Google stuff */
var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-11817192-3']);
_gaq.push(['_trackPageview']);

(function() {
	var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
	ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
	var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
})();