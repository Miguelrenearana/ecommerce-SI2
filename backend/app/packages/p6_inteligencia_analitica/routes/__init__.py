from app.packages.p6_inteligencia_analitica.routes.chatbot_routes import router as chatbot_router
from app.packages.p6_inteligencia_analitica.routes.dashboard_routes import router as dashboard_router
from app.packages.p6_inteligencia_analitica.routes.notification_routes import router as notification_router
from app.packages.p6_inteligencia_analitica.routes.recommendation_routes import router as recommendation_router
from app.packages.p6_inteligencia_analitica.routes.report_routes import router as report_router

__all__ = [
    "chatbot_router",
    "dashboard_router",
    "notification_router",
    "recommendation_router",
    "report_router",
]
