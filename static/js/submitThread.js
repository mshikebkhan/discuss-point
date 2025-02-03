// Add thread on discussion

function submitThread(button) {
    var discussion_id = button.name;
    $("#id_submit_thread_submit_button").prop("disabled", true);
    $("#id_submit_thread_submit_button").addClass('is-loading');

    $.ajax({
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        type:'POST',
        url:'../../../submit_thread/'+discussion_id+'/',
        data:{
            content:$('#id_thread_content').val(),
        },
        success:function(json){

            $("#id_submit_thread_submit_button").removeClass('is-loading');
            $("#id_submit_thread_submit_button").prop("disabled", false);

            if(json.status == "submitted"){

                    var newthread =
                    '<div id="id_new_thread"></div>'+
                    '<div id="id_thread_'+json.id+'" class="card" style="margin-top: 30px;">'+
                    '	<header class="card-header">'+
                    '		<p class="card-header-title">'+
                    '			<a style="color: inherit" href="/profile">'+
                    json.user+
                    '			</a>'+
                    '		</p>'+
                    '		<span style="cursor: default;" class="card-header-icon is-small is-light ">1&nbsp;minute ago</span>'+
                    '	</header>'+
                    '	<div class="card-content">'+
                    '		<div class="content">'+
                    '			<p class="subtitle is-size-5 is-size-6-mobile">'+
                    json.content+
                    '			</p>'+
                    '			<div class="control">'+
                    '				<div class="tags has-addons">'+
                    '					<span class="tag is-dark">Likes</span>'+
                    '					<span class="tag is-info">0</span>'+
                    '				</div>'+
                    '			</div>'+
                    '		</div>'+
                    '	</div>'+
                    '	<footer class="card-footer">'+
                    '		<a class="card-footer-item">'+
                    '		<button onclick="deleteThread(this)" name="'+json.id+'" class="button is-small is-light">Delete</button>'+
                    '		</a>'+
                    '		<a class="card-footer-item">'+
                    '		<button onclick="saveThread(this)" id="id_thread_save_button_'+json.id+'" name="'+json.id+'" class="button is-small is-light">Save</button>'+
                    '		</a>'+
                    '	</footer>'+
                    '</div>';

                document.getElementById("id_submit_thread_form").reset();

                if (document.getElementById("id_new_thread")){
                $("#id_new_thread").before(newthread);
                }
                else {
                    $("#id_for_empty").html(newthread);
                    $("#id_empty_threads_message").remove();

                }

                var threads_count = document.getElementById("id_threads_count");
                var number = threads_count.innerHTML;
                number++;
                threads_count.innerHTML = number;


                setTimeout(function() {
                alert('Your thread has been submitted successfully!')
                },10)

            } else if(json.status == "error"){
                alert("An error occured!");

            }else if(json.status == "not_exists"){
                alert("Discussion does not exists.");

            }else if(json.status == "closed"){
                alert("Discussion has been closed! new threads will not submitted.");

            }
        },

    });

};
