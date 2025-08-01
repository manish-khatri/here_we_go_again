<script>
export default {
  name: 'App'
}
</script>

<template>
  <div id="app">
    <router-view />
  </div>
</template>

<style>
/* Modern Pastel Blue Design System */
:root {
  --primary: #A8D5E8;
  --primary-dark: #7FB3D3;
  --primary-light: #E8F4F8;
  --accent: #B8D4E3;
  --text: #2C3E50;
  --text-light: #6C757D;
  --white: #FFFFFF;
  --gray-50: #F9FAFB;
  --gray-100: #F3F4F6;
  --gray-200: #E5E7EB;
  --gray-300: #D1D5DB;
  --success: #10B981;
  --warning: #F59E0B;
  --error: #EF4444;
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
  color: var(--text);
  background: linear-gradient(135deg, var(--primary-light) 0%, var(--white) 100%);
  min-height: 100vh;
}

#app {
  min-height: 100vh;
}

/* Modern Button Styles */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 12px;
  font-weight: 500;
  font-size: 0.875rem;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.2s ease;
  gap: 0.5rem;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: var(--primary);
  color: var(--text);
  box-shadow: var(--shadow);
}

.btn-primary:hover {
  background: var(--primary-dark);
  transform: translateY(-1px);
  box-shadow: var(--shadow-lg);
}

.btn-secondary {
  background: var(--white);
  color: var(--text);
  border: 2px solid var(--gray-200);
}

.btn-secondary:hover {
  border-color: var(--primary);
  background: var(--primary-light);
}

.btn-success {
  background: var(--success);
  color: var(--white);
}

.btn-danger {
  background: var(--error);
  color: var(--white);
}

/* Modern Form Styles */
.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text);
  font-size: 0.875rem;
}

.form-control {
  width: 100%;
  padding: 0.875rem 1rem;
  border: 2px solid var(--gray-200);
  border-radius: 12px;
  font-size: 1rem;
  background: var(--white);
  transition: all 0.2s ease;
}

.form-control:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(168, 213, 232, 0.1);
}

.form-control::placeholder {
  color: var(--text-light);
}

/* Modern Card Styles */
.card {
  background: var(--white);
  border-radius: 16px;
  box-shadow: var(--shadow);
  border: 1px solid var(--gray-100);
  overflow: hidden;
}

.card-header {
  padding: 1.5rem;
  background: var(--primary-light);
  border-bottom: 1px solid var(--gray-200);
}

.card-body {
  padding: 1.5rem;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text);
  margin: 0;
}

/* Modern Table Styles */
.table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  background: var(--white);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: var(--shadow);
}

.table th {
  background: var(--primary-light);
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: var(--text);
  border-bottom: 1px solid var(--gray-200);
}

.table td {
  padding: 1rem;
  border-bottom: 1px solid var(--gray-100);
  color: var(--text);
}

.table tr:hover {
  background: var(--gray-50);
}

.table tr:last-child td {
  border-bottom: none;
}

/* Modern Navigation */
.navbar {
  background: var(--white);
  box-shadow: var(--shadow);
  border-bottom: 1px solid var(--gray-200);
  padding: 1rem 0;
}

.navbar-brand {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary-dark);
  text-decoration: none;
}

.nav-link {
  color: var(--text);
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.2s ease;
  font-weight: 500;
}

.nav-link:hover,
.nav-link.active {
  background: var(--primary-light);
  color: var(--primary-dark);
}

/* Modern Alert Styles */
.alert {
  padding: 1rem 1.5rem;
  border-radius: 12px;
  border: 1px solid;
  margin-bottom: 1rem;
}

.alert-success {
  background: #D1FAE5;
  border-color: var(--success);
  color: #065F46;
}

.alert-error {
  background: #FEE2E2;
  border-color: var(--error);
  color: #991B1B;
}

.alert-warning {
  background: #FEF3C7;
  border-color: var(--warning);
  color: #92400E;
}

/* Modern Modal Styles */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: var(--white);
  border-radius: 16px;
  box-shadow: var(--shadow-lg);
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid var(--gray-200);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  padding: 1.5rem;
  border-top: 1px solid var(--gray-200);
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
}

/* Utility Classes */
.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }

.mb-0 { margin-bottom: 0; }
.mb-1 { margin-bottom: 0.25rem; }
.mb-2 { margin-bottom: 0.5rem; }
.mb-3 { margin-bottom: 0.75rem; }
.mb-4 { margin-bottom: 1rem; }
.mb-5 { margin-bottom: 1.25rem; }

.mt-0 { margin-top: 0; }
.mt-1 { margin-top: 0.25rem; }
.mt-2 { margin-top: 0.5rem; }
.mt-3 { margin-top: 0.75rem; }
.mt-4 { margin-top: 1rem; }
.mt-5 { margin-top: 1.25rem; }

.p-0 { padding: 0; }
.p-1 { padding: 0.25rem; }
.p-2 { padding: 0.5rem; }
.p-3 { padding: 0.75rem; }
.p-4 { padding: 1rem; }
.p-5 { padding: 1.25rem; }

.d-flex { display: flex; }
.align-items-center { align-items: center; }
.justify-content-center { justify-content: center; }
.justify-content-between { justify-content: space-between; }
.gap-1 { gap: 0.25rem; }
.gap-2 { gap: 0.5rem; }
.gap-3 { gap: 0.75rem; }
.gap-4 { gap: 1rem; }

.w-100 { width: 100%; }
.h-100 { height: 100%; }

/* Responsive Design */
@media (max-width: 768px) {
  .card-body,
  .card-header {
    padding: 1rem;
  }
  
  .table th,
  .table td {
    padding: 0.75rem;
  }
  
  .btn {
    padding: 0.625rem 1.25rem;
    font-size: 0.8rem;
  }
}

/* Loading Animation */
.spinner {
  width: 2rem;
  height: 2rem;
  border: 3px solid var(--gray-200);
  border-top: 3px solid var(--primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Smooth Transitions */
.fade-in {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>

