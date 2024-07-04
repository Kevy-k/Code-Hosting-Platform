<script src="js/jquery.min.js"></script>

function checkPass() {
    var password=document.registerform.pass.value;
    var confirmpass=document.registerform.conpass.value;
    if(confirmpass!=password)
    {
        alert("Hello");
    }
}

$(document).ready(function(){
    $("#confpin").keyup(checkPass);
});