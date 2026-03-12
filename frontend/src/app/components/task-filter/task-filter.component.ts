/**
 * TaskMaster Pro - Task Filter Component
 * Generated with GitHub Copilot assistance
 * Standalone component for filtering tasks by status
 * Constitution: Mobile-First Responsive Design (Principle III), Accessibility (Principle VI)
 */

import { Component, Output, EventEmitter, signal } from '@angular/core';
import { CommonModule } from '@angular/common';

/**
 * Filter option interface
 */
interface FilterOption {
  label: string;
  value: string | null;
}

/**
 * TaskFilterComponent
 * 
 * Provides touch-friendly status filter buttons.
 * Emits filter changes for parent components to handle.
 * 
 * User Story 1 (P1): Filter Tasks by Status
 */
@Component({
  selector: 'app-task-filter',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './task-filter.component.html',
  styleUrls: ['./task-filter.component.scss']
})
export class TaskFilterComponent {
  /**
   * Event emitted when filter selection changes
   * Emits null for "All", or status string for specific filter
   */
  @Output() filterChange = new EventEmitter<string | null>();

  /**
   * Currently active filter (using Angular signal)
   */
  activeFilter = signal<string | null>(null);

  /**
   * Available filter options
   * Includes "All" option to show all tasks
   */
  filterOptions: FilterOption[] = [
    { label: 'All', value: null },
    { label: 'Pending', value: 'Pending' },
    { label: 'In Progress', value: 'In Progress' },
    { label: 'Completed', value: 'Completed' }
  ];

  /**
   * Handle filter button click
   * Updates active filter and emits change event
   * 
   * @param value Filter value (null for "All", or status string)
   */
  onFilterClick(value: string | null): void {
    console.log('Filter changed to:', value || 'All');
    this.activeFilter.set(value);
    this.filterChange.emit(value);
  }

  /**
   * Check if a filter is currently active
   * Used for button styling
   * 
   * @param value Filter value to check
   * @returns true if this filter is active
   */
  isActive(value: string | null): boolean {
    return this.activeFilter() === value;
  }

  /**
   * Get CSS classes for filter button
   * Applies active styling when button is selected
   * 
   * @param value Filter value
   * @returns CSS class string
   */
  getButtonClass(value: string | null): string {
    const baseClasses = 'min-h-touch min-w-touch px-4 py-2 rounded-lg font-medium text-sm transition-all focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2';
    
    if (this.isActive(value)) {
      // Active button styling
      return `${baseClasses} bg-blue-600 text-white shadow-md`;
    } else {
      // Inactive button styling
      return `${baseClasses} bg-white text-gray-700 border border-gray-300 hover:bg-gray-50`;
    }
  }
}
