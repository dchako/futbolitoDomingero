alert("asdada")
$('#busquedjugador').keyup(function(e){
 consulta = $("#busquedjugador").val();
 $.ajax({
 data: {'nombre': consulta},
 url: '/busqueda/',
 type: 'get',
 success : function(data) {
         console.log(data[0].username);
 },
 error : function(message) {
         console.log(message);
      }
 });
});