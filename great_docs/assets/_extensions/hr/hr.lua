-- hr.lua — Quarto shortcode for decorative horizontal rules
--
-- Usage in .qmd files:
--
--   {{< hr >}}
--   {{< hr style="dashed" color="sky" >}}
--   {{< hr style="dotted" thickness="3px" width="50%" align="center" >}}
--   {{< hr text="§" >}}
--   {{< hr text="Continue Reading" style="solid" color="#6366f1" >}}
--   {{< hr preset="gradient-shimmer" >}}
--   {{< hr preset="fade" width="60%" >}}
--
-- Pure Lua implementation — no Python helper needed.
-- All styling is handled via CSS classes in great-docs.scss.

local function kwarg_str(kwargs, key)
    local raw = kwargs[key]
    if raw == nil then return "" end
    local s = pandoc.utils.stringify(raw)
    return s or ""
end

-- Named palette colors that map to CSS custom properties
local PALETTE_COLORS = {
    sky = true,
    peach = true,
    prism = true,
    lilac = true,
    slate = true,
    honey = true,
    dusk = true,
    mint = true,
    accent = true,
}

-- Valid presets
local PRESETS = {
    ["gradient-shimmer"] = true,
    ["gradient-static"] = true,
    ["fade"] = true,
    ["fade-edges"] = true,
    ["dots"] = true,
    ["diamond"] = true,
    ["ornament"] = true,
    ["wave"] = true,
    ["double-line"] = true,
}

-- Valid line styles
local STYLES = {
    solid = true, dotted = true, dashed = true, double = true,
}

-- Named thickness values
local THICKNESS_MAP = {
    thin = "1px",
    medium = "2px",
    thick = "4px",
}

-- Named spacing values
local SPACING_MAP = {
    compact = "1rem",
    normal = "2rem",
    spacious = "4rem",
}

return {
    ["hr"] = function(args, kwargs)
        local preset = kwarg_str(kwargs, "preset")
        local style = kwarg_str(kwargs, "style")
        local color = kwarg_str(kwargs, "color")
        local thickness = kwarg_str(kwargs, "thickness")
        local width = kwarg_str(kwargs, "width")
        local align = kwarg_str(kwargs, "align")
        local text = kwarg_str(kwargs, "text")
        local text_color = kwarg_str(kwargs, "text-color")
        local text_size = kwarg_str(kwargs, "text-size")
        local spacing = kwarg_str(kwargs, "spacing")

        -- Build CSS classes
        local classes = { "gd-hr" }

        if preset ~= "" and PRESETS[preset] then
            table.insert(classes, "gd-hr--" .. preset)
        end

        if style ~= "" and STYLES[style] then
            table.insert(classes, "gd-hr--" .. style)
        end

        if align == "left" then
            table.insert(classes, "gd-hr--left")
        elseif align == "right" then
            table.insert(classes, "gd-hr--right")
        end

        -- Build inline styles for dynamic values
        local inline_styles = {}

        -- Color: palette name → CSS var, otherwise raw CSS color
        if color ~= "" then
            if PALETTE_COLORS[color] then
                table.insert(inline_styles,
                    "--gd-hr-color: var(--gd-palette-" .. color .. ", var(--gd-accent, #6366f1))")
            else
                table.insert(inline_styles, "--gd-hr-color: " .. color)
            end
        end

        -- Thickness
        if thickness ~= "" then
            local resolved = THICKNESS_MAP[thickness] or thickness
            table.insert(inline_styles, "--gd-hr-thickness: " .. resolved)
        end

        -- Width
        if width ~= "" then
            if width == "full" then
                width = "100%"
            end
            table.insert(inline_styles, "--gd-hr-width: " .. width)
        end

        -- Spacing
        if spacing ~= "" then
            local resolved = SPACING_MAP[spacing] or spacing
            table.insert(inline_styles, "--gd-hr-spacing: " .. resolved)
        end

        local style_attr = ""
        if #inline_styles > 0 then
            style_attr = ' style="' .. table.concat(inline_styles, "; ") .. '"'
        end

        local class_attr = table.concat(classes, " ")

        -- If there's embedded text, use the flex wrapper structure
        if text ~= "" then
            local text_classes = { "gd-hr-text" }
            if text_size == "sm" then
                table.insert(text_classes, "gd-hr-text--sm")
            elseif text_size == "lg" then
                table.insert(text_classes, "gd-hr-text--lg")
            end

            local text_style = ""
            if text_color ~= "" then
                text_style = ' style="color: ' .. text_color .. '"'
            end

            local html = '<div class="' .. class_attr .. ' gd-hr--with-text"' .. style_attr .. '>'
                .. '<span class="gd-hr-line"></span>'
                .. '<span class="' .. table.concat(text_classes, " ") .. '"' .. text_style .. '>'
                .. text
                .. '</span>'
                .. '<span class="gd-hr-line"></span>'
                .. '</div>'

            return pandoc.RawBlock("html", html)
        end

        -- Simple <hr> element
        local html = '<hr class="' .. class_attr .. '"' .. style_attr .. '>'
        return pandoc.RawBlock("html", html)
    end,
}
