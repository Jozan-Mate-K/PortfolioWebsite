//The front end recieves the json file and creates a post based on it

function ShowNextPost(title,date,contents,id){
    document.getElementById("revealContainer").innerHTML += '<div onclick="LoadComments('+ id +')" class="reveal forumButton"><div><h1>' + title + '</h1><p style="border: 0; font-style: italic;">' + date + '</p></div><p>'+ contents + '</p></div><div id="'+ id +'" class="commentContainer"></div>';
}
function LoadComments(id){
    document.getElementById(id).classList.add("show");
}
function asd(){

    ShowNextPost('I Eat ass on the daily', 'Every day faggot', 'Weewoooweeeewooooweeeoooowoooowoowwo', '0' );
    ShowNextPost('asd', '2023.09.12', 'Mirror Mirror on the wall, give me torture, cock and ball', '1' );
    ShowNextPost('I just cant anymore', 'never', 'Swallowed shampoo, probably gonna die', '2' );
    ShowNextPost('Nooo', '2001.10.02', 'balls? I lick em ', '3' );
}