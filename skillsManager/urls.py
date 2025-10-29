from django.urls import path

from .views import cv, profile, skill, certificate, skill_search, home
from iommi.experimental.main_menu import MainMenu, M

menu_declaration = MainMenu(
    items=dict(
        home=M(
            icon="home",
            view=home.HomePage().as_view(),
        ),
        cv=M(
            icon="print",
            view=cv.CVPage().as_view(),
        ),
        skill_search=M(
            icon="search",
            view=skill_search.SkillSearchPage().as_view(),
        ),
        profiles=M(
            icon="users",
            view=profile.ProfileView().as_view(),
            paths=[
                path("<int:pk>/", profile.ProfileEdit().as_view(), name="profile-view"),
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
            ],
        ),
        skills=M(
            icon="check",
            view=skill.SkillView().as_view(),
            paths=[
                path("<int:pk>/", skill.skill_edit.as_view(), name="skill-view"),
                path("<int:pk>/edit/", skill.skill_edit.as_view(), name="skill-edit"),
                path(
                    "<int:pk>/delete/",
                    skill.skill_delete.as_view(),
                    name="skill-delete",
                ),
            ],
        ),
        certificates=M(
            icon="certificate",
            view=certificate.VendorView().as_view(),
            paths=[
                path(
                    "<int:pk>/", certificate.VendorEdit().as_view(), name="vendor-view"
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
    )
)

urlpatterns = menu_declaration.urlpatterns()
