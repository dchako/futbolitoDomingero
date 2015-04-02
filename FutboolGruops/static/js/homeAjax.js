
$(document).on('ready',function (){

       $("#asistir").on("click",function(e){
        e.preventDefault();
        var usuario ="dchakos";
        var grupo = "Team Campito";
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
                 	}else{
                 		alert(data.message);
                 	}
                 },
            error : function(data) {
                 	console.log('ERROR EN LA COMUNICACION CON EL SERVIDOR')
                  },
            complete: function(jqXHR, estado)
                {
                console.log(estado);
                },
             });
       });

    $("#no_asistir").on("click",function(e){
        e.preventDefault();
        var usuario ="dchakos";
        var grupo = "Team Campito";
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
                 	}else{
                 		alert(data.message);
                 	}
                 },
            error : function(data) {
                 	console.log('ERROR EN LA COMUNICACION CON EL SERVIDOR')
                  },
            complete: function(jqXHR, estado)
                {
                console.log(estado);
                },
             });
        });

    $("#cambiazo").on("click",function(e){
        e.preventDefault();
        var usuario ="dchakos";
        var grupo = "Team Campito";
	$.ajax({
             data: {'nombre': usuario,
                     'grupo': grupo,
                    },
             url: '/cambioDeEquipo_ajax/',
             type: 'get',
             success : function(data) {
                 	if(data.code=='OK'){
                 	    alert("cambiaste de equipo");
                 	}else{
                 		alert(data.message);
                 	}
                 },
            error : function(data) {
                 	console.log('ERROR EN LA COMUNICACION CON EL SERVIDOR')
                  },
            complete: function(jqXHR, estado)
                {
                console.log(estado);
                },
             });
	
        });

    $(".cambiar").on("click",function()
        {
	alert ("aca va el ajax de cambiar de grupo a otros grupos pero no se todavua")
        });


 });