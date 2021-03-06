//some needed global variables
var sse_div_id        = null;
var sse_event_source  = null;
//This function is to update a specific div
function httpSetDiv(div_id,theUrl)
{
    xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            document.getElementById(div_id).innerHTML=xmlHttp.responseText;
    }
    xmlHttp.open("GET", theUrl,false); // true for asynchronous
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
//this function to change active dropdown menu
function change_active_dropdown_menu(clicked_id)
{
  document.getElementById("active_dropdown_menu").innerHTML = clicked_id;
}
//this function is to change the active menu
function change_active_menu(clicked_id)
{
	var current_section = clicked_id;
	change_class(clicked_id);
	url = clicked_id.concat(".html");
	httpSetDiv("body_section",url);
	//close the old SSE stream
	if (sse_div_id != null)
	{
		closeSseConnection(sse_event_source);
	}
	//open a new SSE stream
	sseUpdateByID("temperature","/stream/"+clicked_id);
}
//this function is to update a specific variable in the page
function updateVariable(variable_id,value)
{
	document.getElementById(variable_id).innerHTML=value;
}

//Server Sent Events update div function
function sseUpdateByID(div_id,source)
{
	var eventSource = new EventSource(source);
	sse_div_id  = div_id;
	sse_event_source  = eventSource;
	eventSource.addEventListener("message", sseUpdateDivOperation);
}
function sseUpdateDivOperation()
{
	document.getElementById(sse_div_id).innerHTML = event.data;
}
//Close the SSE_Connection
function closeSseConnection(eventSource)
{
	//eventSource.removeEventListener("message", sseUpdateDivOperation);
	eventSource.close();
}
