<?php
	// requires php5
	define('UPLOAD_DIR', 'img/');
	$img = $_POST['img'];
	$img = str_replace('data:image/png;base64,', '', $img);
	$img = str_replace(' ', '+', $img);
	$data = base64_decode($img);
	$file = UPLOAD_DIR . uniqid() . '.png';
	$success = file_put_contents($file, $data);
	print $success ? $file : 'Unable to save the file.';
	
	
	
	//Reference:
	//http://stackoverflow.com/questions/13198131/how-to-save-a-html5-canvas-as-image-on-a-server
	//http://j-query.blogspot.com/2011/02/save-base64-encoded-canvas-image-to-png.html
?>