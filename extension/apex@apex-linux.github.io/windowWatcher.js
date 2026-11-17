// Tells the top bar and the dock whether a maximised window covers the
// primary monitor on the active workspace.

import GLib from 'gi://GLib';
import * as Signals from 'resource:///org/gnome/shell/misc/signals.js';
import * as Main from 'resource:///org/gnome/shell/ui/main.js';

/**
 * Emits 'changed' when `maximized` flips. Changes are batched in an idle
 * callback, because one user action fires several window signals.
 */
export class WindowWatcher extends Signals.EventEmitter {
  /** Starts watching windows. */
  constructor() {
    super();
    this.maximized = false;
    this._idleId = 0;
    const queue = () => this._queue();
    global.display.connectObject('restacked', queue, this);
    global.window_manager.connectObject(
        'size-changed', queue,
        'minimize', queue,
        'unminimize', queue,
        'map', queue,
        'destroy', queue,
        'switch-workspace', queue,
        this);
    global.workspace_manager.connectObject(
        'active-workspace-changed', queue, this);
    Main.layoutManager.connectObject('monitors-changed', queue, this);
    this._update();
  }

  /** Stops watching. */
  destroy() {
    if (this._idleId) {
      GLib.source_remove(this._idleId);
      this._idleId = 0;
    }
    global.display.disconnectObject(this);
    global.window_manager.disconnectObject(this);
    global.workspace_manager.disconnectObject(this);
    Main.layoutManager.disconnectObject(this);
  }

  /** Schedules one update for the current burst of window signals. */
  _queue() {
    if (this._idleId) {
      return;
    }
    this._idleId = GLib.idle_add(GLib.PRIORITY_DEFAULT_IDLE, () => {
      this._idleId = 0;
      this._update();
      return GLib.SOURCE_REMOVE;
    });
  }

  /** Recomputes `maximized` and emits 'changed' when it differs. */
  _update() {
    const primary = Main.layoutManager.primaryIndex;
    const workspace = global.workspace_manager.get_active_workspace();
    const maximized = workspace.list_windows().some((window) =>
      window.get_monitor() === primary &&
        !window.minimized &&
        window.showing_on_its_workspace() &&
        window.is_maximized());
    if (maximized !== this.maximized) {
      this.maximized = maximized;
      this.emit('changed');
    }
  }
}
