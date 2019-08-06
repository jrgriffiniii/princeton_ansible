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
test_files = os.system('circleci tests split --split-by=timings $PULIBRARY_ROLES')
print(test_files)
for role in test_files:
    os.system(f'cd ~/princeton_ansible/{role}')
    os.system('molecule test && cd ..')
