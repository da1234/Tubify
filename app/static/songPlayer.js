$(document).ready(function() {
  console.log('initialising $ callbacks for songplayer');
  $("#addFormSubmit").click(function(event) {      
      $('#existingPlaylistModal').modal('toggle');
      $('#addForm').submit();
      console.log('submitted form');
    });
});
