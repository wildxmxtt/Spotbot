'use strict';

function addEventListener(listeners, event, listener, type) {
  if (listeners[type] === undefined) {
    listeners[type] = {};
  }
  var typeEvent = listeners[type][event];
  if (typeEvent === undefined) {
    listeners[type][event] = typeEvent = [];
  }

  typeEvent[typeEvent.length] = listener;
}

function removeEventListener(listeners, callback, context) {
  if (listeners && listeners.length) {
    var newListeners = [];
    for (var i = 0; i < listeners.length; i++) {
      var listener = listeners[i];
      if (listener[0] !== callback || (context && context !== listener[1])) {
        newListeners[newListeners.length] = listener;
      }
    }
    return newListeners;
  }
}

function emitEvent(listeners, a1, a2) {
  var listener;

  if (listeners.length === 1) {
    listener = listeners[0];
    if (a2 === undefined) {
      listener[0].call(listener[1], a1);
    } else {
      listener[0].call(listener[1], a1, a2);
    }
    return;
  }

  var length = listeners.length;
  while (--length) {
    listener = listeners[length];
    listener[0].call(listener[1], a1, a2);
  }
}

function EventEmitter() {
  this.onListeners = undefined;
  this.onceListeners = undefined;
}

['on', 'once'].forEach(function (type) {
  EventEmitter.prototype[type] = function (event, callback, context) {
    addEventListener(this, event, [callback, context], type + 'Listeners');
    return this;
  };
});

EventEmitter.prototype.emit = function (event, a1, a2) {
  var listeners;
  var fired = false;

  if (this.onListeners !== undefined) {
    listeners = this.onListeners[event];
    if (listeners) {
      emitEvent(listeners, a1, a2);
      fired = true;
    }
  }

  if (this.onceListeners !== undefined) {
    listeners = this.onceListeners[event];
    if (listeners !== undefined) {
      this.onceListeners[event] = undefined;
      emitEvent(listeners, a1, a2);
      fired = true;
    }
  }

  return fired;
};

EventEmitter.prototype.listeners = function (event) {
  var onListeners = this.onListeners[event];
  var onceListeners = this.onceListeners[event];
  if (onListeners !== undefined) {
    if (onceListeners !== undefined) {
      return Array.concat(onListeners, onceListeners);
    }
    return onListeners;
  }
  if (onceListeners !== undefined) {
    return onceListeners;
  }
};

EventEmitter.prototype.removeListener = function (event, callback, context) {
  if (this.onListeners !== undefined) {
    this.onListeners[event] = removeEventListener(
      this.onListeners[event], callback, context
    );
  }

  if (this.onceListeners !== undefined) {
    this.onceListeners[event] = removeEventListener(
      this.onceListeners[event], callback, context
    );
  }

  return this;
};

EventEmitter.prototype.removeAllListeners = function (event) {
  if (event) {
    if (this.onListeners !== undefined) {
      this.onListeners[event] = undefined;
    }
    if (this.onceListeners !== undefined) {
      this.onceListeners[event] = undefined;
    }
    return;
  }

  this.onListeners = this.onceListeners = undefined;

  return this;
};

EventEmitter.prototype.addListener = EventEmitter.prototype.on;

EventEmitter.prototype.setMaxListeners = function () {
  return this;
};

EventEmitter.EventEmitter = EventEmitter;

module.exports = EventEmitter;

