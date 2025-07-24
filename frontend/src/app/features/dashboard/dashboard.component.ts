import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subject, takeUntil, forkJoin } from 'rxjs';
import { AuthService, TaskService, AnalyticsService } from '@core/services';
import { User, Task, TaskStatus, UserRole } from '@core/models';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit, OnDestroy {
  currentUser: User | null = null;
  tasks: Task[] = [];
  overdueTasks: Task[] = [];
  recentTasks: Task[] = [];
  isLoading = true;
  
  // Stats
  totalTasks = 0;
  completedTasks = 0;
  pendingTasks = 0;
  inProgressTasks = 0;
  completionRate = 0;

  private destroy$ = new Subject<void>();

  constructor(
    private authService: AuthService,
    private taskService: TaskService,
    private analyticsService: AnalyticsService
  ) {}

  ngOnInit(): void {
    this.currentUser = this.authService.getCurrentUserValue();
    this.loadDashboardData();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  private loadDashboardData(): void {
    this.isLoading = true;

    const requests = [
      this.taskService.getTasks(),
    ];

    // Add analytics for managers
    if (this.isManager()) {
      requests.push(
        this.analyticsService.getTaskCompletionRate(),
        this.analyticsService.getUserProductivity()
      );
    }

    forkJoin(requests)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (results) => {
          this.tasks = results[0] as Task[];
          this.processTaskData();
          this.isLoading = false;
        },
        error: (error) => {
          console.error('Error loading dashboard data:', error);
          this.isLoading = false;
        }
      });
  }

  private processTaskData(): void {
    this.totalTasks = this.tasks.length;
    this.completedTasks = this.tasks.filter(t => t.status === TaskStatus.COMPLETED).length;
    this.pendingTasks = this.tasks.filter(t => t.status === TaskStatus.PENDING).length;
    this.inProgressTasks = this.tasks.filter(t => t.status === TaskStatus.IN_PROGRESS).length;
    
    this.completionRate = this.totalTasks > 0 
      ? Math.round((this.completedTasks / this.totalTasks) * 100) 
      : 0;

    // Get overdue tasks
    const now = new Date();
    this.overdueTasks = this.tasks.filter(task => 
      task.due_date && 
      new Date(task.due_date) < now && 
      task.status !== TaskStatus.COMPLETED
    );

    // Get recent tasks (last 5)
    this.recentTasks = this.tasks
      .sort((a, b) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime())
      .slice(0, 5);
  }

  isManager(): boolean {
    return this.authService.isManager();
  }

  getStatusColor(status: TaskStatus): string {
    switch (status) {
      case TaskStatus.COMPLETED:
        return 'status-completed';
      case TaskStatus.IN_PROGRESS:
        return 'status-in-progress';
      case TaskStatus.PENDING:
        return 'status-pending';
      case TaskStatus.CANCELLED:
        return 'status-cancelled';
      default:
        return '';
    }
  }

  getPriorityColor(priority: string): string {
    switch (priority.toLowerCase()) {
      case 'high':
        return 'priority-high';
      case 'medium':
        return 'priority-medium';
      case 'low':
        return 'priority-low';
      default:
        return '';
    }
  }

  formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString();
  }

  navigateToTasks(): void {
    // Navigation logic would go here
  }

  navigateToAnalytics(): void {
    // Navigation logic would go here
  }
}