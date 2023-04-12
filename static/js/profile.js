var postsBtn = document.querySelector('button.postsBtn');
var likesBtn =  document.querySelector('button.likesBtn');
var savesBtn = document.querySelector('button.savesBtn');


var postsLayout = document.querySelector('div.posts');
var likesLayout = document.querySelector('div.likes');
var savesLayout = document.querySelector('div.saves');


postsBtn.addEventListener('click', () => {
  postsLayout.classList.remove('hide')
  likesLayout.classList.add('hide')
  savesLayout.classList.add('hide')

  postsBtn.classList.add('follow-up')
  likesBtn.classList.remove('follow-up')
  savesBtn.classList.remove('follow-up')
})

likesBtn.addEventListener('click', () => {
  postsLayout.classList.add('hide')
  likesLayout.classList.remove('hide')
  savesLayout.classList.add('hide')
  
  likesBtn.classList.add('follow-up')
  postsBtn.classList.remove('follow-up')
  savesBtn.classList.remove('follow-up')
})

savesBtn.addEventListener('click', () => {
  postsLayout.classList.add('hide')
  likesLayout.classList.add('hide')
  savesLayout.classList.remove('hide')
  
  savesBtn.classList.add('follow-up')
  likesBtn.classList.remove('follow-up')
  postsBtn.classList.remove('follow-up')
})