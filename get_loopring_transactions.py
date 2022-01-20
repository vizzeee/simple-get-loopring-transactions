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

def main(api_key, account_ids):
	API = REST(api_key)

	for account_id in account_ids:
		print(f'Account #{account_id} started.')
		data, headers = get_transactions(account_id, API)
		save_as_csv(account_id, headers, data)
		print(f'Account #{account_id} completed.')

def get_meta(account_id, API):
	data = API.get_user_transfers(account_id, offset=0)
	entries = data['totalNum']
	headers = [header for header in data['transactions'][0]]
	return entries, headers

def get_transactions(account_id, API):
	entries, headers = get_meta(account_id, API)
	results = []
	i = 0
	while i < int(entries):
		print(f'Fetching offset {i} of {entries}')
		data = API.get_user_transfers(account_id, offset=i)
		for transaction in data['transactions']:
			row = [value for _, value in transaction.items()]
			results.append(row)

		i += 50
	return results, headers

def save_as_csv(account_id, headers, data):
	with open(f'{account_id}.csv', 'w', newline='') as f:
		writer = csv.writer(f)
		writer.writerow(headers)
		writer.writerows(data)

if __name__ == '__main__':
	# Set your api key
	api_key	= ''
	# Set the account ids you wish to download ex [37050, 63124] etc
	account_ids	= []

	main(api_key, account_ids)
