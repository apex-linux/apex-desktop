// The top bar pieces that stock GNOME Shell does not draw
// (shell-top-bar-and-dock.md): the Apex diamond in Activities, the focused
// app name after it, and the solid bar while a window is maximised.

import Clutter from 'gi://Clutter';
import Graphene from 'gi://Graphene';
import Shell from 'gi://Shell';
import St from 'gi://St';
import * as Main from 'resource:///org/gnome/shell/ui/main.js';

// Shown when no app has focus (Desktop.dc.html:138).
const NO_APP_LABEL = 'Desktop';
// The panel carries this class while a maximised window covers it; the
// stylesheet then draws --bar-solid even when glass is on.
const SOLID_CLASS = 'apex-solid-bar';

/** Adds the diamond, the focused app label and the solid bar state. */
export class TopBar {
  /**
   * @param {WindowWatcher} watcher tells whether a window is maximised
   */
  constructor(watcher) {
    this._watcher = watcher;
    this._addDiamond();
    this._addFocusLabel();
    this._watcher.connectObject('changed', () => this._syncSolid(), this);
    this._syncSolid();
  }

  /** Removes everything the top bar added. */
  destroy() {
    this._watcher.disconnectObject(this);
    Main.panel.remove_style_class_name(SOLID_CLASS);
    Shell.WindowTracker.get_default().disconnectObject(this);
    Main.overview.disconnectObject(this);
    this._focusLabel.destroy();
    this._removeDiamond();
  }

  /** Puts a 10 px rotated square before the workspace pills. */
  _addDiamond() {
    const activities = Main.panel.statusArea.activities;
    this._indicators = activities.get_first_child();
    this._diamond = new St.Widget({
      style_class: 'apex-activities-diamond',
      y_align: Clutter.ActorAlign.CENTER,
      pivot_point: new Graphene.Point({x: 0.5, y: 0.5}),
      rotation_angle_z: 45,
    });
    this._activitiesBox = new St.BoxLayout({
      style_class: 'apex-activities-box',
      y_align: Clutter.ActorAlign.CENTER,
    });
    activities.remove_child(this._indicators);
    this._activitiesBox.add_child(this._diamond);
    this._activitiesBox.add_child(this._indicators);
    activities.add_child(this._activitiesBox);
  }

  /** Gives Activities back its own child. */
  _removeDiamond() {
    const activities = Main.panel.statusArea.activities;
    this._activitiesBox.remove_child(this._indicators);
    activities.remove_child(this._activitiesBox);
    activities.add_child(this._indicators);
    this._activitiesBox.destroy();
    this._activitiesBox = null;
    this._diamond = null;
    this._indicators = null;
  }

  /** Shows the focused app's name, or "Desktop", after Activities. */
  _addFocusLabel() {
    this._focusLabel = new St.Label({
      style_class: 'apex-focus-label',
      y_align: Clutter.ActorAlign.CENTER,
    });
    const activities = Main.panel.statusArea.activities;
    activities.container.get_parent().insert_child_above(
        this._focusLabel, activities.container);
    Shell.WindowTracker.get_default().connectObject(
        'notify::focus-app', () => this._syncFocusLabel(), this);
    // The overview draws no focused label (Overview.dc.html:30-36).
    Main.overview.connectObject(
        'showing', () => this._focusLabel.hide(),
        'hiding', () => this._focusLabel.show(),
        this);
    this._syncFocusLabel();
    // 'showing' fires before extensions are enabled at session start.
    this._focusLabel.visible = !Main.overview.visible;
  }

  /** Updates the label text from the window tracker. */
  _syncFocusLabel() {
    const app = Shell.WindowTracker.get_default().focus_app;
    this._focusLabel.text = app ? app.get_name() : NO_APP_LABEL;
  }

  /** Marks the panel solid while a window is maximised. */
  _syncSolid() {
    if (this._watcher.maximized) {
      Main.panel.add_style_class_name(SOLID_CLASS);
    } else {
      Main.panel.remove_style_class_name(SOLID_CLASS);
    }
  }
}
