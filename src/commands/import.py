import os
import zipfile

from argparse import ArgumentParser, ArgumentTypeError

from src import settings
from src.logic.loader import Loader

if __name__ == '__main__':
    parser = ArgumentParser(description="Process import arguments")
    parser.add_argument('model', action='store', help="Model name")
    parser.add_argument('connection', action='store', help="Database connection URI")
    parser.add_argument('name', action='store', help="Name json file to be imported")

    args = parser.parse_args()
    if '.' in args.name and 'json' not in args.name.split('.'):
        raise ArgumentTypeError("Only json is currently supported for the import! Use a json format")

    name = args.name
    if '.json' not in args.name:
        name += '.json'
    # unzip fake_profiles.zip
    path = settings.BASEPATH + '/assets/%s' % name.replace('.json', '.zip')
    if os.path.isfile(path):
        with zipfile.ZipFile(path, 'r') as zipped:
            zipped.extractall(settings.BASEPATH + '/assets')
        os.remove(path)

    # this class make as assumption the fact that a csv columns
    # corresponds to a model class, if a csv maps more models
    # all together I need to change it
    Loader(args.model, args.connection, '/assets/%s' % name).execute()
    print("Data imported successfully")
