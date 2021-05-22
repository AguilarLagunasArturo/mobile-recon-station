function send(msg){
  var url = 'localhost/#state';
  var xhr = new XMLHttpRequest();
  xhr.open('POST', url, true);
  xhr.setRequestHeader("Content-Type", "application/mobile-recon-station; charset=UTF-8");
  xhr.send('param1='+msg);
  console.log(msg);
}
