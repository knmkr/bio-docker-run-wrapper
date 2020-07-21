#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pathlib
import textwrap


def _main():
    with open('commands.tsv', 'r') as fin:
        for line in fin:
            if line.startswith('#'):
                continue

            name, image, tag, cmd, ref = line.strip().split('\t')

            options = {
                'jupyter': '''
                  -p 8888:8888 \\
                  -p 8080:8080 \\
                  -p 8081:8081 \\
                  -p 8082:8082 \\''',
            }

            bin_path = pathlib.Path('.', 'bin', name)
            with open(bin_path, 'w') as fout:
                option = options.get(name, '')
                template = f'''\
                #!/bin/bash

                if [ -w /var/run/docker.sock ]; then
                  # rootful docker
                  CONTAINER_USER=$(id -u):$(id -g)
                else
                  # rootless docker
                  CONTAINER_USER=root
                fi

                # {ref}
                docker run -it --rm \\
                  -u $CONTAINER_USER \\
                  -e HOME=$HOME \\
                  -e USER=$USER \\
                  -v $HOME:$HOME \\
                  -w "$PWD" \\{option}
                  {image}:{tag} {cmd} "$@"
                '''

                print(textwrap.dedent(template), file=fout)
                os.chmod(bin_path, 0o755)


if __name__ == '__main__':
    _main()
