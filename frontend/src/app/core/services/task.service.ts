import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, BehaviorSubject, tap } from 'rxjs';
import { 
  Task, 
  CreateTaskRequest, 
  UpdateTaskRequest, 
  AssignTaskRequest,
  AddCommentRequest,
  TaskFilters
} from '@core/models';
import { environment } from '@environments/environment';

@Injectable({
  providedIn: 'root'
})
export class TaskService {
  private readonly API_URL = `${environment.apiUrl}/api/tasks`;
  
  private tasksSubject = new BehaviorSubject<Task[]>([]);
  public tasks$ = this.tasksSubject.asObservable();

  constructor(private http: HttpClient) {}

  getTasks(filters?: TaskFilters): Observable<Task[]> {
    let params = new HttpParams();
    
    if (filters) {
      if (filters.status) params = params.set('status', filters.status);
      if (filters.assignee) params = params.set('assignee', filters.assignee.toString());
      if (filters.created_by) params = params.set('created_by', filters.created_by.toString());
      if (filters.priority) params = params.set('priority', filters.priority);
    }

    return this.http.get<Task[]>(this.API_URL, { params })
      .pipe(
        tap(tasks => this.tasksSubject.next(tasks))
      );
  }

  getTaskById(id: number): Observable<Task> {
    return this.http.get<Task>(`${this.API_URL}/${id}`);
  }

  createTask(task: CreateTaskRequest): Observable<Task> {
    const payload = {
      ...task,
      user_id: this.getCurrentUserId()
    };
    
    return this.http.post<Task>(this.API_URL, payload)
      .pipe(
        tap(newTask => {
          const currentTasks = this.tasksSubject.value;
          this.tasksSubject.next([...currentTasks, newTask]);
        })
      );
  }

  updateTask(id: number, task: UpdateTaskRequest): Observable<Task> {
    return this.http.put<Task>(`${this.API_URL}/${id}`, task)
      .pipe(
        tap(updatedTask => {
          const currentTasks = this.tasksSubject.value;
          const index = currentTasks.findIndex(t => t.id === id);
          if (index !== -1) {
            currentTasks[index] = updatedTask;
            this.tasksSubject.next([...currentTasks]);
          }
        })
      );
  }

  deleteTask(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API_URL}/${id}`)
      .pipe(
        tap(() => {
          const currentTasks = this.tasksSubject.value;
          const filteredTasks = currentTasks.filter(t => t.id !== id);
          this.tasksSubject.next(filteredTasks);
        })
      );
  }

  assignTask(taskId: number, userId: number): Observable<Task> {
    const payload: AssignTaskRequest = { user_id: userId };
    return this.http.post<Task>(`${this.API_URL}/${taskId}/assign`, payload)
      .pipe(
        tap(updatedTask => {
          const currentTasks = this.tasksSubject.value;
          const index = currentTasks.findIndex(t => t.id === taskId);
          if (index !== -1) {
            currentTasks[index] = updatedTask;
            this.tasksSubject.next([...currentTasks]);
          }
        })
      );
  }

  addComment(taskId: number, comment: string): Observable<any> {
    const payload: AddCommentRequest = { text: comment };
    return this.http.post(`${this.API_URL}/${taskId}/comments`, payload);
  }

  // Utility methods for task management
  getTasksByStatus(status: string): Task[] {
    return this.tasksSubject.value.filter(task => task.status === status);
  }

  getOverdueTasks(): Task[] {
    const now = new Date();
    return this.tasksSubject.value.filter(task => 
      task.due_date && 
      new Date(task.due_date) < now && 
      task.status !== 'COMPLETED'
    );
  }

  getTasksAssignedToUser(userId: number): Task[] {
    return this.tasksSubject.value.filter(task => task.assigned_to === userId);
  }

  getTasksCreatedByUser(userId: number): Task[] {
    return this.tasksSubject.value.filter(task => task.created_by === userId);
  }

  private getCurrentUserId(): number {
    const user = JSON.parse(localStorage.getItem('current_user') || '{}');
    return user.id;
  }
}