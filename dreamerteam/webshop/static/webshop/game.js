
function error(error_message){
  var message={};
  message.messageType ="ERROR";
  message.info = error_message;

  var targetFrame = document.getElementById("targetFrame");
  targetFrame.contentWindow.postMessage(message,"*");
}

function updateScore(){

  var destination = getDomain() + "/games/highscore/"+gameID+"/";
  var csrftoken = getCookie('csrftoken');

  function getScores(){
  $.ajax({
    url : destination,
    type : "POST",
    data : {
    username : username,
    csrfmiddlewaretoken : csrftoken
  },
     success : function(json) {
     testData = jQuery.parseJSON(json.top_10);
     $(".top_10_list").remove();

     $.each(testData,function() {
           var username = this.fields.username;
           var highScore = this.fields.highScore;
           // check if top10 list exists:
           $('.top_10_list_ul').append(
             "<li class='list-group-item top_10_list'>"+
             username+" : " + highScore +"</li>");
     });
   },
     error : function(xhr,errmsg,err) {
       error(xhr.responseText);
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

//save or load or sore
function displayPopUp(message){
  var selector = ".message_"+message;
  $(selector).fadeIn();
  setTimeout(function(){
    $(selector).fadeOut();
  }, 3000);
}

function saveScore(score){

  var destination = getDomain() + "/games/highscore/";
  var csrftoken = getCookie('csrftoken');

  $.ajax({
    url : destination,
    type : "POST",
    data : { gameID : gameID,
    username : username,
    score : score,
    csrfmiddlewaretoken : csrftoken
  },
     success : function(json) {
   },
     error : function(xhr,errmsg,err) {
       error(xhr.responseText);
   }
 });

}

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function saveStates(json_text){

  var destination = getDomain() + "/games/save/";
  var csrftoken = getCookie('csrftoken');
  $.ajax({
    url : destination,
    type : "POST",
    data : { gameID : gameID,
    username : username,
    json_text : json_text,
    csrfmiddlewaretoken : csrftoken
  },
     success : function(json) {
     displayPopUp("save");
   },
     error : function(xhr,errmsg,err) {
       error(xhr.responseText);
   }
 });
}

function loadStates(){
  //save to the database
  var destination = getDomain() + "/games/load/";
  var csrftoken = getCookie('csrftoken');
  $.ajax({
    url : destination,
    type : "POST",
    data : { gameID : gameID,
    username : username,
    csrfmiddlewaretoken : csrftoken
  },
     success : function(json) {
      var message={};
      message.messageType ="LOAD";
      message.gameState = JSON.parse(json);

      var targetFrame = document.getElementById("targetFrame");
      targetFrame.contentWindow.postMessage(message,"*");
      displayPopUp("load");

   },
     error : function(xhr,errmsg,err) {
       error(xhr.responseText);
   }
 });
}

function listener(event){

  switch (event.data.messageType){
    case "SETTING":
      //setting height and width of the iframe
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
      updateScore();
      displayPopUp("score");
      saveScore(event.data.score);
      break;

    case "ERROR":
      $(".message_error").fadeIn();
      $(".message_error strong").html(event.data.info);
      $('.game-iframe').addClass("nodisplay");
      break;

    default:
        return;
  }
}
$( document ).ready(function() {
  // Handler for .ready() called.
  if (window.addEventListener){
    addEventListener("message", listener, false);
  } else {
    attachEvent("onmessage", listener);
  }

});
