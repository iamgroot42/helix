// Original code by : Prateek Dewan 
// Modified by : iamgroot42

var which_icon = function(positive_confidence){
    if(positive_confidence >= 0.8){
      icon = "5";
    }
    else if(positive_confidence >= 0.6){
      icon = "4";
    }
    else if(positive_confidence >= 0.4){
      icon = "3";
    }
    else if(positive_confidence >= 0.2){
      icon = "2";
    }
    else{
      icon = "1";
    }
    return chrome.extension.getURL("icons/" + icon + ".png");
};

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
            var apiCallUrl =  "http://labs.precog.iiitd.edu.in/resources/HelixAPI/analyze_fbid?id=";
            if(image_id == ""){
              // jQuery's 'each' treats return true as continue, return false as break
              return true;
            }
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
            // Send GET request to HelixAPI
            chrome.runtime.sendMessage({
              method: 'GET',
              action: 'xhttp',
              url: apiCallUrl,
              data : image_id
              }, function (responseText) {
                $(elem).find(".HelixAPIanalysis").html("");
                var obj = JSON.parse(responseText);
                if(!("error" in obj)){
                	var senti = obj['sentiment'];
                	var tag = obj['tag'];
                	var text = obj['text'];
                  var inner_html = "";
                  // Inceptionv3 tag
                  inner_html += "<b>" + tag['tag'] + "</b> (" + Math.round(100*tag['confidence']) + "% confidence)<br><br>";
                  // Sentibank model sentiment
                  inner_html += "<b>Overall sentiment:</b> ";
                  inner_html += "<img src='" + which_icon(senti["Tensorflow_SentiBank"]["Positive"]) + "' height='32' width='32'> <br><br>";
                  // Text,if any
                  if(text != ""){
                      inner_html += "<b>Text in image:</b> " + text + "<br><br>";
                  }
                  var i = 1;
                  // Sentiment per face
                  for (var key in senti['Faces']) {
                      if(i==1){
                        inner_html += "<b>Sentiment (from faces):</b> ";
                      }
                      inner_html += "<img src='" + which_icon(senti["Faces"][key]["Positive"]) + "' height='32' width='32'>";
                      i++;
                   }
                  if(i>1){
                    inner_html += "<br><br>";
                  }
                  if(senti['Average']){
                      inner_html += "<b>Average sentiment (from faces):</b> ";
                      inner_html += "<img src='" + which_icon(senti['Average']['Positive']) + "' height='32' width='32'> <br>";
                   }
                  var add_button = document.createElement("button");
                  add_button.innerHTML = "Potato";
                  add_button.onclick = function(){
                    // Sweet alert
                    swal({title: "<small>Helix\'s analysis</small>", text: inner_html, html: true }); 
                  };
                  elem.appendChild(add_button);
                }
            });
          }
        });
    });
  }
});
