function addClass() {
    var element = document.getElementById("dolphin");
    element.classList.add("dolphinStyle");
    setTimeout(function(){
      element.classList.remove("dolphinStyle");
      submitForm(); 
      }, 800);
      
 }
 function submitForm() {
  document.getElementById("myForm").submit();
}

  document.write("<div><h1 class=\"title\" style=\"font-family: cursive;color: black;font-size: 20px;font-weight: bolder; position:fixed;right:10px;bottom:10px;\">Chainrocker</h1></div>");