-- keys.lua — Quarto shortcode for styled keyboard key caps
--
-- Usage in .qmd files:
--
--   {{< keys "Esc" >}}
--   {{< keys "Ctrl" >}}+{{< keys "Shift" >}}+{{< keys "P" >}}
--   {{< keys shortcut="Ctrl+Shift+P" >}}
--   {{< keys shortcut="Ctrl+Shift+P" platform="mac" >}}
--   {{< keys shortcut="Cmd+K" platform="win" >}}
--
-- Pure Lua implementation — no Python helper needed.
-- All styling is handled via CSS classes in great-docs.scss.
--
-- NOTE: Quarto ships a built-in {{< kbd >}} shortcode that renders plain-text
-- shortcuts with per-OS keyword args (mac=, win=, linux=). This extension is
-- intentionally named "keys" to avoid conflict. It provides *styled* key caps
-- with a 3D border effect and macOS symbol translation.

local function kwarg_str(kwargs, key)
    local raw = kwargs[key]
    if raw == nil then return "" end
    local s = pandoc.utils.stringify(raw)
    return s or ""
end

-- Map generic key names to macOS symbols
local MAC_KEYS = {
    ctrl       = "⌃",
    control    = "⌃",
    alt        = "⌥",
    option     = "⌥",
    opt        = "⌥",
    shift      = "⇧",
    cmd        = "⌘",
    command    = "⌘",
    meta       = "⌘",
    super      = "⌘",
    enter      = "⏎",
    ["return"] = "⏎",
    tab        = "⇥",
    delete     = "⌫",
    backspace  = "⌫",
    esc        = "⎋",
    escape     = "⎋",
    space      = "␣",
    up         = "▲",
    down       = "▼",
    left       = "◀",
    right      = "▶",
}

-- Map macOS-specific key names to Windows/generic equivalents
local WIN_KEYS = {
    cmd     = "Ctrl",
    command = "Ctrl",
    meta    = "Win",
    super   = "Win",
    option  = "Alt",
    opt     = "Alt",
}

-- Tooltip text for symbolic key labels (shown on hover)
local TOOLTIPS = {
    ["⌃"] = "Control",
    ["⌥"] = "Option",
    ["⇧"] = "Shift",
    ["⌘"] = "Command",
    ["⏎"] = "Enter",
    ["⇥"] = "Tab",
    ["⌫"] = "Delete",
    ["⎋"] = "Escape",
    ["␣"] = "Space",
    ["▲"] = "Up",
    ["▼"] = "Down",
    ["◀"] = "Left",
    ["▶"] = "Right",
}

--- Escape HTML special characters.
local function escape_html(s)
    return s:gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;"):gsub('"', "&quot;")
end

--- Check whether a label is a function key (F1–F20).
local function is_fn_key(label)
    return label:match("^[Ff]%d%d?$") ~= nil
end

--- Render a single key label into an HTML <kbd> element.
--- @param label string  The display text for the key
--- @return string  HTML string
local function render_key(label)
    local cls = "gd-keys"
    if is_fn_key(label) then
        cls = "gd-keys gd-keys-fn"
    end
    local tooltip = TOOLTIPS[label]
    if tooltip then
        return '<kbd class="' .. cls .. '" title="' .. tooltip .. '">' .. escape_html(label) .. '</kbd>'
    end
    return '<kbd class="' .. cls .. '">' .. escape_html(label) .. '</kbd>'
end

--- Translate a single key name for a given platform.
--- @param key string   Raw key name (e.g. "Ctrl", "Cmd")
--- @param platform string  "mac" | "win" | ""
--- @return string  Display label for the key
local function translate_key(key, platform)
    local lower = key:lower()

    if platform == "mac" then
        local sym = MAC_KEYS[lower]
        if sym then return sym end
    elseif platform == "win" then
        local mapped = WIN_KEYS[lower]
        if mapped then return mapped end
    end

    -- For keys that aren't platform-special, title-case single-char keys
    -- and preserve the original casing for multi-char keys
    if #key == 1 then
        return key:upper()
    end
    return key
end

--- Split a shortcut string on "+" while respecting a literal "+" key.
--- E.g. "Ctrl+Shift++" => {"Ctrl", "Shift", "+"}
--- @param shortcut string
--- @return table  List of key names
local function split_shortcut(shortcut)
    local keys = {}
    local i = 1
    local len = #shortcut

    while i <= len do
        -- Find next "+"
        local j = shortcut:find("+", i, true)
        if j == nil then
            -- Last segment
            local seg = shortcut:sub(i)
            if seg ~= "" then
                table.insert(keys, seg)
            end
            break
        end

        local seg = shortcut:sub(i, j - 1)
        if seg == "" then
            -- The "+" itself is the key (e.g. at start, or after another "+")
            table.insert(keys, "+")
            i = j + 1
        else
            table.insert(keys, seg)
            i = j + 1
        end
    end

    return keys
end

return {
    ["keys"] = function(args, kwargs)
        local shortcut = kwarg_str(kwargs, "shortcut")
        local platform = kwarg_str(kwargs, "platform")

        -- Normalise platform
        if platform ~= "" then
            platform = platform:lower()
            if platform ~= "mac" and platform ~= "win" then
                platform = ""
            end
        end

        -- Single-key mode: positional arg or key="" kwarg
        if shortcut == "" then
            local key = kwarg_str(kwargs, "key")
            if key == "" and #args > 0 then
                key = pandoc.utils.stringify(args[1])
            end

            if key == "" then
                return pandoc.RawInline(
                    "html",
                    "<!-- keys shortcode error: missing key or shortcut -->"
                )
            end

            local label = translate_key(key, platform)
            return pandoc.RawInline("html", render_key(label))
        end

        -- Shortcut combo mode: split on "+" and render each key
        local keys = split_shortcut(shortcut)
        local parts = {}
        for _, k in ipairs(keys) do
            local label = translate_key(k, platform)
            table.insert(parts, render_key(label))
        end

        local separator = '<span class="gd-keys-sep">+</span>'
        return pandoc.RawInline("html", table.concat(parts, separator))
    end
}
