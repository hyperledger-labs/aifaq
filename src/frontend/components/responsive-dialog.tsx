import * as React from 'react';

import { Button } from '@/components/ui/button';
import {
	Dialog,
	DialogContent,
	DialogDescription,
	DialogHeader,
	DialogTitle,
	DialogTrigger
} from '@/components/ui/dialog';
import {
	Drawer,
	DrawerClose,
	DrawerContent,
	DrawerDescription,
	DrawerFooter,
	DrawerHeader,
	DrawerTitle,
	DrawerTrigger
} from '@/components/ui/drawer';
import { useWindowSize } from '@/hooks/useWindowSize';

export function ResponsiveDialog({
	children,
	description,
	trigger,
	title
}: {
	trigger: React.ReactNode;
	title: string;
	children: React.ReactNode;
	description: string;
}) {
	const [open, setOpen] = React.useState(false);
	const { isDesktop } = useWindowSize();

	if (isDesktop) {
		return (
			<Dialog open={open} onOpenChange={setOpen}>
				<DialogTrigger asChild>
					{trigger}
				</DialogTrigger>
				<DialogContent className="max-w-xl">
					<DialogHeader>
						<DialogTitle className="font-primary">
							{title}
						</DialogTitle>
						<DialogDescription>
							{description}
						</DialogDescription>
					</DialogHeader>
					{children}
				</DialogContent>
			</Dialog>
		);
	}

	return (
		<Drawer open={open} onOpenChange={setOpen}>
			<DrawerTrigger asChild>
				{trigger}
			</DrawerTrigger>
			<DrawerContent>
				<DrawerHeader className="text-left">
					<DrawerTitle className="font-primary">
						{title}
					</DrawerTitle>
					<DrawerDescription>
						{description}
					</DrawerDescription>
				</DrawerHeader>
				{children}
				<DrawerFooter className="pt-2">
					<DrawerClose asChild>
						<Button variant="outline">
							Cancel
						</Button>
					</DrawerClose>
				</DrawerFooter>
			</DrawerContent>
		</Drawer>
	);
}
