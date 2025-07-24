export interface TaskCompletionRate {
  total_tasks: number;
  completed_tasks: number;
  completion_rate: number;
  period: string;
}

export interface UserProductivity {
  user_id: number;
  total_tasks: number;
  completed_tasks: number;
  pending_tasks: number;
  in_progress_tasks: number;
  average_completion_time: number;
}

export interface TaskDistribution {
  status: string;
  count: number;
  percentage: number;
}

export interface PriorityDistribution {
  priority: string;
  count: number;
  percentage: number;
}

export interface AnalyticsDashboard {
  taskCompletion: TaskCompletionRate;
  userProductivity: UserProductivity;
  statusDistribution: TaskDistribution[];
  priorityDistribution: PriorityDistribution[];
}