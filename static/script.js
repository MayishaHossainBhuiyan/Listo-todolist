// JavaScript to handle deleting tasks and users
function deleteTask(taskId) {
    if (confirm("Are you sure you want to delete this task?")) {
        window.location.href = `/delete_task/${taskId}`;
    }
}

function deleteUser(username) {
    if (confirm("Are you sure you want to delete this user?")) {
        window.location.href = `/delete_user/${username}`;
    }
}
