function getDiv() {
    var thisframe = document.querySelectorAll("iframe#ptifrmtgtframe");
    var div = thisframe[0].contentWindow.document.getElementById("win1div$ICField3$0");
    return div;
}

function capture_save() {
    html2canvas(getDiv(), {
        background :'#FFFFFF',
        dpi: 384,
        scale: 4,
        onrendered: function(canvas) {
            var a = document.createElement('a');
            // toDataURL defaults to png, so we need to request a jpeg, then convert for file download.
            a.href = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");
            a.download = 'transcript.png';
            a.click();
        }
    });
}

function capture_post(url) {
    html2canvas(getDiv(), {
        background :'#FFFFFF',
        dpi: 384,
        scale: 4,
        onrendered: function (canvas) {
            var form = document.createElement("form")
            var image = document.createElement("input")

            form.method = "POST"
            form.action = url
            form.target = "_blank"


            var imagedata = canvas.toDataURL('image/png');
            var imgdata = imagedata.replace(/^data:image\/(png|jpg);base64,/, "");

            image.type = 'hidden'
            image.value = imgdata
            form.appendChild(image)

            document.body.appendChild(form)
            form.submit()


            //ajax call to save image inside folder
            // $.ajax({
            //     url: 'save_image.php',
            //     data: {
            //            imgdata:imgdata
            //            },
            //     type: 'post',
            //     success: function (response) {   
            //        console.log(response);
            //        $('#image_id img').attr('src', response);
            //     }
            // });
        }
    });
}

