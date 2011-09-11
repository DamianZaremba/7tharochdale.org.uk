<<<<<<< HEAD
/*
	This file is included on "print pages",
	these pages are very stripped down and suitable for printing.

	On inclusion of this file, once the document is ready it will
	tell the brower to print the document.
	
	This will load the printer dialog then once done, the window will close
*/
$(document).ready(function() {
	/* Tell the brower to print */
	window.print();

	/* Close the window */
=======
$(document).ready(function() {
	window.print();
>>>>>>> 8af8dd6c0e4b055d3db04a502c105134b5b4f32b
	self.close();
});
