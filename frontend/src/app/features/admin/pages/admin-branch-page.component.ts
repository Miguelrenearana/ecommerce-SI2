import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { firstValueFrom } from 'rxjs';

import { toast } from '@spartan-ng/brain/sonner';

import { AdminActionMenuComponent } from '../components/admin-action-menu.component';
import { HlmButton } from '../../../components/button/src';
import { HlmCardImports } from '../../../components/card/src';
import { HlmFieldImports } from '../../../components/field/src';
import { HlmInput } from '../../../components/input/src';
import { HlmSelectImports } from '../../../components/select/src';
import { AdminBranch, BranchQuota } from '../models/admin-branch.model';
import { AdminBranchService } from '../services/admin-branch.service';
import { getErrorMessage } from '../../../core/utils/http-error.util';
import { requestWithToast } from '../../../core/utils/request-toast.util';

@Component({
  selector: 'app-admin-branch-page',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    HlmButton,
    HlmInput,
    AdminActionMenuComponent,
    ...HlmCardImports,
    ...HlmFieldImports,
    ...HlmSelectImports,
  ],
  templateUrl: './admin-branch-page.component.html',
})
export class AdminBranchPageComponent {
  private readonly fb = inject(FormBuilder);
  private readonly api = inject(AdminBranchService);

  protected readonly branches = signal<AdminBranch[]>([]);
  protected readonly quota = signal<BranchQuota | null>(null);
  protected readonly loading = signal(false);
  protected readonly modalOpen = signal(false);
  protected readonly modalMode = signal<'create' | 'edit'>('create');
  protected readonly editingBranchId = signal<string | null>(null);
  protected readonly deleteConfirmOpen = signal(false);
  protected readonly deletingBranch = signal<AdminBranch | null>(null);
  protected readonly openMenuId = signal<string | null>(null);

  protected readonly defaultSelectLabel = (value: boolean | null | undefined): string => (value ? 'Sí' : 'No');

  protected readonly activeSelectLabel = (value: boolean | null | undefined): string => (value ? 'Activa' : 'Inactiva');

  protected readonly form = this.fb.nonNullable.group({
    name: ['', [Validators.required]],
    city: ['', [Validators.required]],
    address: ['', [Validators.required]],
    phone: [''],
    opening_hours: ['09:00 - 20:00'],
    latitude: [-17.7833, [Validators.required]],
    longitude: [-63.1821, [Validators.required]],
    is_default: [false],
    is_active: [true],
  });

  constructor() {
    void this.loadData();
  }

  protected openModal(): void {
    this.closeMenu();
    this.modalMode.set('create');
    this.editingBranchId.set(null);
    this.form.reset({
      name: '',
      city: '',
      address: '',
      phone: '',
      opening_hours: '09:00 - 20:00',
      latitude: -17.7833,
      longitude: -63.1821,
      is_default: false,
      is_active: true,
    });
    this.modalOpen.set(true);
  }

  protected editBranch(branch: AdminBranch): void {
    this.closeMenu();
    this.modalMode.set('edit');
    this.editingBranchId.set(branch.id);
    this.form.reset({
      name: branch.name,
      city: branch.city,
      address: branch.address || '',
      phone: branch.phone || '',
      opening_hours: branch.opening_hours || '09:00 - 20:00',
      latitude: Number(branch.latitude) || -17.7833,
      longitude: Number(branch.longitude) || -63.1821,
      is_default: branch.is_default,
      is_active: branch.is_active,
    });
    this.modalOpen.set(true);
  }

  protected closeModal(): void {
    this.modalOpen.set(false);
    this.closeMenu();
  }

  protected closeMenu(): void {
    this.openMenuId.set(null);
  }

  protected toggleMenu(branchId: string): void {
    this.openMenuId.set(this.openMenuId() === branchId ? null : branchId);
  }

  protected async toggleActive(branch: AdminBranch): Promise<void> {
    this.closeMenu();
    try {
      await requestWithToast(
        this.api.updateBranchActive(branch.id, { is_active: !branch.is_active }),
        {
          loading: 'Actualizando estado...',
          success: `Sucursal ${!branch.is_active ? 'activada' : 'desactivada'} correctamente.`,
          error: 'No se pudo actualizar el estado de la sucursal.',
        },
      );
      await this.loadData();
    } catch {
      // El toast de error ya se mostró con requestWithToast
    }
  }

  protected askDelete(branch: AdminBranch): void {
    this.closeMenu();
    this.deletingBranch.set(branch);
    this.deleteConfirmOpen.set(true);
  }

  protected cancelDelete(): void {
    this.deleteConfirmOpen.set(false);
    this.deletingBranch.set(null);
  }

  protected async confirmDelete(): Promise<void> {
    const branch = this.deletingBranch();
    if (!branch) return;

    try {
      await requestWithToast(
        this.api.deleteBranch(branch.id),
        { loading: 'Eliminando sucursal...', success: 'Sucursal eliminada correctamente.', error: 'No se pudo eliminar la sucursal.' },
      );
      await this.loadData();
      this.cancelDelete();
    } catch {
      // El toast de error ya se mostró con requestWithToast
    }
  }

  protected async submit(): Promise<void> {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.loading.set(true);
    try {
      const payload = this.form.getRawValue();
      if (this.modalMode() === 'edit' && this.editingBranchId()) {
        await requestWithToast(
          this.api.updateBranch(this.editingBranchId()!, payload),
          { loading: 'Guardando sucursal...', success: 'Sucursal actualizada correctamente.', error: 'No se pudo guardar la sucursal.' },
        );
      } else {
        await requestWithToast(
          this.api.createBranch(payload),
          { loading: 'Guardando sucursal...', success: 'Sucursal creada correctamente.', error: 'No se pudo guardar la sucursal.' },
        );
      }
      this.form.reset();
      await this.loadData();
      this.closeModal();
    } catch {
      // El toast de error ya se mostró con requestWithToast
    } finally {
      this.loading.set(false);
    }
  }

  protected async loadData(): Promise<void> {
    try {
      const [branchesRes, quotaRes] = await Promise.all([
        firstValueFrom(this.api.listBranches()),
        firstValueFrom(this.api.getBranchQuota()).catch(() => null),
      ]);
      this.branches.set(branchesRes.data ?? []);
      if (quotaRes?.data) {
        this.quota.set(quotaRes.data);
      }
    } catch (error) {
      toast.error(getErrorMessage(error, 'No se pudieron cargar los datos de las sucursales.'));
    }
  }
}
