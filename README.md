# ChristmasRandomizer
Provides a way to anonymously assign stockings to each family member.

Uses brute force method to assign stockings to each member. Basic usage:

    python christmas.py

This will look for a file `people.json` in the same directory as the script.

Use `--input '/path/to/filename.json'` to specify a file instead of `people.json`.

Run like this:

    python christmas.py -e

To send emails to the email addresses listed in `people.json`.  This will not print
the results to the screen, in order to preserve anonymous assignments for the person
running the script.

Finally, to enforce rules like "you can't have who you had last year", you can pass in
a restrction string using `--restrict`, with the format `PERSON,STOCKING;PERSON,STOCKING`,
where PERSON is not allowed to have STOCKING.  For example:

    python christmas.py --restrict 'Me,Dad;Dad,Mom;Brother,Sister;Sister,Me;Mom,Brother'

Would prevent Me from getting Dad, Dad from getting Mom, etc.

To use the above restriction string, sending an email, and using a different input file
than the default, run:

    python christmas.py -e --input '../../people.json' --restrict 'Me,Dad;Dad,Mom;Brother,Sister;Sister,Me;Mom,Brother'

Note that the included `email_config.json` and `people.json` files need to be updated to include
correct information for the people in your list.  `email_config.json` should be the address
and password for your gmail account, which must be configured to allow 'less secure apps'
access it.  I would set up a dedicated account for this purpose.  The destination emails
for each person do not necessarily need to be gmail.  You can add as many people to the list as long
as there are more than 2, each with a `name` and `email` property.



