$(document).ready(function() {
    $("#form_id").change(function(){
        let name = $(this).val();

        $.post('/e/macid/test_ajax/'
               ,{ 'name' : name}
               ,function(data,status) {
                   $("#post_out").text(data.new_name);
                   console.log("The reponse was " + data.new_name + "\n with status " + status);
               }
              );
    });
});
