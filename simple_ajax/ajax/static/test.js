$(document).ready(function() {
    $("#form_id").change(function(){
        let name = $(this).val();

        $.post('/e/macid/test_ajax/'
               ,{ 'name' : name}
               ,function(data,status) {
                   console.log("The reponse was " + data.new_name + "\n with status " + status);
               }
              );
    });
});
