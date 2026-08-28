(function () {
  "use strict";

  var storageKey = "useful-code-theme";
  var darkTheme = "modern_dark";
  var lightTheme = "modern_light";

  function readPreference() {
    try {
      var theme = window.localStorage.getItem(storageKey);
      return theme === darkTheme || theme === lightTheme ? theme : null;
    } catch (error) {
      return null;
    }
  }

  function savePreference(theme) {
    try {
      window.localStorage.setItem(storageKey, theme);
    } catch (error) {
      // Persistence is optional when storage is unavailable.
    }
  }

  function applyTheme(theme) {
    if (window.jtd && typeof window.jtd.setTheme === "function") {
      window.jtd.setTheme(theme);
      return;
    }

    var stylesheet = document.querySelector(
      'link[rel="stylesheet"]:not(#jtd-head-nav-stylesheet)'
    );
    if (stylesheet) {
      stylesheet.href = stylesheet.href.replace(
        /just-the-docs-[^/]+\.css$/,
        "just-the-docs-" + theme + ".css"
      );
    }
  }

  function currentTheme(fallback) {
    if (window.jtd && typeof window.jtd.getTheme === "function") {
      var theme = window.jtd.getTheme();
      if (theme === darkTheme || theme === lightTheme) return theme;
    }
    return fallback;
  }

  function updateButton(button, theme) {
    var isLight = theme === lightTheme;
    button.setAttribute("aria-label", isLight ? "Switch to dark theme" : "Switch to light theme");
    button.setAttribute("aria-pressed", String(isLight));
    button.querySelector(".theme-toggle-icon").textContent = isLight ? "☾" : "☀";
    button.querySelector(".theme-toggle-label").textContent = isLight ? "Dark" : "Light";
  }

  function init() {
    var button = document.getElementById("theme-toggle");
    if (!button) return;

    var theme = readPreference() || darkTheme;
    applyTheme(theme);
    updateButton(button, currentTheme(theme));

    button.addEventListener("click", function () {
      theme = currentTheme(theme) === lightTheme ? darkTheme : lightTheme;
      savePreference(theme);
      applyTheme(theme);
      updateButton(button, currentTheme(theme));
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
}());
