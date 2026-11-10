document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("form").forEach(form => {
    if (form.method.toLowerCase() === "post" && !form.querySelector("[data-no-validate]")) {
      form.addEventListener("submit", event => {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add("was-validated");
      });
    }
  });
});
