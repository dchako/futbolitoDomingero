$(document).on('ready',function (){

    $(".aceptar").on("click",function()
        {
	alert ("acepta la invitacion")
	location.reload()
        });

    $(".rechazar").on("click",function()
        {
	alert ("rechaza")
	location.reload()
        });


});