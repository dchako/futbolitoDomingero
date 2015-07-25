$(document).on('ready', function(){
    'use strict';
    var altoWindow          = $(window).height(); // Obtengo el alto de la ventana actual
    var $seccionPrincipal   = $('#principal');

    $seccionPrincipal.height(altoWindow); // seteo la section principal con el alto del dispositivo

    // inicializando wow plugin
    new WOW().init();
});
