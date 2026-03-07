"""
pages/base_page.py

Abstract base class for all Page Objects.
Encapsulates common browser interactions so individual page objects
remain clean and focused on page-specific behaviour.

Responsibilities:
  - Wrapping low-level driver/browser calls (click, type, wait, scroll)
  - Providing screenshot-on-failure hooks
  - Centralising explicit wait strategies
"""
