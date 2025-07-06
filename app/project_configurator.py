import dataclasses
from typing import Optional, Dict

@dataclasses.dataclass
class DattaAbleFlaskProject:
    """
    Концептуальный класс, представляющий настроенный экземпляр проекта Datta Able Flask.
    
    Его конструктор (__init__ и __post_init__) конфигурирует проект
    на основе выбранного уровня (Free, PRO, Custom Development),
    имитируя наборы функций, описанные в README.md.
    Этот класс используется для моделирования бизнес-логики, а не для
    прямой генерации HTML-файлов.
    """
    project_name: str
    tier: str = "Free"  # По умолчанию Free tier

    # Основные функции (общие для всех уровней, на основе README.md)
    up_to_date_dependencies: bool = True
    best_practices: bool = True
    db_tools: bool = True  # ORM, Flask Migrate
    session_based_authentication: bool = True
    docker_support: bool = True
    user_roles: bool = True  # Базовые роли пользователей

    # Функции уровня PRO (инициализируются как False, включаются в зависимости от tier)
    pro_support_email_discord: bool = False
    deployment_assistance: bool = False
    premium_bootstrap5_design: bool = False
    ui_ux_for_github: bool = False
    extended_user_roles: bool = False
    firebase_rest_access: bool = False
    delivery_warranty_30_days: bool = False

    # Специфическая функция для Custom Development
    custom_requirements_fulfilled: bool = False  # Представляет индивидуальные функции

    def __post_init__(self):
        """
        Этот метод вызывается после __init__ и используется для выполнения
        пост-инициализационной конфигурации на основе выбранного уровня.
        """
        self.tier = self.tier.capitalize()  # Нормализация имени уровня

        if self.tier == "Pro": # Changed from "PRO" to "Pro" to match .capitalize()
            self._set_pro_features(enable=True)
        elif self.tier == "Custom development": # Changed for consistency
            self._set_pro_features(enable=True)
            self.custom_requirements_fulfilled = True
        elif self.tier == "Free":
            # Функции Free tier по умолчанию True, PRO/Custom specific по умолчанию False
            pass
        else:
            raise ValueError(
                f"Неверный уровень: '{self.tier}'. Должен быть 'Free', 'Pro' или 'Custom Development'."
            )

        print(f"Концептуальный проект '{self.project_name}' создан с конфигурацией уровня '{self.tier}'.")

    def _set_pro_features(self, enable: bool):
        """
        Вспомогательный метод для включения или отключения функций уровня PRO.
        """
        self.pro_support_email_discord = enable
        self.deployment_assistance = enable
        self.premium_bootstrap5_design = enable
        self.ui_ux_for_github = enable
        self.extended_user_roles = enable
        self.firebase_rest_access = enable
        self.delivery_warranty_30_days = enable

    def get_features_summary(self) -> Dict[str, bool]:
        """Возвращает словарь всех функций и их статуса."""
        return {
            "up_to_date_dependencies": self.up_to_date_dependencies,
            "best_practices": self.best_practices,
            "db_tools": self.db_tools,
            "session_based_authentication": self.session_based_authentication,
            "docker_support": self.docker_support,
            "user_roles": self.user_roles,
            "pro_support_email_discord": self.pro_support_email_discord,
            "deployment_assistance": self.deployment_assistance,
            "premium_bootstrap5_design": self.premium_bootstrap5_design,
            "ui_ux_for_github": self.ui_ux_for_github,
            "extended_user_roles": self.extended_user_roles,
            "firebase_rest_access": self.firebase_rest_access,
            "delivery_warranty_30_days": self.delivery_warranty_30_days,
            "custom_requirements_fulfilled": self.custom_requirements_fulfilled,
        }

    def display_configuration(self):
        """
        Выводит текущую конфигурацию экземпляра проекта Flask.
        """
        print("\n--- Сводка конфигурации проекта ---")
        print(f"Название проекта: {self.project_name}")
        print(f"Выбранный уровень: {self.tier}")
        print("\n--- Включенные функции ---")

        features_map = {
            "Актуальные зависимости": self.up_to_date_dependencies,
            "Лучшие практики": self.best_practices,
            "Инструменты БД (ORM, Flask Migrate)": self.db_tools,
            "Аутентификация на основе сессий": self.session_based_authentication,
            "Поддержка Docker": self.docker_support,
            "Базовые роли пользователей": self.user_roles,
            "PRO Поддержка (Email & Discord)": self.pro_support_email_discord,
            "Помощь с развертыванием": self.deployment_assistance,
            "Премиум дизайн Bootstrap 5": self.premium_bootstrap5_design,
            "UI/UX для GitHub": self.ui_ux_for_github,
            "Расширенные роли пользователей": self.extended_user_roles,
            "Доступ к Firebase REST": self.firebase_rest_access,
            "Гарантия доставки 30 дней": self.delivery_warranty_30_days,
            "Выполнены пользовательские требования": self.custom_requirements_fulfilled,
        }

        for feature, enabled in features_map.items():
            print(f"- {feature}: {'✅ Включено' if enabled else '❌ Отключено'}")
        print("-------------------------------------\n") 