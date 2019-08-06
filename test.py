#!/usr/bin/env python

import glob
import os
from pathlib import Path

role_paths = []
for molecule_path_value in glob.glob('./roles/pulibrary.*/molecule'):
    molecule_path = Path(molecule_path_value)
    role_path = Path(*molecule_path.parts[:-1])
    role_paths.append(str(role_path))
os.environ['PULIBRARY_ROLES'] = "\n".join(role_paths)
os.system('TESTFILES=$(circleci tests split --split-by=timings $PULIBRARY_ROLES)')
test_files = os.system('echo $TESTFILES')
print(test_files)
os.environ['TESTFILES'] = test_files
for role in os.environ['TESTFILES']:
    os.system(f'cd {role}')
    os.system('molecule test && cd ..')
