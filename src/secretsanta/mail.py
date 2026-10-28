import json
import re
import smtplib
from email.message import EmailMessage

import networkx as nx


def split_name(name):
    name_list = name.split(" ")
    first_name, last_name = name_list[0], " ".join(name_list[1:])
    return first_name, last_name


def write_mail(gift_sender_node, gift_receiver_node, global_sender, mail_template):

    msg = EmailMessage()

    sender_first_name, _ = split_name(gift_sender_node["name"])
    sender_email = gift_sender_node["mail"]
    receiver_name = gift_receiver_node["name"]

    variables = {"sender_first_name": sender_first_name, "receiver_name": receiver_name}

    with open(mail_template) as f:
        content = f.read()

        def replace(match: re.Match) -> str:
            key = match.group(1)
            # Keep the original tag if no value is provided
            return str(variables.get(key, match.group(0)))

        content = re.sub(r"\{\{\s*(\w+)\s*\}\}", replace, content)

        msg.set_content(content)

    msg["Subject"] = "Secret santa 2026"
    msg["From"] = global_sender
    msg["To"] = sender_email

    return msg


def parse_mail_config(mail_config_file: str):
    with open(mail_config_file, "r") as f:
        mail_config = json.load(f)

    return mail_config


def write_all_mails(digraph: nx.DiGraph, mail_config: dict):

    msg_list = []

    for sender_idx, receiver_idx in digraph.edges:
        msg_list.append(
            write_mail(
                gift_sender_node=digraph.nodes[sender_idx],
                gift_receiver_node=digraph.nodes[receiver_idx],
                global_sender=mail_config["global-sender"],
                mail_template=mail_config["mail-template"],
            )
        )
        # with open(f"data/tmp/{digraph.nodes[sender_idx]['name']}", "w") as f:
        #     f.write(msg_list[-1].get_content())

    return msg_list


def send_all_mails(msg_list: list[EmailMessage], mail_config: dict) -> None:

    server = smtplib.SMTP("smtp.gmail.com", 587)

    server.ehlo()
    server.starttls()

    server.login(mail_config["username"], mail_config["password"])

    for msg in msg_list:
        print(f"Sending email to {msg['To']}...", end=None)
        server.send_message(msg)
        print("Done.")

    server.close()
