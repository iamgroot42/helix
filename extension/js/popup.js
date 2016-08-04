// Original code by : Prateek Dewan 
// Modified by : iamgroot42

$ (document).ready( function() {
  var observeDOM = (function(){
      var MutationObserver = window.MutationObserver || window.WebKitMutationObserver,
          eventListenerSupported = window.addEventListener;

      return function(obj, callback){
          if( MutationObserver ){
              // define a new observer
              var obs = new MutationObserver(function(mutations, observer){
                  if( mutations[0].addedNodes.length || mutations[0].removedNodes.length )
                      callback();
              });
              // have the observer observe foo for changes in children
              obs.observe( obj, { childList:true, subtree:true });
          }
          else if( eventListenerSupported ){
              obj.addEventListener('DOMNodeInserted', callback, false);
              obj.addEventListener('DOMNodeRemoved', callback, false);
          }
      }
  })();


  if (document.getElementById('globalContainer') !== null) {   
    observeDOM( document.getElementById('globalContainer') ,function(){

        $("._5pcq").each(function() {
          var elem = this;
          if($(this).find("._5ptz").length > 0 && $(this).find(".HelixAPIanalysis").length == 0) {
            var url = $(this).attr("href");
            $(this).addClass("analysed");
            $(this).append("<span class='HelixAPIanalysis'> </span>");

            var image_id = "";
            var index = url.indexOf("fbid");
            if (index > -1) {
              image_id = url.substring(index + 5, url.indexOf("&", index + 5));
            }
            else if (url.indexOf("posts") > -1) {
              image_id = url.split("/")[url.split("/").length-1];
            } else if (url.indexOf("permalink") > -1 || url.indexOf("photos") > -1) {
              image_id = url.split("/")[url.split("/").length-2];
            }
            // var access_token = "<ACCESS TOKEN FROM APP/IPOD>";
            var access_token = "EAACEdEose0cBAIRxyqRID1E62rFZANBOZCdNRF3AxP18Kd7yGv8iLQKoZBZAclvwm8DZCFiG5KJ4DCMcQiq1bvRhZBZCpwV84KHZA184kpGh9GxO3dKV6tgQHDTksbhHphCTtFyqbKJZB1ekVlYVMB8QrFA9R98BujTZArGjRTH9xQHgZDZD";
            var graph_url = "https://graph.facebook.com/v2.3/" + image_id + "?fields=source&access_token=" + access_token;
            var apiCallUrl =  "http://labs.precog.iiitd.edu.in/resources/HelixAPI/analyze_url?image_url=";
            // Way to get send message compatibility over all chrome browser versions
            if(image_id != ""){
              $.ajax({
                type: 'GET',
                url: graph_url,
                dataType: 'json',
                success: function(graph_obj) {
                    // If it's a public image
                    if('source' in graph_obj){
                      var image_url = graph_obj['source'];
                      if (!chrome.runtime) {
                        // Chrome 20-21
                        chrome.runtime = chrome.extension;
                      } else if(!chrome.runtime.onMessage) {
                        // Chrome 22-25
                        chrome.runtime.onMessage = chrome.extension.onMessage;
                        chrome.runtime.sendMessage = chrome.extension.sendMessage;
                        chrome.runtime.onConnect = chrome.extension.onConnect;
                        chrome.runtime.connect = chrome.extension.connect;
                      }
                      // Send GET request to HelixAPI
                      chrome.runtime.sendMessage({
                        method: 'GET',
                        action: 'xhttp',
                        url: apiCallUrl,
                        data : image_url
                        }, function (responseText) {
                          $(elem).find(".HelixAPIanalysis").html("");
                          var obj = JSON.parse(responseText);
                          if(!("error" in obj)){
                          	console.log(responseText);
                          	var senti = obj['sentiment'];
                          	var tag = obj['tag'];
                          	var text = obj['text'];
                          }
                        });
                      }
                  }
              });
            }
          }
        });
    });
  }
});
