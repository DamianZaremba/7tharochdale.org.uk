if(window.location.href.indexOf('?page=') == -1){
	pageToShow = 'photos';
}else{
	pageToShow = String(window.location.href.slice(window.location.href.indexOf('?page=') + 1).split('=')[1].split('&')[0].split('#')[0]);
	if(pageToShow.length == 0){
	/* If the page varible is empty */
		pageToShow = 'photos';
	}
}

function loadFirstPage() {
	cp = $("#page_" + currentPage);
	cp.hide(1);
	switchPage(pageToShow);
}

function jumpTo(section){
	if($("a[name="+section+"]").length != 0){
		section = $("a[name="+section+"]").offset().top - 100;
		$('html,body').animate({scrollTop: section}, 500);
	}
}

function switchPage(newPage, jumpToSection){
	cp = $("#page_"+currentPage);
	np = $("#page_"+newPage);

	if(np.length != 0){
		cp.fadeOut(null, function () {
			$("#menu ul li").each(function(index){
				$(this).removeClass("current_page_item");
			});
			if($("#mainm_"+newPage).length != 0){
				$("#mainm_"+newPage).addClass("current_page_item");
			}
			np.fadeIn();
			currentPage = newPage;
			if(jumpToSection != null){
				jumpTo(jumpToSection);
			}
		});
	}else{
		np = $("#page_404");
		if(np.length != 0){
			$("#menu ul li").each(function(index){
				$(this).removeClass("current_page_item");
			});
			cp.fadeOut(null, function () {
				np.fadeIn();
				currentPage = '404';
			});
		}else{
			alert("Sorry an error occurred, please try again!");
		}
	}
}
