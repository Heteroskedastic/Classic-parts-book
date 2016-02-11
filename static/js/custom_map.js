
list_shp = ""
	function get_preview() {
		// $('#preview').click(function(){

			var div_coords = $('#code_content')[0];
			var coords_txt = div_coords.textContent;
			str_ary = coords_txt.split("shape");
			
			for (var i = 0; i <= str_ary.length - 1; i++) {
				if (str_ary[i][0]=="=") {
					var shp = str_ary[i];
					var shape_and_cords = shp.split('" ')
					var shape = shape_and_cords[0].replace('="',"")
					var cords = shape_and_cords[1].replace('coords="','')
					list_shp += "shape- "+shape +"\n";
					list_shp += "coords- "+cords +"\n";
					console.log("shape- "+list_shp);
					console.log("coords- "+cords);
				};
			};
			alert (list_shp);
		// });
	};

	function save_form() {
		// debugger
		$('#form_save')[0].type = "submit";
		var source = $('#img')[0].src ;
		$('#img_src').val(source);
		$('#img_field').val(list_shp);
		$("#form_save").click();

	}
