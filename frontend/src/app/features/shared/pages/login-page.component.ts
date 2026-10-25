import { CommonModule } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';

import { toast } from '@spartan-ng/brain/sonner';

import { AmbitoAcceso } from '../models/auth.model';
import { SessionService } from '../services/session.service';
import { getDefaultRouteForRole } from '../../../core/utils/role-route.util';
import { HlmCardImports } from '../../../components/card/src';
import { HlmFieldImports } from '../../../components/field/src';
import { HlmInput } from '../../../components/input/src';

@Component({
  selector: 'app-login-page',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterLink,
    HlmInput,
    ...HlmCardImports,
    ...HlmFieldImports,
  ],
  templateUrl: './login-page.component.html',
})
export class LoginPageComponent {
  private readonly fb = inject(FormBuilder);
  private readonly session = inject(SessionService);
  private readonly router = inject(Router);

  protected readonly loading = signal(false);
  protected readonly activeActor = signal<AmbitoAcceso>('clientes');
  protected readonly showPassword = signal(false);

  protected readonly form = this.fb.nonNullable.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required]],
  });

  protected selectActor(actor: AmbitoAcceso): void {
    this.activeActor.set(actor);
  }

  protected togglePasswordVisibility(): void {
    this.showPassword.update((visible) => !visible);
  }

  protected normalizeEmailInput(event: Event): void {
    const input = event.target as HTMLInputElement | null;
    if (!input) return;

    const value = input.value.trim().toLowerCase();
    this.form.controls.email.setValue(value, { emitEvent: false });
  }

  protected async submit(): Promise<void> {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.loading.set(true);
    try {
      const { email, password } = this.form.getRawValue();
      const request = this.session.login(email.trim().toLowerCase(), password, null);
      toast.promise(request, {
        loading: 'Iniciando sesión...',
        success: 'Sesión iniciada correctamente.',
        error: () => 'No se pudo iniciar sesión. Verifica tus credenciales.',
      });
      await request;
      await this.router.navigateByUrl(getDefaultRouteForRole(this.session.user()?.rol));
    } catch {
      // El toast de error ya se mostró con toast.promise
    } finally {
      this.loading.set(false);
    }
  }
}
