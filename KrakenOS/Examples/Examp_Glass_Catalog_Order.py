#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Example: inspect glass catalog loading order.

This example prints the deterministic glass catalog order used by KrakenOS and
shows what happens when a glass name appears in several loaded catalogs.

What this example teaches:
- how `Setup().GlassCat` stores the active catalog list
- why catalog priority matters when a glass name is duplicated
- how to inspect which catalogs contain a given glass name

Expected output:
- the first loaded catalogs
- all catalogs containing the selected glass name
- the first matching catalog that KrakenOS will use by priority

Didactic note:
- this example only reports catalog order. It does not claim that the first
  matching catalog is always the best physical choice.
"""

import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
import KrakenOS as Kos


def catalog_name(path):
    return os.path.basename(path)


def catalogs_containing_glass(config, glass_name):
    matches = []

    for catalog_path in config.GlassCat:
        try:
            with open(catalog_path, "r", encoding="UTF8") as catalog:
                for line in catalog:
                    parts = line.split()
                    if len(parts) >= 2 and parts[0] == "NM" and parts[1] == glass_name:
                        matches.append(catalog_name(catalog_path))
                        break
        except UnicodeError:
            with open(catalog_path, "r", encoding="UTF16") as catalog:
                for line in catalog:
                    parts = line.split()
                    if len(parts) >= 2 and parts[0] == "NM" and parts[1] == glass_name:
                        matches.append(catalog_name(catalog_path))
                        break

    return matches


config = Kos.Setup()

print("\nFirst loaded glass catalogs:")
for catalog_path in config.GlassCat[:10]:
    print(" -", catalog_name(catalog_path))

glass = "LAF2"
matches = catalogs_containing_glass(config, glass)

print(f"\nGlass {glass} was found in {len(matches)} loaded catalogs:")
for catalog in matches:
    print(" -", catalog)

if matches:
    print(f"\nWith the current catalog order, the first matching source is: {matches[0]}")
    print("This example does not decide which catalog is best; it only shows that order matters.")

print(
    "\nKrakenOS uses a deterministic catalog order with SCHOTT.AGF first by default, "
    "similar to Zemax catalog priority. Future improvement: add a catalog manager "
    "or GUI so users can inspect duplicate glass names and choose catalog priority explicitly."
)
