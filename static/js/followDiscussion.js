function followDiscussion(button) {
    var discussion_id = button.name;

    document.getElementById("id_discussion_follow_button_"+discussion_id).setAttribute( "onClick", "" );

    $("#id_discussion_follow_button_"+discussion_id).addClass("is-loading")

    $.ajax({
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        type:'POST',
        url: '../../../follow_discussion/'+discussion_id+'/',

        success:function(json){

            if(json.status == "followed"){

            $("#id_discussion_follow_button_"+discussion_id).html("Following")
            document.getElementById("id_discussion_follow_button_"+discussion_id).setAttribute( "class", "button is-rounded is-small is-primary");

            document.getElementById("id_discussion_follow_button_"+discussion_id).setAttribute( "onClick", "followDiscussion(this)" );




          } else if(json.status == "unfollowed"){
            $("#id_discussion_follow_button_"+discussion_id).html("Follow")
            document.getElementById("id_discussion_follow_button_"+discussion_id).setAttribute( "class", "button is-rounded is-small is-light");

            document.getElementById("id_discussion_follow_button_"+discussion_id).setAttribute( "onClick", "followDiscussion(this)");



            }

            else if(json.status == "not_exists"){
              $("#id_discussion_"+discussion_id).addClass("is-hidden");
              setTimeout(function() {
                  alert('This discussion does not exist.')
                   },10)


            }

        },
    });
}
