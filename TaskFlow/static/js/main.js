document.addEventListener("DOMContentLoaded", () => {

    // =========================
    // SEARCH
    // =========================

    const searchInput =
        document.getElementById("taskSearch");

    const taskList =
        document.getElementById("taskList");


    if (searchInput && taskList) {

        const tasks =
            taskList.querySelectorAll(".task-item");

        searchInput.addEventListener("input", () => {

            const searchValue =
                searchInput.value
                    .trim()
                    .toLowerCase();

            tasks.forEach((task) => {

                const title =
                    task.dataset.taskTitle || "";

                if (title.includes(searchValue)) {
                    task.style.display = "";
                } else {
                    task.style.display = "none";
                }

            });

        });

    }


    // =========================
    // EDIT
    // =========================

    const editButtons =
        document.querySelectorAll(".edit-task");


    editButtons.forEach((button) => {

        button.addEventListener("click", () => {

            const taskId =
                button.dataset.taskId;

            const editForm =
                document.getElementById(
                    `edit-form-${taskId}`
                );

            if (!editForm) {
                return;
            }

            editForm.classList.add("active");

            button.style.display = "none";

        });

    });


    // =========================
    // CANCEL EDIT
    // =========================

    const cancelButtons =
        document.querySelectorAll(".btn-cancel-edit");


    cancelButtons.forEach((button) => {

        button.addEventListener("click", () => {

            const taskId =
                button.dataset.taskId;

            const editForm =
                document.getElementById(
                    `edit-form-${taskId}`
                );

            const editButton =
                document.querySelector(
                    `.edit-task[data-task-id="${taskId}"]`
                );


            if (!editForm) {
                return;
            }


            // Hide form
            editForm.classList.remove("active");


            // Show Edit button
            if (editButton) {
                editButton.style.display = "";
            }

        });

    });

});