{{/*
Expand the name of the chart.
*/}}
{{- define "skillsmanager.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "skillsmanager.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "skillsmanager.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "skillsmanager.labels" -}}
helm.sh/chart: {{ include "skillsmanager.chart" . }}
{{ include "skillsmanager.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "skillsmanager.selectorLabels" -}}
app.kubernetes.io/name: {{ include "skillsmanager.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "skillsmanager.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "skillsmanager.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Combine the persistence volumes with the additional volumes
*/}}
{{- define "skillsmanager.volumes" -}}
{{- if or (or .Values.persistence.database.enabled .Values.persistence.uploads.enabled) .Values.additionalVolumes }}
volumes:
{{- if .Values.persistence.database.enabled }}
  - name: database
    persistentVolumeClaim:
      claimName: {{ include "skillsmanager.fullname" . }}-database
{{- end }}
{{- if .Values.persistence.uploads.enabled }}
  - name: upload
    persistentVolumeClaim:
      claimName: {{ include "skillsmanager.fullname" . }}-uploads
{{- end }}
{{- if .Values.additionalVolumes }}
{{ .Values.additionalVolumes | toYaml | indent 2 }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Combine the persistence volume mounts with the additional volume mounts
*/}}
{{- define "skillsmanager.volumeMounts" -}}
{{- if or (or .Values.persistence.database.enabled .Values.persistence.uploads.enabled) .Values.additionalVolumeMounts }}
volumeMounts:
{{- if .Values.persistence.database.enabled }}
  - name: database
    mountPath: /app/db
{{- end }}
{{- if .Values.persistence.uploads.enabled }}
  - name: upload
    mountPath: /app/static/images
{{- end }}
{{- if .Values.additionalVolumeMounts }}
{{ .Values.additionalVolumeMounts | toYaml | indent 2 }}
{{- end }}
{{- end }}
{{- end }}
