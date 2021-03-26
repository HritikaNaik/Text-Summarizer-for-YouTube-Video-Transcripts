document.getElementById("summarize").addEventListener("click",myFunction);
function myFunction() {
  chrome.runtime.sendMessage({"message":"generate"});
}
chrome.runtime.onMessage.addListener(
 function(request, sender, sendResponse) {
   if( request.message === "result" ) {
       var sum = request.data;
       //$('#YSummarize-form div:last').after('<div class="myDiv">' + sum + '</div>' );
       document.getElementById("myDiv").innerHTML = "<br><br><input type='text' name='mytext" + sum+ "></br></br>"
   }
  }
);

