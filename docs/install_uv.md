# Installing uv on Windows

The `uv` command is not currently installed on your system. Here are the installation options:

## Option 1: PowerShell Installer (Recommended)

Run this command in PowerShell (as Administrator if needed):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

This will:
- Download and install `uv` to `%USERPROFILE%\.cargo\bin\`
- Add it to your PATH automatically

**After installation**, you may need to:
1. Close and reopen your terminal/PowerShell window
2. Or refresh your PATH: `$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")`

## Option 2: Using pip (if you have Python)

If you have Python installed, you can install `uv` via pip:

```powershell
pip install uv
```

## Option 3: Manual Installation

1. Download the latest Windows release from: https://github.com/astral-sh/uv/releases
2. Extract `uv.exe` to a folder (e.g., `C:\tools\uv\`)
3. Add that folder to your PATH:
   - Open System Properties → Environment Variables
   - Edit the `Path` variable
   - Add the folder containing `uv.exe`

## Verify Installation

After installation, verify it works:

```powershell
uv --version
```

You should see something like: `uv 0.10.0` (or similar version number)

## Then Initialize Your Project

Once `uv` is installed, you can run:

```powershell
cd "D:\FAST TRACK CODE\project-chimera"
uv init
```

This will set up your Python project with `uv`'s project structure.
