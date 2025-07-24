import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, Router, UrlTree } from '@angular/router';
import { Observable } from 'rxjs';
import { AuthService } from '@core/services/auth.service';
import { UserRole } from '@core/models';

@Injectable({
  providedIn: 'root'
})
export class RoleGuard implements CanActivate {
  
  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  canActivate(route: ActivatedRouteSnapshot): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
    const expectedRoles: UserRole[] = route.data['expectedRoles'];
    
    if (!expectedRoles || expectedRoles.length === 0) {
      return true;
    }

    const currentUser = this.authService.getCurrentUserValue();
    
    if (!currentUser) {
      this.router.navigate(['/auth/login']);
      return false;
    }

    if (expectedRoles.includes(currentUser.role)) {
      return true;
    } else {
      this.router.navigate(['/dashboard']);
      return false;
    }
  }
}