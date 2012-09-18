function switcher(show_id) {
	/* Get the object we want to show */
	var show = $("#" + show_id);

	/* Test the object is valid */
	if (show.length) {
		/* Test the object is not allready displaying */
		if (show.is(":visible")){
			return true;
		} else {
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
				}
			});
		}
	/* Show object is not valid, return false */
	} else {
		return false;
	}
}

function fb_like(page) {
	/*
		If the page is not specified then pull the page from window.location,
		this is a fallback only and shouldn't be relied upon.
	*/
	if(!page){
		page = window.location;
	}

	/* Write out the facebook iframe */
	document.write(
		'<iframe src="http://www.facebook.com/plugins/like.php?href=' + page +
		'&amp;layout=standard&amp;show_faces=false&amp;width=450&amp;action=like&amp;' +
		'font&amp;colorscheme=light&amp;height=35" scrolling="no" frameborder="0" style="border:' +
		'none; overflow:hidden; width:450px; height:35px;" allowTransparency="true"></iframe>'
	);
}

function popup(link, width, height) {
	/* Create a new window object */
	newwindow = window.open(link, 'popup_window', 'width=' + width + ',height=' + height);

	/* Tell the browser to focus on the new window */
	newwindow.focus()

	/* Stop any furthur actions */
	return false;
}

/* Google analytics stuff */
var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-11817192-3']);
_gaq.push(['_trackPageview']);

/* Things we need to do when the document is ready */
$(document).ready(function() {
	/* Init the analytics stuff */
	var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
	ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
	var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);

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
					switcher(requested_section);
				}
			}
		}

		/* Make any elements with the .switch_unhide class displayable */
		$(".switch_unhide").show();
	});
});
