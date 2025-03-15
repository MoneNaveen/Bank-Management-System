document.addEventListener("DOMContentLoaded", function () {
    const button = document.querySelector("button");

    button.addEventListener("click", function (event) {
        event.preventDefault();
        button.classList.add("clicked");

        // Reset animation after 1.2s
        setTimeout(() => {
            button.classList.remove("clicked");
        }, 1200);

        // Create Flying Money Effect
        for (let i = 0; i < 5; i++) {
            let money = document.createElement("div");
            money.innerHTML = "💸";
            money.classList.add("money-fly");
            money.style.left = `${Math.random() * 80 + 10}%`;
            money.style.animationDuration = `${Math.random() * 1 + 0.5}s`;
            document.body.appendChild(money);

            setTimeout(() => {
                money.remove();
            }, 1200);
        }
    });
});