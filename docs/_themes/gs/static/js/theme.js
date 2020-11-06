document.addEventListener("DOMContentLoaded", () => {
  var trigger = document.getElementById("gs-nav-action");
  var navigation = document.getElementById("wy-nav-shift");

  trigger.addEventListener("click", () => {
    trigger.classList.toggle("active");
    navigation.classList.toggle("shift");
  });
});
