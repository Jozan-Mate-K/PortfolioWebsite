
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