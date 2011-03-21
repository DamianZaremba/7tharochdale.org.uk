<?php 
/*
 * This is horrible and should only be run on the command line.
 * Will generate thumbnail images recursivly for all gallery images and videos.
 */
$images_folder = "/home/damian/Projects/7thA/7tharochdale.org.uk/assests/gallery/images/";
$thumbsfolder = "/home/damian/Projects/7thA/7tharochdale.org.uk/assests/gallery/image_thumbnails/";
$videos_folder = "/home/damian/Projects/7thA/7tharochdale.org.uk/assests/gallery/video/";
$imagesplash_folder = "/home/damian/Projects/7thA/7tharochdale.org.uk/assests/gallery/video_splash/";

$valid_image_exts = array("jpg", "JPG", "JPEG", "jpeg", "png", "PNG");
$valid_video_exts = array("flv", "m4v", "swf", "mp4");
$files = array();

ini_set("gd.jpeg_ignore_warning", 1);
ini_set("max_execution_time", 60*60*24);
ini_set("memory_limit", "512M");

function rm_dirs($path) {
	if (is_dir($path)){
		$handle = opendir($path);
	}

	if (!$handle){
		return false;
	}

	while($file = readdir($handle)) {
		if ($file != "." && $file != "..") {
			if (!is_dir($path . "/" . $file)){
				unlink($path . "/" . $file);
			}else{
				rm_dirs($path . "/" . $file);
			}
		}
	}

	closedir($handle);
	rmdir($path);
	return true;
}

function get_video_files($dir) {
	global $files, $valid_video_exts;

	$handle = opendir($dir);
	while (($path = readdir($handle)) !== false){
		if($path ==  "." || $path ==  ".."){ continue; }
		$path = str_replace("//", "/", $dir . "/" . $path);

		if(is_file($path)){
			$parts = explode(".", $path);
			$ext = $parts[count($parts)-1];
			if(in_array($ext, $valid_video_exts)){
				$files[] = $path;
			}
		}else if(is_dir($path)){
			get_video_files($path);
		}
	}
	closedir($handle);
	return $files;
}

function get_image_files($dir) {
	global $files, $valid_image_exts;

	$handle = opendir($dir);
	while (($path = readdir($handle)) !== false){
		if($path ==  "." || $path ==  ".."){ continue; }
		$path = str_replace("//", "/", $dir . "/" . $path);

		if(is_file($path)){
			$parts = explode(".", $path);
			$ext = $parts[count($parts)-1];
			if(in_array($ext, $valid_image_exts)){
				$files[] = $path;
			}
		}else if(is_dir($path)){
			get_image_files($path);
		}
	}
	closedir($handle);
	return $files;
}

function create_image_thumb($path, $height, $width){
	global $images_folder, $thumbsfolder;
	$new_path = str_replace($images_folder, $thumbsfolder, $path);
	
	$parts = explode(".", $path);
	if (preg_match("/jpg|jpeg/i", $parts[count($parts)-1])){
		$image = imagecreatefromjpeg($path);
	}else if (preg_match("/png/i", $parts[count($parts)-1])){
		$image = imagecreatefrompng($path);
	}else{
		print "Unknown image format";
		return;
	}
	
	if(!$image) { print "Could not open image"; return false; }

	$x = imageSX($image);
	$y = imageSY($image);

	if ($x > $y){
		$thumb_w = $width;
		$thumb_h = $y*($height/$x);
	}else if ($x < $y){
		$thumb_w = $x*($width/$y);
		$thumb_h = $height;
	} else {
		$thumb_w = $width;
		$thumb_h = $height;
	}

	$thumb_image = ImageCreateTrueColor($thumb_w, $thumb_h);
	imagecopyresampled($thumb_image, $image, 0, 0, 0, 0, $thumb_w, $thumb_h, $x, $y); 

	$dir = dirname($new_path);
	if(!is_dir($dir)){
		mkdir($dir, 0777, true);
	}

	if (preg_match("/jpg|jpeg/i", $parts[count($parts)-1])){
		imagejpeg($thumb_image, $new_path); 
	}else if (preg_match("/png/i", $parts[count($parts)-1])){
		imagepng($thumb_image, $new_path);
	}
	imagedestroy($image); 
	imagedestroy($thumb_image); 
}

function create_video_thumb($path, $height, $width, $splash=False) {
		global $imagesplash_folder, $thumbsfolder, $videos_folder, $images_folder;

		if($splash === False){
			$new_path = str_replace($images_folder, $thumbsfolder, $path . ".png");
		}else{
			$new_path = str_replace($videos_folder, $imagesplash_folder, $path . ".png");
		}

		mkdir(dirname($new_path), 0777, true);
		system("ffmpeg -i " . $path . " -r 1 -ss 00:00:05 -s " . $width . "x" . $height . " -an -qscale 1 " . $new_path);
}

if(is_dir($thumbsfolder)){
	rm_dirs($thumbsfolder);
}

$files=array();
$files = get_image_files($images_folder);
foreach($files as $file){
	create_image_thumb($file, 50, 50);
}

$files=array();
$files = get_video_files($images_folder);
foreach($files as $file){
	create_video_thumb($file, 330, 520);
}

$files=array();
$files = get_video_files($videos_folder);
foreach($files as $file){
	create_video_thumb($file, 370, 598,True);
}
?>
