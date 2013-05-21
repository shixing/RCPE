resultHtml = ' <!-- result __rank__ --> \
	<div class = "bus_wrapper" style="background-color: rgb(253,249,230);"> \
	  <div class = "content_left"> \
	    <div class = "name_top"> \
	      <label class="label_name">__name__</label> \
	    </div> \
	    <div class = "address_bottom"> \
	      <label class="label_street">__street__</label><p> \
	      <label class="label_city">__city__</lable> \
	    </div> \
	  </div> \
	  <div class = "links_right"> \
	    <div class = "link_yelp"> \
	      <a href="__href__" target="_blank"> \
		<img src="static/search/images/yelp_logo.png" alt="See in Yelp.com" height ="40px" style="float:right;"/> \
              </a> \
	    </div> \
            <p style="margin: 5px;"/> \
	    <div class = "link_pairs"> \
		<label class="label_pairs"> \
		  Found  <a href="#"><span style="font-size:20px;color:rgb(242,127,2)" onclick="showPairs(\'__BID__\')">__npair__</span></a> RC pairs! \
		</label> \
	    </div> \
	  </div> \
	  </div>'

yelp_url='http://www.yelp.com/search?find_desc=__name__&find_loc=__location__'

pairHTML = '<!-- pair __pair_rank__--> \
      <div class = "pair_wrapper"> \
	<div class = "pair_up"> \
	  <div class = "pair_show_review"> \
	      <a href="#"> \
	      <img src="static/search/images/green-plus.png" alt="Show Full Review" onclick="expand(\'__full_review_id__\')" width ="20px"/></a> \
	    </div> \
	  <div class = "pair_up_left"> \
	    <div class = "pair_rank"> \
	    <label class="label_rank">__pair_number__</label> \
	    </div> \
	  </div> \
	  <div class = "pair_up_right"> \
	    <div class = "reason"> \
	    __reason_1__ \
	    </div> \
	    <div class = "reason"> \
	      __reason_2__ \
	    </div> \
	    <div class = "consequence"> \
	    __consequence__ \
	    </div> \
	  </div> \
	</div> \
	<div class = "pair_down" id="__full_review_id__"> \
	  <div class ="full_review" > \
	    __full_review_html__ \
	  </div> \
	</div> \
      </div>'



function searchBusiness()
{
    xmlhttp = new XMLHttpRequest()
    name = document.getElementById("query_name").value
    address = document.getElementById("query_address").value
    city = '' //document.getElementById("query_city").value
    url = 'search.action'
    connection = '?'
    if (name != '')
    {
	url += connection+'name='+name
	connection = '&'
    }
    if (address != '')
    {
	url += connection+'address='+address
    	connection = '&'
    }
    if (city != '')
    {
	url += connection+'city='+city
    }

    xmlhttp.onreadystatechange = function()
    {
	if (xmlhttp.readyState==4 && xmlhttp.status==200)
	{
	    htmlStr = ''
	    results = eval('('+xmlhttp.responseText+')')
	    for (var i = 0;i<results.length;i++)
		{
		    result = results[i]
		    temp = resultHtml
		    temp = temp.replace('__rank__',i.toString())
		    temp = temp.replace('__name__', result['name'])
		    temp = temp.replace('__BID__', result['BID'])
		    street = result['full_addr']
		    temp_url = yelp_url.replace('__name__',encodeURI(result['name']))
		    temp_url = temp_url.replace('__location__',encodeURI(result['full_addr']))
		    ss = street.split('\n')
		    street = ss[0]
		    city = ss[1]
		    temp = temp.replace('__street__', street)
		    temp = temp.replace('__city__', city)
		    temp = temp.replace('__npair__',result['npair'])
		    temp = temp.replace('__href__',temp_url)
		    htmlStr += temp
		}
	    document.getElementById("results_container").innerHTML= htmlStr
	}
    }
    xmlhttp.open("GET",url,true)
    xmlhttp.send()
}

