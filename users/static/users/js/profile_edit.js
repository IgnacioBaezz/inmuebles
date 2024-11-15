document.addEventListener("DOMContentLoaded", function () {
    const editBtn = document.getElementById("edit-profile-btn");
    const cancelBtn = document.getElementById("cancel-edit-btn");
    const profileView = document.getElementById("profile-view");
    const profileEditForm = document.getElementById("profile-edit-form");

    editBtn.addEventListener("click", function () {
        profileView.classList.remove("d-block");
        profileView.classList.add("d-none");
        profileEditForm.classList.remove("d-none");
        profileEditForm.classList.add("d-block");
    });

    cancelBtn.addEventListener("click", function () {
        profileEditForm.classList.remove("d-block");
        profileEditForm.classList.add("d-none");
        profileView.classList.remove("d-none");
        profileView.classList.add("d-block");
    });
});