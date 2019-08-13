# Setting and modifying PIN values

This example shows you the functionality and usage of the following four commands:
* [set_pin](#set_pin-command) - Sets a new PIN value
* [change_pin](#change_pin-command) - Changes current PIN value to a new one
* [unlock_pin](#unlock_pin-command) - Disables PIN using the corresponding PUK
* [verify_pin](#verify_pin-command) - Verifies a PIN and enables usage of certain command

The contents of `get_reader()` and `activate_card(reader)` have already been covered in the example [get-card-info](../get-card-info). Please reference the previous example if something is unclear in these functions.

## set_pin command
The `set_pin(reader, pin)` command is used to set a new PIN on the Blockchain Security 2Go card. The PIN value uses UTF-8 encoding and has to have a minimum length of 4 but can not exceed a maximum length of 62 bytes. Example PIN values may look like: `1234`, `abcd`, `1234abcd`, `Even this sentence can work as a PIN!`. Like every PIN you should try to make it secure and unpredictable. After using the command it is highly recommended to always store the returned PUK. This PUK has to be used in case the PIN gets locked (PIN entered incorrectly 3 times). Running the example and selecting the "Set pin" instruction will result in an output similar to:

  Found the specified reader and a Blockchain Security 2Go card!
  What would you like to do? ("Set pin", "Change pin", "Unlock pin" or "Verify pin")
  Set pin
  Please enter a new PIN: 1234
	PUK to unlock card (hex): dd401ad08a1f0dcd

Note that if the card already has a PIN, then executing this line will return an error. 

## change_pin command
The `change_pin(reader, old_pin, new_pin)` command is used to change the current PIN value on the Blockchain Security 2Go card to a new PIN value. Same as with the [set_pin](#set_pin-command) command it is very recommended to store the new PUK which was returned. Running the example and selecting the "Change pin" instruction will result in an output similar to:

	Found the specified reader and a Blockchain Security 2Go card!
	What would you like to do? ("Set pin", "Change pin", "Unlock pin" or "Verify pin")
	Change pin
	Please enter PIN: 1234
	Please enter a new PIN: abcd
	New PUK to unlock card (hex): 029ed4787d648666

This command will not work if the PIN has been entered incorrectly 3 times! If you have locked your PIN then you need to use the command [unlock_pin](#unlock_pin-command) and the PUK to reset the PIN.

## unlock_pin command
The `unlock_pin(reader, bytes.fromhex(puk))` command is used to deactivate the PIN authentication from the Blockchain Security 2Go card using the PUK. It can also be used in case the PIN is locked and you have to reset the PIN value. After using this command there will be no PIN on the card. Using this function returns a boolean which is `True` if the PUK was correct. If it was not correct it will return an integer with the remaining tries left. Running the example and selecting the "Unlock pin" instruction will result in an output that should look like:

	Found the specified reader and a Blockchain Security 2Go card!
	What would you like to do? ("Set pin", "Change pin", "Unlock pin" or "Verify pin")
	Unlock pin
	Please enter PUK: dd401ad08a1f0dcd
	OK - Unlocked!

Keep in mind that having no PIN is less secure than using a PIN and therefore it is strongly recommended that you always have a PIN enabled.

Under certain circumstances, for example if you lost the PUK but the PIN is still known, then the functions [change_pin](#change_pin-command) and [unlock_pin](#unlock_pin-command) can be used together to reset the PIN:

	temp_pin = "1234"
	temp_puk = blocksec2go.change_pin(reader, known_pin, temp_pin)
	blocksec2go.unlock_pin(reader, bytes.fromhex(temp_puk))

The value of `temp_pin` is completely irrelevant since it will in any case be removed in the next line.

## verify_pin command
The `verify_pin(reader, pin)` command is used to check the PIN value and it simultaneously enables the usage of the commands `encrypted_keyimport` and `generate_signature`. To get more information on the latter, please refer to the example [generate-signature](../generate-signature). Using the function `verify_pin(reader, pin)` returns a boolean which is `True` if the PIN was correct. If it was not correct it will return an integer with the remaining tries left. Running the example and selecting the "Verify pin" instruction will result in an output that should look like:

	Found the specified reader and a Blockchain Security 2Go card!
	What would you like to do? ("Set pin", "Change pin", "Unlock pin" or "Verify pin")
	Verify pin
	Please enter PIN: 1234
	OK - Verified!