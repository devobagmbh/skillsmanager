from ..widgets import range_field
from ..models import Skill, ProfileSkillReference
from django.db.models import Count, Sum
from iommi import Page, Form, Action, html, Field, Table


class SkillTable(Table):

    class Meta:
        auto__model = ProfileSkillReference
        rows = lambda page, **_: page.extra.results


class SkillSearchPage(Page):

    class Meta:
        extra = dict(results=[])

    def do_search(form, page, **_):
        if form.is_valid():
            relevant_profiles = (
                ProfileSkillReference.objects.filter(
                    skill__in=form.fields["skill"].value,
                    level__gte=form.fields["required_level"].value,
                )
                .values("profile_id")
                .annotate(profile_count=Count("profile_id"))
                .filter(profile_count=len(form.fields["skill"].value))
                .values("profile_id")
            )
            profiles = (
                ProfileSkillReference.objects.filter(
                    profile_id__in=relevant_profiles,
                    skill__in=form.fields["skill"].value,
                )
                .annotate(fav_sum=Sum("favorite"))
                .order_by("fav_sum")
                .reverse()
                .all()
            )
            page.extra.results = profiles

    h1 = html.h1("Skill search")
    body_text = "Please select required skills"

    skill_filter = Form(
        actions__search=Action.submit(
            display_name="Search",
            post_handler=do_search,
        ),
        fields__skill=Field.multi_choice_queryset(
            choices=Skill.objects.all(),
        ),
        fields__required_level=range_field(
            1,
            10,
            required=False,
        ),
    )

    skill_table = SkillTable()
