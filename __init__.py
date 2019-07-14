import os
import subprocess
import tempfile
from cudatext import *
from cuda_fmt import get_config_filename

def do_format_ex(source_text, lang_key):

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

        cmd = '"{}" {} {} "{}"'.format(
            fn_exe,
            lang_key,
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

def do_format_pas(text):

    return do_format_ex(text, '-delphi')

def do_format_cpp(text):

    return do_format_ex(text, '-cpp')
