import os
import subprocess
import tempfile
from cudatext import *
from cuda_fmt import get_config_filename

def do_format(source_text):

    fn_ini = get_config_filename('Embarcadero Format')
    opt_formater_dir = ini_read(fn_ini, 'op', 'formater_directory', '')
    fn_exe = os.path.join(opt_formater_dir, 'formatter.exe')
    fn_exe_cfg = os.path.join(opt_formater_dir, 'formatter.config')

    if not os.path.isfile(fn_exe):
        msg_box('Embarcadero Format:\nPath of formatter.exe is wrong:\n'+fn_exe, MB_OK+MB_ICONERROR)
        return

    try:
        s = source_text

        fx = tempfile.NamedTemporaryFile(delete=False)
        file_name = fx.name
        fx.close()

        with open(file_name, 'w') as f:
            f.write(s)

        if ed.get_prop(PROP_LEXER_FILE, '').lower() == 'c++':
            rad_opt = '-cpp'
        else:
            rad_opt = '-delphi'

        cmd = '"{}" {} {} "{}"'.format(
            fn_exe,
            rad_opt,
            '-config "{}"'.format(fn_exe_cfg) if os.path.isfile(fn_exe_cfg) else '',
            file_name
            )

        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        out, err = proc.communicate()
        proc.stdout.close()

        if err:
            print('Embarcadero Format: '+err)

        with open(file_name, 'r') as f:
            s = f.read()

        os.remove(file_name)

        return s
    except:
        raise
