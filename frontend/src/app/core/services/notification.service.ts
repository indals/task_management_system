import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, BehaviorSubject, tap } from 'rxjs';
import { Notification, NotificationResponse } from '@core/models';
import { environment } from '@environments/environment';

@Injectable({
  providedIn: 'root'
})
export class NotificationService {
  private readonly API_URL = `${environment.apiUrl}/api/notifications`;
  
  private notificationsSubject = new BehaviorSubject<Notification[]>([]);
  public notifications$ = this.notificationsSubject.asObservable();

  private unreadCountSubject = new BehaviorSubject<number>(0);
  public unreadCount$ = this.unreadCountSubject.asObservable();

  constructor(private http: HttpClient) {}

  getNotifications(unreadOnly: boolean = false): Observable<NotificationResponse> {
    let params = new HttpParams();
    if (unreadOnly) {
      params = params.set('unread_only', 'true');
    }

    return this.http.get<NotificationResponse>(this.API_URL, { params })
      .pipe(
        tap(response => {
          this.notificationsSubject.next(response.notifications);
          this.unreadCountSubject.next(response.unread_count);
        })
      );
  }

  markAsRead(notificationId: number): Observable<any> {
    return this.http.post(`${this.API_URL}/${notificationId}/read`, {})
      .pipe(
        tap(() => {
          const currentNotifications = this.notificationsSubject.value;
          const updatedNotifications = currentNotifications.map(notification =>
            notification.id === notificationId 
              ? { ...notification, read: true }
              : notification
          );
          this.notificationsSubject.next(updatedNotifications);
          this.updateUnreadCount();
        })
      );
  }

  markAllAsRead(): Observable<any> {
    return this.http.post(`${this.API_URL}/read-all`, {})
      .pipe(
        tap(() => {
          const currentNotifications = this.notificationsSubject.value;
          const updatedNotifications = currentNotifications.map(notification => ({
            ...notification,
            read: true
          }));
          this.notificationsSubject.next(updatedNotifications);
          this.unreadCountSubject.next(0);
        })
      );
  }

  deleteNotification(notificationId: number): Observable<any> {
    return this.http.delete(`${this.API_URL}/${notificationId}`)
      .pipe(
        tap(() => {
          const currentNotifications = this.notificationsSubject.value;
          const filteredNotifications = currentNotifications.filter(
            notification => notification.id !== notificationId
          );
          this.notificationsSubject.next(filteredNotifications);
          this.updateUnreadCount();
        })
      );
  }

  getUnreadCount(): number {
    return this.unreadCountSubject.value;
  }

  private updateUnreadCount(): void {
    const unreadCount = this.notificationsSubject.value
      .filter(notification => !notification.read).length;
    this.unreadCountSubject.next(unreadCount);
  }
}