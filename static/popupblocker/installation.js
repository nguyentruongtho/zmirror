window['isRoot'] = true;
unsafeWindow = window;
unsafeWindow.window = window;
(function (_window) {
    if (!_window.localStorage) {
        console.log('LocalStorage is required');
        return;
    }

    if (!_window.GM_getValue) {
        _window.GM_getValue = function (name, default_val) {
            let preset = _window.localStorage.getItem(name);
            return preset != null ? preset : default_val;
        };

        _window.GM_setValue = function (name, value) {
            _window.localStorage.setItem(name, value);
        }

        _window.GM_deleteValue = function (name) {
            _window.localStorage.removeItem(name);
        }

        _window.GM_listValues = function() {
            return Object.keys(localStorage);
        }

        _window.GM_getResourceURL = function (resourceName) {
            if (resourceName.startsWith('./')) {
                resourceName = resourceName.substring(2);
            }
            return 'https://userscripts.adtidy.org/release/popup-blocker/2.5/' + resourceName;
        }
    }
})(unsafeWindow);
document.addEventListener("DOMContentLoaded", function(event) {
    setTimeout(function() {
        const nav = document.querySelector('nav.MuiTypography-root');
        if (nav && nav.nextSibling) {
            if (nav.nextSibling.nextSibling) {
                nav.nextSibling.nextSibling.remove();
            }
            nav.nextSibling.remove();
        }
    }, 5000);
})