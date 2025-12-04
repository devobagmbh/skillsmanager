import logging
import re
from urllib.parse import urlsplit

from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.db.models import Model
from django.http import HttpRequest

from skillsManager.models import Profile, Template, Skill, ProfileMeta, Language, Education, ProfileProjectReference, \
    Project, ProfileProjectSkillReference, ProfileSkillReference, ProfileCertificateReference, CertificateVendor, \
    Certificate, Customer, CustomerLog, ProjectLog

path_map: dict[str, tuple[str, str, str, list[type[Model]]]] = {
    "home": (r"^/(home/)?$", "GET", "none", []),

    "media": (r"^/media/.+$", "GET", "auth", []),

    "admin": (r"^/admin/.*$", "GET", "superuser", []),
    "admin-post": (r"^/admin/.*$", "POST", "superuser", []),

    "change_password": (r"^/change_password/$", "GET", "auth", []),
    "change_password-post": (r"^/change_password/$", "POST", "auth", []),
    "login": (r"^/login/$", "GET", "none", []),
    "login-post": (r"^/login/$", "POST", "none", []),
    "logout": (r"^/logout/$", "GET", "auth", []),
    "logout-post": (r"^/logout/$", "POST", "auth", []),

    "cv-view": (r"^/cv/$", "GET", "view",
                [Profile, Template, ProfileSkillReference, ProfileCertificateReference, Language, Education,
                 ProfileProjectSkillReference, ProfileProjectReference, Customer, Project, Skill, CertificateVendor,
                 Certificate]),
    "cv": (r"^/cv/$", "POST", "view",
           [Profile, Template, ProfileSkillReference, ProfileCertificateReference, Language, Education,
            ProfileProjectSkillReference, ProfileProjectReference, Customer, Project, Skill, CertificateVendor,
            Certificate]),
    "skill_search-view": (r"^/skill_search/$", "GET", "view", [Profile, Skill]),
    "skill_search": (r"^/skill_search/$", "POST", "view", [Profile, Skill]),

    "profiles-list": (r"^/profiles/$", "GET", "view", [Profile, ProfileMeta]),
    "profiles-add": (r"^/profiles/$", "POST", "add", [Profile]),
    "profiles-view": (r"^/profiles/\d+/edit/$", "GET", "view", [Profile, ProfileMeta, Language, Education]),
    "profiles-update": (r"^/profiles/\d+/edit/$", "POST", "change", [Profile, ProfileMeta, Language, Education]),
    "profiles-delete-view": (r"^/profiles/\d+/delete/", "GET", "view", [Profile]),
    "profiles-delete": (r"^/profiles/\d+/delete/", "POST", "delete", [Profile, ProfileMeta]),

    "profiles-work-list": (r"^/profiles/\d+/work/$", "GET", "view", [Profile, ProfileProjectReference, Project]),
    "profiles-work-add": (r"^/profiles/\d+/work/$", "POST", "add", [Profile, ProfileProjectReference, Project]),
    "profiles-work-view": (r"^/profiles/\d+/work/\d+/edit.+$", "GET", "view",
                           [Profile, ProfileProjectReference, Project, ProfileProjectSkillReference,
                            ProfileSkillReference, Skill]),
    "profiles-work-update": (r"^/profiles/\d+/work/\d+/edit.+$", "POST", "change",
                             [Profile, ProfileProjectReference, Project, ProfileProjectSkillReference,
                              ProfileSkillReference, Skill]),
    "profiles-work-delete-view": (r"^/profiles/\d+/work/\d+/delete.+", "GET", "view",
                                  [ProfileProjectReference, ProfileProjectSkillReference]),
    "profiles-work-delete": (r"^/profiles/\d+/work/\d+/delete.+", "POST", "delete",
                             [Profile, ProfileProjectReference, Project, ProfileProjectSkillReference,
                              ProfileSkillReference, Skill]),

    "profiles-certificates-list": (r"^/profiles/\d+/certificates/$", "GET", "view",
                                   [Profile, ProfileCertificateReference, CertificateVendor, Certificate]),
    "profiles-certificates-add": (r"^/profiles/\d+/certificates/$", "POST", "add",
                                  [Profile, ProfileCertificateReference, CertificateVendor, Certificate]),
    "profiles-certificates-view": (r"^/profiles/\d+/certificates/\d+/edit.+$", "GET", "view",
                                   [Profile, ProfileCertificateReference, CertificateVendor, Certificate]),
    "profiles-certificates-update": (r"^/profiles/\d+/certificates/\d+/edit.+$", "POST", "change",
                                     [Profile, ProfileCertificateReference, CertificateVendor, Certificate]),
    "profiles-certificates-delete-view": (r"^/profiles/\d+/certificates/\d+/delete.+", "GET", "view",
                                          [ProfileProjectReference, ProfileCertificateReference]),
    "profiles-certificates-delete": (r"^/profiles/\d+/certificates/\d+/delete.+", "POST", "delete",
                                     [Profile, ProfileCertificateReference, CertificateVendor, Certificate]),

    "profiles-skills-list": (r"^/profiles/\d+/skills/$", "GET", "view",
                             [Profile, ProfileSkillReference, Skill]),
    "profiles-skills-add": (r"^/profiles/\d+/skills/$", "POST", "add",
                            [Profile, ProfileSkillReference, Skill]),
    "profiles-skills-view": (r"^/profiles/\d+/skills/\d+/edit.+$", "GET", "view",
                             [Profile, ProfileSkillReference, Skill]),
    "profiles-skills-update": (r"^/profiles/\d+/skills/\d+/edit.+$", "POST", "change",
                               [Profile, ProfileSkillReference, Skill]),
    "profiles-skills-delete-view": (r"^/profiles/\d+/skills/\d+/delete.+", "GET", "view",
                                    [ProfileSkillReference]),
    "profiles-skills-delete": (r"^/profiles/\d+/skills/\d+/delete.+", "POST", "delete",
                               [Profile, ProfileSkillReference, Skill]),

    "skills-list": (r"^/skills/$", "GET", "view", [Skill]),
    "skills-add": (r"^/skills/$", "POST", "add", [Skill]),
    "skills-view": (r"^/skills/\d+/edit/$", "GET", "view", [Skill]),
    "skills-update": (r"^/skills/\d+/edit/$", "POST", "change", [Skill]),
    "skills-delete-view": (r"^/skills/\d+/delete/", "GET", "view", [Skill]),
    "skills-delete": (r"^/skills/\d+/delete/", "POST", "delete", [Skill]),

    "certificates-list": (r"^/certificates/$", "GET", "view", [CertificateVendor, Certificate]),
    "certificates-add": (r"^/certificates/$", "POST", "add", [CertificateVendor, Certificate]),
    "certificates-view": (r"^/certificates/\d+/edit/$", "GET", "view", [CertificateVendor, Certificate]),
    "certificates-update": (r"^/certificates/\d+/edit/$", "POST", "change", [CertificateVendor, Certificate]),
    "certificates-delete-view": (r"^/certificates/\d+/delete/", "GET", "view", [CertificateVendor, Certificate]),
    "certificates-delete": (r"^/certificates/\d+/delete/", "POST", "delete", [CertificateVendor, Certificate]),

    "customer-list": (r"^/customers/$", "GET", "view", [Customer, Project]),
    "customer-add": (r"^/customers/$", "POST", "add", [Customer]),
    "customer-view": (r"^/customers/\d+/edit/$", "GET", "view", [Customer, Project, CustomerLog, ProjectLog]),
    "customer-update": (r"^/customers/\d+/edit/$", "POST", "change", [Customer, Project, CustomerLog, ProjectLog]),
    "customer-delete-view": (r"^/customers/\d+/delete/", "GET", "view", [Customer]),
    "customer-delete": (r"^/customers/\d+/delete/", "POST", "delete", [Customer]),
    "customer-logs": (r"^/customers/\d+/logs/", "GET", "view", [CustomerLog]),
    "customer-logs-change": (r"^/customers/\d+/logs/", "POST", "change", [CustomerLog]),
    "project-edit": (r"^/customers/\d+/projects/\d+/edit/$", "GET", "view", [Customer, Project]),
    "project-update": (r"^/customers/\d+/projects/\d+/edit/$", "POST", "change", [Customer, Project]),
    "project-delete-view": (r"^/customers/\d+/projects/\d+/delete/$", "GET", "delete", [Customer, Project]),
    "project-delete": (r"^/customers/\d+/projects/\d+/delete/$", "POST", "delete", [Customer, Project]),
    "project-logs": (r"^/customers/\d+/projects/\d+/logs/$", "GET", "view", [ProjectLog]),
    "project-logs-change": (r"^/customers/\d+/projects/\d+/logs/$", "POST", "change", [ProjectLog]),

    "templates-list": (r"^/templates/$", "GET", "view", [Template]),
    "templates-add": (r"^/templates/$", "POST", "add", [Template]),
    "templates-view": (r"^/templates/\d+/edit/$", "GET", "view", [Template]),
    "templates-update": (r"^/templates/\d+/edit/$", "POST", "change", [Template]),
    "templates-delete-view": (r"^/templates/\d+/delete/", "GET", "view", [Template]),
    "templates-delete": (r"^/templates/\d+/delete/", "POST", "delete", [Template]),
}


