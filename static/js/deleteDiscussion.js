function deleteDiscussion(button) {
    var discussion_id = button.name;
    var x = confirm('Are you sure you want to delete this discussion?');

    if (x) {
        $("#id_discussion_" + discussion_id).addClass("is-hidden");

        $.ajax({
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            type: 'POST',
            url: '../../../delete_discussion/' + discussion_id + '/',

            success: function(json) {


                if (json.status == "deleted") {

                  if (document.getElementById("id_discussion_" + discussion_id)) {

                    var discussion = document.getElementById("id_discussion_" + discussion_id);
                    discussion.remove();
                  }

                    if (document.getElementById("id_discussions_count")) {
                        var id_discussions_count = document.getElementById("id_discussions_count");
                        var number = id_discussions_count.innerHTML;
                        number--;
                        id_discussions_count.innerHTML = number;
                    }

                    if (document.getElementById("id_empty_message")) {
                        var id_discussions_count = document.getElementById("id_discussions_count");
                        var number = id_discussions_count.innerHTML;
                        if (number == 0) {
                            var x = "<center>" +
                                '<img src="../../static/images/empty-folder.png" style="height: 100px; width: 100px;">' +
                                "<br>No discussions created." +
                                "</center>"
                            $("#id_empty_message").html(x)
                        }

                    }

                    setTimeout(function() {
                        alert('Discussion has been deleted successfully! Please refresh the page if it is still appearing on the page.')
                    }, 10)

                } else if (json.status == "not_exists") {
                    setTimeout(function() {
                        alert('This discussion does not exists.');
                    }, 10)
                }

            },
        });
    };
}
