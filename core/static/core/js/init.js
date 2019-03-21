/*-----------------------------------------------------------------------------------
/*
/* Init JS
/*
-----------------------------------------------------------------------------------*/

jQuery(document).ready(function () {

    /*----------------------------------------------------*/
    /*	Navigation - Double Tap to Go
    ------------------------------------------------------*/

    $('#nav li:has(ul)').doubleTapToGo();

    /*----------------------------------------------------*/
    /*	Back To Top Button
    /*----------------------------------------------------*/
    var pxShow = 300; //height on which the button will show
    var fadeInTime = 400; //how slow/fast you want the button to show
    var fadeOutTime = 400; //how slow/fast you want the button to hide
    var scrollSpeed = 300; //how slow/fast you want the button to scroll to top. can be a value, 'slow', 'normal' or 'fast'

    // Show or hide the sticky footer button
    jQuery(window).scroll(function () {

        if (jQuery(window).scrollTop() >= pxShow) {
            jQuery("#go-top").fadeIn(fadeInTime);
        } else {
            jQuery("#go-top").fadeOut(fadeOutTime);
        }

    });

    // Animate the scroll to top
    jQuery("#go-top a").click(function () {
        jQuery("html, body").animate({scrollTop: 0}, scrollSpeed);
        return false;
    });


    /*----------------------------------------------------*/
    /*	Flexslider
    /*----------------------------------------------------*/
    $('#intro-slider').flexslider({
        namespace: "flex-",
        controlsContainer: "",
        animation: 'fade',
        controlNav: false,
        directionNav: true,
        smoothHeight: true,
        slideshowSpeed: 7000,
        animationSpeed: 600,
        randomize: false,
    });

    /*----------------------------------------------------*/
    /*	contact form
    ------------------------------------------------------*/



    $('form#contactForm button.submit').click(function () {

        let $spinner = $('#image-loader'), $form = $('#contactForm');
        let $warning_field = $('#message-warning'), $success_field = $('#message-success');

        $warning_field.fadeOut();
        $success_field.fadeOut();
        $spinner.fadeIn();

        let auth_type = $form.data('auth-type');
        let fields_ids = [];

        if (auth_type === 'reg'){
            fields_ids = ['#id_first_name', '#id_last_name', '#id_middle_name',
                              '#id_email', '#id_login', '#id_password', '#id_password_repeat'];
        }else
        if (auth_type === 'login') {
            fields_ids = ['#id_login', '#id_password'];
        }else{
            throw "Error: incorrect auth type for validation.";
        }

        let $fields = $(fields_ids.join(','), $form);
        let errors = validate_contact_form($fields, auth_type);

        if(errors.length !== 0) {
            $spinner.fadeOut();
            $warning_field.fadeIn();
            $warning_field.html("Форма заполнена неправильно:" + "<br>" + [...new Set(errors)].join("<br>"));
        }else{
            let data = [];
            $fields.each(function(){
                data.push(this.getAttribute('name') + '=' + this.value);
            });

            // trying to get csrf token:
            let token_field_name = "csrfmiddlewaretoken";
            let $token_field = $('[name='+token_field_name+']', $form);
            if($token_field.length === 1){
                data.push(token_field_name + '=' + $token_field.val());
            }
            data = data.join('&');

            $.ajax({
                type: "POST",
                url: "ajax/",
                data: data,
                success: function (msg) {
                    // Message was sent
                    $spinner.fadeOut();
                    if (msg === 'OK') {
                        $warning_field.hide();
                        $form.fadeOut();
                        $success_field.fadeIn();
                    }
                    // There was an error
                    else {
                        $warning_field.html("Форма заполнена неправильно:" + "<br>" + msg);
                        $warning_field.fadeIn();
                    }
                }
            });
        }
        return false;
    });

});



function validate_contact_form($fields) {
    let check = {
        login: /^[\w-.@+]{4,50}$/,
        name: /^([А-Яа-я]{1,50}|[A-Za-z]{1,50})$/,
        email: /^[A-Za-z][\w-.]{0,49}@[\w][\w.-]{3,49}$/,
        password: /^.{6,50}$/
    };
    let error_text = {
        login: " - Логин может состоять из английских символов, цифр, знака подчеркивания и иметь длину от 4 знаков.",
        name: " - В ФИО допустимы исключительно русские или исключительно английские символы.",
        email: " - Недействительный почтовый адрес.",
        password: " - Длина пароля должна быть не менее 6 символов.",
        pass_identity: " - Пароли должны совпадать.",
        empty: " - Обязательные поля должны быть заполнены."
    };

    let error_messages = [];
    $fields.each(function() {
        let $this = $(this), value = $this.val(), input_type=$this.data('type');

        this.setCustomValidity("");
        $this.removeClass('checked');
        if(value.length === 0){
            if(typeof($this.attr('required')) !== 'undefined'){
                this.setCustomValidity(error_text['empty']);
                error_messages.push(error_text['empty']);
            }
        }
        else {
            if(check[input_type].test(value) === false){
                this.setCustomValidity(error_text[input_type]);
                error_messages.push(error_text[input_type]);
            }
        }
        $this.addClass('checked');
    });
    // check for identity of passwords:
    let $passwords = $fields.filter(':password');
    if($passwords.first().val() !== $passwords.last().val()){
        $passwords.get(0).setCustomValidity(error_text['pass_identity']);
        $passwords.get(1).setCustomValidity(error_text['pass_identity']);
        $passwords.val('');
        error_messages.push(error_text['pass_identity']);
    }

    return error_messages;
}

