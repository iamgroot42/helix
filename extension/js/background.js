$(function() {
 // Useless variables
 var analyze = function(url){
   $.ajax({
      type: 'GET',
      url: 'http://localhost:5000/analyze_url?' + url,
      success: function(text)
      {
        alert(text);
        // Replace alert with sweetalert?
      }
    });
 }
 var wrap_all = function(callback) {
  // Wrap all image tags with custom div to show a pop-up for 'analyze this image'
 };
});
