function reportDiscussion(button) {
    var discussion_id = button.name;

    document.getElementById("id_discussion_report_button_"+discussion_id).setAttribute( "onClick", "" );

    $("#id_discussion_report_a_"+discussion_id).addClass("is-idle");
    $("#id_discussion_report_button_"+discussion_id).addClass("is-loading");

    $.ajax({
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        type:'POST',
        url: '../../../report_discussion/'+discussion_id+'/',

        success:function(json){

            if(json.status == "reported"){

            $("#id_discussion_report_button_"+discussion_id).html("Reported")
            document.getElementById("id_discussion_report_button_"+discussion_id).setAttribute( "class", "button is-small is-danger is-idle");

            setTimeout(function() {
                alert('Discussion has been reported successfully! Our team will check it.')
                 },10)

          } else if(json.status == "already_reported"){
            $("#id_discussion_report_button_"+discussion_id).html("Reported")
            document.getElementById("id_discussion_report_button_"+discussion_id).setAttribute( "class", "button is-small is-danger is-idle");

            setTimeout(function() {
                alert('Discussion is already reported! Refresh the page if it is not showing "Reported".')
                 },10)

            } else if(json.status == "not_exists"){
                $("#id_discussion_"+discussion_id).addClass("is-hidden");
                setTimeout(function() {
                alert('This discussion does not exists.');
                },10)
            }

        },
    });
}
