function reportProfile(button) {
    var profile_id = button.name;

    document.getElementById("id_profile_report_button_"+profile_id).setAttribute( "onClick", "" );

    $("#id_profile_report_a_"+profile_id).addClass("is-idle");
    $("#id_profile_report_button_"+profile_id).addClass("is-loading");

    $.ajax({
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        type:'POST',
        url: '../../../report_profile/'+profile_id+'/',

        success:function(json){

            if(json.status == "reported"){

            $("#id_profile_report_button_"+profile_id).html("Reported")
            document.getElementById("id_profile_report_button_"+profile_id).setAttribute( "class", "button is-small is-danger is-idle");

            setTimeout(function() {
                alert('Profile has been reported successfully! Our team will check it.')
                 },10)

          } else if(json.status == "already_reported"){
            $("#id_profile_report_button_"+profile_id).html("Reported")
            document.getElementById("id_profile_report_button_"+profile_id).setAttribute( "class", "button is-small is-danger is-idle");

            setTimeout(function() {
                alert('Profile is already reported! Refresh the page if it is not showing "Reported".')
                 },10)

            } else if(json.status == "not_exists"){
                $("#id_profile_"+profile_id).addClass("is-hidden");
                setTimeout(function() {
                alert('This profile does not exists.');
                },10)
            }

        },
    });
}
