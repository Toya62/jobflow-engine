"""Unit tests for the unified PostgreSQL database layer."""

import os
import unittest.mock as mock
import pytest

from src.db.database import (
    PgConnectionWrapper,
    PgCursorWrapper,
    get_db_connection,
    is_postgres,
)


def test_is_postgres_detection(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    assert not is_postgres()

    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/db")
    assert is_postgres()

    monkeypatch.setenv("DATABASE_URL", "postgres://user:pass@localhost:5432/db")
    assert is_postgres()

    monkeypatch.setenv("DATABASE_URL", "sqlite:///data/test.db")
    assert not is_postgres()


def test_pg_cursor_translates_placeholders():
    mock_cur = mock.MagicMock()
    wrapper = PgCursorWrapper(mock_cur)

    # Placeholders translated
    wrapper.execute("SELECT * FROM jobs WHERE company = ? AND title = ?", ("ACME", "Dev"))
    mock_cur.execute.assert_called_once_with(
        "SELECT * FROM jobs WHERE company = %s AND title = %s",
        ("ACME", "Dev")
    )


def test_pg_cursor_translates_insert_or_ignore():
    mock_cur = mock.MagicMock()
    wrapper = PgCursorWrapper(mock_cur)

    wrapper.execute("INSERT OR IGNORE INTO jobs (company, title) VALUES (?, ?)", ("ACME", "Dev"))
    mock_cur.execute.assert_called_once_with(
        "INSERT INTO jobs (company, title) VALUES (%s, %s) ON CONFLICT DO NOTHING",
        ("ACME", "Dev")
    )


def test_pg_cursor_translates_insert_or_replace_applications():
    mock_cur = mock.MagicMock()
    wrapper = PgCursorWrapper(mock_cur)

    wrapper.execute(
        "INSERT OR REPLACE INTO applications (job_id, cv_pdf_path) VALUES (?, ?)",
        (1, "cv.pdf")
    )
    mock_cur.execute.assert_called_once()
    called_sql = mock_cur.execute.call_args[0][0]
    assert "INSERT INTO applications" in called_sql
    assert "ON CONFLICT (job_id) DO UPDATE SET" in called_sql
    assert "%s" in called_sql


def test_pg_cursor_ignores_begin_immediate():
    mock_cur = mock.MagicMock()
    wrapper = PgCursorWrapper(mock_cur)

    res = wrapper.execute("BEGIN IMMEDIATE")
    assert res is None
    mock_cur.execute.assert_not_called()


def test_pg_cursor_translates_datetime_now():
    mock_cur = mock.MagicMock()
    wrapper = PgCursorWrapper(mock_cur)

    wrapper.execute("UPDATE evaluations SET evaluated_at = datetime('now') WHERE job_id = ?", (1,))
    mock_cur.execute.assert_called_once_with(
        "UPDATE evaluations SET evaluated_at = CURRENT_TIMESTAMP WHERE job_id = %s",
        (1,)
    )


def test_pg_connection_context_manager():
    mock_conn = mock.MagicMock()
    wrapper = PgConnectionWrapper(mock_conn)

    with wrapper as conn:
        conn.execute("SELECT 1")

    mock_conn.commit.assert_called_once()


def test_pg_connection_context_manager_rollback_on_error():
    mock_conn = mock.MagicMock()
    wrapper = PgConnectionWrapper(mock_conn)

    with pytest.raises(ValueError):
        with wrapper as conn:
            raise ValueError("Test error")

    mock_conn.rollback.assert_called_once()
