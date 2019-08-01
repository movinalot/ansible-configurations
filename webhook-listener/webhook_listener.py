""" Webhook Listener """

import subprocess
import os
from flask import Flask, request

from webexteamssdk import WebexTeamsAPI

FLASK_APP = Flask(__name__)

API = WebexTeamsAPI()
WEBEX_TEAMS_DEST_ROOM_ID = os.environ['WEBEX_TEAMS_DEST_ROOM_ID']
DOMAIN_DIRS = ['aci', 'nxos', 'ucs']
PROCESS_WEBHOOK = True

@FLASK_APP.route('/events', methods=['GET', 'POST'])
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

        # Process the POST data sent from Github
        json_data = request.json
        print("\n")
        print("WEBHOOK POST RECEIVED:")
        print(json_data)
        print("\n")

        if PROCESS_WEBHOOK:
            for commit in json_data["commits"]:
                dirs_to_process = []

                for state in ['added', 'modified']:
                    _ = [dirs_to_process.append(item) for item in [
                        x[0:x.find("/")]
                        for x in commit[state]
                        if x.find("/") > 0
                        ] if item not in dirs_to_process and item in DOMAIN_DIRS]

                if dirs_to_process:
                    print(dirs_to_process)

                if dirs_to_process:
                    cmdline = (
                        '~/projects/ansible-configurations/run-ansible.sh '
                        + ' '.join(dirs_to_process)
                    )
                    print(cmdline)

                    result = subprocess.run(
                        [cmdline],
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )

                    message = (
                        'Committer: ' + commit['committer']['name'] +
                        ' - ' + commit['committer']['email'] + '\n'
                    )

                    message += 'Commit Message: ' + commit['message'] + '\n'
                    message += 'stdout result: \n'
                    message += result.stdout.decode("utf-8") + '\n'
                    message += 'stderr result: \n'
                    message += result.stderr.decode("utf-8") + '\n'

                    print(message)

                    API.messages.create(
                        WEBEX_TEAMS_DEST_ROOM_ID,
                        text=message
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

    response = FLASK_APP.response_class(
        response=doc,
        status=200,
        mimetype='text/html'
    )

    return response


if __name__ == '__main__':
    # Start the Flask web server
    FLASK_APP.run(host='0.0.0.0', port=5403)
