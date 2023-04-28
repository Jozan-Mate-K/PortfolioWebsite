
function Reveal (){
    var reveals = document.querySelectorAll('.reveal');
    for (let i = 0; i < reveals.length; i++) {
        var windowHeight = window.innerHeight;
        var revealTop = reveals[i].getBoundingClientRect().top;
        var revealBottom = reveals[i].getBoundingClientRect().bottom;
        var revealPoint = 200;



        if(revealTop < windowHeight - revealPoint){
            reveals[i].classList.add("active");
        }else{
            reveals[i].classList.remove("active");
        } 
        if(revealBottom < revealPoint){
            reveals[i].classList.remove("active");
        }
    }
}