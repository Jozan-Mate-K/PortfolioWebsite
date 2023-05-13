function changePassword(){
    let old_pass = document.getElementById("oldPass").value;
    let new_pass = document.getElementById("newPass").value;
    let conf_new_pass = document.getElementById("confNewPass").value;
    let responseField = document.getElementById("response");
    let endpoint = "/changePassword";
    let body = {
        'username': localStorage.getItem('name'),
        'token': localStorage.getItem('token'),
        'oldPass': md5(old_pass),
        'newPass': md5(new_pass)
    };
    let method = 'POST'
    document.getElementById("oldPass").value = "";
    document.getElementById("newPass").value = "";
    document.getElementById("confNewPass").value = "";
    //STRENGTH CHECK

    if(new_pass != conf_new_pass){
        responseField.innerHTML = "New passwords don't match";
        return;
    }
    if(new_pass == old_pass){
        responseField.innerHTML = "New password cannot be old password";
        return;
    }
    if(new_pass.length < 8){
        responseField.innerHTML = "The password has to be longer than 8 characters";
        return;
    } 
    if(!new_pass.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/)){
        responseField.innerHTML = "The password has to have both uppercase and lowercase letters";
        return;
    }
    if(!new_pass.match(/([0-9])/)){
        responseField.innerHTML = "The password has to have numeric digits";
        return;
    }
    
    SendChangePass(endpoint, body, method);
}

async function SendChangePass(endpoint, _body, _method){
    let responseField = document.getElementById("response");

    try{

        let res = await fetch(backendIp + endpoint, {
            headers: {
                'Accept': 'aplication/json',
                'Content-Type': 'application/json'
            },
            method: _method,
            body: JSON.stringify(_body)
        });
        
        let data = await res.json();

        if(data['data'] == 'fail'){
            responseField.innerHTML = "Please log in again";
        }else if(data['data'] == 'wrongPass'){
            responseField.innerHTML = "Wrong old Password"; 
        }else{
            responseField.innerHTML = "Password successfully changed!";
        }

    }catch(e){
        console.error(e);
    }
}

function Invite(){
    let endpoint = "/invite";
    let newUserName = document.getElementById("newUserName").value;
    let body = {
        'name' : newUserName,
        'username': localStorage.getItem('name'),
        'token': localStorage.getItem('token'),
    };
    method = 'POST';
    if(newUserName.length == 0){
        alert("Please enter a name")
        return;
    }
    if(newUserName.length < 4){
        alert("Username too short")
        return;
    }
    if(newUserName.length > 16){
        alert("Username too long")
        return;
    }
    document.getElementById("newUserName").value = "";
    call_api(endpoint, body, method);
}

async function call_api(endpoint, _body, _method){
    var data;
    try{

        let res = await fetch(backendIp + endpoint, {
            headers: {
                'Accept': 'aplication/json',
                'Content-Type': 'application/json'
            },
            method: _method,
            body: JSON.stringify(_body)
        });
        
        data = await res.json()['data'];
            
    }catch(e){
        console.error(e);
    }
    return data;
}

function logout(){
    localStorage.clear();
    window.location.href = "/Private";
}

function CheckIfUser(){
    var username = localStorage.getItem('name');
    var token = localStorage.getItem('token');
    if(username == null || token == null){
        logout();
        return;
    }
    let body = {
        'username': username,
        'token': token
    }
    setTimeout(async function(){
        let res = await fetch(backendIp + "/checkToken", {
            headers: {
                'Accept': 'aplication/json',
                'Content-Type': 'application/json'
            },
            method: 'POST',
            body: JSON.stringify(body)
        });
        let data = await res.json();
        if(data['data'] == 'success'){
            return;
        }else{
            logout();
            return;
        }
    }, 100);
}

function LoadAdmin(){
    window.location.href=backendIp + "/adminLogin";
}