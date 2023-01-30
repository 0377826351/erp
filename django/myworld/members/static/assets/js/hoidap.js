$(document).ready(function(){
    if ($(".faq-name").click(function(e) {
        e.preventDefault();
        $(this).children('i').toggleClass("fa-circle-arrow-down").toggleClass("fa-circle-arrow-up");
        if (!$(this).parent().hasClass('active')) {
            $(this).parents('.list-faq').find('.item-faq.active .faq-content').slideUp("fast");
            $(this).parents('.list-faq').find('.item-faq.active .faq-name').children("i").removeClass("fa-circle-arrow-up").addClass("fa-circle-arrow-down");
            $(this).parents('.list-faq').find('.item-faq.active').removeClass('active');
            $(this).parent().addClass('active');
            $(this).parent().find('.faq-content').slideDown("fast");
        }else {
            $(this).parent().removeClass('active');
            $(".faq-content").slideUp("fast");
        }
    }));
});


// $(document).ready(function(){
//     if ($(".faq-name").click(function(e) {
//         e.preventDefault();
//         if (!$(this).parent().hasClass('active')) {
//             $(this).parents('.list-faq').find('.item-faq.active .faq-content').slideUp("fast");
//             $(this).parents('.list-faq').find('.item-faq.active .faq-name').children("i").removeClass("fa-circle-arrow-up");
//             $(this).parents('.list-faq').find('.item-faq.active').removeClass('active');
//             $(this).parent().addClass('active');
//             $(this).children().addClass('fa-circle-arrow-up')
//             $(this).parent().find('.faq-content').slideDown("fast");
//         }else{
//             $(this).children("i").removeClass("fa-circle-arrow-up");
//             $(this).parent().removeClass('active');
//             $(this).parent().children(".faq-content").slideUp("fast");
//         }
//     }));
// });
