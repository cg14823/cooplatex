$(".panel-left").resizable({
    handleSelector: ".splitter",
    resizeHeight: false
});

$( document ).ready(
    function(){
        var newlineCounter = 9;
        $("#linedtext").keydown(function(event){
            if(event.which == 13) {
                newlineCounter += 1;
                if(newlineCounter == 10) {
                    saveSource();
                    newlineCounter = 0;
                }
            }
        });
    }
);

function compile () {
    var csrftoken = getCookie('csrftoken');
    console.log(csrftoken)
    $.ajax({
        type:"POST",
        url: "compile/",
        data:{},
        headers: {"X-CSRFToken": csrftoken},
        dataType: 'json'
    })
    .done(compileSuccess)
    .fail(errorF);
}

function compileSuccess(response){
    if (response.status == 200) {
        $("#container2").empty();
        if (response.link != ""){
            templatePdf = pdfTemplate.replace("%LINK_HERE%", response.link);
            templatePdf = templatePdf.replace("%LINK_HERE%", response.link);
            templatePdf = templatePdf.replace("%LINK_HERE%", response.link);
            $("#container2").empty();
            $("#container2").append(templatePdf);
        }
        else{
            // there was probably an error
        }
    }
    else {
        $("#container2").empty();
        $("#container2").append(response.error_message);
    }
}
function saveSource() {
    var text = $("#linedtext").val();
    var csrftoken = getCookie('csrftoken');
    console.log(csrftoken)
    $.ajax({
        type:"POST",
        url: "save/",
        data:{"file":text},
        headers: {"X-CSRFToken": csrftoken},
        dataType: 'json'
    })
    .done(success)
    .fail(errorF);
}

function success (response){
    console.log("hey");
}

function errorF(errorResponse){
    console.log("fuck");
}

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

var pdfTemplate = '<object data="%LINK_HERE%" type="application/pdf" width="100%" height="100%"> <iframe src="%LINK_HERE%" width="100%" height="100%" style="border: none;">This browser does not support PDFs. Please download the PDF to view it: <a href="%LINK_HERE%">Download PDF</a></iframe></object>'