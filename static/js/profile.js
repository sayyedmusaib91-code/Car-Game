let currentXP = parseInt(document.body.dataset.currentxp);
let maxXP = parseInt(document.body.dataset.maxxp);
let levelUp = document.body.dataset.levelup;

let fill = document.querySelector(".level-fill");
let levelUpText = document.getElementById("levelUpText");
let levelText = document.getElementById("levelText");

// % calculate
let percent = (currentXP / maxXP) * 100;
if (percent > 100) percent = 100;

// 🔥 smooth XP bar fill
setTimeout(() => {
    fill.style.width = percent + "%";
}, 200);

// 🔥 LEVEL UP EFFECT (backend se aayega)
if (levelUp === "True") {

    // show LEVEL UP text
    levelUpText.style.display = "block";

    // level highlight effect
    levelText.style.color = "yellow";
    levelText.style.transform = "scale(1.2)";
    levelText.style.transition = "0.3s";

    // hide after 2 sec
    setTimeout(() => {
        levelUpText.style.display = "none";
        levelText.style.transform = "scale(1)";
        levelText.style.color = "white";
    }, 2000);
}