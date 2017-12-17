$(".panel-left").resizable({
    handleSelector: ".splitter",
    resizeHeight: false
});
var filesBody = {};
var userChange = true;
$( document ).ready(
    function(){
        $("#save-success-alert").hide();
        var insertCounter = 0;
        var insertCadence = 50;
        editor.getSession().on('change', function(e){
            if (!userChange) return;
            console.log("USERCAHNGE");
            var currentElemt = $("#files").find(".currentfile");
            filesBody[currentElemt.attr('id')].body = editor.getValue();
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

        $("#files li").each(function(idx, el){
            if (el.id.indexOf("-other") === -1){
                filesBody[el.id] = {body: $("#"+el.id+"-body").text(),  name:$("#"+el.id+"-body").attr('name')}
            }
        })
        console.log(filesBody)
    }
);

function unimplmented() {
    alert("Sorry this options are currently unimplmented")
}

function toggleOtherFiles(id){
    console.log("UNIMPLEMENTED");
    alert("At the moment you can not preview images")
}
function toggleFiles(id){
    var currentElemt = $("#files").find(".currentfile")
    filesBody[currentElemt.attr('id')].body = editor.getValue();
    console.log("TOGGLE", filesBody)
    userChange = false;
    editor.getSession().setValue("",-1)

    $("#files > li").removeClass("currentfile");
    $("#files > li").removeClass("unselectedfile");
    var classObject = '#'+id;

    $(classObject).removeClass("unselectedfile");
    $(classObject).addClass("currentfile");
    editor.setValue(filesBody[id].body,-1);
    userChange = true;
}

function newFile() {
    $("#newFileError").css("display", "none");
    console.log("got to newfile");
    var newfilename = $("#file-name-input").val();
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
        fname = response.newfilename.replace(".","");
        templateNewFile = newFileTemplate.replace("{{f.name_id}}", fname);
        templateNewFile = templateNewFile.replace("{{f.name_id}}", fname);
        templateNewFile = templateNewFile.replace("{{f.name_id}}", fname);
        templateNewFile = templateNewFile.replace("{{f.name}}", response.newfilename);
        templateNewFile = templateNewFile.replace("{{f.name}}", response.newfilename);
        //console.log("appending: ", templateNewFile);
        $("#files").append(templateNewFile);
        filesBody[fname] ={name: response.newfilename, body:""};
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
    .fail(compileFail);
}

function compileFail(){
    $.jGrowl("Compilation Failed, Logs not available in this version", {life:1000, theme:'error', position:'top-left'});
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

    $.ajax({
        type:"POST",
        url: "save/",
        data:JSON.stringify(filesBody),
        headers: {"X-CSRFToken": csrftoken},
        dataType: 'json'
    })
    .done(done)
    .fail(fail);
}

function success (response){
    console.log("SAVE:", response);
    $.jGrowl("Project saved!", {life:1000, theme:'manilla', position:'top-left'});
}

function errorF(errorResponse){
    $.jGrowl("Action failed :(", {life:1000, theme:'error', position:'top-left'});
}


function uploadFile(){
    var fdata = new FormData();
    fdata.append("file", document.getElementById('id_file_source').files[0])
    var csrftoken = getCookie('csrftoken');
    console.log(fdata);
    $.ajax({
        type:"POST",
        url: "uploadFile/",
        data: fdata,
        cache: false,
        processData: false, // Don't process the files
        contentType: false,
        headers: {"X-CSRFToken": csrftoken},
        dataType: 'json'
    })
    .done(fileAdded)
    .fail(errorF);
}

function fileAdded(response){
    $.jGrowl("File added!", {life:1000, theme:'manilla', position:'top-left'});
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
var newFileTemplate = `<li id="{{f.name_id}}" class="unselectedfile list-group-item" onclick='toggleFiles("{{f.name_id}}")'>{{f.name}}</li><span style="display:none" name="{{f.name}}" id="{{f.name_id}}-body"></span>`

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
        }file_name
    
        window.open(sUrl, '_blank');
        return true;
    }
    
    window.downloadFile.isChrome = navigator.userAgent.toLowerCase().indexOf('chrome') > -1;
    window.downloadFile.isSafari = navigator.userAgent.toLowerCase().indexOf('safari') > -1;

