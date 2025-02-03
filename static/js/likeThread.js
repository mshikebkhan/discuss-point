function likeThread(button) {
    var thread_id = button.name;

    document.getElementById("id_thread_like_button_"+thread_id).setAttribute( "onClick", "" );

    $("#id_thread_like_button_"+thread_id).addClass("is-loading")

    $.ajax({
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        type:'POST',
        url: '../../../like_thread/'+thread_id+'/',

        success:function(json){

            if(json.status == "liked"){

            $("#id_thread_like_button_"+thread_id).html("Liked")
            document.getElementById("id_thread_like_button_"+thread_id).setAttribute( "class", "button is-small is-info");

            document.getElementById("id_thread_like_button_"+thread_id).setAttribute( "onClick", "likeThread(this)" );

            if (document.getElementById("id_thread_likes_count_"+thread_id)){
            var id_thread_likes_count = document.getElementById("id_thread_likes_count_"+thread_id);
            var number = id_thread_likes_count.innerHTML;
            number++;
            id_thread_likes_count.innerHTML = number;
            }

          } else if(json.status == "unliked"){
            $("#id_thread_like_button_"+thread_id).html("Like")
            document.getElementById("id_thread_like_button_"+thread_id).setAttribute( "class", "button is-small is-light");

            document.getElementById("id_thread_like_button_"+thread_id).setAttribute( "onClick", "likeThread(this)");

            if (document.getElementById("id_thread_likes_count_"+thread_id)){
            var id_thread_likes_count = document.getElementById("id_thread_likes_count_"+thread_id);
            var number = id_thread_likes_count.innerHTML;
            number--;
            id_thread_likes_count.innerHTML = number;
            }

            }

          else if(json.status == "not_exists"){
            $("#id_thread_"+thread_id).addClass("is-hidden");
            setTimeout(function() {
                alert('This thread does not exist.')
                 },10)


          }

        },
    });
}
