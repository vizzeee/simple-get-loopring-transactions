import requests
import csv

class REST:
	def __init__(self, api_key):
		self.base_url   = 'https://api3.loopring.io'
		self.api_key    = api_key

	def _get_headers(self):
		headers = {
			'Accept'    : 'application/json',
			'X-API-KEY' : self.api_key
		}
		return headers

	def get_user_transfers(self, acc_id, offset):
		url = f'{self.base_url}/api/v3/user/transfers?accountId={acc_id}&offset={offset}'
		return requests.get(url, headers=self._get_headers()).json()

def main():
	API = REST(api_key)
	results = []

	for account_id in account_ids:
		print(f'Account #{account_id} started.')
		data, headers = get_transactions(account_id, API)
		results.append([account_id, headers, data])
		print(f'Account #{account_id} completed.')
	
	save(results)

def save(results):
	if one_file:
		data = []
		for item in results:
			data += item[2]
		save_as_csv('all_accounts', item[1], data)
	else:
		for item in results:
			save_as_csv(f'account_{item[0]}', item[1], item[2])

def get_meta(account_id, API):
	data = API.get_user_transfers(account_id, offset=0)
	entries = data['totalNum']
	headers = [header for header in data['transactions'][0]]
	return entries, headers

def get_transactions(account_id, API):
	entries, headers = get_meta(account_id, API)
	results = []
	i = 0
	while i <= int(entries):
		print(f'Fetching offset {i} of {entries}')
		data = API.get_user_transfers(account_id, offset=i)
		# a transaction has happened after our first query. we dont want duplicates
		if data['totalNum'] != entries:
			print(f'New transaction, offset skipped and updated.')
			i += data['totalNum'] - entries
			entries = data['totalNum']
			continue
		for transaction in data['transactions']:
			row = [value for _, value in transaction.items()]
			results.append(row)

		i += 50
	return results, headers

def save_as_csv(name, headers, data):
	with open(f'{name}.csv', 'w', newline='') as f:
		writer = csv.writer(f)
		writer.writerow(headers)
		writer.writerows(data)

if __name__ == '__main__':
	# Set your api key
	api_key	= ''
	# Set the account ids you wish to download ex [37050, 63124] etc
	account_ids = []
	# save as one file or separate files
	one_file = False

	main()
