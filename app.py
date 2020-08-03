from flask import Flask, render_template, send_from_directory, send_file
from flask_socketio import SocketIO
import random
from flask_mail import Mail, Message
from validate_email import validate_email
import os

app = Flask(__name__)
socketio = SocketIO(app)


mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": "kunjcmehta@gmail.com",
    "MAIL_PASSWORD": "Atoz1998"
}

app.config.update(mail_settings)
mail = Mail(app)


@app.route("/")
def home():
    return render_template("iframe.html")

@app.route("/index.html")
def main():
    return render_template("index.html")


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('response')
def response(json, methods=['GET', 'POST']):

    # greetings = {"Hello": "Hey! What can I do for you?",
    #              "Hi": "Hello. What can I do for you?",
    #              "Hey!": "Hi. What can I do for you?"}
    #
    # order = {"I want to give an order":"Takeaway or Delivery?",
    #          "Takeaway":"What would you like to o   rder?",
    #          "Show me the menu": "Here is the menu",
    #          "Order already":"Tell me",
    #          "Order": "Tell me",
    #          "Delivery":"Please order on this link: ",
    #          }
    #
    # reservation = {"I want to make a reservation": "How many people do you want to reserve a table for",
    #                "2": "At what time?",
    #                "4": "At what time?",
    #                "Before 12": "Done",
    #                "After 12": "Done"}
    #
    # bill = {"I want the bill": "Do you have Zomato Gold?",
    #         "Yes": "Please unlock it",
    #         "No": "Do you have a corporate id card?",
    #         "yes": "Please show it",
    #         "no": "We're processing the bill"
    #         }
    #

    # print('received my event: ' + str(json))

    # if json["message"] in greetings.keys():
    #     dict["b1"] = "I want to make a reservation"
    #     dict["b2"] = "I want to give an order"
    #     dict["b3"] = "I want the bill"
    #
    #     response = random.choice(list(greetings.values()))
    #     dict["response"] = response
    #
    #     socketio.emit('my response', dict, callback=messageReceived)
    #     dict.clear()
    #
    # elif json["message"] == "Show me the menu":
    #     response = "Here is the menu"
    #     dict["response"] = response
    #     dict["url"] = "static/background.jpg"
    #     dict["b1"] = "Order"
    #
    #     socketio.emit('my response', dict, callback=messageReceived)
    #     dict.clear()
    #
    # elif json["message"] in order.keys():
    #     key = json["message"]
    #     dict["response"] = order[key]
    #
    #     if key == "I want to give an order":
    #         dict["b1"] = "Takeaway"
    #         dict["b2"] = "Delivery"
    #
    #     if key == "Takeaway":
    #         dict["b1"] = "Show me the menu"
    #         dict["b2"] = "Order already"
    #
    #     if key == "Delivery":
    #         dict["b1"] = "Order"
    #         dict["hyperlink"] = "www.dominos.in"
    #
    #     socketio.emit('my response', dict, callback=messageReceived)
    #     dict.clear()
    #
    # elif json["message"] in reservation.keys():
    #     if json["message"] == "I want to make a reservation":
    #         dict["b1"] = "2",
    #         dict["b2"] = "4"
    #         key = json["message"]
    #         dict["response"] = reservation[key]
    #         socketio.emit('my response', dict, callback=messageReceived)
    #     elif json["message"] == "2":
    #         dict["b1"] = "Before 12",
    #         dict["b2"] = "After 12"
    #         key = json["message"]
    #         dict["response"] = reservation[key]
    #         socketio.emit('my response', dict, callback=messageReceived)
    #         dict.clear()
    #     elif json["message"] == "4":
    #         dict["b1"] = "Before 12",
    #         dict["b2"] = "After 12"
    #         key = json["message"]
    #         dict["response"] = reservation[key]
    #         socketio.emit('my response', dict, callback=messageReceived)
    #         dict.clear()
    #
    # elif json["message"] in bill.keys():
    #     if json["message"] == "I want the bill":
    #         dict["b1"] = "Yes",
    #         dict["b2"] = "No"
    #         key = json["message"]
    #         dict["response"] = bill[key]
    #         socketio.emit('my response', dict, callback=messageReceived)
    #         dict.clear()
    #     elif json["message"] == "Yes":
    #         dict["b1"] = "Unlocked",
    #         key = json["message"]
    #         dict["response"] = bill[key]
    #         socketio.emit('my response', dict, callback=messageReceived)
    #         dict.clear()
    #     elif json["message"] == "No":
    #         dict["b1"] = "yes",
    #         dict["b2"] = "no"
    #         key = json["message"]
    #         dict["response"] = bill[key]
    #         socketio.emit('my response', dict, callback=messageReceived)
    #         dict.clear()
    #     elif json["message"] == "yes":
    #         dict["b1"] = "Showing",
    #         key = json["message"]
    #         dict["response"] = bill[key]
    #         socketio.emit('my response', dict, callback=messageReceived)
    #         dict.clear()
    #     elif json["message"] == "no":
    #         dict["b1"] = "Okay",
    #         key = json["message"]
    #         dict["response"] = bill[key]
    #         socketio.emit('my response', dict, callback=messageReceived)
    #         dict.clear()
    #
    #
    # else:
    #     response = "I don't know what you are talking about"
    #     dict["response"] = response
    #
    #     socketio.emit('my response', dict, callback=messageReceived)
    #     dict.clear()
    dict = {}

    # get and validate email
    if json["input"] == "Write a query":
        is_valid = validate_email(json["email"], verify=True)
        print(is_valid)
        dict["response"] = is_valid
        socketio.emit('my response', dict, callback=messageReceived)
        dict.clear()


    # get query
    if json["input"] == "Submit query":
        token = random.randint(1, 1000)
        query = json["query"]
        email = json["email"]

        # admin side
        with app.app_context():
            msg = Message(subject="Query #" + str(token) + " received",
                          sender=app.config.get("MAIL_USERNAME"),
                          recipients=[email],
                          body="Your query has been recorded. We will try to reply as soon as possible")
            mail.send(msg)

        # customer side
        with app.app_context():
            msg = Message(subject="You have got a query with token #" + str(token),
                          sender=app.config.get("MAIL_USERNAME"),
                          recipients=["iammanojmj@gmail.com"],
                          body=query)
            mail.send(msg)


if __name__ == '__main__':
    socketio.run(app, debug=True)


