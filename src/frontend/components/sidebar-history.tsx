'use client';
import React, {
	useEffect,
	useState
} from 'react';
import {
	DropdownMenuCheckboxItemProps,
	DropdownMenuItem
} from '@radix-ui/react-dropdown-menu';
import { Button } from '@/components/ui/button';
import {
	DropdownMenu,
	DropdownMenuCheckboxItem,
	DropdownMenuContent,
	DropdownMenuSeparator,
	DropdownMenuTrigger
} from '@/components/ui/dropdown-menu';
import {
	EllipsisVertical,
	Pencil,
	Pin,
	Trash2
} from 'lucide-react';

// Import the mock data
import { historyData as mockHistoryData } from './history-data';

type Props = {};
type Checked =
	DropdownMenuCheckboxItemProps['checked'];

const SidebarHistory = (props: Props) => {
	const [checkedItems, setCheckedItems] =
		useState<Record<number, Checked>>({});
	const [historyData, setHistoryData] = useState<
		{ id: number; title: string }[]
	>([]);

	useEffect(() => {
		setHistoryData(mockHistoryData);
	}, []);

	const handleCheckedChange = (id: number) => {
		setCheckedItems((prevCheckedItems) => ({
			...prevCheckedItems,
			[id]: !prevCheckedItems[id]
		}));
	};

	

	return (
		<div className="mt-10">
			{historyData.map((item) => (
				<div
					key={item.id}
					className="flex justify-between mt-1 p-3 border-none rounded-lg font-semibold bg-slate-800 hover:bg-slate-800 cursor-pointer"
				>
					<span className="my-auto truncate overflow-hidden whitespace-nowrap">
						{item.title}
					</span>

					<button>
						<DropdownMenu>
							<DropdownMenuTrigger asChild>
								<Button
									variant="outline"
									className="p-0 m-0 text-white bg-slate-800 hover:bg-slate-800 hover:text-white font-semibold border-none"
								>
									<EllipsisVertical />
								</Button>
							</DropdownMenuTrigger>
							<DropdownMenuContent className="w-56">
								<DropdownMenuSeparator />
								<DropdownMenuCheckboxItem
									checked={
										!!checkedItems[item.id]
									}
									onCheckedChange={() =>
										handleCheckedChange(item.id)
									}
								>
									<Pin className="mr-2" /> Pin
								</DropdownMenuCheckboxItem>
								<button className="p-[7px] flex flex-rowtext-left w-full hover:bg-hover-blue border-none hover:border-none ">
									<Pencil className="ml-6" />
									<span className="ml-3">
										Rename
									</span>
								</button>

								<button className="p-[7px] flex flex-rowtext-left w-full hover:bg-hover-blue border-none hover:border-none ">
									<Trash2 className="ml-6" />
									<span className="ml-3">
										Delete
									</span>
								</button>
							</DropdownMenuContent>
						</DropdownMenu>
					</button>
				</div>
			))}
		</div>
	);
};

export default SidebarHistory;
