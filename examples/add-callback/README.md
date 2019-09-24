# Executing functions when card get connected/disconnected

This example shows you how to add callbacks to the insertion/removal of a smartcard. 

The contents of `get_reader()` and `activate_card(reader)` have already been covered in the previous example [get-card-info](../get-card-info). Please reference that example if something is unclear in these functions.

Before we add any callbacks we need to first start monitoring the readers for any smartcard insertions / removals. This is done by using the command `observer.start()`:

    cardmonitor, cardobserver = observer.start()

It is very important to store the `cardmonitor` and `cardobserver` object since these are essential to close the monitoring of the readers:

    observer.stop(cardmonitor, cardobserver)

Please do not forget to stop the monitoring since this can lead to issues with the reader if left open.

Using the `add_callback(connect = connected, disconnect = disconnected)` function we are able to add the function `connected(self)` as a callback when a smartcard gets inserted and add the function `disconnected(self)` as a callback when a card gets removed:

    def connected(self):
    ...
    def disconnected(self):
    ...
    blocksec2go.add_callback(connect = connected, disconnect = disconnected)


Be careful of the fact that the insertion and removal of any smartcard on any reader also triggers the callbacks above. You need to manually check if the inserted or removed card was a Blockchain Security 2Go card.

Additionally you also need the `reader` object which is used by the other commands in the  blocksec2go library:

    def connected(self):
        print('A smartcard is connected to the reader!')
        reader = get_reader()
        activate_card(reader)

You can press the "Enter" button on your keyboard at any time to stop the monitoring process and close the program. An example output would look like this:

    Insert a Blockchain Security 2Go card onto the reader!
    Press Enter at any time to exit the program!
    A smartcard is connected to the reader!
    Found the specified reader and a Blockchain Security 2Go card!
    The card is disconnected from the reader!