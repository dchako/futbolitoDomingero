$(document).on('ready',function (){

    $(".boton-invitar").on("click",function()
        {
         var usuario_invitado = $("#nombre").text();
         var grupete = $("#nombre_de_grupo").text();
         $.ajax({
             data: {'usuario_invitado': usuario_invitado,
                     'grupete': grupete,
                    },
             url: '/invitar_ajax/',
             type: 'get',
             success : function(data) {
                 	if(data.code=='OK'){
                 	    alert("invitaste al usuario ");
                 	    location.href = /invitar/ ;
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