document.addEventListener("DOMContentLoaded", () => {
    const deleteButtons = document.querySelectorAll(".btn-delete-customer");
    const deleteForm = document.getElementById("deleteCustomerForm");
    const deleteUsernameSpan = document.getElementById("deleteModalUsername");

    if (!deleteButtons.length || !deleteForm || !deleteUsernameSpan) return;

    deleteButtons.forEach(button => {
        button.addEventListener("click", (event) => {
            const btn = event.currentTarget;
            const userId = btn.getAttribute("data-user-id");
            const username = btn.getAttribute("data-username");
            
            deleteUsernameSpan.textContent = username;
            
            deleteForm.action = `/accounts/dashboard/admin/customers/${userId}/delete/`;
        });
    });
});
