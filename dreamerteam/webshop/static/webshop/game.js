function updateScore(){
  console.log("called");
  var destination = getDomain() + "/games/highscore/"+gameID+"/";
  var csrftoken = getCookie('csrftoken');

  function getScores(){
  $.ajax({
    url : destination, // the endpoint,commonly same url
    type : "POST", // http method
    data : {
    username : username,
    csrfmiddlewaretoken : csrftoken
  }, // data sent with the post request
     // handle a successful response
     success : function(json) {
     console.log(json); // another sanity check
     //On success show the data posted to server as a message
     console.log(json.highscore);

    if ( $( ".user_hs" ).length ) {
      $('.user_hs').html(json.highscore);
    }
    else {
      $('.user_hs_container').append("</br> user_highscore: <span class='user_hs'>"+json.highscore+"</span>");
    }
    if ( $( ".global_hs" ).length ) {
      $('.global_hs').html(json.global_highscore);
    }
    else{
      $('.global_hs_container').append("</br> global_highscore: <span class='global_hs'> "+json.global_highscore+"</span>");
    }
   },

 // handle a non-successful response
     error : function(xhr,errmsg,err) {
     //console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
   }
 });
}
  setTimeout(getScores, 1000);
}

function getDomain(){
  var url = window.location.href;
  var arr = url.split("/");
  var result = arr[0] + "//" + arr[2];
  return result;
}
function displayScore(score){

}
function displayPopUp(message){
  alert(message);
}
function saveScore(score){
  var destination = getDomain() + "/games/highscore/";
  var csrftoken = getCookie('csrftoken');
  $.ajax({
    url : destination, // the endpoint,commonly same url
    type : "POST", // http method
    data : { gameID : gameID,
    username : username,
    score : score,
    csrfmiddlewaretoken : csrftoken
  }, // data sent with the post request
     // handle a successful response
     success : function(json) {
     //console.log(json); // another sanity check
     //On success show the data posted to server as a message

   },

 // handle a non-successful response
     error : function(xhr,errmsg,err) {
     //console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
   }
 });

}
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
    // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function saveStates(json_text){
  //console.log(gameID + ", "+username +"," + json_text);
  //save to the database
  var destination = getDomain() + "/games/save/";
  //console.log("destination : "+ destination);
  var csrftoken = getCookie('csrftoken');
  $.ajax({
    url : destination, // the endpoint,commonly same url
    type : "POST", // http method
    data : { gameID : gameID,
    username : username,
    json_text : json_text,
    csrfmiddlewaretoken : csrftoken
  }, // data sent with the post request
     // handle a successful response
     success : function(json) {
     //console.log(json); // another sanity check
     //On success show the data posted to server as a message
     displayPopUp("Game saved!");
   },

 // handle a non-successful response
     error : function(xhr,errmsg,err) {
     //console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
   }
 });
}

function loadStates(){

  //save to the database
  var destination = getDomain() + "/games/load/";
  //console.log("destination : "+ destination);
  var csrftoken = getCookie('csrftoken');
  $.ajax({
    url : destination, // the endpoint,commonly same url
    type : "POST", // http method
    data : { gameID : gameID,
    username : username,
    csrfmiddlewaretoken : csrftoken
  }, // data sent with the post request
     // handle a successful response
     success : function(json) {
     //console.log(json); // another sanity check
     //On success show the data posted to server as a message

      var message={};
      message.messageType ="LOAD";
      message.gameState = JSON.parse(json);

      //var iframContent = $(".game-iframe").contentWindow;
      //iframContent.postMessage(message,"www.example.com");
      var targetFrame = document.getElementById("targetFrame");
      targetFrame.contentWindow.postMessage(message,"*");
      displayPopUp("Game loaded!");
   },

 // handle a non-successful response
     error : function(xhr,errmsg,err) {
     //console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
   }
 });
}


function listener(event){
  //if ( event.origin !== "http://javascript.info" )
    //return
  //console.log(event.data);
  switch (event.data.messageType){
    case "SETTING":
      //setting height and weight
      var height = event.data.options.height + "px";
      $('.game-iframe').height(height);
      var width = event.data.options.width + "px";
      $('.game-iframe').css("max-width",width);
      break;

    case "SAVE":
      //stringify the gmestats object
      var save_json_text = JSON.stringify(event.data.gameState);
      saveStates(save_json_text);
      break;

    case "LOAD_REQUEST":
      //load the data from the database
      loadStates();
      //send the data to the game
      break;
    case "SCORE":
      //console.log(event.data.score);
      updateScore();
      displayPopUp("Score Submitted!");
      displayScore(event.data.score);
      saveScore(event.data.score);


      break;
    case "ERROR":
      $('.errorDiv').html(event.data.info);
      $('.errorDiv').removeClass("invisible");
      $('.game-iframe').addClass("invisible");
      break;
    default:
        return;
  }

}

if (window.addEventListener){
  addEventListener("message", listener, false);
} else {
  attachEvent("onmessage", listener);
}
