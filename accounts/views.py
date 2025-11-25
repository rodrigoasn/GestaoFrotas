# ────────────────────────────────────────────────────────────────────
# IMPORTS
# ────────────────────────────────────────────────────────────────────
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


# ────────────────────────────────────────────────────────────────────
# DASHBOARD VIEW
# ────────────────────────────────────────────────────────────────────
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
