/**
 * TaskMaster Pro - Task Service
 * Generated with GitHub Copilot assistance
 * Angular service for task CRUD operations and state management
 * Constitution: API Contract Compliance (Principle V), TDD (Principle II)
 */

import { Injectable, signal, computed } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { tap, catchError } from 'rxjs/operators';
import { environment } from '../../environments/environment';
import { Task, TaskCreateDto, TaskUpdateDto, TaskStatusUpdateDto } from '../models/task.model';

/**
 * Task Service
 * 
 * Manages task data with HTTP API communication and reactive state management.
 * Provides CRUD operations and filtering capabilities.
 * 
 * User Story 1 (P1): View and Filter Tasks
 * User Story 2 (P2): Create New Tasks
 * User Story 3 (P3): Quick Status Update
 * User Story 4 (P4): Edit and Delete Tasks
 */
@Injectable({
  providedIn: 'root'
})
export class TaskService {
  private readonly apiUrl = `${environment.apiUrl}/tasks`;

  // Reactive state using Angular signals (v18 feature)
  private tasksSignal = signal<Task[]>([]);
  private filterSignal = signal<string | null>(null);
  private loadingSignal = signal<boolean>(false);
  private errorSignal = signal<string | null>(null);

  // Public computed signals for components
  public readonly tasks = this.tasksSignal.asReadonly();
  public readonly currentFilter = this.filterSignal.asReadonly();
  public readonly isLoading = this.loadingSignal.asReadonly();
  public readonly error = this.errorSignal.asReadonly();

  // Filtered tasks based on current filter
  public readonly filteredTasks = computed(() => {
    const allTasks = this.tasksSignal();
    const filter = this.filterSignal();
    
    if (!filter || filter === 'All') {
      return allTasks;
    }
    
    return allTasks.filter(task => task.status === filter);
  });

  constructor(private http: HttpClient) {
    console.log('TaskService initialized with API URL:', this.apiUrl);
  }

  /**
   * Fetch all tasks from the API
   * User Story 1: View and Filter Tasks
   * 
   * @returns Observable<Task[]> Array of all tasks
   */
  public getTasks(): Observable<Task[]> {
    this.loadingSignal.set(true);
    this.errorSignal.set(null);

    return this.http.get<Task[]>(this.apiUrl).pipe(
      tap(tasks => {
        console.log(`Fetched ${tasks.length} tasks from API`);
        this.tasksSignal.set(tasks);
        this.loadingSignal.set(false);
      }),
      catchError(error => {
        console.error('Error fetching tasks:', error);
        this.errorSignal.set('Failed to load tasks. Please try again.');
        this.loadingSignal.set(false);
        throw error;
      })
    );
  }

  /**
   * Fetch tasks filtered by status
   * User Story 1: View and Filter Tasks
   * 
   * @param status Status filter ('Pending', 'In Progress', 'Completed')
   * @returns Observable<Task[]> Filtered tasks
   */
  public getTasksByStatus(status: string): Observable<Task[]> {
    this.loadingSignal.set(true);
    this.errorSignal.set(null);

    const params = new HttpParams().set('status', status);
    
    return this.http.get<Task[]>(this.apiUrl, { params }).pipe(
      tap(tasks => {
        console.log(`Fetched ${tasks.length} tasks with status: ${status}`);
        this.tasksSignal.set(tasks);
        this.filterSignal.set(status);
        this.loadingSignal.set(false);
      }),
      catchError(error => {
        console.error(`Error fetching tasks with status ${status}:`, error);
        this.errorSignal.set(`Failed to filter tasks by ${status}. Please try again.`);
        this.loadingSignal.set(false);
        throw error;
      })
    );
  }

  /**
   * Apply filter to displayed tasks (client-side filtering)
   * User Story 1: View and Filter Tasks
   * 
   * @param status Status to filter by, or null for all tasks
   */
  public setFilter(status: string | null): void {
    console.log('Setting filter to:', status || 'All');
    this.filterSignal.set(status);
  }

  /**
   * Clear the current filter and show all tasks
   * User Story 1: View and Filter Tasks
   */
  public clearFilter(): void {
    console.log('Clearing filter');
    this.filterSignal.set(null);
  }

