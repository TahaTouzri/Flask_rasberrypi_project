//This function is to update a specific div 
function httpSetDiv(div_id,theUrl)
{
    xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            document.getElementById(div_id).innerHTML=xmlHttp.responseText;
    }
    xmlHttp.open("GET", theUrl, true); // true for asynchronous 
    xmlHttp.send(null);
}
//this function is to implement a polling update
function pollUpdateDiv(div_id,theUrl,time_stamp)
{
	setInterval( function() { httpSetDiv(div_id,theUrl); }, time_stamp );
}
//this function is to change the active menu class
function change_class(clicked_id)
{
	$("#menu>li.active").removeClass("active");
	document.getElementById(clicked_id).className = "active";
}
//this function is to change the active menu
function change_active_menu(clicked_id)
{
	var current_section = clicked_id;
	change_class(clicked_id);
	url = clicked_id.concat(".html");
	httpSetDiv("body_section",url);
	//----------------------------------------------------------------
	//Need to stop the old event if exist before starting the new one
	//----------------------------------------------------------------
	sseUpdateDiv("temperature","/stream/"+clicked_id);
}
//this function is to update a specific variable in the page
function updateVariable(variable_id,value)
{
	document.getElementById(variable_id).innerHTML=value;
}

//Server Sent Events update div function
function sseUpdateDiv(div_id,source)
{
	var eventSource = new EventSource(source);
	eventSource.addEventListener("message", function(event) 
	{
		document.getElementById(div_id).innerHTML = event.data;
	}
	);
}