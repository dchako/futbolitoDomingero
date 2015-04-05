$(document).on('ready',function (){

    $(".aceptar").on("click",function()
        {
         var id = $(".id").text();
         var accion = 1;
         $.ajax({
             data: {'id': id,
                     'accion': accion,
                    },
             url: '/invitacion_ajax/',
             type: 'get',
             success : function(data) {
                 	if(data.code=='OK'){
                 		
                 		alert("agira asiste");
                 		location.reload()
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

    $(".rechazar").on("click",function()
        {
         var id = $(".id").text();
         var accion = 0;
         $.ajax({
             data: {'id': id,
                     'accion': accion,
                    },
             url: '/invitacion_ajax/',
             type: 'get',
             success : function(data) {
                 	if(data.code=='OK'){
                 		
                 		alert("agira asiste");
                 		location.reload()
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


});