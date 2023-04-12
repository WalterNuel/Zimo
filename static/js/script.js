var slideIn = document.querySelector('button.info-btn');
var slide = document.querySelector('div.users');

var slideOut = document.querySelector('button.info-back');


slideIn.addEventListener('click', function () {
  slide.classList.toggle("show");
})

slideOut.addEventListener('click', function () {
  slide.classList.toggle("show");
})
