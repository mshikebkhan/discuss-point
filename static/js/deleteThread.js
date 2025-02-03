function deleteThread(button) {
    var thread_id = button.name;
    var x = confirm('Are you sure you want to delete this thread?');

    if (x) {
        $("#id_thread_" + thread_id).addClass("is-hidden");

        $.ajax({
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            type: 'POST',
            url: '../../../delete_thread/' + thread_id + '/',

            success: function(json) {


                if (json.status == "deleted") {

                  if (document.getElementById("id_thread_" + thread_id)) {

                    var thread = document.getElementById("id_thread_" + thread_id);
                    thread.remove();
                  }

                    if (document.getElementById("id_threads_count")) {
                        var id_threads_count = document.getElementById("id_threads_count");
                        var number = id_threads_count.innerHTML;
                        number--;
                        id_threads_count.innerHTML = number;
                    }



                    if (document.getElementById("id_empty_message")) {
                        var id_threads_count = document.getElementById("id_threads_count");
                        var number = id_threads_count.innerHTML;
                        if (number == 0) {
                            var x = "<center>" +
                                '<img src="../../static/images/empty-folder.png" style="height: 100px; width: 100px;">' +
                                "<br>No threads submitted." +
                                "</center>"
                            $("#id_empty_message").html(x)
                        }

                    }

                    setTimeout(function() {
                        alert('Thread has been deleted successfully! Please refresh the page if it is still appearing on the page.')
                    }, 10)

                } else if (json.status == "not_exists") {
                    setTimeout(function() {
                        alert('This thread does not exists.');
                    }, 10)
                }

            },
        });
    };
}
