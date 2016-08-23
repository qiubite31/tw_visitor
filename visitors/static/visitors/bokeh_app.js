var main = function() {
    $(".visitor_area").change(function(){
        alert($(".visitor_area").val())
        window.location.href = "http://localhost:8000/visitors/" + $(".visitor_area").val();
    });
}

$(document).ready(main);