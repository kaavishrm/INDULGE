"""Builds the deck: python3 pitches/westside/build.py (add STRICT=1 to fail on internal notes or placeholders)."""
import runpy, pathlib
runpy.run_path(str(pathlib.Path(__file__).resolve().parent / 'src' / 'build3.py'), run_name='__main__')
