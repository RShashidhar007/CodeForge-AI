import { toast, type ToastOptions } from "react-toastify";

const defaultOptions: ToastOptions = {
  position: "top-right",
  autoClose: 4000,
};

export function showSuccess(message: string, options?: ToastOptions): void {
  toast.success(message, { ...defaultOptions, ...options });
}

export function showError(message: string, options?: ToastOptions): void {
  toast.error(message, { ...defaultOptions, ...options });
}

export function showInfo(message: string, options?: ToastOptions): void {
  toast.info(message, { ...defaultOptions, ...options });
}
