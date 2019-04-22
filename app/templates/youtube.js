// Iframse set up
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;
var previous = null;
function onYouTubeIframeAPIReady() {
  player = new YT.Player('player', {
     height: '390',
     width: '640',
     videoId: document.getElementById('video_id').value,
     events: {
       'onReady': onPlayerReady,
       'onStateChange': onPlayerStateChange
      }
     })
};

function onPlayerReady(event) {
  event.target.setVolume(50);
};

function onPlayerStateChange(event) {
  switch (event.data) {
    case YT.PlayerState.PLAYING:
      console.log('PLAYING:' + $('#video_id').data('currently-playing'));
      break;
    case YT.PlayerState.ENDED:
      console.log('ENDED');
      playCuedSong();
      queueNewSong();
    default:
      break;
  };
};

function queueNewSong() {
  last_idx = $('#video_id').data('next-song-idx');
  next_idx = (last_idx + 1) % $('#video_id').data('no-songs');
  $('#video_id').data('next-song-idx',next_idx);
};

function playCuedSong() {
  next_idx = $('#video_id').data('next-song-idx').toString();
  next_song_id = $('#play-button-' + next_idx).data('song-id');
  $('#video_id').data('currently-playing',next_song_id);
  player.loadVideoById(next_song_id);
};

function playNextSong() {
  queueNewSong();
  playCuedSong();
};

function playPreviousSong() {
  queueNewSong();
  playCuedSong();
};
