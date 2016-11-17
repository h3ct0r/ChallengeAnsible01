import re
from concurrent.futures import as_completed, ThreadPoolExecutor
import argparse
from collections import Counter

def process_access_input(lines):
	url_map = Counter()

	for line in lines:
		match = re.search(r"\"(GET|POST)\s+(\/.*) .*\" ([0-9]{3})", line)
		if match:
			request = match.group(2)
			code = match.group(3)
			if request not in url_map.keys():
				url_map[request] = 1
			else:
				url_map[request] += 1
	return url_map

def send_email(emailfrom, emailto, smtp_server, port, username, password, subject, content):
	import smtplib
	import mimetypes
	from email.mime.multipart import MIMEMultipart

	msg = MIMEMultipart()
	msg["From"] = emailfrom
	msg["To"] = emailto
	msg["Subject"] = subject
	msg.preamble = content

	server = smtplib.SMTP("smtp.gmail.com:587")
	server.starttls()
	server.login(username,password)
	server.sendmail(emailfrom, emailto, msg.as_string())
	server.quit()

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--log', required=True)

	parser.add_argument('--email-from', required=True)
	parser.add_argument('--email-to', required=True)
	parser.add_argument('--smtp-server', default='smtp.gmail.com')
	parser.add_argument('--smtp-port', default='587')
	parser.add_argument('--smtp-user', required=True)
	parser.add_argument('--smtp-pass', required=True)


	parser.add_argument('--workers', default=4, type=int)
	parser.add_argument('--buff', default=1024, type=int)
	parser.add_argument('--debug', dest='debug', action='store_true')

	args = parser.parse_args()

	total_requests = Counter()

	with ThreadPoolExecutor(max_workers=args.workers) as executor:

		print '[INFO]', 'Parsing log...', args.log
		print '[INFO]', 'Loading workers...', args.workers
		print '[INFO]', 'Buff size...', args.buff

		f = open(args.log,'r')

		tmp_lines = f.readlines(args.buff)
		while tmp_lines:
			waits = dict()
			for i in xrange(args.workers):
				waits[executor.submit(process_access_input, tmp_lines)] = i
				tmp_lines = f.readlines(args.buff)

			for future in as_completed(waits):
				node = waits[future]
				try:
					w_result = future.result()
					total_requests += w_result # sum Counters
				except Exception as e:
					print '{} generated an exception: {}'.format(node, e)
				else:
					if args.debug:
						print '{}: Result: {}'.format(node, w_result)

	print '\n=== RESULT ==='
	print '\tTotal requests:{}'.format(total_requests)
	if len(total_requests.keys()) > 0:
		subject = 'Daily request report'
		msg = ['Request enumaration of successful requests (http 200):\n']
		for k,v in total_requests.items():
			msg.append('Query:')
			msg.append(k)
			msg.append('size:')
			msg.append(v)
			msg.append('\n')

		print '[INFO]', 'Sending email...'
		send_email(args.email_from, args.email_to, args.smtp_server, args.smtp_port, args.smtp_user, args.smtp_pass, subject, ''.join(msg))
