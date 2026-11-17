// The Apex Shell extension. Its generated stylesheet themes the shell; this
// file wires the parts that need code: the top bar additions and the dock.

import {Extension} from 'resource:///org/gnome/shell/extensions/extension.js';
import * as Main from 'resource:///org/gnome/shell/ui/main.js';

import {Dock} from './dock.js';
import {TopBar} from './topBar.js';
import {WindowWatcher} from './windowWatcher.js';

// Every rule in stylesheet-*.css is scoped under this class.
const ROOT_CLASS = 'apex-shell';
// Added when translucent-surfaces is on; selects the glass tints.
const GLASS_CLASS = 'apex-glass';

/** Applies the Apex look to the running shell. */
export default class ApexExtension extends Extension {
  /** Scopes the stylesheet and starts the top bar and dock. */
  enable() {
    this._ui = Main.layoutManager.uiGroup;
    this._ui.add_style_class_name(ROOT_CLASS);
    this._settings = this.getSettings();
    this._settings.connectObject(
        'changed::translucent-surfaces', () => this._syncGlass(), this);
    this._syncGlass();
    // The extension stays enabled on the lock screen so the stylesheet
    // applies there; the top bar additions and the dock do not.
    Main.sessionMode.connectObject('updated', () => this._syncMode(), this);
    this._syncMode();
  }

  /** Puts the shell back the way it was. */
  disable() {
    Main.sessionMode.disconnectObject(this);
    this._stopSession();
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

  /** Runs the top bar and dock in the user session only. */
  _syncMode() {
    if (Main.sessionMode.isLocked) {
      this._stopSession();
    } else if (!this._watcher) {
      this._watcher = new WindowWatcher();
      this._topBar = new TopBar(this._watcher);
      this._dock = new Dock(this._watcher);
    }
  }

  /** Destroys the top bar and dock, if they run. */
  _stopSession() {
    this._dock?.destroy();
    this._topBar?.destroy();
    this._watcher?.destroy();
    this._dock = null;
    this._topBar = null;
    this._watcher = null;
  }
}
