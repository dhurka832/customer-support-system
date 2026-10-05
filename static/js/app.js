/**
 * SupportSphere Vanilla JS UI Engine
 * Pure Vanilla JavaScript: Accordions, Modals, Dropdowns, Toast, Mobile Navigation.
 * Zero Bootstrap Dependency.
 */

document.addEventListener('DOMContentLoaded', () => {
    initDropdowns();
    initCollapses();
    initModals();
    initMobileNav();
    initDemoCredentials();
    initQuickPrompts();
});

/* ==========================================================================
   DROPDOWNS
   ========================================================================== */
function initDropdowns() {
    const dropdownToggles = document.querySelectorAll('[data-toggle="dropdown"], [data-bs-toggle="dropdown"]');
    
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            
            const dropdownContainer = toggle.closest('.dropdown') || toggle.parentElement;
            const menu = dropdownContainer.querySelector('.dropdown-menu');
            
            // Close other open dropdowns
            document.querySelectorAll('.dropdown-menu.show').forEach(openMenu => {
                if (openMenu !== menu) {
                    openMenu.classList.remove('show');
                }
            });
            
            if (menu) {
                menu.classList.toggle('show');
            }
        });
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.dropdown')) {
            document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
                menu.classList.remove('show');
            });
        }
    });
}

/* ==========================================================================
   COLLAPSE & ACCORDION (SMOOTH HEIGHT TRANSITION)
   ========================================================================== */
function initCollapses() {
    const collapseToggles = document.querySelectorAll('[data-toggle="collapse"], [data-bs-toggle="collapse"]');
    
    collapseToggles.forEach(toggle => {
        toggle.addEventListener('click', (e) => {
            e.preventDefault();
            const targetSelector = toggle.getAttribute('data-target') || 
                                   toggle.getAttribute('data-bs-target') || 
                                   toggle.getAttribute('href');
            
            if (!targetSelector) return;
            const target = document.querySelector(targetSelector);
            if (!target) return;

            const isExpanded = target.classList.contains('show') || target.classList.contains('open');
            const parentSelector = toggle.getAttribute('data-parent') || toggle.getAttribute('data-bs-parent');

            if (parentSelector) {
                const parent = document.querySelector(parentSelector);
                if (parent) {
                    parent.querySelectorAll('.collapse.show, .collapse.open, .ticket-accordion-body.show, .conversation-accordion-body.show').forEach(sibling => {
                        if (sibling !== target) {
                            sibling.classList.remove('show', 'open');
                            sibling.style.maxHeight = null;
                        }
                    });
                    parent.querySelectorAll('[data-toggle="collapse"], [data-bs-toggle="collapse"]').forEach(btn => {
                        if (btn !== toggle) {
                            btn.classList.add('collapsed');
                            btn.setAttribute('aria-expanded', 'false');
                        }
                    });
                }
            }

            if (isExpanded) {
                target.classList.remove('show', 'open');
                target.style.maxHeight = null;
                toggle.classList.add('collapsed');
                toggle.setAttribute('aria-expanded', 'false');
            } else {
                target.classList.add('show', 'open');
                target.style.maxHeight = (target.scrollHeight + 100) + 'px';
                toggle.classList.remove('collapsed');
                toggle.setAttribute('aria-expanded', 'true');
            }
        });
    });
}

/* ==========================================================================
   MODAL CONTROLLER (BOOTSTRAP-FREE)
   ========================================================================== */
function initModals() {
    const modalToggles = document.querySelectorAll('[data-toggle="modal"], [data-bs-toggle="modal"]');
    const modalDismisses = document.querySelectorAll('[data-dismiss="modal"], [data-bs-dismiss="modal"]');
    
    modalToggles.forEach(toggle => {
        toggle.addEventListener('click', (e) => {
            e.preventDefault();
            const targetSelector = toggle.getAttribute('data-target') || toggle.getAttribute('data-bs-target');
            if (!targetSelector) return;
            const modal = document.querySelector(targetSelector);
            if (modal) {
                openModal(modal);
            }
        });
    });

    modalDismisses.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const modal = btn.closest('.modal, .modal-backdrop-custom');
            if (modal) {
                closeModal(modal);
            }
        });
    });

    // Close when clicking modal backdrop
    document.querySelectorAll('.modal, .modal-backdrop-custom').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeModal(modal);
            }
        });
    });

    // Close on Escape key press
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            document.querySelectorAll('.modal.show, .modal-backdrop-custom.show').forEach(modal => {
                closeModal(modal);
            });
        }
    });
}

