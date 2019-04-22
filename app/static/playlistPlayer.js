$(document).ready(function() {
  console.log('initialising $ callbacks for playlist player');

    // Main play button functionality
  $('#play-all-button').click(function() {
    $(this).toggleClass(' btn-outline-primary  btn-outline-success');
    switch (player.getPlayerState()) {
      case YT.PlayerState.PLAYING:
        player.pauseVideo();
        break;
      case YT.PlayerState.PAUSED:
        player.playVideo();
        break;
      default:
        playPlaylist();
        break;
    }
  });

  // fast forward button functionality
  $('#forward-button').click(function() {
    playNextSong();
  });

  // backward forward button functionality
  $('#backward-button').click(function() {    
    playPreviousSong();
  })
});


// Status' can be ready, playing, paused, stopped
function changeSong(newId, button) {
  switch ($(button).data('status')) {
    case 'ready':
      // Check that we haven't switched songs.
      if (previous && button !== previous) {
        console.log('previous button clicked thats not me');
        // Change previous class.
        if ($(previous).hasClass('btn-success')) {
          console.log('previous button green');
          $(previous).toggleClass(' btn-success  btn-secondary');
        } else if ($(previous).hasClass('btn-primary')) {
          console.log('previous button green');
          $(previous).toggleClass(' btn-primary  btn-secondary');
        }
        $(previous).data('status','ready');
      }

      player.loadVideoById(newId);
      $(button).toggleClass(' btn-secondary  btn-success');
      previous = button;
      $(button).data('status','playing');
      break;
    case 'playing':
      player.pauseVideo();
      $(button).toggleClass(' btn-success  btn-primary');
      $(button).data('status','paused');
      previous = button;
      break;
    case 'paused':
        player.playVideo();
        $(button).toggleClass(' btn-primary  btn-success');
        $(button).data('status','playing');
        previous = button;
        break;
    default:
      break
  }
}


function playPlaylist() {
  playCuedSong();
  queueNewSong();
}



function pauseSong() {
  player.pauseVideo()
}
