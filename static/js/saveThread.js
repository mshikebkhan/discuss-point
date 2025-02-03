function saveThread(button) {
    var thread_id = button.name;

    document.getElementById("id_thread_save_button_"+thread_id).setAttribute( "onClick", "" );

    $("#id_thread_save_button_"+thread_id).addClass("is-loading")

    $.ajax({
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        type:'POST',
        url: '../../../save_thread/'+thread_id+'/',

        success:function(json){

            if(json.status == "saved"){

            $("#id_thread_save_button_"+thread_id).html("Saved")
            document.getElementById("id_thread_save_button_"+thread_id).setAttribute( "class", "button is-small is-success");

            document.getElementById("id_thread_save_button_"+thread_id).setAttribute( "onClick", "saveThread(this)" );

            if (document.getElementById("id_saved_threads_count")){
            var id_saved_threads_count = document.getElementById("id_saved_threads_count");
            var number = id_saved_threads_count.innerHTML;
            number++;
            id_saved_threads_count.innerHTML = number;
            }

          } else if(json.status == "removed"){
            $("#id_thread_save_button_"+thread_id).html("Save")
            document.getElementById("id_thread_save_button_"+thread_id).setAttribute( "class", "button is-small is-light");

            document.getElementById("id_thread_save_button_"+thread_id).setAttribute( "onClick", "saveThread(this)");

            if (document.getElementById("id_saved_threads_count")){
            var id_saved_threads_count = document.getElementById("id_saved_threads_count");
            var number = id_saved_threads_count.innerHTML;
            number--;
            id_saved_threads_count.innerHTML = number;
            }

            } else if(json.status == "not_exists"){
                $("#id_thread_"+thread_id).addClass("is-hidden");
                setTimeout(function() {
                alert('This thread does not exists.');
                },10)
            }

        },
    });
}
