function deleteProject(ownerID, projectname){
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        type: "POST",
        url: ownerID +"/"+projectname+"/delete/",
        data: {},
        headers: {"X-CSRFToken": csrftoken},
        dataType: 'json'
    })
    .done(deleteSucces)
    .fail(deleteFail);
}

function deleteSucces(response){

    location.reload(true);
}

function deleteFail (response){
    console.log(response);
    errorhappen = errorTemplate.replace("%ERROR_HERE%", "Unkown error occured and project could not be deleted.");
    $("body").prepend(errorhappen);
}

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

var errorTemplate = `<div class="alert alert-danger fade show" role="alert">
<button type="button" class="close" data-dismiss="alert" aria-label="Close">
    <span aria-hidden="true">&times;</span>
</button>
%ERROR_HERE%
</div>`