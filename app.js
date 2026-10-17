async function handleSubscribe(e) {
    e.preventDefault();

    const msg = document.getElementById("response-msg");
    const emailInput = document.getElementById("email");
    const latInput = document.getElementById("lat");
    const lonInput = document.getElementById("long");

    if (!msg || !emailInput || !latInput || !lonInput) {
        console.error("Form elements not found in DOM");
        return;
    }

    msg.className = "text-[10px] mt-4 text-zinc-400 text-center";
    msg.innerText = "CALCULATING PASSES FOR THE NEXT 2 WEEKS.";
    msg.classList.remove("hidden");

    const formData = new FormData();
    formData.append("email", emailInput.value);
    formData.append("lat", latInput.value);
    formData.append("lon", lonInput.value);

    try {
        const res = await fetch("/api/track", {
            method: "POST",
            body: formData
        });

        if (res.ok) {
            const data = await res.json();
            msg.className = "text-[10px] mt-4 text-emerald-400 text-center";
            msg.innerText = data.message;
        } else {
            const errorText = await res.text();
            throw new Error(errorText);
        }
    } catch (err) {
        msg.className = "text-[10px] mt-4 text-red-400 text-center";
        
        let errorMsg = err.message;
        try {
            const errObj = JSON.parse(err.message);
            if (Array.isArray(errObj.detail)) {
                errorMsg = errObj.detail.map(d => d.msg).join(", ");
            } else if (errObj.detail) {
                errorMsg = errObj.detail;
            }
        } catch (e) {
        }

        msg.innerText = "ERROR: " + errorMsg;
        console.error(err);
    }
}
