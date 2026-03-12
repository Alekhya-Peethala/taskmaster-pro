/**
 * TaskMaster Pro - HTTP Error Interceptor
 * Generated with GitHub Copilot assistance
 * Global HTTP error handling for Angular application
 * Provides consistent error handling and user notifications
 */

import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { catchError, throwError } from 'rxjs';

/**
 * HTTP Interceptor for handling API errors
 * Catches HTTP errors and provides consistent error handling
 */
export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      let errorMessage = 'An unexpected error occurred';

      if (error.error instanceof ErrorEvent) {
        // Client-side or network error
        errorMessage = `Network error: ${error.error.message}`;
        console.error('Client-side error:', error.error.message);
      } else {
        // Backend returned an unsuccessful response code
        if (error.status === 0) {
          errorMessage = 'Unable to connect to server. Please check your network connection.';
        } else if (error.status === 400) {
          // Validation errors from Pydantic
          if (error.error?.detail && Array.isArray(error.error.detail)) {
            const validationErrors = error.error.detail
              .map((err: any) => `${err.loc.join('.')}: ${err.msg}`)
              .join(', ');
            errorMessage = `Validation error: ${validationErrors}`;
          } else {
            errorMessage = error.error?.detail || 'Invalid request data';
          }
        } else if (error.status === 404) {
          errorMessage = 'Resource not found';
        } else if (error.status === 500) {
          errorMessage = 'Server error. Please try again later.';
        } else {
          errorMessage = error.error?.detail || `Error: ${error.statusText}`;
        }

        console.error(
          `Backend error: ${error.status} - ${error.statusText}`,
          error.error
        );
      }

      // TODO: Display error message to user via notification service
      // Example: inject(NotificationService).showError(errorMessage);

      // Re-throw the error for component-level handling
      return throwError(() => new Error(errorMessage));
    })
  );
};
