import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { 
  TaskCompletionRate, 
  UserProductivity, 
  TaskDistribution, 
  PriorityDistribution 
} from '@core/models';
import { environment } from '@environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AnalyticsService {
  private readonly API_URL = `${environment.apiUrl}/api/analytics`;

  constructor(private http: HttpClient) {}

  getTaskCompletionRate(userId?: number, period: string = 'month'): Observable<TaskCompletionRate> {
    let params = new HttpParams().set('period', period);
    if (userId) {
      params = params.set('user_id', userId.toString());
    }

    return this.http.get<TaskCompletionRate>(`${this.API_URL}/task-completion`, { params });
  }

  getUserProductivity(userId?: number): Observable<UserProductivity> {
    let params = new HttpParams();
    if (userId) {
      params = params.set('user_id', userId.toString());
    }

    return this.http.get<UserProductivity>(`${this.API_URL}/user-productivity`, { params });
  }

  getTaskStatusDistribution(): Observable<TaskDistribution[]> {
    return this.http.get<TaskDistribution[]>(`${this.API_URL}/task-status-distribution`);
  }

  getTaskPriorityDistribution(): Observable<PriorityDistribution[]> {
    return this.http.get<PriorityDistribution[]>(`${this.API_URL}/task-priority-distribution`);
  }

  // Utility methods for data processing
  calculateCompletionPercentage(completed: number, total: number): number {
    return total > 0 ? Math.round((completed / total) * 100) : 0;
  }

  formatChartData(data: TaskDistribution[]): any {
    return {
      labels: data.map(item => item.status),
      datasets: [{
        data: data.map(item => item.count),
        backgroundColor: [
          '#FF6384',
          '#36A2EB',
          '#FFCE56',
          '#4BC0C0'
        ]
      }]
    };
  }

  formatPriorityChartData(data: PriorityDistribution[]): any {
    return {
      labels: data.map(item => item.priority),
      datasets: [{
        data: data.map(item => item.count),
        backgroundColor: [
          '#FF6B6B', // High priority - Red
          '#FFD93D', // Medium priority - Yellow
          '#6BCF7F'  // Low priority - Green
        ]
      }]
    };
  }
}