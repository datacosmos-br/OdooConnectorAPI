{{/*
Generate basic labels
*/}}
{{- define "chart.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Define the full name
*/}}
{{- define "chart.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- include "chart.name" . | trunc 63 | trimSuffix "-" -}}
{{- if ne .Release.Name .Chart.Name -}}
{{- printf "%s-%s" .Release.Name (include "odooconnectorapi.name" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}
