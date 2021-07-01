// nombre de vignettes à décaler lors
// du click
var num_to_show = 5;
function defer(method) {
  if (window.jQuery)
    method();
  else
    setTimeout(function() {
      defer(method)
    }, 50);
}
defer(function() {
  (function($) {

    function doneResizing() {
      var totalScroll = $('.resource-slider-frame').scrollLeft();
      var itemWidth = $('.resource-slider-item').width();
      var difference = totalScroll % itemWidth;
      if ( difference !== 0 ) {
        $('.resource-slider-frame').animate({
          scrollLeft: '-=' + difference
        }, 500, function() {
          // check arrows
          checkArrows();
        });
      }
    }

    function checkArrows() {
      var totalWidth = $('#resource-slider .resource-slider-item').length * $('.resource-slider-item').width();
      var frameWidth = $('.resource-slider-frame').width();
      var itemWidth = $('.resource-slider-item').width();
      var totalScroll = $('.resource-slider-frame').scrollLeft();

      if ( ((totalWidth - frameWidth) - totalScroll) < itemWidth ) {
        $(".next").css("visibility", "hidden");
      }
      else {
        $(".next").css("visibility", "visible");
      }
      if ( totalScroll < itemWidth ) {
        $(".prev").css("visibility", "hidden");
      }
      else {
        $(".prev").css("visibility", "visible");
      }
    }

    $('.arrow').on('click', function() {
      var $this = $(this),
        width = $('.resource-slider-item').width(),
        speed = 500
      width2 = num_to_show*parseFloat(width);
      if ($this.hasClass('prev')) {
        $('.resource-slider-frame').animate({
          scrollLeft: '-=' + width2 +'px'
        }, speed, function() {
          // check arrows
          checkArrows();
        });
      } else if ($this.hasClass('next')) {
        $('.resource-slider-frame').animate({
          scrollLeft: '+=' + width2 + 'px'
        }, speed, function() {
          // check arrows
          checkArrows();
        });
      }
    }); // end on arrow click

    $(window).on("load resize", function() {
      checkArrows();
      $('#resource-slider .resource-slider-item').each(function(i) {
        var $this = $(this),
          left = $this.width() * i;
        $this.css({
          left: left,
          top: -40
        })
      }); // end each
    }); // end window resize/load

    var resizeId;
    $(window).resize(function() {
        clearTimeout(resizeId);
        resizeId = setTimeout(doneResizing, 500);
    });

  })(jQuery); // end function
});
