// Keeps "light" meaning a light shell. GNOME Shell draws itself dark for
// color-scheme 'default' and light only for 'prefer-light', while the
// Quick Settings "Dark Style" toggle writes 'default' when it is turned
// off. Apex's light look is the default (design/INDEX.md), so 'default' is
// written back as 'prefer-light'. Apps treat the two the same, and the
// toggle reads only 'prefer-dark', so it keeps its state.

import Gio from 'gi://Gio';

const SCHEMA = 'org.gnome.desktop.interface';
const KEY = 'color-scheme';

/** Rewrites color-scheme 'default' to 'prefer-light' while it runs. */
export class ColorScheme {
  /** Starts watching the setting and fixes its current value. */
  constructor() {
    this._settings = new Gio.Settings({schema_id: SCHEMA});
    this._settings.connectObject(`changed::${KEY}`, () => this._sync(), this);
    this._sync();
  }

  /** Stops watching; the setting keeps its value. */
  destroy() {
    this._settings.disconnectObject(this);
    this._settings = null;
  }

  /** Turns 'default' into 'prefer-light'. */
  _sync() {
    if (this._settings.get_string(KEY) === 'default') {
      this._settings.set_string(KEY, 'prefer-light');
    }
  }
}
