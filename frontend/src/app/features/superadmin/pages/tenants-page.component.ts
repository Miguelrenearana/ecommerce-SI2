import { CommonModule } from '@angular/common';
import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { toast } from '@spartan-ng/brain/sonner';

import { CompanyService } from '../../../core/services/company.service';
import { Company } from '../../../core/models/company.model';
import { TenantFormModalComponent } from '../components/tenant-form-modal.component';

@Component({
  selector: 'app-tenants-page',
  standalone: true,
  imports: [CommonModule, FormsModule, TenantFormModalComponent],
  template: `
    <div class="space-y-8 p-6 lg:p-10 max-w-7xl mx-auto">
      
      <!-- HEADER CON RESUMEN EJECUTIVO -->
      <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <span class="text-xs font-semibold uppercase tracking-wider text-slate-500">
            Portal Master SaaS • CU01
          </span>
          <h1 class="text-2xl lg:text-3xl font-bold tracking-tight text-slate-900 mt-1">
            Empresas Contratantes
          </h1>
          <p class="text-sm text-slate-500 mt-1">
            Gestión centralizada de inquilinos (*tenants*), planes de suscripción y aislamiento lógico.
          </p>
        </div>

        <button
          type="button"
          (click)="isModalOpen.set(true)"
          class="inline-flex items-center justify-center gap-2 rounded-lg bg-slate-900 px-4 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-slate-800 transition-colors"
        >
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          <span>Registrar Empresa</span>
        </button>
      </div>

      <!-- TARJETAS DE MÉTRICAS (KPIs) -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div class="rounded-xl border border-slate-200 bg-white p-5 shadow-xs">
          <p class="text-xs font-medium text-slate-500">Total Empresas</p>
          <p class="text-2xl font-bold text-slate-900 mt-2">{{ totalTenants() }}</p>
          <p class="text-[11px] text-slate-400 mt-1">Tenants registrados en la plataforma</p>
        </div>

        <div class="rounded-xl border border-slate-200 bg-white p-5 shadow-xs">
          <div class="flex items-center justify-between">
            <p class="text-xs font-medium text-slate-500">Operativas</p>
            <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
          </div>
          <p class="text-2xl font-bold text-emerald-700 mt-2">{{ activeTenants() }}</p>
          <p class="text-[11px] text-slate-400 mt-1">Empresas con suscripción y acceso activo</p>
        </div>

        <div class="rounded-xl border border-slate-200 bg-white p-5 shadow-xs">
          <div class="flex items-center justify-between">
            <p class="text-xs font-medium text-slate-500">Suspendidas</p>
            <span class="w-2 h-2 rounded-full bg-rose-500"></span>
          </div>
          <p class="text-2xl font-bold text-rose-700 mt-2">{{ suspendedTenants() }}</p>
          <p class="text-[11px] text-slate-400 mt-1">Bloqueadas por mora o administración</p>
        </div>
      </div>

      <!-- BARRA DE BÚSQUEDA Y FILTROS -->
      <div class="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
        <!-- Input de búsqueda -->
        <div class="relative flex-1 max-w-md">
          <svg class="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            type="text"
            [ngModel]="searchQuery()"
            (ngModelChange)="searchQuery.set($event)"
            placeholder="Buscar por nombre, NIT o subdominio..."
            class="w-full rounded-lg border border-slate-200 bg-white pl-10 pr-4 py-2 text-sm text-slate-800 placeholder-slate-400 focus:border-slate-800 focus:outline-none focus:ring-1 focus:ring-slate-800 shadow-xs"
          />
        </div>

        <!-- Filtros de estado -->
        <div class="inline-flex rounded-lg border border-slate-200 bg-slate-50 p-1 text-xs font-medium">
          <button
            type="button"
            (click)="statusFilter.set('all')"
            class="rounded-md px-3 py-1.5 transition-colors"
            [ngClass]="statusFilter() === 'all' ? 'bg-white text-slate-900 shadow-xs font-semibold' : 'text-slate-600 hover:text-slate-900'"
          >
            Todas ({{ totalTenants() }})
          </button>
          <button
            type="button"
            (click)="statusFilter.set('ACTIVO')"
            class="rounded-md px-3 py-1.5 transition-colors"
            [ngClass]="statusFilter() === 'ACTIVO' ? 'bg-white text-emerald-800 shadow-xs font-semibold' : 'text-slate-600 hover:text-slate-900'"
          >
            Activas
          </button>
          <button
            type="button"
            (click)="statusFilter.set('SUSPENDIDO')"
            class="rounded-md px-3 py-1.5 transition-colors"
            [ngClass]="statusFilter() === 'SUSPENDIDO' ? 'bg-white text-rose-800 shadow-xs font-semibold' : 'text-slate-600 hover:text-slate-900'"
          >
            Suspendidas
          </button>
        </div>
      </div>

      <!-- TABLA DE TENANTS -->
      <div class="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-xs">
        @if (loading()) {
          <div class="flex flex-col items-center justify-center p-12 text-slate-400">
            <span class="inline-block w-6 h-6 border-2 border-slate-300 border-t-slate-800 rounded-full animate-spin"></span>
            <p class="text-sm mt-3">Cargando empresas registradas...</p>
          </div>
        } @else if (filteredCompanies().length === 0) {
          <div class="flex flex-col items-center justify-center p-12 text-center">
            <div class="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center text-slate-400 mb-3">
              <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
            </div>
            <h3 class="text-sm font-semibold text-slate-900">No se encontraron empresas</h3>
            <p class="text-xs text-slate-500 mt-1 max-w-sm">
              @if (searchQuery()) {
                No hay resultados coincidentes con "{{ searchQuery() }}".
              } @else {
                Aún no has registrado empresas clientes. Pulsa "Registrar Empresa" para dar de alta la primera.
              }
            </p>
          </div>
        } @else {
          <div class="overflow-x-auto">
            <table class="w-full text-left text-sm text-slate-700">
              <thead class="border-b border-slate-200 bg-slate-50/75 text-xs font-semibold text-slate-500">
                <tr>
                  <th scope="col" class="py-3.5 pl-6 pr-3">Empresa / Razón Social</th>
                  <th scope="col" class="px-3 py-3.5">Subdominio</th>
                  <th scope="col" class="px-3 py-3.5">NIT / RUT</th>
                  <th scope="col" class="px-3 py-3.5">Contacto</th>
                  <th scope="col" class="px-3 py-3.5">Estado</th>
                  <th scope="col" class="py-3.5 pl-3 pr-6 text-right">Acciones</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                @for (company of filteredCompanies(); track company.id) {
                  <tr class="hover:bg-slate-50/50 transition-colors">
                    
                    <!-- Nombre y Razón Social -->
                    <td class="py-4 pl-6 pr-3">
                      <div class="font-semibold text-slate-900">{{ company.name }}</div>
                      <div class="text-xs text-slate-400">{{ company.business_name }}</div>
                    </td>

                    <!-- Subdominio con preview -->
                    <td class="px-3 py-4">
                      <span class="inline-flex items-center gap-1 font-mono text-xs font-medium px-2 py-0.5 rounded bg-slate-100 text-slate-700">
                        {{ company.subdomain }}
                        <span class="text-slate-400">.fashionstore.app</span>
                      </span>
                    </td>

                    <!-- NIT / RUT -->
                    <td class="px-3 py-4 text-xs font-mono text-slate-600">
                      {{ company.nit_rut }}
                    </td>

                    <!-- Contacto -->
                    <td class="px-3 py-4 text-xs text-slate-500">
                      <div>{{ company.email || '—' }}</div>
                      <div class="text-[11px] text-slate-400">{{ company.phone || '' }}</div>
                    </td>

                    <!-- Estado -->
                    <td class="px-3 py-4">
                      @if (company.status === 'ACTIVO') {
                        <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-200/60">
                          <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                          Activo
                        </span>
                      } @else {
                        <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium bg-rose-50 text-rose-700 border border-rose-200/60">
                          <span class="w-1.5 h-1.5 rounded-full bg-rose-500"></span>
                          Suspendido
                        </span>
                      }
                    </td>

                    <!-- Acciones -->
                    <td class="py-4 pl-3 pr-6 text-right">
                      @if (company.status === 'ACTIVO') {
                        <button
                          type="button"
                          [disabled]="togglingId() === company.id"
                          (click)="toggleStatus(company, 'SUSPENDIDO')"
                          class="text-xs font-medium text-rose-600 hover:text-rose-800 disabled:opacity-50 transition-colors"
                        >
                          @if (togglingId() === company.id) {
                            Actualizando...
                          } @else {
                            Suspender
                          }
                        </button>
                      } @else {
                        <button
                          type="button"
                          [disabled]="togglingId() === company.id"
                          (click)="toggleStatus(company, 'ACTIVO')"
                          class="text-xs font-medium text-emerald-600 hover:text-emerald-800 disabled:opacity-50 transition-colors"
                        >
                          @if (togglingId() === company.id) {
                            Actualizando...
                          } @else {
                            Reactivar
                          }
                        </button>
                      }
                    </td>
                  </tr>
                }
              </tbody>
            </table>
          </div>
        }
      </div>

      <!-- MODAL DE REGISTRO REACTIVO -->
      <app-tenant-form-modal
        [isOpen]="isModalOpen()"
        (close)="isModalOpen.set(false)"
        (created)="onCompanyCreated($event)"
      />

    </div>
  `,
})
export class TenantsPageComponent implements OnInit {
  private readonly companyService = inject(CompanyService);

