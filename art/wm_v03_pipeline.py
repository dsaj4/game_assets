"""Publish/verify v03 with the shared saved-master pipeline; never target old outputs."""
from pathlib import Path
import sys, runpy
sys.path.insert(0,str(Path(__file__).resolve().parent))
import wm_tools
wm_tools.OUT=wm_tools.ROOT/'art/wand-management-v03'
mode=next((a for a in sys.argv if a in ('publish','verify')),None)
if mode is None:
    raise ValueError('Specify -- publish or -- verify')
runpy.run_path(str(Path(__file__).with_name(('publish' if mode=='publish' else 'verify')+'_wand_management.py')),run_name='__main__')
