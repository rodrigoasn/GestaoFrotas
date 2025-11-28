# ────────────────────────────────────────────────────────────────────
# IMPORTS
# ────────────────────────────────────────────────────────────────────
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


# ────────────────────────────────────────────────────────────────────
# DASHBOARD VIEW
# ────────────────────────────────────────────────────────────────────
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
