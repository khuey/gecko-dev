var u8array = new Uint8Array([1,2,3]);
var xhr = new XMLHttpRequest();

xhr.open("post", "testXHR.txt");
xhr.send(u8array);
postMessage("sent");
