/**
 * VELOCE AUTO SPA & DETAILING - LÓGICA DE INTERFAZ GENERAL
 * Manejo de modales, autocompletado demo, reservas y notificaciones toast.
 */

document.addEventListener('DOMContentLoaded', () => {
    // Auto-ocultar mensajes Flash tras 5 segundos
    const toasts = document.querySelectorAll('.alert-toast');
    toasts.forEach(toast => {
        setTimeout(() => {
            toast.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            setTimeout(() => toast.remove(), 400);
        }, 5000);
    });

    // Delegación para cerrar toast con el botón de cruz
    document.addEventListener('click', (e) => {
        if (e.target.closest('.alert-close')) {
            const toast = e.target.closest('.alert-toast');
            if (toast) toast.remove();
        }
    });

    // Función para mostrar notificaciones dinámicas
    window.showToast = function(message, type = 'info') {
        let container = document.querySelector('.alert-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'alert-container';
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        toast.className = `alert-toast ${type}`;
        toast.innerHTML = `
            <span>${message}</span>
            <button class="alert-close" aria-label="Cerrar">&times;</button>
        `;
        container.appendChild(toast);

        setTimeout(() => {
            toast.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            setTimeout(() => toast.remove(), 400);
        }, 5000);
    };

    // Control de Modales Generales
    window.openModal = function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        }
    };

    window.closeModal = function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('active');
            document.body.style.overflow = '';
        }
    };

    // Cerrar modal al hacer clic en el backdrop
    document.querySelectorAll('.modal-overlay').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeModal(modal.id);
            }
        });
    });

    // Botones de Credenciales Demo en pantalla de Login
    const btnDemoAdmin = document.getElementById('btnDemoAdmin');
    const btnDemoClient = document.getElementById('btnDemoClient');

    if (btnDemoAdmin) {
        btnDemoAdmin.addEventListener('click', () => {
            const uInput = document.getElementById('loginUsername');
            const pInput = document.getElementById('loginPassword');
            if (uInput && pInput) {
                uInput.value = 'admin';
                pInput.value = 'admin123';
                uInput.focus();
                showToast('Credenciales de Administrador cargadas. Presione Iniciar Sesión.', 'info');
            }
        });
    }

    if (btnDemoClient) {
        btnDemoClient.addEventListener('click', () => {
            const uInput = document.getElementById('loginUsername');
            const pInput = document.getElementById('loginPassword');
            if (uInput && pInput) {
                uInput.value = 'carlos_m';
                pInput.value = 'cliente123';
                uInput.focus();
                showToast('Credenciales de Cliente cargadas. Presione Iniciar Sesión.', 'info');
            }
        });
    }

    // Modal de Reserva de Servicios (en panel de cliente)
    const bookingButtons = document.querySelectorAll('.btn-book-service');
    bookingButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const serviceId = btn.dataset.serviceId;
            const serviceName = btn.dataset.serviceName;
            const servicePrice = btn.dataset.servicePrice;

            const inputServiceId = document.getElementById('bookServiceId');
            const labelServiceName = document.getElementById('bookServiceName');
            const labelServicePrice = document.getElementById('bookServicePrice');

            if (inputServiceId) inputServiceId.value = serviceId;
            if (labelServiceName) labelServiceName.textContent = serviceName;
            if (labelServicePrice) labelServicePrice.textContent = `$${parseFloat(servicePrice).toLocaleString()}`;

            // Fijar fecha por defecto a mañana
            const dateInput = document.getElementById('bookDateTime');
            if (dateInput) {
                const tomorrow = new Date();
                tomorrow.setDate(tomorrow.getDate() + 1);
                tomorrow.setHours(10, 0, 0, 0);
                const localIso = new Date(tomorrow.getTime() - (tomorrow.getTimezoneOffset() * 60000)).toISOString().slice(0, 16);
                dateInput.value = localIso;
            }

            openModal('bookingModal');
        });
    });

    // Formulario de Reserva
    const bookingForm = document.getElementById('bookingForm');
    if (bookingForm) {
        bookingForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const submitBtn = bookingForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = 'Agendando...';

            const formData = new FormData(bookingForm);

            try {
                const response = await fetch('/api/book-service', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();

                if (data.success) {
                    showToast(data.message, 'success');
                    closeModal('bookingModal');
                    bookingForm.reset();
                    // Opcional: recargar después de 1.5s para ver los puntos actualizados
                    setTimeout(() => window.location.reload(), 1500);
                } else {
                    showToast(data.error || 'Ocurrió un error al agendar', 'error');
                }
            } catch (err) {
                showToast('Error de conexión al servidor.', 'error');
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            }
        });
    }
});
