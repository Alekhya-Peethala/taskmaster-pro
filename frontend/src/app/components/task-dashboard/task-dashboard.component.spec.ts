/**
 * TaskMaster Pro - Task Dashboard Component Tests
 * Generated with GitHub Copilot assistance
 * Test-Driven Development: Write test FIRST, verify FAIL, then implement (Principle II)
 * User Story 1: View and Filter Tasks (P1) - Dashboard loading workflow
 */

import { ComponentFixture, TestBed } from '@angular/core/testing';
import { TaskDashboardComponent } from './task-dashboard.component';
import { TaskService } from '../../services/task.service';
import { of, throwError } from 'rxjs';
import { Task } from '../../models/task.model';

describe('TaskDashboardComponent', () => {
  let component: TaskDashboardComponent;
  let fixture: ComponentFixture<TaskDashboardComponent>;
  let taskServiceSpy: jasmine.SpyObj<TaskService>;

  const mockTasks: Task[] = [
    {
      id: 1,
      title: 'Task 1',
      description: 'Description 1',
      dueDate: '2026-03-15',
      priority: 'High',
      status: 'Pending',
      reminderSent: false,
      createdAt: '2026-03-12T10:00:00Z',
      updatedAt: '2026-03-12T10:00:00Z',
    },
    {
      id: 2,
      title: 'Task 2',
      description: 'Description 2',
      dueDate: '2026-03-16',
      priority: 'Medium',
      status: 'In Progress',
      reminderSent: false,
      createdAt: '2026-03-12T11:00:00Z',
      updatedAt: '2026-03-12T11:00:00Z',
    },
  ];

  beforeEach(async () => {
    const spy = jasmine.createSpyObj('TaskService', ['getTasks', 'filterByStatus']);

    await TestBed.configureTestingModule({
      imports: [TaskDashboardComponent],
      providers: [{ provide: TaskService, useValue: spy }],
    }).compileComponents();

    taskServiceSpy = TestBed.inject(TaskService) as jasmine.SpyObj<TaskService>;
    fixture = TestBed.createComponent(TaskDashboardComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load all tasks on initialization', () => {
    taskServiceSpy.getTasks.and.returnValue(of(mockTasks));

    fixture.detectChanges(); // Trigger ngOnInit

    expect(taskServiceSpy.getTasks).toHaveBeenCalled();
    expect(component.tasks).toEqual(mockTasks);
    expect(component.tasks.length).toBe(2);
  });

  it('should display loading state while fetching tasks', () => {
    taskServiceSpy.getTasks.and.returnValue(of(mockTasks));

    expect(component.loading).toBeTruthy(); // Initially loading

    fixture.detectChanges();

    expect(component.loading).toBeFalsy(); // Loading complete
  });

  it('should handle error when loading tasks fails', () => {
    const errorMessage = 'Failed to load tasks';
    taskServiceSpy.getTasks.and.returnValue(throwError(() => new Error(errorMessage)));

    fixture.detectChanges();

    expect(component.error).toBeTruthy();
    expect(component.tasks.length).toBe(0);
  });

  it('should display empty state when no tasks exist', () => {
    taskServiceSpy.getTasks.and.returnValue(of([]));

    fixture.detectChanges();

    expect(component.tasks.length).toBe(0);
    // TODO: Verify empty state message is displayed in template
  });

  it('should render task cards for each task', () => {
    taskServiceSpy.getTasks.and.returnValue(of(mockTasks));

    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    const taskCards = compiled.querySelectorAll('app-task-card');

    expect(taskCards.length).toBe(2);
  });

  it('should update tasks when filter is applied', () => {
    const filteredTasks = [mockTasks[0]]; // Only pending tasks
    taskServiceSpy.getTasks.and.returnValue(of(mockTasks));
    taskServiceSpy.filterByStatus.and.returnValue(of(filteredTasks));

    fixture.detectChanges();

    component.applyFilter('Pending');

    expect(taskServiceSpy.filterByStatus).toHaveBeenCalledWith('Pending');
    expect(component.tasks).toEqual(filteredTasks);
  });

  it('should display all tasks when filter is cleared', () => {
    taskServiceSpy.getTasks.and.returnValue(of(mockTasks));

    fixture.detectChanges();

    component.clearFilter();

    expect(taskServiceSpy.getTasks).toHaveBeenCalled();
    expect(component.tasks).toEqual(mockTasks);
  });
});
