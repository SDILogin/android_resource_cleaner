import argparse
import logging
import os
import subprocess
from xml.etree import ElementTree as ET


def initialize_logger(log_level):
    if log_level == "DEBUG":
        logging.basicConfig(level=logging.DEBUG)
    elif log_level == "INFO":
        logging.basicConfig(level=logging.INFO)
    elif log_level == "WARNING":
        logging.basicConfig(level=logging.WARNING)
    else:
        logging.basicConfig(level=logging.ERROR)


def get_all_string_resource_files(project_directory):
    result = []
    for root, _, files in os.walk(project_directory, topdown=False):
        if "build" not in root and ".idea" not in root:
            for name in files:
                if "strings.xml" in name:
                    result.append(os.path.join(root, name))
    return result


def resource_used_in_layout_files(dir, target_resource_name):
    result = subprocess.run(['grep', '-r',
                             '--include', "*.xml",
                             '--exclude', "strings.xml",
                             '--exclude-dir', "*build*",
                             '--exclude-dir', ".idea",
                             '--exclude-dir', "./.git",
                             target_resource_name,
                             dir], capture_output=True)
    output = result.stdout
    return output is not None and output != b''


def resource_used_in_kotlin_or_java_files(dir, target_resource_name):
    result = subprocess.run(['grep', '-r',
                             '--include', "*.kt",
                             '--include', "*.java",
                             '--exclude-dir', "*build*",
                             '--exclude-dir', ".idea",
                             '--exclude-dir', "./.git",
                             f'.{target_resource_name}',
                             dir], capture_output=True)
    output = result.stdout
    return output is not None and output != b''


def cleanup(project_dir, base_xml):
    xml_data = ET.parse(base_xml)
    string_xml_items = list(xml_data.getroot())
    string_resource_names = [x.get('name') for x in string_xml_items]
    unused_resources = []
    logging.info("searching for unused resources")
    for i in range(0, len(string_resource_names)):
        if i % 10 == 0:
            logging.info(f"{i} / {len(string_resource_names)} | {i / len(string_resource_names) * 100}%")

        string_resource_name = string_resource_names[i]
        if not resource_used_in_layout_files(project_dir, string_resource_name) and \
                not resource_used_in_kotlin_or_java_files(project_dir, string_resource_name):
            unused_resources.append(string_resource_name)

    logging.info(f"found {len(unused_resources)} unused resources")

    string_resource_files = get_all_string_resource_files(args.path)
    logging.info(f"found {len(string_resource_files)} string resource files")

    for string_resource_file in string_resource_files:
        xml_data = ET.parse(string_resource_file)
        string_xml_items = list(xml_data.getroot())

        changed = False
        for string_xml_item in string_xml_items:
            if string_xml_item.get('name') in unused_resources:
                changed = True
                xml_data.getroot().remove(string_xml_item)

        if changed:
            xml_data.write(string_resource_file, encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='String resources checker for android. Will look for unused strings')
    parser.add_argument('--log-level',
                        choices=['DEBUG', "INFO", "WARNING", "ERROR"],
                        help='Logging level. DEBUG, INFO, WARNING, ERROR')

    parser.add_argument('--path', '-p', metavar='path', type=str, help='Project path')
    parser.add_argument('--base-xml',
                        metavar='path',
                        type=str,
                        help='Base xml file path. Will be used to determinate what strings are not stored in base xml')

    args = parser.parse_args()

    initialize_logger(args.log_level)

    cleanup(args.path, args.base_xml)
