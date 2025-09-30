
#   Terminal Database Explorer

A **curses-based terminal tool** for exploring `.db` files directly from your projects.  
Built for developers who want a lightweight way to inspect SQLite databases without leaving their editor.  
Integrates seamlessly with **Neovim** via ToggleTerm + WhichKey, so you can open a floating DB viewer with a single keybind.

---

##  ✨ Features
- 🔍 **Auto-discovery**: Scans the current file’s directory for `.db` files  
- 📑 **Table browser**: Navigate tables interactively with arrow keys  
- 📊 **Row viewer**: Scroll through rows in a clean terminal interface  
- ⌨️ **Keyboard-driven**:  
  - `↑/↓` to move  
  - `Enter` to select  
  - `q` to quit  
- 🖥 **Neovim-ready**: Trigger the viewer in a floating terminal from inside your project  

---

##  📦 Installation
Clone this repo:

```bash
git clone https://github.com/yourusername/terminal-database-scanner.git
cd terminal-database-scanner
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Make the script executable:

```bash
chmod +x db_viewer.py
```

---

##  ⚡Neovim Integration

Add this snippet to your Neovim config:

```lua
local function open_db_viewer()
  local home = vim.fn.expand("~")
  local file_dir = vim.fn.expand("%:p:h")
  local venv_activate = home .. "/Documents/GitHub/terminal-database-scanner/venv/bin/activate"
  local script_path   = home .. "/Documents/GitHub/terminal-database-scanner/db_viewer.py"
  local cmd = "bash -c 'source " .. venv_activate .. " && python " .. script_path .. " " .. file_dir .. "'"

  require("toggleterm.terminal").Terminal
      :new({ cmd = cmd, direction = "float", hidden = true })
      :toggle()
end

vim.keymap.set("n", "<leader>db", open_db_viewer, { desc = "Open DB Viewer" })
```
