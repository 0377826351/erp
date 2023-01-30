$(document).ready(function(){
    if ($(".service-name").click(function(e) {
        e.preventDefault();
        // $(this).children('i').toggleClass("fa-circle-arrow-down").toggleClass("fa-circle-arrow-up");
        if (!$(this).parent().hasClass('active')) {
            $(this).parents('.list-service').find('.item-service.active .service-content').slideUp("fast");
            $(this).parents('.list-service').find('.item-service.active .service-name').children("i").removeClass("fa-circle-arrow-up");
            $(this).parents('.list-service').find('.item-service.active').removeClass('active');
            $(this).parent().addClass('active');
            $(this).children().addClass('fa-circle-arrow-up')
            $(this).parent().find('.service-content').slideDown("fast");
        }else{
            $(this).children("i").removeClass("fa-circle-arrow-up");
            $(this).parent().removeClass('active');
            $(this).parent().children(".service-content").slideUp("fast");
        }
    }));
});


