import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { toast } from '@spartan-ng/brain/sonner';

import { Company, Plan, Subscription } from '../../../core/models/company.model';
import { CompanyService } from '../../../core/services/company.service';

@Component({
  selector: 'app-subscription-modal',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    @if (isOpen && company) {
      <div
        class="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 overflow-y-auto"
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        (keydown.escape)="onClose()"
      >
        <!-- BACKDROP -->
        <div
          class="fixed inset-0 bg-slate-900/60 backdrop-blur-xs transition-opacity"
          (click)="onClose()"
        ></div>

        <!-- MODAL CARD -->
        <div
          class="relative w-full max-w-2xl bg-white rounded-2xl shadow-2xl border border-slate-200 overflow-hidden z-10 transition-all text-slate-800"
          (click)="$event.stopPropagation()"
        >
          <!-- HEADER -->
          <div class="px-6 py-5 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
            <div>
              <span class="text-[11px] font-bold uppercase tracking-wider text-slate-500">
                CU02 • Gestión de Suscripciones y Límites
              </span>
              <h2 id="modal-title" class="text-xl font-bold text-slate-900 mt-0.5">
                Plan de Suscripción: {{ company.name }}
              </h2>
              <p class="text-xs text-slate-500">
                Subdominio: <code class="font-mono font-semibold text-slate-700">{{ company.subdomain }}.fashionstore.app</code>
              </p>
            </div>

            <button
              type="button"
              (click)="onClose()"
              class="rounded-lg p-1.5 text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors"
            >
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- BODY -->
          <div class="p-6 space-y-6">

            <!-- ESTADO ACTUAL -->
            <div class="rounded-xl border border-slate-200 bg-slate-50 p-4">
              <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div>
                  <p class="text-xs font-semibold text-slate-500 uppercase tracking-wide">Plan Actual</p>
                  <p class="text-lg font-bold text-slate-900 mt-0.5">
                    @if (loadingSubscription()) {
                      <span class="text-sm font-normal text-slate-400">Consultando suscripción...</span>
                    } @else if (currentSubscription()?.plan) {
                      {{ currentSubscription()?.plan?.name }}
                      <span class="text-xs font-normal text-slate-500">
                        (\${{ currentSubscription()?.plan?.price_monthly }}/mes)
                      </span>
                    } @else {
                      <span class="text-sm text-amber-600 font-medium">Sin suscripción activa asignada</span>
                    }
                  </p>
                </div>

                @if (currentSubscription()?.plan) {
                  <div class="flex items-center gap-3 text-xs">
                    <div class="px-2.5 py-1 rounded-md bg-white border border-slate-200">
                      <span class="text-slate-500">Cuota Sucursales:</span>
                      <strong class="text-slate-900 ml-1">Máx. {{ currentSubscription()?.plan?.max_branches }}</strong>
                    </div>
                    <div class="px-2.5 py-1 rounded-md bg-white border border-slate-200">
                      <span class="text-slate-500">Inteligencia Artificial:</span>
                      <strong class="ml-1" [ngClass]="currentSubscription()?.plan?.has_ai_access ? 'text-emerald-700' : 'text-slate-400'">
                        {{ currentSubscription()?.plan?.has_ai_access ? 'Habilitada' : 'No incluida' }}
                      </strong>
                    </div>
                  </div>
                }
              </div>
            </div>

            <!-- SELECTOR DE NUEVO PLAN -->
            <div>
              <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
                Selecciona el Plan Destino
              </label>

              @if (loadingPlans()) {
                <div class="py-6 text-center text-xs text-slate-400">
                  Cargando planes comerciales...
                </div>
              } @else {
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  @for (plan of plans(); track plan.id) {
                    <div
                      (click)="selectedPlanId.set(plan.id)"
                      class="relative rounded-xl border-2 p-4 cursor-pointer transition-all"
                      [ngClass]="{
                        'border-slate-900 bg-slate-50/70 shadow-xs': selectedPlanId() === plan.id,
                        'border-slate-200 bg-white hover:border-slate-300': selectedPlanId() !== plan.id
                      }"
                    >
                      <div class="flex items-start justify-between">
                        <div>
                          <span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-bold"
                            [ngClass]="plan.code === 'pro' ? 'bg-amber-100 text-amber-800' : 'bg-slate-200 text-slate-700'">
                            {{ plan.name }}
                          </span>
                          <div class="text-xl font-bold text-slate-900 mt-2">
                            \${{ plan.price_monthly }}
                            <span class="text-xs font-normal text-slate-500">/mes</span>
                          </div>
                        </div>

                        <input
                          type="radio"
                          name="target_plan"
                          [value]="plan.id"
                          [checked]="selectedPlanId() === plan.id"
                          class="mt-1 h-4 w-4 text-slate-900 focus:ring-slate-900 border-slate-300"
                        />
                      </div>

                      <p class="text-xs text-slate-500 mt-2 line-clamp-2">
                        {{ plan.description || 'Configuración comercial oficial' }}
                      </p>

                      <ul class="text-xs space-y-1.5 mt-3 pt-3 border-t border-slate-100 text-slate-600">
                        <li class="flex items-center gap-1.5">
                          <svg class="w-3.5 h-3.5 text-emerald-600 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                          </svg>
                          <span>Hasta <strong>{{ plan.max_branches }} sucursales</strong> físicas</span>
                        </li>
                        <li class="flex items-center gap-1.5">
                          @if (plan.has_ai_access) {
                            <svg class="w-3.5 h-3.5 text-emerald-600 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                            </svg>
                            <span class="font-medium text-emerald-800">IA Generativa (Voz) y ML</span>
                          } @else {
                            <svg class="w-3.5 h-3.5 text-slate-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                            </svg>
                            <span class="text-slate-400">Sin Inteligencia Artificial</span>
                          }
                        </li>
                      </ul>
                    </div>
                  }
                </div>
              }
            </div>

            <!-- MENSAJE DE ADVERTENCIA / ERROR DE DOWNGRADE -->
            @if (errorMessage()) {
              <div class="rounded-xl border border-rose-200 bg-rose-50 p-3.5 text-xs text-rose-800 flex items-start gap-2.5">
                <svg class="w-4 h-4 text-rose-600 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <div class="flex-1">
                  <p class="font-bold">Restricción de Negocio (Regla de Suscripción):</p>
                  <p class="mt-0.5">{{ errorMessage() }}</p>
                </div>
              </div>
            }

          </div>

          <!-- FOOTER -->
          <div class="px-6 py-4 bg-slate-50/80 border-t border-slate-100 flex items-center justify-end gap-3">
            <button
              type="button"
              (click)="onClose()"
              class="px-4 py-2 text-xs font-semibold text-slate-600 hover:text-slate-900 rounded-lg transition-colors"
            >
              Cancelar
            </button>
            <button
              type="button"
              (click)="onSubmit()"
              [disabled]="saving() || !selectedPlanId() || selectedPlanId() === currentSubscription()?.plan_id"
              class="px-5 py-2 text-xs font-semibold text-white bg-slate-900 hover:bg-slate-800 rounded-lg shadow-sm disabled:opacity-50 disabled:cursor-not-allowed transition-colors inline-flex items-center gap-1.5"
            >
              @if (saving()) {
                <svg class="animate-spin w-3.5 h-3.5 text-white" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
                </svg>
                <span>Actualizando Suscripción...</span>
              } @else {
                <span>Confirmar Cambio de Plan</span>
              }
            </button>
          </div>

        </div>
      </div>
    }
  `,
})
export class SubscriptionModalComponent implements OnChanges {
  private readonly companyService = inject(CompanyService);

  @Input() isOpen = false;
  @Input() company: Company | null = null;
  @Output() close = new EventEmitter<void>();
  @Output() updated = new EventEmitter<Subscription>();

  protected readonly plans = signal<Plan[]>([]);
  protected readonly currentSubscription = signal<Subscription | null>(null);
  protected readonly selectedPlanId = signal<string>('');
  protected readonly loadingPlans = signal<boolean>(false);
  protected readonly loadingSubscription = signal<boolean>(false);
  protected readonly saving = signal<boolean>(false);
  protected readonly errorMessage = signal<string | null>(null);

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['isOpen'] && this.isOpen && this.company) {
      this.resetModal();
      this.loadData();
    }
  }

  private resetModal(): void {
    this.selectedPlanId.set('');
    this.errorMessage.set(null);
    this.currentSubscription.set(null);
  }

  private loadData(): void {
    if (!this.company) return;

    this.loadingPlans.set(true);
    this.companyService.getPlans().subscribe({
      next: (plansList) => {
        this.plans.set(plansList);
        this.loadingPlans.set(false);
      },
      error: () => {
        this.loadingPlans.set(false);
        toast.error('Error al cargar catálogo de planes');
      },
    });

    this.loadingSubscription.set(true);
    this.companyService.getCompanySubscription(this.company.id).subscribe({
      next: (sub) => {
        this.currentSubscription.set(sub);
        if (sub?.plan_id) {
          this.selectedPlanId.set(sub.plan_id);
        }
        this.loadingSubscription.set(false);
      },
      error: () => {
        this.loadingSubscription.set(false);
      },
    });
  }

  protected onClose(): void {
    this.close.emit();
  }

  protected onSubmit(): void {
    if (!this.company || !this.selectedPlanId()) return;

    this.saving.set(true);
    this.errorMessage.set(null);

    this.companyService.assignSubscription(this.company.id, this.selectedPlanId()).subscribe({
      next: (newSub) => {
        this.saving.set(false);
        toast.success(`Plan actualizado exitosamente para ${this.company?.name}`);
        this.updated.emit(newSub);
        this.onClose();
      },
      error: (err) => {
        this.saving.set(false);
        const detail = err?.error?.detail || err?.error?.message || 'Error al actualizar el plan de suscripción';
        this.errorMessage.set(detail);
        toast.error(detail);
      },
    });
  }
}
