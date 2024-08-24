import os
import sys
import json

def create_notebook(file_path):
    dir_name = os.path.dirname(file_path)
    notebook_name = os.path.join(dir_name, "magick.ipynb")

    # Define the content of the new Jupyter notebook
    notebook_content = {
        "cells": [
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "%load_ext sqlmagick\n"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "%%dump_files\n",
                    f"{file_path}\n"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.5"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    # Write the notebook content to a .ipynb file
    with open(notebook_name, 'w') as notebook_file:
        json.dump(notebook_content, notebook_file, indent=4)

    # Open the notebook in VS Code
    os.system(f'code "{notebook_name}"')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python open_with_jupyter.py <file_path>")
    else:
        create_notebook(sys.argv[1])
