async function handleSubscribe(e){

    e.preventDefault();
    const msg = document.getElementById("response-msg");
    const email = document.getElementById("email").value;
    const lat = parseFloat(document.getElementById("lat").value);
    const lon = parseFloat(document.getElementById("lon").value);

    msg.className = "text-[10px] mt-4 text-zinc-400 text-center";
    msg.innerText = "Processing.";
    msg.classList.remove("hidden");

    try {
        const res = await fetch("/api/subscribe", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({email, lat, lon})
        });
        if (res.ok) {
            msg.className = "text-[10px] mt-4 text-emerald-400 text-center";
            msg.innerText = "COORDS SAVED";
        } else {
            throw new Error();
        }
    } catch (err) {
        msg.className = "text-[10px] mt-4 text-red-400 text-center";
        msg.innerText = "ERROR";
    }


}