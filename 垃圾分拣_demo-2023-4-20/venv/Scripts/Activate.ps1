function global:deactivate ([switch]$NonDestructive) {
    # Revert to original values
    if (Test-Path function:_OLD_VIRTUAL_PROMPT) {
        copy-item function:_OLD_VIRTUAL_PROMPT function:prompt
        remove-item function:_OLD_VIRTUAL_PROMPT
    }

    if (Test-Path env:_OLD_VIRTUAL_PYTHONHOME) {
        copy-item env:_OLD_VIRTUAL_PYTHONHOME env:PYTHONHOME
        remove-item env:_OLD_VIRTUAL_PYTHONHOME
    }

    if (Test-Path env:_OLD_VIRTUAL_PATH) {
        copy-item env:_OLD_VIRTUAL_PATH env:PATH
        remove-item env:_OLD_VIRTUAL_PATH
    }

    if (Test-Path env:VIRTUAL_ENV) {
        remove-item env:VIRTUAL_ENV
    }

    if (!$NonDestructive) {
        # Self destruct!
        remove-item function:deactivate
    }
}

deactivate -nondestructive

$env:VIRTUAL_ENV="D:\1、硕博工作\固废智能检测\分拣垃圾流水线\2023-4-20 垃圾分拣链软件\垃圾分拣_demo-2023-4-20\venv"

if (! $env:VIRTUAL_ENV_DISABLE_PROMPT) {
    # Set the prompt to include the env name
    # Make sure _OLD_VIRTUAL_PROMPT is global
    function global:_OLD_VIRTUAL_PROMPT {""}
    copy-item function:prompt function:_OLD_VIRTUAL_PROMPT
    function global:prompt {
        Write-Host -NoNewline -ForegroundColor Green '(venv) '
        _OLD_VIRTUAL_PROMPT
    }
}

# Clear PYTHONHOME
if (Test-Path env:PYTHONHOME) {
    copy-item env:PYTHONHOME env:_OLD_VIRTUAL_PYTHONHOME
    remove-item env:PYTHONHOME
}

# Add the venv to the PATH
copy-item env:PATH env:_OLD_VIRTUAL_PATH
$env:PATH = "$env:VIRTUAL_ENV\Scripts;$env:PATH"
