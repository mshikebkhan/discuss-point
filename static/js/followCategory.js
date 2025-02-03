function followCategory(button) {
    var category_id = button.name;

    document.getElementById("id_category_follow_button_"+category_id).setAttribute( "onClick", "" );

    $("#id_category_follow_button_"+category_id).addClass("is-loading")

    $.ajax({
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        type:'POST',
        url: '../../../follow_category/'+category_id+'/',

        success:function(json){

            if(json.status == "followed"){

            $("#id_category_follow_button_"+category_id).html("Following")
            document.getElementById("id_category_follow_button_"+category_id).setAttribute( "class", "button is-small is-info");

            document.getElementById("id_category_follow_button_"+category_id).setAttribute( "onClick", "followCategory(this)" );


            var followers_count = document.getElementById("id_followers_count");
            var number = followers_count.innerHTML;
            number++;
            followers_count.innerHTML = number;


          } else if(json.status == "unfollowed"){
            $("#id_category_follow_button_"+category_id).html("Follow")
            document.getElementById("id_category_follow_button_"+category_id).setAttribute( "class", "button is-small is-light");

            document.getElementById("id_category_follow_button_"+category_id).setAttribute( "onClick", "followCategory(this)");

            var followers_count = document.getElementById("id_followers_count");
            var number = followers_count.innerHTML;
            number--;
            followers_count.innerHTML = number;

            }

        },
    });
}
