window.addEventListener('scroll', function () {
    let header = document.querySelector("header");
    header.classList.toggle("fixed", window.scrollY > 0);
})