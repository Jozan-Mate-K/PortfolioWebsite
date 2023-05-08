function Reveal (){
    var reveals = document.querySelectorAll('.reveal');
    for (let i = 0; i < reveals.length; i++) {
        var windowHeight = window.innerHeight;
        var revealTop = reveals[i].getBoundingClientRect().top;
        var revealBottom = reveals[i].getBoundingClientRect().bottom;
        var revealPoint = 150;



        if(revealTop < windowHeight - revealPoint){
            reveals[i].classList.add("active");
        }else{
            
            if(reveals[i].classList.contains("show")){
                reveals[i].innerHTML = "";
                reveals[i].classList.remove("show");    
            }
            reveals[i].classList.remove("active");
        } 
        if(revealBottom < revealPoint){
            reveals[i].classList.remove("active");
        }
    }
}

function Scrolled (){
    const element = document.getElementById("contentContainer");
    var delta = (element.scrollTop / (element.scrollHeight - element.clientHeight))* window.innerWidth;
    document.documentElement.style.setProperty('--scroll', -delta  + 'px');
}
onmousemove = function(e){
    document.documentElement.style.setProperty('--x', -e.clientX  + 'px');
    var a = e.clientX / this.window.innerWidth;
    var xPercent = (2 * a)-1;
    document.documentElement.style.setProperty('--xPercent', xPercent);
}