from cx_Freeze import setup, Executable

base = None    

executables = [Executable("organized.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "<myuzicBackend>",
    options = options,
    version = "<1.0>",
    description = '<Arya is so handsome wow what a great looking guy>',
    executables = executables
)
