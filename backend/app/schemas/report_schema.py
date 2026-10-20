# Legacy compatibility shim - Canonical location: app.packages.p6_inteligencia_analitica.schemas.report_schema
from app.packages.p6_inteligencia_analitica.schemas.report_schema import (
    DEFAULT_INVENTORY_REPORT_COLUMNS,
    DEFAULT_MOVEMENT_REPORT_COLUMNS,
    DEFAULT_SALES_REPORT_COLUMNS,
    InventoryReportRow,
    MovementReportRow,
    NaturalReportInterpretation,
    NaturalReportRequest,
    NaturalReportResponse,
    ReportFormat,
    ReportQuery,
    ReportSummary,
    ReportType,
    SalesReportRow,
)

__all__ = [
    "ReportType",
    "ReportFormat",
    "DEFAULT_SALES_REPORT_COLUMNS",
    "DEFAULT_INVENTORY_REPORT_COLUMNS",
    "DEFAULT_MOVEMENT_REPORT_COLUMNS",
    "ReportQuery",
    "ReportSummary",
    "SalesReportRow",
    "InventoryReportRow",
    "MovementReportRow",
    "NaturalReportRequest",
    "NaturalReportInterpretation",
    "NaturalReportResponse",
]
