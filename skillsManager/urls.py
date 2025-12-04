import os

from django.urls import path
from django.utils.translation import gettext as _
from iommi.main_menu import MainMenu, M, EXTERNAL

from .middleware.auth import has_permission_for_name
from .views import (
    cv,
    profile,
    skill,
    skill_search,
    home,
    template,
    certificate,
    project,
)

menu_declaration = MainMenu(
    items=(
        dict(
            home=M(
                display_name=_("Home"),
                icon="home",
                view=home.HomePage().as_view(),
            ),
            cv=M(
                display_name=_("CV"),
                icon="print",
                view=cv.CVPage().as_view(),
                include=lambda user, **_: has_permission_for_name(user, "cv"),
            ),
            skill_search=M(
                display_name=_("Search"),
                icon="search",
                view=skill_search.SkillSearchPage().as_view(),
                include=lambda user, **_: has_permission_for_name(user, "skill_search"),
            ),
            profiles=M(
                display_name=_("Profiles"),
                icon="users",
                view=profile.ProfileView().as_view(),
                include=lambda user, **_: has_permission_for_name(user, "profiles-list"),
                paths=[
                    path(
                        "<int:pk>/",
                        profile.ProfileEdit().as_view(),
                        name="profile-view",
                    ),
                    path(
                        "<int:pk>/edit/",
                        profile.ProfileEdit().as_view(),
                        name="profile-edit",
                    ),
                    path(
                        "<int:pk>/delete/",
                        profile.profile_delete.as_view(),
                        name="profile-delete",
                    ),
                    path(
                        "<int:profile_pk>/work/",
                        profile.project_work.ProjectWorkView().as_view(),
                        name="projectwork-list",
                    ),
                    path(
                        "<int:profile_pk>/work/<int:pk>/",
                        profile.project_work.ProjectWorkEdit().as_view(),
                        name="projectwork-view",
                    ),
                    path(
                        "<int:profile_pk>/work/<int:pk>/edit/",
                        profile.project_work.ProjectWorkEdit().as_view(),
                        name="projectwork-edit",
                    ),
                    path(
                        "<int:profile_pk>/work/<int:pk>/delete/",
                        profile.project_work.project_work_delete.as_view(),
                        name="projectwork-delete",
                    ),
                    path(
                        "<int:profile_pk>/certificates/",
                        profile.certificate.ProfileCertificateView().as_view(),
                        name="profilecertificates-list",
                    ),
                    path(
                        "<int:profile_pk>/certificates/<int:pk>/",
                        profile.certificate.ProfileCertificateEdit().as_view(),
                        name="profilecertificates-view",
                    ),
                    path(
                        "<int:profile_pk>/certificates/<int:pk>/edit/",
                        profile.certificate.ProfileCertificateEdit().as_view(),
                        name="profilecertificates-edit",
                    ),
                    path(
                        "<int:profile_pk>/certificates/<int:pk>/delete/",
                        profile.certificate.profile_certificate_delete.as_view(),
                        name="profilecertificates-delete",
                    ),
                    path(
                        "<int:profile_pk>/skills/",
                        profile.skill.ProfileSkillView().as_view(),
                        name="profileskills-list",
                    ),
                    path(
                        "<int:profile_pk>/skills/<int:pk>/",
                        profile.skill.ProfileSkillEdit().as_view(),
                        name="profileskills-view",
                    ),
                    path(
                        "<int:profile_pk>/skills/<int:pk>/edit/",
                        profile.skill.ProfileSkillEdit().as_view(),
                        name="profileskills-edit",
                    ),
                    path(
                        "<int:profile_pk>/skills/<int:pk>/delete/",
                        profile.skill.profile_skill_delete.as_view(),
                        name="profileskills-delete",
                    ),
                ],
            ),
            skills=M(
                display_name=_("Skills"),
                icon="check",
                view=skill.SkillView().as_view(),
                include=lambda user, **_: has_permission_for_name(user, "skills-list"),
                paths=[
                    path("<int:pk>/", skill.SkillEdit().as_view(), name="skill-view"),
                    path(
                        "<int:pk>/edit/",
                        skill.SkillEdit().as_view(),
                        name="skill-edit",
                    ),
                    path(
                        "<int:pk>/delete/",
                        skill.skill_delete.as_view(),
                        name="skill-delete",
                    ),
                ],
            ),
            certificates=M(
                display_name=_("Certificates"),
                icon="certificate",
                view=certificate.VendorView().as_view(),
                include=lambda user, **_: has_permission_for_name(user, "certificates-list"),
                paths=[
                    path(
                        "<int:pk>/",
                        certificate.VendorEdit().as_view(),
                        name="vendor-view",
                    ),
                    path(
                        "<int:pk>/edit/",
                        certificate.VendorEdit().as_view(),
                        name="vendor-edit",
                    ),
                    path(
                        "<int:pk>/delete/",
                        certificate.vendor_delete.as_view(),
                        name="vendor-delete",
                    ),
                ],
            ),
            customers=M(
                display_name=_("Projects"),
                icon="book",
                view=project.customer.CustomerView().as_view(),
                include=lambda user, **_: has_permission_for_name(user, "customer-list"),
                paths=[
                    path(
                        "<int:pk>/",
                        project.customer.CustomerEdit().as_view(),
                        name="customer-view",
                    ),
                    path(
                        "<int:pk>/edit/",
                        project.customer.CustomerEdit().as_view(),
                        name="customer-edit",
                    ),
                    path(
                        "<int:pk>/delete/",
                        project.customer.customer_delete.as_view(),
                        name="customer-delete",
                    ),
                    path(
                        "<int:pk>/logs/",
                        project.customer.CustomerLogView().as_view(),
                        name="customer-logs",
                    ),
                    path(
                        "<int:customer_pk>/projects/",
                        project.customer.CustomerEdit().as_view(),
                        name="projects-list",
                    ),
                    path(
                        "<int:customer_pk>/projects/<int:pk>/",
                        project.customer.CustomerEdit().as_view(),
                        name="projects-view",
                    ),
                    path(
                        "<int:customer_pk>/projects/<int:pk>/edit/",
                        project.project.project_edit.as_view(),
                        name="projects-edit",
                    ),
                    path(
                        "<int:customer_pk>/projects/<int:pk>/delete/",
                        project.project.project_delete.as_view(),
                        name="projects-delete",
                    ),
                    path(
                        "<int:customer_pk>/projects/<int:pk>/logs/",
                        project.project.ProjectLogView().as_view(),
                        name="projects-log",
                    ),
                ],
            ),
            templates=M(
                display_name=_("Templates"),
                icon="file",
                view=template.TemplateView().as_view(),
                include=lambda user, **_: has_permission_for_name(user, "templates-list"),
                paths=[
                    path(
                        "<int:pk>/",
                        template.TemplateEdit().as_view(),
                        name="template-view",
                    ),
                    path(
                        "<int:pk>/edit/",
                        template.TemplateEdit().as_view(),
                        name="template-edit",
                    ),
                    path(
                        "<int:pk>/delete/",
                        template.template_delete.as_view(),
                        name="template-delete",
                    ),
                ],
            ),
            admin=M(
                display_name=_("Administration"),
                icon="wrench",
                view=EXTERNAL,
                url="/admin/",
                include=lambda user, **_: user.is_staff
            ),
            login=M(
                display_name=_("Login"),
                icon="sign-in",
                view=EXTERNAL,
                url="/login",
                include=lambda request, user, **_: (
                        os.environ.get("AZURE_ENABLED", "false").lower() == "false"
                        and not user.is_authenticated
                        or request.path.startswith("/login")
                )
            ),
            change_password=M(
                icon="key",
                view=EXTERNAL,
                url="/change_password",
                include=lambda user, **_: (
                        os.environ.get("AZURE_ENABLED", "false").lower() == "false"
                        and has_permission_for_name(user, "change_password")
                ),
            ),
            logout=M(
                icon="sign-out",
                view=EXTERNAL,
                url="/logout",
                include=lambda user, **_: has_permission_for_name(user, "logout"),
            )
        )
    )
)

urlpatterns = menu_declaration.urlpatterns()
