var btnUpload = $("#upload_file"),
		btnOuter = $(".button_outer");
	    btnUpload.on("change", async function(e){
		var ext = btnUpload.val().split('.').pop().toLowerCase();
		if($.inArray(ext, ['gif','png','jpg','jpeg']) == -1) {
			$(".error_msg").text("Not an Image...");
		} else {
            let dataFile = new FormData()
        		dataFile.append("file", upload_file.files[0]);
        		await fetch('/', {
            	method: "POST",
            	body: dataFile
        	});
			$(".error_msg").text("");
			btnOuter.addClass("file_uploading");
			setTimeout(function(){
				btnOuter.addClass("file_uploaded");
			},3000);
			setInterval(() => {
        		$.getJSON(                            
            	$SCRIPT_ROOT + "/update",      
            	{},                                
            	function(data)                    
            	{
					alert(data)
              		$("#ekspresi").text(data.result);                               
            	});
    		},500);  
			var uploadedFile = URL.createObjectURL(e.target.files[0]);
			setTimeout( function(){
				$("#uploaded_view").append('<img src="'+uploadedFile+'" />').addClass("show");
			},3500);
		}
	});
	$(".file_remove").on("click", function(e){
		$("#uploaded_view").removeClass("show");
		$("#uploaded_view").find("img").remove();
		btnOuter.removeClass("file_uploading");
		btnOuter.removeClass("file_uploaded");
	});