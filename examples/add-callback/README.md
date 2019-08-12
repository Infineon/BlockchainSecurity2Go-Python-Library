# Executing functions when card get connected/disconnected

This example shows you how to add callbacks to the insertion/removal of a smartcard. 

The contents of `get_reader()` and `activate_card(reader)` have already been covered in the previous example [get-card-info](../get-card-info). Please reference that example if something is unclear in these functions.

Before we add any callbacks we need to first start monitoring the readers for any smartcard insertions / removals. This is done by using the command `observer.start()`:

    cardmonitor, cardobserver = observer.start()

It is very important to store the `cardmonitor` and `cardobserver` object since these are essential to close the monitoring of the readers:

    observer.stop(cardmonitor, cardobserver)

Please dont forget to stop the monitoring since this can lead to issues with the reader if left open.

Using the `add_callback(connect = connected, disconnect = disconnected)` function we are able to add the function `connected(self)` as a callback when a smarcard gets inserted and add the function `disconnected(self)` as a callback when a card gets removed:

    def connected(self):
    ...
    def disconnected(self):
    ...
    blocksec2go.add_callback(connect = connected, disconnect = disconnected)


Be careful of the fact that at the time when a callback gets triggered there is no guarantee that there is a Blockchain Security 2Go card present or that a Blockchain Security 2Go card was removed. You need to manually check which card reader was affected by the callback or if the card that was inserted was actually a Blockchain Security 2Go card. This is because the callbacks happen whenever any smartcard gets inserted/removed!

Apart from the problem mentioned above you would also still need the `reader` object which is used by the other commands in the  blocksec2go library:

    def connected(self):
        print('A smartcard is connected to the reader!')
        reader = get_reader()
        activate_card(reader)

You can press the "Enter" button at any time on your Keyboard to stop the monitoring process and close the program.