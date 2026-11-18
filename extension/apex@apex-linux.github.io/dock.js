// The Apex dock (shell-top-bar-and-dock.md): the stock Dash, always shown
// at the bottom of the primary monitor with a fixed icon size, hidden
// behind maximised windows and revealed by pushing against the bottom
// edge. The route (this subclass rather than a Dash to Dock fork) is
// OQ-09.

import Clutter from 'gi://Clutter';
import GLib from 'gi://GLib';
import GObject from 'gi://GObject';
import Meta from 'gi://Meta';
import Shell from 'gi://Shell';
import St from 'gi://St';
import * as Dash from 'resource:///org/gnome/shell/ui/dash.js';
import * as Layout from 'resource:///org/gnome/shell/ui/layout.js';
import * as Main from 'resource:///org/gnome/shell/ui/main.js';

// Medium dock icons (tokens.json spacing.fixed.dockIcon).
const ICON_SIZE = 54;
// Gap between the dock and the bottom edge (spacing.fixed.dockBottomOffset).
const BOTTOM_OFFSET = 10;
// Hide transform: below the edge by its own height plus 12 px
// (Desktop.dc.html:142-143), over 250 ms.
const HIDE_EXTRA = 12;
const HIDE_TIME = 250;
// Not drawn (OQ-09 question 3); Dash to Dock's defaults.
const PRESSURE_THRESHOLD = 100;
const PRESSURE_TIMEOUT = 1000;
const HIDE_DELAY = 500;

/** The stock Dash with a fixed icon size. */
const ApexDash = GObject.registerClass(
    class ApexDash extends Dash.Dash {
      /** Keeps every icon at ICON_SIZE instead of fitting the space. */
      _adjustIconSize() {
        const items = this._box.get_children().filter((actor) =>
          actor.child?._delegate?.icon && !actor.animatingOut);
        items.push(this._showAppsIcon);
        if (this.iconSize !== ICON_SIZE) {
          this.iconSize = ICON_SIZE;
          this.emit('icon-size-changed');
        }
        for (const item of items) {
          item.child._delegate.icon.setIconSize(ICON_SIZE);
        }
      }
    });

/** Places, shows and hides the dock. */
export class Dock {
  /**
   * @param {WindowWatcher} watcher tells whether a window is maximised
   */
  constructor(watcher) {
    this._watcher = watcher;
    this._revealed = false;
    this._hideId = 0;
    this._placeLater = 0;

    this._dash = new ApexDash();
    this._container = new St.Bin({
      name: 'apexDock',
      child: this._dash,
      reactive: true,
      track_hover: true,
    });
    this._container.accessible_name = 'Dock';
    Main.layoutManager.addChrome(this._container, {
      affectsStruts: false,
      trackFullscreen: true,
    });

    this._dash.showAppsButton.connectObject(
        'notify::checked', () => this._onShowApps(), this);
    this._container.connectObject(
        'notify::width', () => this._queuePlace(),
        'notify::height', () => this._queuePlace(),
        'notify::hover', () => this._onHover(),
        this);
    Main.layoutManager.connectObject(
        'monitors-changed', () => this._onMonitorsChanged(), this);
    Main.overview.connectObject(
        'showing', () => this._container.hide(),
        'hidden', () => this._onOverviewHidden(),
        this);
    this._watcher.connectObject('changed', () => this._sync(), this);

    this._pressure = new Layout.PressureBarrier(
        PRESSURE_THRESHOLD, PRESSURE_TIMEOUT, Shell.ActionMode.NORMAL);
    this._pressure.connectObject('trigger', () => this._reveal(), this);
    this._onMonitorsChanged();
    // The session starts in the overview, which emits 'showing' before
    // extensions are enabled.
    if (Main.overview.visible) {
      this._container.hide();
    }
  }

  /** Removes the dock and its barrier. */
  destroy() {
    this._clearHide();
    if (this._placeLater) {
      global.compositor.get_laters().remove(this._placeLater);
      this._placeLater = 0;
    }
    this._watcher.disconnectObject(this);
    Main.layoutManager.disconnectObject(this);
    Main.overview.disconnectObject(this);
    this._removeBarrier();
    this._pressure.destroy();
    this._pressure = null;
    this._container.destroy();
    this._container = null;
    this._dash = null;
  }

