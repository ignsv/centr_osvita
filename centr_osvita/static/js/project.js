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

if ($("#id_institution_type").length) {
  let input = $("#id_institution_type");

  const handleInstitutionInput = () => {
    if (input.val() == 0 || input.val() == 3) {
      $("#id_grade").css("display", "none");
      $("#id_grade").prop("disabled", true);
      $("#label_for_institution").text("Навчальний заклад");
      if ($("#institution_container").hasClass("col-md-6")) {
        $("#institution_container").toggleClass("col-md-6 col-md-8");
      }
    } else {
      $("#id_grade").css("display", "block");
      $("#id_grade").prop("disabled", false);
      $("#label_for_institution").text("Навчальний заклад та клас");
      if ($("#institution_container").hasClass("col-md-8")) {
        $("#institution_container").toggleClass("col-md-8 col-md-6");
      }
    }
  };

  handleInstitutionInput();

  input.change(e => {
    handleInstitutionInput();
  });
}
