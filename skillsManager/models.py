from auditlog.registry import auditlog
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    given_name = models.CharField(_("Given name"), max_length=200)
    last_name = models.CharField(_("Last name"), max_length=200)
    email = models.EmailField(_("E-Mail"))
    active_since = models.DateField(_("Active since"), default=now)
    active_until = models.DateField(_("Active until"), blank=True, null=True)

    def get_absolute_url(self):
        return reverse("profile-view", kwargs={"pk": self.pk})

    def __str__(self):
        return "%s, %s (%s)" % (self.last_name, self.given_name, self.email)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")


auditlog.register(Profile)


class ProfileMeta(models.Model):
    profile = models.ForeignKey(Profile, verbose_name=_("Profile"), on_delete=models.CASCADE)
    birthday = models.DateField(_("Birthday"), blank=True, null=True)
    photo = models.ImageField(_("Photo"), blank=True, null=True)
    available_from = models.DateField(_("Available from"), blank=True, null=True)
    job_title = models.CharField(_("Job title"), max_length=200, blank=True, null=True)
    description = models.TextField(_("Description"), blank=True, null=True)
    maturity_level = models.PositiveSmallIntegerField(_("Maturity level"), default=7)

    @property
    def maturity_level_percent(self, max=10):
        return int(round(self.maturity_level / max * 100, 0))

    def __str__(self):
        return self.profile.__str__()

    class Meta:
        verbose_name = _("Profile meta")
        verbose_name_plural = _("Profile metas")


auditlog.register(ProfileMeta)


class Education(models.Model):
    profile = models.ForeignKey(Profile, verbose_name=_("Profile"), on_delete=models.CASCADE)
    name = models.CharField(_("Name"), max_length=200)

    class Meta:
        verbose_name = _("Education")
        verbose_name_plural = _("Educations")


auditlog.register(Education)


class Language(models.Model):
    profile = models.ForeignKey(Profile, verbose_name=_("Profile"), on_delete=models.CASCADE)
    language = models.CharField(_("Language"), max_length=200)

    class Meta:
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")


auditlog.register(Language)


