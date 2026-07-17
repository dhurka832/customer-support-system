document.addEventListener("DOMContentLoaded", () => {
    const statusSelectors = document.querySelectorAll(".status-selector");

    statusSelectors.forEach(selector => {
        selector.addEventListener("change", handleStatusChange);
    });
});

function handleStatusChange(event) {
    const selector = event.currentTarget;
    const ticketId = selector.getAttribute("data-id") || selector.getAttribute("data-ticket-id");
    const newStatus = selector.value;
    
    const updateUrl = selector.dataset.updateUrl || "/accounts/dashboard/admin/tickets/status/";

    const csrfTokenEl = document.querySelector('[name=csrfmiddlewaretoken]') || document.querySelector('meta[name="csrf-token"]');
    const csrfToken = csrfTokenEl ? (csrfTokenEl.value || csrfTokenEl.getAttribute('content')) : '';

    fetch(updateUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        },
        body: JSON.stringify({
            ticket_id: ticketId,
            status: newStatus
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            selector.classList.add("is-valid");
            setTimeout(() => {
                selector.classList.remove("is-valid");
            }, 1000);
        } else {
            alert(`Error: ${data.error}`);
        }
    })
    .catch(error => {
        console.error("Failed to update status", error);
        alert("Failed to update status. Please try again.");
    });
}
