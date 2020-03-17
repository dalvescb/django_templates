$(document).ready(function() {
    // respond to form submission
    function onSubmit(event){
        // stop form from submitting normally
        event.preventDefault();

        let form = $(this);
        let name = form.find("input[name='fname']").val();
        let json_data = { 'name' : name };
        let url_path = '/e/macid/test_ajax/';

        $.post(url_path,
               json_data,
               handleResponse
              );
    }

    // handle Json Response from form POST
    function handleResponse(data,status) {
        $("#h1_id").text("Name Evaluation Recieved: " + data.new_name);
        // console.log("The reponse was " + data.new_name + "\n with status " + status);
    }

    // when form submit buttons is clicked, call onSubmit
    $("#form_id").submit(onSubmit);
});
