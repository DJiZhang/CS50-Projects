const saved_theme = localStorage.getItem('theme');

if (saved_theme) {
    document.documentElement.setAttribute('data-bs-theme', saved_theme);
    const buttons = document.querySelectorAll('button');

    buttons.forEach(function(button){
        if (saved_theme === "light") {
            button.classList.remove("btn-outline-light");
            button.classList.add("btn-outline-dark");
        } else {
            button.classList.remove("btn-outline-dark");
            button.classList.add("btn-outline-light");
        }
    });
}


const buttons = document.querySelectorAll('button');
let toggles = document.querySelectorAll('[data-theme]');
toggles.forEach(function(toggle){
    toggle.addEventListener('click', function(){
        let theme = toggle.getAttribute('data-theme');
        document.documentElement.setAttribute('data-bs-theme', theme);
        localStorage.setItem('theme', theme);


        buttons.forEach(function(button){
        if (theme === "light") {
            button.classList.remove("btn-outline-light");
            button.classList.add("btn-outline-dark");
        } else {
            button.classList.remove("btn-outline-dark");
            button.classList.add("btn-outline-light");
        }
        });
    });
});


