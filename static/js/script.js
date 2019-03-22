function addClass() {
    var element = document.getElementById("dolphin");
    element.classList.add("dolphinStyle");
    setTimeout(function(){
      submitForm(); 
      }, 800);
 }
 function submitForm() {
  document.getElementById("myForm").submit();
}
 function myMove() {
    var elem = document.getElementById("dolphin");  
    elem.style.backgroundImage = url('../img/dolphin.png');
    var pos = 0;
    var id = setInterval(frame, 5);
    function frame() {
      if (pos == 200) {
        clearInterval(id);
      } else {
        pos+=4; 
        elem.style.bottom = pos + "px"; 
      }
    }
  }