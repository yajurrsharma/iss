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

        const contentType = res.headers.get("content-type");
        let data;
        if (contentType && contentType.includes("application/json")) {
            data = await res.json();
        } else {
            throw new Error(await res.text());
        }

        if (res.ok) {
            msg.className = "text-[10px] mt-4 text-emerald-400 text-center";
            msg.innerText = data.message;
        } else {
            throw new Error(data.detail || "Failed to process request");
        }
    } catch (err) {
        msg.className = "text-[10px] mt-4 text-red-400 text-center";
        msg.innerText = "ERROR: " + err.message;
        console.error(err);
    }
}