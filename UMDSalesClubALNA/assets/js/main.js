/*
	Alpha by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
*/

(function($) {

	var	$window = $(window),
		$body = $('body'),
		$header = $('#header'),
		$banner = $('#banner');

	// Breakpoints.
		breakpoints({
			wide:      ( '1281px',  '1680px' ),
			normal:    ( '981px',   '1280px' ),
			narrow:    ( '737px',   '980px'  ),
			narrower:  ( '737px',   '840px'  ),
			mobile:    ( '481px',   '736px'  ),
			mobilep:   ( null,      '480px'  )
		});

	// Play initial animations on page load.
		$window.on('load', function() {
			window.setTimeout(function() {
				$body.removeClass('is-preload');
			}, 100);
		});

	// Dropdowns.
		$('#nav > ul').dropotron({
			alignment: 'right'
		});

	// NavPanel.

		// Button.
			$(
				'<div id="navButton">' +
					'<a href="#navPanel" class="toggle"></a>' +
				'</div>'
			)
				.appendTo($body);

		// Panel.
			$(
				'<div id="navPanel">' +
					'<nav>' +
						$('#nav').navList() +
					'</nav>' +
				'</div>'
			)
				.appendTo($body)
				.panel({
					delay: 500,
					hideOnClick: true,
					hideOnSwipe: true,
					resetScroll: true,
					resetForms: true,
					side: 'left',
					target: $body,
					visibleClass: 'navPanel-visible'
				});

	// Header.
		if (!browser.mobile
		&&	$header.hasClass('alt')
		&&	$banner.length > 0) {

			$window.on('load', function() {

				$banner.scrollex({
					bottom:		$header.outerHeight() + 250,
					terminate:	function() { $header.removeClass('alt'); },
					enter:		function() { $header.addClass('alt'); },
					leave:		function() { $header.removeClass('alt'); }
				});

			});

		}
	// Member Slideshow
		(function() {
			var $slides = $('.slideshow-container .slide');
			var $dots = $('.slideshow-dots .dot');
			if ($slides.length > 0) {
				var currentIndex = 0;
				var timer;

				function goToSlide(index) {
					$slides.eq(currentIndex).removeClass('active');
					$dots.eq(currentIndex).removeClass('active');
					currentIndex = index;
					$slides.eq(currentIndex).addClass('active');
					$dots.eq(currentIndex).addClass('active');
				}

				function nextSlide() {
					var nextIndex = (currentIndex + 1) % $slides.length;
					goToSlide(nextIndex);
				}

				function startTimer() {
					timer = setInterval(nextSlide, 8000);
				}

				$dots.on('click', function() {
					if (timer) clearInterval(timer);
					goToSlide($(this).data('slide'));
					startTimer();
				});

				startTimer();
			}
		})();

})(jQuery);