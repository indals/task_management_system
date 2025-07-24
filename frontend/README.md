# Task Management System - Angular Frontend

A production-quality Angular frontend for a Flask-based Task Management System, similar to Jira, Asana, or Trello. Built with Angular 17, Angular Material, and modern development practices.

## 🚀 Features

### 🔐 Authentication & Authorization
- JWT-based authentication
- Role-based access control (Manager vs Employee)
- Login/Register with form validation
- Auto token refresh and logout

### 👥 User Roles & Permissions
**Manager:**
- Create and manage projects
- Assign tasks to employees
- View analytics and reports
- Track team performance
- Manage all tasks

**Employee:**
- View assigned tasks
- Update task status
- Add comments to tasks
- View personal dashboard

### 📋 Task Management
- Create, edit, and delete tasks
- Task assignment and reassignment
- Priority levels (High, Medium, Low)
- Status tracking (Pending, In Progress, Completed, Cancelled)
- Due date management
- Task comments and collaboration
- Overdue task indicators

### 📊 Analytics & Reporting (Manager Only)
- Task completion rates
- User productivity metrics
- Task status distribution charts
- Priority distribution analysis
- Performance dashboards

### 🔔 Real-time Notifications
- Task assignment notifications
- Status change alerts
- Due date reminders
- Real-time updates

## 🏗️ Architecture

### Folder Structure
```
src/app/
├── core/                     # Singleton services, guards, interceptors
│   ├── models/              # TypeScript interfaces and enums
│   │   ├── user.model.ts
│   │   ├── task.model.ts
│   │   ├── notification.model.ts
│   │   ├── analytics.model.ts
│   │   └── index.ts         # Barrel exports
│   ├── services/            # Global services
│   │   ├── auth.service.ts
│   │   ├── task.service.ts
│   │   ├── notification.service.ts
│   │   ├── analytics.service.ts
│   │   └── index.ts
│   ├── guards/              # Route guards
│   │   ├── auth.guard.ts
│   │   └── role.guard.ts
│   ├── interceptors/        # HTTP interceptors
│   │   └── auth.interceptor.ts
│   └── index.ts
├── shared/                  # Reusable components and utilities
│   ├── components/
│   │   ├── header/
│   │   ├── loading-spinner/
│   │   └── task-card/
│   └── index.ts
├── features/                # Feature modules (lazy-loaded)
│   ├── auth/
│   │   ├── login/
│   │   ├── register/
│   │   └── auth.module.ts
│   ├── dashboard/
│   │   ├── dashboard.component.ts
│   │   └── dashboard.module.ts
│   ├── tasks/
│   │   ├── task-list/
│   │   ├── task-detail/
│   │   ├── task-form/
│   │   └── tasks.module.ts
│   ├── projects/            # Manager only
│   │   ├── project-list/
│   │   ├── project-form/
│   │   └── projects.module.ts
│   ├── analytics/           # Manager only
│   │   ├── analytics-dashboard/
│   │   ├── charts/
│   │   └── analytics.module.ts
│   ├── notifications/
│   │   ├── notification-list/
│   │   └── notifications.module.ts
│   └── profile/
│       ├── profile-view/
│       ├── profile-edit/
│       └── profile.module.ts
├── app-routing.module.ts    # Main routing configuration
├── app.component.ts
├── app.component.html
├── app.component.scss
└── app.module.ts
```

### Key Architecture Principles

1. **Modular Design**: Features are organized into lazy-loaded modules
2. **Barrel Exports**: Clean imports using index.ts files
3. **Separation of Concerns**: Clear separation between models, services, and components
4. **Reactive Programming**: RxJS observables for async operations
5. **Type Safety**: Strong TypeScript typing throughout
6. **Material Design**: Consistent UI using Angular Material
7. **Responsive Design**: Mobile-first approach

## 🛠️ Technology Stack

- **Angular 17** - Latest Angular framework
- **Angular Material** - UI component library
- **RxJS** - Reactive programming
- **TypeScript** - Type-safe JavaScript
- **SCSS** - Enhanced CSS with variables and mixins
- **Chart.js** - Data visualization
- **Date-fns** - Date manipulation utilities

## 📦 Installation & Setup

### Prerequisites
- Node.js (v18 or higher)
- npm or yarn
- Angular CLI (`npm install -g @angular/cli`)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd task-management-frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment**
   Update `src/environments/environment.ts` with your Flask API URL:
   ```typescript
   export const environment = {
     production: false,
     apiUrl: 'http://localhost:5000'  // Your Flask API URL
   };
   ```

