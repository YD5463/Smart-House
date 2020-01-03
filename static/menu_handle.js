alert("Hello "+document.cookie.split('=')[1]);

document.getElementById("change_password_form").style.display="none";

function show_form(to_show)
{
    if(to_show==1)
    {
        document.getElementById("change_password_form").style.display="block";
    }
    else
    {
        document.getElementById("change_password_form").style.display="none";
    }
}
function openNav()
{
    document.getElementById("mySidenav").style.width = "250px";
}

function closeNav()
{
    document.getElementById("mySidenav").style.width = "0";
}

function record()
{
    navigator.mediaDevices.getUserMedia({
        audio: true
    })
  .then(stream => {
    const aCtx = new AudioContext();
    const streamSource = aCtx.createMediaStreamSource(stream);
    var rec = new Recorder(streamSource);
    rec.record();
    setTimeout(() => {
        stream.getTracks().forEach(t => t.stop());
        rec.stop();
        rec.exportWAV((blob) => {
        // now we could send this blob with an FormData too
         var fd = new FormData();
        fd.append('fname', 'test.wav');
        fd.append('data', blob);
        $.ajax({
        type: 'POST',
        url: '/input_speech_to_text_request',
        data: fd,
        processData: false,
        contentType: false
        }).done(function(data) {
            console.log(data);
        });

        });
    }, 4000);
    })
}

function openForm() {
  document.getElementById("myForm").style.display = "block";
}
function closeForm() {
  document.getElementById("myForm").style.display = "none";
}
function CheckOption() {
    var Device_type = $('#Device_type').find(":selected").text();
    if(Device_type=="Tv")
    {
        alert("Tv");
    }
    if(Device_type=="Ac")
    {
        alert("Ac");
    }
    if(Device_type=="Light")
    {
        alert("Light");
    }
}

function validate_add_form()
{
    if(document.forms["add_device"]["Device_name"].value == "")
    {
        alert("Please fill the device name field!");
        return false;
    }
    return true;
}
