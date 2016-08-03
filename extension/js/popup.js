// Original code by : Prateek Dewan 
// Slightly modified by : iamgroot42

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


  if (document.getElementById('globalContainer') !== null) {   //'contentArea'
    observeDOM( document.getElementById('globalContainer') ,function(){


        $("._5pcq").each(function() {
          var elem = this;
          if($(this).find("._5ptz").length > 0 && $(this).find(".HelixAPIanalysis").length == 0) {
            var url = $(this).attr("href");
            $(this).addClass("analysed");
            $(this).append("<span class='HelixAPIanalysis'> Analysing</span>");

            var postId = "";

            if (url.indexOf("fbid") > -1) {
              postId = url.substring(url.indexOf("fbid") + 5, url.indexOf("&", url.indexOf("fbid") + 5));
            }
            else if (url.indexOf("posts") > -1) {
              postId = url.split("/")[url.split("/").length-1];
            } else if (url.indexOf("permalink") > -1 || url.indexOf("photos") > -1) {
              postId = url.split("/")[url.split("/").length-2];
            } else {
              postId = "1234";
            }

            var image_url = 'image_url=https://dz2k5jx87b7zc.cloudfront.net/wp-content/uploads/2013/05/All-American-Potato-Salad.jpg.jpg';
            var apiCallUrl =  "http://labs.precog.iiitd.edu.in/resources/HelixAPI/analyze_url";

            // Way to get send message compatibility over all chrome browser versions
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
            alert('sending get!');

            chrome.runtime.sendMessage({
                method: 'GET',
                action: 'xhttp',
                url: apiCallUrl,
                data : image_url
            }, function (responseText) {
                $(elem).find(".HelixAPIanalysis").html("");
                // var obj = JSON.parse(responseText);
                console.log(responseText);
                // if ('label' in obj && obj['label'] == "Malicious") {
                  // $(elem).append("<a href='http://precog.iiitd.edu.in/osm.html#fbi'> <img src='"+chrome.extension.getURL('error.png')+"' title='Confidence:" + obj['confidence'] + ".&#013Click on image for more details'></a>");
                  // $(elem).append("<a href='http://google.com>Google</a>");
                // }
            });
          }
        });
    });
  }
});
