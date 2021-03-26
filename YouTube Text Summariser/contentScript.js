chrome.runtime.onMessage.addListener((message, callback) => {
  if (message == "generate"){
    chrome.scripting.executeScript({
      file: 'app.py'
    });
  }
});

