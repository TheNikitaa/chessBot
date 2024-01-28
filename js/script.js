document.addEventListener('DOMContentLoaded', () => {

	var hamburger = document.querySelector('.hamburger');
	var menu = document.querySelector('.menu');
	var menuClose = document.querySelector('.menu-close');

	hamburger.addEventListener('click', function() {
		menu.classList.add('is-active');
	});
	menuClose.addEventListener('click', function() {
		menu.classList.remove('is-active');
	});
})
$("a[href^='#']").click(function () {
	var _href = $(this).attr("href");
	$("html, body").animate({scrollTop: $(_href).offset().top -100 + "px"});
	return false;
});
function scrollToSection(sectionId) {
	var section = document.getElementById(sectionId);
	section.scrollIntoView({ behavior: 'smooth' });
}