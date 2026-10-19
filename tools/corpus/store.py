"""SQLite storage for corpus documents: file states, doc rows, an FTS5 table and dense vectors."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterable, Iterator

from tools.corpus.docs import Doc

SCHEMA = """
CREATE TABLE IF NOT EXISTS sources(path TEXT PRIMARY KEY, mtime REAL, size INTEGER, sha TEXT);
CREATE TABLE IF NOT EXISTS docs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doc_id TEXT UNIQUE, kind TEXT, path TEXT, line INTEGER,
    title TEXT, text TEXT, meta TEXT, sha TEXT
);
CREATE INDEX IF NOT EXISTS docs_path ON docs(path);
CREATE INDEX IF NOT EXISTS docs_kind ON docs(kind);
CREATE VIRTUAL TABLE IF NOT EXISTS docs_fts USING fts5(title, text, tokenize='porter unicode61');
CREATE TABLE IF NOT EXISTS vectors(sha TEXT PRIMARY KEY, vec BLOB);
CREATE TABLE IF NOT EXISTS info(key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE IF NOT EXISTS issues(path TEXT, message TEXT);
CREATE INDEX IF NOT EXISTS issues_path ON issues(path);
"""


def content_sha(title: str, text: str) -> str:
    return hashlib.sha1(f"{title}\n{text}".encode("utf-8")).hexdigest()


class Store:
    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(path, timeout=30)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.executescript(SCHEMA)

    def close(self) -> None:
        self.conn.close()

    @contextmanager
    def write(self) -> Iterator[None]:
        """One write transaction: commit on success, roll back on any exception (even Ctrl-C).

        BEGIN IMMEDIATE takes the write lock up front, so two refreshing agents queue instead
        of failing half-way, and nothing is left holding the lock after an error.
        """
        self.conn.execute("BEGIN IMMEDIATE")
        try:
            yield
        except BaseException:
            self.conn.rollback()
            raise
        self.conn.commit()

    # file states -------------------------------------------------------
    def file_states(self) -> dict[str, tuple[float, int, str]]:
        return {row[0]: (row[1], row[2], row[3]) for row in self.conn.execute("SELECT path, mtime, size, sha FROM sources")}

    def set_file_state(self, path: str, mtime: float, size: int, sha: str) -> None:
        self.conn.execute("INSERT OR REPLACE INTO sources VALUES (?, ?, ?, ?)", (path, mtime, size, sha))

    # parse problems ------------------------------------------------------
    def set_issues(self, path: str, messages: Iterable[str]) -> None:
        self.conn.execute("DELETE FROM issues WHERE path = ?", (path,))
        self.conn.executemany("INSERT INTO issues VALUES (?, ?)", [(path, message) for message in messages])

    def issues(self) -> list[tuple[str, str]]:
        return list(self.conn.execute("SELECT path, message FROM issues ORDER BY path, rowid"))

    # documents -----------------------------------------------------------
    def _delete_rows(self, ids: list[int]) -> None:
        self.conn.executemany("DELETE FROM docs_fts WHERE rowid = ?", [(i,) for i in ids])
        self.conn.executemany("DELETE FROM docs WHERE id = ?", [(i,) for i in ids])

    def remove_file(self, path: str) -> list[int]:
        ids = [row[0] for row in self.conn.execute("SELECT id FROM docs WHERE path = ?", (path,))]
        self._delete_rows(ids)
        self.conn.execute("DELETE FROM sources WHERE path = ?", (path,))
        self.conn.execute("DELETE FROM issues WHERE path = ?", (path,))
        return ids

    def _insert(self, doc: Doc, sha: str, meta: str) -> int:
        """Insert one doc and its FTS row. An id another file already uses gets an `@path` suffix."""
        row = (doc.kind, doc.path, doc.line, doc.title, doc.text, meta, sha)
        candidates = [doc.doc_id, f"{doc.doc_id}@{doc.path}"]
        attempt = 0
        while True:
            doc_id = candidates[attempt] if attempt < len(candidates) else f"{doc.doc_id}@{doc.path}~{attempt}"
            try:
                cursor = self.conn.execute(
                    "INSERT INTO docs(doc_id, kind, path, line, title, text, meta, sha) VALUES (?,?,?,?,?,?,?,?)",
                    (doc_id, *row),
                )
                break
            except sqlite3.IntegrityError:
                attempt += 1
        rowid = cursor.lastrowid
        self.conn.execute("INSERT INTO docs_fts(rowid, title, text) VALUES (?, ?, ?)", (rowid, doc.title, doc.text))
        return rowid

    def replace_file(self, path: str, docs: Iterable[Doc]) -> tuple[list[int], list[int]]:
        """Bring one file's docs up to date; returns (added row ids, removed row ids).

        Docs whose id, kind, title and text are unchanged keep their row (and so their place in
        the TF-IDF matrix); only a moved line or changed metadata is updated in place.
        """
        suffix = f"@{path}"
        existing: dict[str, tuple[int, str, int, str, str]] = {}
        removed: list[int] = []
        for rowid, doc_id, kind, line, meta, sha in self.conn.execute(
            "SELECT id, doc_id, kind, line, meta, sha FROM docs WHERE path = ? ORDER BY id", (path,)
        ):
            base = doc_id[: -len(suffix)] if doc_id.endswith(suffix) else doc_id.split(f"{suffix}~")[0]
            if base in existing:  # a duplicate left by an older index
                removed.append(rowid)
                continue
            existing[base] = (rowid, kind, line, meta, sha)
        insert: list[tuple[Doc, str, str]] = []
        for doc in docs:
            sha = content_sha(doc.title, doc.text)
            meta = json.dumps(doc.meta, default=str)
            old = existing.pop(doc.doc_id, None)
            if old is not None and old[1] == doc.kind and old[4] == sha:
                if (old[2], old[3]) != (doc.line, meta):
                    self.conn.execute("UPDATE docs SET line = ?, meta = ? WHERE id = ?", (doc.line, meta, old[0]))
                continue
            if old is not None:
                removed.append(old[0])
            insert.append((doc, sha, meta))
        removed.extend(old[0] for old in existing.values())
        self._delete_rows(removed)
        added = [self._insert(doc, sha, meta) for doc, sha, meta in insert]
        return added, removed

    def drop_orphan_fts_rows(self) -> None:
        """Older indexes could leave FTS rows whose document was replaced; drop them."""
        self.conn.execute("DELETE FROM docs_fts WHERE rowid NOT IN (SELECT id FROM docs)")

    def commit(self) -> None:
        self.conn.commit()

    def rollback(self) -> None:
        self.conn.rollback()

    def count(self) -> int:
        return self.conn.execute("SELECT COUNT(*) FROM docs").fetchone()[0]

    def doc_ids(self) -> list[str]:
        return [row[0] for row in self.conn.execute("SELECT doc_id FROM docs ORDER BY id")]

    def kinds_by_row(self) -> dict[int, str]:
        return dict(self.conn.execute("SELECT id, kind FROM docs"))

    def texts(self, ids: Iterable[int] | None = None) -> Iterator[tuple[int, str]]:
        if ids is None:
            yield from self.conn.execute("SELECT id, title || ' ' || text FROM docs ORDER BY id")
            return
        for rowid in ids:
            row = self.conn.execute("SELECT id, title || ' ' || text FROM docs WHERE id = ?", (rowid,)).fetchone()
            if row:
                yield row

    def rows(self, ids: Iterable[int]) -> dict[int, Doc]:
        found: dict[int, Doc] = {}
        for rowid in ids:
            row = self.conn.execute(
                "SELECT id, doc_id, kind, path, line, title, text, meta FROM docs WHERE id = ?", (rowid,)
            ).fetchone()
            if row:
                found[row[0]] = Doc(row[1], row[2], row[3], row[4], row[5], row[6], json.loads(row[7]))
        return found

    def row_of(self, doc_id: str) -> int | None:
        row = self.conn.execute("SELECT id FROM docs WHERE doc_id = ?", (doc_id,)).fetchone()
        return row[0] if row else None

    def get(self, doc_id: str) -> Doc | None:
        rowid = self.row_of(doc_id)
        return self.rows([rowid]).get(rowid) if rowid is not None else None

    # full-text search ------------------------------------------------------
    def fts(self, match: str, kinds: tuple[str, ...], limit: int) -> list[int]:
        if not match:
            return []
        sql = (
            "SELECT docs_fts.rowid FROM docs_fts JOIN docs ON docs.id = docs_fts.rowid "
            "WHERE docs_fts MATCH ?"
        )
        params: list[Any] = [match]
        if kinds:
            sql += f" AND docs.kind IN ({','.join('?' * len(kinds))})"
            params.extend(kinds)
        sql += " ORDER BY bm25(docs_fts, 2.0, 1.0) LIMIT ?"
        params.append(limit)
        return [row[0] for row in self.conn.execute(sql, params)]

    # dense vectors -----------------------------------------------------------
    def missing_vector_rows(self) -> list[tuple[str, str]]:
        """(sha, text) for every distinct doc content that has no stored vector."""
        return list(
            self.conn.execute(
                "SELECT docs.sha, MIN(docs.title || ' ' || substr(docs.text, 1, 1500)) FROM docs "
                "LEFT JOIN vectors ON vectors.sha = docs.sha WHERE vectors.sha IS NULL GROUP BY docs.sha"
            )
        )

    def docs_without_vectors(self) -> int:
        return self.conn.execute(
            "SELECT COUNT(*) FROM docs LEFT JOIN vectors ON vectors.sha = docs.sha WHERE vectors.sha IS NULL"
        ).fetchone()[0]

    def put_vectors(self, items: Iterable[tuple[str, bytes]]) -> None:
        self.conn.executemany("INSERT OR REPLACE INTO vectors VALUES (?, ?)", items)

    def vector_rows(self) -> Iterator[tuple[int, bytes]]:
        yield from self.conn.execute("SELECT docs.id, vectors.vec FROM docs JOIN vectors ON vectors.sha = docs.sha")

    def has_vectors(self) -> bool:
        return self.conn.execute("SELECT 1 FROM vectors LIMIT 1").fetchone() is not None

    # info ---------------------------------------------------------------------
    def info(self, key: str, default: str | None = None) -> str | None:
        row = self.conn.execute("SELECT value FROM info WHERE key = ?", (key,)).fetchone()
        return row[0] if row else default

    def set_info(self, key: str, value: str) -> None:
        self.conn.execute("INSERT OR REPLACE INTO info VALUES (?, ?)", (key, value))
