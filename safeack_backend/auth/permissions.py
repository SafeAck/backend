'''Permissions module'''

from enum import Enum


class Role(Enum):
    '''User Roles'''

    USER = "user"
    STAFF = "staff"
    SUPERUSER = "superuser"


class MePerm(Enum):
    '''User Permissions'''

    READ = "me:read"
    WRITE = "me:write"
    READ_RESULTS = "me:read_results"
    WRITE_RESULTS = "me:write_results"


class StaffPerm(Enum):
    '''Staff User Permissions'''

    RESTRICTED_READ = "staff:restricted_read"


user_permissions: dict[str, str] = {
    MePerm.READ.name: "read information about current user",
    MePerm.WRITE.name: "write information about current user",
    MePerm.READ_RESULTS.name: "read information about current user's scan results",
    MePerm.WRITE_RESULTS.name: "write information about current user's scan results",
}


staff_permissions: dict[str, str] = {
    StaffPerm.RESTRICTED_READ.name: "read all users scan results",
}

# make sure user and staff permission have unique keys
superuser_permissions: dict[str, str] = {
    **user_permissions,
    **staff_permissions,
}

role_based_scopes: dict[str, dict[str, str]] = {
    Role.USER.name: user_permissions,
    Role.STAFF.name: staff_permissions,
    Role.SUPERUSER.name: superuser_permissions,
}
