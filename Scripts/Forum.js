//The front end recieves the json file and creates a post based on it

function ShowNextPost(title,date,contents,id){
    document.getElementById("revealContainer").innerHTML += '<div onclick="LoadComments('+ id +')" class="reveal forumButton"><div><h1>' + title + '</h1><p style="border: 0; font-style: italic;">' + date + '</p></div><p>'+ contents + '</p></div><div id="'+ id +'" class="commentContainer"></div>';
}
function LoadComments(id){
    document.getElementById(id).classList.add("show");
}