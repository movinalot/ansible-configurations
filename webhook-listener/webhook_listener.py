""" Webhook Listener """

# pylint: disable=invalid-name, too-many-nested-blocks

import subprocess
import os
from flask import Flask, request

from webexteamssdk import WebexTeamsAPI

flask_app = Flask(__name__)

api = WebexTeamsAPI()
WEBEX_TEAMS_DEST_ROOM_ID = os.environ['WEBEX_TEAMS_DEST_ROOM_ID']
PROCESS_WEBHOOK = True

@flask_app.route('/events', methods=['GET', 'POST'])
def webhook_events():
    """Processes incoming requests to the '/events' URI."""

    if request.method == 'GET':
        doc = """
                <!DOCTYPE html>
                  <html lang="en">
                    <head>
                      <title>Webhook handler via Flask</title><meta charset="UTF-8">
                    </head>
                    <body>
                      <p><strong>Your Flask web server is up and running!</strong></p>
                    </body>
                  </html>
              """
    elif request.method == 'POST':

        # Get the POST data sent from Github
        json_data = request.json
        print("\n")
        print("WEBHOOK POST RECEIVED:")
        print(json_data)
        print("\n")

        if PROCESS_WEBHOOK:
            dirs_to_process = []
            for commit in json_data["commits"]:
                for file_state in ['added', 'modified']:
                    for file_name in commit[file_state]:
                        if file_name.find("/") > 0:
                            print(file_state + ":" + file_name)
                            dir_to_process = file_name[0:file_name.find("/")]
                            dirs_to_process.append(dir_to_process)

            if dirs_to_process:
                dirs_to_process_set = set(dirs_to_process)
                dirs_to_process_uni = list(dirs_to_process_set)
                print(" ".join(dirs_to_process_uni))

                result = subprocess.run(
                    [
                        (
                            '~/projects/ansible-configurations/run-ansible.sh '
                            + ' '.join(dirs_to_process_uni)
                        )
                    ],
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                print(result.stdout)
                print(result.stderr)

                api.messages.create(
                    WEBEX_TEAMS_DEST_ROOM_ID,
                    text=result.stdout.decode("utf-8")
                )

        doc = """
                <!DOCTYPE html>
                  <html lang="en">
                    <head>
                      <title>Webhook handler via Flask</title><meta charset="UTF-8">
                    </head>
                  <body>
                    <p><strong>Processed the hook!</strong></p>
                  </body>
                  </html>
              """

    response = flask_app.response_class(
        response=doc,
        status=200,
        mimetype='text/html'
    )

    return response


if __name__ == '__main__':
    # Start the Flask web server
    flask_app.run(host='0.0.0.0', port=5403)