def has_permission_for_name(user, name) -> bool:
    if user.is_authenticated and not settings.SKILLSMANAGER_USE_RBAC:
        return True
    elif user.is_authenticated and user.is_superuser:
        return True
    is_ok = True
    try:
        path = path_map[name]

        if path[2] == "none":
            return True
        elif path[2] == "auth":
            return user.is_authenticated
        elif path[2] == "superuser":
            return user.is_superuser

        for model in path[3]:
            if not user.has_perm("skillsManager.%s_%s" % (path[2], model._meta.model_name)):
                is_ok = False
        return is_ok
    except KeyError:
        logging.warning("Permission request for path <%s> resulted in unknown path. Defaulting to forbid" % name)
        return False


def has_permission_for_request(request) -> bool:
    for name, path in path_map.items():
        if re.search(path[0], request.path) and request.method == path[1]:
            return has_permission_for_name(request.user, name)
    return False


def has_permission(user, permissions: str | list, require_all=False):
    if not settings.SKILLSMANAGER_USE_RBAC:
        return True
    if type(permissions) is str:
        return user.has_perm(permissions)
    elif require_all:
        return user.has_perms(permissions)
    else:
        for permission in permissions:
            if user.has_perm(permission):
                return True
    return False


def has_permission_lambda(permission: str | list, require_all=False):
    return lambda user, **_: has_permission(user, permission, require_all)


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        if has_permission_for_request(request):
            # Requests to /login are always allowed
            return self.get_response(request)
        else:
            path = request.build_absolute_uri()
            resolved_login_url = settings.LOGIN_URL
            # If the login url is the same scheme and net location then use the
            # path as the "next" url.
            login_scheme, login_netloc = urlsplit(resolved_login_url)[:2]
            current_scheme, current_netloc = urlsplit(path)[:2]
            if (not login_scheme or login_scheme == current_scheme) and (
                    not login_netloc or login_netloc == current_netloc
            ):
                path = request.get_full_path()

            return redirect_to_login(
                path,
                resolved_login_url,
            )
