from enum import Enum


class ProjectRole(str, Enum):
    """
    Roles disponibles dentro de un proyecto.
    """

    OWNER = "OWNER"
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"
    VIEWER = "VIEWER"