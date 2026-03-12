/**
 * TaskMaster Pro - TypeScript Task Interfaces
 * Generated with GitHub Copilot assistance
 * Type-safe interfaces matching backend Pydantic schemas
 * Constitution: API Contract Compliance (Principle V)
 */

/**
 * Task priority level
 * Must match backend PriorityType enum
 */
export type TaskPriority = 'Low' | 'Medium' | 'High';

/**
 * Task status
 * Must match backend StatusType enum
 */
export type TaskStatus = 'Pending' | 'In Progress' | 'Completed';

/**
 * Complete Task interface matching TaskResponse from backend
 * Used for displaying existing tasks from API
 */
export interface Task {
  id: number;
  title: string;
  description: string;
  dueDate: string;              // ISO date string (YYYY-MM-DD)
  priority: TaskPriority;
  status: TaskStatus;
  reminderSent: boolean;
  createdAt: string;            // ISO datetime string
  updatedAt: string;            // ISO datetime string
}

/**
 * Task creation DTO matching TaskCreate from backend
 * Used for creating new tasks (POST /api/tasks)
 */
export interface TaskCreateDto {
  title: string;
  description: string;
  dueDate: string;              // ISO date string (YYYY-MM-DD)
  priority: TaskPriority;
  status: TaskStatus;
}

/**
 * Task update DTO matching TaskUpdate from backend
 * All fields optional for partial updates (PUT /api/tasks/{id})
 */
export interface TaskUpdateDto {
  title?: string;
  description?: string;
  dueDate?: string;             // ISO date string (YYYY-MM-DD)
  priority?: TaskPriority;
  status?: TaskStatus;
}

/**
 * Quick status update DTO matching TaskStatusUpdate from backend
 * Used for checkbox toggle (PATCH /api/tasks/{id}/status)
 * User Story 3: Quick Status Update via Checkbox
 */
export interface TaskStatusUpdateDto {
  status: TaskStatus;
}

/**
 * API error response interface
 * Standardized error format from FastAPI
 */
export interface ApiError {
  detail: string | ApiValidationError[];
}

/**
 * Validation error detail from Pydantic
 */
export interface ApiValidationError {
  loc: (string | number)[];
  msg: string;
  type: string;
}
