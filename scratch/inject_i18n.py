import re
import json
from pathlib import Path
from update_i18n import MAP_KEYS_BY_LANG

APP_JS = Path("backend/app/static/app.js")
content = APP_JS.read_text(encoding="utf-8")

# Merge keys for each language
for lang, map_dict in MAP_KEYS_BY_LANG.items():
    # Find the language block inside i18n
    pattern = rf"({lang}:\s*\{{)"
    entries = ",\n        ".join([f"{k}: '{v.replace("'", "\\'")}'" for k, v in map_dict.items()])
    replacement = rf"\1\n        {entries},"
    content = re.sub(pattern, replacement, content)

# Update setLanguage function to translate all map element IDs
set_lang_pattern = r"(if \(document\.getElementById\('lbl-db-subtitle'\)\) document\.getElementById\('lbl-db-subtitle'\)\.innerHTML = t\.dbSubtitle;)"

map_updates = """\1
    if (document.getElementById('lbl-map-title')) document.getElementById('lbl-map-title').innerHTML = t.mapTitle || 'Crop Suitability & Water Stress Map';
    if (document.getElementById('lbl-map-subtitle')) document.getElementById('lbl-map-subtitle').innerHTML = t.mapSubtitle || '';
    if (document.getElementById('lbl-crop-select-title')) document.getElementById('lbl-crop-select-title').innerHTML = t.selectCrop || 'Select Crop:';
    if (document.getElementById('lbl-layer-select-title')) document.getElementById('lbl-layer-select-title').innerHTML = t.layer || 'Layer:';
    if (document.getElementById('btn-layer-suitability')) document.getElementById('btn-layer-suitability').innerHTML = t.cropSuitability || '🌾 Crop Suitability';
    if (document.getElementById('btn-layer-water-stress')) document.getElementById('btn-layer-water-stress').innerHTML = t.waterStress || '💧 Water Stress';
    if (document.getElementById('btn-toggle-compare')) document.getElementById('btn-toggle-compare').innerHTML = t.compareCrop || '⚔️ Compare Crop';
    if (document.getElementById('map-active-title')) document.getElementById('map-active-title').innerHTML = t.mapOverviewTitle || 'India Regional Suitability Overview';
    if (document.getElementById('lbl-catalog-accordion')) document.getElementById('lbl-catalog-accordion').innerHTML = t.catalogAccordionLabel || 'View Standardized Footprint Database Catalog (41 Items)';

    renderMapLegend();
    if (activeStateId) selectRegionalState(activeStateId);"""

content = re.sub(set_lang_pattern, map_updates, content)
APP_JS.write_text(content, encoding="utf-8")
print("app.js updated successfully with i18n map keys and setLanguage logic!")
