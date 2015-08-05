
$(document).on('ready',function (){

       $("#asistir").on("click",function(e){
        e.preventDefault();
        var usuario = $("#nombre_usuario").text();
        var grupo = $("#nombre_de_grupo").text();
        //alert(usuario);
        //var usuario ="dchakos";
        //var grupo = "Team Campito";
        var accion = 1;
	$.ajax({
             data: {'nombre': usuario,
                     'grupo': grupo,
                     'accion': accion,
                    },
             url: '/asistencia_ajax/',
             type: 'get',
             success : function(data) {
                 	if(data.code=='OK'){
                 		
                 		alert("agira asiste");
                 		location.reload();
                 	}else{
                 		alert(data.message);
                 	}
                 },
            error : function(data) {
                 	console.log('ERROR EN LA COMUNICACION CON EL SERVIDOR');
                  },
            complete: function(jqXHR, estado)
                {
                console.log(estado);
                },
             });
       });

    $("#no_asistir").on("click",function(e){
        e.preventDefault();
        var usuario = $("#nombre_usuario").text();
        var grupo = $("#nombre_de_grupo").text();
        var accion = 0;
	$.ajax({
             data: {'nombre': usuario,
                     'grupo': grupo,
                     'accion': accion,
                    },
             url: '/asistencia_ajax/',
             type: 'get',
             success : function(data) {
                 	if(data.code=='OK'){
                 		
                 		alert("ya no asiste");
                 		location.reload();
                 	}else{
                 		alert(data.message);
                 	}
                 },
            error : function(data) {
                 	console.log('ERROR EN LA COMUNICACION CON EL SERVIDOR');
                  },
            complete: function(jqXHR, estado)
                {
                console.log(estado);
                },
             });
        });

    $("#cambiazo").on("click",function(e){
        e.preventDefault();
        var usuario = $("#nombre_usuario").text();
        var grupo = $("#nombre_de_grupo").text();
	$.ajax({
             data: {'nombre': usuario,
                     'grupo': grupo,
                    },
             url: '/cambioDeEquipo_ajax/',
             type: 'get',
             success : function(data) {
                 	if(data.code=='OK'){
                 	    alert("cambiaste de equipo");
                 	    location.reload();
                 	}else{
                 		alert(data.message);
                 	}
                 },
            error : function(data) {
                 	console.log('ERROR EN LA COMUNICACION CON EL SERVIDOR');
                  },
            complete: function(jqXHR, estado)
                {
                console.log(estado);
                },
             });
	
        });

    $(".cambiarlo").on("click",function()
        {
	var nombre = $(this).text();
	alert (nombre);
        });


 });