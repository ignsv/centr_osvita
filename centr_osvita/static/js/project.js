/* Project specific Javascript goes here. */
if ($("#time").length) {
  const renderTimer = (min, sec) => {
    if (min < 10) {
      min = "0" + min;
    }
    if (sec < 10) {
      sec = "0" + sec;
    }
    $("#timer").html(`${min}:${sec}`);
  };
  $("#timeoutModal").on("hide.bs.modal", e => {
    window.location.replace($("#timeout-results").attr("href"));
  });

  let time = +$("#time").html();
  let minutes = Math.floor(time / 60);
  let seconds = time - minutes * 60;
  renderTimer(minutes, seconds);

  let timer = setInterval(function() {
    if (seconds > 0) {
      seconds--;
    } else if (seconds == 0 && minutes > 0) {
      seconds = 59;
      minutes--;
    } else {
      clearInterval(timer);
      $("#timeoutModal").modal("toggle");
    }
    renderTimer(minutes, seconds);
  }, 1000);
}
