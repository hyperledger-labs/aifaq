import { SERVER_BASE_URL } from '../const';
import { Message } from '@/lib/types';

export async function handleSend(
	message: Message
) {
	return fetch(SERVER_BASE_URL + '/query', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(message)
	})
		.then((response) => {
			return response.json();
		})
		.catch((err) => {
			console.log(err);
		});
}
