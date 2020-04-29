$.sidebarMenu = function(menu) {
  var animationSpeed = 300,
      subMenuSelector = '.sidebar-submenu';
  $(menu).on('click', 'li a', function(e) {
    var $this = $(this);
    var checkElement = $this.next();
    if (checkElement.is(subMenuSelector) && checkElement.is(':visible')) {
      checkElement.slideUp(animationSpeed, function() {
        checkElement.removeClass('menu-open');
      });
      checkElement.parent("li").removeClass("active");
    }
    else if ((checkElement.is(subMenuSelector)) && (!checkElement.is(':visible'))) {
      var parent = $this.parents('ul').first();
      var ul = parent.find('ul:visible').slideUp(animationSpeed);
      ul.removeClass('menu-open');
      var parent_li = $this.parent("li");
      checkElement.slideDown(animationSpeed, function() {
        checkElement.addClass('menu-open');
        parent.find('li.active').removeClass('active');
        parent_li.addClass('active');
      });
    }
    if (checkElement.is(subMenuSelector)) {
      e.preventDefault();
    }
  });
}

$.sidebarMenu($('.sidebar-menu'))
$nav = $('.page-sidebar');
$header = $('.page-main-header');
$icon = $('.page-wrapper');
$sidebar_icon = $('.page-body-wrapper');
$toggle_nav_top = $('#sidebar-toggle');
$toggle_nav_top.click(function() {
  $this = $(this);
  $nav = $('.page-sidebar');
  $nav.toggleClass('open');
  $sidebar_icon.toggleClass('sidebar-hover');
  $icon.toggleClass('compact-page');
  $header.toggleClass('open');
});

$( window ).resize(function() {
  $.sidebarMenu($('.sidebar-menu'));
  $nav = $('.page-sidebar');
  $header = $('.page-main-header');
  $toggle_nav_top = $('#sidebar-toggle');
  $toggle_nav_top.click(function() {
    $this = $(this);
    $nav = $('.page-sidebar');
    $nav.toggleClass('open');
    $sidebar_icon.toggleClass('sidebar-hover');
    $icon.toggleClass('compact-page');
    $header.toggleClass('open');
  });
});

$body_part_side = $('.body-part');
$body_part_side.click(function(){
  $toggle_nav_top.attr('checked', false);
  $nav.addClass('open');
  $sidebar_icon.addClass('sidebar-hover');
  $icon.addClass('compact-page');
  $header.addClass('open');
});

//    responsive sidebar
var $window = $(window);
var widthwindow = $window.width();
(function($) {
  "use strict";
  if(widthwindow+17 <= 991) {
    $toggle_nav_top.attr('checked', false);
    $sidebar_icon.addClass('sidebar-hover');
    $icon.addClass('compact-page');
    $nav.addClass("open");
  }
})(jQuery);
$( window ).resize(function() {
  var widthwindaw = $window.width();
  if(widthwindaw+17 <= 991){
    $toggle_nav_top.attr('checked', false);
    $nav.addClass("open");
    $sidebar_icon.addClass('sidebar-hover');
    $icon.addClass('compact-page');
  }else{
    $toggle_nav_top.attr('checked', true);
    $nav.removeClass("open");
    $sidebar_icon.removeClass('sidebar-hover');
    $icon.removeClass('compact-page');
  }
});

// $(".sidebar-menu>li").removeClass("active");
$( ".sidebar-menu" ).find( "a" ).removeClass("active");
$( ".sidebar-menu" ).find( "li" ).removeClass("active");

var current = window.location.pathname
$(".sidebar-menu>li a").filter(function() {

  // console.log(window.location.pathname);
  // console.log($(this).attr("href"));

  var link = $(this).attr("href");
  if(link){
    if (current.indexOf(link) != -1) {
      $(this).parents('li').addClass('active');
      $(this).addClass('active');
    }
  }
});
