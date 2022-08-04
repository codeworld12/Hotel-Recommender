var closebtns = document.getElementsByClassName("close");
var close=document.getElementById("popup")
window.addEventListener('load',()=>{
    close.style.display="flex";
})

closebtns[0].addEventListener('click',(e)=>{
e.preventDefault()
close.style.display="none"
})