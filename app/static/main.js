$(document).ready(function() {
  console.log('initialising $ callbacks');
  $(".nav-link").click(function(event) {
      if ($(event.target).data('type') === 'playlist') {
          console.log('changing playlist');
          window.location.replace($(event.target).data('playlist-url'))        
      }
    });
});
