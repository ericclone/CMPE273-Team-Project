
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>html2canvas_demo1</title>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>
<script src="html2canvas.js"></script>
<script>
	$(document).ready(function(){
		//alert("ready")
		
		html2canvas($("#target"), {
			onrendered: function(canvas) {
				$("#showPlace").append(canvas);
				
				var dataURL = canvas.toDataURL();
				
				$("#img").val(dataURL);
				
				alert(dataURL);
				
				
			}
		});
		
	});// END ready

</script>
</head>

<body>

<form id="form1" method="post" action="genImg.php">
	<input id="img" name="img" type="text" value="">
	<div id="target" style="background-color:yellow;width:300px;height:150px">
	CMPE202<br>
	CMPE208
	</div>
	<br><br>
	<div id="showPlace">canvas:<br></div>
	<input type="submit">
</form>
</body>
</html>