class Skill(models.Model):
    name = models.CharField(_("Name"), max_length=200)
    description = models.TextField(_("Description"), blank=True, null=True)
    related_skills = models.ManyToManyField("self", verbose_name=_("Related skills"), symmetrical=False, blank=True)

    def get_absolute_url(self):
        return reverse("skill-view", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Skill")
        verbose_name_plural = _("Skills")


class ProfileSkillReference(models.Model):
    profile = models.ForeignKey(Profile, verbose_name=_("Profile"), on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, verbose_name=_("Skill"), on_delete=models.CASCADE)
    level = models.IntegerField(_("Level"))
    favorite = models.IntegerField(_("Favorite"))
    remarks = models.TextField(_("Remarks"), blank=True, null=True)

    def __str__(self):
        return "%s - %d/%d" % (self.skill.name, self.level, self.favorite)

    def get_absolute_url(self):
        return reverse("profileskills-view", kwargs={"profile_pk": self.profile.pk, "pk": self.pk})

    class Meta:
        verbose_name = _("Profile skill reference")
        verbose_name_plural = _("Profile skill references")


class Customer(models.Model):
    name = models.CharField(_("Name"), max_length=200)
    industry = models.CharField(_("Industry"), max_length=200, blank=True, null=True)
    description = models.TextField(_("Description"), blank=True, null=True)
    parent_customer = models.ForeignKey(
        "self", blank=True, null=True, on_delete=models.SET_NULL, verbose_name=_("Customer")
    )
    active_since = models.DateField(_("Active since"), default=now)
    active_until = models.DateField(_("Active until"), blank=True, null=True)

    def get_absolute_url(self):
        return reverse("customer-view", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")


class CustomerLog(models.Model):
    customer = models.ForeignKey(Customer, verbose_name=_("Customer"), on_delete=models.CASCADE)
    notice = models.TextField(_("Notice"))
    timestamp = models.DateTimeField(_("Timestamp"), default=now)

    def __str__(self):
        return "%s (%s)" % (self.customer.name, self.timestamp.isoformat())

    class Meta:
        verbose_name = _("Customer log")
        verbose_name_plural = _("Customer logs")


class Project(models.Model):
    name = models.CharField(_("Name"), max_length=200)
    description = models.TextField(_("Description"), blank=True, null=True)
    customer = models.ForeignKey(Customer, verbose_name=_("Customer"), on_delete=models.CASCADE)
    active_since = models.DateField(_("Active since"), default=now)
    active_until = models.DateField(_("Active until"), blank=True, null=True)

    def __str__(self):
        return "%s/%s" % (self.customer.name, self.name)

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")


class ProfileProjectReference(models.Model):
    profile = models.ForeignKey(Profile, verbose_name=_("Profile"), on_delete=models.CASCADE)
    project = models.ForeignKey(Project, verbose_name=_("Project"), on_delete=models.CASCADE)
    active_since = models.DateField(_("Active since"), default=now)
    active_until = models.DateField(_("Active until"), blank=True, null=True)
    remarks = models.TextField(_("Remarks"), blank=True, null=True)

    def get_absolute_url(self):
        return reverse(
            "projectwork-view", kwargs={"profile_pk": self.profile.pk, "pk": self.pk}
        )

    class Meta:
        verbose_name = _("Profile project reference")
        verbose_name_plural = _("Profile project references")


class ProfileProjectSkillReference(models.Model):
    profile_project_reference = models.ForeignKey(
        ProfileProjectReference, on_delete=models.CASCADE, verbose_name=_("Profile project reference")
    )
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, verbose_name=_("Skill"))

    class Meta:
        verbose_name = _("Profile project skill reference")
        verbose_name_plural = _("Profile project skill references")


class ProjectLog(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name=_("Profile"))
    notice = models.TextField(_("Notice"))
    timestamp = models.DateTimeField(_("Timestamp"), default=now)

    def __str__(self):
        return "%s (%s)" % (self.project.customer.name, self.timestamp.isoformat())

    class Meta:
        verbose_name = _("Project log")
        verbose_name_plural = _("Project logs")


class CertificateVendor(models.Model):
    name = models.CharField(_("Name"), max_length=200)

    def get_absolute_url(self):
        return reverse("vendor-view", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Certificate vendor")
        verbose_name_plural = _("Certificate vendors")


class Certificate(models.Model):
    vendor = models.ForeignKey(CertificateVendor, verbose_name=_("Vendor"), on_delete=models.CASCADE)
    name = models.CharField(_("Name"), max_length=200)
    description = models.TextField(_("Description"), blank=True, null=True)

    def __str__(self):
        return "%s (%s)" % (self.name, self.vendor)

    class Meta:
        verbose_name = _("Certificate")
        verbose_name_plural = _("Certificates")


def generate_certificate_filename(instance, filename):
    return "certificates/%s.%s/%s-%s" % (
        instance.profile.given_name, instance.profile.last_name, instance.certificate.name, filename
    )


class ProfileCertificateReference(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_("Profile"))
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE, verbose_name=_("Certificate"))
    active_since = models.DateField(_("Active since"), default=now)
    active_until = models.DateField(_("Active until"), blank=True, null=True)
    file = models.FileField(_("File"), blank=True, null=True, upload_to=generate_certificate_filename)

    def __str__(self):
        return "%s %s-%s" % (
            self.certificate.name,
            self.active_since,
            self.active_until,
        )

    def get_absolute_url(self):
        return reverse("profilecertificates-view", kwargs={"profile_pk": self.profile.pk, "pk": self.pk})

    class Meta:
        verbose_name = _("Profile certificate reference")
        verbose_name_plural = _("Profile certificate references")


class Template(models.Model):
    name = models.CharField(_("Name"), max_length=200)
    description = models.TextField(_("Description"), blank=True, null=True)
    template = models.TextField(_("Template"))

    def get_absolute_url(self):
        return reverse("template-view", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Template")
        verbose_name_plural = _("Templates")
