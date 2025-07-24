import { User } from './user.model';

export interface Task {
  id: number;
  title: string;
  description: string;
  status: TaskStatus;
  priority: TaskPriority;
  assigned_to: number | null;
  created_by: number;
  due_date: string | null;
  created_at: string;
  updated_at: string;
  assignee?: User;
  creator?: User;
  comments?: TaskComment[];
}

export enum TaskStatus {
  PENDING = 'PENDING',
  IN_PROGRESS = 'IN_PROGRESS',
  COMPLETED = 'COMPLETED',
  CANCELLED = 'CANCELLED'
}

export enum TaskPriority {
  LOW = 'LOW',
  MEDIUM = 'MEDIUM',
  HIGH = 'HIGH'
}

export interface TaskComment {
  id: number;
  task_id: number;
  user_id: number;
  comment: string;
  created_at: string;
  author?: User;
}

export interface CreateTaskRequest {
  title: string;
  description: string;
  priority: TaskPriority;
  assigneeId?: number;
  due_date?: string;
}

export interface UpdateTaskRequest {
  title?: string;
  description?: string;
  status?: TaskStatus;
  priority?: TaskPriority;
  assigned_to?: number;
  due_date?: string;
}

export interface AssignTaskRequest {
  user_id: number;
}

export interface AddCommentRequest {
  text: string;
}

export interface TaskFilters {
  status?: TaskStatus;
  assignee?: number;
  created_by?: number;
  priority?: TaskPriority;
}