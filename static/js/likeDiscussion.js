function likeDiscussion(button) {
    var discussion_id = button.name;

    document.getElementById("id_discussion_like_button_"+discussion_id).setAttribute( "onClick", "" );

    $("#id_discussion_like_button_"+discussion_id).addClass("is-loading")

    $.ajax({
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        type:'POST',
        url: '../../../like_discussion/'+discussion_id+'/',

        success:function(json){

            if(json.status == "liked"){

            $("#id_discussion_like_button_"+discussion_id).html("Liked")
            document.getElementById("id_discussion_like_button_"+discussion_id).setAttribute( "class", "button is-small is-info");

            document.getElementById("id_discussion_like_button_"+discussion_id).setAttribute( "onClick", "likeDiscussion(this)" );

            if (document.getElementById("id_discussion_likes_count_"+discussion_id)){
            var id_discussion_likes_count = document.getElementById("id_discussion_likes_count_"+discussion_id);
            var number = id_discussion_likes_count.innerHTML;
            number++;
            id_discussion_likes_count.innerHTML = number;
            }

          } else if(json.status == "unliked"){
            $("#id_discussion_like_button_"+discussion_id).html("Like")
            document.getElementById("id_discussion_like_button_"+discussion_id).setAttribute( "class", "button is-small is-light");

            document.getElementById("id_discussion_like_button_"+discussion_id).setAttribute( "onClick", "likeDiscussion(this)");

            if (document.getElementById("id_discussion_likes_count_"+discussion_id)){
            var id_discussion_likes_count = document.getElementById("id_discussion_likes_count_"+discussion_id);
            var number = id_discussion_likes_count.innerHTML;
            number--;
            id_discussion_likes_count.innerHTML = number;
            }

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
