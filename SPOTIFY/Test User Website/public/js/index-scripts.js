$(document).ready(function () {

    /*====================================
          SUBSCRIPTION   SCRIPTS 
    ======================================*/


   $("#postcontent").submit(function (e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "mail.php",
            data: $("#postcontent").serialize(),
             success: function (response) {
			  $('[name="email"]').val('');
               // alert(response); // FOR ACTUAL RESPONSE
			   alert('Thanks for subscribing Us');
            }
        });
        e.preventDefault();
    });

    // SCROLL SCRIPTS 
    $('.scroll-me a').bind('click', function (event) { //just pass scroll-me class and start scrolling
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top
        }, 1000, 'easeInOutQuad');
        event.preventDefault();
    });

   });

/*!
 * IE10 viewport hack for Surface/desktop Windows 8 bug
 * Copyright 2014 Twitter, Inc.
 * Licensed under the Creative Commons Attribution 3.0 Unported License. For
 * details, see http://creativecommons.org/licenses/by/3.0/.
 */

// See the Getting Started docs for more information:
// http://getbootstrap.com/getting-started/#support-ie10-width

(function () {
    'use strict';
    if (navigator.userAgent.match(/IEMobile\/10\.0/)) {
        var msViewportStyle = document.createElement('style')
        msViewportStyle.appendChild(
          document.createTextNode(
            '@-ms-viewport{width:auto!important}'
          )
        )
        document.querySelector('head').appendChild(msViewportStyle)
    }
})();
