function create_project(){
    console.log("HERE");
    var name = $("#project-name-input").val();
    if (name.length < 3 || !(/^[a-zA-Z][0-9a-zA-Z_]+$/.test(name))){
        show_failure("Invalid project name. It must have at least 3 characters and start with a letter");
        return;
    }
    var crsftoken = $("input[name=csrfmiddlewaretoken]").val();
    console.log(crsftoken);
    $.ajax({
        type: "POST",
        url: "create/",
        data: {"name":name},
        headers: {"X-CSRFToken": crsftoken},
        success: show_success,
        error: show_failure("Unknown error occuered please try later"),
    });
}

function show_success(response){
    console.log(response);
    if (response.statusCode == 200){
        $("#project-created").toggleClass("none-display");
        window.location.href= "/dash/";
        return;
    }

    show_failure(response.error_message);
}

function show_failure(message){
    //window.location.href= "/dash/";
    
    console.log("failed");
    $("#titleModal").modal('hide');
    $("#error-alert").toggleClass("none-display");
    $("#creationError").text(message);
}