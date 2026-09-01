const token = localStorage.getItem("access_token");


// -------------------------
// Check authentication
// -------------------------

if (!token) {
    window.location.href = "/login";
}


// -------------------------
// DOM elements
// -------------------------

const taskForm =
    document.getElementById("task-form");

const tasksContainer =
    document.getElementById("tasks-container");

const logoutBtn =
    document.getElementById("logout-btn");

const refreshBtn =
    document.getElementById("refresh-btn");


// -------------------------
// API helper
// -------------------------

async function apiRequest(url, options = {}) {

    const headers = {
        ...options.headers,
        "Authorization": `Bearer ${token}`
    };

    const response = await fetch(url, {
        ...options,
        headers
    });

    if (response.status === 401) {

        localStorage.removeItem("access_token");

        window.location.href = "/login";

        return null;
    }

    return response;
}


// -------------------------
// Get tasks
// -------------------------

async function loadTasks() {

    tasksContainer.innerHTML =
        "<p>Loading tasks...</p>";

    try {

        const response =
            await apiRequest("/api/tasks");

        if (!response) return;

        const data =
            await response.json();

        if (!response.ok) {

            tasksContainer.innerHTML =
                `<p>${data.detail}</p>`;

            return;
        }

        renderTasks(data.items);

    } catch (error) {

        console.error(error);

        tasksContainer.innerHTML =
            "<p>Failed to load tasks.</p>";
    }
}


// -------------------------
// Render tasks
// -------------------------

function renderTasks(tasks) {

    tasksContainer.innerHTML = "";

    if (tasks.length === 0) {

        tasksContainer.innerHTML =
            "<p>No tasks found.</p>";

        return;
    }

    tasks.forEach(task => {

        const taskElement =
            document.createElement("div");

        taskElement.className = "task-card";

        taskElement.innerHTML = `

            <div>

                <h3>${task.title}</h3>

                <p>
                    ${task.description || ""}
                </p>

                <span class="status">
                    ${task.status}
                </span>

                <span class="priority">
                    ${task.priority}
                </span>

                ${
                    task.due_date
                    ? `<p>Due: ${task.due_date}</p>`
                    : ""
                }

            </div>

            <div class="task-actions">

                <button
                    onclick="completeTask(${task.id})">
                    Complete
                </button>

                <button
                    onclick="deleteTask(${task.id})">
                    Delete
                </button>

            </div>
        `;

        tasksContainer.appendChild(taskElement);

    });
}


// -------------------------
// Create task
// -------------------------

taskForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();

        const title =
            document.getElementById("title").value;

        const description =
            document.getElementById("description").value;

        const status =
            document.getElementById("status").value;

        const priority =
            document.getElementById("priority").value;

        const dueDate =
            document.getElementById("due_date").value;


        const taskData = {
            title: title,
            description: description || null,
            status: status,
            priority: priority,
            due_date: dueDate || null
        };


        try {

            const response = await apiRequest(
                "/api/tasks",
                {
                    method: "POST",
                    headers: {
                        "Content-Type":
                            "application/json"
                    },
                    body: JSON.stringify(taskData)
                }
            );

            if (!response) return;

            const data =
                await response.json();

            if (!response.ok) {

                alert(
                    data.detail ||
                    "Failed to create task"
                );

                return;
            }


            taskForm.reset();

            loadTasks();

        } catch (error) {

            console.error(error);

            alert("Failed to create task");
        }

    }
);


// -------------------------
// Complete task
// -------------------------

async function completeTask(taskId) {

    try {

        const response =
            await apiRequest(
                `/api/tasks/${taskId}`,
                {
                    method: "PATCH",
                    headers: {
                        "Content-Type":
                            "application/json"
                    },
                    body: JSON.stringify({
                        status: "completed"
                    })
                }
            );

        if (!response) return;

        if (!response.ok) {

            const data =
                await response.json();

            alert(
                data.detail ||
                "Failed to update task"
            );

            return;
        }

        loadTasks();

    } catch (error) {

        console.error(error);

    }
}


// -------------------------
// Delete task
// -------------------------

async function deleteTask(taskId) {

    const confirmed =
        confirm("Delete this task?");

    if (!confirmed) return;


    try {

        const response =
            await apiRequest(
                `/api/tasks/${taskId}`,
                {
                    method: "DELETE"
                }
            );

        if (!response) return;

        if (!response.ok) {

            const data =
                await response.json();

            alert(
                data.detail ||
                "Failed to delete task"
            );

            return;
        }

        loadTasks();

    } catch (error) {

        console.error(error);

    }
}


// -------------------------
// Logout
// -------------------------

logoutBtn.addEventListener(
    "click",
    function () {

        localStorage.removeItem(
            "access_token"
        );

        window.location.href = "/login";
    }
);


// -------------------------
// Refresh
// -------------------------

refreshBtn.addEventListener(
    "click",
    loadTasks
);


// -------------------------
// Initial load
// -------------------------

loadTasks();