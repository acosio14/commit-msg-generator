import argparse


def cli():
    parser = argparse.ArgumentParser(prog="Commit Message Generator",
                                     description="Generate a list of conventional commits to select from.")

    parser.add_argument("-e", "--eval")