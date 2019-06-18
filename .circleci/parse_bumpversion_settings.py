import os
import pathlib
import re

from configparser import ConfigParser

import tomlkit

from bitex import __version__

GIT_COMMIT_DESCR = os.environ.get('GIT_COMMIT_DESC', '')

HOTFIX_RE = re.compile(r"")
BUGFIX_RE = re.compile(r"")
FEATURE_RE = re.compile(r"")

if HOTFIX_RE.match(GIT_COMMIT_DESCR):
    pass
elif BUGFIX_RE.match(GIT_COMMIT_DESCR):
    pass
elif FEATURE_RE.match(GIT_COMMIT_DESCR):
    pass
else:
    exit()


def parse_and_prepare_global_settings(settings, fallback_current_version):
    current_version = settings.get('current_version', fallback_current_version)
    new_version = settings.get('new_version')
    tag = settings.get('tag')
    sign_tags = settings.get('sign_tags')
    tag_name = settings.get('tag_name')
    commit = settings.get('commit')
    commit_message = settings.get('message')
    parse = settings.get('parse')
    serialize = settings.get('serialize')

    serialize_as_multi_line_str = '\n' + '\n'.join(serialize or []) or None
    serialize_as_single_line_str = ','.join(serialize or []) or None

    new_version_option = f'--new-version {new_version}' if new_version else None
    current_version_option = f'--current-version {current_version}' if current_version else None
    tag_option = "--tag" if tag else "--no-tag"
    sign_tags_option = "--sign-tags" if sign_tags else '--no-sign-tags'
    tag_name_option = f"--tag-name {tag_name}" if tag_name else None
    create_commit_option = "--commit" if commit else "--no-commit"
    commit_message_option = f"--message {commit_message}" if commit_message else None
    parse_option = f'--parse {parse}' if parse else None
    serialize_option = f'--serialize {serialize_as_single_line_str}' if serialize else None

    cfg_global_section = {
        'current_version': current_version,
        'new_version': new_version,
        'tag': tag,
        'sign_tags': sign_tags,
        'tag_name': tag_name,
        'commit': commit,
        'message': commit_message,
        'parse': parse,
        'serialize': serialize_as_multi_line_str,
    }

    cli_flags = [
        current_version_option,
        new_version_option,
        tag_option,
        tag_name_option,
        sign_tags_option,
        create_commit_option,
        commit_message_option,
        parse_option,
        serialize_option,
    ]
    # Drop None values, letting bumpversion handling defaults.
    cfg_global_section = {k: v for k, v in cfg_global_section.items() if v is not None}
    cli_flags = [option for option in cli_flags if option is not None]

    return cfg_global_section, cli_flags


def parse_config_from_pyproject_toml():
    root_toml = pathlib.Path('pyproject.toml')
    if root_toml.exists():
        with root_toml.open('r') as f:
            content = f.read()

    else:
        parent_toml = pathlib.Path('../pyproject.toml')
        with parent_toml.open('r') as f:
            content = f.read()
    pyproject = tomlkit.loads(content)

    # Convert to ordinary dict, since toml document's pop() does not remove the key.
    global_config = dict(pyproject.get('tool', {}).get('bumpversion', {}))

    cfg_global_section, _ = parse_and_prepare_global_settings(global_config, __version__)

    part_configs = global_config.pop('part', {})
    file_configs = global_config.pop('file', {})


    # Parse file-specific options
    cfg_file_sections = {}
    for name, section in file_configs.items():
        # It's necessary to prepend '../', as this script lives in a sub-folder of the project root,
        # but the pyproject.toml lives at root and the files are referenced relative from it.
        name = 'bumpversion:file:' + "../" + name

        section_settings = {
            'search': section.get('search'),
            'replace': section.get('replace'),
            'parse': section.get('parse'),
            'serialize': section.get('serialize'),
        }
        section_settings = {k:v for k,v in section_settings.items() if v is not None}

        # Bumpversion expects one value per line for lists in values, split by newlines, like so::
        #
        #     serialize =
        #          {major}.{minor}.{patch}
        #          {major}.{minor}
        #          {major}
        #
        # Where the number of spaces used to indent is irrelevant, as whitespace is stripped.
        #
        # This is true for all settings that allow lists as values.
        #
        # See bumpversion's source code for more information:
        #   https://github.com/peritus/bumpversion/blob/master/bumpversion/__init__.py#L654
        if 'serialize' in section_settings:
            section_settings['serialize'] = '\n' + '\n'.join(section_settings['serialize'])
        cfg_file_sections[name] = section_settings

    # Parse part-specific options
    cfg_parts_sections = {}
    for name, section in part_configs.items():
        name = 'bumpversion:part:' + name
        section_settings = {
            'first_value': section.get('first_value'),
            'optional_value': section.get('optional_value'),
            'values': section.get('values'),
        }
        section_settings = {k:v for k,v in section_settings.items() if v is not None}

        # Bumpversion expects one value per line, split by newlines like so::
        #
        #     values =
        #          value1
        #          value2
        #          value3
        #
        # Where the number of spaces used to indent is irrelevant, as whitespace is stripped.
        #
        # This is true for all settings that allow lists as values.
        #
        # See bumpversion's source code for more information:
        #   https://github.com/peritus/bumpversion/blob/master/bumpversion/__init__.py#L654
        if 'values' in section_settings:
            section_settings['values'] = '\n' + '\n'.join(section_settings['values'])

        cfg_parts_sections[name] = section_settings

    # Build temporary .bumpversion.cfg
    config = ConfigParser()
    config['bumpversion'] = cfg_global_section
    for section, settings in (*cfg_file_sections.items(), *cfg_parts_sections.items()):
        print(section, settings)
        config[section] = settings

    with open('.bumpversion.cfg', '+w') as f:
        config.write(f)

parse_config_from_pyproject_toml()