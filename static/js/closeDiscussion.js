function closeDiscussion(button) {
    var discussion_id = button.name;

    document.getElementById("id_discussion_close_button_"+discussion_id).setAttribute( "onClick", "" );

    $("#id_discussion_close_button_"+discussion_id).addClass("is-loading")

    $.ajax({
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        type:'POST',
        url: '../../../close_discussion/'+discussion_id+'/',

        success:function(json){

            if(json.status == "closed"){

            $("#id_discussion_close_button_"+discussion_id).html("Closed")
            document.getElementById("id_discussion_close_button_"+discussion_id).setAttribute( "class", "button is-small is-danger");

            document.getElementById("id_discussion_close_button_"+discussion_id).setAttribute( "onClick", "closeDiscussion(this)" );

            setTimeout(function() {
                alert('Discussion has been closed successfully! No new threads will be submitted in this discussion.')
                 },10)

          } else if(json.status == "open"){
            $("#id_discussion_close_button_"+discussion_id).html("Close")
            document.getElementById("id_discussion_close_button_"+discussion_id).setAttribute( "class", "button is-small is-light");

            document.getElementById("id_discussion_close_button_"+discussion_id).setAttribute( "onClick", "closeDiscussion(this)");

            }
           else if(json.status == "not_exists"){
              $("#id_discussion_"+discussion_id).addClass("is-hidden");
              setTimeout(function() {
              alert('This discussion does not exists.');
              },10)
          }

        },
    });
}
