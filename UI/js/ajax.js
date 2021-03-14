var btn = document.getElementById("submit");

btn.onclick = function() {

    // ajax request to api 
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log("Hey I am able to connect..")
        } else {
            console.log("Not able to connect")
        }
    };
    xhttp.open("GET", "https://nirqsn5nj2.execute-api.us-west-2.amazonaws.com/live", true);
    xhttp.send();

}