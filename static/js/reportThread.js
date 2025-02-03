function reportThread(button) {
    var thread_id = button.name;

    document.getElementById("id_thread_report_button_"+thread_id).setAttribute( "onClick", "" );

    $("#id_thread_report_a_"+thread_id).addClass("is-idle");
    $("#id_thread_report_button_"+thread_id).addClass("is-loading");

    $.ajax({
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        type:'POST',
        url: '../../../report_thread/'+thread_id+'/',

        success:function(json){

            if(json.status == "reported"){

            $("#id_thread_report_button_"+thread_id).html("Reported")
            document.getElementById("id_thread_report_button_"+thread_id).setAttribute( "class", "button is-small is-danger is-idle");

            setTimeout(function() {
                alert('Thread has been reported successfully! Our team will check it.')
                 },10)

          } else if(json.status == "already_reported"){
            $("#id_thread_report_button_"+thread_id).html("Reported")
            document.getElementById("id_thread_report_button_"+thread_id).setAttribute( "class", "button is-small is-danger is-idle");

            setTimeout(function() {
                alert('Thread is already reported! Refresh the page if it is not showing "Reported".')
                 },10)

            } else if(json.status == "not_exists"){
                $("#id_thread_"+thread_id).addClass("is-hidden");
                setTimeout(function() {
                alert('This thread does not exists.');
                },10)
            }

        },
    });
}
