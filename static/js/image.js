var body = document.querySelector('body');
var fade = document.querySelector('.f-one');
var fade2 = document.querySelector('.f-two');

body.addEventListener('click', function () {
  fade.classList.toggle("out");
  fade2.classList.toggle("out");
})