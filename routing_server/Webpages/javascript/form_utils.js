function check_and_submit_form(form,fields){
    check_form_fields(fields);
    document.getElementById(form).submit();
}

function check_form_fields(fields){
    var clear = true;

    for (field of fields){
        element = document.getElementById(field);
        if (element.value.trim() == ''){
            document.getElementById(field+'_error').style.display="block";
            clear = false;
        }else{
            document.getElementById(field+'_error').style.display="none";
        }
    }
    return clear;
}