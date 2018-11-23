$(function() {

    // Chamado ao clicar no Toogle (On/Off)
    $(".handleToogle").on("change", function() {
        var status = $(this).is(":checked") ? '1' : '0';

        try {
            $.ajax({
                type: 'POST',
                url: '/requisicao',
                dataType: 'jsonp',
                data: {id: $(this).attr("data-pin"), status: status}
            })
            .done(function(data) {
                console.log(data);
            })
            .fail(function() {
                alertify.error("Falha ao realizar a operação!")
            });
            
        } catch (e) {
            alertify.error("Error ao enviar a requisição!")
        }
    }); // handleToogle


});
