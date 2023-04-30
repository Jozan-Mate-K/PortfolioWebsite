function OpenBox(whatToShow){
    if(whatToShow == "MD5"){

        document.getElementById("MD5Container").classList.add("appear");
        document.getElementById("AESContainer").classList.remove("appear");
        document.getElementById("SHAContainer").classList.remove("appear");
    }
    else if(whatToShow == "AES"){

        document.getElementById("MD5Container").classList.remove("appear");
        document.getElementById("AESContainer").classList.add("appear");
        document.getElementById("SHAContainer").classList.remove("appear");
    }else if(whatToShow == "SHA"){

        document.getElementById("MD5Container").classList.remove("appear");
        document.getElementById("AESContainer").classList.remove("appear");
        document.getElementById("SHAContainer").classList.add("appear");
    }

}