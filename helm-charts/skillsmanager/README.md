# skillsmanager

![Version: 0.1.0](https://img.shields.io/badge/Version-0.1.0-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: 1.0.0](https://img.shields.io/badge/AppVersion-1.0.0-informational?style=flat-square)

A Helm chart for deploying Skillsmanager

**Homepage:** <https://github.com/devobagmbh/skillsmanager>

## Source Code

* <https://github.com/devobagmbh/skillsmanager>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| additionalVolumeMounts | list | `[]` |  |
| additionalVolumes[0].name | string | `"foo"` |  |
| additionalVolumes[0].secret.optional | bool | `false` |  |
| additionalVolumes[0].secret.secretName | string | `"mysecret"` |  |
| affinity | object | `{}` |  |
| autoscaling.enabled | bool | `false` |  |
| autoscaling.maxReplicas | int | `100` |  |
| autoscaling.minReplicas | int | `1` |  |
| autoscaling.targetCPUUtilizationPercentage | int | `80` |  |
| configuration.applicationHost | string | `""` | Host the application runs on (e.g. skills.company.com). Required if DEBUG is not set to true |
| configuration.azure | object | `{"clientId":"","clientSecret":{"secretKey":"azureClientSecret","secretName":""},"enabled":false,"prompt":"none","roles":{},"tenantId":""}` | Configuration for Azure EntraID based login |
| configuration.azure.clientId | string | `""` | Azure client id |
| configuration.azure.clientSecret | object | `{"secretKey":"azureClientSecret","secretName":""}` | Azure client secret key secret reference |
| configuration.azure.clientSecret.secretKey | string | `"azureClientSecret"` | Key inside the secret |
| configuration.azure.clientSecret.secretName | string | `""` | Name of the secret |
| configuration.azure.enabled | bool | `false` | Enable Azure EntraID based login |
| configuration.azure.prompt | string | `"none"` | Whether to just accept the login (`none`) force to user to `login`, `consent` again or select an account (`select_account`) |
| configuration.azure.roles | object | `{}` | Role to Django group mapping in JSON form. e.g.: ```json {        "95170e67-2bbf-4e3e-a4d7-e7e5829fe7a7": "GroupName1", # mapped to one Django group        "3dc6539e-0589-4663-b782-fef100d839aa": ["GroupName2", "GroupName3"] # mapped to multiple Django groups } ``` |
| configuration.azure.tenantId | string | `""` | Azure tenant id |
| configuration.databaseUrl | object | `{"secretKey":"databaseUrl","secretName":""}` | Database URL secret reference if the integrated SQLite database is not used |
| configuration.databaseUrl.secretKey | string | `"databaseUrl"` | Key inside the secret |
| configuration.databaseUrl.secretName | string | `""` | Name of the secret |
| configuration.debug | bool | `false` | Whether to run the application in Django debug mode |
| configuration.djangoSecretKey | object | `{"secretKey":"djangoSecretKey","secretName":""}` | Secret reference for the django secret key |
| configuration.djangoSecretKey.secretKey | string | `"djangoSecretKey"` | Key inside the secret |
| configuration.djangoSecretKey.secretName | string | `""` | Name of the secret |
| configuration.djangoSuperUser.email | string | `""` | Email of the Django superuser |
| configuration.djangoSuperUser.password | object | `{"secretKey":"djangoSuperUserPassword","secretName":""}` | Secret reference for the django superuser password |
| configuration.djangoSuperUser.password.secretKey | string | `"djangoSuperUserPassword"` | Key inside the secret |
| configuration.djangoSuperUser.password.secretName | string | `""` | Name of the secret |
| configuration.djangoSuperUser.username | string | `"admin"` | Username of the Django superuser |
| fullnameOverride | string | `""` |  |
| httpRoute | object | `{"annotations":{},"enabled":false,"hostnames":["chart-example.local"],"parentRefs":[{"name":"gateway","sectionName":"http"}],"rules":[{"matches":[{"path":{"type":"PathPrefix","value":"/headers"}}]}]}` | Expose the service via gateway-api HTTPRoute Requires Gateway API resources and suitable controller installed within the cluster (see: https://gateway-api.sigs.k8s.io/guides/) |
| image.pullPolicy | string | `"IfNotPresent"` |  |
| image.repository | string | `"ghcr.io/devobagmbh/skillsmanager"` |  |
| image.tag | string | `""` |  |
| imagePullSecrets | list | `[]` |  |
| ingress.annotations | object | `{}` |  |
| ingress.className | string | `""` |  |
| ingress.enabled | bool | `false` |  |
| ingress.hosts[0].host | string | `"chart-example.local"` |  |
| ingress.hosts[0].paths[0].path | string | `"/"` |  |
| ingress.hosts[0].paths[0].pathType | string | `"ImplementationSpecific"` |  |
| ingress.tls | list | `[]` |  |
| livenessProbe.httpGet.path | string | `"/"` |  |
| livenessProbe.httpGet.port | string | `"http"` |  |
| nameOverride | string | `""` |  |
| nodeSelector | object | `{}` |  |
| persistence | object | `{"database":{"accessModes":["ReadWriteOnce"],"annotations":{},"enabled":false,"labels":{},"size":"10Gi","storageClass":""},"uploads":{"accessModes":["ReadWriteOnce"],"annotations":{},"enabled":false,"labels":{},"size":"10Gi","storageClass":""}}` | Persistence configuration |
| persistence.database | object | `{"accessModes":["ReadWriteOnce"],"annotations":{},"enabled":false,"labels":{},"size":"10Gi","storageClass":""}` | Configures a volume used for the embedded SQLite database |
| persistence.uploads | object | `{"accessModes":["ReadWriteOnce"],"annotations":{},"enabled":false,"labels":{},"size":"10Gi","storageClass":""}` | Configures a volume used for uploads in SkillsManager |
| podAnnotations | object | `{}` |  |
| podLabels | object | `{}` |  |
| podSecurityContext | object | `{}` |  |
| readinessProbe.httpGet.path | string | `"/"` |  |
| readinessProbe.httpGet.port | string | `"http"` |  |
| replicaCount | int | `1` |  |
| resources | object | `{}` |  |
| securityContext | object | `{}` |  |
| service.port | int | `8000` |  |
| service.type | string | `"ClusterIP"` |  |
| serviceAccount.annotations | object | `{}` |  |
| serviceAccount.automount | bool | `true` |  |
| serviceAccount.create | bool | `true` |  |
| serviceAccount.name | string | `""` |  |
| tolerations | list | `[]` |  |

----------------------------------------------
Autogenerated from chart metadata using [helm-docs v1.14.2](https://github.com/norwoodj/helm-docs/releases/v1.14.2)