  /**
   * Fetch a single task by ID
   * 
   * @param id Task ID
   * @returns Observable<Task> Task details
   */
  public getTaskById(id: number): Observable<Task> {
    this.loadingSignal.set(true);
    this.errorSignal.set(null);

    return this.http.get<Task>(`${this.apiUrl}/${id}`).pipe(
      tap(task => {
        console.log('Fetched task:', task);
        this.loadingSignal.set(false);
      }),
      catchError(error => {
        console.error(`Error fetching task ${id}:`, error);
        this.errorSignal.set('Failed to load task. Please try again.');
        this.loadingSignal.set(false);
        throw error;
      })
    );
  }

  /**
   * Create a new task
   * User Story 2: Create New Tasks
   * 
   * @param taskData Task creation data
   * @returns Observable<Task> Created task with ID
   */
  public createTask(taskData: TaskCreateDto): Observable<Task> {
    this.loadingSignal.set(true);
    this.errorSignal.set(null);

    return this.http.post<Task>(this.apiUrl, taskData).pipe(
      tap(newTask => {
        console.log('Created task:', newTask);
        // Add new task to local state
        const currentTasks = this.tasksSignal();
        this.tasksSignal.set([...currentTasks, newTask]);
        this.loadingSignal.set(false);
      }),
      catchError(error => {
        console.error('Error creating task:', error);
        this.errorSignal.set('Failed to create task. Please try again.');
        this.loadingSignal.set(false);
        throw error;
      })
    );
  }

  /**
   * Update an existing task
   * User Story 4: Edit Tasks
   * 
   * @param id Task ID
   * @param taskData Updated task data
   * @returns Observable<Task> Updated task
   */
  public updateTask(id: number, taskData: TaskUpdateDto): Observable<Task> {
    this.loadingSignal.set(true);
    this.errorSignal.set(null);

    return this.http.put<Task>(`${this.apiUrl}/${id}`, taskData).pipe(
      tap(updatedTask => {
        console.log('Updated task:', updatedTask);
        // Update task in local state
        const currentTasks = this.tasksSignal();
        const updatedTasks = currentTasks.map(task => 
          task.id === id ? updatedTask : task
        );
        this.tasksSignal.set(updatedTasks);
        this.loadingSignal.set(false);
      }),
      catchError(error => {
        console.error(`Error updating task ${id}:`, error);
        this.errorSignal.set('Failed to update task. Please try again.');
        this.loadingSignal.set(false);
        throw error;
      })
    );
  }

  /**
   * Quick status update for a task (checkbox toggle)
   * User Story 3: Quick Status Update via Checkbox
   * 
   * @param id Task ID
   * @param status New status
   * @returns Observable<Task> Updated task
   */
  public updateTaskStatus(id: number, status: string): Observable<Task> {
    this.loadingSignal.set(true);
    this.errorSignal.set(null);

    const statusUpdate: TaskStatusUpdateDto = { status };

    return this.http.patch<Task>(`${this.apiUrl}/${id}/status`, statusUpdate).pipe(
      tap(updatedTask => {
        console.log(`Updated task ${id} status to ${status}`);
        // Update task in local state
        const currentTasks = this.tasksSignal();
        const updatedTasks = currentTasks.map(task => 
          task.id === id ? updatedTask : task
        );
        this.tasksSignal.set(updatedTasks);
        this.loadingSignal.set(false);
      }),
      catchError(error => {
        console.error(`Error updating task ${id} status:`, error);
        this.errorSignal.set('Failed to update task status. Please try again.');
        this.loadingSignal.set(false);
        throw error;
      })
    );
  }

  /**
   * Delete a task
   * User Story 4: Delete Tasks
   * 
   * @param id Task ID
   * @returns Observable<void>
   */
  public deleteTask(id: number): Observable<void> {
    this.loadingSignal.set(true);
    this.errorSignal.set(null);

    return this.http.delete<void>(`${this.apiUrl}/${id}`).pipe(
      tap(() => {
        console.log(`Deleted task ${id}`);
        // Remove task from local state
        const currentTasks = this.tasksSignal();
        const updatedTasks = currentTasks.filter(task => task.id !== id);
        this.tasksSignal.set(updatedTasks);
        this.loadingSignal.set(false);
      }),
      catchError(error => {
        console.error(`Error deleting task ${id}:`, error);
        this.errorSignal.set('Failed to delete task. Please try again.');
        this.loadingSignal.set(false);
        throw error;
      })
    );
  }
}
