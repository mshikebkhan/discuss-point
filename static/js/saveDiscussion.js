function saveDiscussion(button) {
    var discussion_id = button.name;

    document.getElementById("id_discussion_save_button_"+discussion_id).setAttribute( "onClick", "" );

    $("#id_discussion_save_button_"+discussion_id).addClass("is-loading")

    $.ajax({
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        type:'POST',
        url: '../../../save_discussion/'+discussion_id+'/',

        success:function(json){

            if(json.status == "saved"){

            $("#id_discussion_save_button_"+discussion_id).html("Saved")
            document.getElementById("id_discussion_save_button_"+discussion_id).setAttribute( "class", "button is-small is-success");

            document.getElementById("id_discussion_save_button_"+discussion_id).setAttribute( "onClick", "saveDiscussion(this)" );

            if (document.getElementById("id_saved_discussions_count")){
            var id_saved_discussions_count = document.getElementById("id_saved_discussions_count");
            var number = id_saved_discussions_count.innerHTML;
            number++;
            id_saved_discussions_count.innerHTML = number;
            }

          } else if(json.status == "removed"){
            $("#id_discussion_save_button_"+discussion_id).html("Save")
            document.getElementById("id_discussion_save_button_"+discussion_id).setAttribute( "class", "button is-small is-light");

            document.getElementById("id_discussion_save_button_"+discussion_id).setAttribute( "onClick", "saveDiscussion(this)");

            if (document.getElementById("id_saved_discussions_count")){
            var id_saved_discussions_count = document.getElementById("id_saved_discussions_count");
            var number = id_saved_discussions_count.innerHTML;
            number--;
            id_saved_discussions_count.innerHTML = number;
            }

            } else if(json.status == "not_exists"){
                $("#id_discussion_"+discussion_id).addClass("is-hidden");
                setTimeout(function() {
                alert('This discussion does not exists.');
                },10)
            }

        },
    });
}
