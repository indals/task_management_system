export interface Notification {
  id: number;
  user_id: number;
  task_id: number;
  message: string;
  read: boolean;
  created_at: string;
}

export interface NotificationResponse {
  notifications: Notification[];
  total: number;
  unread_count: number;
}