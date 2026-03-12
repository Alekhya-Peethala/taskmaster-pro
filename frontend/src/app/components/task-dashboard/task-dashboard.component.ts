/**
 * TaskMaster Pro - Task Dashboard Component
 * Generated with GitHub Copilot assistance
 * Main dashboard for viewing and managing tasks
 * Constitution: Mobile-First Responsive Design (Principle III), TDD (Principle II)
 */

import { Component, OnInit, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TaskService } from '../../services/task.service';
import { TaskFilterComponent } from '../task-filter/task-filter.component';
import { TaskCardComponent } from '../task-card/task-card.component';
import { Task } from '../../models/task.model';

/**
 * TaskDashboardComponent
 * 
 * Main dashboard displaying tasks with filtering capability.
 * Manages task loading, filtering, and CRUD operations.
 * 
 * User Story 1 (P1): View and Filter Tasks
 * User Story 3 (P3): Quick Status Update
 * User Story 4 (P4): Edit and Delete Tasks
 */
@Component({
  selector: 'app-task-dashboard',
  standalone: true,
  imports: [CommonModule, TaskFilterComponent, TaskCardComponent],
  templateUrl: './task-dashboard.component.html',
  styleUrls: ['./task-dashboard.component.scss']
})
export class TaskDashboardComponent implements OnInit {
  /**
   * Computed signal for filtered tasks from service
   */
  tasks = computed(() => this.taskService.filteredTasks());

  /**
   * Loading state signal
   */
  isLoading = computed(() => this.taskService.isLoading());

  /**
   * Error state signal
   */
  error = computed(() => this.taskService.error());

  /**
   * Current filter signal
   */
  currentFilter = computed(() => this.taskService.currentFilter());

  constructor(private taskService: TaskService) {
    console.log('TaskDashboardComponent initialized');
  }

  /**
   * Component initialization
   * Loads tasks from API on component load
   */
  ngOnInit(): void {
    console.log('Loading tasks...');
    this.loadTasks();
  }

  /**
   * Load all tasks from API
   * User Story 1: View Tasks
   */
  loadTasks(): void {
    this.taskService.getTasks().subscribe({
      next: (tasks) => {
        console.log(`Loaded ${tasks.length} tasks successfully`);
      },
      error: (error) => {
        console.error('Failed to load tasks:', error);
      }
    });
  }

  /**
   * Handle filter change from TaskFilterComponent
   * User Story 1: Filter Tasks
   * 
   * @param status Filter value (null for All, or status string)
   */
  onFilterChange(status: string | null): void {
    console.log('Dashboard filter changed to:', status || 'All');
    
    if (status === null) {
      // Show all tasks (client-side)
      this.taskService.setFilter(null);
    } else {
      // Filter by status (client-side using signal computed)
      this.taskService.setFilter(status);
    }
  }

  /**
   * Handle status change from TaskCardComponent
   * User Story 3: Quick Status Update
   * 
   * @param event Status change event with task ID and new status
   */
  onStatusChange(event: { id: number; status: string }): void {
    console.log(`Updating task ${event.id} status to ${event.status}`);
    
    this.taskService.updateTaskStatus(event.id, event.status).subscribe({
      next: (updatedTask) => {
        console.log('Task status updated successfully:', updatedTask);
      },
      error: (error) => {
        console.error('Failed to update task status:', error);
        alert('Failed to update task status. Please try again.');
      }
    });
  }

  /**
   * Handle edit action from TaskCardComponent
   * User Story 4: Edit Tasks
   * 
   * @param task Task to edit
   */
  onEditTask(task: Task): void {
    console.log('Edit task:', task);
    // TODO: Open edit modal/form (User Story 4 implementation)
    alert(`Edit functionality for task "${task.title}" will be implemented in User Story 4`);
  }

  /**
   * Handle delete action from TaskCardComponent
   * User Story 4: Delete Tasks
   * 
   * @param taskId ID of task to delete
   */
  onDeleteTask(taskId: number): void {
    const confirmed = confirm('Are you sure you want to delete this task?');
    
    if (!confirmed) {
      console.log('Delete cancelled');
      return;
    }

    console.log('Deleting task:', taskId);
    
    this.taskService.deleteTask(taskId).subscribe({
      next: () => {
        console.log(`Task ${taskId} deleted successfully`);
      },
      error: (error) => {
        console.error('Failed to delete task:', error);
        alert('Failed to delete task. Please try again.');
      }
    });
  }

  /**
   * Retry loading tasks after error
   */
  retryLoad(): void {
    console.log('Retrying task load...');
    this.loadTasks();
  }

  /**
   * TrackBy function for ngFor performance optimization
   * Prevents unnecessary re-rendering of task cards
   * 
   * @param index Array index
   * @param task Task item
   * @returns Unique identifier for tracking
   */
  trackByTaskId(index: number, task: Task): number {
    return task.id;
  }
}
