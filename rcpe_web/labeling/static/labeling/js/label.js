pair_html = '<div class = "pair_wrapper"> \
	  <p><label class = "label_title">id = __pair_id__</label></p> \
	<div class = "sent_wrapper"> \
	  <input type="checkbox" id="not_reasonable">not reasonable pair</input>\
	  <input type="checkbox" id="too_complex">too complex</input>\
	  </div> \
	 <label class = "label_title"> reason:</label>\
	<div class = "sent_wrapper"> \
        __reason_sent__ \
	</div> \
	  <label class = "label_title">consequences:</label> \
	<div class = "sent_wrapper"> \
        __consequence_sent__  \
        </div> \
	<input type="button" value="Next" class="search_button" onclick="next_label()"  id="next_button"/> \
	 </div>'

word_html = '<input type="checkbox" id="__word_id__" >__word__</input>'


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

global_result = ''

function set_result(result)
{
    global_result = result
    pair_id = result['id']
    tph = pair_html
    tph = tph.replace('__pair_id__',pair_id)
    rws = ''
    reasons = result['r']
    reason_word = ''
    for (var i=0;i<reasons.length;i++)
    {
	for (var j=0;j<reasons[i].length;j++)
	{
	    id = 'r_'+i+'_'+j
	    wh = word_html.replace('__word_id__',id)
	    wh = wh.replace('__word__',reasons[i][j])
	    reason_word += wh
	}	
    }
    cons = result['c']
    con_word = ''
    for (var i=0;i<cons.length;i++)
    {
	for (var j=0;j<cons[i].length;j++)
	{
	    id = 'c_'+i+'_'+j
	    wh = word_html.replace('__word_id__',id)
	    wh = wh.replace('__word__',cons[i][j])
	    con_word += wh
	}	
    }
    tph = tph.replace('__reason_sent__',reason_word)
    tph = tph.replace('__consequence_sent__',con_word)
    document.getElementById('results_container').innerHTML = tph
}

function start_label()
{
    xmlhttp = new XMLHttpRequest()
    user = document.getElementById("user_name").value
    document.getElementById("user_name").readOnly = "readOnly"
    document.getElementById("change_user").style.display = "inline-block"
    url = "label_next.action"
    xmlhttp.onreadystatechange = function()
    {
	if (xmlhttp.readyState==4 && xmlhttp.status==200)
	{
	    result = eval('('+xmlhttp.responseText+')')
	    set_result(result)
	}
    }
    params = 'userName='+user
    xmlhttp.open("POST",url,true)
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    csrftoken = getCookie('csrftoken');
    xmlhttp.setRequestHeader('X-CSRFToken',csrftoken);
    //xmlhttp.setRequestHeader("Content-length", params.length);
    //xmlhttp.setRequestHeader("Connection", "close");
    xmlhttp.send(params)
}

function change_user_func()
{
    document.getElementById("user_name").readOnly = ""
    document.getElementById("change_user").style.display = "none"
}


function next_label()
{
    not_reasonable= document.getElementById('not_reasonable').checked
    too_complex = document.getElementById('too_complex').checked
    xmlhttp = new XMLHttpRequest()
    user = document.getElementById("user_name").value
    url = "label_next.action"

    xmlhttp.onreadystatechange = function()
    {
	if (xmlhttp.readyState==4 && xmlhttp.status==200)
	{
	    result = eval('('+xmlhttp.responseText+')')
	    set_result(result)
	}
    }
    params = 'userName='+user
    id = global_result['id']
    params += '&id='+id
    if (not_reasonable==true)
    {
	params +='&nr=1'
    }
    else if (too_complex==true)
    {
	params += '&tc=1'
    }
    else
    {
	o = {}
	o['id'] = id
	reasons = result['r']
	reasons_result = []
	for (var i=0;i<reasons.length;i++)
	{
	    temp = []
	    for (var j=0;j<reasons[i].length;j++)
	    {
		id = 'r_'+i+'_'+j
		c = document.getElementById(id).checked
		if (c == true)
		{
		    w = reasons[i][j]+'_:_I'
		}
		else
		{
		    w = reasons[i][j]+'_:_O'
		}
		temp.push(w)
	    }
	    reasons_result.push(temp)
	}
	cons = result['c']
	cons_result = []
	for (var i=0;i<cons.length;i++)
	{
	    temp = []
	    for (var j=0;j<cons[i].length;j++)
	    {
		id = 'c_'+i+'_'+j
		c = document.getElementById(id).checked
		if (c == true)
		{
		    w = cons[i][j]+'_:_I'
		}
		else
		{
		    w = cons[i][j]+'_:_O'
		}
		temp.push(w)
	    }	
	    cons_result.push(temp)
	}
	o['r'] = reasons_result
	o['c'] = cons_result
	params += '&label='+JSON.stringify(o)
    }

    xmlhttp.open("POST",url,true)
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    csrftoken = getCookie('csrftoken');
    xmlhttp.setRequestHeader('X-CSRFToken',csrftoken);
    //xmlhttp.setRequestHeader("Content-length", params.length);
    //xmlhttp.setRequestHeader("Connection", "close");
    xmlhttp.send(params)
}
