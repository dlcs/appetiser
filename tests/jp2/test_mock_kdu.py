import pathlib
import pytest
import subprocess

from app.jp2.kdu import (
        _run_kdu_command,
        kdu_compress, 
        kdu_expand_to_image
        )

def test__run_kdu_command(mocker):
    mocker.patch('subprocess.run')
    command = '/path/to/kdu/command --and args'
    env = {'ENVIRONMENTAL': 'VARIABLES'}
    _run_kdu_command(command, env)
    subprocess.run.assert_called_once_with(
            command, 
            env=env,
            capture_output=True,
            check=True, 
            shell=True
            )

def test__run_kdu_command_exception(mocker):
    command = 'false'
    env = {'ENVIRONMENTAL': 'VARIABLES'}
    with pytest.raises(subprocess.CalledProcessError):
        _run_kdu_command(command, env)


def test_kdu_compress_kdu_low_rgb(mocker):
    mocker.patch('subprocess.run')
    mocker.patch.dict('os.environ', {
        'KDU_COMPRESS': '/path/to/kdu_compress', 
        'KDU_LIB': '/path/to/kdu_lib', 
        })
    expected_command = '/path/to/kdu_compress -i /path/to/image.tiff -o /path/to/image.jp2'\
    ' Clevels=7 "Cblk={64,64}" "Cuse_sop=yes" -jp2_space sRGB "ORGgen_plt=yes"'\
    ' "ORGtparts=R" "Corder=RPCL" -rate 0.5 "Cprecincts={256,256},{256,256},'\
    '{256,256},{128,128},{128,128},{64,64},{64,64},{32,32},{16,16}"'
    expected_env = {
            'LD_LIBRARY_PATH': '/path/to/kdu_lib',
            'PATH': '/path/to/kdu_compress'
            }
    kdu_compress(
            pathlib.Path('/path/to/image.tiff'),
            pathlib.Path('/path/to/image.jp2'), 
            'kdu_low', 
            'RGB'
            )
    subprocess.run.assert_called_once_with(
            expected_command, 
            env=expected_env,
            capture_output=True,
            check=True, 
            shell=True
            )

def test_kdu_compress_kdu_med_rgba(mocker):
    mocker.patch('subprocess.run')
    mocker.patch.dict('os.environ', {
        'KDU_COMPRESS': '/path/to/kdu_compress', 
        'KDU_LIB': '/path/to/kdu_lib', 
        })
    expected_command = '/path/to/kdu_compress -i /path/to/image.tiff -o /path/to/image.jp2'\
    ' Clevels=7 "Cblk={64,64}" "Cuse_sop=yes" -jp2_space sRGB -jp2_alpha "ORGgen_plt=yes"'\
    ' "ORGtparts=R" "Corder=RPCL" -rate 2 "Cprecincts={256,256},{256,256},'\
    '{256,256},{128,128},{128,128},{64,64},{64,64},{32,32},{16,16}"'
    expected_env = {
            'LD_LIBRARY_PATH': '/path/to/kdu_lib',
            'PATH': '/path/to/kdu_compress'
            }
    kdu_compress(
            pathlib.Path('/path/to/image.tiff'),
            pathlib.Path('/path/to/image.jp2'), 
            'kdu_med', 
            'RGBA'
            )
    subprocess.run.assert_called_once_with(
            expected_command, 
            env=expected_env,
            capture_output=True,
            check=True, 
            shell=True
            )

def test_kdu_compress_kdu_med_layers_rgb(mocker):
    mocker.patch('subprocess.run')
    mocker.patch.dict('os.environ', {
        'KDU_COMPRESS': '/path/to/kdu_compress', 
        'KDU_LIB': '/path/to/kdu_lib', 
        })
    expected_command = '/path/to/kdu_compress -i /path/to/image.tiff -o /path/to/image.jp2'\
    ' Clevels=7 "Cblk={64,64}" "Cuse_sop=yes" -jp2_space sRGB "ORGgen_plt=yes"'\
    ' "ORGtparts=R" "Corder=RPCL" Clayers=6 -rate 2 "Cprecincts={256,256},{256,256},'\
    '{256,256},{128,128},{128,128},{64,64},{64,64},{32,32},{16,16}"'
    expected_env = {
            'LD_LIBRARY_PATH': '/path/to/kdu_lib',
            'PATH': '/path/to/kdu_compress'
            }
    kdu_compress(
            pathlib.Path('/path/to/image.tiff'),
            pathlib.Path('/path/to/image.jp2'), 
            'kdu_med_layers', 
            'RGB'
            )
    subprocess.run.assert_called_once_with(
            expected_command, 
            env=expected_env,
            capture_output=True,
            check=True, 
            shell=True
            )

