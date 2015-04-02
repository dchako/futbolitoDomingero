

	$.ajax({
             data: {'nombre': consulta},
             url: '/busqueda/',
             type: 'get',
             success : function(data) {
                 console.log(data[0].username);
                 },
            error : function(jqXHR, estado, error) {
                 console.log(estado);
                 console.log(error);
                  }
            complete: function(jqXHR, estado)
                {
                console.log(estado);
                },
             });