function Toggle(){
    let form = document.getElementById("emailForm");
    if(form.classList.contains("active")){
        form.classList.remove("active");
    }else{
        form.classList.add("active");
    }
}
function Hide(){
    let container = document.getElementById("emailContainer");
    if(!container.classList.contains('hidden')){
        container.classList.add("hidden");
    }
}
function Show(){
    let container = document.getElementById("emailContainer");
    container.classList.remove("hidden");
}