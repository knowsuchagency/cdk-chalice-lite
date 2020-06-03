from pprint import pprint

from chalice import Chalice, Rate

app = Chalice(app_name="testing-chalice")


@app.route("/")
def test():
    """This is just an initial test endpoint."""
    return {"hello": "world"}


@app.lambda_function
def foo(event, context):
    pprint(event)


@app.schedule(Rate(5, unit=Rate.MINUTES))
def periodic_task(event):
    return {"hello": "world"}


@app.on_sqs_message(queue="test-queue")
def sqs_handler(event):
    for record in event:
        print("Message body: %s" % record.body)
