/**
 * TaskMaster Pro - Production Environment Configuration
 * Generated with GitHub Copilot assistance
 * Configuration for Azure Container Apps deployment
 * Constitution: Azure-Native Architecture (Principle I)
 */

export const environment = {
  production: true,
  apiUrl: 'https://taskmaster-api.azurecontainerapps.io/api',  // Azure Container Apps backend
  apiTimeout: 30000,                                             // 30 seconds timeout
  enableDebugLogs: false,                                        // Disable console logging in prod
};
