#!/usr/bin/env python3
"""
scripts/shorten_long_application_filenames.py

Renames application packages in `applications/` where the filename exceeds 90 characters
(standard ATS requirement: "Der Dateiname darf nicht mehr als 90 Zeichen umfassen").
Also updates references in:
- .meta.json files
- SQLite data/karriere.db
- Outputs SQL statements to sync with PostgreSQL on oracle-server
"""

import os
import glob
import json
import sqlite3
import subprocess

def main():
    root = "applications"
    bases = set()
    
    # 1. Gather all files > 90 chars
    for p in glob.glob(f"{root}/**/*", recursive=True):
        if os.path.isfile(p):
            fname = os.path.basename(p)
            if len(fname) > 90:
                d = os.path.dirname(p)
                if fname.endswith("_cv.pdf"):
                    b = fname[:-7]
                elif fname.endswith("_cover.pdf"):
                    b = fname[:-10]
                elif fname.endswith(".meta.json"):
                    b = fname[:-10]
                elif fname.endswith("_cv.tex"):
                    b = fname[:-7]
                elif fname.endswith("_cover.tex"):
                    b = fname[:-10]
                else:
                    b = os.path.splitext(fname)[0]
                bases.add((d, b))

    print(f"Found {len(bases)} application packages with filenames > 90 chars.")
    if not bases:
        print("Nothing to shorten.")
        return

    # 2. Build mapping (d, old_base) -> new_base
    mapping = {}
    for d, b in sorted(bases):
        parts = b.split('_', 1)
        if len(parts) == 2:
            comp, pos = parts
            new_comp = comp[:30].rstrip('-')
            new_pos = pos[:35].rstrip('-')
            base_cand = f"{new_comp}_{new_pos}"
        else:
            base_cand = b[:65].rstrip('-')

        curr = base_cand
        counter = 2
        used = {v for (md, mb), v in mapping.items() if md == d}
        while curr in used or any(os.path.exists(os.path.join(d, f"{curr}{s}")) for s in ["_cv.pdf", "_cover.pdf", ".meta.json"] if not os.path.exists(os.path.join(d, f"{b}{s}"))):
            curr = f"{base_cand[:55].rstrip('-')}-{counter}"
            counter += 1

        mapping[(d, b)] = curr
        max_len = max(len(f"{curr}_cv.pdf"), len(f"{curr}_cover.pdf"), len(f"{curr}.meta.json"))
        assert max_len <= 85, f"Filename still too long: {curr} ({max_len} chars)"

    # 3. Rename files and update .meta.json
    renamed_files = [] # list of (old_path, new_path)
    path_replacements = {} # old_rel_path -> new_rel_path

    for (d, old_b), new_b in mapping.items():
        # Find all files belonging to this old base
        pattern = os.path.join(d, f"{old_b}*")
        matching_files = glob.glob(pattern)
        
        for old_path in matching_files:
            old_name = os.path.basename(old_path)
            # Replace the base prefix
            if old_name.startswith(old_b):
                suffix = old_name[len(old_b):]
                new_name = f"{new_b}{suffix}"
                new_path = os.path.join(d, new_name)
                
                if old_path != new_path:
                    # Rename on disk
                    os.rename(old_path, new_path)
                    renamed_files.append((old_path, new_path))
                    path_replacements[old_path] = new_path

        # If .meta.json exists under new path, update its contents
        new_meta_path = os.path.join(d, f"{new_b}.meta.json")
        if os.path.exists(new_meta_path):
            try:
                with open(new_meta_path, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                
                # Update fields if present
                if "cv_file" in meta and meta["cv_file"]:
                    meta["cv_file"] = meta["cv_file"].replace(old_b, new_b)
                if "cover_file" in meta and meta["cover_file"]:
                    meta["cover_file"] = meta["cover_file"].replace(old_b, new_b)
                if "cv_path" in meta and meta["cv_path"]:
                    meta["cv_path"] = meta["cv_path"].replace(old_b, new_b)
                if "cover_path" in meta and meta["cover_path"]:
                    meta["cover_path"] = meta["cover_path"].replace(old_b, new_b)

                with open(new_meta_path, "w", encoding="utf-8") as f:
                    json.dump(meta, f, indent=2, ensure_ascii=False)
            except Exception as e:
                print(f"Error updating {new_meta_path}: {e}")

    print(f"Renamed {len(renamed_files)} files on disk.")

    # 4. Update SQLite database data/karriere.db
    sqlite_db = "data/karriere.db"
    if os.path.exists(sqlite_db):
        conn = sqlite3.connect(sqlite_db)
        cursor = conn.cursor()
        updated_cv = 0
        updated_cov = 0
        
        for old_p, new_p in path_replacements.items():
            if old_p.endswith("_cv.pdf"):
                cursor.execute(
                    "UPDATE applications SET cv_pdf_path = ? WHERE cv_pdf_path = ?",
                    (new_p, old_p)
                )
                updated_cv += cursor.rowcount
            elif old_p.endswith("_cover.pdf"):
                cursor.execute(
                    "UPDATE applications SET cover_pdf_path = ? WHERE cover_pdf_path = ?",
                    (new_p, old_p)
                )
                updated_cov += cursor.rowcount
                
        conn.commit()
        conn.close()
        print(f"Updated SQLite: {updated_cv} CV paths, {updated_cov} cover paths.")

    # 5. Output SQL script for PostgreSQL
    sql_file = "scripts/update_postgres_short_paths.sql"
    with open(sql_file, "w", encoding="utf-8") as f:
        f.write("BEGIN;\n")
        for old_p, new_p in path_replacements.items():
            if old_p.endswith("_cv.pdf"):
                f.write(f"UPDATE applications SET cv_pdf_path = '{new_p}' WHERE cv_pdf_path = '{old_p}';\n")
            elif old_p.endswith("_cover.pdf"):
                f.write(f"UPDATE applications SET cover_pdf_path = '{new_p}' WHERE cover_pdf_path = '{old_p}';\n")
        f.write("COMMIT;\n")
    print(f"Wrote PostgreSQL migration script to {sql_file}.")

if __name__ == "__main__":
    main()
