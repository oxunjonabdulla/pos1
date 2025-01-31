// Check section availability

// document.addEventListener("DOMContentLoaded", function () {
//     // Ensure CSRF token is available
//     const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]') ?
//         document.querySelector('[name="csrfmiddlewaretoken"]').value : null;
//
//     if (!csrfToken) {
//         console.error("CSRF token is missing!");
//         return;
//     }
//
//     document.querySelectorAll(".section-link").forEach(link => {
//         link.addEventListener("click", function (e) {
//             e.preventDefault(); // Prevent navigation
//
//             const sectionUrl = this.getAttribute("href");
//             const sectionName = this.getAttribute("data-section");
//
//             if (!sectionUrl || !sectionName) {
//                 console.error("Missing section URL or name");
//                 return;
//             }
//
//             // AJAX request to check cart section
//             fetch(`/check-section/`, {
//                 method: "POST",
//                 headers: {
//                     "Content-Type": "application/json",
//                     "X-CSRFToken": csrfToken
//                 },
//                 body: JSON.stringify({section: sectionName})
//             })
//                 .then(response => response.json())
//                 .then(data => {
//                     if (data.success) {
//                         // Navigate to the section if successful
//                         window.location.href = sectionUrl;
//                     } else {
//                         // Show confirmation modal if failed
//                         showConfirmationModal(data.message, sectionUrl);
//                     }
//                 })
//                 .catch(error => {
//                     console.error("Error:", error);
//                     alert("An error occurred. Please try again.");
//                 });
//         });
//     });
//
//     // Function to show the confirmation modal
//     function showConfirmationModal(message, sectionUrl) {
//         if (document.getElementById("confirmationModal")) {
//             // Avoid adding multiple modals if one already exists
//             return;
//         }
//
//         // Import the gettext function
//         const modalHtml = `
//     <div class="modal fade" id="confirmationModal" tabindex="-1" role="dialog">
//         <div class="modal-dialog" role="document">
//             <div class="modal-content">
//                 <div class="modal-header">
//                     <h5 class="modal-title">Tasdiqlash</h5>
//                     <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
//                 </div>
//                 <div class="modal-body">
//                     <p>${message}</p>
//                 </div>
//                 <div class="modal-footer">
//                     <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Yopish</button>
//                     <button type="button" class="btn btn-primary" id="confirm-action">Davom etish</button>
//                 </div>
//             </div>
//         </div>
//     </div>
// `;
//
//         // Append modal HTML to body
//         document.body.insertAdjacentHTML("beforeend", modalHtml);
//         const modal = new bootstrap.Modal(document.getElementById("confirmationModal"));
//
//         // Event for the "Confirm" button
//         document.getElementById("confirm-action").addEventListener("click", function () {
//             modal.hide();
//             document.getElementById("confirmationModal").remove();
//             window.location.href = sectionUrl; // Redirect after confirmation
//         });
//
//         // Show the modal
//         modal.show();
//
//         // Clean up modal after closing
//         document.getElementById("confirmationModal").addEventListener("hidden.bs.modal", function () {
//             document.getElementById("confirmationModal").remove();
//         });
//     }
// });



