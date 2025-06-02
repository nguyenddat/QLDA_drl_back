import enum

class AuthProviderEnum(str, enum.Enum):
    local = 'local'
    google = 'google'

class UserRoleEnum(str, enum.Enum):
    admin = "admin"
    student = "student"
    class_leader = "class_leader"
    teacher = "teacher"