c = 0;
function showPairs(bid)
{
    xmlhttp = new XMLHttpRequest()
    xmlhttp.onreadystatechange = function()
    {
	if (xmlhttp.readyState==4 && xmlhttp.status==200)
	{
	    tempHtml = '';
	    results = eval('('+xmlhttp.responseText+')')
	    for (var i=0;i<results.length;i++)
	    {
		temp = pairHTML;
		temp = temp.replace('__pair_rank__',i.toString())
		pair_number = (i+1).toString();
		if (i+1<10)
		{
		    pair_number = '0'+pair_number;
		}
		temp = temp.replace('__pair_number__',pair_number)
		result = results[i]
		clauses = result['clauses']
		has_clauses = true;
		if (clauses.length == 0)
		{
		    has_clauses = false;
		    clauses = ['Sorry, full review currently is not available.']
		}
		consequence = result['consequence'][0][0]
		consequence_id = result['consequence'][0][1]
		if (has_clauses)
		    clauses[consequence_id] = '<span class="span_red">'+clauses[consequence_id]+'</span>'
		reason1 = result['reason'][0][0]
		reason1_id = result['reason'][0][1]
		if (has_clauses)
		    clauses[reason1_id] = '<span class="span_green">'+clauses[reason1_id]+'</span>'
		reason2 = ' '
		if (result['reason'].length>=2)
		{
		    reason2 = result['reason'][1][0];
		    reason2_id = result['reason'][1][1];
		    if (has_clauses)
			clauses[reason2_id] = '<span class="span_green">'+clauses[reason2_id]+'</span>';
		}
		full_review = '';
		for (var j = 0;j<clauses.length;j++)
		{
		    full_review+=clauses[j]+' ';
		}
		temp = temp.replace('__reason_1__',reason1);
		temp = temp.replace('__reason_2__',reason2);
		temp = temp.replace('__consequence__',consequence);
		temp = temp.replace('__full_review_html__',full_review);
		full_review_id = 'full_review_'+i.toString();
		temp = temp.replace(/__full_review_id__/g,full_review_id);
		tempHtml += temp;

	    }
	    $("#pairs_window")[0].innerHTML = tempHtml;
	    loadingOn()
	}
    }
    url = 'searchRC.action?bid='+bid
    xmlhttp.open("GET",url,true)
    xmlhttp.send()
}

function loadingOn()
{
    $('#shadow').fadeIn(300);
}

function loadingOff()
{
   $('#shadow').fadeOut(100);
}


function expand(id)
{
    div = document.getElementById(id)
    if (div.style.display =="block" )
    {
	div.style.display = "none"
    }
    else
    {
	div.style.display = "block"
    }
}

function searchRCPair()
{
    xmlhttp = new XMLHttpRequest()
    reason = document.getElementById('query_reason').value
    consequence = document.getElementById('query_consequence').value
    url = 'searchRCPair.action'
    connection = '?'
    if (reason != '')
    {
	url += connection+'r='+reason
	connection = '&'
    }
    if (consequence != '')
    {
	url += connection+'c='+consequence
    }
    xmlhttp.onreadystatechange = function()
    {
	if (xmlhttp.readyState==4 && xmlhttp.status==200)
	{
	    tempHtml = '';
	    results = eval('('+xmlhttp.responseText+')')
	    for (var i=0;i<results.length;i++)
	    {
		temp = pairHTML;
		temp = temp.replace('__pair_rank__',i.toString())
		pair_number = (i+1).toString();
		if (i+1<10)
		{
		    pair_number = '0'+pair_number;
		}
		temp = temp.replace('__pair_number__',pair_number)
		result = results[i]
		clauses = result['clauses']
		has_clauses = true;
		if (clauses.length == 0)
		{
		    has_clauses = false;
		    clauses = ['Sorry, full review currently is not available.']
		}
		consequence = result['consequence'][0][0]
		consequence_id = result['consequence'][0][1]
		if (has_clauses)
		    clauses[consequence_id] = '<span class="span_red">'+clauses[consequence_id]+'</span>'
		reason1 = result['reason'][0][0]
		reason1_id = result['reason'][0][1]
		if (has_clauses)
		    clauses[reason1_id] = '<span class="span_green">'+clauses[reason1_id]+'</span>'
		reason2 = ' '
		if (result['reason'].length>=2)
		{
		    reason2 = result['reason'][1][0];
		    reason2_id = result['reason'][1][1];
		    if (has_clauses)
			clauses[reason2_id] = '<span class="span_green">'+clauses[reason2_id]+'</span>';
		}
		full_review = '';
		for (var j = 0;j<clauses.length;j++)
		{
		    full_review+=clauses[j]+' ';
		}
		temp = temp.replace('__reason_1__',reason1);
		temp = temp.replace('__reason_2__',reason2);
		temp = temp.replace('__consequence__',consequence);
		temp = temp.replace('__full_review_html__',full_review);
		full_review_id = 'full_review_'+i.toString();
		temp = temp.replace(/__full_review_id__/g,full_review_id);
		tempHtml += temp;

	    }
	    $("#results_container")[0].innerHTML = tempHtml;
	}
    }
    xmlhttp.open("GET",url,true)
    xmlhttp.send()
}