  protected readonly companies = signal<Company[]>([]);
  protected readonly loading = signal<boolean>(true);
  protected readonly searchQuery = signal<string>('');
  protected readonly statusFilter = signal<string>('all');
  protected readonly isModalOpen = signal<boolean>(false);
  protected readonly togglingId = signal<string | null>(null);

  protected readonly totalTenants = computed(() => this.companies().length);
  protected readonly activeTenants = computed(
    () => this.companies().filter((c) => c.status === 'ACTIVO').length,
  );
  protected readonly suspendedTenants = computed(
    () => this.companies().filter((c) => c.status === 'SUSPENDIDO').length,
  );

  protected readonly filteredCompanies = computed(() => {
    const query = this.searchQuery().toLowerCase().trim();
    const status = this.statusFilter();

    return this.companies().filter((company) => {
      const matchesStatus = status === 'all' || company.status === status;
      if (!matchesStatus) return false;

      if (!query) return true;
      return (
        company.name.toLowerCase().includes(query) ||
        company.business_name.toLowerCase().includes(query) ||
        company.nit_rut.toLowerCase().includes(query) ||
        company.subdomain.toLowerCase().includes(query)
      );
    });
  });

  ngOnInit(): void {
    this.loadCompanies();
  }

  loadCompanies(): void {
    this.loading.set(true);
    this.companyService.getCompanies().subscribe({
      next: (list) => {
        this.companies.set(list);
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
        toast.error('No se pudieron cargar las empresas registradas.');
      },
    });
  }

  toggleStatus(company: Company, targetStatus: 'ACTIVO' | 'SUSPENDIDO'): void {
    this.togglingId.set(company.id);
    this.companyService.updateCompanyStatus(company.id, targetStatus).subscribe({
      next: (updated) => {
        this.togglingId.set(null);
        this.companies.update((prev) =>
          prev.map((c) => (c.id === updated.id ? { ...c, status: updated.status } : c)),
        );
        toast.success(`Empresa '${updated.name}' ahora está ${updated.status}.`);
      },
      error: (err) => {
        this.togglingId.set(null);
        const detail = err.error?.detail || 'Error al cambiar estado de la empresa.';
        toast.error(detail);
      },
    });
  }

  onCompanyCreated(newCompany: Company): void {
    this.companies.update((prev) => [newCompany, ...prev]);
  }
}
