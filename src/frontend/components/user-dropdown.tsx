import React from 'react';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import {
	DropdownMenu,
	DropdownMenuContent,
	DropdownMenuItem,
	DropdownMenuLabel,
	DropdownMenuSeparator,
	DropdownMenuTrigger
} from '@/components/ui/dropdown-menu';
import { UserRound } from 'lucide-react';

type Props = {};

const UserDropdown = (props: Props) => {
	return (
		<DropdownMenu>
			<DropdownMenuTrigger asChild>
				<Avatar className="">
					<AvatarImage src="" />
					<AvatarFallback>
						<UserRound />
					</AvatarFallback>
				</Avatar>
			</DropdownMenuTrigger>
			<DropdownMenuContent align="end" className="w-60">
				<DropdownMenuLabel className="flex flex-col">
					<span className="text-base">John Doe</span>
					<span className="text-xs font-normal text-muted-foreground">user@email.com</span>
				</DropdownMenuLabel>
				<DropdownMenuSeparator />
				<DropdownMenuItem>Profile</DropdownMenuItem>
				<DropdownMenuItem>Settings</DropdownMenuItem>
				<DropdownMenuItem>Logout</DropdownMenuItem>
			</DropdownMenuContent>
		</DropdownMenu>
	);
};

export default UserDropdown;
