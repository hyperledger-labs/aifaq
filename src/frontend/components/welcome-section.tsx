'use-client';
import React, {
	useState,
	useEffect
} from 'react';
import { IconHyperledger } from './icons/IconHyperledger';
import { SERVER_BASE_URL } from '@/lib/const';
import { Suspense } from 'react';

type Props = {};

interface Message {
	id: string;
	name: string;
}

const WelcomeSection = (props: Props) => {
	const [messages, setMessages] = useState<
		Message[]
	>([]);

	useEffect(() => {
		async function fetchData() {
			const response = await fetch(
				SERVER_BASE_URL + '/response-keys'
			);
			const data = await response.json();
			setMessages(data);
		}

		fetchData();
	}, []);

	return (
		<>
			<div className="flex h-1/2 flex-col items-center justify-center text-primary space-y-2">
				<IconHyperledger className="w-16 h-16 fill-primary shrink-0" />
			</div>

			<Suspense fallback={<p>Loading....</p>}>
				<div className="grid grid-cols-2 gap-2 p-4">
					{messages.map((user: Message) => (
						<li
							key={user.id}
							className="flex flex-end items-center justify-between p-4 bg-white shadow rounded-lg text-gray-600"
						>
							<div className="flex flex-col space-y-1">
								<h2 className="text-lg font-semibold">
									{user.name}
								</h2>
							</div>
						</li>
					))}
				</div>
			</Suspense>
		</>
	);
};

export default WelcomeSection;
