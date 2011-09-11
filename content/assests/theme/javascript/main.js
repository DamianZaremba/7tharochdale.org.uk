function preLoadImages(imageArray){
	$.each(imageArray, function (i, val) {
		/*
			Lets just make a new dom img object and set it's src to this value,
			the browser /should/ then cache the image making the hover effects work nicely with no loading delay!
		*/
		cacheImage = document.createElement('img').src = val;
	});
}

function switch_menu_image(item) {
	/* Hack to get the current image stuff. */
	image_parts = item.getAttribute('src').split('/');
	image_path = image_parts.splice(0, image_parts.length-1).join("/");
	image_name = image_parts[image_parts.length-1];

	if(image_name.split('depressed_').length == 2){
		/*
			We are the depressed image, lets load the happy image
		*/
		replace_image = image_path+'/'+image_name.split('depressed_')[1];
	}else{
		/*
			We are the happy image (ha!), lets load the depressed image
		*/
		replace_image = image_path+'/depressed_'+image_name;
	}
	/* Actually do the update to the image src */
	item.src = replace_image;
}

function switcher(show_id, init) {
	/* Get the object we want to show */
	var show = $("#" + show_id);

	/* Test the object is valid */
	if (show.length) {
		/* Test the object is not allready displaying */
		if (show.is(":visible")){
			if(!init) {
				show.fadeOut("fast");
			}
			return true;
		} else {
<<<<<<< HEAD
			/* Get all the switch elements on the page */
			elements = $(".switch");

			/* Figure out how many switch elements there are on this page */
			lastId = elements.length - 1;

			/* Loop though the elements */
			elements.each(function(i) {
				/* Fade out the image */
				$(this).fadeOut("fast");

				/* Check if this is the last element we need to fade out */
				if(i == lastId) {
					/* Fade in the element we want to show */
					show.fadeIn("fast");
					return true;
=======
			elements = $(".switch");
			lastId = elements.length - 1;
			elements.each(function(i) {
				$(this).fadeOut("fast");

				if(i == lastId) {
					show.fadeIn("fast");
>>>>>>> 8af8dd6c0e4b055d3db04a502c105134b5b4f32b
				}
			});
		}
	/* Show object is not valid, return false */
	} else {
		return false;
	}
}

function popup(link, width, height) {
	/* Create a new window object */
	newwindow = window.open(link, 'popup_window', 'width=' + width + ',height=' + height);

	/* Tell the browser to focus on the new window */
	newwindow.focus()

	/* Stop any furthur actions */
	return false;
}

<<<<<<< HEAD
/* Google analytics stuff */
=======
function popup(link, width, height) {
	var href;
	if(typeof(link) == 'string') {
		href=link;
	} else {
		href = link.href;
	}

	newwindow = window.open(href, 'popup_window', 'width=' + width + ',height=' + height);
	newwindow.focus()
	return false;
}

/* Google stuff */
>>>>>>> 8af8dd6c0e4b055d3db04a502c105134b5b4f32b
var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-11817192-3']);
_gaq.push(['_trackPageview']);

/* Things we need to do when the document is ready */
$(document).ready(function() {
	/* Init the analytics stuff */
	var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
	ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
	var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);

<<<<<<< HEAD
	/*
		Hide any displaying switches,
		we don't hide them in css in case js is disabled.
	*/
	$(".switch, .switch_hide").hide('fast', function () {
		/* Try and auto load an section specified in the url */
		if(window.location.href.indexOf('#') != -1){
			/* Figure out the requested section */
			requested_section = String(window.location.href.slice(window.location.href.indexOf('#') + 1));

			/* Check the requested section is a larger than 0 */
			if(requested_section.length != 0){
				/* Check the requested section is valid */
				if($("#" + requested_section).length != 0){
					/*
						Pass the string off to the switcher to actually load it,
						this saves code duplication as the switcher does magic to tidy stuff up
					*/
					switcher(requested_section, 1);
=======
	/* Deal with switches */
	$(".switch, .switch_hide").hide('fast', function () {
		/* Try and auto load an section specified in the url */
		if(window.location.href.indexOf('#') != -1){
			requested_section = String(window.location.href.slice(window.location.href.indexOf('#') + 1));
			if(requested_section.length != 0){
				if($("#" + requested_section).length != 0){
					switcher(requested_section);
>>>>>>> 8af8dd6c0e4b055d3db04a502c105134b5b4f32b
				}
			}
		}

<<<<<<< HEAD
		/* Make any elements with the .switch_unhide class displayable */
=======
>>>>>>> 8af8dd6c0e4b055d3db04a502c105134b5b4f32b
		$(".switch_unhide").show();
	});
});
