// The Apex Shell extension. Its generated stylesheet themes the shell; the
// extension scopes that stylesheet by putting a class on the UI group, and
// turns the translucent variant on and off.

import {Extension} from 'resource:///org/gnome/shell/extensions/extension.js';
import * as Main from 'resource:///org/gnome/shell/ui/main.js';

// Every rule in stylesheet-*.css is scoped under this class.
const ROOT_CLASS = 'apex-shell';
// Added when translucent-surfaces is on; selects the glass tints.
const GLASS_CLASS = 'apex-glass';

/** Applies the Apex look to the running shell. */
export default class ApexExtension extends Extension {
  /** Scopes the stylesheet to the shell and follows the glass setting. */
  enable() {
    this._ui = Main.layoutManager.uiGroup;
    this._ui.add_style_class_name(ROOT_CLASS);
    this._settings = this.getSettings();
    this._settings.connectObject(
        'changed::translucent-surfaces', () => this._syncGlass(), this);
    this._syncGlass();
  }

  /** Puts the shell back the way it was. */
  disable() {
    this._settings.disconnectObject(this);
    this._settings = null;
    this._ui.remove_style_class_name(GLASS_CLASS);
    this._ui.remove_style_class_name(ROOT_CLASS);
    this._ui = null;
  }

  /** Adds or removes the glass class to match the setting. */
  _syncGlass() {
    if (this._settings.get_boolean('translucent-surfaces')) {
      this._ui.add_style_class_name(GLASS_CLASS);
    } else {
      this._ui.remove_style_class_name(GLASS_CLASS);
    }
  }
}