def test_kdu_compress_kdu_high_l(mocker):
    mocker.patch('subprocess.run')
    mocker.patch.dict('os.environ', {
        'KDU_COMPRESS': '/path/to/kdu_compress', 
        'KDU_LIB': '/path/to/kdu_lib', 
        })
    expected_command = '/path/to/kdu_compress -i /path/to/image.tiff -o /path/to/image.jp2'\
    ' Clevels=7 "Cblk={64,64}" "Cuse_sop=yes" -no_palette "ORGgen_plt=yes"'\
    ' "ORGtparts=R" "Corder=RPCL" -rate 4 "Cprecincts={256,256},{256,256},'\
    '{256,256},{128,128},{128,128},{64,64},{64,64},{32,32},{16,16}"'
    expected_env = {
            'LD_LIBRARY_PATH': '/path/to/kdu_lib',
            'PATH': '/path/to/kdu_compress'
            }
    kdu_compress(
            pathlib.Path('/path/to/image.tiff'),
            pathlib.Path('/path/to/image.jp2'), 
            'kdu_high', 
            'L'
            )
    subprocess.run.assert_called_once_with(
            expected_command, 
            env=expected_env,
            capture_output=True,
            check=True, 
            shell=True
            )

def test_kdu_compress_kdu_max_1(mocker):
    mocker.patch('subprocess.run')
    mocker.patch.dict('os.environ', {
        'KDU_COMPRESS': '/path/to/kdu_compress', 
        'KDU_LIB': '/path/to/kdu_lib', 
        })
    expected_command = '/path/to/kdu_compress -i /path/to/image.tiff -o /path/to/image.jp2'\
    ' Clevels=7 "Cblk={64,64}" "Cuse_sop=yes" -no_palette "ORGgen_plt=yes"'\
    ' "ORGtparts=R" "Corder=RPCL" -rate - "Cprecincts={256,256},{256,256},'\
    '{256,256},{128,128},{128,128},{64,64},{64,64},{32,32},{16,16}"'
    expected_env = {
            'LD_LIBRARY_PATH': '/path/to/kdu_lib',
            'PATH': '/path/to/kdu_compress'
            }
    kdu_compress(
            pathlib.Path('/path/to/image.tiff'),
            pathlib.Path('/path/to/image.jp2'), 
            'kdu_max', 
            '1'
            )
    subprocess.run.assert_called_once_with(
            expected_command, 
            env=expected_env,
            capture_output=True,
            check=True, 
            shell=True
            )

def test_kdu_expand_to_image(mocker):
    mocker.patch('subprocess.run')
    mocker.patch('PIL.Image.open')
    mock_tmp = mocker.patch('tempfile.TemporaryDirectory')
    mock_tmp.return_value.__enter__ = lambda x: '/tmp/path/to/'
    mocker.patch.dict('os.environ', {
        'KDU_EXPAND': '/path/to/kdu_expand', 
        'KDU_LIB': '/path/to/kdu_lib', 
        })
    expected_env = {
            'LD_LIBRARY_PATH': '/path/to/kdu_lib',
            'PATH': '/path/to/kdu_expand'
            }
    expected_command = '/path/to/kdu_expand -i /path/to/image.jp2 -o /tmp/path/to/image.bmp -quiet -num_threads 4'
    kdu_expand_to_image(pathlib.Path('/path/to/image.jp2'))
    subprocess.run.assert_called_once_with(
            expected_command, 
            env=expected_env,
            capture_output=True,
            check=True, 
            shell=True
            )