  /**
   * Re-centres the dock before the next redraw. The size notifications
   * arrive during allocation; moving the dock there would leave it needing
   * another allocation after layout, and Clutter logs "Can't update stage
   * views actor apexDock".
   */
  _queuePlace() {
    if (this._placeLater) {
      return;
    }
    this._placeLater = global.compositor.get_laters().add(
        Meta.LaterType.BEFORE_REDRAW, () => {
          this._placeLater = 0;
          this._place();
          return GLib.SOURCE_REMOVE;
        });
  }

  /** Centres the dock above the bottom edge of the primary monitor. */
  _place() {
    const monitor = Main.layoutManager.primaryMonitor;
    if (!monitor) {
      return;
    }
    const [width, height] = this._container.get_size();
    this._container.set_position(
        monitor.x + Math.floor((monitor.width - width) / 2),
        monitor.y + monitor.height - height - BOTTOM_OFFSET);
  }

  /** Moves the dock and its barrier to the new primary monitor. */
  _onMonitorsChanged() {
    const monitor = Main.layoutManager.primaryMonitor;
    if (!monitor) {
      return;
    }
    this._dash.setMaxSize(monitor.width, monitor.height);
    this._place();
    this._removeBarrier();
    this._barrier = new Meta.Barrier({
      backend: global.backend,
      x1: monitor.x,
      x2: monitor.x + monitor.width,
      y1: monitor.y + monitor.height,
      y2: monitor.y + monitor.height,
      directions: Meta.BarrierDirection.NEGATIVE_Y,
    });
    this._pressure.addBarrier(this._barrier);
    this._sync();
  }

  /** Removes the bottom-edge barrier, if there is one. */
  _removeBarrier() {
    if (!this._barrier) {
      return;
    }
    this._pressure.removeBarrier(this._barrier);
    this._barrier.destroy();
    this._barrier = null;
  }

  /** Opens the app grid from the Show Apps button. */
  _onShowApps() {
    if (this._dash.showAppsButton.checked) {
      Main.overview.showApps();
    }
  }

  /** Shows the dock again after the overview, with Show Apps unchecked. */
  _onOverviewHidden() {
    this._dash.showAppsButton.checked = false;
    this._container.show();
    this._sync();
  }

  /** Shows the dock over a maximised window after edge pressure. */
  _reveal() {
    this._revealed = true;
    this._clearHide();
    this._sync();
  }

  /** Hides a revealed dock again once the pointer has left it. */
  _onHover() {
    this._clearHide();
    if (this._container.hover || !this._revealed) {
      return;
    }
    this._hideId = GLib.timeout_add(GLib.PRIORITY_DEFAULT, HIDE_DELAY, () => {
      this._hideId = 0;
      this._revealed = false;
      this._sync();
      return GLib.SOURCE_REMOVE;
    });
  }

  /** Cancels a pending hide. */
  _clearHide() {
    if (this._hideId) {
      GLib.source_remove(this._hideId);
      this._hideId = 0;
    }
  }

  /** Slides the dock in or out to match the windows and the pointer. */
  _sync() {
    const hidden = this._watcher.maximized && !this._revealed &&
      !this._container.hover;
    const offset = hidden ? this._container.height + HIDE_EXTRA +
      BOTTOM_OFFSET : 0;
    // An animation needs the actor's stage view, which an actor that is
    // hidden or not yet allocated (just shown after the overview) has not
    // got: Clutter logs "Can't update stage views". Jump there instead.
    if (!this._container.visible || !this._container.has_allocation()) {
      this._container.remove_transition('translation-y');
      this._container.translation_y = offset;
      return;
    }
    this._container.ease({
      translation_y: offset,
      duration: HIDE_TIME,
      mode: Clutter.AnimationMode.EASE_OUT_QUAD,
    });
  }
}
