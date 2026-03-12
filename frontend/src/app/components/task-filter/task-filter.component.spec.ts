/**
 * TaskMaster Pro - Task Filter Component Tests
 * Generated with GitHub Copilot assistance
 * Test-Driven Development: Write test FIRST, verify FAIL, then implement (Principle II)
 * User Story 1: View and Filter Tasks (P1) - Status filter interaction
 */

import { ComponentFixture, TestBed } from '@angular/core/testing';
import { TaskFilterComponent } from './task-filter.component';
import { TaskStatus } from '../../models/task.model';

describe('TaskFilterComponent', () => {
  let component: TaskFilterComponent;
  let fixture: ComponentFixture<TaskFilterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TaskFilterComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(TaskFilterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should have all status filter options', () => {
    const expectedOptions: (TaskStatus | 'All')[] = ['All', 'Pending', 'In Progress', 'Completed'];

    expect(component.filterOptions).toEqual(expectedOptions);
  });

  it('should default to "All" filter', () => {
    expect(component.selectedFilter).toBe('All');
  });

  it('should emit filterChange event when filter is selected', () => {
    spyOn(component.filterChange, 'emit');

    component.selectFilter('Pending');

    expect(component.filterChange.emit).toHaveBeenCalledWith('Pending');
    expect(component.selectedFilter).toBe('Pending');
  });

  it('should emit null when "All" filter is selected', () => {
    spyOn(component.filterChange, 'emit');

    component.selectFilter('All');

    expect(component.filterChange.emit).toHaveBeenCalledWith(null);
    expect(component.selectedFilter).toBe('All');
  });

  it('should render filter buttons for each option', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    const buttons = compiled.querySelectorAll('button');

    expect(buttons.length).toBe(4); // All, Pending, In Progress, Completed
  });

  it('should apply active state to selected filter button', () => {
    component.selectFilter('Pending');
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    const activeButton = compiled.querySelector('button.active');

    expect(activeButton).toBeTruthy();
    expect(activeButton?.textContent).toContain('Pending');
  });

  it('should have touch-friendly button sizes (44x44px minimum)', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    const firstButton = compiled.querySelector('button') as HTMLElement;

    // Buttons should meet minimum touch target size (Constitution Principle IV)
    const { minWidth, minHeight } = window.getComputedStyle(firstButton);
    
    const minWidthValue = parseFloat(minWidth);
    const minHeightValue = parseFloat(minHeight);

    expect(minWidthValue).toBeGreaterThanOrEqual(44);
    expect(minHeightValue).toBeGreaterThanOrEqual(44);
  });

  it('should change filter when button is clicked', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    const pendingButton = Array.from(compiled.querySelectorAll('button')).find(
      btn => btn.textContent?.includes('Pending')
    ) as HTMLButtonElement;

    spyOn(component.filterChange, 'emit');

    pendingButton.click();
    fixture.detectChanges();

    expect(component.selectedFilter).toBe('Pending');
    expect(component.filterChange.emit).toHaveBeenCalledWith('Pending');
  });

  it('should update UI when filter changes', () => {
    component.selectFilter('In Progress');
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    const activeButton = compiled.querySelector('button.active');

    expect(activeButton?.textContent).toContain('In Progress');
  });
});