document.addEventListener("DOMContentLoaded", function () {
    // Ensure CSRF token is available
    const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]') ?
        document.querySelector('[name="csrfmiddlewaretoken"]').value : null;

    if (!csrfToken) {
        console.error("CSRF token is missing!");
        return;
    }

    document.querySelectorAll(".section-link").forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault(); // Prevent navigation

            const sectionUrl = this.getAttribute("href");
            const sectionName = this.getAttribute("data-section");

            if (!sectionUrl || !sectionName) {
                console.error("Missing section URL or name");
                return;
            }

             // AJAX request to check cart section
            fetch(`/check-section/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({section: sectionName})
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Navigate to the section if successful
                        window.location.href = sectionUrl;
                    } else {
                        // Show confirmation modal if failed
                        showConfirmationModal(data.message, sectionUrl);
                    }
                })
                .catch(error => {
                    console.error("Error:", error);
                    alert("An error occurred. Please try again.");
                });
        });
    });

    // Function to show the confirmation modal
    function showConfirmationModal(message, sectionUrl) {
        if (document.getElementById("confirmationModal")) {
            // Avoid adding multiple modals if one already exists
            return;
        }

        const modalHtml = `
            <div class="modal fade" id="confirmationModal" tabindex="-1" role="dialog">
                <div class="modal-dialog" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Tasdiqlash</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <p>${message}</p>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Yopish</button>
                            <button type="button" class="btn btn-primary" id="confirm-action">Davom etish</button>
                        </div>
                        </div>
                </div>
            </div>
        `;

        // Append modal HTML to body
        document.body.insertAdjacentHTML("beforeend", modalHtml);
        const modal = new bootstrap.Modal(document.getElementById("confirmationModal"));

        // Event for the "Confirm" button
        document.getElementById("confirm-action").addEventListener("click", function () {
            modal.hide();
            document.getElementById("confirmationModal").remove();
            window.location.href = sectionUrl; // Redirect after confirmation
        });

        // Show the modal
        modal.show();
  // Clean up modal after closing
        document.getElementById("confirmationModal").addEventListener("hidden.bs.modal", function () {
            document.getElementById("confirmationModal").remove();
        });
    }
});


//  --------- Check section availability

// Logout function with confirmation

// Logout function with confirmation


function showConfirmationModal(message, onConfirm) {
    const modal = document.createElement("div");
    modal.className = "modal fade";
    modal.tabIndex = "-1";
    modal.role = "dialog";
    modal.innerHTML = `
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Tasdiqlash</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <p>${message}</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Yo'q</button>
                        <button type="button" class="btn btn-danger" id="confirm-clear-cart">Ha</button>
                    </div>
                </div>
            </div>
        `;

    document.body.appendChild(modal);
    const bsModal = new bootstrap.Modal(modal);

    // Attach event listener for confirm button
    modal.querySelector("#confirm-clear-cart").addEventListener("click", function () {
        bsModal.hide();
        modal.remove();

        if (onConfirm) onConfirm(); // Call the confirm callback
    });

    // Show the modal
    bsModal.show();

    // Remove modal from DOM on close
    modal.addEventListener("hidden.bs.modal", function () {
        modal.remove();
    });
}

function logoutConfirm(event) {
    event.preventDefault(); // Prevent the default anchor behavior

    showConfirmationModal("Rostdan ham tizimni tark etmoqchimisiz?", function () {
        console.log("Ok");
        window.location.href = '/auth/logout/';
    });
}

// --------- Logout function with confirmation


// --------- Logout function with confirmation


// Order handling

// Submit Order Form Handler
document.getElementById("submitOrderForm").addEventListener("submit", function (event) {
    event.preventDefault();

    const password = document.getElementById("submitOrderPassword").value;
    const orderPk = document.getElementById("submitOrderForm").dataset.orderPk; // Fetch pk from form dataset

    fetch(`/submit-order/${orderPk}/`, { // Append pk to the URL
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "{{ csrf_token }}"
        },
        body: JSON.stringify({password})
    })
        .then(response => response.json())
        .then(data => {
            const modal = bootstrap.Modal.getInstance(document.getElementById("submitOrderModal"));
            modal.hide();

            if (data.success) {
                showAlert("Buyurtma muvaffaqiyatli tasdiqlandi!", "success");
                setTimeout(() => location.reload(), 2000);
            } else {
                showAlert(data.message || "Xatolik yuz berdi!", "danger");
            }
        })
        .catch(error => {
            console.error(error);
            showAlert("Xatolik yuz berdi!", "danger");
        });
});


// Cancel Order Form Handler
document.getElementById("cancelOrderForm").addEventListener("submit", function (event) {
    event.preventDefault();

    const password = document.getElementById("cancelOrderPassword").value;
    const orderPk = document.getElementById("cancelOrderForm").dataset.orderPk; // Fetch pk from form dataset
    const reason = document.getElementById("cancelOrderReason").value;

    fetch(`/cancel-order/${orderPk}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "{{ csrf_token }}"
        },
        body: JSON.stringify({password, reason})
    })
        .then(response => response.json())
        .then(data => {
            const modalElement = document.getElementById("cancelOrderModal");
            const modal = bootstrap.Modal.getInstance(modalElement);
            modal.hide();

            if (data.success) {
                showAlert("Buyurtma bekor qilindi!", "success");
                setTimeout(() => location.reload(), 2000);
            } else {
                showAlert(data.message || "Xatolik yuz berdi!", "danger");
            }
        })
        .catch(error => {
            console.error(error);
            showAlert("Xatolik yuz berdi!", "danger");
        });
});

// Attach pk to modal on open
document.querySelectorAll('[data-bs-target="#cancelOrderModal"]').forEach(button => {
    button.addEventListener("click", function () {
        const pk = this.getAttribute("data-pk"); // Get pk from button
        const modalElement = document.getElementById("cancelOrderModal");
        modalElement.setAttribute("data-pk", pk); // Pass pk to modal
    });
});

// Function to display alerts
function showAlert(message, type = "info") {
    const alertBox = document.createElement("div");
    alertBox.className = `alert alert-${type} alert-dismissible fade show fixed-top`;
    alertBox.role = "alert";
    alertBox.style.marginTop = "20px";
    alertBox.innerHTML = `
    <div class="container">
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
`;
    document.body.appendChild(alertBox);

    setTimeout(() => alertBox.remove(), 5000);
}


// --------- Order handling







