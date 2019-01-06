#!/usr/bin/python
import getopt, smtplib, json, random, sys, copy

def send_email(sendToAddress, emailConfigFile, stocking, person):

	# load config data	
	with open(emailConfigFile) as conf:
		print 'Loading json email data...'
		emailData = json.load(conf)
	
	# send via gmail (the email address has to be a gmail
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()

	# this is way easier than I expected
	server.login(emailData["username"], emailData["password"])

	# use message headers -- you need a blank line between the subject and the message body
	message = "\r\n".join(["From: {0}".format(emailData["username"]), "To: {0}".format(sendToAddress), "Subject: Christmas Stocking Assignment", "\nHello {0}, you have been assigned {1} for stockings this year\n-Christmas assignment code".format(person, stocking)])

	# actually sends it
	server.sendmail(emailData["username"], sendToAddress, message)
	server.quit()

	print 'Successfully sent email to {0}'.format(sendToAddress)

def main(argv):

	try:
		opts, args = getopt.getopt(sys.argv[1:], "e", ["email","restrict=","input="])
	except getopt.GetoptError, e:
		print 'christmas.py: {0}'.format(str(e))
		sys.exit(2)

	emailConfigFile = 'email_config.json'
	
	# default to no names
	names = []

	# contains eventual assignments
	assignments = {}

	# email addresses to send the assignments to
	sendToAddresses = {}

	# default to not sending an email (testing)
	sendEmail = False

	# default location of people file -- overwritten using --input
	peopleFile = '.\people.json'

	# default to no restrictions
	restrictions = {}
	restrictionStr = None
	# if email is true, the email is sent and results aren't printed to the screen
	for opt, arg in opts:
		if opt in ['-e', '--email']:
			print "Sending email due to opt [{0}]".format(opt)
			sendEmail = True
		elif opt in ['--input']:
			print "Got input file: [{0}]".format(arg)
			peopleFile = arg
		elif opt in ['--restrict']:
			restrictionStr = arg
			print "Got restriction string: [{0}]".format(arg)

	with open(peopleFile) as inputFile:
		# load the input data
		people = json.load(inputFile)

	# parse input data
	for person in people['names']:
		name = person['name']
		emailAddress = person['email']

		if name in names:
			print "Error: duplicate name found in input file: {0}".format(name)
			exit()

		print "Adding [{0}] to the list of names with email [{1}]".format(name, emailAddress)
		names.append(name)

		sendToAddresses[name] = emailAddress

	if restrictionStr is not None:
		try:
			pairings = restrictionStr.split(';')
			for pairing in pairings:
				pair = pairing.split(',')
				restrictions[pair[0]] = pair[1]	
				print '{0} cannot have {1}'.format(pair[0], pair[1])
		except:
			print "Restriction string should be of the form 'GIFT_GETTER1,STOCKING_OWNER1';GIFT_GETTER2,STOCKING_OWNER2' (no trailing semicolon)"
			exit(2)

	if len(names) < 2:
		print "Error: There should be 2 or more people in the list. Length is [{0}]".format(len(names))
		exit()

	success = False
	index = 1

	# loop until success
	while not success:
		success = True
		print "Trying on iteration {0}...".format(index)
		
		# pool of possible assignments
		assignmentPool = copy.deepcopy(names)
		
		#randomize the order
		random.shuffle(assignmentPool)
	
		# for each person, generate assignment
		for person in names:
			# get possible assignment
			stocking = assignmentPool.pop()
	
			# if the name is the same person's name, try to get another name (will always get another name unless there's only one name left 
			if stocking == person:
				# put the bad one back
				assignmentPool.append(stocking)

				# get another one
				stocking = assignmentPool.pop()
		
			checkRestrict = False
			if restrictions != None and restrictions.has_key(person):
				checkRestrict = True
				if stocking == restrictions[person]:
					# put the bad one back
					assignmentPool.append(stocking)

					# get another one
					stocking = assignmentPool.pop()
					
			# if the name is the same here, it means there's no other options left and we have to start over
			if stocking == person:
				success = False
				print "This iteration will fail because {0} got his/her self".format(person)
			elif checkRestrict and stocking == restrictions[person]:
				success = False
				print "This iteration will fail because {0} got {1}, which is restricted".format(person, stocking)
			else:
				assignments[person] = stocking
		index+=1

	# if email, send email and don't print
	if sendEmail:
		for person in sendToAddresses:
			send_email(sendToAddresses[person], emailConfigFile, assignments[person], person)
		print 'Email sent'
	# if not email, print to screen
	else:
		for person in assignments:
			print "{0: <7} --> {1}".format(person, assignments[person])

	# done

# call main
if __name__ == "__main__":
	main(sys.argv[1:])
