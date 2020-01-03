document.getElementById("forgot-form").style.display="none";
    $('.message a').click(function(){
      $('form').animate({height: "toggle", opacity:"toggle"},"slow");
      document.getElementById("forgot-form").style.display="none";
    });
	 $('#forgot_password').click(function(){
          $('form').animate({height: "toggle", opacity:"toggle"},"slow");
          document.getElementsByClassName("reg-form")[0].style.display="none";
        });
     $('#back_to_login').click(function(){
          $('form').animate({height: "toggle", opacity:"toggle"},"slow");
          document.getElementsByClassName("reg-form")[0].style.display="none";
          document.getElementById("forgot-form").style.display="none";
        });
    function validate_reg_form()
    {
        var a=document.forms["reg_form"]["username"].value;
        var b=document.forms["reg_form"]["password"].value;
        var c=document.forms["reg_form"]["email"].value;
        if (a=="" || b=="" || c=="")
        {
            alert("Please Fill All Required Field");
            return false;
        }
        var ctObj = CryptoJS.AES.encrypt(document.forms["reg_form"]["email"].value, "some password");
        document.forms["reg_form"]["email"].value = ctObj.toString();
        var ctObj = CryptoJS.AES.encrypt(document.forms["reg_form"]["password"].value, "some password");
        document.forms["reg_form"]["password"].value = ctObj.toString();
        var ctObj = CryptoJS.AES.encrypt(document.forms["reg_form"]["username"].value, "some password");
        document.forms["reg_form"]["username"].value = ctObj.toString();
        return true;
    }

    function validate_log_form()
    {
        var a=document.forms["log_form"]["password"].value;
        var b=document.forms["log_form"]["email"].value;

        if(a=="" || b=="")
        {
            alert("Please Fill All Required Field");
            return false;
        }
        var ctObj = CryptoJS.AES.encrypt(document.forms["log_form"]["email"].value, "some password");
        document.forms["log_form"]["email"].value = ctObj.toString();
        var ctObj = CryptoJS.AES.encrypt(document.forms["log_form"]["password"].value, "some password");
        document.forms["log_form"]["password"].value = ctObj.toString();
        return true;
    }
    function validate_forgot_form()
    {
        var a = document.forms["forgot_form"]["forgot_email"].value;
        if(a=="")
        {
           alert("Please Fill All Required Field");
            return false;
        }
        var ctObj = CryptoJS.AES.encrypt(document.forms["forgot_form"]["forgot_email"].value, "some password");
        document.forms["forgot_form"]["forgot_email"].value = ctObj.toString();
        return true;
    }