4. **Start the development server**
   ```bash
   npm start
   # or
   ng serve
   ```

5. **Open your browser**
   Navigate to `http://localhost:4200`

### Production Build
```bash
npm run build
# or
ng build --prod
```

## 🔧 Configuration

### Environment Variables
- `environment.apiUrl`: Flask API base URL
- `environment.production`: Production flag

### API Integration
The frontend is designed to work with the Flask Task Management API with these endpoints:

**Authentication:**
- `POST /api/auth/login`
- `POST /api/auth/register`
- `GET /api/auth/me`
- `PUT /api/auth/profile`

**Tasks:**
- `GET /api/tasks`
- `POST /api/tasks`
- `GET /api/tasks/{id}`
- `PUT /api/tasks/{id}`
- `DELETE /api/tasks/{id}`
- `POST /api/tasks/{id}/assign`
- `POST /api/tasks/{id}/comments`

**Analytics:**
- `GET /api/analytics/task-completion`
- `GET /api/analytics/user-productivity`
- `GET /api/analytics/task-status-distribution`

**Notifications:**
- `GET /api/notifications`
- `POST /api/notifications/{id}/read`
- `POST /api/notifications/read-all`

## 🎨 UI/UX Features

### Design System
- **Material Design 3** principles
- **Consistent color palette** with primary, accent, and warn colors
- **Typography scale** using Roboto font family
- **Elevation and shadows** for depth
- **Responsive breakpoints** for mobile, tablet, and desktop

### User Experience
- **Loading states** with spinners and skeleton screens
- **Error handling** with user-friendly messages
- **Form validation** with real-time feedback
- **Keyboard navigation** support
- **Accessibility** features (ARIA labels, focus management)

### Dashboard Features
- **Role-based dashboard** content
- **Quick stats cards** with key metrics
- **Recent tasks** overview
- **Overdue tasks** highlighting
- **Performance charts** (Manager view)

## 🔐 Security Features

### Authentication
- **JWT token** storage in localStorage
- **Automatic token refresh** before expiration
- **Secure logout** with token cleanup
- **Route protection** with guards

### Authorization
- **Role-based access control** (RBAC)
- **Feature-level permissions** (Manager vs Employee views)
- **API endpoint protection** via interceptors
- **XSS protection** with Angular's built-in sanitization

## 📱 Responsive Design

### Breakpoints
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

### Mobile Features
- **Collapsible navigation** menu
- **Touch-friendly** button sizes
- **Optimized forms** for mobile input
- **Swipe gestures** for task cards

## 🧪 Testing Strategy

### Unit Testing
```bash
npm test
# or
ng test
```

### E2E Testing
```bash
npm run e2e
# or
ng e2e
```

### Test Structure
- **Component tests** for UI components
- **Service tests** for business logic
- **Guard tests** for route protection
- **Interceptor tests** for HTTP handling

## 🚀 Deployment

### Development
```bash
ng serve --host 0.0.0.0 --port 4200
```

### Production
```bash
ng build --prod
```

### Docker Deployment
```dockerfile
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist/task-management-frontend /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## 📊 Performance Optimizations

### Code Splitting
- **Lazy loading** for feature modules
- **Dynamic imports** for heavy components
- **Tree shaking** for unused code elimination

### Bundle Optimization
- **AOT compilation** for smaller bundles
- **Minification** and **uglification**
- **Gzip compression** for assets

### Runtime Performance
- **OnPush change detection** strategy
- **TrackBy functions** for ngFor loops
- **Async pipe** for automatic subscriptions
- **Virtual scrolling** for large lists

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Code Style
- Follow **Angular Style Guide**
- Use **Prettier** for code formatting
- Follow **TypeScript best practices**
- Write **meaningful commit messages**

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. **Check the documentation** first
2. **Search existing issues** on GitHub
3. **Create a new issue** with detailed information
4. **Contact the development team**

## 🎯 Roadmap

### Phase 1 (Current)
- ✅ Authentication and authorization
- ✅ Task management CRUD operations
- ✅ User dashboard
- ✅ Basic notifications

### Phase 2 (Upcoming)
- 🔄 Real-time updates with WebSockets
- 🔄 Advanced search and filtering
- 🔄 File attachments for tasks
- 🔄 Team collaboration features

### Phase 3 (Future)
- 📅 Calendar integration
- 📊 Advanced analytics
- 🔗 Third-party integrations
- 📱 Mobile app (Ionic/React Native)

---

**Built with ❤️ by the Task Management Team**