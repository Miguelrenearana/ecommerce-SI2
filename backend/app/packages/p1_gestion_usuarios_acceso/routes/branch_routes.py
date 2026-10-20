from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.auth.dependencies import require_roles, get_current_branch_id
from app.core.database import get_db
from app.packages.p1_gestion_usuarios_acceso.models.user import User
from app.packages.p1_gestion_usuarios_acceso.schemas.branch_schema import BranchCreate, BranchRead, BranchUpdate, BranchActiveUpdate
from app.schemas.enums import RolEnum
from app.packages.p1_gestion_usuarios_acceso.services.branch_service import create_branch, get_branches, update_branch, delete_branch, set_branch_active
from app.utils.response import response


router = APIRouter(prefix="/branches", tags=["Branches"])


@router.get("/")
async def list_branches_route(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles(RolEnum.administrador)),
    current_branch_id: UUID | None = Depends(get_current_branch_id),
):
    branches = get_branches(db, current_branch_id)
    branches_data = [BranchRead.model_validate(branch).model_dump() for branch in branches]
    return response(
        status_code=status.HTTP_200_OK,
        message="Sucursales obtenidas exitosamente",
        data=branches_data,
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_branch_route(
    branch: BranchCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles(RolEnum.administrador)),
    current_branch_id: UUID | None = Depends(get_current_branch_id),
):
    if current_branch_id is not None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No puedes crear sucursales desde una sucursal asignada")

    try:
        db_branch = create_branch(db, branch)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    branch_data = BranchRead.model_validate(db_branch).model_dump()
    return response(
        status_code=status.HTTP_201_CREATED,
        message="Sucursal creada exitosamente",
        data=branch_data,
    )


@router.put("/{branch_id}")
async def update_branch_route(
    branch_id: UUID,
    branch_data: BranchUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles(RolEnum.administrador)),
    current_branch_id: UUID | None = Depends(get_current_branch_id),
):
    if current_branch_id is not None and current_branch_id != branch_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para modificar esta sucursal")

    updated_branch = update_branch(db, branch_id, branch_data)
    if not updated_branch:
        raise HTTPException(status_code=404, detail=f"Sucursal con id {branch_id} no encontrada")

    return response(
        status_code=status.HTTP_200_OK,
        message="Sucursal actualizada exitosamente",
        data=BranchRead.model_validate(updated_branch).model_dump(),
    )


@router.patch("/{branch_id}/active")
async def update_branch_active_route(
    branch_id: UUID,
    active_data: BranchActiveUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles(RolEnum.administrador)),
    current_branch_id: UUID | None = Depends(get_current_branch_id),
):
    if current_branch_id is not None and current_branch_id != branch_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para modificar esta sucursal")

    updated_branch = set_branch_active(db, branch_id, active_data.is_active)
    if not updated_branch:
        raise HTTPException(status_code=404, detail=f"Sucursal con id {branch_id} no encontrada")

    return response(
        status_code=status.HTTP_200_OK,
        message="Estado de sucursal actualizado exitosamente",
        data=BranchRead.model_validate(updated_branch).model_dump(),
    )


@router.delete("/{branch_id}")
async def delete_branch_route(
    branch_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles(RolEnum.administrador)),
    current_branch_id: UUID | None = Depends(get_current_branch_id),
):
    if current_branch_id is not None and current_branch_id != branch_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para eliminar esta sucursal")

    try:
        deleted = delete_branch(db, branch_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    if not deleted:
        raise HTTPException(status_code=404, detail=f"Sucursal con id {branch_id} no encontrada")

    return response(
        status_code=status.HTTP_200_OK,
        message="Sucursal eliminada exitosamente",
        data={"id": str(branch_id)},
    )
