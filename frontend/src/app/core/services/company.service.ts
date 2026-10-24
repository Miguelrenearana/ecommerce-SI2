import { Injectable, inject } from '@angular/core';
import { Observable, map } from 'rxjs';
import { ApiService } from './api.service';
import { ApiResponse, Company, CompanyCreateDto, Plan } from '../models/company.model';

@Injectable({ providedIn: 'root' })
export class CompanyService {
  private readonly api = inject(ApiService);

  getCompanies(statusFilter?: string): Observable<Company[]> {
    const query = statusFilter && statusFilter !== 'all' ? `?status=${statusFilter}` : '';
    return this.api.get<ApiResponse<Company[]>>(`/saas/companies${query}`).pipe(
      map((res) => res.data || []),
    );
  }

  getCompanyById(id: string): Observable<Company> {
    return this.api.get<ApiResponse<Company>>(`/saas/companies/${id}`).pipe(
      map((res) => res.data),
    );
  }

  getPlans(): Observable<Plan[]> {
    return this.api.get<ApiResponse<Plan[]>>('/saas/plans').pipe(
      map((res) => res.data || []),
    );
  }

  createCompany(dto: CompanyCreateDto): Observable<{ company: Company; initial_admin_id?: string }> {
    return this.api.post<ApiResponse<{ company: Company; initial_admin_id?: string }>>('/saas/companies', dto).pipe(
      map((res) => res.data),
    );
  }

  updateCompanyStatus(id: string, status: 'ACTIVO' | 'SUSPENDIDO'): Observable<Company> {
    return this.api.patch<ApiResponse<Company>>(`/saas/companies/${id}/status`, { status }).pipe(
      map((res) => res.data),
    );
  }
}
