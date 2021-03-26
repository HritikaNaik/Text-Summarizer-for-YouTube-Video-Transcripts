chrome.browserAction.onClicked.addListener(IconClicked);
function IconClicked(tab)
{
	let msg = {
		txt : "Icon Clicked!"
	}
	chrome.tabs.sendMessage(tab.id, msg);
}