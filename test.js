function confirmDelete() {
    let result = confirm("Are you sure you completed this task?");

    if (result) {
        alert("Hurrah! You completed a todo. Keep the momentum going!");
        return true;
    } else {
        return false;
    }
}

