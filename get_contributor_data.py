#!/usr/bin/env python
# -*- coding: utf-8 -*-


from github import Github
from time import sleep
import configparser
import codecs
import csv
import sys
from datetime import datetime
import os
import argparse
#import ipdb as pdb


def parse_args():
    """
    Parse script input arguments.

    Returns the parsed args, having validated that the input
    file can be read, and that there is a valid Username.
    """
    parser = get_parser()
    args = parser.parse_args()

    # pdb.set_trace()
    if os.path.isfile(args.input):
        args.input_filename = args.input
    else:
        return None

    args.csv_filename = args.output

    return args


def get_parser():
    """ Return the parser used to interpret the script arguments."""
    usage = (
        "Script to send an HTML file as an HTML email."
        "\nExamples:"
        "\n1. Send the contents of test_file.html to fred"
        "\n$ send_html_email.py test_file.html"
        "\n"
    )
    epilog = "NB This script requires a Gmail account."

    formatter_class = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(description=usage,
                                     epilog=epilog,
                                     formatter_class=formatter_class
                                     )

    parser.add_argument('-i', '--input',
                        help=('The test email subject line (defaults to "Test'
                              'email")'
                              )
                        )
    parser.add_argument('-o', '--output',
                        help=('The test email subject line (defaults to "Test'
                              'email")'
                              ),
                        default="get_contribuitor_data.csv"
                        )
    return parser
def print_message(message):
    """Exibe uma mensagem de forma personalizada

    :message: A messagem a ser escrita
    :returns: None

    """
    str_date = datetime.strftime(datetime.now(), '%d-%m-%Y %H:%M:%S')
    print(('[{0}] {1}'.format(str_date, message)))

try:
    # pdb.set_trace()
    config = configparser.ConfigParser()
    config.read_file(open(('./conf/get_contribuitor_data.ini')))
    api_token = config.get('API_TOKEN', 'token')
    git_api = Github(login_or_token=api_token)
    contrib_counter = 0
    email_counter = 0
    seconds_to_wait = 2
    args = parse_args()
    csv_file_name = args.csv_filename
    repositories_file =  args.input_filename

    with codecs.open(csv_file_name, 'w') as f:
        writer_csv = csv.writer(f,
                                delimiter=';',
                                quotechar='"',
                                quoting=csv.QUOTE_NONNUMERIC
                                )
        # Escrevendo o cabeçaho do arquivo CSV
        writer_csv.writerow(('#',
                             'repositorio',
                             'nome_contribuidor',
                             'email_contribuidor'
                             )
                            )
        with codecs.open(repositories_file, 'r') as repo_file:
            repo = repo_file.readline()
            user_message = 'Analisando o repositório {0}.'.format(repo)
            print_message(user_message)
            repo_git = git_api.get_repo(repo)
            for contrib in repo_git.get_contributors():
                contrib_counter = contrib_counter + 1
                if contrib.email is not None:
                    email_counter = email_counter + 1
                    writer_csv.writerow((email_counter,
                                        repo,
                                        contrib.name,
                                        contrib.email)
                                        )
                user_message = ('Esperando {0} segundos para uma nova '
                                'consulta!'
                                ).format(seconds_to_wait)
                print_message(user_message)
                sleep(seconds_to_wait)

            user_message = ('Fim da análise do projeto {0}.'
                            'Total de contribuidores: {1}. '
                            'Total com e-mail {2}').format(repo,
                                                           contrib_counter,
                                                           email_counter)
        print_message(user_message)
except Exception as e:
    print_message(e)
