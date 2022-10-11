$(document).ready(function() {
    $('#replytitle').click(function() {
      $('.comment-form-block').slideToggle("slow");
    });

    //Searchbar code 
    $('.nav-link.search-iamge').click(function() {
      $(".navbar.navbar-expand-lg.navbar-dark bg-dark").css("display","none");
      $('.sh-header-search').slideDown();
    });

    // close searchbar code 
    $('.sh-header-search-close.close-header-search').click(function() {
      $('.sh-header-search').slideUp();
      $(".navbar.navbar-expand-lg.navbar-dark bg-dark").css("display","block");
    });
});

// JavaScript code for fetch login/register API

console.log("ss")
function login(){
  var username = document.getElementById('loginUsername').value
  var password = document.getElementById('loginPassword').value
  var csrf = document.getElementById('csrf').value

  if(username == '' && password == ''){
    alert('you must enter both')
  }

  var data = {
    'username': username,
    'password': password
  }

  fetch('/api/login/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken' : csrf,
    },
    body : JSON.stringify(data)
  }).then(result => result.json())
  .then(response => {
    if(response.status == 200) {
      window.location.href = '/'
    }
    else {
      alert(response.message)
    }
    console.log("Got the response" , response)
  })
} 