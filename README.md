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


