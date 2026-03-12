/**
 * TaskMaster Pro - Task Card Component
 * Generated with GitHub Copilot assistance
 * Standalone component for displaying individual task cards
 * Constitution: Mobile-First Responsive Design (Principle III), Accessibility (Principle VI)
 */

import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Task } from '../../models/task.model';

/**
 * TaskCardComponent
 * 
 * Displays a single task with priority styling and status indicator.
 * Provides actions for quick status toggle and task management.
 * 
 * User Story 1 (P1): View Tasks
 * User Story 3 (P3): Quick Status Update via Checkbox
 */
@Component({
  selector: 'app-task-card',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './task-card.component.html',
  styleUrls: ['./task-card.component.scss']
})
export class TaskCardComponent {
  /**
   * Task data to display
   */
  @Input({ required: true }) task!: Task;

  /**
   * Event emitted when task status changes
   * User Story 3: Quick Status Update
   */
  @Output() statusChange = new EventEmitter<{ id: number; status: string }>();

  /**
   * Event emitted when edit button is clicked
   * User Story 4: Edit Tasks
   */
  @Output() edit = new EventEmitter<Task>();

  /**
   * Event emitted when delete button is clicked
   * User Story 4: Delete Tasks
   */
  @Output() delete = new EventEmitter<number>();

  /**
   * Get priority CSS class for styling
   * Maps priority level to Tailwind utility classes
   * 
   * @returns CSS class string
   */
  getPriorityClass(): string {
    const priorityMap: { [key: string]: string } = {
      'Low': 'border-l-priority-low text-priority-low',
      'Medium': 'border-l-priority-medium text-priority-medium',
      'High': 'border-l-priority-high text-priority-high'
    };
    return priorityMap[this.task.priority] || 'border-l-gray-400 text-gray-600';
  }

  /**
   * Get status CSS class for badge styling
   * Maps status to Tailwind background colors
   * 
   * @returns CSS class string
   */
  getStatusClass(): string {
    const statusMap: { [key: string]: string } = {
      'Pending': 'bg-status-pending text-white',
      'In Progress': 'bg-status-inProgress text-white',
      'Completed': 'bg-status-completed text-white'
    };
    return statusMap[this.task.status] || 'bg-gray-400 text-white';
  }

  /**
   * Handle checkbox toggle for status update
   * User Story 3: Quick Status Update
   * 
   * @param event Checkbox change event
   */
  onStatusToggle(event: Event): void {
    const checked = (event.target as HTMLInputElement).checked;
    const newStatus = checked ? 'Completed' : 'Pending';
    
    console.log(`Task ${this.task.id} status changed to ${newStatus}`);
    this.statusChange.emit({ id: this.task.id, status: newStatus });
  }

  /**
   * Handle edit button click
   * User Story 4: Edit Tasks
   */
  onEdit(): void {
    console.log(`Edit task ${this.task.id}`);
    this.edit.emit(this.task);
  }

  /**
   * Handle delete button click
   * User Story 4: Delete Tasks
   */
  onDelete(): void {
    console.log(`Delete task ${this.task.id}`);
    this.delete.emit(this.task.id);
  }

  /**
   * Format date for display
   * Converts ISO date string to localized date string
   * 
   * @param dateString ISO date string
   * @returns Formatted date string
   */
  formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  }

  /**
   * Check if task is overdue
   * Used for visual warning indicators
   * 
   * @returns true if task is past due date and not completed
   */
  isOverdue(): boolean {
    if (this.task.status === 'Completed') {
      return false;
    }
    const dueDate = new Date(this.task.dueDate);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return dueDate < today;
  }
}
