function change()
{
    let x = document.querySelector("a");

    if (x.style.visibility === "hidden")
    {
        x.style.visibility = "visible";
    }
    else
    {
        x.style.visibility = "hidden";
    }
}

//blik

window.setInterval(change, 500);