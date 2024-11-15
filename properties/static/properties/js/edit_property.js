document.addEventListener("DOMContentLoaded", function () {
    const editBtn = document.getElementById("edit-property-btn");
    const cancelBtn = document.getElementById("cancel-edit-property-btn");
    const propertyView = document.getElementById("property-view");
    const propertyEditForm = document.getElementById("property-edit-form");


    editBtn.addEventListener("click", function (event) {
        event.preventDefault();
        propertyView.classList.add("d-none");
        propertyEditForm.classList.remove("d-none");
        cancelBtn.classList.remove("d-none");
    });

    cancelBtn.addEventListener("click", function (event) {
        event.preventDefault();
        propertyEditForm.classList.add("d-none");
        propertyView.classList.remove("d-none");
        cancelBtn.classList.add("d-none");
    });
});