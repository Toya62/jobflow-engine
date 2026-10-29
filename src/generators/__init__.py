"""
src/generators package
Provides tailored LaTeX application generation, PDF compilation, and outreach emails.
"""

from src.generators.application import generate_tailored_application
from src.generators.compiler import compile_all_applications
from src.generators.email import generate_application_email
from src.generators.auto_generate import auto_generate_approved_applications

__all__ = [
    "generate_tailored_application",
    "compile_all_applications",
    "generate_application_email",
    "auto_generate_approved_applications",
]