function openModal(modal) {
    modal.classList.add('show');
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

function closeModal(modal) {
    modal.classList.remove('show');
    setTimeout(() => {
        modal.style.display = 'none';
        if (!document.querySelector('.modal.show, .modal-backdrop-custom.show')) {
            document.body.style.overflow = '';
        }
    }, 200);
}

/* ==========================================================================
   MOBILE NAVIGATION & SIDEBAR
   ========================================================================== */
function initMobileNav() {
    const navToggle = document.getElementById('navbarToggle') || document.querySelector('[data-bs-toggle="collapse"][data-bs-target="#navbarContent"]');
    const navContent = document.getElementById('navbarContent');

    if (navToggle && navContent) {
        navToggle.addEventListener('click', () => {
            navContent.classList.toggle('show');
            navToggle.classList.toggle('active');
        });
    }

    const sidebar = document.getElementById('sidebar');
    const sidebarCollapse = document.getElementById('sidebarCollapse');
    const sidebarClose = document.getElementById('sidebarClose');

    if (sidebarCollapse && sidebar) {
        sidebarCollapse.addEventListener('click', (e) => {
            e.stopPropagation();
            sidebar.classList.toggle('active');
        });
    }

    if (sidebarClose && sidebar) {
        sidebarClose.addEventListener('click', () => {
            sidebar.classList.remove('active');
        });
    }

    // Close sidebar on mobile when clicked outside
    document.addEventListener('click', (e) => {
        if (sidebar && sidebar.classList.contains('active') && !sidebar.contains(e.target) && !sidebarCollapse.contains(e.target)) {
            sidebar.classList.remove('active');
        }
    });
}

/* ==========================================================================
   DEMO CREDENTIALS QUICK-FILL
   ========================================================================== */
function initDemoCredentials() {
    const credPills = document.querySelectorAll('.demo-cred-pill');
    credPills.forEach(pill => {
        pill.addEventListener('click', () => {
            const user = pill.getAttribute('data-user');
            const pass = pill.getAttribute('data-pass');
            
            const userInput = document.querySelector('input[name="username"]');
            const passInput = document.querySelector('input[name="password"]');

            if (userInput && user) {
                userInput.value = user;
                userInput.style.borderColor = 'var(--primary-500)';
                setTimeout(() => userInput.style.borderColor = '', 800);
            }
            if (passInput && pass) {
                passInput.value = pass;
                passInput.style.borderColor = 'var(--primary-500)';
                setTimeout(() => passInput.style.borderColor = '', 800);
            }

            // Show feedback
            const originalHtml = pill.innerHTML;
            pill.innerHTML = `<i class="bi bi-check-circle-fill text-success"></i> <span class="cred-val text-success">Filled!</span>`;
            setTimeout(() => {
                pill.innerHTML = originalHtml;
            }, 1200);
        });
    });
}

/* ==========================================================================
   CHAT QUICK PROMPT CHIPS
   ========================================================================== */
function initQuickPrompts() {
    const promptChips = document.querySelectorAll('.prompt-chip');
    const userInput = document.getElementById('userInput');

    promptChips.forEach(chip => {
        chip.addEventListener('click', () => {
            const promptText = chip.getAttribute('data-prompt') || chip.textContent.trim();
            if (userInput) {
                userInput.value = promptText;
                userInput.focus();
            }
        });
    });
}

/* ==========================================================================
   TOAST NOTIFICATION HELPER
   ========================================================================== */
window.showToast = function(message, type = 'success') {
    let container = document.getElementById('toastContainer');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast-pill toast-${type}`;
    const icon = type === 'success' ? 'bi-check-circle-fill' : type === 'error' ? 'bi-exclamation-triangle-fill' : 'bi-info-circle-fill';
    toast.innerHTML = `<i class="bi ${icon}"></i> <span>${message}</span>`;
    
    container.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('show');
    }, 10);

    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3500);
};
