$(".panel-left").resizable({
    handleSelector: ".splitter",
    resizeHeight: false
});

$( document ).ready(
    function(){
        var insertCounter = 0;
        var insertCadence = 50;
        editor.getSession().on('change', function(e){
            if ("insert"=== e.action){
                insertCounter ++;
                if (insertCounter % insertCadence === 0){
                    saveSource()                
                }
            }
        });

        $(".splitter-files").click(function (){
            $(".panel-file-view").toggleClass('active');
        });

        $("#new-file-form").on('submit', function(event){
            event.preventDefault();
            console.log("submit clicked");
            newFile();
        });

        $("#newFileModal").on("hidden.bs.modal", function(event){
            $("#newFileError").css("display", "none");
            $("#file-name-input").val("");
        });
    }
);

function newFile() {
    $("#newFileError").css("display", "none");
    console.log("got to newfile");
    var newfilename = $("#filename-input").val();
    console.log(newfilename);
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        type: "POST",
        url: "newfile/",
        data: {"filename": newfilename}, //Put relevant form data into this with appropriate names to handled in the view
        headers: {"X-CSRFToken": csrftoken},
        dataType: 'json'
    })
    .done(newFileSuccess)
    .fail(newFileFailure);
}

function newFileSuccess (response) {
    if (response.status == 200) {
        $("#newFileModal").modal().hide();
        $('body').removeClass('modal-open');
        $('.modal-backdrop').remove();
        $("#file-name-input").val("");
        // append new file to list on file view
        templateNewFile = newFileTemplate.replace("%FILE_NAME_PLACEHOLDER%", response.newfilename);
        //console.log("appending: ", templateNewFile);
        $("#files").append(templateNewFile);
        // console.log("appended");
    }
}

function newFileFailure (response) {
    if (response.status == 422) {
        console.log("Filename was invalid");
        $("#newFileError").css("display", "inline");
    }
}

function compile () {
    var csrftoken = getCookie('csrftoken');
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
function saveSource(done=success, fail=errorF) {
    var text = editor.getValue();
    var csrftoken = getCookie('csrftoken');
    console.log(csrftoken)
    $.ajax({
        type:"POST",
        url: "save/",
        data:{"file":text},
        headers: {"X-CSRFToken": csrftoken},
        dataType: 'json'
    })
    .done(done)
    .fail(fail);
}

function success (response){
    console.log("Saved");
}

function errorF(errorResponse){
    console.log("Not saved");
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

function downloadPdf() {
    var csrftoken = getCookie('csrftoken');

    $.ajax({
        type:"POST",
        url: "getpdf/",
        data:{},
        headers: {"X-CSRFToken": csrftoken},
        dataType: 'json'
    })
    .done(gotPdf)
    .fail(pdfFail);
}

function gotPdf (response) {
    console.log("here");
    downloadFile(response.Link);
}

function pdfFail (jqXHR, textStatus, erroThrown){
    console.log(jqXHR, textStatus, erroThrown);
    if (jqXHR.status == 404) {
        var responseText = jQuery.parseJSON(jqXHR.responseText);
        alert(responseText.Error);
    }
}

var csrftoken = getCookie('csrftoken');

var pdfTemplate = '<object data="%LINK_HERE%" type="application/pdf" width="100%" height="100%"> <iframe src="%LINK_HERE%" width="100%" height="100%" style="border: none;">This browser does not support PDFs. Please download the PDF to view it: <a href="%LINK_HERE%">Download PDF</a></iframe></object>'

window.downloadFile = function (sUrl) {
    
        //iOS devices do not support downloading. We have to inform user about this.
        if (/(iP)/g.test(navigator.userAgent)) {
           //alert('Your device does not support files downloading. Please try again in desktop browser.');
           window.open(sUrl, '_blank');
           return false;
        }
    
        //If in Chrome or Safari - download via virtual link click
        if (window.downloadFile.isChrome || window.downloadFile.isSafari) {
            //Creating new link node.
            var link = document.createElement('a');
            link.href = sUrl;
            link.setAttribute('target','_blank');
    
            if (link.download !== undefined) {
                //Set HTML5 download attribute. This will prevent file from opening if supported.
                var fileName = sUrl.substring(sUrl.lastIndexOf('/') + 1, sUrl.length);
                link.download = fileName;
            }
    
            //Dispatching click event.
            if (document.createEvent) {
                var e = document.createEvent('MouseEvents');
                e.initEvent('click', true, true);
                link.dispatchEvent(e);
                return true;
            }
        }
    
        // Force file download (whether supported by server).
        if (sUrl.indexOf('?') === -1) {
            sUrl += '?download';
        }
    
        window.open(sUrl, '_blank');
        return true;
    }
    
    window.downloadFile.isChrome = navigator.userAgent.toLowerCase().indexOf('chrome') > -1;
    window.downloadFile.isSafari = navigator.userAgent.toLowerCase().indexOf('safari') > -1;