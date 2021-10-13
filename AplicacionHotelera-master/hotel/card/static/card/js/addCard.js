Paymentez.init('stg', 'INNOVA-EC-CLIENT', 'ZjgaQCbgAzNF7k8Fb1Qf4yYLHUsePk ');
$(document).ready(function(){
    $("#agregarTarjeta").click(function(){
        console.log("click");
        console.log($('#my-card'));
        var myCard = $('#my-card');
        var cardToSave = myCard.PaymentezForm('card');
        if(cardToSave == null){
            alert("Invalid Card Data");
        }
        console.log(cardToSave);
    });
});
