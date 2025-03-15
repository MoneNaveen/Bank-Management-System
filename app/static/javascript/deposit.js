document.addEventListener("DOMContentLoaded", function () {
    const button = document.querySelector("button");

    button.addEventListener("click", function (event) {
        button.classList.add("clicked");

        // Reset animation after 1s
        setTimeout(() => {
            button.classList.remove("clicked");
        }, 1000);

        // Create Falling Money Effect
        for (let i = 0; i < 5; i++) {
            let money = document.createElement("div");
            money.innerHTML = "💰";
            money.classList.add("money-fall");
            money.style.left = `${Math.random() * 80 + 10}%`;
            money.style.animationDuration = `${Math.random() * 1 + 0.5}s`;
            document.body.appendChild(money);

            setTimeout(() => {
                money.remove();
            }, 1000);
        }
    });
});