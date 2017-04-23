
// var app = chrome.runtime.getBackgroundPage();

function save() {
      chrome.tabs.executeScript(null, { file: "html2canvas.min.js" }, function() {
        chrome.tabs.executeScript(null, { file: "capture.js" }, function() {
            chrome.tabs.executeScript(null, { code: "capture_save()" })
        })
    }); 
}

function post() {
      chrome.tabs.executeScript(null, { file: "html2canvas.min.js" }, function() {
        chrome.tabs.executeScript(null, { file: "capture.js" }, function() {
            chrome.tabs.executeScript(null, { code: "capture_post()" })
        })
    }); 
}

document.getElementById('save').addEventListener('click', save);
document.getElementById('post').addEventListener('click', post);
