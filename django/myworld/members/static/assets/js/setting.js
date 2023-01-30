$(document).ready(function(){
    $(".icon-bars").click(function () {
        $(this).children('i').toggleClass("fa-times").toggleClass("fa-bars");
        $("body").toggleClass("open-menu");
    });

    $('.opbg-mb').click(function(e) {
        $("body").removeClass("open-menu");
        $(this).parents().find(".icon-bars i").removeClass("fa-times").addClass("fa-bars");
    });

    $(function () {
        $(document).scroll(function () {
          var $nav = $(".navbar-fixed-top");
          $nav.toggleClass('scrolled', $(this).scrollTop() > $nav.height());
        });
      });

    $(document).mouseup(function(e) 
    {
        var container = $(".popup-search");
        if (!container.is(e.target) && container.has(e.target).length === 0) 
        {
            $(".opbg").css("visibility", "hidden");
        }
    });

    $(".search-header").click(function () {
        $(".opbg").css("visibility", "visible");
    });

    $(".close-pop").click(function () {
        $(".opbg").css("visibility", "hidden");
    });
    
});

$('.owl-carousel').owlCarousel({
    loop:true,
    margin:20,
    nav: true,
    responsive:{
        0:{
            items:1,
            nav: false
        },
        600:{
            items:2
        },
        1000:{
            items:3
        }
    }
});
