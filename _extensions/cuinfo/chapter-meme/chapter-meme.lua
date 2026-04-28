-- chapter-meme: read each chapter's `meme:` YAML frontmatter, hash-check
-- against a sidecar, invoke scripts/generate_chapter_meme.py to produce
-- graphics/memes/<slug>.png if missing or stale, and emit a {.column-margin}
-- block referencing the PNG.
--
-- The shortcode takes no args. Editorial content lives in the chapter's
-- frontmatter:
--
--   meme:
--     template: fine
--     lines:
--       - ""
--       - "MY CODE IS ON FIRE BUT THIS IS FINE"
--     alt: "My code is on fire but this is fine."
--     rationale: "humor — ..."   # optional, source-only

local function file_exists(path)
  local f = io.open(path, "r")
  if f then f:close(); return true end
  return false
end

local function read_text(path)
  local f = io.open(path, "r")
  if not f then return "" end
  local s = f:read("*a") or ""
  f:close()
  return s
end

local function write_text(path, s)
  local f = io.open(path, "w")
  if not f then return false end
  f:write(s)
  f:close()
  return true
end

local function basename_no_ext(path)
  local name = path:match("([^/\\]+)$") or path
  return (name:gsub("%.qmd$", ""))
end

local function shell_escape(s)
  return "'" .. s:gsub("'", "'\\''") .. "'"
end

local function hash_hex(s)
  -- pandoc.utils.sha1 is reliably available in Quarto's Lua runtime.
  return pandoc.utils.sha1(s):sub(1, 16)
end

return {
  ["chapter-meme"] = function(args, kwargs, meta)
    local m = meta and meta.meme
    if not m or not m.template or not m.lines then
      return pandoc.RawBlock(
        "html",
        "<!-- chapter-meme: no `meme:` frontmatter, skipping -->"
      )
    end

    local template = pandoc.utils.stringify(m.template)
    local alt = pandoc.utils.stringify(m.alt or "Chapter meme")
    -- Default to 192pt; matches the generator script's default. Folding the
    -- value into the spec hash below means changing the default here (or
    -- overriding per-chapter via `meme.fontsize:`) invalidates the cached PNG.
    local fontsize = m.fontsize and pandoc.utils.stringify(m.fontsize) or "192"
    local lines = {}
    for _, v in ipairs(m.lines) do
      table.insert(lines, pandoc.utils.stringify(v))
    end

    local input = ""
    if quarto and quarto.doc and quarto.doc.input_file then
      input = quarto.doc.input_file
    end
    local slug = basename_no_ext(input)
    if slug == "" then
      return pandoc.RawBlock(
        "html",
        "<!-- chapter-meme: cannot resolve chapter slug from input file -->"
      )
    end

    -- Quarto runs each render with cwd set to the chapter's directory, so
    -- shell-outs and file checks need absolute paths anchored at the project
    -- root. quarto.project.directory is the standard API; the gsub fallback
    -- assumes parts/<part>/<chapter>.qmd.
    local project_root = (quarto.project and quarto.project.directory) or ""
    if project_root == "" then
      project_root = input:gsub("/parts/[^/]+/[^/]+%.qmd$", "")
    end

    local png_abs = project_root .. "/graphics/memes/" .. slug .. ".png"
    local spec_abs = project_root .. "/graphics/memes/" .. slug .. ".spec"
    local script_abs = project_root .. "/scripts/generate_chapter_meme.py"

    local spec_payload = template .. "\n" .. fontsize .. "\n" .. table.concat(lines, "\n")
    local hash = hash_hex(spec_payload)
    local existing_hash = file_exists(spec_abs) and read_text(spec_abs) or ""

    if (not file_exists(png_abs)) or existing_hash ~= hash then
      local cmd = "python " .. shell_escape(script_abs) .. " "
        .. "--template " .. shell_escape(template) .. " "
        .. "--fontsize " .. shell_escape(fontsize) .. " "
      for _, line in ipairs(lines) do
        cmd = cmd .. "--line " .. shell_escape(line) .. " "
      end
      cmd = cmd .. "--out " .. shell_escape(png_abs) .. " 1>&2"
      local ok = os.execute(cmd)
      if ok and file_exists(png_abs) then
        write_text(spec_abs, hash)
      else
        io.stderr:write(
          "chapter-meme: failed to generate " .. png_abs .. "\n"
        )
        return pandoc.RawBlock(
          "html",
          "<!-- chapter-meme: generator failed for slug " .. slug .. " -->"
        )
      end
    end

    -- Build the Pandoc AST directly. The image path stays relative to the
    -- source file: every chapter lives at parts/<part>/<chapter>.qmd, so
    -- ../../ is the right prefix back to graphics/. Returning a constructed
    -- Div lets Quarto wire up the column-margin layout and HTML alt text.
    local img = pandoc.Image(
      {pandoc.Str("")},
      "../../graphics/memes/" .. slug .. ".png",
      ""
    )
    img.attributes["fig-alt"] = alt
    local para = pandoc.Para({img})
    return pandoc.Div({para}, pandoc.Attr("", {"column-margin"}, {}))
  end,
}
