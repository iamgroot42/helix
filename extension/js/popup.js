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
            var access_token = "EAACEdEose0cBAMhBYEwF9UfdZBI0m5J2e01EBZA7JkmPNQ9tTGQ5UNGL6ZCaZCOGOj8Q4EZBLafYmzGnHmScyOw1lVc3lToSeevGHEWwa0eAUSmeHchM6jLuOeHUTHUXIQXMeIzTzIfsPHhYyd97zjFJFb3pgQ7uI7lSd9PPtSgZDZD";
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
                      // Convert png to jpg (if it is png) by simply renaming; FB allows that :)
                      if(image_url.lastIndexOf(".png") == image_url.length - 3){
                      	image_url = image_url.split(".png")[0] + ".jpg";
                      }
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
                          	var senti = obj['sentiment'];
                          	var tag = obj['tag'];
                          	var text = obj['text'];
                            var inner_html = "";
                            // Inceptionv3 tag
                            inner_html += "<b>" + tag['tag'] + "</b> (" + Math.round(100*tag['confidence']) + "% confidence)<br>";
                            // Sentibank model sentiment
                            if(senti["Tensorflow_SentiBank"]["Positive"] > senti["Tensorflow_SentiBank"]["Negative"])
                            {
                                inner_html += "<b>Positive sentiment</b> " + " (" + Math.round(100*senti["Tensorflow_SentiBank"]["Positive"]) + "% confidence)<br>";
                            }
                            else
                            {
                                inner_html += "<b>Negative sentiment</b> " + " (" + Math.round(100*senti["Tensorflow_SentiBank"]["Negative"]) + "% confidence)<br>";
                            }
                            // Text,if any
                            if(text != ""){
                                inner_html += "<b>Text in image:</b> " + text + "<br>";
                            }
                            var i = 1;
                            // Sentiment per face
                            for (var key in senti['Face']) {
                                inner_html += "<b>Face " + i.toString() + ": ";
                                if(senti["Face"][key]["Positive"] > senti["Face"][key]["Negative"])
                                {
                                    inner_html += "Positive sentiment</b> " + " (" + Math.round(100*senti["Face"][key]["Positive"]) + "% confidence)<br>";
                                }
                                else
                                {
                                    inner_html += "Negative sentiment</b> " + " (" + Math.round(100*senti["Face"][key]["Negative"]) + "% confidence)<br>";
                                }
                                i++;
                             }
                             if(senti['Face']['Average']){

                                inner_html += "<b>Average sentiment (from faces):</b> ";
                                if(senti['Face']['Average']['Positive'] > senti['Face']['Average']["Negative"])
                                {
                                    inner_html += "Positive " + " (" + Math.round(100*senti['Face']['Average']['Positive']) + "% confidence)<br>";
                                }
                                else
                                {
                                    inner_html += "Negative " + " (" + Math.round(100*senti['Face']['Average']["Negative"]) + "% confidence)<br>";
                                }
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
                  }
              });
            }
          }
        });
    });
  }
});
