
$(function() {
    
    $(".delete-button").click(function () {
        var id = $(this).parent().closest('div[id]').attr('id');
        console.log(id);
        delete_article(id)
    });

	$('#article-form').on('submit', function(event){
	    event.preventDefault();
	    console.log("form submitted!")  // sanity check
	    create_article();
	});

    function delete_article(id) {
        console.log("delete article is working!");
        $.ajax({
            url : "/delete/".concat(id), 
            type : "GET", 

            // handle a successful response
            success : function(json) {
                console.log(json); 

                if(json.hasOwnProperty('Error')){
                    console.log("Error!")
                    $('#error').html(json.Error);
                } else {
                    var element = document.getElementById(id);
                    element.parentNode.removeChild(element);
                }
        
            },

    
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); 
                console.log(xhr.status + ": " + xhr.responseText); 
            }
        });
    };

		// AJAX for posting
	function create_article() {
	    console.log("create article is working!") 
	    $.ajax({
	        url : "/create_article/", 
	        type : "POST", 
	        data : { url : $('#url').val() }, 

	        // handle a successful response
	        success : function(json) {
			    $('#url').val(''); 
			    console.log(json); 

                if(json.hasOwnProperty('Error')){
                    console.log("Error!");
                    $('#error').html(json.Error);
                }

			    else {
                    console.log("Sucess!");
                    $('#error').html('Success! Your link has been posted!');

                    $('#add-card').prepend(
                    "  <div class='ui card'>"+
                    "    <div class='image'>"+
                    "      <img src='"+ json.article_image +"'>"+
                    "    </div>"+
                    "    <div class='content'>" +
                    "      <div class='header'>"+
                    "        <a href='"+ json.article_url+"'> "+ json.article_title+" </a>"+
                    "      </div>"+
                    "      <div class='meta'>"+
                    "        <a class='group'>"+ json.article_site_name+"</a>"+
                    "      </div>"+
                    "      <div class='description'>"+
                    "        "+ json.article_description +" <br><br>"+
                    "        Posted by <a href='/profile/"+ json.article_user_id+"/'> "+ json.article_user+" </a> <br><br>"+
                    "        "+ json.article_pub_date+
                    "      </div>"+
                    "    </div>"+
                    "    <div class='ui two bottom attached buttons'>"+
                    "      <div class='ui button'>"+
                    "        Like"+
                    "      </div>"+
                    "      <div class='ui button'>"+
                    "        Delete"+
                    "      </div>"+
                    "    </div>"+
                    "  </div>"
                );
                }
        
			},

	
	        error : function(xhr,errmsg,err) {
	            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
	                " <a href='#' class='close'>&times;</a></div>"); 
	            console.log(xhr.status + ": " + xhr.responseText); 
	        }
	    });
	};

    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});